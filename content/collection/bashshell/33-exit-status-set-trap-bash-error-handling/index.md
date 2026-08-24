---
draft: false
slug: exit-status-set-trap
title: "[Bash Shell] 33. 종료 코드와 set -e/-x, trap - 스크립트 안정성"
description: "Bash 스크립트는 기본적으로 명령이 실패해도 다음 줄로 넘어가는 관대한 실행기라는 점과, $?·set -e·set -x·set -u·set -o pipefail·trap(EXIT/ERR/INT/TERM)으로 이 동작을 통제하는 방법을 깨진 스크립트와 고친 스크립트의 실행 비교로 정리합니다."
date: 2026-08-22
lastmod: 2026-08-22
collection_order: 330
categories:
- Bash Shell
tags:
- Bash
- Shell(셸)
- Linux(리눅스)
- Terminal
- Command
- Automation(자동화)
- Error-Handling(에러처리)
- Debugging(디버깅)
- Signal
- Process
- Best-Practices
- Pitfalls(함정)
- Guide(가이드)
- Tutorial(튜토리얼)
- Reference(참고)
- Beginner
- Exit-Status
- 종료코드
- Set-Builtin
- Trap
- ERR-Trap
- Errexit
- Xtrace
- Nounset
- Pipefail
- Shell-Scripting
- 시그널핸들러
- Script-Robustness
image: "wordcloud.png"
---

Bash 스크립트가 중간에 실패했을 때 셸이 실제로 무엇을 하는지, 그리고 그 동작을 개발자가 어떻게 통제할지를 다룬다. 종료 코드(`$?`)를 확인하는 법부터 `set -e`/`set -x`/`set -u`/`set -o pipefail`로 실패 처리 방식을 바꾸는 법, `trap`으로 종료·신호 시점에 코드를 실행하는 법까지 실습 예제로 정리한다.

## 이 장을 읽기 전에

직전 챕터인 [32장: functions](/post/bashshell/functions/)에서 함수를 정의하고 호출하는 법을 다뤘다. `trap`에 등록하는 핸들러는 형태상 명령 문자열이지만, 실행 시점이 되면 셸이 특정 이벤트(신호 수신, 스크립트 종료 등)를 만났을 때 호출하는 콜백이라는 점에서 사실상 함수와 같은 역할을 한다 — 함수 개념 없이 곧바로 `trap`을 배우면 "왜 이 문자열이 지금이 아니라 나중에 실행되는가"를 이해하기 어렵다. 이 장은 Part 5(셸 스크립팅)의 마지막 안정성 단계로, 종료 코드부터 `set` 옵션, `trap`까지 셸 스크립트가 실패를 다루는 방식 전체를 묶어서 다룬다.

난이도는 중급이다. `if`/`for`([27–28장](/post/bashshell/if-test/))로 조건·반복을 다룰 수 있고 함수(32장)를 정의할 수 있다고 가정한다. 파이프라인([19장: pipe](/post/bashshell/pipe/))의 기본 개념도 `set -o pipefail`을 이해하는 데 필요하다.

**다루지 않는 것**: 실행 중인 프로세스에 터미널에서 직접 시그널을 보내는 것(`kill -9`, `kill -TERM` 등)은 [25장: kill, jobs](/post/bashshell/kill-jobs/)에서 이미 다뤘다. 이 장은 그 반대편 — 스크립트 "안쪽"에서 신호나 종료 이벤트를 받아 반응하는 코드(`trap`)만 다룬다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| 입문 | 개요 + 정신 모델, 핵심 개념의 `$?`·`set -e` | 스크립트가 실패해도 기본적으로 계속 진행한다는 사실을 이해하고 `$?`로 성공·실패를 확인할 수 있다 |
| 중급 | 핵심 개념 전체, 실전 예제 | `set -euo pipefail`을 실전 스크립트에 적용하고 `trap`으로 정리 작업을 등록할 수 있다 |
| 심화 | 주의사항·함정, 흔한 오개념 | `set -e`가 발동하지 않는 예외 케이스를 코드에서 알아보고, CI/배포 스크립트에서 안전하게 활용할 수 있다 |

## 개요 + 정신 모델

Bash는 기본적으로 각 명령의 종료 코드를 검사하지 않고, 실패한 명령이 있어도 스크립트의 다음 줄로 그냥 넘어가는 관대한(permissive) 실행기다. 대화형 셸에서는 이 기본값이 합리적이다 — 오타로 명령 하나가 실패했다고 터미널 세션 전체가 종료돼 버리면 오히려 불편하다. 하지만 자동화 스크립트에서는 이 관대함이 그대로 위험으로 바뀐다. 백업 스크립트의 `tar` 명령이 디스크 공간 부족으로 실패해도 스크립트는 이를 모른 채 다음 줄의 `rm -rf`를 그대로 실행해 원본 데이터를 지워버릴 수 있다.

`set` 빌트인은 이 기본 동작을 바꾸는 스위치판이다 — 어떤 상황에서 셸이 "멈춰야" 하는지, 어떤 상황을 "에러"로 취급할지를 옵션 하나하나로 켜고 끌 수 있다. `trap`은 이 스위치판과는 별개로, 스크립트가 종료되거나 신호를 받는 순간에 실행할 코드를 미리 등록해 두는 메커니즘이다. 이 둘을 조합하면 "실패하면 즉시 멈추고, 멈추기 직전에 반드시 정리 작업을 실행한다"는 안정적인 스크립트 골격을 만들 수 있다.

## 핵심 개념

### 종료 코드($?)

모든 명령은 종료할 때 0–255 사이의 정수를 운영체제에 반환하며, 셸은 이를 특수 변수 `$?`에 저장한다. 관례상 `0`은 성공을, 0이 아닌 값은 실패를 의미하지만 그 구체적인 의미는 명령마다 다르게 정의한다(예: `grep`은 매치 없음을 `1`로, 문법 오류를 `2` 이상으로 구분한다). `$?`는 직전에 실행된 명령 하나의 종료 코드만 담고 있으므로, 확인하려면 실패할 수 있는 명령 바로 다음 줄에서 검사해야 한다 — 다른 명령을 하나라도 더 실행하면 그 값으로 덮어써진다.

```bash
grep "ERROR" /var/log/app.log
echo "grep 종료 코드: $?"

ls /no/such/directory 2>/dev/null
echo "ls 종료 코드: $?"
```

### set -e (errexit) — 실패 시 즉시 종료

`set -e`(또는 `set -o errexit`)를 켜면 파이프라인이 0이 아닌 상태로 종료될 때 셸이 즉시 그 스크립트(또는 서브셸)를 종료한다. 목적은 실패를 조용히 넘기지 않고 그 자리에서 멈추게 만드는 것이다.

```bash
#!/bin/bash
set -e
echo "1단계 시작"
false            # 여기서 스크립트가 즉시 종료된다
echo "이 줄은 실행되지 않는다"
```

### set -x (xtrace) — 실행 추적

`set -x`(또는 `set -o xtrace`)는 셸이 각 단순 명령을 실행하기 직전, 변수·명령 치환까지 모두 확장된 실제 형태를 `+`로 시작하는 줄로 표준 오류에 출력한다. 디버깅할 때 "이 변수가 실제로 어떤 값으로 치환되어 실행됐는가"를 눈으로 바로 확인할 수 있다.

```bash
set -x
name="world"
echo "hello, $name"
set +x
```

출력은 다음과 같다.

```text
+ name=world
+ echo 'hello, world'
hello, world
```

### set -u (nounset) — 미정의 변수 참조를 에러로

`set -u`(또는 `set -o nounset`)는 정의되지 않은 변수를 참조하면 에러로 취급하고 스크립트를 종료한다. 변수 이름 오타나, 인자를 안 받았는데 `$1`을 그대로 참조하는 실수를 조기에 잡아낸다.

```bash
set -u
echo "빌드 대상: $TARGET_DIR"   # TARGET_DIR을 정의한 적이 없다면 여기서 즉시 종료된다
```

### set -o pipefail — 파이프라인 중간 실패까지 잡기

`set -e`만으로는 파이프라인 전체를 안전하게 감시하지 못한다. 파이프라인의 종료 코드는 기본적으로 **마지막 명령**의 종료 코드이므로, 앞쪽 명령이 실패해도 마지막 명령이 성공하면 전체 파이프라인은 성공으로 간주된다. `set -o pipefail`을 켜면 파이프라인 안의 명령 중 하나라도 실패했을 때 그중 가장 오른쪽에서 실패한 명령의 코드를 파이프라인 전체의 종료 코드로 채택해, `set -e`가 그 실패를 실제로 감지할 수 있게 만든다.

```bash
set -e
false | true
echo "pipefail 없이는 여기 도달함: $?"   # true가 마지막이라 파이프라인 전체가 성공(0) 취급된다

set -o pipefail
false | true                              # 이번엔 파이프라인 전체가 실패로 간주돼 즉시 종료된다
echo "여기는 도달하지 않는다"
```

### trap — 종료·신호 핸들러 등록

`trap '핸들러' 신호명...`은 셸이 지정한 신호를 받거나 특정 이벤트가 발생했을 때 실행할 명령(문자열)을 등록한다. `EXIT`는 스크립트가 어떤 이유로 끝나든(정상 종료, `set -e`에 의한 강제 종료, 신호 수신) 마지막에 정확히 한 번 실행되는 가장 안전한 정리 지점이라 임시 파일 삭제나 잠금 해제에 자주 쓴다. `ERR`은 (뒤에서 다룰 `-e`와 동일한 예외 규칙 아래) 명령이 실패할 때마다 실행된다. `INT`(Ctrl+C, `SIGINT`)와 `TERM`(`kill`의 기본 신호)은 외부에서 스크립트를 중단시키려는 시도에 반응할 때 쓴다.

```bash
tmpfile=$(mktemp)
trap 'rm -f "$tmpfile"; echo "임시 파일 정리 완료"' EXIT
trap 'echo "명령 실패 감지"' ERR
trap 'echo "Ctrl+C 감지, 정리 후 종료합니다"; exit 130' INT

echo "$tmpfile 사용 중..."
```

## 실전 예제: 에러를 무시하는 스크립트 고치기

### 깨진 스크립트

다음은 로그 디렉터리를 압축해 백업한 뒤 원본을 비우는, 흔히 볼 수 있는 형태의 스크립트다.

```bash
#!/bin/bash
# broken-backup.sh — set -e 없이 작성된 백업 스크립트
SRC="/var/log/myapp"
DEST="/backup/myapp-$(date +%F).tar.gz"

tar -czf "$DEST" "$SRC"
rm -rf "${SRC:?}"/*
echo "백업 완료: $DEST"
```

### 원인

`$SRC` 디렉터리가 없거나, 권한이 없거나, 대상 디스크 공간이 부족해 `tar`가 실패해도 이 스크립트는 이를 전혀 알아채지 못한다. 앞서 "개요 + 정신 모델"에서 설명했듯 Bash의 기본 동작은 각 명령의 종료 코드를 확인하지 않고 무조건 다음 줄로 진행하는 것이므로, `tar`가 0이 아닌 코드로 끝나도 셸은 이를 검사하지 않고 곧바로 `rm -rf`를 실행한다. 결과적으로 백업은 만들어지지 않았는데 원본 로그는 이미 삭제된, 되돌릴 수 없는 데이터 손실이 발생한다.

### 고친 버전

```bash
#!/bin/bash
# fixed-backup.sh — set -euo pipefail + trap으로 안전하게 만든 버전
set -euo pipefail
trap 'echo "[cleanup] 스크립트 종료(코드 $?): 정리 작업 실행" >&2' EXIT

SRC="/var/log/myapp"
DEST="/backup/myapp-$(date +%F).tar.gz"

tar -czf "$DEST" "$SRC"
rm -rf "${SRC:?}"/*
echo "백업 완료: $DEST"
```

`set -e`가 `tar` 실패 즉시 스크립트를 끝내므로 `rm -rf`에는 아예 도달하지 않는다. `set -u`는 `$SRC`·`$DEST`가 오타로 빈 문자열이 되는 사고를 조기에 잡고, `set -o pipefail`은 이 스크립트에 파이프라인이 추가되더라도 중간 실패를 놓치지 않도록 미리 대비해 둔 것이다. `trap ... EXIT`은 성공이든 `set -e`에 의한 강제 종료든 상관없이 마지막에 한 번 실행되어 종료 코드를 로그로 남긴다.

### 검증 절차

두 버전의 차이는 `$SRC`를 존재하지 않는 경로로 바꿔 `tar`를 의도적으로 실패시켜 재현할 수도 있지만, 아래처럼 `false`로 최소 재현만 따로 떼어내 셸에서 직접 확인하는 편이 원리를 이해하기 빠르다.

```bash
# 1) set -e 없이는 실패해도 다음 줄이 그대로 실행된다
bash -c 'false; echo "다음 줄 실행됨, 직전 종료 코드: $?"'

# 2) set -e를 걸면 실패 즉시 종료되어 다음 줄이 실행되지 않는다
bash -c 'set -e; false; echo "이 줄은 출력되지 않는다"'
echo "위 서브셸의 종료 코드: $?"

# 3) trap EXIT은 정상 종료·set -e에 의한 강제 종료 모두에서 실행된다
bash -c 'trap "echo cleanup 실행됨" EXIT; set -e; false'

# 4) bash -x로 실행 추적을 켜면 set -e가 정확히 어느 줄에서 스크립트를 끊었는지 눈으로 확인할 수 있다
bash -x -c 'set -e; echo before; false; echo after'
```

1)은 `false` 다음 줄까지 실행되어 `$?`가 `1`로 출력되는 것을 보여준다. 2)는 `set -e` 때문에 `false` 줄에서 곧바로 끝나 뒤의 `echo`가 출력되지 않고, 서브셸 자체의 종료 코드도 `1`이 되는 것을 보여준다. 3)은 `set -e`로 강제 종료되는 상황에서도 `trap ... EXIT` 핸들러가 반드시 실행됨을 확인한다. 4)는 `bash -x`의 추적 로그에서 `+ false` 다음 줄로 `+ echo after`가 찍히지 않는 것으로, 정확히 어디서 멈췄는지 확인하는 절차다.

## 주의사항·함정

**`set -e`가 발동하지 않는 잘 알려진 예외**: `set -e`는 "명령이 실패하면 무조건 종료한다"가 아니다. GNU Bash Reference Manual은 다음 경우에는 실패해도 셸이 종료하지 않는다고 명시한다.

> "The shell does not exit if the command that fails is part of the command list immediately following a while or until keyword, part of the test in an if statement, part of any command executed in a && or || list except the command following the final && or ||, any command in a pipeline but the last, or if the command's return value is being inverted with !." — GNU Bash Reference Manual, "The Set Builtin"

즉 `while`/`until` 뒤에 오는 명령 리스트의 일부, `if` 문의 테스트 부분, `&&`/`||` 리스트에서 마지막이 아닌 명령, 파이프라인에서 마지막이 아닌 명령(`pipefail` 상태에 따라 달라짐), `!`로 반전된 명령은 실패해도 스크립트를 끊지 않는다.

```bash
set -e
if false; then echo "참"; fi     # if의 조건절이라 종료되지 않는다
false && echo "출력 안 됨"        # && 리스트의 첫 명령이라 종료되지 않는다
false || echo "폴백 실행됨"       # || 리스트의 첫 명령이라 종료되지 않는다
! false                           # !로 반전됐으므로 종료되지 않는다
echo "여기까지 전부 살아서 도달한다"
```

`ERR` 트랩도 동일한 예외 규칙을 따른다.

> "The ERR trap is not executed if the failed command is part of the command list immediately following an until or while keyword, part of the test following the if or elif reserved words, part of a command executed in a && or || list except the command following the final && or ||, any command in a pipeline but the last, or if the command's return status is being inverted using !." — GNU Bash Reference Manual, "Bourne Shell Builtins"

**`trap`은 서브셸에 상속되지 않는다**: `trap`으로 등록한 핸들러는 그 셸(또는 스크립트) 안에서만 유효하다.

> "Trapped signals that are not being ignored are reset to their original values in a subshell or subshell environment when one is created." — GNU Bash Reference Manual, "Bourne Shell Builtins"

즉 `(...)`로 만든 서브셸이나 `$(...)` 명령 치환 내부에서는 부모 셸에서 등록한 `trap`이 그대로 상속되지 않고 원래 값(대부분 기본 동작)으로 리셋된다.

**`local`과 명령 치환을 한 줄에 합치면 `set -e`가 실패를 놓친다**: `local x=$(failing_command)`처럼 쓰면, 셸이 실제로 검사하는 종료 코드는 `local` 자체의 것이지 그 안의 명령 치환 결과가 아니다. `local`은 변수명이 유효한 한 거의 항상 성공하므로, `failing_command`가 실패해도 `set -e`가 이를 감지하지 못하고 조용히 넘어간다.

```bash
set -e
get_value() { return 1; }

broken() {
  local result=$(get_value)   # get_value가 실패해도 set -e가 감지하지 못한다
  echo "여기 도달함: $result"
}

fixed() {
  local result
  result=$(get_value)         # 선언과 대입을 분리하면 실패가 그대로 감지된다
  echo "여기 도달 안 함"
}

broken
fixed
```

## 흔한 오개념

<strong>"`set -e`를 걸면 모든 실패에서 스크립트가 멈춘다"</strong>는 가장 흔한 오해다. 실제로는 위에서 정리한 예외(파이프라인 중간, `if`/`while` 조건, `&&`/`||`, `!` 반전) 때문에 놓치는 실패가 흔하다. `set -e`는 "관대한 기본 동작을 없앤다"가 아니라 "관대한 기본 동작에 몇 가지 예외적인 정지 조건을 추가한다"에 더 가깝다.

<strong>"`trap` 핸들러 안에서는 `$?`가 항상 원래 실패의 종료 코드를 가리킨다"</strong>도 틀리기 쉽다. 핸들러 안에서 명령을 두 개 이상 실행하면, 뒤쪽 명령에서 참조하는 `$?`는 스크립트를 종료시킨 원래 실패의 코드가 아니라 핸들러 안에서 방금 실행된 명령 자신의 코드로 이미 바뀌어 있다. 원래 종료 코드를 남기려면 핸들러의 첫 명령으로 즉시 변수에 저장해 둬야 한다.

```bash
trap 'code=$?; echo "정리 작업 실행"; echo "원래 종료 코드: $code"; exit "$code"' EXIT
```

## 다음 장에서는

[34장: echo, export, env](/post/bashshell/echo-export-env/)에서는 표준 출력으로 값을 내보내는 `echo`, 자식 프로세스에 변수를 물려주는 `export`, 현재 환경을 확인·조작하는 `env`를 다룬다. 이 장이 종료 코드와 `trap`으로 스크립트의 "실행 흐름"을 통제하는 법이었다면, 다음 장은 그 스크립트가 다른 프로세스와 값을 주고받는 "환경"을 다룬다.

## 평가 기준

- `$?`로 직전 명령의 종료 코드를 확인하고, 0과 0이 아닌 값의 의미 차이를 설명할 수 있다.
- `set -e`, `set -x`, `set -u`, `set -o pipefail`이 각각 무엇을 통제하는지 구분하고 스크립트에 조합해 적용할 수 있다.
- `set -e`가 발동하지 않는 예외 케이스(파이프라인 중간, `if`/`while` 조건, `&&`/`||`, `!` 반전)를 나열하고 코드에서 알아볼 수 있다.
- `trap`으로 `EXIT`/`ERR`/`INT`/`TERM` 핸들러를 등록하고, 그 핸들러가 서브셸에는 상속되지 않는다는 점을 설명할 수 있다.
- 실패를 무시하는 스크립트와 `set -euo pipefail` + `trap`으로 고친 스크립트의 차이를 실제로 실행해 검증할 수 있다.

## 참고

- [The Set Builtin — GNU Bash Reference Manual](https://doc.guix.gnu.org/bash/latest/en/html_node/The-Set-Builtin.html)
- [Bourne Shell Builtins — GNU Bash Reference Manual](https://doc.guix.gnu.org/bash/latest/en/html_node/Bourne-Shell-Builtins.html)
