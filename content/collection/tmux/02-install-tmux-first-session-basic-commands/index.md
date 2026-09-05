---
draft: false
slug: install-tmux-first-session-basic-commands
title: "[Tmux] 02. 설치와 첫 세션 - 기본 명령과 실행 흐름"
description: "Debian/Ubuntu apt, macOS Homebrew, Fedora dnf, 소스 빌드까지 운영체제별 tmux 설치 방법과 libevent·ncurses 의존성을 정리하고, tmux를 처음 실행했을 때 서버·세션이 자동으로 만들어지는 흐름을 다룹니다."
date: 2026-09-04
lastmod: 2026-09-06
collection_order: 2
categories:
- Tmux
tags:
- Tmux
- Terminal
- Linux(리눅스)
- macOS
- Shell(셸)
- Session(세션)
- Process
- Compiler(컴파일러)
- OS(운영체제)
- SSH(Secure Shell)
- DevOps
- Education(교육)
- Curriculum(커리큘럼)
- Tutorial(튜토리얼)
- Guide(가이드)
- How-To
- Tips
- Reference(참고)
- Beginner
- Advanced
- Best-Practices
- Documentation(문서화)
- Workflow(워크플로우)
- Environment
- Version-Control(버전관리)
image: "wordcloud.png"
---

01장에서 tmux가 서버-클라이언트 구조로 동작한다는 것을 배웠다면, 이 장은 그 서버를 실제로 자신의 컴퓨터·서버에 설치하고 처음 실행해 보는 단계다. 운영체제별 설치 방법, 소스에서 직접 빌드하는 법, 그리고 `tmux`를 옵션 없이 실행했을 때 서버·세션이 자동으로 만들어지는 흐름을 다룬다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [01장: tmux란 무엇인가](/post/tmux/what-is-tmux-terminal-multiplexer-architecture/)에서 다룬 서버-클라이언트 구조를 실제로 손에 쥐어보는 단계다. 01장의 서버-클라이언트 개념을 알고 있다는 전제로 서술한다.

**이 장의 깊이**: **입문** 난이도다. **다루지 않는 것**: 이름을 붙인 세션을 여러 개 만들고 오가며 관리하는 방법은 03장에서, 윈도우·패널을 나누고 옮기는 조작은 04장에서, `tmux.conf`로 동작을 바꾸는 설정 문법은 2부(05–08장)에서 각각 다룬다. 이 장은 "설치가 끝났다"와 "tmux가 실행됐다"를 확인하는 데서 멈춘다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| tmux를 처음 설치하는 완전 초보자 | 설치, 설치 확인과 첫 실행 | 자신의 운영체제에 맞는 방법으로 tmux를 설치하고 첫 세션을 실행할 수 있다 |
| 이미 tmux가 설치된 환경에서 배우기 시작한 사람 | 설치 확인과 첫 실행, 흔한 오개념 | 지금 실행 중인 tmux의 버전과 서버 상태를 명령으로 직접 확인할 수 있다 |
| 오래된 배포판·구형 서버를 관리하는 사람 | 소스에서 빌드하기, 비교/트레이드오프 | 패키지 저장소 버전이 오래돼 필요한 기능이 빠졌을 때 소스 빌드로 대응할 수 있다 |
| 팀 온보딩 문서를 작성하려는 사람 | 설치(전체 표), 주의사항·함정 | 여러 운영체제를 아우르는 설치 가이드를 정리할 수 있다 |

## 설치

대부분의 상황에서는 운영체제의 패키지 매니저로 설치하는 쪽이 낫다. 의존성을 자동으로 해결해 주고, 이후 배포판·시스템을 업데이트할 때 tmux도 함께 최신 보안 패치를 받기 때문이다. tmux는 OpenBSD·FreeBSD·NetBSD·Linux·macOS·Solaris에서 동작하며, 패키지 이름은 대부분의 배포판에서 동일하게 `tmux`다.

| 운영체제 | 설치 명령 | 비고 |
|---|---|---|
| Debian / Ubuntu | `sudo apt update && sudo apt install tmux` | APT 저장소 버전은 배포판 릴리스 주기를 따르므로 다소 오래될 수 있다 |
| Fedora / RHEL / CentOS | `sudo dnf install tmux` | 구형 배포판은 `dnf` 대신 `yum install tmux` |
| Arch Linux | `sudo pacman -S tmux` | 롤링 릴리스라 비교적 최신 버전이 유지된다 |
| macOS | `brew install tmux` | macOS에는 기본 탑재돼 있지 않아 Homebrew가 필요하다 |
| Windows | (네이티브 지원 없음) WSL 설치 후 그 안에서 위 리눅스 배포판별 명령 사용 | WSL(Windows Subsystem for Linux)이 사실상 유일한 경로다 |

배포판마다 패키지 매니저 명령이 다른 이유는 각 시스템이 패키지를 저장·색인하는 방식 자체가 다르기 때문이다. Debian 계열은 `.deb` 패키지를 APT 저장소에서, Fedora/RHEL 계열은 `.rpm` 패키지를 DNF(또는 구형 시스템은 YUM) 저장소에서, Arch Linux는 롤링 릴리스 특성상 저장소를 거의 실시간으로 최신 상태로 유지하는 pacman에서 각각 받아온다. macOS는 애초에 시스템 패키지 매니저가 없어 Homebrew 같은 서드파티 도구가 그 역할을 대신하고, Windows는 네이티브 POSIX 환경이 아니므로 WSL로 리눅스 배포판을 통째로 올린 뒤 그 안에서 위 방법을 그대로 쓰는 우회 경로만 남는다.

## 소스에서 빌드하기

패키지 저장소의 tmux가 너무 오래돼 이후 챕터에서 다루는 기능(예: 08장의 확장 상태바 포맷)을 지원하지 않을 때는 소스에서 직접 빌드한다. tmux는 <strong>libevent 2.x</strong>와 <strong>ncurses</strong> 라이브러리에 의존하며, 빌드에는 C 컴파일러(gcc·clang 등)와 `make`, `pkg-config`, `yacc` 또는 `bison`이 필요하다.

```bash
# 릴리스 tarball을 내려받아 빌드하는 경우
./configure && make
sudo make install

# 저장소에서 최신 개발 버전을 직접 빌드하는 경우
# (autoconf, automake, pkg-config가 추가로 필요하다)
git clone https://github.com/tmux/tmux.git
cd tmux
sh autogen.sh
./configure && make
sudo make install
```

`sudo` 권한이 없는 공유 서버라면 `./configure --prefix=$HOME/.local`처럼 사용자 홈 디렉터리 아래에 설치 경로를 지정하고, `make install`(sudo 없이) 뒤 `$HOME/.local/bin`을 `PATH`에 추가하는 방식으로 우회할 수 있다.

## 설치 확인과 첫 실행

설치가 끝나면 버전을 확인하고, 옵션 없이 `tmux`를 실행해 무슨 일이 일어나는지 관찰한다.

```bash
# 설치된 버전 확인
tmux -V
# 예: tmux 3.4
```

01장에서 배운 서버-클라이언트 구조를 떠올려 보면, 아래 명령이 왜 이렇게 동작하는지 설명할 수 있다.

```bash
# 아무 옵션 없이 실행하면: 서버가 없으면 새로 띄우고,
# 이름을 지정하지 않은 새 세션을 만들어 그 안으로 즉시 들어간다
tmux

# (세션 안에서) 서버가 이 세션을 실제로 관리하고 있는지 확인
tmux ls
# 예: 0: 1 windows (created ...)  -- 이름을 지정하지 않으면 0부터 정수 이름이 자동으로 붙는다
```

이름 없이 만든 세션은 `tmux ls` 결과에서 숫자로만 구분되므로, 세션을 여러 개 오가야 하는 상황이라면 처음부터 이름을 붙이는 쪽이 낫다. 이름 붙이기·전환은 03장의 주제지만, 이 장에서는 세션을 만드는 시점에 이름을 지정하는 방법과 화면에 붙지 않고 백그라운드에만 만드는 방법까지만 다룬다.

```bash
# 이름을 지정해 세션을 만들면 tmux ls 결과가 훨씬 읽기 쉬워진다
tmux new -s work

# 만들자마자 화면에 붙지(attach) 않고 백그라운드에 남겨두려면 -d
tmux new -s batch -d

# 세션 안의 셸을 정상 종료하면(exit) 그 세션 자체도 함께 사라진다
exit
```

## 비교/트레이드오프

패키지 매니저 설치와 소스 빌드 중 무엇을 선택할지는 상황에 따라 갈린다.

| 구분 | 패키지 매니저(apt/brew/dnf 등) | 소스 빌드 |
|---|---|---|
| 설치 속도 | 명령 한 줄, 의존성 자동 해결 | 의존성을 직접 준비하고 빌드 시간이 든다 |
| 버전 | 배포판 릴리스 주기를 따름(다소 오래될 수 있음) | 항상 최신(개발 버전까지 선택 가능) |
| 업데이트 | 배포판 업데이트에 자동으로 묻어옴 | 새 버전이 나올 때마다 수동으로 다시 빌드해야 함 |
| 적합한 상황 | 대부분의 로컬 환경과 서버 | 최신 기능이 꼭 필요하거나 패키지가 아예 없는 환경 |

안정성이 중요한 프로덕션 서버나 여러 명이 함께 쓰는 공용 환경이라면, 버전이 다소 오래되더라도 배포판이 검증한 패키지 매니저 설치가 유지보수 부담을 훨씬 줄여준다. 반대로 이후 챕터에서 다루는 최신 기능이 꼭 필요하거나 배포판 저장소에 아예 tmux가 없는 환경이라면, 빌드 시간을 감수하고 소스 빌드를 택하는 것이 유일한 선택지가 된다.

## 주의사항·함정

**macOS는 기본 탑재가 아니다**: Xcode나 macOS 자체에 tmux가 포함돼 있지 않으므로, Homebrew 없이 tmux를 쓸 수는 없다(또는 소스 빌드).

**LTS 배포판의 오래된 버전**: Ubuntu LTS 같은 장기 지원 배포판은 릴리스 시점의 tmux 버전을 몇 년씩 그대로 유지하는 경우가 흔하다. 이후 챕터에서 소개하는 기능(플러그인 생태계가 요구하는 최소 버전 등)이 동작하지 않는다면 가장 먼저 `tmux -V`로 버전을 확인해야 한다.

**원격 서버 설치 시 권한**: SSH로 접속한 서버에 `sudo` 권한이 없다면 패키지 매니저 설치 자체가 막힌다. 이럴 때는 앞서 설명한 `--prefix`를 사용자 홈 디렉터리로 지정하는 소스 빌드가 유일한 대안이 되는 경우가 많다.

## 흔한 오개념

<strong>"tmux를 실행할 때마다 매번 새 서버가 뜬다"</strong>는 생각은 01장에서 배운 서버-클라이언트 구조와 어긋난다. 서버는 이미 떠 있으면 재사용되고, `tmux`를 옵션 없이 다시 실행하면 그 위에 이름 없는 세션이 하나 더 추가될 뿐이다.

<strong>"패키지 매니저로 설치하면 항상 최신 버전이 깔린다"</strong>는 오해도 흔하다. Debian·Ubuntu LTS처럼 안정성을 우선하는 배포판은 릴리스 당시 버전을 오래 고정하는 경우가 많아, 최신 GitHub 릴리스와 몇 단계 차이가 날 수 있다.

<strong>"설치가 끝나면 별도 설정이 필요하다"</strong>는 오해도 있다. tmux는 `tmux.conf`가 전혀 없어도 기본 키바인딩과 기본 동작만으로 바로 쓸 수 있다 — 다만 그 기본값이 매우 미니멀해서, 상태바 색상이나 편의 기능은 2부에서 다루는 설정을 거쳐야 눈에 띄게 나아진다.

## 다음 장에서는

[03장: 세션(Session) 다루기 - 생성·접속·분리·종료](/post/tmux/tmux-session-new-attach-detach-kill/)에서는 이 장에서 만든 이름 없는 세션을 넘어, 여러 세션을 이름으로 구분해 만들고 전환·종료하는 법을 다룬다.

## 평가 기준

이 장을 읽은 후 다음을 할 수 있어야 한다.

- 자신의 운영체제에 맞는 tmux 설치 방법을 선택하고 실행할 수 있다.
- 패키지 매니저 설치와 소스 빌드의 트레이드오프를 설명하고, 상황에 맞게 하나를 선택할 수 있다.
- `tmux`를 옵션 없이 실행했을 때 서버-클라이언트 구조상 어떤 일이 일어나는지 01장 개념과 연결해 설명할 수 있다.
- `-s`(이름 지정)와 `-d`(detached로 생성) 옵션이 세션 생성 방식을 어떻게 바꾸는지 설명할 수 있다.
- `tmux -V`, `tmux ls`로 설치된 버전과 서버 상태를 직접 확인할 수 있다.

## 참고 및 출처

1. [tmux/tmux](https://github.com/tmux/tmux) — README의 의존성(libevent, ncurses)·빌드 절차 설명.
2. [tmux(1) - OpenBSD Manual](https://man.openbsd.org/tmux) — `new-session`, `-d` 옵션 등 공식 명령 설명.
