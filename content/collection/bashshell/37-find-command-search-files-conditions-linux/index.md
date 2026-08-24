---
draft: false
slug: find-command-search-files-conditions-linux
title: "[Bash Shell] 37. find - 파일 탐색과 조건 필터"
description: "디렉터리 트리를 순회하며 이름·타입·시간·크기 조건(predicate)을 평가해 파일을 걸러내는 find의 정신 모델과 사용법, find -print0 | xargs -0 안전 패턴, -exec {} \\; 대 {} + 성능 차이, -prune, GNU·BSD 이식성 차이를 예제로 정리합니다."
date: 2026-03-15
lastmod: 2026-08-24
collection_order: 370
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
- Guide(가이드)
- Tutorial(튜토리얼)
- Reference(참고)
- Quick-Reference
- Troubleshooting(트러블슈팅)
- How-To
- Tips
- Beginner
- Comparison(비교)
- Deep-Dive
- Best-Practices
- Workflow(워크플로우)
- Recursion(재귀)
- Searching(탐색)
- System-Administration(시스템관리)
- Pipeline
- find
- 파일탐색
- 조건필터
- exec
- xargs
- print0
- prune
- glob
- mtime
image: "wordcloud.png"
---

`find`는 리눅스·유닉스에서 지정한 경로 아래를 **재귀적으로 순회**하며, 이름·타입·수정 시간·크기 등 **조건(predicate)에 맞는 파일·디렉터리**를 찾아내는 명령어다. 찾아내는 것으로 끝나지 않고 `-exec`·`-delete`로 "찾은 뒤 무엇을 할지"까지 한 명령으로 표현할 수 있어, 스크립트·백업·정리 작업에서 핵심적으로 쓰인다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [36장: chmod, chown](/post/bashshell/chmod-chown-commands-file-permissions-ownership/)에서 이어진다. Part 6(파일 시스템과 권한)의 두 번째 챕터로, 36장에서 권한·소유자를 다루는 대상 자체를 어떻게 특정하는지가 필요해진다 — `find`는 바로 그 "대상이 될 파일들을 조건으로 골라내는" 역할을 맡는다. [21장: xargs](/post/bashshell/xargs-command-build-execute-command-lines/)를 먼저 읽었다면, 그 장에서 예고만 됐던 `find ... -print0 | xargs -0` 안전 패턴을 이 장에서 실제로 완결한다.

**이 장의 깊이**: **입문–중급** 난이도다. 이름·타입·시간·크기 조건 조합부터 `-exec`·`-delete`로 찾은 결과를 바로 처리하는 법까지 실무에서 매일 쓰는 범위를 다루고, `-prune`·`-regextype` 같은 GNU 확장은 고급 구간으로 함께 짚는다. **다루지 않는 것**: `xargs`의 세부 옵션(`-I`, `-P`, 배치 크기 등)은 [21장: xargs](/post/bashshell/xargs-command-build-execute-command-lines/)에서, 찾아낸 파일을 실제로 압축·해제하는 법은 [38장: gzip](/post/bashshell/gzip-command-compress-decompress-files/)에서 다룬다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| 조건에 맞는 파일을 바로 찾아 처리하고 싶은 사람 | 개요+정신 모델, 사용법·옵션의 "이름·경로"·"타입"·"시간", 예시의 "이름으로 검색"~"exec·삭제" | 이름·타입·시간 조건을 조합해 원하는 파일을 찾고 `-exec`·`-delete`로 바로 처리한다 |
| 안전하고 빠른 배치 스크립트를 작성해야 하는 사람 | 사용법·옵션 전체, 예시의 "print0과 xargs"·"exec 배치 처리"·"prune", 주의사항·함정 전체 | 공백·특수문자가 섞인 파일명도 안전하게 처리하고, `-exec {} +`와 `-prune`으로 성능·범위를 제어한다 |

---

## 개요 + 정신 모델

`find`는 **디렉터리 트리를 순회하며 각 항목에 술어(predicate)를 평가하는 필터링 엔진**이다. `-name`, `-type`, `-mtime` 같은 조건은 참/거짓을 판단하는 개별 술어이고, 여러 술어를 나열하면 기본적으로 AND로 묶인 하나의 **불리언 표현식**이 된다. `find`는 트리의 각 항목마다 이 표현식을 왼쪽에서 오른쪽으로 평가해, 결과가 참인 항목에 대해서만 기본 동작인 `-print`(경로 출력)를 수행한다.

이 모델에서 중요한 것은 `-exec`나 `-delete`도 술어와 **동일한 표현식 안의 한 항목**이라는 점이다. `find . -name "*.tmp" -delete`는 "이름이 `*.tmp`이면서(AND) 삭제에 성공하면 참"이라는 하나의 표현식이다. 즉 `find`는 다른 명령(`grep`, `xargs` 등)의 도움 없이도 "조건에 맞는 것을 찾아서 즉시 무엇을 할지"까지 한 문장으로 표현할 수 있는 몇 안 되는 도구다. 이 정신 모델을 이해하면, 뒤에서 다룰 "왜 조건의 순서가 결과에 영향을 주는가"(주의사항·함정)도 자연스럽게 이해된다 — `find`는 옵션을 미리 다 모아서 평가하는 게 아니라, 표현식을 순서대로 하나씩 판단하며 지나가기 때문이다.

## 사용법 · 옵션

```bash
find [경로...] [표현식]
```

- **경로**: 검색을 시작할 디렉터리. 생략 시 현재 디렉터리(`.`)로 간주.
- **표현식**: 검색 조건·동작. 여러 개를 나열하면 AND로 묶인다. `-o`로 OR, `!`로 부정.

### 검색 범위·순서

| 옵션 | 설명 |
|------|------|
| `-maxdepth N` | 최대 깊이 N까지만 검색 (1이면 해당 디렉터리만). POSIX 표준에는 없지만 GNU findutils·BSD find 모두 지원하는 사실상 표준 확장 |
| `-mindepth N` | 최소 깊이 N부터 검색 |
| `-depth` | 디렉터리 내용을 먼저, 그 다음 디렉터리 자체 (rm 등과 조합 시 유용) |
| `-prune` | 항상 참으로 평가되며, 디렉터리일 경우 그 **하위로 내려가지 않고 건너뛴다**(POSIX 표준 술어) |

### 이름·경로

| 표현식 | 설명 |
|--------|------|
| `-name PATTERN` | 파일명이 PATTERN과 일치 (glob: `*`, `?`, `[]`). 셸이 먼저 확장하지 않도록 항상 따옴표로 감싼다 |
| `-iname PATTERN` | `-name`과 같으나 대소문자 무시 |
| `-path PATTERN` | 경로 전체가 PATTERN과 일치 |
| `-regex PATTERN` | 경로가 정규식 PATTERN과 일치. 기본 정규식 문법은 GNU find와 BSD find가 서로 다르다 |

### 타입

| 표현식 | 설명 |
|--------|------|
| `-type d` | 디렉터리만 |
| `-type f` | 일반 파일만 |
| `-type l` | 심볼릭 링크만 |
| `-type s` | 소켓, `-type p` 파이프 등 |

### 시간

| 표현식 | 설명 |
|--------|------|
| `-mmin N` | 수정이 N분 이내(이전: `-N`, 초과: `+N`) |
| `-mtime N` | 수정이 N일 이내(`-N` 이내, `+N` 초과) |
| `-amin N`, `-atime N` | 접근 시간 기준 |
| `-cmin N`, `-ctime N` | 상태 변경 시간 기준 |

### 크기·기타

| 표현식 | 설명 |
|--------|------|
| `-size N[cwbkMG]` | 크기. `+N` 초과, `-N` 미만. c=바이트, k=KB, M=MB 등 |
| `-empty` | 빈 파일·디렉터리 |
| `-perm MODE` | 권한이 MODE와 일치 |
| `-user NAME`, `-group NAME` | 소유자·그룹 |

### 동작

| 표현식 | 설명 |
|--------|------|
| `-print` | 경로 출력 (기본 동작) |
| `-print0` | 널 문자로 구분 (`xargs -0`와 조합) |
| `-exec CMD {} \;` | 매칭 항목마다 CMD를 **한 번씩** 실행. `{}`는 해당 경로로 치환 |
| `-exec CMD {} +` | 매칭 항목 여러 개를 **한 번의 CMD 호출**에 묶어서 전달(`xargs`처럼 배치 처리) |
| `-execdir CMD \;` | 해당 디렉터리에서 CMD 실행 |
| `-delete` | 매칭 항목 삭제 |
| `-quit` | 첫 매칭 후 종료 |

## 예시

### 이름으로 검색

```bash
# 현재 디렉터리 아래 .log 파일
find . -name "*.log"

# 대소문자 무시
find /var -iname "*.LOG"

# 이름이 config로 시작하는 파일
find . -name "config*"
```

### 타입·깊이 제한

```bash
# 디렉터리만, 최대 깊이 2
find . -maxdepth 2 -type d

# 현재 디렉터리 직하위 .txt 파일만 (깊이 1)
find . -maxdepth 1 -type f -name "*.txt"
```

### 시간 기준

```bash
# 7일 이내 수정된 파일
find /tmp -type f -mtime -7

# 30일 넘게 수정 안 된 파일
find /var/log -type f -mtime +30

# 1시간 이내 변경된 파일
find . -type f -mmin -60
```

### 크기·빈 파일

```bash
# 100MB 초과 파일
find /home -type f -size +100M

# 빈 디렉터리
find . -type d -empty
```

### exec·삭제

```bash
# 매칭 파일에 chmod 적용 (파일마다 chmod 프로세스를 새로 fork)
find . -name "*.sh" -exec chmod +x {} \;

# 30일 지난 로그 삭제 (주의해서 사용)
find /var/log -name "*.log" -mtime +30 -delete
```

### exec 배치 처리 비교 ({} \; 대 {} +)

```bash
# {} \; : 매칭 100개면 chmod가 100번 실행된다 — 파일마다 새 프로세스를 fork
find . -name "*.sh" -exec chmod +x {} \;

# {} + : 매칭된 파일들을 한 번(또는 ARG_MAX에 맞춰 몇 번)의 chmod 호출에 묶어 전달
find . -name "*.sh" -exec chmod +x {} +
```

### print0과 xargs로 안전하게 처리

```bash
# 공백·줄바꿈이 있는 파일명도 안전하게 처리 ([21장: xargs] 참고)
find . -name "*.txt" -print0 | xargs -0 grep -l "keyword"
```

### -prune으로 특정 디렉터리 건너뛰기

```bash
# .git, node_modules 디렉터리는 아예 내려가지 않고 건너뛴 채 .js 파일만 찾는다
find . \( -path "./.git" -o -path "./node_modules" \) -prune -o -type f -name "*.js" -print
```

## 주의사항·함정

**파일명에 공백·특수문자가 있을 때는 `find -print0 | xargs -0`로 처리한다.** [21장: xargs](/post/bashshell/xargs-command-build-execute-command-lines/)에서 이미 예고했던 이 안전 패턴을 여기서 완결한다. 기본 `xargs`는 입력을 공백·탭·개행으로 구분하기 때문에, `find`가 찾아낸 경로에 공백이 섞여 있으면(`March report.log`처럼) `March`와 `report.log`라는 두 개의 별개 인자로 쪼개져 버린다. `find`의 `-print0`은 각 결과를 구분자로 쓸 수 없는 문자인 <strong>널 문자(`\0`)</strong>로 구분해 출력하고, `xargs -0`은 그 널 문자를 기준으로 다시 정확히 하나의 인자로 읽어들인다. `find . -name "*.log" -print0 | xargs -0 rm`처럼 삭제·이동같이 되돌릴 수 없는 작업일수록 이 조합을 기본값으로 삼아야 한다.

**`-exec CMD {} \;`와 `-exec CMD {} +`는 결과는 같아도 성능이 크게 다르다.** `\;`로 끝내면 매칭된 항목마다 CMD를 **한 번씩** 새로 fork·exec한다 — 파일이 10만 개면 프로세스도 10만 번 생성된다. 반대로 `+`로 끝내면 `find`가 매칭된 경로들을 모아 뒀다가 (운영체제의 `ARG_MAX` 한도 안에서) 최소한의 횟수로 CMD 명령줄 끝에 한꺼번에 붙여 실행한다 — [21장: xargs](/post/bashshell/xargs-command-build-execute-command-lines/)가 표준입력을 인자로 바꿔 배치 실행하는 방식과 동일한 아이디어다. 파일 수가 많고 CMD 자체가 여러 인자를 한 번에 받을 수 있는 명령(`chmod`, `rm`, `grep` 등)이라면 `+`가 압도적으로 빠르다.

**술어의 평가 순서가 결과와 성능에 함께 영향을 준다.** `find`는 표현식을 왼쪽에서 오른쪽으로 평가하다가 AND는 좌변이 거짓, OR는 좌변이 참인 순간 나머지를 건너뛴다(단락 평가). 이 때문에 비용이 싼 조건(`-type f` 같은 단순 비교)을 비용이 비싼 조건(`-exec`, 정규식 매칭) 앞에 두면 불필요한 실행을 줄일 수 있다. 더 중요한 것은 `-prune`처럼 **동작을 겸하는 술어**의 위치다. `-prune`은 반드시 `-print`나 다른 동작보다 **앞쪽**, 그리고 건너뛸 디렉터리를 판별하는 조건 바로 뒤에 와야 한다 — 예시의 `\( -path ... -o -path ... \) -prune -o -type f -print`처럼 순서를 지키지 않으면 디렉터리를 건너뛰지 않고 그대로 내려가 버린다.

**GNU find와 BSD/macOS find는 옵션 지원 범위가 다르다.** 이 글의 예시는 리눅스 배포판 대부분이 쓰는 **GNU findutils** 기준이다. `-print0`, `-maxdepth`, `-prune`, `-exec {} +`는 POSIX 표준이거나 GNU·BSD 양쪽이 공통으로 지원하지만, `-regextype`(정규식 문법을 바꾸는 옵션)이나 `-executable`/`-readable`/`-writable` 같은 술어는 **GNU 전용 확장**이라 macOS 기본 `find`(BSD find 계열)에서는 지원하지 않는다. macOS에서 GNU find와 동일하게 동작시키려면 Homebrew로 `brew install findutils`를 설치해 `gfind`로 실행해야 한다. `-regex`의 기본 정규식 문법도 GNU find는 POSIX BRE인 반면 BSD find는 자체 문법을 쓰므로, 같은 패턴이 두 환경에서 다르게 매칭될 수 있다.

## 흔한 오개념

**"`find`의 조건 순서는 결과에 영향을 주지 않는다"는 정확하지 않다.** `find`는 조건들을 한꺼번에 모아 논리적으로만 판단하는 것이 아니라, 하나의 표현식을 **왼쪽에서 오른쪽으로 차례로 평가**하며 지나간다. `-exec`·`-print`·`-prune`처럼 부수효과가 있는 항목이 섞이면 순서가 곧 실행 순서이므로, `-prune`을 뒤에 두거나 `-o`로 묶인 그룹의 괄호를 빠뜨리면 의도와 다른 디렉터리까지 내려가거나 원하는 항목이 빠질 수 있다.

**"`-name` 패턴은 따옴표 없이 써도 괜찮다"는 오해도 흔하다.** `find . -name *.txt`처럼 따옴표를 빼면, `find`가 패턴을 받기 전에 **셸이 먼저** `*.txt`를 현재 디렉터리의 실제 `.txt` 파일 이름들로 확장해 버린다. 디렉터리에 `.txt` 파일이 하나도 없으면 패턴 문자열 그대로 전달돼 우연히 의도대로 동작하지만, 파일이 하나라도 있으면 `find`는 `-name`을 그 파일 이름 하나에만 적용하게 되어 나머지 `.txt` 파일을 놓친다. `-name`·`-path`·`-regex`에 넘기는 패턴은 항상 따옴표로 감싸 셸이 아니라 `find`가 직접 해석하게 해야 한다.

## 다음 장에서는

다음은 [38장: gzip](/post/bashshell/gzip-command-compress-decompress-files/) — `find`로 찾아낸 파일을 실제로 압축·해제하는 `gzip`을 다룬다.

## 평가 기준

- `find`의 정신 모델(트리 순회 + 술어 평가, 찾은 뒤 무엇을 할지까지 한 표현식으로 결합)을 설명할 수 있다.
- 이름·타입·시간·크기 조건을 조합해 원하는 파일을 필터링할 수 있다.
- `find -print0 | xargs -0` 안전 패턴이 왜 필요한지, 기본 `xargs`가 어떤 파일명에서 깨지는지 설명할 수 있다.
- `-exec CMD {} \;`와 `-exec CMD {} +`의 프로세스 생성 비용 차이를 설명하고 상황에 맞게 선택할 수 있다.
- `-prune`으로 특정 디렉터리를 탐색에서 제외하는 법과, 술어 평가 순서가 결과·성능에 미치는 영향을 판단할 수 있다.
- GNU find와 BSD/macOS find의 옵션 차이를 구분하고 스크립트를 이식할 때 무엇을 점검해야 하는지 설명할 수 있다.

## 참고

- [find(1) - Linux manual page](https://man7.org/linux/man-pages/man1/find.1.html)
- [find - POSIX.1-2017 (The Open Group Base Specifications)](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/find.html)
- [find(1) - FreeBSD Manual Pages](https://man.freebsd.org/cgi/man.cgi?query=find&sektion=1)
