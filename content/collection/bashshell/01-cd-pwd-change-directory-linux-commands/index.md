---
draft: false
slug: cd-pwd-change-directory-linux-commands
title: "[Bash Shell] 01. cd, pwd - 디렉터리 이동과 현재 위치"
description: "셸이 항상 유지하는 숨은 상태인 현재 작업 디렉터리(cwd) 개념을 중심으로 cd와 pwd의 옵션·상대경로 해석 방식을 정리하고, cd -와 OLDPWD, CDPATH의 부작용, 심볼릭 링크에서 -L/-P 경로 해석 차이를 GNU Bash 매뉴얼 기준으로 다룹니다."
date: 2026-03-15
lastmod: 2026-08-22
collection_order: 10
categories:
- Bash Shell
tags:
- Bash
- Shell(셸)
- Linux(리눅스)
- Terminal
- Command
- File-System
- Process
- Automation(자동화)
- Environment
- OS(운영체제)
- Guide(가이드)
- Tutorial(튜토리얼)
- Reference(참고)
- Quick-Reference
- Beginner
- How-To
- Tips
- cd
- pwd
- PWD(Print Working Directory)
- OLDPWD
- CDPATH
- 디렉터리
- 경로
- 작업디렉터리
- current-directory
- 홈디렉터리
- 심볼릭링크
- 상대경로
- 절대경로
image: "wordcloud.png"
---

`cd`(change directory)는 셸의 **작업 디렉터리**를 바꾸는 내장 명령이고, `pwd`(print working directory)는 그 작업 디렉터리의 절대 경로를 출력한다. 이 두 명령은 셸이 항상 붙들고 있는 단 하나의 숨은 상태 — 지금 내가 "어디에" 있는가 — 를 확인하고 옮기는 가장 기본적인 도구이며, 이 상태를 이해하지 못하면 이후 챕터에서 다룰 상대경로 기반의 파일 조작·스크립트 전체가 헷갈리기 시작한다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [00장: 과정 개요와 커리큘럼](/post/bashshell/getting-started-bash-shell/) 바로 다음에 오는 <strong>Part 1(셸 기초와 탐색)</strong>의 첫 기술 챕터다. 셸을 처음 열어 명령을 입력할 수 있다는 것 외에 별도로 전제하는 지식은 없다.

**이 장의 깊이**: **입문** 난이도다. 경로 지정 방식(절대·상대·홈·이전 디렉터리)과 `cd`/`pwd`의 옵션을 실무에서 쓰는 범위까지 다룬다. **다루지 않는 것**: 디렉터리 안의 파일 목록을 실제로 나열하는 법은 [02장: ls](/post/bashshell/ls-command-list-files-directories-linux/)에서 다루고, 명령어 자체를 셸이 어떻게 찾아 실행하는지(`PATH`·`type`·`hash`·`command`)는 이 커리큘럼의 뒤쪽 챕터에서 별도로 다룬다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| 입문 | 개요 + 정신 모델, 사용법·옵션, 예시 1–5번 | 절대·상대 경로로 원하는 디렉터리로 이동하고 `pwd`로 현재 위치를 확인할 수 있다 |
| 중급 | 예시 6–8번, 주의사항·함정 | `cd -`와 `OLDPWD`로 디렉터리를 오가고, `CDPATH`가 스크립트에서 왜 위험한지 설명할 수 있다 |
| 심화 | 주의사항·함정의 심볼릭 링크 부분, 흔한 오개념 | 심볼릭 링크 디렉터리 안에서 `cd ..`가 논리 경로(`-L`)와 물리 경로(`-P`)에 따라 다르게 동작하는 이유를 설명할 수 있다 |

## 개요 + 정신 모델

셸은 명령을 실행할 때마다 매번 "지금 어디서 실행되는지"를 새로 묻지 않는다. 대신 프로세스마다 <strong>현재 작업 디렉터리(current working directory, cwd)</strong>라는 숨은 상태 하나를 계속 들고 있다가, `/`로 시작하지 않는 모든 경로(상대경로)를 그 cwd를 기준으로 해석한다. `cat notes.txt`를 입력하면 셸이 찾는 실제 대상은 `notes.txt`가 아니라 `<현재 cwd>/notes.txt`다. `cd`는 이 cwd 값 자체를 바꾸는 유일한 표준 수단이고, `pwd`는 그 값을 사람이 읽을 수 있는 절대 경로 문자열로 확인하는 창구다.

이 모델에서 중요한 점은 cwd가 셸(또는 셸에서 파생된 각 프로세스) 고유의 상태라는 것이다. 터미널 탭을 두 개 열어 각각 다른 디렉터리로 `cd`해도 서로 영향을 주지 않으며, 스크립트 안에서 자식 프로세스로 실행한 프로그램이 `cd`를 하더라도 그 변경은 자식 프로세스 안에서만 유효하고 스크립트를 실행한 부모 셸의 cwd는 그대로 남는다 — `cd`가 내장 명령(빌트인)이어야 하는 이유도 여기 있다. 별도 프로세스로 실행되는 외부 명령이라면 자신을 실행한 셸의 cwd를 바꿀 방법이 원천적으로 없기 때문이다.

## 사용법 · 옵션

### pwd

```bash
pwd [-L | -P]
```

인자 없이 실행하면 현재 작업 디렉터리의 절대 경로를 한 줄로 출력한다.

| 옵션 | 설명 |
|---|---|
| `-L`, `--logical` | (기본값) 심볼릭 링크를 그대로 유지한 논리적 경로를 출력한다 |
| `-P`, `--physical` | 심볼릭 링크를 모두 실제 경로로 풀어낸 물리적 경로를 출력한다 |

### cd

```bash
cd [-L | -P [-e]] [-@] [디렉터리]
```

GNU Bash Reference Manual은 `cd`의 기본 동작을 다음과 같이 정의한다.

> "Change the current working directory to directory. If directory is not supplied, the value of the `HOME` shell variable is used." — GNU Bash Reference Manual, "Bourne Shell Builtins"

즉 인자를 생략하면 `$HOME`(홈 디렉터리)으로 이동한다.

| 옵션 | 설명 |
|---|---|
| `-L` | (기본값) `..`를 처리한 **뒤**에 심볼릭 링크를 해석한다(논리적 경로) |
| `-P` | `..`를 처리하기 **전**에 심볼릭 링크를 실제 경로로 미리 풀어낸다(물리적 경로) |
| `-e` | `-P`와 함께 쓰며, 이동 후 실제 작업 디렉터리 경로를 확인할 수 없으면 실패로 처리한다 |
| `-@` | (일부 시스템) 확장 속성을 가진 파일을 디렉터리처럼 탐색할 수 있게 한다 |

### 경로 지정 방식

| 대상 | 예시 | 설명 |
|---|---|---|
| 절대 경로 | `cd /var/log` | `/`로 시작, cwd와 무관하게 항상 같은 위치를 가리킨다 |
| 상대 경로 | `cd src/utils`, `cd ..` | 현재 cwd를 기준으로 해석된다 |
| 홈 디렉터리 | `cd`, `cd ~` | 인자 생략 시 `$HOME`, `~`도 동일하게 해석됨 |
| 다른 사용자 홈 | `cd ~otheruser` | 권한이 있을 때만 이동 가능 |
| 이전 디렉터리 | `cd -` | `$OLDPWD`로 이동(아래 "주의사항" 참고) |

## 예시

### 기본 이동과 확인

```bash
# 현재 위치 확인
pwd
# 예: /home/user/project

# 절대 경로로 이동
cd /var/log

# 상대 경로로 한 단계 위로
cd ..

# 상대 경로로 하위 디렉터리 진입
cd project/src
```

### 홈 디렉터리와 이전 디렉터리

```bash
# 인자 없이 실행하면 홈으로 이동
cd

# ~ 로 홈 디렉터리를 명시적으로 지정
cd ~

# 직전에 있던 디렉터리로 복귀 (OLDPWD 값 사용, 이동한 경로를 화면에 출력)
cd -
```

### 스크립트에서 자주 쓰는 패턴

```bash
# 스크립트 파일이 위치한 디렉터리로 이동
cd "$(dirname "$0")"

# 현재 디렉터리 경로를 변수에 저장해 나중에 활용
SCRIPT_DIR=$(pwd)

# 이동에 실패하면 스크립트를 즉시 중단(디렉터리가 없을 때 잘못된 위치에서 계속 실행되는 사고 방지)
cd /backup/target || exit 1
```

### 심볼릭 링크 경로 확인

```bash
# 심볼릭 링크가 걸린 디렉터리로 이동한 뒤
cd /var/www/current   # 예: current -> /var/www/releases/v42

# 논리적 경로(기본): 링크 이름 그대로 보여준다
pwd
# /var/www/current

# 물리적 경로: 링크를 실제 경로로 풀어서 보여준다
pwd -P
# /var/www/releases/v42
```

## 주의사항·함정

**`cd -`와 `OLDPWD`**: `cd -`는 `$OLDPWD` 환경변수가 가리키는 디렉터리로 이동하는 축약 표현이다. GNU Bash Reference Manual은 이 동작을 "`-`가 인자로 주어지면 이는 디렉터리 변경이 시도되기 전에 `$OLDPWD`로 치환된다"고 설명하고, `cd`가 성공적으로 디렉터리를 바꾸면 그 직전 cwd 값을 `$OLDPWD`에 저장한다고 명시한다. 즉 `cd`를 한 번도 실행하지 않은 새 셸에서는 `OLDPWD`가 비어 있어 `cd -`가 실패하거나 예기치 않은 곳으로 이동할 수 있다. 또한 `cd -`는 일반 `cd`와 달리 이동한 뒤의 경로를 화면에 자동으로 출력한다는 점도 다른 이동 방식과 다르다.

**`CDPATH`의 부작용**: `CDPATH` 환경변수를 설정해 두면, `cd`에 상대 경로를 주었을 때 현재 디렉터리뿐 아니라 `CDPATH`에 나열된 디렉터리들도 순서대로 검색해 먼저 매칭되는 곳으로 이동한다. GNU Bash Reference Manual은 "디렉터리가 슬래시로 시작하면 `CDPATH`는 사용되지 않는다"고 명시하는데, 뒤집어 말하면 슬래시로 시작하지 않는 상대 경로는 항상 `CDPATH` 검색의 영향을 받는다는 뜻이다. 이 때문에 `CDPATH`가 설정된 환경에서 `cd project`처럼 흔한 이름의 하위 디렉터리로 이동하면, 현재 디렉터리 바로 아래가 아니라 `CDPATH`에 등록된 전혀 다른 위치의 `project`로 조용히 이동해 버리는 사고가 생긴다. 이런 이동은 성공 시 새 절대 경로를 표준 출력에 함께 찍어주긴 하지만, 스크립트에서 이 출력을 놓치면 원인을 찾기 어려운 버그가 된다. 이식성과 예측 가능성이 중요한 스크립트에서는 `CDPATH`를 아예 설정하지 않거나, 스크립트 맨 앞에서 `unset CDPATH`로 명시적으로 무력화하는 것이 안전하다.

**심볼릭 링크와 `-L`/`-P`의 `cd ..` 해석 차이**: `cd`의 기본값은 `-L`(논리적 경로)이다. GNU Bash Reference Manual은 두 옵션의 차이를 다음과 같이 구분한다.

> "`-L`: symbolic links in directory are resolved after `cd` processes an instance of '..' in directory. `-P`: symbolic links are resolved while `cd` is traversing directory and before processing an instance of '..' in directory." — GNU Bash Reference Manual, "Bourne Shell Builtins"

이 차이는 심볼릭 링크로 연결된 디렉터리 안에서 `cd ..`를 실행할 때 실제로 다른 결과를 낳는다. 예를 들어 `/var/www/current`가 `/var/www/releases/v42`를 가리키는 심볼릭 링크라고 하자. 기본값(`-L`)에서는 셸이 `..`를 **링크 이름을 기준으로 문자열 그대로** 처리하므로 `cd /var/www/current` 다음 `cd ..`를 실행하면 `/var/www`로 이동한다. 반면 `cd -P /var/www/current`로 물리 경로를 먼저 확정한 뒤 `cd ..`를 실행하면, 셸은 실제 디스크 구조상의 부모인 `/var/www/releases`로 이동한다. 두 결과가 다른 이유는 `-L`이 링크를 나중에(경로 문자열 수준에서) 처리하고 `-P`는 링크를 먼저(실제 디렉터리 트리 수준에서) 풀어버리기 때문이다. 배포·심볼릭 링크 기반 릴리스 구조(`current` → 최신 버전 디렉터리)를 다루는 스크립트에서 이 차이를 모르면 `cd ..`의 목적지를 착각하기 쉽다.

## 흔한 오개념

**"`pwd`는 항상 실제 디스크 경로를 보여준다"는 틀렸다.** 기본 동작(`-L`)은 심볼릭 링크를 거친 경로 문자열을 그대로 보여주므로, 링크를 거쳐 들어온 디렉터리에서는 `pwd`와 `pwd -P`의 출력이 다를 수 있다. 물리적으로 디스크상 진짜 위치가 필요하면 반드시 `-P`를 명시해야 한다.

**"`cd`로 이동한 디렉터리는 스크립트를 호출한 셸에도 반영된다"는 흔한 오해다.** 스크립트를 `./script.sh`처럼 별도 프로세스(서브셸)로 실행하면, 그 스크립트 안에서 아무리 `cd`를 해도 스크립트를 실행시킨 부모 셸(터미널)의 cwd는 전혀 바뀌지 않는다. 현재 셸의 cwd를 스크립트로 바꾸고 싶다면 `./script.sh`가 아니라 `source script.sh`(또는 `. script.sh`)로 현재 셸 안에서 직접 실행해야 한다.

## 다음 장에서는

[02장: ls](/post/bashshell/ls-command-list-files-directories-linux/)에서는 지금 위치한 디렉터리 안에 실제로 무엇이 있는지 목록으로 확인하는 법을 다룬다.

## 평가 기준

- 현재 작업 디렉터리(cwd)가 셸(프로세스)마다 독립적으로 유지되는 숨은 상태이며, 상대경로가 이를 기준으로 해석된다는 점을 설명할 수 있다.
- 절대 경로·상대 경로·홈 디렉터리·`cd -`를 상황에 맞게 선택해 이동할 수 있다.
- `CDPATH`가 설정된 환경에서 `cd`에 상대 경로를 줄 때 어떤 부작용이 생길 수 있는지 설명할 수 있다.
- 심볼릭 링크가 걸린 디렉터리에서 `cd ..`의 결과가 `-L`(논리적)과 `-P`(물리적)에 따라 달라지는 이유를 설명할 수 있다.
- `pwd`와 `pwd -P`의 출력이 다를 수 있는 상황을 식별할 수 있다.

## 참고

- [Bourne Shell Builtins — GNU Bash Reference Manual](https://doc.guix.gnu.org/bash/latest/en/html_node/Bourne-Shell-Builtins.html)
- [POSIX cd — The Open Group Base Specifications](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/cd.html)
