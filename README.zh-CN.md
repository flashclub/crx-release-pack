# CRX Release Pack

**CRX Release Pack** 是一个零配置的 Python 脚本，专门用于打包 Chrome 扩展。它能自动读取配置、清理开发环境特有的本地链接，一键生成可以直接上传至 Chrome Web Store 的干净压缩包。

[English](README.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

## 🌟 核心特性

- **开箱即用**：无需任何配置，自动从 `manifest.json` 中提取扩展名称和版本号作为压缩包的文件名。
- **支持多语言解析**：如果你的名字是 `__MSG_name__`，它会自动读取 `_locales` 目录下的 `messages.json` 来解析真实的扩展名。
- **自动清理本地调试地址**：在打包过程中，自动剥离以下字段中的本地开发地址（如 `http://localhost:*` 或 `http://127.0.0.1:*`）：
  - `host_permissions`
  - `content_scripts` 里的 `matches`
  - `externally_connectable` 里的 `matches`
- **自定义忽略文件**：支持通过参数轻松忽略不需要被打包的文件夹（比如 `icons`、`assets` 或是本地临时文件夹）。

## 📦 安装

无需安装任何依赖，确保你的电脑上有 Python 3 即可运行。

```bash
git clone https://github.com/your-username/crx-release-pack.git
cd crx-release-pack
```

## 🚀 如何使用

**基础打包：**
```bash
python pack.py 你的扩展目录路径
```

**指定输出路径** (`-o`)：
```bash
python pack.py ./my-extension -o /Users/me/desktop/builds
```

**忽略特定文件夹** (`-i`)：
```bash
python pack.py ./my-extension -i "node_modules,icons,tmp"
```

## 🛠 命令行参数

| 参数 | 缩写 | 说明 | 默认值 |
|----------|-------|-------------|---------|
| `target_dir` | 无 | **必填。** 扩展目录路径（必须包含 `manifest.json`）。 | 无 |
| `--out-dir` | `-o` | `.zip` 压缩包的输出目录。 | `./dist` |
| `--ignore` | `-i` | 逗号分隔的忽略文件夹列表。 | `""` |

## 📝 许可证

本项目基于 MIT 许可证开源。
