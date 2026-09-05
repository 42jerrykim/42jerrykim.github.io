---
draft: false
collection_order: 2
slug: git-install-config-user-setup
title: "[Git] 02. Git 설치와 최초 설정 — git config"
date: 2026-09-04
lastmod: 2026-09-04
description: "Windows·macOS·Linux에 Git을 설치하는 방법과, git config의 system/global/local 3단계 우선순위, 이름·이메일·기본 편집기·alias를 설정하는 최초 설정 절차를 정리한 Git 입문 챕터다."
categories:
- Git
tags:
- Git
- GitHub
- Version-Control(버전관리)
- Configuration(설정)
- Terminal
- Installation
- Cross-Platform
- Windows(윈도우)
- macOS
- Linux(리눅스)
- Guide(가이드)
- Education(교육)
- Beginner
- Productivity(생산성)
- Documentation(문서화)
- Quick-Reference
- Best-Practices
- Comparison(비교)
- Reference(참고)
- How-To
- Tips
- Troubleshooting(트러블슈팅)
- WinGet
- Homebrew
- Package-Manager
- DevOps
- Workflow(워크플로우)
image: "wordcloud.png"
---

Git을 설치한 직후 첫 커밋을 시도하면 "Please tell me who you are"라는 오류를 만나게 된다. Git이 모든 커밋에 작성자 이름과 이메일을 기록하도록 요구하기 때문인데, 이 설정을 어디에(시스템 전체·사용자 전체·저장소 하나) 해두느냐에 따라 나중에 여러 프로젝트를 오갈 때 결과가 달라진다. 이 장은 설치 방법과 `git config`의 우선순위를 다룬다.

## 개요

Git 설치 방법은 운영체제마다 다르며, 상황에 따라 권장되는 방식도 갈린다.

| 운영체제 | 설치 방법 |
|---|---|
| Windows | WinGet, 공식 설치 프로그램(Git for Windows), Chocolatey |
| macOS | Xcode Command Line Tools, Homebrew |
| Linux(Debian/Ubuntu 계열) | APT 패키지 관리자(`apt`) |
| Linux(RHEL/Fedora 계열) | DNF/YUM 패키지 관리자 |

Windows에서는 WinGet이 가장 간단하다.

```powershell
winget install --id Git.Git -e --source winget
```

macOS는 Homebrew를 쓰거나, 터미널에서 `git` 명령을 처음 실행하면 Xcode Command Line Tools 설치를 안내하는 대화상자가 뜬다.

```bash
brew install git
```

Debian·Ubuntu 계열 Linux는 APT로 설치한다.

```bash
sudo apt update && sudo apt install git
```

설치가 끝나면 버전을 확인해 정상적으로 PATH에 등록됐는지 검증한다.

```bash
git --version
```

## 기본 개념

Git 설정은 `git config` 명령으로 관리하며, 설정값은 적용 범위에 따라 3단계로 나뉘고 좁은 범위가 넓은 범위를 덮어쓴다.

| 단계 | 옵션 | 저장 위치 | 적용 범위 |
|---|---|---|---|
| system | `--system` | Git 설치 디렉터리의 `gitconfig` | 해당 컴퓨터의 모든 사용자 |
| global | `--global` | 사용자 홈 디렉터리의 `~/.gitconfig` | 해당 사용자의 모든 저장소 |
| local | (옵션 없음, 기본값) | 저장소 안의 `.git/config` | 해당 저장소 하나만 |

이 우선순위 때문에 회사용 이메일과 개인용 이메일을 프로젝트별로 다르게 쓰고 싶다면, 전역 설정에는 기본값(개인 이메일)을 두고 특정 저장소 안에서만 `--local`로 다시 설정하면 된다. 지금 어떤 값이 어느 단계에서 왔는지 확인하려면 `--show-origin` 옵션을 함께 쓴다.

```bash
git config --global user.name "Jerry Kim"
git config --global user.email "user@example.com"
git config --list --show-origin
```

## 종류/세부

### 자주 설정하는 항목

이름·이메일 외에도 실무에서 자주 바꾸는 설정이 몇 가지 있다.

```bash
git config --global core.editor "code --wait"     # 커밋 메시지를 작성할 기본 편집기
git config --global init.defaultBranch main        # git init 시 기본 브랜치 이름
git config --global core.autocrlf true             # Windows에서 줄바꿈 자동 변환(입력 시 LF, 체크아웃 시 CRLF)
git config --global pull.rebase false               # git pull 시 merge/rebase 기본 동작
```

`core.autocrlf`는 Windows·macOS·Linux 팀원이 섞인 저장소에서 줄바꿈 문자(CRLF vs LF)로 인한 불필요한 diff를 줄이는 데 쓴다. Windows에서는 `true`(체크아웃 시 CRLF로 변환, 커밋 시 LF로 저장), macOS·Linux에서는 `input`(커밋 시에만 LF로 정규화)이 일반적으로 권장되는 값이다.

### alias로 자주 쓰는 명령 줄이기

`git config`의 `alias.*` 네임스페이스를 쓰면 자주 쓰는 긴 명령을 짧은 이름으로 줄일 수 있다.

```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.lg "log --oneline --graph --all"
```

이렇게 설정하면 `git st`가 `git status`와 동일하게 동작한다. alias는 `.gitconfig` 파일에 저장되므로, 여러 컴퓨터에서 같은 alias 세트를 쓰고 싶다면 `.gitconfig` 파일 자체를 dotfiles 저장소로 관리하는 방법도 흔히 쓰인다.

## 주의사항·함정

**`--global` 없이 설정하면 저장소 하나에만 적용된다**: 옵션 없이 `git config user.name "..."`을 실행하면 현재 디렉터리가 Git 저장소일 때 `.git/config`(local)에 저장된다. 새 컴퓨터에서 다른 프로젝트를 클론했는데 이름·이메일이 비어 있다면, 이전에 `--global` 없이 설정했을 가능성이 크다.

**회사·개인 이메일 혼용 실수**: `--global`로 회사 이메일을 설정해두고 개인 오픈소스 프로젝트에 커밋하면, 공개 저장소의 커밋 이력에 회사 이메일이 그대로 노출된다. 이미 커밋된 이력의 이메일을 바꾸려면 단순 설정 변경으로는 부족하고 히스토리 재작성이 필요하므로(27장의 인터랙티브 리베이스), 애초에 프로젝트 성격에 맞는 이메일을 `--local`로 먼저 확인하는 습관이 필요하다.

**`core.autocrlf` 설정 없이 팀에 합류하면 불필요한 diff가 쌓인다**: 이미 LF로 통일된 저장소에 `core.autocrlf` 설정이 없는 Windows 환경에서 파일을 저장하면, 편집기 설정에 따라 줄바꿈이 CRLF로 바뀌어 실제 코드 변경이 없는데도 파일 전체가 변경된 것처럼 diff에 나타날 수 있다. 저장소에 `.gitattributes`(40장)로 줄바꿈 규칙이 명시되어 있다면 그 규칙을 우선 따른다.

## Reference

- [Getting Started - Installing Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [git-config Documentation](https://git-scm.com/docs/git-config)
