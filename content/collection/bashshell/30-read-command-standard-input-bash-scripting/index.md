---
draft: false
slug: read-command-standard-input-bash-scripting
title: "[Bash Shell] 30. read - 표준입력과 사용자 입력"
description: "read가 표준입력의 한 줄을 IFS 규칙대로 쪼개 변수에 담는 빌트인이라는 점과, -p·-s·-a·-t·-n 옵션, -r 없이 쓸 때 백슬래시가 이스케이프로 해석되는 SC2162 함정, while read의 리다이렉션·파이프 차이를 정리합니다."
date: 2026-08-24
lastmod: 2026-08-24
collection_order: 300
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
- Stdin
- IO(Input/Output)
- Array(배열)
- Timeout(타임아웃)
- Password(비밀번호)
- Quick-Reference
- Read-Builtin
- Field-Splitting
- IFS
- Escape-Character
- Backslash
- ShellCheck
- SC2162
- User-Input
- Prompt
- While-Read-Loop
- Subshell
- Shell-Scripting
- Shell-Builtin
image: "wordcloud.png"
---

`read`는 표준입력의 한 줄을 읽어 변수(들)에 나눠 담는 빌트인이다. 스크립트가 사용자에게 값을 물어보거나, 파일·파이프에서 들어오는 데이터를 한 줄씩 처리하는 통로가 바로 이 명령이다. 이 장은 `read`의 옵션과 필드 분리 규칙, 그리고 `-r` 없이 썼을 때 벌어지는 흔한 사고를 다룬다.

## 이 장을 읽기 전에

직전 챕터인 [29장: case와 산술 연산](/post/bashshell/case-statement-arithmetic-expansion-bash/)의 예시에서 이미 `read -rp "환경을 선택하세요 ..." env`로 사용자 입력을 받아 `case`로 분기하는 코드를 썼다. [28장: for, while](/post/bashshell/for-while-loop-bash-shell-scripting/)에서도 `while read -r line; do ... done < file.txt`와 `while IFS=: read -r user _ uid _; do ... done < /etc/passwd`로 파일을 한 줄씩 읽는 패턴을 예고 없이 미리 보여줬다. 이 장은 그 두 장에서 "일단 써 본" `read`를 정식으로 분해한다 — 어떤 옵션이 있고, 여러 변수에 값이 어떻게 나뉘어 들어가는지, `-r`을 빼면 왜 위험한지를 다룬다.

난이도는 초급이다. 27장의 `if`/`test`와 28장의 `while`을 읽을 수 있다고 가정한다.

**다루지 않는 것**: `read -a`로 배열 전체를 채우는 문법과 `"${arr[@]}"` 전개는 [31장: 배열과 셸 확장](/post/bashshell/bash-arrays-brace-parameter-expansion/)에서 본격적으로 다룬다 — 이 장에서는 `-a`가 무엇을 하는지만 짧게 미리 보여준다. `while read` 파이프의 오른쪽이 서브셸에서 실행되어 변수가 밖으로 전달되지 않는 문제 자체와 그 해결책(프로세스 치환, `lastpipe`)은 [28장](/post/bashshell/for-while-loop-bash-shell-scripting/)에서 이미 다뤘으므로, 이 장의 "주의사항·함정"에서는 그 결과를 `read`의 관점에서 다시 확인만 하고 해결책을 반복하지 않는다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| 입문 | 개요 + 정신 모델, 핵심 개념의 기본 문법·`-p`/`-s` | 사용자에게 프롬프트를 보여주고 입력값을 변수에 담을 수 있다 |
| 중급 | 핵심 개념 전체, 예시 | 여러 변수에 값을 나눠 담고, `-t`/`-n`/`-a`로 타임아웃·문자 수·배열을 다룰 수 있다 |
| 심화 | 주의사항·함정, 흔한 오개념 | `-r`을 빠뜨렸을 때 생기는 사고를 설명하고, `while read`의 리다이렉션·파이프 차이를 코드에서 구분할 수 있다 |

## 개요 + 정신 모델

`read`는 셸이 표준입력(또는 `-u`로 지정한 파일 디스크립터)에서 **한 줄**을 가져와, 그 줄을 `IFS`(내부 필드 구분자) 규칙에 따라 단어로 쪼갠 뒤 순서대로 변수에 대입하는 빌트인이다. 이 한 문장이 `read`의 정신 모델 전부다 — 변수를 하나만 주면 그 변수에 줄 전체가 들어가고, 변수를 여러 개 주면 각 단어가 순서대로 나뉘어 들어가되 마지막 변수는 남은 단어와 그 사이 구분자까지 통째로 떠안는다. `read`가 없다면 셸 스크립트는 미리 정해둔 값만 다룰 수 있는 일방향 도구에 머문다 — `read`가 있어야 스크립트가 실행 중에 사용자와 대화하거나, 파일·파이프로 들어오는 줄 단위 데이터를 그때그때 소비할 수 있다.

## 핵심 개념

### 기본 문법과 단어 분배

GNU Bash Reference Manual은 `read`의 문법을 다음과 같이 정의한다.

> "read [-ers] [-a aname] [-d delim] [-i text] [-n nchars] [-N nchars] [-p prompt] [-t timeout] [-u fd] [name …]" — GNU Bash Reference Manual, "Bash Builtin Commands"

`read`는 한 줄을 읽어 `IFS`로 단어를 나눈 뒤 나열된 변수명(`name ...`)에 순서대로 대입한다. 변수 개수와 단어 개수가 맞지 않을 때의 동작은 명확히 정의되어 있다.

> "If there are more words than names, the remaining words and their intervening delimiters are assigned to the last name. If there are fewer words read from the input stream than names, the remaining names are assigned empty values." — GNU Bash Reference Manual, "Bash Builtin Commands"

즉 단어가 변수보다 많으면 남는 단어 전부(구분자 포함)가 마지막 변수 하나에 몰리고, 단어가 변수보다 적으면 남는 변수는 빈 문자열이 된다. 변수를 아예 지정하지 않으면 어떻게 될까.

> "If no names are supplied, the line read is assigned to the variable REPLY." — GNU Bash Reference Manual, "Bash Builtin Commands"

`read`만 단독으로 쓰면 읽은 줄이 자동으로 `REPLY`에 담긴다는 뜻이다.

### IFS와 필드 분리

`read`가 한 줄을 단어로 쪼개는 기준은 `IFS` 변수다. 기본값은 공백·탭·개행이며, GNU Bash Reference Manual은 이 기본값의 동작을 다음과 같이 규정한다.

> "If IFS is unset, or its value is exactly \<space\>\<tab\>\<newline\>, the default, then sequences of \<space\>, \<tab\>, and \<newline\> at the beginning and end of the results of the previous expansions are ignored, and any sequence of IFS characters not at the beginning or end serves to delimit words." — GNU Bash Reference Manual, "Word Splitting"

풀어 쓰면 줄 앞뒤의 공백·탭은 무시되고, 줄 중간의 공백·탭 연속은 몇 개가 이어지든 구분자 하나로 취급된다. `IFS`를 다른 문자(예: `:`, `,`)로 바꾸면 이 규칙이 그 문자 기준으로 바뀌고, 앞뒤 무시 규칙도 사라진다 — CSV나 `/etc/passwd`처럼 고정 구분자로 된 데이터를 파싱할 때 `IFS=:`처럼 임시로 바꿔 쓰는 이유다.

### 주요 옵션

| 옵션 | 동작 |
|---|---|
| `-p prompt` | 입력을 기다리기 전에 개행 없이 `prompt`를 출력한다 |
| `-s` | 조용한 모드. 터미널 입력이면 글자를 화면에 echo하지 않는다(비밀번호 입력용) |
| `-a aname` | 읽은 단어들을 배열 `aname`의 인덱스 0부터 순서대로 채운다(31장에서 상세) |
| `-t timeout` | `timeout`초 안에 한 줄을 다 읽지 못하면 시간 초과로 실패 처리한다 |
| `-n nchars` | 정확히 `nchars` 글자를 읽으면 개행을 기다리지 않고 반환한다(구분자를 만나면 그 전에 반환) |
| `-N nchars` | 구분자를 무시하고 정확히 `nchars` 글자를 읽을 때까지 반환하지 않는다 |
| `-d delim` | 개행 대신 `delim`의 첫 글자를 줄 종료 문자로 쓴다 |
| `-r` | 백슬래시를 이스케이프 문자로 해석하지 않는다(원시 모드) |
| `-u fd` | 표준입력이 아니라 파일 디스크립터 `fd`에서 읽는다 |
| `-e` | Readline을 사용해 줄을 입력받는다(방향키·히스토리 편집 가능) |
| `-i text` | `-e`와 함께 써서 편집 버퍼에 `text`를 미리 채워 둔다 |

### 종료 상태

`read`의 종료 코드도 명확히 규정되어 있다.

> "The exit status is zero, unless end-of-file is encountered, read times out (in which case the status is greater than 128), a variable assignment error occurs, or an invalid file descriptor is supplied." — GNU Bash Reference Manual, "Bash Builtin Commands"

파일 끝(EOF)에 도달하거나 `-t` 타임아웃이 발생하면 `read`는 실패(0이 아닌 코드)를 반환한다. 이 성질 덕분에 `while read -r line; do ... done < file`처럼 `read` 자체를 `while`의 조건으로 쓸 수 있다 — 더 읽을 줄이 없어지는 순간이 곧 반복 종료 조건이 된다. 타임아웃으로 실패한 경우 종료 코드가 128보다 크다는 점은, [33장](/post/bashshell/exit-status-set-trap-bash-error-handling/)에서 다룬 "신호로 종료된 프로세스는 128+신호번호를 반환한다"는 관례와 같은 맥락이다.

## 예시

### 1. 가장 단순한 형태 — 변수 하나

```bash
read -rp "이름을 입력하세요: " name
echo "안녕하세요, $name 님"
```

### 2. 여러 변수에 나눠 담기

```bash
read -rp "이름과 나이를 공백으로 구분해 입력하세요: " name age
echo "이름: $name, 나이: $age"
```

단어가 두 개보다 많으면 세 번째 단어부터는 `age`에 나머지 전부가 붙어서 들어간다 — "핵심 개념"에서 확인한 "남는 단어는 마지막 변수에 몰린다" 규칙이 그대로 적용된 결과다.

### 3. 변수 없이 REPLY로 받기

```bash
read -rp "계속하시겠습니까? (y/n) "
if [[ $REPLY == y ]]; then
    echo "계속 진행합니다"
fi
```

### 4. -s로 비밀번호 입력받기

```bash
read -rsp "비밀번호: " password
echo
echo "입력된 길이: ${#password}자"
```

`-s`는 터미널 echo만 끌 뿐 입력 자체를 암호화하지 않는다 — 화면에 안 보이게 할 뿐, 셸 히스토리나 프로세스 인자로 노출되지 않게 하려면 별도 조치(변수로만 다루고 명령행 인자로 넘기지 않기 등)가 필요하다.

### 5. -t로 타임아웃 걸기

```bash
if read -rt 5 -p "5초 안에 아무 키나 입력하세요: " answer; then
    echo "입력받음: $answer"
else
    echo "시간 초과로 진행합니다"
fi
```

### 6. -n으로 글자 수 제한하기

```bash
read -rn 1 -p "계속하려면 아무 키나 누르세요..." key
echo
echo "누른 키: $key"
```

`-n 1`은 한 글자만 읽으면 개행을 기다리지 않고 즉시 반환한다 — Y/N 확인처럼 Enter 없이 즉답을 받고 싶을 때 쓴다.

### 7. IFS를 바꿔 구분자가 다른 데이터 읽기

```bash
while IFS=, read -r name score grade; do
    echo "$name: 점수 $score, 등급 $grade"
done <<'EOF'
Alice,92,A
Bob,78,C
EOF
```

`IFS=,`는 이 `read` 명령 실행 동안만 유효한 임시 대입이라, 루프가 끝나면 `IFS`는 원래 값(기본 공백/탭/개행)으로 돌아온다.

### 8. -a로 배열에 통째로 담기 (31장 예고)

```bash
read -ra fields <<< "apple banana cherry"
echo "두 번째 항목: ${fields[1]}"
echo "전체 개수: ${#fields[@]}"
```

배열 인덱싱(`${fields[1]}`)과 전체 전개(`${fields[@]}`) 문법 자체는 [31장](/post/bashshell/bash-arrays-brace-parameter-expansion/)에서 다룬다. 여기서는 `-a`가 단어를 변수 하나가 아니라 배열 전체에 순서대로 채운다는 것만 확인한다.

### 9. while read < file — 리다이렉션은 서브셸을 만들지 않는다

```bash
count=0
while read -r line; do
    count=$((count + 1))
done < access.log
echo "총 줄 수: $count"   # 실제 줄 수가 그대로 출력된다
```

### 10. -r 없이 읽으면 백슬래시가 사라진다

```bash
printf 'C:\\Users\\name\n' | { read line; echo "[$line]"; }
printf 'C:\\Users\\name\n' | { read -r line; echo "[$line]"; }
```

첫 번째는 `-r`이 없어 백슬래시가 이스케이프로 해석되고, 두 번째는 `-r`이 있어 입력 그대로 보존된다 — 정확한 차이는 "주의사항·함정"에서 다룬다.

## 주의사항·함정

**`-r` 없이 `read`를 쓰면 백슬래시가 이스케이프로 해석된다.** GNU Bash Reference Manual은 `-r`의 동작을 다음과 같이 규정한다.

> "-r: Backslash does not act as an escape character. The backslash is considered to be part of the line. In particular, a backslash-newline pair may not be used as a line continuation." — GNU Bash Reference Manual, "Bash Builtin Commands"

거꾸로 말하면 `-r`이 **없을 때**는 백슬래시가 이스케이프로 동작한다 — 백슬래시 다음 글자를 문자 그대로 취급하며 그 과정에서 백슬래시 자신은 사라지고, 줄 끝의 `\<개행>`은 줄바꿈이 아니라 다음 줄과 이어붙이는 연속 문자로 소비된다. 예시 10에서 확인했듯 `C:\Users\name`을 `-r` 없이 읽으면 `C:Usersname`처럼 백슬래시가 통째로 사라진다. 윈도우 스타일 경로, 정규식 패턴, `\n`·`\t` 같은 이스케이프 시퀀스가 포함된 텍스트를 그대로 보존해야 하는 모든 상황에서 이 함정에 걸린다. ShellCheck는 이 문제를 [SC2162](https://www.shellcheck.net/wiki/SC2162) 규칙으로 정확히 지적한다 — "read without -r will mangle backslashes"라는 경고 메시지 그대로, 사실상 모든 `read` 호출에 `-r`을 습관적으로 붙이는 것이 안전하다.

**`IFS` 기본값이 필드 분리 방식을 좌우한다.** "핵심 개념"에서 확인했듯 기본 `IFS`(공백/탭/개행)는 줄 앞뒤의 공백을 버리고 중간의 연속 공백을 구분자 하나로 뭉친다. 탭으로 구분된 데이터를 읽을 때 이 기본 동작을 그대로 쓰면 빈 필드가 사라지거나 필드가 밀리는 사고가 난다 — 필드 사이에 빈 값이 있을 수 있는 데이터(예: `이름,,점수`처럼 중간 필드가 비어 있는 CSV)는 `IFS=,`로 구분자를 명시해야 빈 필드가 스킵되지 않는다.

**`while read line < file`과 `cat file | while read line`은 변수의 생존 범위가 다르다.** [19장: 파이프](/post/bashshell/pipe-operator-linux-command-chaining/)와 [28장](/post/bashshell/for-while-loop-bash-shell-scripting/)에서 다뤘듯, 파이프로 연결된 명령은 각각 별도의 서브셸에서 실행된다.

| 형태 | 서브셸 여부 | 루프 안에서 갱신한 변수 |
|---|---|---|
| `while read -r line; do ...; done < file` | 없음(리다이렉션) | 루프가 끝난 뒤에도 그대로 남는다 |
| `cat file \| while read -r line; do ...; done` | 있음(파이프 오른쪽) | 서브셸이 끝나는 순간 사라진다 |

```bash
count=0
while read -r line; do
    count=$((count + 1))
done < access.log
echo "리다이렉션: $count"     # 실제 줄 수

count=0
cat access.log | while read -r line; do
    count=$((count + 1))
done
echo "파이프: $count"         # 항상 0
```

`< file` 형태는 `while` 전체가 현재 셸에서 그대로 실행되므로 `count`가 루프 밖에서도 살아 있지만, `cat file |` 형태는 `while`이 파이프 오른쪽이라 별도 서브셸에서 돌고 그 서브셸의 `count`는 서브셸이 끝나는 즉시 사라진다. 게다가 `cat file | while ...`은 `cat` 프로세스 하나를 더 띄우는 불필요한 비용까지 있으므로("Useless Use of Cat"), 파일을 통째로 읽을 때는 애초에 리다이렉션 형태를 우선 고려하는 편이 낫다. 파이프가 꼭 필요한 상황(다른 명령의 출력을 이어받아야 할 때)의 해결책은 [28장](/post/bashshell/for-while-loop-bash-shell-scripting/)에서 다룬 프로세스 치환·`lastpipe`를 그대로 적용한다.

## 흔한 오개념

<strong>"`read`는 입력을 한 줄 통째로 변수에 담는다"</strong>는 변수를 하나만 쓸 때만 맞는 말이다. 변수를 두 개 이상 나열하면 `IFS` 규칙에 따라 줄이 단어로 쪼개져 각 변수에 순서대로 들어가고, 남는 단어는 마지막 변수에 몰린다. `read line`처럼 변수를 하나만 쓰면 이 분리가 눈에 띄지 않아 "그냥 줄 전체가 들어간다"고 오해하기 쉽지만, 실제로는 변수 개수만큼 분리를 시도한 결과가 우연히 하나로 합쳐진 것이다.

<strong>"`-t` 타임아웃으로 실패하면 종료 코드가 1이다"</strong>도 흔히 하는 오해다. "핵심 개념"에서 인용한 GNU Bash Reference Manual대로 타임아웃 실패의 종료 코드는 128보다 큰 값이다 — EOF나 일반 실패와 같은 `1`이 아니다. `if read -t 5 ...; then ... else ...; fi`처럼 성공/실패만 분기할 때는 문제가 안 되지만, `$?` 값 자체로 실패 원인(EOF인지 타임아웃인지)을 구분하려는 코드는 이 차이를 놓치면 잘못된 분기를 탄다.

## 다음 장에서는

[31장: 배열과 셸 확장](/post/bashshell/bash-arrays-brace-parameter-expansion/)에서는 이 장의 예시 8에서 잠깐 다룬 `read -a`가 채워 넣는 대상, 즉 배열 자체를 정식으로 다룬다. 인덱스 배열 선언과 순회, `"${arr[@]}"`와 `"${arr[*]}"`의 차이, 브레이스 확장·파라미터 확장까지 셸이 값을 여러 개로 펼치는 방법 전반을 다룬다.

## 평가 기준

- `read`가 한 줄을 `IFS` 규칙에 따라 단어로 나눠 변수에 순서대로 대입하며, 변수보다 단어가 많으면 마지막 변수에 나머지가 몰린다는 점을 설명할 수 있다.
- `-p`, `-s`, `-a`, `-t`, `-n`의 각 동작을 구분하고 상황에 맞게 조합해 쓸 수 있다.
- `-r` 없이 `read`를 쓰면 백슬래시가 이스케이프로 해석돼 입력이 변형된다는 점(SC2162)을 알고, 습관적으로 `-r`을 붙일 수 있다.
- `while read line < file`(서브셸 없음)과 `cat file | while read line`(서브셸 있음)의 변수 생존 범위 차이를 코드로 구분할 수 있다.
- `read`의 타임아웃 실패 종료 코드가 128보다 크다는 점을 알고, EOF·일반 실패와 구분해 처리할 수 있다.

## 참고

- [Bash Builtin Commands — GNU Bash Reference Manual](https://doc.guix.gnu.org/bash/latest/en/html_node/Bash-Builtins.html)
- [Word Splitting — GNU Bash Reference Manual](https://doc.guix.gnu.org/bash/latest/en/html_node/Word-Splitting.html)
- [SC2162: read without -r will mangle backslashes — ShellCheck Wiki](https://www.shellcheck.net/wiki/SC2162)
