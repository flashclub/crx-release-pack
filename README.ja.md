# CRX Release Pack

**CRX Release Pack** は、Chrome 拡張機能をパッケージ化するための設定不要な Python スクリプトです。ローカル開発環境の設定を自動的にクリーンアップし、Chrome Web Store にそのままアップロードできるクリーンな `.zip` アーカイブを生成します。

[English](README.md) | [中文文档](README.zh-CN.md) | [한국어](README.ko.md)

## 🌟 主な機能

- **設定不要**: 拡張機能のディレクトリを指定するだけです。`manifest.json` から名前とバージョンを自動的に抽出します。
- **多言語サポート**: `__MSG_name__` が設定されている場合、`_locales` ディレクトリの `messages.json` から正しい拡張機能名を自動的に解決し、出力される `.zip` ファイルの命名に使用します。
- **ローカルホストのサニタイズ**: 以下のフィールドからローカル開発用の URL (例: `http://localhost:*`, `http://127.0.0.1:*`) を自動的に削除します:
  - `host_permissions`
  - `content_scripts` 内の `matches`
  - `externally_connectable` 内の `matches`
- **柔軟な除外設定**: 特定のディレクトリ（`icons`、`assets`、`node_modules` など）を最終ビルドから簡単に除外できます。

## 📦 インストール

これは独立した Python 3 スクリプトです。依存関係のインストール (`pip install`) は不要です。スクリプトをダウンロードして実行するだけです。

```bash
git clone https://github.com/your-username/crx-release-pack.git
cd crx-release-pack
```

## 🚀 使い方

```bash
python pack.py <target_dir> [options]
```

### 基本的な使い方

`my-extension` ディレクトリにある拡張機能をパッケージ化します。zip ファイルは自動的に `./dist` フォルダに作成されます。

```bash
python pack.py ./my-extension
```

### 出力ディレクトリの指定

`-o` または `--out-dir` を使用して、`.zip` ファイルを保存する場所を指定します:

```bash
python pack.py ./my-extension -o /path/to/my/builds
```

### 特定のディレクトリを除外

`-i` または `--ignore` を使用して、zip アーカイブから除外するフォルダ名のカンマ区切りリストを指定します:

```bash
python pack.py ./my-extension -i "node_modules,icons,assets"
```

## 🛠 コマンドライン引数

| 引数 | 省略形 | 説明 | デフォルト |
|----------|-------|-------------|---------|
| `target_dir` | なし | **必須。** 拡張機能ディレクトリのパス (`manifest.json` を含む必要があります)。 | なし |
| `--out-dir` | `-o` | `.zip` ファイルの出力ディレクトリ。 | `./dist` |
| `--ignore` | `-i` | 除外するディレクトリのカンマ区切りリスト。 | `""` |

## 📝 ライセンス

このプロジェクトは MIT ライセンスの下でオープンソース化されています。
