---
draft: false
slug: path-type-hash-command-shell-command-lookup
title: "[Bash Shell] 10. PATH, type, hash, command - 셸의 명령어 탐색 원리"
description: "PATH 환경변수가 콜론으로 구분된 디렉터리를 왼쪽부터 탐색하는 순서, type이 별칭·함수·빌트인·외부파일을 정확히 구분하는 원리, hash가 경로를 캐싱해 재탐색을 건너뛰다 오래되면 문제가 되는 이유, command로 별칭·함수를 우회하는 법을 정리합니다."
date: 2026-08-23
lastmod: 2026-08-23
collection_order: 100
categories:
- Bash Shell
tags:
- Bash
- Shell(셸)
- Linux(리눅스)
- Terminal
- Command
- Environment
- PATH
- Process
- Automation(자동화)
- Guide(가이드)
- Tutorial(튜토리얼)
- Reference(참고)
- Beginner
- Troubleshooting(트러블슈팅)
- Pitfalls(함정)
- How-To
- Tips
- Cache
- System-Administration(시스템관리)
- Configuration(설정)
- File-System
- Type-Builtin
- Hash-Builtin
- Command-Builtin
- Command-Search
- Executable-Lookup
- 명령어탐색
- PATH탐색
- 셸빌트인
- 캐싱
image: "wordcloud.png"
---

터미널에 `ls`라고 입력하면 셸은 그 두 글자를 어떻게 실제로 실행 가능한 프로그램으로 바꾸는가. 이 장은 Bash가 명령어 이름 하나를 받아 실제로 무엇을 실행할지 결정하는 내부 규칙 — 함수·빌트인·`PATH` 탐색의 우선순위, 탐색 결과를 기억해 두는 `hash`, 그 판단 과정을 사용자가 직접 조회하는 `type`, 별칭·함수를 건너뛰고 강제로 외부 명령을 부르는 `command` — 를 GNU Bash Reference Manual 원문과 대조해 다룬다.

## 이 장을 읽기 전에

직전 챕터인 [09장: which, whereis, locate](/post/bashshell/which-whereis-locate-commands-find-command-location/)에서 다룬 `which`·`whereis`·`locate`는 모두 셸 바깥에서 명령어의 위치를 알려주는 **외부 유틸리티**였다 — `which`조차도 `PATH`를 참고해 경로를 알려줄 뿐, 실제로 셸이 명령을 실행할 때 거치는 판단 과정과는 별개의 프로그램이다. 이 장은 관점을 뒤집는다. 셸 자신이 명령어 한 줄을 받았을 때 내부적으로 무엇을 먼저 확인하고, 어디를 탐색하고, 그 결과를 어떻게 기억해 두는지 — 즉 `which`가 흉내만 내던 그 판단 과정을 셸이 실제로 수행하는 메커니즘 자체를 다룬다.

난이도는 입문–중급이다. [01장: cd, pwd](/post/bashshell/cd-pwd-change-directory-linux-commands/) 수준의 셸 기본 조작과, 환경변수가 문자열 값을 담고 있다는 정도만 알면 충분하다. **다루지 않는 것**: 별칭(alias)을 정의·삭제하는 문법 자체는 [35장: alias](/post/bashshell/alias-command-shell-command-shortcuts/)에서, 로그인·비로그인 셸에 따라 `PATH`가 애초에 어떻게 채워지는지는 다음 [11장: .bashrc와 로그인/비로그인 셸](/post/bashshell/bashrc-bash-profile-login-shell-startup-files/)에서 다룬다. 이 장은 이미 설정된 `PATH` 값을 셸이 어떻게 소비하는지에 집중한다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| 입문 | 개요 + 정신 모델, 핵심 개념의 PATH·type | `PATH`가 콜론으로 구분된 디렉터리 목록이라는 것과 `type`으로 명령어 종류를 확인하는 법을 이해한다 |
| 중급 | 핵심 개념 전체, 예시 | `hash`로 캐시를 조회·초기화하고 `command`로 별칭·함수를 우회할 수 있다 |
| 심화 | 주의사항·함정, 흔한 오개념 | hash 캐시가 오래된 경로를 가리켜 생기는 문제를 진단·해결하고, alias shadowing의 동작 범위를 예측할 수 있다 |

## 개요 + 정신 모델

Bash에게 명령어 이름 하나는 곧바로 실행할 프로그램이 아니라, 정해진 순서대로 확인해야 할 후보 목록에 대한 질의다. 셸은 이름을 받으면 가장 먼저 자신이 정의한 함수인지, 그다음 내장된 빌트인인지 확인하고, 둘 다 아니면 그제야 파일시스템으로 나가 `PATH`에 나열된 디렉터리를 왼쪽부터 순서대로 뒤져 실행 파일을 찾는다. 이 마지막 단계가 매번 반복되면 비용이 크기 때문에 Bash는 한 번 찾은 전체 경로를 해시 테이블에 기억해 뒀다가 같은 이름이 다시 나오면 탐색을 건너뛴다. `type`은 이 판단 과정의 결과를 사용자에게 그대로 보여주는 창이고, `hash`는 그 기억(캐시) 자체를 조회·조작하는 도구이며, `command`는 이 우선순위 목록의 앞부분(별칭·함수)을 의도적으로 건너뛰라고 지시하는 명령이다. 네 요소 모두 "셸이 이름을 실행 가능한 것으로 바꾸는 하나의 파이프라인"을 서로 다른 각도에서 다룬다는 점에서 한 장으로 묶일 이유가 있다.

## 핵심 개념

### PATH — 콜론으로 구분된 탐색 경로 목록

`PATH`는 셸이 명령어를 찾을 때 뒤질 디렉터리 목록을 담은 환경변수다. GNU Bash Reference Manual은 이를 다음과 같이 정의한다.

> "A colon-separated list of directories in which the shell looks for commands. A zero-length (null) directory name in the value of PATH indicates the current directory." — GNU Bash Reference Manual, "Bourne Shell Variables"

즉 `PATH`는 콜론(`:`)으로 구분된 디렉터리 목록이며, 값이 비어 있는 항목(콜론이 연속되거나 값의 맨 앞·맨 뒤에 콜론이 오는 경우)은 현재 디렉터리를 의미한다. 탐색은 **왼쪽부터 순서대로** 이루어지고, 같은 이름의 실행 파일이 여러 디렉터리에 있으면 가장 먼저 매치되는(가장 왼쪽 디렉터리의) 파일이 채택된다 — 뒤쪽 디렉터리에 더 최신 버전이 있어도 소용없다.

```bash
echo "$PATH"
# /usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin

echo "$PATH" | tr ':' '\n'
# 한 줄씩 보면 실제 탐색 순서가 눈에 들어온다
```

### type — 명령어가 실제로 무엇인지 정확히 구분

`type`은 주어진 이름을 셸이 어떻게 해석할지 판정한다. 별칭(alias)·함수(function)·빌트인(builtin)·키워드(keyword)·외부 파일(file) 중 무엇인지 구분해 알려준다는 점에서, `PATH`만 뒤져 파일 경로를 찾는 `which`보다 훨씬 신뢰할 수 있다 — `which`는 셸의 내부 상태(그 셸에 정의된 별칭·함수)를 애초에 알지 못하는 별개의 외부 프로그램이기 때문이다.

| 옵션 | 설명 |
|---|---|
| (없음) | 이름이 별칭·함수·빌트인·키워드·파일 중 무엇인지 사람이 읽기 쉬운 문장으로 출력 |
| `-t` | 위 판정 결과를 `alias`/`function`/`builtin`/`keyword`/`file` 중 한 단어로만 출력(스크립트에서 조건 분기에 쓰기 좋음) |
| `-a` | `PATH`·함수·빌트인·별칭을 모두 뒤져 매치되는 **모든** 위치를 나열 |
| `-p` | 파일로 실행될 경로만 출력(별칭·함수·빌트인이면 아무것도 출력하지 않음) |
| `-P` | 분류와 무관하게 강제로 `PATH` 탐색을 수행해 경로를 출력 |
| `-f` | 함수 검색을 건너뛰고 빌트인·파일만 확인 |

```bash
type cd
# cd is a shell builtin

type ls
# ls is aliased to `ls --color=auto' (배포판·설정에 따라 다름)

type -t grep
# file

type -a python3
# 여러 위치에 있으면 전부 나열, 실제로 실행되는 것은 첫 줄
```

GNU Bash Reference Manual은 `type -p`/`-P`가 캐시된 값을 우선 출력한다는 점도 명시한다.

> "If a command is hashed, -p and -P print the hashed value, which is not necessarily the file that appears first in `$PATH`." — GNU Bash Reference Manual, "Bash Builtins"

즉 `PATH`를 바꿔도 이미 캐시(다음 항목의 `hash`)된 명령이라면 `type -p`가 새 `PATH` 기준 첫 번째 파일이 아니라 캐시된 예전 경로를 보여줄 수 있다.

### hash — 탐색 결과 캐싱

Bash는 명령어를 한 번 찾을 때마다 그 전체 경로를 해시 테이블에 기억해 둔다. GNU Bash Reference Manual은 이 동작을 다음과 같이 설명한다.

> "Bash uses a hash table to remember the full pathnames of executable files to avoid multiple `PATH` searches." — GNU Bash Reference Manual, "Command Search and Execution"

`hash` 빌트인은 이 캐시 자체를 들여다보고 조작하는 도구다.

| 옵션 | 설명 |
|---|---|
| (없음) | 현재 캐시된 명령어와 경로 목록 전체 출력 |
| `-t name` | 지정한 이름의 캐시된 전체 경로만 출력 |
| `-d name` | 지정한 이름 하나의 캐시만 잊어버림(다음 호출 때 다시 탐색) |
| `-r` | 캐시 전체를 잊어버림(다음 호출부터 전부 다시 탐색) |
| `-p path name` | 실제로 탐색하지 않고 지정한 경로를 그 이름의 캐시 값으로 강제 등록 |
| `-l` | 캐시 내용을 다시 `hash` 명령으로 재사용할 수 있는 형식으로 출력 |

```bash
hash
# 현재 세션에서 이미 실행해 캐시된 명령과 경로 목록

hash -t bash
# /usr/bin/bash

hash -d node
# node 캐시만 초기화

hash -r
# 캐시 전체 초기화 — PATH를 바꾼 뒤 흔히 쓴다
```

### command — 별칭·함수를 우회해 진짜 외부 명령 호출

`command`는 지정한 이름을 셸 함수로 해석하지 않고 오직 빌트인이나 `PATH` 탐색으로 찾은 실행 파일로만 실행한다.

> "Runs command with args suppressing the normal shell function lookup... Only shell builtin commands or commands found by searching the PATH are executed." — GNU Bash Reference Manual, "Bash Builtins"

이 규칙은 명시적으로 **함수** 우회만 언급하지만, 실제로는 별칭도 함께 우회된다 — 다만 그 이유는 `command`가 별칭을 특별 취급해서가 아니다. Bash의 별칭 치환은 애초에 "각 단순 명령의 첫 단어"에만 적용된다.

> "The first word of each simple command, if unquoted, is checked to see if it has an alias." — GNU Bash Reference Manual, "Aliases"

`command ls`에서 별칭 치환 대상이 되는 첫 단어는 `command`이고 `ls`는 그 뒤에 오는 두 번째 단어이므로, `ls`에 별칭이 걸려 있어도 애초에 검사 대상이 아니다. 결과적으로 `command`는 함수는 규칙으로 직접 배제하고, 별칭은 첫 단어 규칙의 부수 효과로 함께 우회하게 된다.

| 옵션 | 설명 |
|---|---|
| (없음) | 함수 탐색을 생략하고 빌트인 또는 `PATH`에서 찾은 명령만 실행 |
| `-p` | 표준 유틸리티를 확실히 찾을 수 있는 기본 `PATH` 값을 사용(사용자가 `PATH`를 이상하게 바꿔놔도 안전) |
| `-v` | 실제로 어떤 이름·파일이 쓰일지 한 단어로 출력(스크립트의 존재 여부 확인에 자주 씀) |
| `-V` | `-v`보다 더 자세한 설명 출력 |

```bash
alias ls='ls --color=auto -F'
command ls          # 별칭 없이 원래 ls 실행
\ls                  # 백슬래시로도 동일하게 우회 가능(첫 단어 자체가 "\ls"가 되어 별칭과 문자열이 다르게 매치됨)

command -v git >/dev/null 2>&1 && echo "git 설치됨"
# 스크립트에서 명령어 존재 여부를 확인하는 이식성 높은 관용구
```

## 예시

```bash
# 1. 현재 PATH를 한 줄씩 확인
echo "$PATH" | tr ':' '\n'

# 2. cd가 빌트인이라는 것을 확인
type cd

# 3. grep이 외부 파일이라는 것과 그 경로를 한 번에 확인
type -a grep

# 4. 스크립트에서 분기용으로 한 단어짜리 분류만 얻기
type -t docker 2>/dev/null || echo "docker 없음"

# 5. 현재 셸에서 이미 탐색된(캐시된) 명령 목록 보기
hash

# 6. 특정 명령의 캐시 경로만 확인
hash -t python3

# 7. PATH를 바꾼 뒤 캐시를 강제로 비워 재탐색을 유도
export PATH="$HOME/.local/bin:$PATH"
hash -r

# 8. 함수로 재정의된 이름을 command로 우회해 원래 빌트인 호출
pwd() { echo "가짜 pwd 함수 실행됨"; }
pwd            # 함수가 우선이므로 가짜 출력이 나온다
command pwd    # 함수를 건너뛰고 진짜 pwd 빌트인이 실행된다
unset -f pwd   # 실습 후 함수 정리

# 9. 표준 유틸리티를 안전하게 찾는 command -p
command -p ls /tmp

# 10. 이식성 있는 "명령어 존재 확인" 관용구(존재하면 조용히 통과)
if command -v curl >/dev/null 2>&1; then
  echo "curl 사용 가능"
fi
```

## 주의사항·함정

**`hash` 캐시가 오래된 경로를 가리키는 문제**: `hash`는 명령어를 한 번이라도 실행한 뒤에야 그 경로를 기억한다. 문제는 그 뒤에 같은 이름의 바이너리를 다른 경로로 옮기거나, 재설치해서 실제 파일이 사라지거나, 버전 관리 도구(nvm, pyenv, rbenv 등)로 활성 버전을 바꿔도 **현재 셸 세션의 캐시는 자동으로 갱신되지 않는다**는 점이다. 실무에서 실제로 자주 겪는 형태는 다음과 같다.

```bash
type node
# node is hashed (/home/user/.nvm/versions/node/v18.0.0/bin/node)

nvm use 20                 # node 20으로 전환(디렉터리가 바뀜)

node -v
# bash: /home/user/.nvm/versions/node/v18.0.0/bin/node: No such file or directory
# 예전 버전 디렉터리를 정리했다면 이런 식으로 "파일이 없다"는 에러가 난다

hash -r                    # 캐시 전체 초기화
node -v
# v20.x.x — 새 PATH 기준으로 다시 탐색해 정상 실행된다
```

이 문제는 새 셸을 열면(캐시가 비어 있으므로) 저절로 사라지지만, 이미 열려 있던 터미널·오래 살아있는 tmux 세션·백그라운드 스크립트에서는 그대로 남는다. `PATH`를 바꾸는 스크립트(버전 관리 도구의 `use`/`switch` 계열 명령 등)를 직접 짤 때는 마지막에 `hash -r`을 호출해 이 문제를 예방하는 것이 안전하다.

**alias가 명령어를 가려서(shadowing) 예상과 다르게 동작하는 문제**: 대화형 셸에서 흔한 `alias rm='rm -i'`, `alias grep='grep --color=auto'` 같은 설정은 같은 이름의 명령을 호출할 때마다 조용히 다른 동작으로 바뀐다. 이 자체가 함정이 되는 지점은 두 가지다. 첫째, 스크립트 안에서는 기본적으로 별칭이 전혀 확장되지 않는다.

> "Aliases are not expanded when the shell is not interactive, unless the `expand_aliases` shell option is set using `shopt`." — GNU Bash Reference Manual, "Aliases"

즉 터미널에서 손으로 입력할 때는 `rm`이 `rm -i`로 확장돼 삭제 전 확인을 받지만, 같은 이름으로 스크립트 파일 안에 적으면(기본 설정에서는) 확인 없이 그대로 삭제된다 — 대화형 환경에서 테스트하고 안심한 스크립트가 실제 배치 실행에서 다르게 동작하는 원인이 된다. 둘째, 원래의 외부 명령을 확실히 호출하고 싶을 때는 `command 명령` 또는 `\명령`으로 별칭을 우회해야 한다는 점을 앞서 다뤘다 — 이 우회는 함수에도 동일하게 적용되므로, 별칭인지 함수인지 굳이 구분하지 않고도 "원래 명령"을 부르는 공통 수단으로 쓸 수 있다.

```bash
alias rm='rm -i'
rm test.txt          # 대화형 셸에서는 삭제 전 확인을 받는다
command rm test.txt  # 별칭을 건너뛰고 확인 없이 바로 삭제한다 — 자동화 스크립트에서 의도적으로 쓸 때만 사용
```

## 흔한 오개념

<strong>"PATH를 바꾸면 그 즉시 모든 명령어 탐색에 반영된다"</strong>는 가장 흔한 오해다. 실제로는 이미 그 셸 세션에서 한 번이라도 실행해 캐시된 명령은 `hash -r`을 하기 전까지 예전 경로를 그대로 유지한다. `export PATH=...`만으로는 부족하고, 이미 캐시된 명령에 한해서는 재탐색을 명시적으로 유도해야 한다.

<strong>"`which`이 실제로 실행될 명령을 항상 정확히 알려준다"</strong>도 틀리기 쉽다. `which`는 대부분의 시스템에서 셸 내부 상태(별칭·함수·빌트인 목록)를 전혀 모르는 **별도의 외부 프로그램**이라, `PATH`상의 파일만 보고하고 실제로는 별칭이나 함수가 먼저 가로채 다른 동작을 할 수 있다는 사실을 반영하지 못한다. 정확한 판정이 필요하면 셸 자신의 판단을 그대로 보여주는 `type`(특히 `type -a`)을 쓰는 편이 안전하다.

## 다음 장에서는

[11장: .bashrc와 로그인/비로그인 셸](/post/bashshell/bashrc-bash-profile-login-shell-startup-files/)에서는 지금까지 이미 만들어져 있다고 가정했던 `PATH` 값이 애초에 어떻게 채워지는지 — 로그인 셸과 비로그인 셸이 각각 어떤 설정 파일을 읽고, `.bashrc`와 `.bash_profile`이 왜 나뉘어 있는지를 다룬다. 이 장이 "이미 있는 PATH를 셸이 어떻게 소비하는가"였다면, 다음 장은 "그 PATH가 애초에 어떻게 만들어지는가"다.

## 평가 기준

- `PATH`가 콜론으로 구분된 디렉터리 목록이며 왼쪽부터 순서대로 탐색된다는 것을 설명할 수 있다.
- Bash가 명령어를 해석할 때 함수 → 빌트인 → `PATH` 탐색(해시 캐시 경유) 순서로 확인한다는 것을 설명할 수 있다.
- `type`(특히 `-a`, `-t`)으로 명령어가 별칭·함수·빌트인·외부 파일 중 무엇인지 정확히 구분하고, `which`보다 신뢰할 수 있는 이유를 설명할 수 있다.
- `hash` 캐시가 오래된 경로를 가리켜 생기는 문제를 진단하고 `hash -r`로 해결할 수 있다.
- `command`로 별칭·함수를 우회해 원래의 외부 명령을 강제로 호출할 수 있고, 그 우회가 스크립트에서 별칭이 애초에 확장되지 않는 것과는 별개의 메커니즘임을 구분할 수 있다.

## 참고

- [Command Search and Execution — GNU Bash Reference Manual](https://doc.guix.gnu.org/bash/latest/en/html_node/Command-Search-and-Execution.html)
- [Bash Builtins — GNU Bash Reference Manual](https://doc.guix.gnu.org/bash/latest/en/html_node/Bash-Builtins.html)
- [Bourne Shell Builtins — GNU Bash Reference Manual](https://doc.guix.gnu.org/bash/latest/en/html_node/Bourne-Shell-Builtins.html)
- [Bourne Shell Variables — GNU Bash Reference Manual](https://doc.guix.gnu.org/bash/latest/en/html_node/Bourne-Shell-Variables.html)
- [Aliases — GNU Bash Reference Manual](https://doc.guix.gnu.org/bash/latest/en/html_node/Aliases.html)
