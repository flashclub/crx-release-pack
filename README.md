# CRX Release Pack

A smart, zero-config Python utility script to package Chrome extensions into `.zip` files for distribution. It automatically sanitizes local development configurations and outputs a clean archive ready for the Chrome Web Store.

[中文文档往下看](#中文文档-zh-cn)

## 🌟 Features

- **Zero Configuration**: Just point it at your extension directory. It automatically extracts the name and version from `manifest.json`.
- **Smart Localization Support**: Automatically resolves `__MSG_name__` to get the correct extension name from your `_locales` directories for naming the output `.zip` file.
- **Localhost Sanitization**: Automatically strips out local development URLs (e.g., `http://localhost:*`, `http://127.0.0.1:*`) from:
  - `host_permissions`
  - `content_scripts[].matches`
  - `externally_connectable.matches`
- **Flexible Exclusions**: Easily ignore specific directories (like `icons`, `assets`, or `node_modules`) from the final build.

## 📦 Installation

This is a standalone Python 3 script. No dependencies (`pip install`) are required! Just download the script and run it.

```bash
git clone https://github.com/your-username/crx-release-pack.git
cd crx-release-pack
```

## 🚀 Usage

```bash
python pack.py <target_dir> [options]
```

### Basic Usage

Package an extension located in the `my-extension` directory. The zip file will be created in the `./dist` folder automatically.

```bash
python pack.py ./my-extension
```

### Specify Output Directory

Use `-o` or `--out-dir` to specify where the `.zip` file should be saved:

```bash
python pack.py ./my-extension -o /path/to/my/builds
```

### Ignore Specific Directories

Use `-i` or `--ignore` to provide a comma-separated list of folder names to exclude from the zip archive:

```bash
python pack.py ./my-extension -i "node_modules,icons,assets"
```

## 🛠 Command Line Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `target_dir` | N/A | **Required.** Path to the extension directory (must contain `manifest.json`). | N/A |
| `--out-dir` | `-o` | Output directory for the `.zip` file. | `./dist` |
| `--ignore` | `-i` | Comma-separated list of directories to ignore. | `""` |

## 📝 License

This project is open-sourced under the MIT License.

---

# 中文文档 (zh-CN)

**CRX Release Pack** 是一个零配置的 Python 脚本，专门用于打包 Chrome 扩展。它能自动读取配置、清理开发环境特有的本地链接，一键生成可以直接上传至 Chrome Web Store 的干净压缩包。

## 🌟 核心特性

- **开箱即用**：无需任何配置，自动从 `manifest.json` 中提取扩展名称和版本号作为压缩包的文件名。
- **支持多语言解析**：如果你的名字是 `__MSG_name__`，它会自动读取 `_locales` 目录下的 `messages.json` 来解析真实的扩展名。
- **自动清理本地调试地址**：在打包过程中，自动剥离以下字段中的本地开发地址（如 `http://localhost:*` 或 `http://127.0.0.1:*`）：
  - `host_permissions`
  - `content_scripts` 里的 `matches`
  - `externally_connectable` 里的 `matches`
- **自定义忽略文件**：支持通过参数轻松忽略不需要被打包的文件夹（比如 `icons`、`assets` 或是本地临时文件夹）。

## 🚀 如何使用

无需安装任何依赖，确保你的电脑上有 Python 3 即可运行。

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
