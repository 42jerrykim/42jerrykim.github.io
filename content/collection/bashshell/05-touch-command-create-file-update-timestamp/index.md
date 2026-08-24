---
draft: false
slug: touch
title: "[Bash Shell] 05. touch - 파일 생성과 타임스탬프 갱신"
description: "touch의 본질은 파일 생성이 아니라 접근·수정 시각(atime/mtime) 갱신이며 빈 파일 생성은 부수 효과일 뿐이라는 점을 정신 모델부터 짚고, -a/-m 선택 갱신, -r/-d/-t 시각 지정, GNU·BSD/macOS의 -d/-t 날짜 형식 차이와 -h 심볼릭 링크 옵션까지 예제로 다룹니다."
date: 2026-03-15
lastmod: 2026-08-22
collection_order: 50
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
- Guide(가이드)
- Tutorial(튜토리얼)
- Reference(참고)
- Quick-Reference
- Troubleshooting(트러블슈팅)
- How-To
- Tips
- Beginner
- Best-Practices
- Pitfalls(함정)
- macOS
- Permission
- Configuration(설정)
- touch
- 타임스탬프
- mtime
- atime
- 빈파일
- timestamp
- GNU-Coreutils
- BSD
- POSIX
- 심볼릭링크
image: "wordcloud.png"
---

`touch`는 리눅스·유닉스 셸에서 파일의 <strong>접근 시각(atime)</strong>과 <strong>수정 시각(mtime)</strong>을 원하는 시점으로 바꾸는 명령이다. 대상 파일이 없으면 크기 0바이트짜리 빈 파일을 만드는 것으로 흔히 알려져 있지만, 이는 시각을 기록할 자리를 마련하기 위한 부수 효과일 뿐 touch의 본래 목적이 아니다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [04장: less, more](/post/bashshell/less-more/)에서 페이저로 파일 내용을 화면 단위로 넘겨 보는 법을 다룬 뒤 이어진다. 1–4장은 셸을 오가고(`cd`, `pwd`) 디렉터리 내용을 나열하고(`ls`) 파일을 화면에 출력하거나(`cat`) 페이지 단위로 읽는(`less`, `more`) 등, 이미 존재하는 파일을 "보는" 작업이었다. 이 장부터는 파일을 직접 만들고 그 메타데이터를 조작하는 "쓰기" 방향으로 처음 전환하는 지점이다.

난이도는 **입문**이다. 셸에서 파일 경로를 지정할 수 있다는 것 정도만 전제한다. **다루지 않는 것**: 파일을 실제로 복사·이동·삭제하는 작업은 [7장: cp, mv, rm](/post/bashshell/cp-mv-rm/)에서, 디렉터리를 만들고 지우는 작업은 [06장: mkdir, rmdir](/post/bashshell/mkdir-rmdir/)에서 다룬다. touch가 다루는 시각 메타데이터가 `ls -l`에 어떻게 표시되는지는 이미 [2장: ls](/post/bashshell/ls/)에서 다뤘으므로 여기서는 반복하지 않는다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| 스크립트에서 빈 파일·최신 타임스탬프가 급한 사람 | 개요+정신 모델, 사용법·옵션, 예시의 "빈 파일 생성"–"수정 시각만 갱신" | 상황에 맞는 touch 명령을 바로 조합해 쓴다 |
| 타임스탬프 조작을 제대로 이해하려는 사람 | 예시 전체, 주의사항·함정, 흔한 오개념 | GNU/BSD 날짜 형식 차이와 심볼릭 링크 시각 처리까지 이해하고 이식성 있는 스크립트를 작성한다 |

## 개요 + 정신 모델

POSIX는 touch의 목적을 이렇게 정의한다.

> "The touch utility shall change the last data modification timestamps, the last data access timestamps, or both." — POSIX.1-2017, `touch`

즉 touch가 세상을 보는 방식은 "파일을 만드는 도구"가 아니라 "파일의 시각 메타데이터, 즉 inode에 저장된 접근 시각(atime)과 수정 시각(mtime)을 지금 또는 지정한 시각으로 갱신하는 도구"다. 대상 파일이 이미 있으면 touch는 내용을 전혀 건드리지 않고 시각 필드만 바꾼다. 대상 파일이 없을 때 touch가 빈 파일을 만드는 것은 목적이 아니라 부수 효과에 가깝다 — POSIX 명세는 파일이 없을 때의 동작을 별도 항목으로 규정한다.

> "If file does not exist: The creat() function is called with the following arguments: The file operand is used as the path argument." — POSIX.1-2017, `touch`

GNU coreutils 매뉴얼도 같은 동작을 이렇게 서술한다.

> "Any file argument that does not exist is created empty, unless option --no-create (-c) or --no-dereference (-h) was in effect." — GNU Coreutils Manual, "touch invocation"

시각을 기록할 inode 자체가 없으면 갱신할 대상이 없으므로, touch는 먼저 `creat()` 계열 시스템 호출로 크기 0바이트짜리 파일을 만들어 inode를 확보한 뒤 그 inode의 시각 필드를 채운다. 이 정신 모델을 갖고 있으면 `-c`(`--no-create`) 옵션이 왜 존재하는지, 그리고 `make` 같은 빌드 시스템이 touch를 "파일이 이미 있을 때만 시각을 최신으로 만들고 새로 만들지는 않는" 용도로 자주 쓰는 이유가 자연스럽게 설명된다. 반대로 "touch=빈 파일 생성"으로만 외우면, 이미 존재하는 로그 파일에 touch를 실행했다가 내용은 그대로인데 수정 시각만 바뀌어 다른 스크립트의 캐시 무효화 로직이 엉뚱하게 발동하는 상황을 이해하기 어렵다.

## 사용법·옵션

```bash
touch [옵션] 파일...
```

- **파일**: 시각을 갱신(또는 새로 생성)할 대상. 여러 개를 한 번에 지정할 수 있다.

### 시각 선택

| 옵션 | 설명 |
|---|---|
| `-a` | 접근 시각(atime)만 변경 |
| `-m` | 수정 시각(mtime)만 변경 |
| (기본, 옵션 없음) | atime·mtime 둘 다 현재 시각으로 변경 |

### 시각 지정

| 옵션 | 설명 |
|---|---|
| `-r FILE`, `--reference=FILE` | FILE의 시각을 그대로 참조해 사용 |
| `-d STRING`, `--date=STRING` | STRING이 나타내는 시각으로 지정(GNU: 월 이름·시간대·`yesterday` 등 자유 형식 허용) |
| `-t STAMP` | `[[CC]YY]MMDDhhmm[.SS]` 고정 형식으로 시각 지정 |

### 생성 동작 제어

| 옵션 | 설명 |
|---|---|
| `-c`, `--no-create` | 파일이 없으면 만들지 않고 경고 없이 건너뜀 |
| `-h`, `--no-dereference` | 대상이 심볼릭 링크면 링크가 가리키는 파일이 아니라 **링크 자체**의 시각을 변경 |

## 예시

### 빈 파일 생성

```bash
# 파일이 없으면 새로 만들고, 있으면 atime·mtime만 현재 시각으로 갱신
touch newfile.txt

# 여러 파일을 한 번에
touch a.txt b.txt c.txt
```

### 접근 시각만/수정 시각만 갱신 (-a/-m)

```bash
# 접근 시각만 현재 시각으로 (파일 내용·수정 시각은 그대로)
touch -a cache/session.dat

# 수정 시각만 갱신 (make가 "이 파일은 방금 바뀌었다"고 인식하게 만들 때 자주 사용)
touch -m build/output.o
```

### 특정 시각으로 설정 (-d, -t)

```bash
# GNU: 자유 형식 날짜 문자열
touch -d "2026-01-15 09:30:00" report.csv
touch -d "3 days ago" old-marker.txt

# 두 진영 모두 지원하는 고정 형식([[CC]YY]MMDDhhmm[.SS])
touch -t 202601150930 report.csv
```

### 다른 파일과 같은 시각으로 맞추기 (-r)

```bash
# source.txt와 정확히 같은 atime·mtime으로 맞춤 (배포 시 파일 시각을 원본과 동일하게 유지할 때 유용)
touch -r source.txt target.txt

# 참조 시각을 기준으로 5초 전 시각 지정 (-r과 -d를 조합, 참조 파일이 원점이 된다)
touch -r source.txt -d '-5 seconds' target.txt
```

### 파일이 있을 때만 갱신 (-c)

```bash
# 파일이 없으면 생성하지 않고 조용히 넘어감 (배치 스크립트에서 없는 파일을 실수로 만들지 않도록)
touch -c maybe-missing.log
```

### 심볼릭 링크 자체의 시각 변경 (-h)

```bash
# config는 real.conf를 가리키는 심볼릭 링크라고 가정
ln -s real.conf config

# -h 없이 실행하면 링크가 아니라 real.conf의 시각이 바뀐다
touch config

# 링크 자체의 시각만 변경(real.conf는 건드리지 않음)
touch -h config
```

## 주의사항·함정

**GNU와 BSD/macOS의 `-d`/`-t` 날짜 형식은 서로 다르다**: `-t` 형식은 두 진영이 동일하다. GNU coreutils 매뉴얼은 `-t[[cc]yy]mmddhhmm[.ss]`로, FreeBSD(및 이를 그대로 물려받은 macOS 기본 touch)의 매뉴얼은 `-t [[CC]YY]MMDDhhmm[.SS]`로 표기해 표기 대소문자만 다를 뿐 실제 형식은 같다. 문제는 `-d`다. GNU coreutils 매뉴얼은 `-d`가 받는 값을 다음과 같이 설명한다.

> "Use time instead of the current time. It can contain month names, time zones, 'am' and 'pm', 'yesterday', etc." — GNU Coreutils Manual, "touch invocation"

즉 GNU touch의 `-d`는 GNU date 문자열 파서를 그대로 재사용해 `"2026-01-15 09:30:00"`, `"yesterday"`, `"3 days ago"`처럼 사람이 쓰는 표현에 가까운 자유 형식을 받는다. 반면 FreeBSD의 touch(1) 매뉴얼은 `-d`의 형식을 이렇게 못박는다.

> "Change the access and modification times to the specified date time instead of the current time of day. The argument is of the form \"YYYY-MM-DDThh:mm:SS[.frac][tz]\"" — FreeBSD General Commands Manual, `touch(1)`

FreeBSD/macOS의 `-d`는 `T`로 날짜와 시각을 구분하는 ISO 8601 스타일 한 가지 형식만 받는다. 이 형식을 벗어난 `"yesterday"`, `"3 days ago"` 같은 GNU 스타일 자유 형식 문자열을 macOS 기본 touch에 그대로 넘기면, 파서가 인식하지 못하는 인자로 처리되어 에러가 난다. 반대로 `"2026-01-15T09:30:00"`처럼 `T` 구분자를 쓴 ISO 8601 문자열은 GNU touch의 자유 형식 파서도 그대로 인식하므로 문제가 없다. 결론적으로, 여러 플랫폼에서 동일하게 동작해야 하는 스크립트는 `-d`의 자유 형식에 기대지 말고 두 진영 모두가 지원하는 `-t [[CC]YY]MMDDhhmm[.SS]` 고정 형식을 쓰는 편이 안전하다.

**`-h`는 심볼릭 링크의 시각을 바꿀 수 있는 시스템에서만 동작한다**: GNU coreutils 매뉴얼은 `-h`에 대해 다음과 같이 덧붙인다.

> "Not all systems support changing the timestamps of symlinks, since underlying system support for this action was not required until POSIX 2008." — GNU Coreutils Manual, "touch invocation"

심볼릭 링크 자체의 타임스탬프 변경은 POSIX 2008에서야 요구 사항이 됐을 만큼 비교적 늦게 표준화된 기능이다. 또한 `-h` 없이 심볼릭 링크를 대상으로 touch를 실행하면 링크를 따라가 실제 파일의 시각이 바뀐다는 점도 함께 기억해야 한다 — 링크 자체를 건드릴 의도였다면 반드시 `-h`를 명시해야 한다.

**의도치 않은 캐시 무효화**: touch는 파일 내용을 바꾸지 않지만 mtime을 바꾸는 것만으로도 `make`, `rsync`의 증분 백업, 정적 사이트 생성기의 증분 빌드처럼 mtime을 "변경 여부"의 신호로 쓰는 도구들을 속인다. 디버깅 목적으로 무심코 `touch *`를 실행하면 프로젝트 전체가 "방금 전부 수정됨"으로 인식되어 불필요한 전체 재빌드가 시작될 수 있다.

## 흔한 오개념

<strong>"touch의 핵심 기능은 빈 파일 생성이다"</strong>는 가장 흔한 오해다. 정신 모델에서 설명했듯 touch의 1차 목적은 시각 갱신이고, 빈 파일 생성은 시각을 기록할 대상이 없을 때 발생하는 부수 효과다. 이미 존재하는 파일에 touch를 실행하는 것이 오히려 더 흔한 실사용 패턴이다(락 파일 갱신, 빌드 의존성 갱신, `make` 타깃 최신화 등).

<strong>"touch로 만든 파일은 다른 방법으로 만든 빈 파일과 다르게 취급된다"</strong>는 오해도 있다. touch가 만든 파일은 `> file`이나 다른 방법으로 만든 빈 파일과 완전히 동일한 0바이트 일반 파일이다. touch는 파일을 만드는 특별한 형식을 쓰지 않고 다른 도구와 마찬가지로 `creat()` 계열 시스템 호출을 거칠 뿐이라, 파일 자체에는 "touch로 만들어졌다"는 흔적이 전혀 남지 않는다.

## 다음 장에서는

다음은 [06장: mkdir, rmdir](/post/bashshell/mkdir-rmdir/) — 파일이 아니라 디렉터리를 만들고 지우는 명령으로 넘어간다. 이 장이 "이미 존재하거나 방금 만든 파일의 시각을 다루는 법"이었다면, 다음 장은 "파일들을 담을 디렉터리 자체를 만들고 없애는 법"이다.

## 평가 기준

- touch의 핵심 목적이 시각(atime/mtime) 갱신이며 빈 파일 생성은 부수 효과라는 것을 설명할 수 있다.
- `-a`/`-m`으로 접근·수정 시각을 선택적으로 갱신할 수 있다.
- `-r`로 다른 파일과 같은 시각을 맞추고, `-d`/`-t`로 임의의 시각을 지정할 수 있다.
- GNU touch의 `-d`(자유 형식)와 BSD/macOS touch의 `-d`(ISO 8601 고정 형식)의 차이를 설명하고, 두 진영에서 모두 동작하는 이식성 있는 형식(`-t`)을 선택할 수 있다.
- `-h`로 심볼릭 링크 자체의 시각과 링크가 가리키는 파일의 시각을 구분해 변경할 수 있다.

## 참고

- [POSIX.1-2017: touch](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/touch.html)
- [GNU Coreutils Manual: touch invocation](https://www.gnu.org/software/coreutils/manual/html_node/touch-invocation.html)
- [FreeBSD General Commands Manual: touch(1)](https://man.freebsd.org/cgi/man.cgi?query=touch&sektion=1)
