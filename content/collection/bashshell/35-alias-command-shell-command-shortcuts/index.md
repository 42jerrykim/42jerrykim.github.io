---
draft: false
slug: alias-command-shell-command-shortcuts
title: "[Bash Shell] 35. alias - 명령 별칭"
description: "alias는 명령줄 첫 단어를 다른 문자열로 치환하는 셸 빌트인이다. 인자를 받아 처리하는 로직은 짤 수 없는 이유를 32장 functions와 대조하고, 비대화형 셸에서 기본적으로 확장되지 않는 함정과 unalias로 제거하는 법을 정리한다."
date: 2026-03-15
lastmod: 2026-08-24
collection_order: 350
categories:
- Bash Shell
tags:
- Bash
- Shell(셸)
- Linux(리눅스)
- Terminal
- Command
- Automation(자동화)
- Environment
- Configuration(설정)
- Guide(가이드)
- Tutorial(튜토리얼)
- Reference(참고)
- Beginner
- Process
- Best-Practices
- Pitfalls(함정)
- Comparison(비교)
- Productivity(생산성)
- Quick-Reference
- How-To
- Tips
- alias
- unalias
- 별칭
- Text-Substitution
- Shell-Builtin
- Interactive-Shell
- Non-Interactive-Shell
- expand_aliases
- Command-Alias
- Shorthand
- Shell-Functions
- Positional-Parameters
- 명령별칭
image: "wordcloud.png"
---

`alias`는 자주 쓰는 명령을 짧은 이름으로 줄여 부를 수 있게 하는 셸 빌트인이다. 겉보기엔 함수와 비슷해 보이지만, 실제로는 명령줄 첫 단어를 다른 문자열로 그대로 바꿔치는 **텍스트 치환**일 뿐이라는 점에서 32장의 `functions`와 근본적으로 다르다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [34장: echo, export, env](/post/bashshell/echo-export-env-commands-shell-variables/)에서 값을 출력하고 환경 변수로 내보내는 법을 다룬 뒤 이어진다. 이 장이 전제하는 지식은 명령을 셸에 입력해 실행하는 기본 감각뿐이며, 32장에서 다룬 `functions`(위치 매개변수 `$1`, `$#`, `return` 등)를 이미 읽었다면 이 장의 대조 설명이 훨씬 잘 들어온다.

**이 장의 깊이**: **입문** 난이도다. `alias`·`unalias` 문법 자체는 단순하지만, "왜 스크립트에서는 안 먹히는가"라는 함정을 이해하려면 대화형/비대화형 셸의 구분(10장·11장)까지 함께 봐야 한다. **다루지 않는 것**: 셸이 로그인/비로그인·대화형/비대화형을 어떻게 판정하고 어떤 설정 파일을 읽는지의 전체 그림은 [11장: .bashrc와 로그인/비로그인 셸](/post/bashshell/bashrc-bash-profile-login-shell-startup-files/)에서 이미 다뤘으므로 이 장에서는 반복하지 않고 링크로 대신한다. 인자를 받아 조건 분기하는 로직이 필요하면 [32장: functions](/post/bashshell/bash-shell-functions-code-reuse/)로 넘어가야 한다 — 그것이 이 장의 핵심 주제이기도 하다.

이 장은 <strong>Part 5(셸 스크립팅)</strong>의 마지막 챕터다. 27장(`if`/`test`)부터 시작해 34장(`echo`/`export`/`env`)까지 이어진 스크립팅 문법 학습이 여기서 마무리되고, 다음 장부터는 완전히 다른 영역인 파일 시스템 관리로 넘어간다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| 대화형 셸에서 자주 쓰는 명령을 줄이고 싶은 사람 | 개요 + 정신 모델, 사용법·옵션, 예시 | `alias`로 자주 쓰는 명령 조합을 짧은 이름으로 등록하고 `.bashrc`에 영구 저장할 수 있다 |
| 스크립트에 alias를 쓰려다 막힌 사람 | 주의사항·함정, 흔한 오개념 | 비대화형 셸에서 alias가 확장되지 않는 이유와 첫 단어 위치 제약을 이해하고, 그 자리에 함수를 써야 하는 이유를 설명할 수 있다 |

## 개요 + 정신 모델

`alias`를 이해하는 가장 정확한 방법은 이것을 "짧은 이름의 프로그램"이 아니라 **셸이 명령줄을 읽는 도중에 수행하는 문자열 치환 한 단계**로 보는 것이다. `alias ll='ls -la'`를 등록하면 셸은 이후 입력에서 `ll`이라는 토큰을 명령으로 실행하기 직전, 그 자리를 `ls -la`라는 문자열로 그대로 바꿔 넣은 다음 나머지 파싱을 계속한다. POSIX 사양은 이를 "명령 이름을 만났을 때 그 자리를 대체할 문자열 값을 제공하는 정의"라고 규정한다.

> "An alias definition provides a string value that shall replace a command name when it is encountered." — POSIX.1-2017, "alias"

이 정신 모델에서 중요한 함의는 두 가지다. 첫째, 치환은 **글자 그대로**(literal) 일어난다 — alias 정의 시점에 인자를 미리 받아둘 방법이 없고, 실행 시점에 조건에 따라 다른 문자열로 바뀌게 만들 수도 없다. 둘째, 치환은 셸이 명령줄을 **파싱하는 단계**에서 일어나므로, 이미 파싱이 끝난 자리(파이프 뒤나 인자 위치)에는 적용되지 않는다. 이 두 특성이 뒤에서 다룰 함정들의 근본 원인이다.

이 지점에서 32장의 `functions`와 정확히 갈린다. 함수는 셸이 별도로 관리하는 **실행 단위**로, 호출될 때 위치 매개변수(`$1`, `$2`, `$@`, `$#`)로 인자를 넘겨받고, 내부에서 `if`·`case` 같은 조건 분기를 실행하며, `return`으로 종료 상태를 돌려줄 수 있다. `alias`에는 이 중 어느 것도 없다. `alias greet='echo Hello, $1'`처럼 써도 `$1`은 alias 정의 시점의 함수 인자가 아니라 그 alias를 호출한 스크립트/셸 자체의 위치 매개변수를 그대로 참조할 뿐이며, alias 자신에게 전달된 인자와는 무관하다. "인자를 받아 처리하는 로직"이 필요한 순간 `alias`는 도구로서 자격을 잃고, 그 자리는 함수의 몫이 된다.

| | `alias` | `functions`(32장) |
|---|---|---|
| 정체 | 명령줄 첫 단어의 문자열 치환 | 독립된 실행 단위 |
| 인자 처리 | 불가(alias 자체에 매개변수 개념 없음) | `$1`, `$2`, `$@`, `$#`로 위치 매개변수 전달 |
| 조건 분기·반복 | 불가 | `if`/`case`/`for` 등 셸 문법 전체 사용 가능 |
| 반환값 | 없음(치환된 명령의 종료 코드를 그대로 물려받음) | `return`으로 종료 상태 지정 가능 |
| 비대화형 셸(스크립트) | 기본적으로 확장 안 됨(아래 참고) | 항상 정상 동작 |
| 적합한 용도 | 자주 치는 명령 조합을 짧게 줄이기 | 재사용 가능한 로직 캡슐화 |

## 사용법 · 옵션

```bash
alias [이름[=값] ...]
unalias [-a] 이름 ...
```

인자 없이 `alias`만 실행하면 현재 등록된 별칭 목록을 `이름='값'` 형태로 출력한다. `이름=값` 형태로 실행하면 새 별칭을 등록하거나 기존 별칭을 덮어쓴다. `unalias`는 지정한 이름의 별칭을 제거한다.

| 옵션/형태 | 대상 | 설명 |
|---|---|---|
| `alias` | 조회 | 등록된 모든 별칭을 `이름='값'` 형식으로 출력 |
| `alias 이름` | 조회 | 특정 별칭 하나의 정의만 출력 |
| `alias 이름='명령'` | 등록 | 새 별칭 정의(따옴표로 값 전체를 감싸는 것이 안전) |
| `unalias 이름` | 제거 | 지정한 별칭 하나 제거 |
| `unalias -a` | 제거 | 등록된 별칭 전체 제거 |

## 예시

```bash
# 자주 쓰는 옵션 조합을 짧게 줄이기
alias ll='ls -la'
alias la='ls -A'
alias ..='cd ..'

# git 같은 긴 명령 이름을 줄이기
alias g=git
alias gs='git status'
alias gc='git commit -v'

# 파괴적 명령에 확인 옵션을 기본으로 붙이기
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# 등록된 별칭 확인
alias
alias ll
# ll='ls -la'

# 별칭 제거
unalias ..
unalias -a   # 전부 제거

# .bashrc에 넣어 영구 적용 (11장에서 다룬 시작 파일 규칙에 따라 대화형 셸에서 읽힘)
echo "alias ll='ls -la'" >> ~/.bashrc
```

`.bashrc`에 등록해 두는 이유는 명확하다 — [11장](/post/bashshell/bashrc-bash-profile-login-shell-startup-files/)에서 다뤘듯 `~/.bashrc`는 새 대화형 셸을 열 때마다 매번 다시 읽히는 파일이므로, 여기 등록한 별칭은 터미널을 새로 열어도 그대로 남는다.

## 주의사항·함정

**비대화형 셸(스크립트)에서는 alias가 기본적으로 확장되지 않는다.** [10장: PATH, type, hash, command](/post/bashshell/path-type-hash-command-shell-command-lookup/)에서 alias shadowing 문제를 다루며 이미 인용했듯, GNU Bash Reference Manual은 이 동작을 명시적으로 규정한다.

> "Aliases are not expanded when the shell is not interactive, unless the `expand_aliases` shell option is set using `shopt`." — GNU Bash Reference Manual, "Aliases"

즉 터미널에 직접 입력할 때는 잘 동작하던 `ll`이, 그 정의를 그대로 스크립트 파일 맨 위에 옮겨 놓고 `bash script.sh`로 실행하면 "command not found"로 실패한다. 셸이 비대화형으로 판정되는 조건은 [11장](/post/bashshell/bashrc-bash-profile-login-shell-startup-files/)에서 다룬 대화형/비대화형 구분과 정확히 같다 — 스크립트 파일을 실행하는 셸은 기본적으로 비대화형이므로 이 규칙에 그대로 걸린다. 스크립트 안에서도 굳이 alias를 확장시키고 싶다면 alias 정의보다 먼저 옵션을 켜야 한다.

```bash
#!/bin/bash
shopt -s expand_aliases   # 이 줄이 없으면 아래 별칭은 비대화형 셸에서 무시된다
alias ll='ls -la'
ll
```

다만 이렇게 옵션을 켜더라도, 스크립트에서 재사용 가능한 로직이 필요한 상황이라면 애초에 alias 대신 [32장: functions](/post/bashshell/bash-shell-functions-code-reuse/)를 쓰는 편이 낫다 — `expand_aliases`는 함정을 피해가는 우회로일 뿐, alias 자체가 인자를 처리하지 못한다는 근본 제약을 없애주지는 않는다.

**alias는 명령줄의 첫 단어 자리에서만 확장된다.** GNU Bash Reference Manual은 이 규칙도 정확히 못박는다.

> "The first word of each simple command, if unquoted, is checked to see if it has an alias." — GNU Bash Reference Manual, "Aliases"

따라서 파이프 뒤(`ls | ll`처럼 `ll`을 필터로 쓰려는 시도)나 다른 명령의 인자 위치(`echo ll`)에 놓인 alias 이름은 확장되지 않고 글자 그대로 처리된다. 다만 한 가지 예외가 있다 — alias로 정의한 값이 공백으로 끝나면, 그다음 단어도 다시 alias 확장 대상이 된다. 이 덕분에 `alias sudo='sudo '`처럼 마지막에 공백을 붙여 두면 `sudo ll`에서 `ll`까지 정상적으로 확장된다.

**unalias로 제거하지 않으면 세션 내내 남는다.** 별칭은 파일이 아니라 현재 셸 프로세스의 메모리 상태이므로, `unalias 이름`으로 지우거나 그 셸을 종료하기 전까지는 계속 남아 있다. 실수로 등록한 alias가 원래 명령을 계속 가리는 상태에서 디버깅에 시간을 쓰지 않으려면, `type 명령`(10장에서 다룬 것처럼) 또는 `alias 명령`으로 지금 그 이름이 별칭으로 잡혀 있는지부터 확인하는 습관이 유용하다.

## 흔한 오개념

**"alias도 함수처럼 인자를 받아 로직을 짤 수 있다"는 착각이 가장 흔하다.** `alias backup='cp $1 $1.bak'`처럼 정의해도 `$1`은 alias 호출 시 넘긴 값이 아니라, 그 alias가 확장되는 시점에 **현재 셸(또는 스크립트)의 위치 매개변수**를 그대로 참조한다. 즉 대화형 셸에서 직접 실행하면 `$1`은 대부분 비어 있어 아무 일도 일어나지 않고, 스크립트 안에서라면 그 스크립트 자신의 첫 번째 인자가 엉뚱하게 끼어든다. 인자를 받아 처리해야 한다면 이것이 이미 함수가 필요하다는 신호다.

**"alias 정의는 셸을 재시작해야 사라진다"도 정확하지 않다.** alias는 파일에 쓰여 있는 게 아니라 현재 셸 프로세스가 메모리에 들고 있는 목록일 뿐이므로, `unalias 이름` 한 줄로 그 자리에서 바로 제거된다. `.bashrc`에 alias 정의를 넣어 두었다면 그 파일 자체를 지우거나 수정해야 다음 로그인부터 사라지지만, 지금 열려 있는 셸에서 즉시 지우는 데는 `unalias`면 충분하다.

## 다음 장에서는

지금까지 셸 스크립팅 문법을 배웠다면, [36장: chmod, chown](/post/bashshell/chmod-chown-commands-file-permissions-ownership/)부터 시작하는 Part 6부터는 파일 시스템의 권한·소유권·아카이브를 다룬다. 27장(`if`/`test`)부터 이 장까지 아홉 개 챕터에 걸쳐 조건 분기·반복·입력 처리·배열·함수·오류 처리·환경 변수·별칭까지 스크립트를 짜는 데 필요한 문법을 훑었으니, 이제 그 스크립트가 실제로 다룰 대상인 파일과 디렉터리를 시스템 수준에서 관리하는 단계로 넘어간다.

## 평가 기준

- `alias`가 명령줄 첫 단어를 실행 전에 문자열로 치환하는 셸 빌트인이며, 인자를 받아 조건 분기하는 로직은 짤 수 없다는 것을 `functions`와 대조해 설명할 수 있다.
- 비대화형 셸(스크립트)에서 alias가 기본적으로 확장되지 않는 이유를 GNU Bash Reference Manual 근거와 함께 설명하고, 필요할 때 `shopt -s expand_aliases`로 우회할 수 있다.
- alias가 명령줄의 첫 단어 자리에서만 확장되며, 파이프 뒤나 인자 위치에서는 적용되지 않는다는 제약을 설명할 수 있다.
- `unalias`로 별칭을 제거하는 법과, alias가 파일이 아니라 현재 셸 세션의 상태라는 점을 설명할 수 있다.

## 참고

- [Aliases — GNU Bash Reference Manual](https://doc.guix.gnu.org/bash/latest/en/html_node/Aliases.html)
- [alias — POSIX.1-2017 Shell & Utilities](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/alias.html)
