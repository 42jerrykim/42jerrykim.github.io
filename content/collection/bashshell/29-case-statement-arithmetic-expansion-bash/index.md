---
draft: false
slug: case-statement-arithmetic-expansion-bash
title: "[Bash Shell] 29. case와 산술 연산 - 조건 분기 확장"
description: "case가 값 하나를 여러 글롭 패턴에 순서대로 매칭하는 다중 분기라는 점과, 산술 확장 $(( ))이 정수 전용 별도 컨텍스트라는 점을 GNU Bash Reference Manual 원문과 실행 예제로 정리합니다."
date: 2026-08-23
lastmod: 2026-08-23
collection_order: 290
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
- Numerical-Computing(수치계산)
- Floating-Point(부동소수점)
- Modular-Arithmetic(모듈러)
- Case-Statement
- Glob-Pattern
- Pattern-Matching
- Shell-Arithmetic
- Arithmetic-Expansion
- Integer-Arithmetic
- Conditional-Branching
- Multi-Way-Branch
- Extglob
- Fallthrough
- Shell-Scripting
- Shell-Builtin
- C-Style-For-Loop
image: "wordcloud.png"
---

`if`/`elif`로 조건 분기를, `for`/`while`로 반복을 다룰 수 있게 됐다면 이번 장은 그 조건 분기를 확장하는 두 가지 도구를 다룬다. 값 하나를 여러 후보와 비교하는 `if-elif` 체인이 길어질 때 더 읽기 쉬운 형태로 바꿔주는 `case` 문과, 문자열이 아니라 숫자로 계산해야 하는 상황에서 쓰는 산술 확장 `$(( ))`이다. 두 도구 모두 셸 스크립트가 표현할 수 있는 조건·계산의 폭을 넓혀준다.

## 이 장을 읽기 전에

직전 챕터인 [28장: for, while](/post/bashshell/for-while-loop-bash-shell-scripting/)에서 반복 제어를 다뤘고, 그 앞의 [27장: if, test](/post/bashshell/if-test-command-bash-conditional-statements/)에서 조건 분기의 기본 형태인 `if-elif-else`와 `[ ]`/`test` 조건식을 다뤘다. 이 장은 그 두 기초 위에서 두 가지를 확장한다 — 값 하나를 여러 경우와 비교하는 조건 분기를 `if-elif` 체인보다 읽기 쉬운 형태(`case`)로 표현하는 법과, 조건식·변수 대입에서 문자열이 아니라 정수로 계산해야 하는 상황을 다루는 법(산술 확장)이다. `case`의 패턴 매칭은 [22장: quoting](/post/bashshell/bash-quoting-escaping-special-characters/)에서 다룬 인용 규칙과도 맞닿아 있다 — 패턴에 들어갈 와일드카드를 실수로 인용해버리면 매칭 자체가 깨진다.

난이도는 초급–중급이다. `if`/`test`([27장](/post/bashshell/if-test-command-bash-conditional-statements/))로 조건을 작성할 수 있고 반복문([28장](/post/bashshell/for-while-loop-bash-shell-scripting/))을 읽을 수 있다고 가정한다.

**다루지 않는 것**: 텍스트 안에서 패턴을 찾는 정규식 자체는 [13장: grep](/post/bashshell/grep-command-search-text-pattern-linux/), [14장: sed](/post/bashshell/sed-command-stream-editor-linux/)에서 다룬다 — `case`의 패턴은 정규식이 아니라 셸 글롭 패턴이라는 점이 이 장의 핵심 주의사항 중 하나다. 부동소수점이 필요한 계산은 이 장에서 한계로만 언급하고(`bc`, `awk` 대안 제시) 별도로 깊이 다루지 않는다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| 입문 | 개요 + 정신 모델, 핵심 개념의 `case` 기본 문법·`$(( ))` 기본 사용 | 값 하나를 여러 패턴과 비교하는 `case` 문을 작성하고, 정수 계산에 `$(( ))`을 쓸 수 있다 |
| 중급 | 핵심 개념 전체, 예시 | `;;`/`;&`/`;;&` 종결자를 구분하고, `(( ))`를 조건문에, `$(( ))`을 값 계산에 구분해 쓸 수 있다 |
| 심화 | 주의사항·함정, 흔한 오개념 | `case` 패턴이 정규식이 아니라 글롭이라는 한계를 정확히 알고, 정수 오버플로우·나눗셈 절삭 같은 산술 함정을 피할 수 있다 |

## 개요 + 정신 모델

`case`는 값 하나를 여러 **글롭 패턴**과 순서대로 비교해 가장 먼저 매칭되는 분기의 명령을 실행하는 다중 분기 구문이다. `if-elif-else`로 같은 일을 하려면 매번 `[[ "$var" == pattern ]]`처럼 비교 대상 변수를 반복해서 써야 하지만, `case`는 비교 대상을 한 번만 쓰고 그 아래에 패턴 목록만 나열하면 되므로 분기가 세 개 이상이면 가독성이 뚜렷하게 좋아진다. 셸이 이 값을 "여러 후보 중 어디에 속하는가"라는 분류 문제로 다룬다는 점이 정신 모델의 핵심이다.

산술 확장 `$(( 산술식 ))`은 이와 완전히 다른 문제를 푼다. 셸은 기본적으로 모든 것을 **문자열**로 다룬다 — `x=3`이라고 쓰면 `x`에는 숫자 3이 아니라 문자 `"3"`이 저장된다. `$(( ))`는 그 문자열들을 잠시 정수 산술 컨텍스트로 옮겨 실제 숫자 연산(덧셈, 비교, 나머지 등)을 수행한 뒤 결과를 다시 문자열로 돌려주는 별도의 평가 공간이다. 이 컨텍스트 안에서는 셸의 일반 규칙(단어 분리, 글롭 확장 등)이 적용되지 않고 C 언어에 가까운 산술 규칙이 적용된다.

## 핵심 개념

### case 문법 구조

GNU Bash Reference Manual은 `case`의 문법을 다음과 같이 정의한다.

> "case word in \[ \[(\] pattern \[| pattern\]...) command-list ;;\]... esac" — GNU Bash Reference Manual, "Conditional Constructs"

풀어 쓰면 `case` 뒤의 `word`(비교 대상 값)를 `in` 다음에 나열된 패턴들과 순서대로 비교하고, 매칭되는 첫 패턴의 `command-list`를 실행한 뒤 `esac`(`case`를 거꾸로 쓴 것)로 끝난다는 뜻이다. 각 패턴은 `)`로 끝나고, 여는 괄호 `(`는 있어도 되고 없어도 되며, `|`로 여러 패턴을 하나의 절에 묶을 수 있다.

```bash
read -rp "환경을 선택하세요 (dev/stage/prod): " env

case "$env" in
    dev)
        echo "개발 환경으로 배포합니다."
        ;;
    stage | staging)
        echo "스테이징 환경으로 배포합니다."
        ;;
    prod | production)
        echo "운영 환경입니다. 배포 전 승인이 필요합니다."
        ;;
    *)
        echo "알 수 없는 환경: $env" >&2
        exit 1
        ;;
esac
```

`stage | staging`처럼 `|`로 여러 패턴을 한 절에 묶을 수 있고, 마지막의 `*)`는 어떤 패턴에도 매칭되지 않은 값을 처리하는 기본값 역할을 한다.

### 패턴 매칭 규칙

`case`의 패턴은 정규식이 아니라 **셸 글롭(파일명 확장) 패턴**이다. GNU Bash Reference Manual은 패턴 매칭에 쓰이는 기본 문자를 다음과 같이 설명한다.

> "`*`: Matches any string, including the null string." / "`?`: Matches any single character." / "`[…]`: Matches any one of the enclosed characters." — GNU Bash Reference Manual, "Pattern Matching"

즉 `*`는 빈 문자열을 포함한 임의의 문자열에, `?`는 문자 하나에, `[...]`는 대괄호 안에 나열된 문자 중 하나에 매칭된다. `[...]` 안에서 하이픈으로 문자 쌍을 이으면 범위(`[0-9]`)를, 앞에 `!`나 `^`를 붙이면 부정(포함되지 않은 문자)을 뜻한다.

`case`의 `word`는 패턴과 비교되기 전에 확장을 거친다는 점도 중요하다.

> "The word undergoes tilde expansion, parameter expansion, command substitution, arithmetic expansion, and quote removal before matching is attempted." — GNU Bash Reference Manual, "Conditional Constructs"

즉 `case $(( a + b )) in ...`처럼 산술 확장 결과를 바로 `case`의 비교 대상으로 쓸 수 있다 — 뒤의 예시에서 이 조합을 다룬다.

### 종결자: ;; vs ;& vs ;;&

각 절은 보통 `;;`로 끝나 매칭이 확정되면 더 이상 다른 패턴을 검사하지 않지만, bash는 이 동작을 바꾸는 두 가지 대안을 제공한다.

> "If the ';;' operator is used, no subsequent matches are attempted after the first pattern match." / "Using ';&' in place of ';;' causes execution to continue with the command-list associated with the next clause, if any." / "Using ';;&' in place of ';;' causes the shell to test the patterns in the next clause, if any, and execute any associated command-list on a successful match, continuing the case statement execution." — GNU Bash Reference Manual, "Conditional Constructs"

정리하면 `;;`는 매칭 즉시 종료, `;&`는 다음 절의 패턴을 검사하지 않고 그 명령 목록을 무조건 이어서 실행(폴스루), `;;&`는 다음 절의 패턴을 다시 검사해서 매칭되면 실행하는 방식이다. 셋 다 같은 `case` 블록 안에서 절마다 다르게 섞어 쓸 수 있다.

### 산술 확장 $(( ))

`$(( 산술식 ))`은 그 안의 표현식을 정수 산술로 평가하고 결과값을 문자열로 반환한다. 이 컨텍스트 안에서는 변수를 `$` 접두사 없이 이름만으로 참조할 수 있다.

> "Within an expression, shell variables may also be referenced by name without using the parameter expansion syntax." — GNU Bash Reference Manual, "Shell Arithmetic"

```bash
count=5
echo "다음 값: $(( count + 1 ))"    # $count가 아니라 count로 바로 참조 가능
echo "다음 값: $(( $count + 1 ))"   # $count로 써도 동작은 같다
```

산술식만 평가하고 조건 판단이 필요 없다면 `$(( ))`(확장, 값을 반환)를, 조건문의 참/거짓만 필요하다면 `(( ))`(명령, 종료 상태를 반환)를 쓴다. `(( expr ))`은 `expr`이 0이 아니면 종료 코드 0(성공), 0이면 종료 코드 1(실패)을 반환한다 — 산술 참/거짓과 셸 종료 코드의 참/거짓이 반대라는 점에 유의한다.

```bash
x=10
if (( x > 5 )); then
    echo "x는 5보다 크다"
fi
```

### 산술 연산자

GNU Bash Reference Manual은 `$(( ))` 안에서 쓸 수 있는 연산자를 우선순위가 높은 것부터 다음과 같이 나열한다.

| 그룹 | 연산자 |
|---|---|
| 증감 | `++`, `--` |
| 단항 | `-`, `+`, `!`, `~` |
| 지수 | `**` |
| 곱셈/나눗셈/나머지 | `*`, `/`, `%` |
| 덧셈/뺄셈 | `+`, `-` |
| 비트 시프트 | `<<`, `>>` |
| 비교 | `<=`, `>=`, `<`, `>` |
| 등가 | `==`, `!=` |
| 비트 AND/XOR/OR | `&`, `^`, `|` |
| 논리 AND/OR | `&&`, `||` |
| 삼항 조건 | `? :` |
| 대입 | `=`, `+=`, `-=`, `*=`, `/=`, `%=` 등 |

C 언어의 연산자·우선순위와 거의 동일하다는 점을 기억해 두면 대부분의 표현식을 직관적으로 읽을 수 있다.

## 예시

### 1. 여러 패턴을 하나의 절에 묶기

```bash
fruit="apple"
case "$fruit" in
    apple | pear | peach)
        echo "$fruit 은(는) 씨과실류다."
        ;;
    banana | mango)
        echo "$fruit 은(는) 열대 과일이다."
        ;;
    *)
        echo "분류를 모르는 과일: $fruit"
        ;;
esac
```

### 2. 범위·와일드카드 패턴으로 파일 확장자 분기

```bash
for file in report.txt photo.JPG archive.tar.gz script.sh; do
    case "$file" in
        *.txt | *.md)
            echo "$file: 텍스트 문서"
            ;;
        *.[jJ][pP][gG] | *.png)
            echo "$file: 이미지"
            ;;
        *.tar.gz | *.tgz)
            echo "$file: 압축 아카이브"
            ;;
        *)
            echo "$file: 분류 안 됨"
            ;;
    esac
done
```

`*.[jJ][pP][gG]`처럼 대괄호 문자 클래스를 문자마다 반복하면 대소문자를 가리지 않는 매칭을 흉내 낼 수 있다(진짜 대소문자 무시가 필요하면 `shopt -s nocasematch`가 더 간결하다).

### 3. ;;& 로 다음 절까지 이어서 검사하기

```bash
grade=85
case $grade in
    9[0-9] | 100)
        echo "A 학점"
        ;;&
    [6-9][0-9] | 100)
        echo "합격"
        ;;
    *)
        echo "불합격"
        ;;
esac
```

`;;&`는 첫 절이 매칭돼도 다음 절의 패턴을 다시 검사하므로, `grade=85`는 "A 학점"과 "합격"을 모두 출력한다. `;;`만 썼다면 첫 매칭에서 바로 끝나 "합격"은 출력되지 않는다.

### 4. case의 word 자리에 산술 확장 넣기

```bash
n=17
case $(( n % 15 )) in
    0)
        echo "FizzBuzz"
        ;;
    3 | 6 | 9 | 12)
        echo "Fizz"
        ;;
    5 | 10)
        echo "Buzz"
        ;;
    *)
        echo "$n"
        ;;
esac
```

앞서 "패턴 매칭 규칙"에서 확인했듯 `case`의 `word`는 매칭 전에 산술 확장을 거치므로, `$(( n % 15 ))`의 계산 결과(정수)가 곧바로 비교 대상이 된다.

### 5. $(( ))으로 값 계산, (( ))으로 조건 판단 구분

```bash
total=0
for price in 12000 8500 30000; do
    total=$(( total + price ))
done
echo "합계: $total"

if (( total >= 30000 )); then
    echo "무료 배송 대상"
else
    echo "배송비 추가: $(( 30000 - total ))원"
fi
```

### 6. C 스타일 for와 산술 대입 연산자

```bash
for (( i = 1; i <= 5; i++ )); do
    echo "제곱: $(( i ** 2 ))"
done
```

C 스타일 `for (( 초기화; 조건; 증감 ))`은 세 부분 모두 산술 컨텍스트라 `$` 없이 변수를 바로 쓴다 — 28장에서 다룬 `for` 구문의 변형이다.

### 7. 정수 나눗셈 절삭 확인

```bash
echo $(( 7 / 2 ))     # 3 (소수점 이하 절삭)
echo $(( -7 / 2 ))    # -3 (0을 향해 절삭)
echo $(( 7 % 2 ))     # 1
```

## 주의사항·함정

**`case`의 패턴은 정규식이 아니라 글롭 패턴이다**: `grep`·`sed`의 정규식에 익숙하면 `case`에서도 `+`(1회 이상 반복), 괄호 그룹핑, `(a|b)` 같은 표현이 될 것이라 기대하기 쉽지만, 기본 글롭에는 이런 문법이 없다. `case`가 지원하는 것은 `*`(임의 문자열), `?`(문자 하나), `[...]`(문자 클래스), 그리고 `|`로 여러 패턴을 나열하는 것뿐이다. `+`·`@`·`!`로 시작하는 확장 패턴(`+(pattern-list)`, `@(pattern-list)`, `!(pattern-list)` 등)은 `shopt -s extglob`로 `extglob` 옵션을 켜야만 쓸 수 있는 bash 확장이며, 기본 상태에서는 `+`나 괄호가 리터럴 문자로 취급된다.

> "`?(pattern-list)`: Matches zero or one occurrence of the given patterns." / "`+(pattern-list)`: Matches one or more occurrences of the given patterns." — GNU Bash Reference Manual, "Pattern Matching" (extglob 활성화 시)

```bash
shopt -s extglob
case "file.tar.gz" in
    *.@(tar.gz|tgz))
        echo "tar.gz 계열 압축 파일"
        ;;
esac
shopt -u extglob   # 다른 곳에서 파서 동작이 바뀌는 걸 막기 위해 다시 끈다
```

**산술 컨텍스트에서는 변수를 $ 없이 쓸 수 있다**: 위 "핵심 개념"에서 확인했듯 `$(( ))`/`(( ))` 안에서는 `count`처럼 이름만 써도 변수로 인식된다. 반대로 이 컨텍스트 밖(일반 명령 인자, 문자열 등)에서는 `$` 없이 쓴 이름이 그냥 리터럴 문자열로 취급되므로, 컨텍스트 안팎을 넘나들며 코드를 수정할 때 `$` 유무를 놓치기 쉽다.

**bash 산술은 정수 전용이라 부동소수점 연산이 안 된다**: GNU Bash Reference Manual은 이를 명시한다.

> "Evaluation is done in fixed-width integers with no check for overflow, though division by 0 is trapped and flagged as an error." — GNU Bash Reference Manual, "Shell Arithmetic"

`$(( 3 / 2 ))`는 `1.5`가 아니라 `1`이다(소수점 이하 절삭). 소수 계산이 필요하면 `bc`나 `awk`처럼 부동소수점을 지원하는 외부 도구에 위임해야 한다.

```bash
echo $(( 3 / 2 ))                 # 1 (정수 절삭)
echo "3 / 2" | bc -l              # 1.50000000000000000000
awk 'BEGIN { print 3 / 2 }'       # 1.5
```

**정수 오버플로우는 에러 없이 값이 순환한다**: 인용문의 "no check for overflow"가 뜻하는 바는, 고정폭 정수 범위를 벗어난 계산도 에러를 내지 않고 그 범위 안에서 값이 순환(wrap-around)한다는 것이다. 나눗셈만 0으로 나누는 경우를 예외로 잡아 에러 처리한다. 64비트 환경에서 부호 있는 정수의 최댓값에 1을 더하면 이를 직접 확인할 수 있다.

```bash
echo $(( 9223372036854775807 + 1 ))   # 에러 없이 -9223372036854775808으로 순환한다(64비트 환경 기준)
echo $(( 5 / 0 ))                     # 이건 에러: division by 0
```

## 흔한 오개념

<strong>"case의 패턴도 정규식처럼 그룹과 반복을 쓸 수 있다"</strong>는 가장 흔한 오해다. 기본 글롭에는 `+`·`()`그룹핑·`{n,m}` 반복 같은 정규식 문법이 없고, 비슷한 기능을 쓰려면 `extglob` 옵션을 별도로 켜야 한다. `case`에 정규식을 쓰고 싶다면 애초에 다른 도구다 — `[[ "$var" =~ regex ]]`(bash 확장 조건식)나 `grep -E`로 옮겨야 한다.

<strong>"$(( ))와 (( ))는 그냥 같은 것이다"</strong>도 자주 틀리는 지점이다. `$(( ))`는 <strong>확장(expansion)</strong>이라 산술식의 계산 결과(값)를 문자열로 돌려주므로 `x=$(( a + b ))`처럼 대입이나 출력에 쓴다. `(( ))`는 <strong>명령(command)</strong>이라 계산 결과 자체가 아니라 그 결과가 0인지 아닌지에 따른 **종료 코드**를 돌려주므로 `if (( x > 5 )); then ...`처럼 조건문에 쓴다. 둘을 바꿔 쓰면(`if $(( x > 5 )); then`처럼) 셸이 계산 결과 문자열을 명령으로 실행하려다 오류를 내는 경우가 많다.

## 다음 장에서는

[30장: read, 표준입력](/post/bashshell/read-command-standard-input-bash-scripting/)에서는 사용자나 파이프로부터 값을 받아 변수에 채우는 `read`를 다룬다. 이 장의 예시 다수가 `read -rp`로 입력을 받아 `case`로 분기하는 조합을 썼는데, 다음 장은 그 `read`가 표준입력을 정확히 어떻게 처리하는지(구분자, `-r` 원시 모드, 여러 변수 동시 할당 등)를 깊이 다룬다.

## 평가 기준

- `case word in pattern) command-list ;; ... esac` 문법으로 다중 분기를 작성할 수 있다.
- `case`의 패턴이 정규식이 아니라 셸 글롭 패턴(`*`, `?`, `[...]`, `|`)이라는 점과, 정규식과 유사한 표현이 필요하면 `extglob`이나 `[[ =~ ]]`로 옮겨야 한다는 점을 설명할 수 있다.
- `;;`, `;&`, `;;&` 세 종결자의 동작 차이를 설명하고 상황에 맞게 선택할 수 있다.
- `$(( ))`(값을 반환하는 확장)와 `(( ))`(종료 코드를 반환하는 명령)를 구분해 조건문과 값 계산에 각각 올바르게 쓸 수 있다.
- bash 산술이 정수 전용이라 나눗셈이 절삭되고 부동소수점을 지원하지 않는다는 점을 알고, 필요할 때 `bc`/`awk`로 대체할 수 있다.

## 참고

- [Conditional Constructs — GNU Bash Reference Manual](https://doc.guix.gnu.org/bash/latest/en/html_node/Conditional-Constructs.html)
- [Shell Arithmetic — GNU Bash Reference Manual](https://doc.guix.gnu.org/bash/latest/en/html_node/Shell-Arithmetic.html)
- [Pattern Matching — GNU Bash Reference Manual](https://doc.guix.gnu.org/bash/latest/en/html_node/Pattern-Matching.html)
