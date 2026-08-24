---
draft: false
slug: bash-arrays-brace-parameter-expansion
title: "[Bash Shell] 31. 배열과 셸 확장 - Brace/Parameter Expansion"
description: "bash 배열이 인덱스 배열·연관 배열 두 종류로 나뉜다는 점, 중괄호 확장이 반복문이 아니라 실행 전 텍스트로 미리 펼쳐진다는 점, \"${arr[@]}\"와 \"${arr[*]}\"의 인용 여부에 따른 차이를 GNU Bash Reference Manual 원문으로 정리합니다."
date: 2026-08-24
lastmod: 2026-08-24
collection_order: 310
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
- Guide(가이드)
- Tutorial(튜토리얼)
- Reference(참고)
- Beginner
- Array(배열)
- Data-Structures(자료구조)
- File-System
- Process(프로세스)
- Indexed-Array
- Associative-Array
- Brace-Expansion
- Parameter-Expansion
- IFS
- Word-Splitting
- Globbing
- Filename-Expansion
- Quoting
- Shell-Scripting
- Shell-Builtin
- Declare-Builtin
- Compound-Assignment
- Portability
- Subscript
image: "wordcloud.png"
---

값 하나를 담는 변수로는 부족한 상황 — 파일 목록, 사용자 이름 목록, 설정 키-값 쌍 — 을 위해 bash는 배열이라는 자료구조를 제공한다. 그리고 배열을 명령 인자로 펼쳐 넘기려면, 셸이 명령을 실행하기 전에 명령줄을 어떤 순서로 다시 쓰는지(셸 확장)를 알아야 한다. 이 장은 인덱스 배열·연관 배열의 생성과 참조, 그리고 중괄호 확장부터 파일명 확장(글로빙)까지 이어지는 셸 확장의 순서를 GNU Bash Reference Manual 원문과 함께 다룬다.

## 이 장을 읽기 전에

직전 챕터인 [30장: read, 표준입력](/post/bashshell/read-command-standard-input-bash-scripting/)에서 값 하나를 변수 하나에 채우는 법을 다뤘다. 이 장은 그 확장이다 — 값 여러 개를 이름 하나 아래 묶어 두는 자료구조(배열)를 만들고, 그 요소들을 명령 인자로 펼쳐 넘기는 법을 다룬다. 배열을 펼칠 때 결과가 왜 상황에 따라 달라지는지 이해하려면 셸이 명령줄을 실행 전에 어떤 순서로 다시 쓰는지(셸 확장)부터 알아야 하므로, 두 주제를 한 장에 묶었다.

난이도는 중급이다. [27–28장](/post/bashshell/if-test-command-bash-conditional-statements/)의 조건·반복문과 [29장: case, 산술 연산](/post/bashshell/case-statement-arithmetic-expansion-bash/)의 `$(( ))` 산술 확장, [30장: read](/post/bashshell/read-command-standard-input-bash-scripting/)의 변수 대입을 이미 안다고 가정한다.

**다루지 않는 것**: 문자열 일부를 잘라내거나 치환하는 나머지 파라미터 확장 연산자(`${var#pattern}`, `${var%pattern}`, `${var/pattern/repl}` 등)와 명령 치환 `$( )`은 이 장의 범위 밖이다 — 여기서는 배열 참조에 곧바로 필요한 `${arr[@]}`/`${arr[*]}`와 인덱스·길이 조회만 다룬다. 정규식·글롭 패턴 자체의 문법은 [13장: grep](/post/bashshell/grep-command-search-text-pattern-linux/), [29장: case](/post/bashshell/case-statement-arithmetic-expansion-bash/)에서 이미 다뤘으므로 여기서는 패턴 문법을 반복하지 않는다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| 입문 | 개요 + 정신 모델, 핵심 개념의 배열 생성·참조 | 인덱스 배열을 만들고 `${arr[i]}`로 요소를 꺼낼 수 있다 |
| 중급 | 핵심 개념 전체, 예시 | 연관 배열을 선언하고, `"${arr[@]}"`로 배열 전체를 안전하게 순회하며, `{1..N}`으로 반복 없이 명령을 생성할 수 있다 |
| 심화 | 주의사항·함정, 흔한 오개념 | `"${arr[@]}"`와 `"${arr[*]}"`의 차이를 정확히 설명하고, bash 배열의 이식성 한계와 중괄호 확장·글로빙의 근본적 차이를 구분할 수 있다 |

## 개요 + 정신 모델

배열은 이름 하나 아래 여러 값을 슬롯별로 저장하고, 정수 인덱스 또는 문자열 키로 개별 슬롯에 접근하는 자료구조다. 일반 변수 `x=3`이 슬롯 하나짜리 상자라면, 배열 `arr=(a b c)`는 번호가 매겨진 여러 칸을 가진 서랍장이다. bash는 이 서랍장을 두 가지 방식으로 제공한다 — 칸 번호가 항상 정수인 **인덱스 배열**과, 칸 이름을 임의의 문자열로 쓰는 **연관 배열**(bash 4.0 이상, `declare -A`로 명시적 선언 필요)이다.

셸 확장은 이와 완전히 다른 층위의 개념이다. 셸은 사용자가 입력한 명령줄을 곧바로 실행하지 않는다. 실행 전에 정해진 순서에 따라 명령줄의 텍스트를 여러 단계로 다시 쓴다 — 중괄호를 풀어 여러 단어로 만들고, 변수와 명령 치환 결과를 끼워 넣고, 그 결과를 공백 기준으로 다시 쪼개고, 마지막으로 와일드카드를 실제 파일명으로 바꾼다. 이 순서를 파이프라인으로 이해하면, 배열을 펼친 결과가 어떤 단계에서 몇 개의 "단어"로 쪼개지는지(그리고 `"${arr[@]}"`처럼 따옴표로 그 쪼개짐을 막을 수 있는지)를 예측할 수 있게 된다.

## 핵심 개념

### 인덱스 배열과 연관 배열

GNU Bash Reference Manual은 두 배열 유형을 다음과 같이 구분한다. 인덱스 배열은 아무 선언 없이도 `name[subscript]=value` 형태로 대입하는 순간 자동으로 만들어지거나, `declare -a name`으로 명시적으로 선언할 수 있다. 연관 배열은 반드시 `declare -A name`으로 먼저 선언해야 하며, 첨자로 정수가 아닌 임의의 문자열(키)을 쓴다.

```bash
# 인덱스 배열 - 선언 없이 대입만으로 생성된다
fruits=(apple banana cherry)

# 연관 배열 - declare -A 없이는 키 문자열을 첨자로 쓸 수 없다
declare -A prices
prices[apple]=1200
prices[banana]=800
```

### 배열 생성 - compound assignment

배열은 괄호로 감싼 값 목록을 대입하는 compound assignment 문법으로 만든다. 인덱스 배열은 첨자를 생략하면 0부터 순서대로 채워지고, `[n]=value`로 특정 인덱스를 지정하면 그 사이 인덱스는 비워둔 채(sparse) 채워진다.

```bash
colors=(red green blue)          # colors[0]=red, colors[1]=green, colors[2]=blue
sparse=([0]=first [5]=sixth)     # 인덱스 1~4는 존재하지 않는다(비어 있는 게 아니라 아예 없다)
declare -A capital=([kr]=Seoul [jp]=Tokyo [us]="Washington DC")
```

### 요소 참조와 전체 참조

개별 요소는 `${name[subscript]}`로 참조한다. 중괄호는 셸이 이를 파일명 확장 문자로 오인하지 않게 막아주는 역할이라 생략할 수 없다. 배열 전체를 참조할 때는 첨자 자리에 `@` 또는 `*`를 쓰고, 길이는 `${#name[@]}`로, 인덱스(또는 키) 목록은 `${!name[@]}`로 얻는다.

```bash
fruits=(apple banana cherry)
echo "${fruits[0]}"        # apple
echo "${fruits[-1]}"       # cherry (음수 인덱스는 끝에서부터)
echo "${#fruits[@]}"       # 3 (요소 개수)
echo "${!fruits[@]}"       # 0 1 2 (인덱스 목록)

declare -A capital=([kr]=Seoul [jp]=Tokyo)
echo "${capital[kr]}"      # Seoul
echo "${!capital[@]}"      # kr jp (키 목록, 정렬 순서는 보장되지 않는다)
```

### 셸 확장의 순서

셸은 명령줄을 실행하기 전, 정해진 순서로 확장을 적용한다. GNU Bash Reference Manual은 이 순서를 다음과 같이 명시한다.

> "The order of expansions is: brace expansion; tilde expansion, parameter and variable expansion, arithmetic expansion, and command substitution (done in a left-to-right fashion); word splitting; and filename expansion." — GNU Bash Reference Manual, "Shell Expansions"

즉 ① 중괄호 확장이 가장 먼저 일어나 텍스트를 여러 단어로 펼치고, ② 그 각 단어에 대해 물결 확장·변수 확장·산술 확장·명령 치환이 왼쪽에서 오른쪽으로 적용되며, ③ 그 결과를 공백(정확히는 `IFS`)으로 다시 쪼개는 단어 분리가 일어나고, ④ 마지막으로 각 단어를 실제 파일명과 대조해 바꾸는 파일명 확장(글로빙)이 적용된다. 배열의 `"${arr[@]}"`/`"${arr[*]}"` 차이는 바로 이 ③ 단어 분리 단계에서 갈린다 — 뒤의 "핵심 개념" 항목과 "주의사항·함정"에서 이어서 다룬다.

### 중괄호 확장 {x..y}

중괄호 확장은 `{1..10}`, `{a..e}`처럼 정수 또는 알파벳 범위를, 혹은 `{red,green,blue}`처럼 쉼표로 나열한 목록을 여러 단어로 펼치는 기능이다. GNU Bash Reference Manual은 이를 다음과 같이 정의한다.

> "Brace expansion is a mechanism by which arbitrary strings may be generated. This mechanism is similar to filename expansion, but the filenames generated need not exist." — GNU Bash Reference Manual, "Brace Expansion"

즉 중괄호 확장은 파일명 확장(글로빙)과 겉보기에 비슷한 결과를 내지만, 생성되는 문자열이 실제 파일명일 필요가 전혀 없다. 이 차이는 매우 근본적이라 "주의사항·함정"에서 별도로 다룬다.

```bash
echo {1..5}          # 1 2 3 4 5
echo {a..e}           # a b c d e
echo {05..08}         # 05 06 07 08 (앞자리 0으로 자릿수를 맞춘다)
echo {1..10..2}       # 1 3 5 7 9 (증분 지정)
echo file{1,2,3}.txt  # file1.txt file2.txt file3.txt
```

## 예시

### 1. for 루프로 인덱스 배열 순회

```bash
fruits=(apple banana cherry)
for f in "${fruits[@]}"; do
    echo "과일: $f"
done
```

### 2. 연관 배열 선언과 키 순회

```bash
declare -A capital=([kr]=Seoul [jp]=Tokyo [us]="Washington DC")
for country in "${!capital[@]}"; do
    echo "$country 의 수도: ${capital[$country]}"
done
```

### 3. 배열 길이와 마지막 인덱스

```bash
nums=(10 20 30 40)
echo "요소 개수: ${#nums[@]}"
echo "마지막 인덱스: $((${#nums[@]} - 1))"
echo "마지막 요소: ${nums[-1]}"
```

### 4. 배열 슬라이스와 요소 삭제

```bash
letters=(a b c d e)
echo "${letters[@]:1:3}"   # b c d (인덱스 1부터 3개)
unset 'letters[2]'          # c 삭제 - 인덱스 2는 사라지고 배열은 sparse가 된다
echo "${letters[@]}"        # a b d e
echo "${!letters[@]}"       # 0 1 3 4 (2가 빠진 인덱스 목록)
```

### 5. "${arr[@]}"로 공백 포함 요소를 안전하게 명령 인자로 넘기기

```bash
paths=("/tmp/log dir/a.log" "/tmp/log dir/b.log")
for p in "${paths[@]}"; do
    ls -l "$p" 2>/dev/null || echo "없음: $p"
done
```

`"${paths[@]}"`는 요소마다 공백이 있어도 각 요소를 정확히 하나의 단어로 유지한다. 따옴표 없이 `${paths[@]}`로 썼다면 `"/tmp/log dir/a.log"`가 `/tmp/log`와 `dir/a.log`라는 별개의 두 단어로 쪼개져 버렸을 것이다.

### 6. 중괄호 확장으로 디렉터리 여러 개를 한 번에 생성

```bash
mkdir -p project/{src,tests,docs}
mkdir -p logs/{2026-01..2026-03}    # 이렇게는 안 된다 - 날짜 문자열은 시퀀스로 확장되지 않는다
mkdir -p backup-{01..05}             # backup-01 backup-02 backup-03 backup-04 backup-05
```

두 번째 줄은 의도적인 오답 예시다 — `{2026-01..2026-03}`은 하이픈이 포함된 문자열이라 정수/알파벳 시퀀스 규칙에 맞지 않아 그대로 리터럴 텍스트로 남는다. 시퀀스 확장은 순수한 정수 범위(`{1..12}`) 또는 알파벳 범위(`{a..z}`)에만 적용된다.

### 7. 중괄호 확장은 파일이 없어도 그대로 펼쳐진다

```bash
cd /tmp && mkdir -p empty_dir && cd empty_dir
echo report-{2024,2025,2026}.txt   # report-2024.txt report-2025.txt report-2026.txt (파일이 하나도 없어도 텍스트로 출력된다)
echo *.txt                          # *.txt (매칭되는 파일이 없으면 리터럴 패턴 그대로 남는다, nullglob 미설정 기준)
```

같은 디렉터리에서 실행해도 두 줄의 결과가 근본적으로 다르다 — 이 차이는 "주의사항·함정"에서 원문과 함께 정리한다.

### 8. 배열 요소를 명령 인자로 한꺼번에 전달

```bash
grep_targets=(access.log error.log debug.log)
grep -l "OutOfMemory" "${grep_targets[@]}" 2>/dev/null
```

### 9. C 스타일 for와 배열을 함께 써서 인덱스로 순회

```bash
scores=(88 92 79 95)
for (( i = 0; i < ${#scores[@]}; i++ )); do
    echo "학생 $((i + 1)): ${scores[i]}점"
done
```

## 주의사항·함정

**`"${arr[@]}"`(각 요소를 별도 단어로) vs `"${arr[*]}"`(하나의 문자열로 합침)**: 이 둘의 차이는 bash 배열에서 가장 헷갈리기 쉬운 지점이다. GNU Bash Reference Manual은 큰따옴표로 감쌌을 때의 동작을 정확히 이렇게 명시한다.

> "If the word is double-quoted, `${name[*]}` expands to a single word with the value of each array member separated by the first character of the `IFS` variable, and `${name[@]}` expands each element of name to a separate word." — GNU Bash Reference Manual, "Arrays"

즉 큰따옴표 안에서 `"${arr[*]}"`는 배열 요소 전체를 **`IFS`의 첫 글자**로 이어 붙인 문자열 하나가 되고, `"${arr[@]}"`는 요소 각각이 독립된 단어로 남는다. `IFS`를 바꾸지 않은 기본 상태에서는 첫 글자가 공백이라 두 결과가 눈으로는 똑같이 보이기 쉽지만, 명령에 인자로 넘겼을 때의 개수는 완전히 다르다.

```bash
arr=("a b" "c d")
set -- "${arr[@]}"
echo "@ 방식 - 인자 개수: $#"        # 2 (요소 "a b"와 "c d" 각각 하나의 인자)

set -- "${arr[*]}"
echo "* 방식 - 인자 개수: $#"        # 1 (전체가 "a b c d"라는 문자열 하나로 합쳐짐)

IFS=,
set -- "${arr[*]}"
echo "* + IFS=, 방식: $1"           # a b,c d (IFS의 첫 글자인 쉼표로 연결됨)
unset IFS
```

큰따옴표 없이 `${arr[@]}`와 `${arr[*]}`를 그냥 쓰면 이 차이가 사라진다 — 둘 다 단어 분리 단계를 거쳐 공백 기준으로 쪼개진, 사실상 동일한 결과가 된다. 차이는 **오직 큰따옴표로 감쌌을 때만** 나타난다. 그래서 배열을 명령 인자로 안전하게 펼치려면 거의 항상 `"${arr[@]}"`를 쓴다 — 공백이나 특수문자가 포함된 요소도 인자 하나로 유지되기 때문이다.

**bash 배열은 POSIX `/bin/sh`에 없는 bash 확장이다**: 배열(`name=(...)`, `${arr[@]}`, `declare -A`)은 POSIX Shell Command Language 표준에 정의돼 있지 않은 bash 고유 기능이다. 스크립트 맨 위에 `#!/bin/sh`를 쓰거나 `sh script.sh`로 실행하면, `/bin/sh`가 dash 같은 최소 POSIX 셸로 연결된 시스템(대표적으로 Debian/Ubuntu)에서는 배열 문법이 문법 오류를 낸다. 배열을 쓰는 스크립트는 반드시 셔뱅을 `#!/bin/bash`로 명시하고, `bash script.sh`처럼 bash로 직접 실행해야 한다.

```bash
#!/bin/sh
arr=(1 2 3)     # dash에서 실행하면: syntax error near unexpected token '('
```

**중괄호 확장 `{1..10}`은 반복문이 아니라 텍스트 치환이다**: `{1..10}`을 보면 반복문처럼 느껴지기 쉽지만, 실제로는 셸이 명령을 실행하기도 전에 그 텍스트를 `1 2 3 4 5 6 7 8 9 10`이라는 10개의 단어로 미리 펼쳐 쓰는 것이다. GNU Bash Reference Manual이 명시하듯 "brace expansion is performed before any other expansions"이며 "strictly textual"하다 — 순수하게 텍스트를 다시 쓰는 단계일 뿐, 조건을 평가하며 반복을 도는 제어 구조가 아니다. 이 때문에 위 예시 7에서 확인했듯 `report-{2024,2025,2026}.txt`는 그런 이름의 파일이 하나도 없어도 세 단어로 그대로 펼쳐진다. 반면 파일명 확장(글로빙, `*.txt`)은 확장 순서상 중괄호 확장보다 훨씬 뒤에 일어나며 실제 파일 시스템과 대조해 매칭되는 파일이 있을 때만 그 파일명으로 치환된다 — 매칭되는 파일이 하나도 없으면 기본 설정에서는 패턴 문자열 자체가 그대로 남는다(`shopt -s nullglob`을 켜면 빈 문자열로 사라진다). 겉모습이 비슷해 보여도 "존재 여부와 무관하게 항상 펼쳐지는 텍스트 치환"과 "존재하는 것만 골라내는 검색"이라는 정반대의 동작 원리를 가진다.

## 흔한 오개념

<strong>"인덱스 배열의 인덱스는 항상 0부터 연속된 정수다"</strong>는 흔한 오해다. `unset`으로 중간 요소를 지우거나 `arr[10]=x`처럼 특정 인덱스에만 값을 대입하면 인덱스 사이에 구멍이 생기는 sparse 배열이 된다. 이때 `${#arr[@]}`가 반환하는 값은 "요소 개수"이지 "가장 큰 인덱스+1"이 아니므로, 배열을 순회할 때는 `for i in $(seq 0 N)`처럼 인덱스를 직접 만들기보다 `"${!arr[@]}"`(실제 존재하는 인덱스 목록)나 `"${arr[@]}"`(값 자체)로 순회하는 편이 안전하다.

<strong>"`{1..10}`은 파일명 확장(글로빙)의 일종이라 실제 대상이 있어야 동작한다"</strong>도 자주 나오는 오해다. 위 "주의사항·함정"에서 확인했듯 중괄호 확장은 글로빙보다 먼저 일어나는 순수 텍스트 치환이라 대상의 존재 여부와 무관하게 항상 펼쳐진다. `*.txt`가 매칭되는 파일이 없을 때 다르게 동작하는 것과 비교하면 이 차이가 분명해진다.

## 다음 장에서는

[32장: functions](/post/bashshell/bash-shell-functions-code-reuse/)에서는 반복되는 코드 블록을 이름 붙여 재사용하는 함수를 다룬다. 이 장에서 배운 배열은 함수의 인자로 그대로 넘기거나(`"$@"`와 함께), 함수 안에서 지역 변수로 선언(`local -a`/`local -A`)해 활용할 수 있다 — 다음 장은 그 조합을 실전 예제로 이어간다.

## 평가 기준

- 인덱스 배열과 연관 배열의 차이를 설명하고, `declare -A` 없이 연관 배열을 쓸 수 없는 이유를 말할 수 있다.
- compound assignment(`name=(...)`)로 배열을 생성하고, `${arr[i]}`·`${#arr[@]}`·`${!arr[@]}`로 요소·길이·인덱스를 조회할 수 있다.
- `"${arr[@]}"`와 `"${arr[*]}"`가 큰따옴표 안에서 어떻게 다르게 동작하는지(단어 개수, `IFS` 첫 글자의 역할) 원문 근거로 설명할 수 있다.
- 셸 확장의 순서(중괄호 확장 → 물결/변수/산술 확장·명령 치환 → 단어 분리 → 파일명 확장)를 나열할 수 있다.
- 중괄호 확장이 텍스트 치환이고 글로빙이 파일 시스템 검색이라는 근본적 차이를 설명하고, bash 배열이 POSIX `/bin/sh`에서 동작하지 않는 이유를 말할 수 있다.

## 참고

- [Arrays — GNU Bash Reference Manual](https://doc.guix.gnu.org/bash/latest/en/html_node/Arrays.html)
- [Shell Parameter Expansion — GNU Bash Reference Manual](https://doc.guix.gnu.org/bash/latest/en/html_node/Shell-Parameter-Expansion.html)
- [Brace Expansion — GNU Bash Reference Manual](https://doc.guix.gnu.org/bash/latest/en/html_node/Brace-Expansion.html)
- [Shell Expansions — GNU Bash Reference Manual](https://doc.guix.gnu.org/bash/latest/en/html_node/Shell-Expansions.html)
