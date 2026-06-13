# CRX Release Pack

A smart, zero-config Python utility script to package Chrome extensions into `.zip` files for distribution. It automatically sanitizes local development configurations and outputs a clean archive ready for the Chrome Web Store.

[中文文档](README.zh-CN.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

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
