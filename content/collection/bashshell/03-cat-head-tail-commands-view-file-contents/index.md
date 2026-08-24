---
draft: false
slug: cat-head-tail-commands-view-file-contents
title: "[Bash Shell] 03. cat, head, tail - 파일 내용 출력과 일부 보기"
description: "cat으로 파일 전체를 표준 출력에 흘려보내는 법부터, head·tail로 앞뒤 N줄·N바이트만 가볍게 스트리밍해 보는 법, tail -f/-F로 로그를 실시간 추적하는 법까지 옵션 표와 실전 예시 18개, GNU·BSD 이식성 차이로 정리합니다."
date: 2026-03-15
lastmod: 2026-08-23
collection_order: 30
categories:
- Bash Shell
tags:
- Bash
- Shell(셸)
- Linux(리눅스)
- Terminal
- Command
- File-System
- Automation(자동화)
- Stdin
- Stdout
- String(문자열)
- Pipe(파이프)
- Pipeline
- Troubleshooting(트러블슈팅)
- Pitfalls(함정)
- Best-Practices
- Guide(가이드)
- Tutorial(튜토리얼)
- Reference(참고)
- Quick-Reference
- How-To
- Tips
- Beginner
- cat
- UUOC
- 파일연결
- concatenate
- GNU-Coreutils
- BSD-Unix
- POSIX
- Command-Line-Tool
- 표준입력
- 표준출력
- 리다이렉션
- head
- tail
- tail-f
- follow
- 로그추적
- Streaming
- Real-Time(실시간)
- Logging(로깅)
- Monitoring(모니터링)
image: "wordcloud.png"
---

`cat`("concatenate"의 줄임)은 리눅스·유닉스에서 <strong>하나 이상의 파일 내용을 표준 출력으로 그대로 이어 붙여 흘려보내는</strong> 명령어다. 사람이 화면으로 읽을 때뿐 아니라, 파이프라인의 시작점에서 파일을 스트림으로 바꿔 다음 명령에 넘겨주는 용도로도 자주 쓴다. 같은 "파일 내용을 표준 출력으로 보여준다"는 목적을 공유하지만 전체가 아니라 <strong>앞부분만</strong> 또는 <strong>뒷부분만</strong> 가볍게 확인하고 싶을 때는 `head`와 `tail`을 쓴다 — 특히 `tail -f`는 커지고 있는 로그 파일을 실시간으로 추적하는 표준 도구라 `cat`만으로는 할 수 없는 일을 한다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [2장: ls](/post/bashshell/ls-command-list-files-directories-linux/)에서 이어진다. 앞 장에서 `ls`로 어떤 파일이 있는지 목록을 살펴봤다면, 이 장에서는 그 목록 안의 파일을 실제로 열어 내용을 확인한다 — "무엇이 있는지 본다"에서 "그 안에 무엇이 들어 있는지 본다"로 넘어가는 자연스러운 흐름이며, 아직 <strong>Part 1(셸 기초와 탐색)</strong> 진행 중이다.

**이 장의 깊이**: **입문** 난이도다. 기본 출력, 여러 파일 연결, 줄 번호·비인쇄 문자 표시 옵션에 더해 `head`·`tail`로 파일의 일부만 보는 법과 `tail -f`의 실시간 추적까지 다룬다. **다루지 않는 것**: `cat`으로 파일을 만들거나 이어붙일 때 쓰는 리다이렉션(`>`, `>>`) 연산자 자체의 문법은 [20장: 리다이렉션](/post/bashshell/io-redirection-linux-bash-tutorial/)에서 다루므로, 여기서는 `cat`의 관점에서 필요한 만큼만 언급한다. 대용량 파일을 화면 단위로 나눠 보거나 검색하는 방법은 이 장에서 다루지 않고 바로 다음 장인 [4장: less, more](/post/bashshell/less-more-commands-view-large-files-linux/)로 넘긴다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| 지금 바로 파일 내용을 확인해야 하는 사람 | "사용법·옵션"의 기본 문법, "예시"의 "기본 출력"·"여러 파일 연결" | `cat file`로 내용을 바로 확인하고, 여러 파일을 순서대로 이어 붙여 새 파일로 저장할 수 있다 |
| 로그·설정 파일을 정밀하게 들여다봐야 하는 사람 | "옵션"의 "번호 매김"·"비인쇄 문자 표시", "주의사항·함정" 전체 | 줄 번호·탭·줄 끝 문자를 옵션으로 드러내고, `cat`을 잘못 쓸 때 생기는 파괴적 동작과 이식성 함정을 피할 수 있다 |
| 파일 앞부분만 훑어보거나 로그를 실시간으로 지켜봐야 하는 사람 | "head, tail" 섹션 전체 | `head -n`/`tail -n`으로 파일의 일부만 가볍게 확인하고, `tail -f`/`-F`로 커지는 로그를 실시간 추적할 수 있다 |

---

## 개요 + 정신 모델

`cat`의 정신 모델은 단순하다 — **입력을 가리지 않고, 처음부터 끝까지, 있는 그대로 표준 출력에 흘려보낸다.** 파일을 여러 개 지정하면 각 파일의 내용을 순서대로 이어 붙여 마치 하나의 연속된 스트림인 것처럼 출력하고, 파일을 지정하지 않으면 표준 입력을 그대로 받아 출력한다. 이 동작 방식에는 파일 크기에 대한 판단이나 "사람이 읽기 좋게 나눠서 보여준다"는 배려가 전혀 없다 — `cat`은 파일이 10줄이든 1000만 줄이든 똑같이 전량을 한 번에 쏟아낸다.

이 "가리지 않고 그대로 흘려보낸다"는 성질 때문에 `cat`은 두 가지 상반된 역할을 동시에 수행한다. 사람이 짧은 파일 내용을 눈으로 확인할 때는 그 자체로 완결된 도구이고, 파이프라인 안에서는 파일이라는 정적인 대상을 다른 명령이 받아들일 수 있는 스트림으로 바꿔주는 변환기 역할을 한다. 뒤에서 다룰 "쓸데없는 `cat` 사용"(UUOC) 안티패턴은 대부분 이 두 번째 역할을 오해해서, 이미 파일을 직접 받을 수 있는 명령 앞에 굳이 변환기를 끼워 넣는 데서 생긴다.

## 사용법 · 옵션

```bash
cat [옵션] [파일...]
```

파일을 여러 개 지정하면 순서대로 이어서 출력한다. 파일 이름 대신 `-`을 쓰거나 아예 생략하면 표준 입력을 읽는다.

### 번호 매김

| 옵션 | 긴 옵션 | 설명 |
|------|---------|------|
| `-n` | `--number` | 모든 출력 줄에 번호를 붙인다 |
| `-b` | `--number-nonblank` | 빈 줄을 제외하고 내용이 있는 줄에만 번호를 붙인다(`-n`보다 우선) |
| `-s` | `--squeeze-blank` | 연속된 빈 줄을 한 줄로 압축한다 |

### 비인쇄 문자·줄 끝 표시

| 옵션 | 긴 옵션 | 설명 |
|------|---------|------|
| `-A` | `--show-all` | `-vET`와 동일 — 비인쇄 문자·탭·줄 끝을 모두 표시 |
| `-E` | `--show-ends` | 각 줄 끝에 `$`(윈도우식 줄바꿈이면 `^M$`) 표시 |
| `-T` | `--show-tabs` | 탭 문자를 `^I`로 표시 |
| `-v` | `--show-nonprinting` | 제어 문자를 `^`·`M-` 표기법으로 표시(줄바꿈·탭 제외) |
| `-e` | | `-vE`와 동일 |
| `-t` | | `-vT`와 동일 |

### 기타

| 옵션 | 긴 옵션 | 설명 |
|------|---------|------|
| `-u` | | (무시됨 — 항상 버퍼링 없이 출력하는 GNU 구현이라 하위 호환용으로만 남아 있다) |
| | `--help` | 도움말 출력 후 종료 |
| | `--version` | 버전 정보 출력 후 종료 |

## 예시

### 기본 출력

```bash
# 파일 전체 내용을 화면에 출력
cat config.ini

# 표준 입력을 그대로 전달 (동작 확인용)
echo "hello" | cat
```

### 여러 파일 연결

```bash
# 세 파일을 순서대로 이어서 화면에 출력
cat header.txt body.txt footer.txt

# 이어 붙인 결과를 새 파일로 저장
cat header.txt body.txt footer.txt > full.txt

# 기존 파일 끝에 다른 파일 내용을 추가
cat extra.txt >> full.txt
```

### 파일 생성·입력

```bash
# 표준 입력을 받아 그대로 파일로 저장 (Ctrl+D로 입력 종료)
cat > note.txt

# Here Document로 여러 줄을 한 번에 파일로 저장
cat << 'EOF' > note.txt
첫 번째 줄
두 번째 줄
EOF
```

### 번호·비인쇄 문자 확인

```bash
# 줄 번호와 함께 출력
cat -n app.log

# 빈 줄은 번호 없이, 내용 있는 줄만 번호
cat -b app.log

# 탭과 줄 끝을 눈에 보이게 표시 (설정 파일의 숨은 탭 확인)
cat -A Makefile

# 연속된 빈 줄을 한 줄로 압축해서 출력
cat -s messy.txt
```

### 파이프 조합

```bash
# 여러 파일을 이어 붙인 뒤 grep으로 필터링
cat access.log access.log.1 | grep "500"

# 이어 붙인 결과의 줄 수 세기
cat *.csv | wc -l
```

## head, tail — 파일의 앞·뒤 일부만 보기

### 정신 모델

`head`와 `tail`의 정신 모델은 `cat`과 뚜렷이 갈린다 — **파일 전체를 읽어 들이는 대신, 앞부분(`head`) 또는 뒷부분(`tail`)의 정해진 줄 수·바이트 수만 스트리밍으로 읽어 온다.** `cat`이 "가리지 않고 전량을 흘려보낸다"는 전제 위에 서 있다면, `head`·`tail`은 "필요한 건 대개 파일의 극히 일부, 특히 로그라면 맨 뒤 최신 내용"이라는 전제 위에 서 있다. 그래서 수 GB짜리 로그 파일이라도 `head -n 20`은 앞 20줄만 읽고 즉시 끝나고, `tail -n 20`은 파일 끝에서부터 필요한 만큼만 거슬러 읽으므로 `cat`보다 훨씬 가볍다.

`tail`에는 여기서 한 걸음 더 나아간 역할이 있다. `-f`(follow) 옵션을 주면 파일 끝에 도달한 뒤에도 종료하지 않고, 파일에 새 줄이 추가될 때마다 그 내용을 즉시 화면에 흘려보낸다. 이 덕분에 `tail -f`는 애플리케이션 로그를 실시간으로 지켜보는 사실상의 표준 도구가 됐다 — `head`에는 이에 대응하는 "앞부분을 실시간으로 지켜본다"는 개념 자체가 없다. 파일의 앞부분은 한 번 쓰이고 나면 보통 다시 바뀌지 않지만, 뒷부분(끝)은 로그처럼 계속 자라나는 파일에서 바로 그 "지금 막 추가된" 지점이기 때문이다.

### 사용법 · 옵션

```bash
head [옵션] [파일...]
tail [옵션] [파일...]
```

옵션을 주지 않으면 각각 파일의 <strong>앞 10줄</strong>, <strong>뒤 10줄</strong>을 출력한다. 파일을 여러 개 지정하면 파일마다 `==> 파일명 <==` 헤더를 붙여 구분한다.

| 옵션 | 긴 옵션 | 설명 |
|------|---------|------|
| `-n K` | `--lines=K` | 앞(`head`)·뒤(`tail`) K줄만 출력 |
| `-c K` | `--bytes=K` | 앞(`head`)·뒤(`tail`) K바이트만 출력 |
| `-n +K` | | (`tail` 전용) 처음부터 K번째 줄부터 끝까지 출력 — 헤더 한 줄을 건너뛸 때 유용 |
| `-f` | `--follow` | (`tail` 전용) 파일 끝에 도달해도 종료하지 않고 새로 추가되는 내용을 실시간으로 출력 |
| `-F` | | (`tail` 전용, GNU) `--follow=name --retry`와 동일 — 파일이 삭제·교체돼도 같은 이름의 파일을 다시 열어 계속 추적 |
| `-q` | `--quiet`, `--silent` | 파일이 여럿이어도 `==> 파일명 <==` 헤더를 생략 |
| `-v` | `--verbose` | 파일이 하나뿐이어도 헤더를 항상 출력 |

`head -n -K`(K 앞에 `-`)는 "뒤 K줄을 제외한 나머지 전부"를, `tail -n +K`(K 앞에 `+`)는 "K번째 줄부터 끝까지"를 뜻한다 — 부호 하나로 기준점이 반대로 뒤집히므로 스크립트에 쓸 때는 특히 주의해서 읽는다.

### 예시

```bash
# 로그 파일을 실시간으로 추적 (Ctrl+C로 종료)
tail -f app.log

# 파일 앞 20줄만 확인
head -n 20 file.txt

# CSV의 헤더 줄을 제외하고 두 번째 줄부터 출력
tail -n +2 file.csv

# 바이너리·텍스트 파일의 앞 100바이트만 확인 (파일 형식 판별 등)
head -c 100 file

# 로그 로테이션에도 끊기지 않는 실시간 추적 (GNU tail)
tail -F /var/log/app.log
```

## 주의사항·함정

**UUOC(Useless Use of Cat)**: `cat file | grep pattern`처럼 파이프 앞에 대상 파일이 하나뿐인데도 습관적으로 `cat`을 앞세우는 패턴은 유닉스 커뮤니티에서 오래전부터 지적돼 온 흔한 안티패턴이다. Perl 창시자 커뮤니티의 Randal L. Schwartz는 1995년 무렵부터 이런 사례에 "Useless Use of Cat Award"라는 이름을 붙여 comp.unix.shell 등지에 꾸준히 게시해 왔다.

> "The purpose of cat is to concatenate (or "catenate") files. If it's only one file, concatenating it with nothing at all is a waste of time, and costs you a process."
> — Randal L. Schwartz, [Useless Use of Cat Award](http://www.smallo.ruhr.de/award.html)

`grep`을 비롯해 대부분의 필터 명령은 파일 이름을 인자로 직접 받을 수 있으므로, `cat file | grep pattern`은 `grep pattern file`로 쓰는 편이 프로세스 하나를 덜 띄우고 더 짧다. 대상 파일이 둘 이상이라 실제로 "이어 붙여야" 하는 상황(`cat a.txt b.txt | grep pattern`)이라면 이는 UUOC가 아니라 `cat`의 정상적인 용례다.

**대용량 파일에 `cat`을 쓰면 터미널이 먹통이 된다**: `cat`은 파일 크기와 무관하게 전체를 한 번에 쏟아내므로, 수 GB짜리 로그 파일에 `cat`을 실행하면 수만 줄이 순식간에 스크롤되어 지나가며 터미널이 한동안 응답하지 않는 것처럼 느껴진다. 필요한 부분만 골라 보거나 검색해야 한다면 화면 단위로 멈춰 가며 읽을 수 있는 [4장: less](/post/bashshell/less-more-commands-view-large-files-linux/)를 쓰는 편이 안전하다.

**자기 자신에게 리다이렉트하면 내용이 사라진다**: `cat file1 file2 > file1`처럼 입력 파일과 출력 대상이 같으면, 셸은 `cat`을 실행하기 **전에** `>`를 먼저 처리해 `file1`을 빈 파일로 만들어(truncate) 버린다. `cat`이 실제로 `file1`을 읽으려는 시점에는 이미 내용이 사라진 뒤라 원본 데이터를 복구할 수 없다. 여러 파일을 합쳐 그중 하나에 덮어써야 한다면 임시 파일에 먼저 쓴 뒤 `mv`로 옮기는 방식이 안전하다.

**GNU와 BSD/macOS `cat`의 옵션 차이**: 이 글의 `-A`, `-E`, `-T`, `--show-*` 계열 긴 옵션은 **GNU coreutils cat**의 확장이다. macOS를 비롯한 BSD 계열 `cat`은 `-b`, `-e`, `-n`, `-s`, `-t`, `-u`, `-v`는 지원하지만 `-A`·`-E`·`-T`나 긴 옵션 이름은 제공하지 않는다(BSD의 `-e`는 GNU와 동일하게 비인쇄 문자와 줄 끝 `$`를 함께 표시하는 조합 옵션이다). 반대로 BSD `cat`에는 표준 출력에 배타적 잠금을 거는 `-l` 옵션이 있는데 이는 GNU `cat`에 없다. POSIX 사양 자체는 `-u`(출력 버퍼링 없음) 외에는 옵션을 규정하지 않으므로, `-b`·`-e`·`-n`·`-s`·`-t`·`-v`조차 "POSIX 확장"으로 분류된다 — 스크립트를 여러 플랫폼에 옮길 때는 이 옵션들이 표준이 아니라 구현별 확장이라는 점을 염두에 둬야 한다.

**`tail -f`는 로그 로테이션에 취약하다 — `-F`와의 차이**: GNU coreutils `tail`의 기본 추적 방식은 `--follow=descriptor`(짧게 `-f`)로, 열려 있는 <strong>파일 디스크립터</strong>를 계속 따라간다. `logrotate` 같은 도구가 로그를 회전시킬 때는 보통 기존 파일을 다른 이름으로 옮긴 뒤 원래 경로에 새 파일을 만드는데, `-f`로 실행 중이던 `tail`은 옮겨진 옛 파일의 디스크립터를 그대로 붙들고 있어 새로 생긴 파일에 쓰이는 내용을 더 이상 보지 못한다 — 화면이 멈춘 것처럼 보이는 흔한 원인이다. `-F`는 `--follow=name --retry`와 동일한 GNU 전용 옵션으로, 디스크립터가 아니라 <strong>파일 이름</strong>을 기준으로 주기적으로 다시 열어 확인하기 때문에 파일이 교체되거나 일시적으로 사라져도(`--retry`) 같은 경로에 다시 나타나는 파일을 놓치지 않고 이어서 추적한다. 로그 로테이션 대상을 실시간으로 지켜봐야 한다면 `-f`가 아니라 `-F`를 쓰는 편이 안전하다. GNU coreutils 매뉴얼도 "이름 변경·삭제·재생성을 아우르며 파일을 추적하려면 `--follow=name`을 쓰라(`Use --follow=name in that case. That causes tail to track the named file in a way that accommodates renaming, removal and creation.`)"고 명시한다([tail(1) - Linux manual page](https://man7.org/linux/man-pages/man1/tail.1.html)). BSD/macOS `tail`의 `-F`도 동일하게 "`-f`를 내포하면서 파일이 이름 변경·회전됐는지 추가로 확인"하는 기능이지만, GNU와 세부 재시도 정책이 다를 수 있으므로 이식성이 중요하면 각 플랫폼 man 페이지로 재확인한다.

**GNU와 BSD `head`/`tail`의 `-n`/`-c` 문법, 그리고 구버전 축약형**: 이 글에서 쓰는 `-n K`, `-c K` 문법은 GNU·BSD 모두 지원하는 현재 표준 형태다. 다만 역사적으로 BSD 계열 `head`/`tail`은 `-n 5` 대신 `head -5`, `tail -5`처럼 옵션 문자 없이 숫자만 붙이는 축약 문법도 오랫동안 허용해 왔다(OpenBSD man 페이지의 `tail -500 foo` 예시가 이 계보다). GNU coreutils도 하위 호환을 위해 이 "obsolete" 문법을 여전히 지원한다 — `head`는 문서에서 "count 앞에 숫자만 오는 구식 옵션 문법(예: `head -5`)을 첫 인자로 지정했을 때만 인식하며, 새 스크립트는 `-n count`를 쓰라"고 명시하고, `tail` 역시 `tail -5f file`처럼 숫자·크기 문자(`b`/`c`/`l`)·`f`를 붙여 쓰는 구식 문법을 지원하되 "표준을 지키려는 스크립트는 `-c count[b]`, `-n count`, `-f`를 대신 쓰라"고 권한다. 즉 이 축약형은 "BSD에만 있던 옛날 문법"이 아니라 GNU에도 하위 호환으로 남아 있는 obsolete 문법이며, 두 진영 모두 신규 코드에서는 `-n`/`-c`를 명시하는 표준 문법을 쓰도록 권고한다는 점이 핵심이다.

## 흔한 오개념

**"`cat`으로 여러 파일을 출력하면 파일들이 하나로 합쳐진다"는 오해**: `cat a.txt b.txt`를 실행해도 디스크 위의 `a.txt`와 `b.txt`는 전혀 바뀌지 않는다. `cat`은 두 파일의 내용을 순서대로 표준 출력 스트림에 흘려보낼 뿐이며, 그 결과를 실제 파일로 "합치려면" `cat a.txt b.txt > merged.txt`처럼 반드시 별도의 리다이렉션이 필요하다. `cat`이 하는 일은 언제나 스트림을 만드는 것이지 파일을 병합하는 것이 아니다.

**"`tail -f`가 멈춘 것처럼 보이면 명령이 실패한 것"이라는 오해**: `tail -f`는 파일에 새 줄이 추가될 때까지 화면에 아무것도 찍지 않고 <strong>계속 대기</strong>하는 것이 정상 동작이다. 아무 출력이 없다고 해서 명령이 멈추거나 실패한 게 아니라, 단지 그 사이 파일에 아무것도 쓰이지 않았을 뿐이다(Ctrl+C로 직접 종료하기 전까지는 끝나지 않는다). 반대로 로그가 계속 쌓이는데도 `tail -f`가 새 내용을 안 보여준다면, 그건 명령이 멈춘 게 아니라 앞서 다룬 로그 로테이션으로 옛 디스크립터를 붙들고 있는 상황일 가능성이 크다.

## 다음 장에서는

다음은 [4장: less, more](/post/bashshell/less-more-commands-view-large-files-linux/) — 대용량 파일은 `cat`으로 한 번에 쏟아내는 대신, 화면 단위로 멈춰 가며 검색까지 할 수 있는 페이저로 보는 법을 다룬다.

## 평가 기준

- `cat`의 정신 모델(입력을 가리지 않고 그대로 이어 붙여 흘려보낸다)을 설명하고, 여러 파일을 연결해 새 파일로 저장할 수 있다.
- `-n`/`-b`/`-s`와 `-A`/`-E`/`-T` 옵션의 차이를 구분하고, 로그·설정 파일 확인에 맞게 선택할 수 있다.
- UUOC(Useless Use of Cat) 패턴을 알아보고 `cat file | command`를 `command file`로 바꿀 수 있다.
- `cat file1 file2 > file1`처럼 자기 자신에게 리다이렉트할 때 발생하는 데이터 손실 위험을 설명할 수 있다.
- GNU `cat`과 BSD/macOS `cat`의 옵션 차이를 구분하고, 스크립트를 옮길 때 무엇을 점검해야 하는지 설명할 수 있다.
- `head`·`tail`의 정신 모델(파일 전체가 아니라 앞·뒤 일부만 스트리밍으로 읽는다)을 설명하고, `-n`/`-c`/`-n +K` 옵션으로 원하는 범위를 골라낼 수 있다.
- `tail -f`와 `-F`의 차이(디스크립터 추적 vs 이름 기반 재오픈)를 설명하고, 로그 로테이션 상황에서 어느 쪽을 써야 하는지 판단할 수 있다.

## 참고

- [cat(1) - Linux manual page (GNU coreutils)](https://man7.org/linux/man-pages/man1/cat.1.html)
- [cat - POSIX.1-2017 (The Open Group Base Specifications)](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/cat.html)
- [Useless Use of Cat Award](http://www.smallo.ruhr.de/award.html)
- [head(1) - Linux manual page (GNU coreutils)](https://man7.org/linux/man-pages/man1/head.1.html)
- [tail(1) - Linux manual page (GNU coreutils)](https://man7.org/linux/man-pages/man1/tail.1.html)
