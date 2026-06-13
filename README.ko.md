# CRX Release Pack

**CRX Release Pack**은 Chrome 확장 프로그램을 배포용 `.zip` 파일로 패키징하기 위한 설정이 필요 없는 Python 유틸리티 스크립트입니다. 로컬 개발 환경 설정을 자동으로 정리하여 Chrome 웹 스토어에 바로 업로드할 수 있는 깨끗한 아카이브를 생성합니다.

[English](README.md) | [中文文档](README.zh-CN.md) | [日本語](README.ja.md)

## 🌟 주요 기능

- **설정 필요 없음**: 확장 프로그램 디렉토리를 지정하기만 하면 됩니다. `manifest.json`에서 이름과 버전을 자동으로 추출합니다.
- **다국어 지원**: `__MSG_name__`이 있는 경우, `_locales` 디렉토리의 `messages.json`에서 올바른 확장 프로그램 이름을 자동으로 해석하여 출력되는 `.zip` 파일의 이름으로 사용합니다.
- **로컬호스트 정리**: 다음 필드에서 로컬 개발용 URL(예: `http://localhost:*`, `http://127.0.0.1:*`)을 자동으로 제거합니다:
  - `host_permissions`
  - `content_scripts` 내의 `matches`
  - `externally_connectable` 내의 `matches`
- **유연한 제외 설정**: 최종 빌드에서 특정 디렉토리(`icons`, `assets`, `node_modules` 등)를 쉽게 제외할 수 있습니다.

## 📦 설치

이 스크립트는 독립적인 Python 3 스크립트입니다. 의존성 설치(`pip install`)가 필요하지 않습니다! 스크립트를 다운로드하고 실행하기만 하면 됩니다.

```bash
git clone https://github.com/your-username/crx-release-pack.git
cd crx-release-pack
```

## 🚀 사용법

```bash
python pack.py <target_dir> [options]
```

### 기본 사용법

`my-extension` 디렉토리에 있는 확장 프로그램을 패키징합니다. zip 파일은 자동으로 `./dist` 폴더에 생성됩니다.

```bash
python pack.py ./my-extension
```

### 출력 디렉토리 지정

`-o` 또는 `--out-dir`을 사용하여 `.zip` 파일이 저장될 위치를 지정합니다:

```bash
python pack.py ./my-extension -o /path/to/my/builds
```

### 특정 디렉토리 제외

`-i` 또는 `--ignore`를 사용하여 zip 아카이브에서 제외할 폴더 이름의 쉼표로 구분된 목록을 제공합니다:

```bash
python pack.py ./my-extension -i "node_modules,icons,assets"
```

## 🛠 명령줄 인수

| 인수 | 약어 | 설명 | 기본값 |
|----------|-------|-------------|---------|
| `target_dir` | 없음 | **필수.** 확장 프로그램 디렉토리 경로 (`manifest.json`이 포함되어야 함). | 없음 |
| `--out-dir` | `-o` | `.zip` 파일의 출력 디렉토리. | `./dist` |
| `--ignore` | `-i` | 제외할 디렉토리의 쉼표로 구분된 목록. | `""` |

## 📝 라이선스

이 프로젝트는 MIT 라이선스에 따라 오픈 소스로 공개됩니다.
