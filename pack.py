#!/usr/bin/env python3
"""
Chrome Extension Packager

A utility script to package Chrome extensions into a zip file for distribution.
It automatically:
- Reads the manifest.json to determine the version and name.
- Resolves localized names (__MSG_name__) if present.
- Strips out localhost URLs from host_permissions, content_scripts, and externally_connectable.
- Generates a clean .zip file ready for the Chrome Web Store.
"""

import os
import json
import re
import zipfile
import argparse

LOCALHOST_MATCH_PREFIXES = (
    'http://localhost',
    'https://localhost',
    'http://127.0.0.1',
    'https://127.0.0.1',
)

GENERIC_PROJECT_DIR_NAMES = {'extension', 'chrome-extension', 'src'}

def slugify(value, fallback='extension'):
    slug = re.sub(r'[^a-z0-9]+', '-', str(value).lower()).strip('-')
    return slug or fallback

def get_project_fallback_name(project_dir):
    name = os.path.basename(project_dir)
    if name in GENERIC_PROJECT_DIR_NAMES:
        parent_name = os.path.basename(os.path.dirname(project_dir))
        return parent_name or name
    return name

def get_locale_candidates(manifest, project_dir):
    candidates = []
    default_locale = manifest.get('default_locale')
    if default_locale:
        candidates.append(default_locale)

    for fallback_locale in ('en', 'en_US'):
        if fallback_locale not in candidates:
            candidates.append(fallback_locale)

    locales_dir = os.path.join(project_dir, '_locales')
    if os.path.isdir(locales_dir):
        for locale_name in sorted(os.listdir(locales_dir)):
            if locale_name not in candidates:
                candidates.append(locale_name)

    return candidates

def resolve_manifest_message(raw_value, manifest, project_dir):
    if not isinstance(raw_value, str):
        return None

    match = re.fullmatch(r'__MSG_([A-Za-z0-9_@]+)__', raw_value.strip())
    if not match:
        return raw_value

    message_key = match.group(1)
    for locale_name in get_locale_candidates(manifest, project_dir):
        messages_path = os.path.join(project_dir, '_locales', locale_name, 'messages.json')
        if not os.path.exists(messages_path):
            continue

        try:
            with open(messages_path, 'r', encoding='utf-8') as f:
                messages = json.load(f)
        except Exception:
            continue

        message = messages.get(message_key, {}).get('message')
        if message:
            return message

    return None

def is_localhost_match(pattern):
    return any(pattern.startswith(prefix) for prefix in LOCALHOST_MATCH_PREFIXES)

def strip_localhost_manifest_entries(manifest):
    sanitized = json.loads(json.dumps(manifest))

    if isinstance(sanitized.get('host_permissions'), list):
        sanitized['host_permissions'] = [
            pattern for pattern in sanitized['host_permissions']
            if not is_localhost_match(pattern)
        ]
        if not sanitized['host_permissions']:
            sanitized.pop('host_permissions')

    if 'externally_connectable' in sanitized and isinstance(sanitized['externally_connectable'].get('matches'), list):
        sanitized['externally_connectable']['matches'] = [
            pattern for pattern in sanitized['externally_connectable']['matches']
            if not is_localhost_match(pattern)
        ]
        if not sanitized['externally_connectable']['matches']:
            sanitized.pop('externally_connectable')

    if 'content_scripts' in sanitized:
        scripts = []
        for script in sanitized['content_scripts']:
            if isinstance(script.get('matches'), list):
                script['matches'] = [
                    pattern for pattern in script['matches']
                    if not is_localhost_match(pattern)
                ]
                if script['matches']:
                    scripts.append(script)
            else:
                scripts.append(script)
        sanitized['content_scripts'] = scripts
        if not sanitized['content_scripts']:
            sanitized.pop('content_scripts')

    return sanitized

def pack_extension(target_dir, out_dir=None, ignore_dirs=None):
    if ignore_dirs is None:
        ignore_dirs = set()
        
    # Default security exclusions to prevent leaking source/secrets
    default_ignores = {'.git', '.svn', '.vscode', '.idea', '__MACOSX', 'node_modules', '.DS_Store'}
    ignore_dirs.update(default_ignores)

    project_dir = os.path.abspath(target_dir)
    
    if out_dir:
        dist_dir = os.path.abspath(out_dir)
    else:
        dist_dir = os.path.join(os.getcwd(), 'dist')
        
    manifest_path = os.path.join(project_dir, 'manifest.json')

    print(f"🚀 开始打包 (Start packaging)...")

    if not os.path.isdir(project_dir):
        print(f"❌ 错误: 目标目录 {project_dir} 不存在")
        return

    # 1. 检查并读取 manifest.json
    if not os.path.exists(manifest_path):
        print(f"❌ 错误: 在目标目录中找不到 manifest.json")
        return

    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
            version = manifest.get('version', 'unknown')
            fallback_name = get_project_fallback_name(project_dir)
            resolved_name = resolve_manifest_message(manifest.get('name'), manifest, project_dir)
            name = slugify(resolved_name or fallback_name, slugify(fallback_name))
    except Exception as e:
        print(f"❌ 解析 manifest.json 失败: {e}")
        return

    # 2. 创建 dist 目录
    if not os.path.exists(dist_dir):
        os.makedirs(dist_dir)
        print(f"📂 已创建输出目录: {dist_dir}")

    # 3. 准备压缩包名称
    zip_filename = f"{name}_v{version}.zip"
    zip_path = os.path.join(dist_dir, zip_filename)

    # 4. 执行打包
    print(f"📦 正在打包 {name} v{version}...")
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(project_dir):
                # Prevent packaging the dist directory itself if it's inside the target_dir
                if os.path.abspath(root) == dist_dir:
                    dirs[:] = []
                    continue
                    
                dirs[:] = [d for d in dirs if d not in ignore_dirs]
                for file in files:
                    if file in ignore_dirs:
                        continue
                        
                    file_path = os.path.join(root, file)
                    
                    # Prevent packaging the target zip file if it's somehow inside the walk tree
                    if os.path.abspath(file_path) == zip_path:
                        continue
                        
                    # Calculate relative path and ensure forward slashes for ZIP spec (Windows fix)
                    arcname = os.path.relpath(file_path, project_dir)
                    arcname = arcname.replace(os.sep, '/')
                    if arcname == 'manifest.json':
                        release_manifest = strip_localhost_manifest_entries(manifest)
                        zipf.writestr(
                            arcname,
                            json.dumps(release_manifest, ensure_ascii=False, indent=2) + '\n'
                        )
                        print(f"  + {arcname} (localhost entries removed)")
                        continue
                    zipf.write(file_path, arcname)
                    print(f"  + {arcname}")

        print(f"\n✅ 打包成功!")
        print(f"📍 文件位置: {zip_path}")
        
    except Exception as e:
        print(f"❌ 打包过程中出错: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Package a Chrome Extension into a ready-to-publish ZIP file.")
    parser.add_argument("target_dir", help="Path to the extension directory (must contain manifest.json)")
    parser.add_argument("-o", "--out-dir", help="Output directory for the zip file (default: ./dist)", default=None)
    parser.add_argument("-i", "--ignore", help="Comma-separated list of directories to ignore (e.g. 'icons,assets')", default="")
    
    args = parser.parse_args()
    
    ignore_set = set(filter(bool, args.ignore.split(',')))
    
    pack_extension(args.target_dir, out_dir=args.out_dir, ignore_dirs=ignore_set)
