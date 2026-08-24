---
draft: false
slug: echo-export-env-commands-shell-variables
title: "[Bash Shell] 34. echo, export, env - 출력과 환경변수"
description: "echo는 단순 출력, export는 셸 변수를 자식 프로세스 환경으로 승격시키는 도구, env는 현재 환경을 나열·변경해 명령을 실행하는 도구라는 정신 모델과 함께 echo -e 이스케이프의 이식성 문제, export 상속 원리, env -i 디버깅 기법을 정리합니다."
date: 2026-03-15
lastmod: 2026-08-24
collection_order: 340
categories:
- Bash Shell
tags:
- Bash
- Shell(셸)
- Linux(리눅스)
- Terminal
- Command
- Automation(자동화)
- Process
- File-System
- Environment
- Tutorial(튜토리얼)
- Guide(가이드)
- Reference(참고)
- Beginner
- Configuration(설정)
- Inheritance(상속)
- Pitfalls(함정)
- Quick-Reference
- echo
- export
- env
- 환경변수
- PATH
- Shell-Variable
- Environment-Variable
- Standard-Output
- POSIX
- Printf
- Portability
- Shell-Builtin
- Child-Process
- env-i
image: "wordcloud.png"
---

`echo`는 표준 출력에 문자열을 내보낼 뿐인 가장 단순한 명령이고, `export`는 셸이 관리하는 변수를 자식 프로세스가 물려받는 **환경**으로 승격시키는 도구이며, `env`는 그 환경 자체를 나열하거나 일시적으로 바꿔 명령을 실행하는 도구다. 셋 다 짧고 흔히 쓰는 명령이지만, "셸 변수"와 "환경변수"가 서로 다른 것이라는 구분을 모르면 `export` 없이 스크립트를 작성해 놓고 왜 하위 프로세스에서 변수가 비어 있는지 몇 시간을 헤매게 된다.

## 이 장을 읽기 전에

직전 챕터인 [33장: 종료 코드와 set -e/-x, trap](/post/bashshell/exit-status-set-trap-bash-error-handling/)에서는 스크립트 "안쪽"에서 명령의 실패를 감지하고 실행 흐름을 통제하는 법을 다뤘다. 이 장은 관점을 바꿔 스크립트가 **다른 프로세스와 값을 어떻게 주고받는지**를 다룬다 — `echo`로 값을 화면에 내보내는 것과 `export`로 값을 자식 프로세스에 넘기는 것은 목적지가 전혀 다른 별개의 동작이라는 구분이 이 장의 핵심이다.

난이도는 입문–중급이다. 변수에 값을 대입하는 기본 문법(`name=value`)과 `$변수`로 값을 참조하는 법을 이미 안다고 가정한다. **다루지 않는 것**: 변수를 함수 안에서만 유효하게 선언하는 법(`local`)과 배열·매개변수 확장은 [31장: 배열, 셸 확장](/post/bashshell/bash-arrays-brace-parameter-expansion/)과 [32장: functions](/post/bashshell/bash-shell-functions-code-reuse/)에서 이미 다뤘다. 명령어 자체를 다른 문자열로 치환하는 `alias`는 다음 [35장: alias](/post/bashshell/alias-command-shell-command-shortcuts/)에서 다룬다 — `export`가 "값"을 자식에게 넘기는 것이라면 `alias`는 "명령 이름"을 셸 자신 안에서 바꿔치는 것이라 성격이 다르다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| 입문 | 개요 + 정신 모델, 사용법·옵션의 echo/export | `echo`로 출력하고 `export`로 자식 프로세스에 변수를 넘길 수 있다 |
| 중급 | 사용법·옵션 전체, 예시, 주의사항·함정 | `env`로 환경을 확인·수정하고, `echo -e`의 이식성 문제를 피해 `printf`를 선택할 수 있다 |
| 심화 | 주의사항·함정의 `env -i`, 흔한 오개념 | `env -i`로 클린 환경을 만들어 스크립트의 환경변수 의존성을 진단할 수 있다 |

## 개요 + 정신 모델

세 명령은 서로 다른 층위에서 동작한다. `echo`는 인자로 받은 문자열을 표준 출력으로 흘려보내는, 프로세스 경계를 넘지 않는 가장 단순한 출력기다. 화면에 뭔가를 찍는다는 점에서 디버깅과 로그에 자주 쓰이지만, 그 값은 `echo`를 실행한 셸 바깥으로는 나가지 않는다.

`export`는 이야기가 다르다. 셸은 두 종류의 이름-값 저장소를 동시에 관리한다 — 그 셸 프로세스 안에서만 보이는 **셸 변수**와, 새로 만드는 모든 자식 프로세스에 자동으로 복사되는 **환경변수**다. `name=value`로 대입한 값은 기본적으로 셸 변수일 뿐이라 그 셸이 실행하는 다른 프로그램(스크립트, 바이너리, 서브셸)은 그 값을 전혀 볼 수 없다. `export name`은 이 변수를 환경변수 쪽으로 옮겨, 이 시점 이후 만들어지는 모든 자식 프로세스가 상속받게 만드는 **승격 스위치**다. 이 상속은 반드시 부모에서 자식으로만 흐르는 단방향이다 — 자식 프로세스가 자기 환경변수를 아무리 바꿔도 그 변화는 부모 셸로 거슬러 올라가지 않는다. 각 프로세스는 부모로부터 받은 환경의 **복사본**을 갖고 시작하기 때문이다.

`env`는 이 환경 자체를 다루는 도구다. 인자 없이 실행하면 현재 프로세스가 물려받은 환경변수 전체를 나열하고, `name=value` 쌍과 명령을 함께 주면 그 변수들만 추가·덮어쓴 환경에서 명령 하나를 실행한다. `env -i`는 상속받은 환경을 아예 비우고 시작하는 특수한 경우로, "이 스크립트가 실제로 어떤 환경변수에 의존하는지"를 검증하는 도구로 쓰인다. 세 명령을 하나로 묶으면, `echo`는 출력, `export`는 상속 설정, `env`는 그 상속된 결과를 확인·조작하는 도구라는 역할 분담이 드러난다.

## 사용법 · 옵션

### echo

```bash
echo [-neE] [문자열...]
```

| 옵션 | 설명 |
|---|---|
| `-n` | 끝에 붙는 줄바꿈을 생략한다 |
| `-e` | `\n`, `\t` 등 백슬래시 이스케이프 시퀀스 해석을 켠다 |
| `-E` | 이스케이프 해석을 끈다(기본값이 해석하도록 바뀐 시스템에서 되돌릴 때 사용) |

Bash 빌트인 `echo`는 기본적으로 이스케이프를 해석하지 않지만, `shopt -s xpg_echo`로 기본 동작 자체를 바꿀 수 있다. 인자가 `-`로 시작하면 옵션으로 해석을 시도하므로 임의 문자열을 안전하게 출력하려면 `--`가 아니라(← `echo`는 `--`를 옵션 종료 표시로 인식하지 않는다) `printf '%s\n' "$str"`을 쓰는 편이 안전하다.

### export

```bash
export [-fnp] [name[=value]]...
```

| 옵션 | 설명 |
|---|---|
| `-p` | 현재 내보내진 변수 목록을 `declare -x` 형식으로 출력한다 |
| `-n` | 지정한 이름을 환경에서 제외한다(변수 자체는 셸 변수로 남는다) |
| `-f` | 이름이 변수가 아니라 함수임을 가리킨다(함수를 자식 프로세스에 내보낼 때) |

`value`를 생략하고 `export name`만 쓰면 이미 존재하는 셸 변수를 환경으로 승격만 시키고, `export name=value`처럼 대입까지 함께 하면 값 설정과 승격을 한 번에 처리한다.

### env

```bash
env [옵션] [name=value...] [명령 [인자...]]
```

| 옵션 | 설명 |
|---|---|
| `-i`, `--ignore-environment` | 상속받은 환경을 무시하고 빈 환경에서 시작한다 |
| `-u name`, `--unset=name` | 실행할 환경에서 특정 변수 하나를 제거한다 |
| `-0`, `--null` | 환경변수 나열 시 줄바꿈 대신 NUL 문자로 구분한다(값에 줄바꿈이 섞여도 안전하게 파싱 가능) |
| `--` | 이후 인자를 옵션으로 해석하지 않고 실행할 명령으로 취급한다 |

인자 없이 `env`만 실행하면 `-i`도 `name=value`도 명령도 주지 않은 것이므로 현재 환경을 그대로 나열하는 동작이 된다.

## 예시

```bash
# 1) 기본 출력과 변수 참조
echo "빌드 대상: $TARGET_DIR"

# 2) 줄바꿈 없이 진행 상황 표시
echo -n "설치 중... "; sleep 1; echo "완료"

# 3) 이스케이프가 필요하면 echo -e보다 printf를 우선한다
printf 'name\tstatus\n'

# 4) 셸 변수는 자식 프로세스에서 안 보인다
MY_VAR=hello
bash -c 'echo "자식에서 본 값: [$MY_VAR]"'   # 빈 값이 출력된다

# 5) export로 승격하면 자식 프로세스에서 보인다
export MY_VAR=hello
bash -c 'echo "자식에서 본 값: [$MY_VAR]"'   # hello가 출력된다

# 6) 대입과 export를 한 줄로
export BUILD_ENV=production

# 7) 현재 환경변수 전체 나열, grep으로 필터링
env | grep -i path

# 8) 이번 실행에만 임시로 변수를 덮어써 명령 실행 (셸 변수를 바꾸지 않음)
env LANG=C sort file.txt

# 9) 클린 환경에서 스크립트를 실행해 숨은 환경변수 의존성을 찾는다
env -i PATH=/usr/bin:/bin bash myscript.sh

# 10) export -p로 지금 내보내진 변수 목록만 확인
export -p | grep MY_VAR
```

## 주의사항·함정

**`echo -e`의 이스케이프 처리는 셸·구현체마다 매우 비일관적이다.** POSIX 표준은 `echo`를 이식성 있게 쓸 방법이 사실상 없다고 명시한다.

> "It is not possible to use echo portably across all POSIX systems unless both -n (as the first argument) and escape sequences are omitted." — The Open Group Base Specifications, *echo*

같은 표준 문서는 대안으로 `printf`를 명시적으로 권장한다. "New applications are encouraged to use printf instead of echo." 리눅스 GNU coreutils의 `echo(1)` 매뉴얼도 옵션처럼 보이는 문자열을 출력할 때 문제가 생기는 것을 피하려면 `printf`를 쓰라고 조언한다.

> "Consider using the printf(1) command instead, as it avoids problems when outputting option-like strings." — GNU coreutils, `echo(1)` man page

원인은 역사적으로 System V 계열 `echo`는 옵션 없이 이스케이프를 항상 해석했고 BSD 계열 `echo`는 `-n`만 지원하고 이스케이프는 해석하지 않는 등, 두 계보가 서로 호환되지 않는 동작을 각자 표준처럼 굳혔기 때문이다. Bash 빌트인은 기본적으로 BSD에 가깝게 동작하지만 `shopt -s xpg_echo`나 `sh` 호환 모드로 실행하면 동작이 바뀐다 — 즉 같은 `echo -e "a\nb"`라도 실행 환경에 따라 백슬래시가 그대로 출력되거나 줄바꿈으로 해석되거나 둘 다 벌어질 수 있다. 이스케이프가 필요한 출력은 항상 `printf`로 대체하는 편이 안전하다.

**`export`하지 않은 변수는 자식 프로세스에서 보이지 않는다.** 셸이 실행하는 모든 자식 프로세스(서브셸, `bash script.sh`처럼 실행한 스크립트, `curl`·`python` 같은 외부 바이너리 전부)는 부모 셸의 환경을 물려받아 시작하지만, 그 상속은 항상 부모→자식 방향으로만 흐른다.

> "The environment for any simple command or function may be augmented temporarily by prefixing it with parameter assignments... Executed commands inherit the environment." — GNU Bash Reference Manual, "Environment"

`export`로 내보내지 않은 셸 변수는 애초에 자식이 물려받을 환경에 포함되지 않으므로, `MY_VAR=hello; some_script.sh`처럼 쓰면 `some_script.sh` 안에서 `$MY_VAR`는 항상 비어 있다. 반대로 자식 프로세스 안에서 물려받은 환경변수 값을 바꾸거나 `unset`해도 그 변화는 부모 셸로 절대 되돌아가지 않는다 — 각 프로세스는 시작 시점에 부모 환경의 복사본을 받을 뿐이기 때문이다.

**`env -i`로 클린 환경을 만들어 환경변수 의존성을 디버깅한다.** 스크립트가 실제로는 `$PATH`나 사용자 정의 환경변수 없이는 동작하지 않는데, 개발자의 셸에는 우연히 그 값들이 이미 설정돼 있어서 문제를 못 알아채는 경우가 흔하다. `env -i`는 상속받은 환경 전부를 버리고 지정한 것만 남긴 빈 환경에서 명령을 실행하므로, CI나 cron처럼 환경이 최소화된 곳에서 스크립트가 실패하는 이유를 로컬에서 미리 재현할 수 있다.

```bash
# 개발자의 셸에서는 우연히 성공하지만
myscript.sh

# 클린 환경에서는 숨어 있던 의존성이 드러난다
env -i PATH=/usr/bin:/bin myscript.sh
```

## 흔한 오개념

<strong>"셸 변수와 환경변수는 같은 것이다"</strong>는 가장 흔한 오해다. 실제로는 셸이 관리하는 두 개의 서로 다른 저장소이며, `export`는 그 경계를 넘어 셸 변수를 환경변수 쪽으로 옮기는 명시적인 동작이다. `set`이나 `declare -p`로 보이는 목록에는 두 종류가 섞여 있지만, `export -p` 또는 `env`로 보이는 목록에는 실제로 자식 프로세스에 전달되는 환경변수만 나온다.

<strong>"자식 프로세스에서 `export`한 값을 바꾸면 부모 셸에도 반영된다"</strong>도 자주 하는 착각이다. 서브셸이나 실행한 스크립트 안에서 환경변수를 아무리 수정·추가해도 그 변화는 자신과 자신의 자식에게만 적용될 뿐, 자신을 실행시킨 부모 프로세스의 환경에는 어떤 경로로도 되돌아가지 않는다. 부모 셸의 값을 바꾸고 싶다면 `export`가 아니라 `source`(`.`)로 그 셸 자신 안에서 스크립트를 실행해야 한다.

## 다음 장에서는

[35장: alias](/post/bashshell/alias-command-shell-command-shortcuts/)에서는 명령줄의 첫 단어를 다른 문자열로 치환하는 `alias`를 다룬다. 이 장이 값을 자식 프로세스에 넘기는 법(`export`)을 다뤘다면, 다음 장은 셸 자신의 명령 해석 단계에서 이름 자체를 바꿔치는 훨씬 얕은 층위의 치환을 다룬다 — 둘의 차이를 비교하면 셸이 명령을 처리하는 여러 층위를 더 분명히 구분할 수 있다.

## 평가 기준

- `echo`, `export`, `env`가 각각 어떤 층위(출력, 프로세스 간 상속, 환경 조회·조작)에서 동작하는지 설명할 수 있다.
- 셸 변수와 환경변수의 차이를, `export` 전후로 자식 프로세스에서 값이 보이는지 여부로 직접 검증할 수 있다.
- `echo -e`의 이스케이프 처리가 왜 이식성이 없는지 설명하고, 이스케이프가 필요한 상황에서 `printf`를 선택할 수 있다.
- 환경 상속이 부모→자식 단방향이라는 원리를 근거로, 자식 프로세스에서의 변경이 부모에 반영되지 않는 이유를 설명할 수 있다.
- `env -i`로 클린 환경을 만들어 스크립트의 숨은 환경변수 의존성을 진단할 수 있다.

## 참고

- [echo — The Open Group Base Specifications (POSIX.1-2017)](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/echo.html)
- [echo(1) — Linux manual page](https://man7.org/linux/man-pages/man1/echo.1.html)
- [Bash Builtins — GNU Bash Reference Manual](https://doc.guix.gnu.org/bash/latest/en/html_node/Bash-Builtins.html)
- [Bourne Shell Builtins — GNU Bash Reference Manual](https://doc.guix.gnu.org/bash/latest/en/html_node/Bourne-Shell-Builtins.html)
- [Environment — GNU Bash Reference Manual](https://doc.guix.gnu.org/bash/latest/en/html_node/Environment.html)
- [env(1) — Linux manual page](https://man7.org/linux/man-pages/man1/env.1.html)
