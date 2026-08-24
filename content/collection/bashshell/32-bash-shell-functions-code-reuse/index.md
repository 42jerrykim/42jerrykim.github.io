---
draft: false
slug: bash-shell-functions-code-reuse
title: "[Bash Shell] 32. functions - 함수와 코드 재사용"
description: "Bash 함수는 이름 붙은 명령 그룹으로 위치 매개변수를 받고 return으로 0–255 종료 코드만 반환한다는 점, local 없이는 전역 스코프를 오염시킨다는 점을 예제와 GNU Bash Reference Manual 인용으로 정리합니다."
date: 2026-03-15
lastmod: 2026-08-24
collection_order: 320
categories:
- Bash Shell
tags:
- Bash
- Shell(셸)
- Linux(리눅스)
- Terminal
- Command
- Automation(자동화)
- Best-Practices
- Pitfalls(함정)
- Guide(가이드)
- Tutorial(튜토리얼)
- Reference(참고)
- Beginner
- Scope(스코프)
- Modularity
- Readability
- Maintainability
- Error-Handling(에러처리)
- Recursion(재귀)
- Refactoring(리팩토링)
- Software-Engineering(소프트웨어공학)
- Programming-Language(프로그래밍언어)
- Process
- Shell-Scripting
- function
- 함수
- local
- return
- 인자
- Positional-Parameters
- Return-Status
- Global-Variable
- 지역변수
- 전역변수
image: "wordcloud.png"
---

Bash **함수**는 반복되는 명령을 이름으로 묶어 호출할 수 있게 하는 코드 재사용 단위다. 다른 언어의 함수와 달리 **값을 리턴하지 않고 0–255 사이의 종료 코드만 반환**하며, 문자열이나 자료구조를 실제로 돌려주려면 `echo`와 명령 치환을 조합해야 한다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [31장: 배열과 셸 확장](/post/bashshell/bash-arrays-brace-parameter-expansion/)에서 배열과 매개변수 확장으로 여러 값을 다루는 법을 익힌 뒤 이어진다. 함수 인자를 받을 때 `$@`를 배열처럼 순회하거나 배열을 함수에 넘기는 상황이 자주 나오므로, 배열 문법에 대한 감이 있으면 이 장의 예제를 더 수월하게 읽을 수 있다. 또한 [27장: if, test](/post/bashshell/if-test-command-bash-conditional-statements/)와 [28장: for, while](/post/bashshell/for-while-loop-bash-shell-scripting/)의 제어 구조를 함수 본문 안에서 그대로 재사용하므로, 조건문·반복문 문법을 이미 안다고 가정한다.

**이 장의 깊이**: **입문–중급** 난이도다. 함수 정의·호출·인자 처리·`local` 스코프까지 스크립트를 함수 단위로 구조화하는 데 필요한 범위를 다룬다. **다루지 않는 것**: 함수를 종료 코드가 아니라 스크립트 전체 실행 흐름 통제(`set -e`, `trap`)와 연결하는 내용은 [33장: 종료 코드와 set -e/-x, trap](/post/bashshell/exit-status-set-trap-bash-error-handling/)에서 다룬다. 함수 정의를 파일 밖으로 분리해 여러 스크립트에서 재사용하는 방법(`source`를 통한 라이브러리화)은 이 장의 범위를 넘어가므로 간단히만 언급한다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| 입문 | 개요 + 정신 모델, 핵심 개념의 "정의와 호출"·"인자" | 함수를 정의·호출하고 `$1`, `$2`, `$#`로 인자를 받을 수 있다 |
| 중급 | 핵심 개념 전체, 예시 | `local`로 변수를 격리하고, `return`과 `echo`+명령 치환의 차이를 구분해 값을 주고받을 수 있다 |
| 심화 | 주의사항·함정, 흔한 오개념 | `local`을 빠뜨렸을 때의 부작용을 진단하고, 함수 정의 순서·종료 코드 범위 제약을 스크립트 설계에 반영할 수 있다 |

## 개요 + 정신 모델

Bash 함수를 이해하는 가장 정확한 방법은 "미니 스크립트"로 보는 것이다. 함수는 새로운 프로세스를 만들지 않고 현재 셸 안에서 실행되는, 이름이 붙은 명령 그룹이다. 호출될 때 함수는 자신만의 위치 매개변수 집합(`$1`, `$2`, … , `$@`, `$#`)을 받는데, 이는 스크립트 자체가 커맨드라인 인자를 받는 방식과 완전히 같은 메커니즘이다. 그리고 함수가 끝날 때는 스크립트나 외부 명령과 마찬가지로 **종료 코드**(0–255 사이의 정수)를 반환한다.

여기서 다른 프로그래밍 언어의 함수 개념과 정신 모델이 갈라진다. Python이나 C의 함수는 `return`으로 임의의 값(문자열, 리스트, 구조체)을 호출부에 돌려줄 수 있지만, Bash의 `return`은 그 명령이 성공했는지 실패했는지, 실패했다면 어떤 종류로 실패했는지를 나타내는 **상태 코드**만 돌려준다. 실제 데이터를 "반환"하고 싶다면 함수 안에서 `echo`로 표준 출력에 값을 쓰고, 호출하는 쪽에서 `$(함수이름 인자...)` 명령 치환으로 그 출력을 캡처하는 관용구를 쓴다. 즉 Bash 함수는 "값을 리턴하는 서브루틴"이 아니라 "종료 코드를 보고하고, 필요하면 표준 출력으로 결과물을 흘려보내는 미니 명령"이라는 정신 모델로 접근해야 옵션 하나하나를 외우지 않고도 동작을 예측할 수 있다.

## 핵심 개념

### 정의와 호출

Bash는 함수를 정의하는 두 가지 동등한 문법을 제공한다.

```bash
# 방식 1: function 키워드 사용(Bash 확장, POSIX sh에는 없음)
function greet() {
  echo "Hello, $1"
}

# 방식 2: POSIX 호환 문법(함수명 뒤 괄호만)
greet() {
  echo "Hello, $1"
}
```

두 방식은 동작이 같지만, `function` 키워드가 붙은 문법은 Bash 전용 확장이라 `dash`처럼 POSIX sh만 지원하는 셸에서는 문법 오류가 난다. 스크립트를 다른 셸에서도 돌릴 가능성이 있다면 방식 2(괄호만 쓰는 형태)가 더 이식성이 높다. 함수는 정의만으로는 아무 일도 하지 않으며, 이름을 명령처럼 그대로 호출해야 실행된다: `greet "world"`.

### 인자($1, $@, $*, $#, shift)

함수 안에서 인자에 접근하는 특수 변수는 스크립트 최상위에서 커맨드라인 인자에 접근할 때와 이름이 동일하지만, **함수를 호출하는 순간 그 함수만의 새 위치 매개변수 집합으로 교체**된다.

```bash
show_args() {
  echo "첫 번째 인자: $1"
  echo "인자 개수: $#"
  echo "전체(각각 인용): $@"
  echo "전체(하나의 문자열): $*"
}

show_args "a b" c d
```

`$@`는 각 인자를 원래 경계 그대로 유지하고, `$*`는 `IFS`의 첫 글자(기본은 공백)로 이어붙인 문자열 하나로 만든다는 차이가 있다 — 이 차이는 인자를 다시 다른 명령에 그대로 전달할 때(`"$@"`) 특히 중요하다. `shift`는 `$1`을 버리고 나머지를 한 칸씩 당겨 `$2`가 새 `$1`이 되게 하며, 인자 개수가 가변적인 함수에서 `while [ "$#" -gt 0 ]; do ... shift; done` 형태의 순회에 쓴다.

### 지역 변수(local)

함수 안에서 `local var=value`로 선언한 변수는 그 함수와, 그 함수가 호출하는 하위 함수에서만 보인다. `local` 없이 변수를 대입하면 Bash는 이를 함수 밖에서도 보이는 **전역 변수**로 취급한다.

```bash
counter=0

increment() {
  local step=1        # step은 increment 함수 안에서만 존재
  counter=$((counter + step))   # counter는 local이 없으므로 전역 변수를 그대로 수정
}

increment
echo "$counter"   # 1
echo "$step"      # 비어 있음 — step은 함수 밖에서 보이지 않는다
```

### return과 값 "반환"의 차이

`return N`은 함수의 종료 코드를 `N`(0–255 정수)으로 설정할 뿐, 문자열이나 숫자 계산 결과 같은 실제 데이터를 돌려주지 않는다. 값을 돌려주려면 함수가 `echo`로 표준 출력에 쓰고, 호출부가 `$(...)` 명령 치환으로 그 출력을 캡처하는 방식을 쓴다.

```bash
add() {
  local sum=$(( $1 + $2 ))
  echo "$sum"        # 계산 결과를 표준 출력으로 "반환"
  return 0            # 함수 자체의 성공 여부는 별도로 종료 코드로 반환
}

result=$(add 3 4)     # 표준 출력을 캡처 → result="7"
echo "합계: $result, 종료 코드: $?"
```

값 하나가 아니라 여러 값을 넘겨야 하거나 명령 치환의 서브셸 비용을 피하고 싶을 때는, 함수가 결과를 직접 미리 정해둔 전역 변수에 대입하는 관용구도 널리 쓰인다(`local` 없이 대입해 전역 스코프에 결과를 남기는 의도적 사용).

```bash
divmod() {
  # 여러 값을 반환해야 하므로 전역 변수 두 개에 결과를 채운다
  DIVMOD_Q=$(( $1 / $2 ))
  DIVMOD_R=$(( $1 % $2 ))
}

divmod 17 5
echo "몫: $DIVMOD_Q, 나머지: $DIVMOD_R"
```

## 예시

### 함수를 스크립트 상단에 모아두는 관례

```bash
#!/bin/bash
# 함수는 호출되기 전에 정의돼 있어야 하므로, 관례상 스크립트 상단에 모아둔다

log() {
  echo "[$(date +%H:%M:%S)] $1"
}

check_disk() {
  local usage
  usage=$(df --output=pcent / | tail -1 | tr -dc '0-9')
  [ "$usage" -lt 90 ]
}

# --- 실제 로직은 함수 정의 아래에서 시작 ---
log "디스크 사용량 확인 시작"
if check_disk; then
  log "정상"
else
  log "경고: 디스크 사용량 90% 초과"
fi
```

### 인자 검증과 조기 반환

```bash
require_arg() {
  if [ -z "$1" ]; then
    echo "오류: 인자가 필요합니다" >&2
    return 1
  fi
  echo "받은 값: $1"
  return 0
}

require_arg "" || echo "require_arg 실패, 종료 코드 $?"
require_arg "ok"
```

### shift로 가변 인자 순회

```bash
print_all() {
  while [ "$#" -gt 0 ]; do
    echo "남은 인자 개수 $#: $1"
    shift
  done
}

print_all one two three
```

### 재귀 함수

```bash
factorial() {
  local n=$1
  if [ "$n" -le 1 ]; then
    echo 1
    return 0
  fi
  local sub
  sub=$(factorial $((n - 1)))
  echo $((n * sub))
}

factorial 5   # 120
```

### 배열을 함수에 전달하고 받기

```bash
sum_array() {
  local -n arr_ref=$1   # nameref로 배열을 참조 전달(값 복사 없이 원본 배열을 가리킴)
  local total=0
  for v in "${arr_ref[@]}"; do
    total=$((total + v))
  done
  echo "$total"
}

numbers=(10 20 30)
sum_array numbers   # 배열 이름을 인자로 넘긴다(값이 아니라 이름)
```

### 함수 존재 여부 확인 후 호출

```bash
if declare -f log > /dev/null; then
  log "log 함수가 정의돼 있다"
else
  echo "log 함수 없음, 기본 echo 사용" 
fi
```

## 주의사항·함정

**`local`을 빠뜨리면 전역 스코프를 오염시킨다**: Bash 함수는 별도의 변수 스코프를 자동으로 만들어주지 않는다. `local` 키워드를 붙이지 않은 모든 대입은 함수 밖에서도 그대로 보이는 전역 변수를 만들거나 덮어쓴다. GNU Bash Reference Manual은 `local`의 역할을 다음과 같이 명시한다.

> "local can only be used within a function; it makes the variable name have a visible scope restricted to that function and its children." — GNU Bash Reference Manual, "Bash Builtin Commands"

이 규칙을 모르고 함수 안에서 흔한 이름(`i`, `result`, `tmp` 등)을 `local` 없이 재사용하면, 호출부에서 이미 쓰고 있던 동일한 이름의 전역 변수를 조용히 덮어써 버그가 발생한다. 특히 반복문 안에서 함수를 여러 번 호출하는 스크립트에서는 이 오염이 반복마다 누적돼 원인을 찾기 어려운 상태 불일치로 이어진다.

**`return`은 0–255 범위의 정수만 담을 수 있다**: `return`이 받는 값은 운영체제가 프로세스 종료 코드로 쓰는 것과 동일한 8비트 정수 표현을 공유하므로, 그 범위를 벗어나거나 정수가 아닌 값을 주면 잘려나가거나 오류가 난다.

> "If n is supplied, the return value is its least significant 8 bits." — GNU Bash Reference Manual, "Bourne Shell Builtins"

즉 `return 300`은 실제로는 `300 mod 256 = 44`가 되고, `return "실패"`처럼 문자열을 주면 정수가 아니라는 오류가 난다. 이 제약은 [33장](/post/bashshell/exit-status-set-trap-bash-error-handling/)에서 다루는 종료 코드 규약과 정확히 같은 규칙이다 — 함수의 `return`과 외부 명령의 종료 코드는 셸 입장에서 구분되지 않는 동일한 메커니즘이며, `$?`로 확인하는 값도 함수 호출과 명령 실행 모두에서 같은 방식으로 갱신된다. 그래서 계산 결과나 문자열처럼 0–255를 벗어나는 데이터는 반드시 앞서 다룬 `echo`+명령 치환이나 전역 변수 관용구로 전달해야 한다.

**함수는 호출되기 전에 정의돼 있어야 한다**: Bash는 스크립트를 위에서 아래로 순차 실행하며, 다른 언어처럼 함수 선언을 먼저 전부 스캔한 뒤 실행을 시작하지 않는다. 따라서 아직 정의되지 않은 함수를 먼저 호출하는 코드는 "명령을 찾을 수 없다"는 오류로 실패한다.

```bash
greet "world"   # 오류: greet: command not found

greet() {
  echo "Hello, $1"
}
```

이 때문에 실무 스크립트에서는 실행 로직보다 먼저, 스크립트 상단에 모든 함수 정의를 모아두는 관례를 따른다(위 "함수를 스크립트 상단에 모아두는 관례" 예시 참고). 여러 스크립트에서 같은 함수를 재사용하려면 함수들만 모은 파일을 만들고 `source ./lib.sh`(또는 `. ./lib.sh`)로 현재 셸에 불러들이는 방법도 널리 쓰인다.

## 흔한 오개념

<strong>"`return`으로 문자열이나 계산 결과를 직접 돌려줄 수 있다"</strong>는 가장 흔한 오해다. `return`이 다루는 값은 항상 0–255 사이의 정수 종료 코드이며, `return "hello"`나 `return 3.14`는 동작하지 않는다. 문자열·부동소수점·여러 값을 전달하려면 앞서 설명한 `echo`+명령 치환 또는 전역 변수 관용구를 써야 한다 — "함수가 값을 반환한다"는 감각 자체는 옳지만, 그 값이 지나가는 통로가 `return`이 아니라 표준 출력이라는 점이 다른 언어와 근본적으로 다르다.

<strong>"함수 안에서 선언한 변수는 자동으로 그 함수만의 지역 변수다"</strong>도 자주 틀리는 지점이다. Bash는 기본적으로 모든 변수를 전역으로 취급하며, `local` 키워드를 명시적으로 붙였을 때만 스코프가 함수로 제한된다. 다른 언어(Python, JavaScript 등)의 함수 로컬 변수 관례에 익숙한 사람일수록 이 차이를 놓치기 쉽다.

## 다음 장에서는

다음은 [33장: 종료 코드와 set -e/-x, trap](/post/bashshell/exit-status-set-trap-bash-error-handling/)이다. 이 장에서 다룬 `return`과 종료 코드 규약을, 함수 하나의 성공·실패 판단을 넘어 스크립트 전체의 실행 흐름을 통제하는 도구로 확장한다. `trap`에 등록하는 핸들러는 형태상 명령 문자열이지만, 실행 시점이 되면 셸이 특정 이벤트(신호 수신, 스크립트 종료 등)를 만났을 때 호출하는 콜백이라는 점에서 사실상 함수와 같은 역할을 한다 — 이 장에서 함수 정의·호출·종료 코드 개념을 먼저 익혀 두면, 왜 그 핸들러 문자열이 등록 시점이 아니라 나중에 실행되는지를 자연스럽게 이해할 수 있다.

## 평가 기준

- 함수를 정의·호출하고 `$1`, `$2`, `$@`, `$*`, `$#`로 인자를 받아 처리할 수 있다.
- `local`을 쓴 경우와 쓰지 않은 경우의 변수 스코프 차이를 설명하고, `local` 누락이 전역 변수를 오염시키는 사례를 코드에서 알아볼 수 있다.
- `return`이 0–255 범위의 종료 코드만 반환한다는 점과, 실제 값을 "반환"하려면 `echo`+명령 치환 또는 전역 변수 관용구를 써야 한다는 점을 구분해 설명할 수 있다.
- 함수가 호출되기 전에 정의돼 있어야 한다는 제약을 알고, 스크립트 상단에 함수를 모아두는 관례를 적용할 수 있다.
- `return`의 종료 코드 규약이 [33장](/post/bashshell/exit-status-set-trap-bash-error-handling/)에서 다루는 스크립트 전체의 종료 코드 처리와 동일한 메커니즘임을 설명할 수 있다.

## 참고

- [Shell Functions — GNU Bash Reference Manual](https://doc.guix.gnu.org/bash/latest/en/html_node/Shell-Functions.html)
- [Bash Builtin Commands(local) — GNU Bash Reference Manual](https://doc.guix.gnu.org/bash/latest/en/html_node/Bash-Builtins.html)
- [Bourne Shell Builtins(return) — GNU Bash Reference Manual](https://doc.guix.gnu.org/bash/latest/en/html_node/Bourne-Shell-Builtins.html)
- [Special Parameters($@, $*, $#) — GNU Bash Reference Manual](https://doc.guix.gnu.org/bash/latest/en/html_node/Special-Parameters.html)
