---
draft: false
slug: tar-command-archive-files-linux
title: "[Bash Shell] 39. tar - 아카이브 묶기"
description: "여러 파일과 디렉터리를 하나의 아카이브 스트림으로 묶는 tar의 정신 모델과 -c·-x·-t·-z·-j·-J 옵션, gzip과의 파이프 결합을 예제로 다루고, GNU tar와 BSD/macOS tar(bsdtar)의 옵션 차이·경로 트래버설 방어 기본값을 1차 문서로 검증해 정리합니다."
date: 2026-03-15
lastmod: 2026-08-24
collection_order: 390
categories:
- Bash Shell
tags:
- Bash
- Shell(셸)
- Linux(리눅스)
- Terminal
- Command
- File-System
- Process
- Automation(자동화)
- Backup
- Compression
- System-Administration(시스템관리)
- Security(보안)
- Guide(가이드)
- Tutorial(튜토리얼)
- Reference(참고)
- Quick-Reference
- Troubleshooting(트러블슈팅)
- How-To
- Tips
- Beginner
- Comparison(비교)
- Deep-Dive
- Best-Practices
- Workflow(워크플로우)
- tar
- gzip
- 아카이브
- archive
- 압축
- Path-Traversal
- GNU-Tar
- BSD-Tar
image: "wordcloud.png"
---

`tar`(tape archive)는 **여러 파일과 디렉터리 구조를 하나의 아카이브 스트림으로 묶는** 명령어다. 압축 자체는 tar의 원래 역할이 아니었고, `-z`/`-j`/`-J` 옵션으로 gzip·bzip2·xz와 결합해야 비로소 `.tar.gz`처럼 실제로 크기가 줄어든 압축 아카이브가 만들어진다.

## 이 장을 읽기 전에

**선행 챕터**: 직전 [38장: gzip](/post/bashshell/gzip-command-compress-decompress-files/)에서는 `gzip`이 파일 하나를 압축하는 도구라는 것을 다뤘다. gzip이 파일 하나만 압축했다면, `tar`는 여러 파일·디렉터리를 하나로 묶고 gzip과 결합해 진짜 압축 아카이브를 만든다 — 이번 장은 그 결합의 뒷단, 즉 "묶기" 자체를 다룬다. [36장: chmod, chown](/post/bashshell/chmod-chown-commands-file-permissions-ownership/)에서 다룬 권한 개념도 압축 해제 후 파일 권한이 그대로 복원된다는 점에서 다시 등장한다.

**이 장의 깊이**: **입문–중급** 난이도다. 기본 아카이브 생성·해제부터 압축 필터 결합, GNU/BSD 이식성, 경로 트래버설 방어까지 실무에서 자주 마주치는 범위를 다룬다. **다루지 않는 것**: `tar` 아카이브의 내부 바이너리 포맷(ustar/pax/gnu 헤더 구조의 바이트 단위 명세)과 테이프 드라이브를 직접 다루는 멀티볼륨 아카이브는 범위 밖이다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| 백업·배포 파일을 급히 묶어야 하는 사람 | "개요 + 정신 모델", "사용법·옵션"의 기본 표, "예시"의 "기본 아카이브"·"압축 아카이브" | `tar -czvf`/`tar -xzvf` 조합으로 디렉터리를 압축·해제할 수 있다 |
| 스크립트를 여러 OS에 배포하거나 신뢰할 수 없는 아카이브를 다루는 사람 | "주의사항·함정" 전체, "흔한 오개념" | GNU tar와 BSD tar의 옵션 차이, 경로 트래버설 방어 기본값을 이해하고 안전하게 스크립트를 작성할 수 있다 |

## 개요 + 정신 모델

`tar`라는 이름 자체가 "tape archive"의 줄임말이다. 1979년 Seventh Edition Unix에 처음 등장했을 당시 이 명령어의 유일한 임무는 여러 파일과 디렉터리 트리를 순서대로 읽어 하나의 연속된 바이트 스트림(원래는 자기 테이프에 기록하는 스트림)으로 직렬화하는 것이었다. 각 파일은 이름·소유자·권한·크기 같은 메타데이터를 담은 헤더 블록 뒤에 데이터가 이어지는 형태로 512바이트 블록 단위에 맞춰 순차적으로 기록된다. 이 순차 스트림 구조는 zip처럼 파일 끝부분에 중앙 디렉터리(central directory)를 두고 임의 위치를 바로 찾아가는 랜덤 액세스 포맷과 근본적으로 다르다 — tar는 스트림을 처음부터 순서대로 읽어야 각 멤버를 찾을 수 있고, 그래서 `tar -tf`로 목록만 보려 해도 아카이브 전체(또는 앞부분)를 훑어야 한다.

중요한 점은 압축이 이 스트림 형식에 원래 없던 기능이라는 것이다. 초기 tar는 압축을 전혀 몰랐고, 사용자는 `tar cf - dir | compress > archive.tar.Z`처럼 tar의 출력을 별도 압축 명령에 파이프로 연결해야 했다. 오늘날의 `-z`(gzip), `-j`(bzip2), `-J`(xz) 옵션은 이 파이프 연결을 tar 내부로 편입시킨 **단축 문법**일 뿐이다 — `tar -czvf archive.tar.gz dir/`는 개념적으로 `tar -cvf - dir/ | gzip > archive.tar.gz`와 동일한 일을 한다. 따라서 tar와 gzip의 역할 분담은 "tar=묶기, gzip/bzip2/xz=압축"으로 명확히 나뉘고, `-z`/`-j`/`-J`는 그 둘을 한 번의 명령으로 잇는 접착제에 불과하다.

## 사용법 · 옵션

기본 문법은 `tar [옵션] [아카이브] [파일...]`이다. 옵션은 크게 "무엇을 할지(모드)", "압축 필터를 걸지", "그 외 동작을 어떻게 조정할지"로 나뉜다.

### 모드 옵션 (반드시 하나 지정)

| 옵션 | 설명 |
|------|------|
| `-c`, `--create` | 새 아카이브 생성 |
| `-x`, `--extract` | 아카이브에서 파일 추출 |
| `-t`, `--list` | 아카이브 내용을 목록만 출력(추출하지 않음) |
| `-r`, `--append` | 기존 아카이브 끝에 항목 추가(압축되지 않은, 시크 가능한 일반 파일 아카이브에서만 동작) |
| `-u`, `--update` | 아카이브의 항목보다 수정일이 최신인 파일만 추가(`-r`과 같은 제약) |
| `--delete` | 아카이브에서 특정 멤버 제거(**GNU tar 전용**, 자기 테이프에서는 동작하지 않음) |

### 압축 필터 옵션

| 옵션 | 설명 |
|------|------|
| `-z`, `--gzip` | gzip으로 압축/해제(`.tar.gz`, `.tgz`) |
| `-j`, `--bzip2` | bzip2로 압축/해제(`.tar.bz2`) |
| `-J`, `--xz` | xz로 압축/해제(`.tar.xz`) |
| `-a`, `--auto-compress` | 파일 확장자를 보고 압축 방식을 자동 선택(생성 시) |

추출(`-x`)·목록(`-t`) 모드에서는 GNU tar와 BSD tar 모두 압축 형식을 매직 바이트로 자동 인식하므로, 압축 아카이브라도 `-z`/`-j`/`-J`를 생략하고 `tar -xf archive.tar.gz`만 써도 대개 문제없이 풀린다. 다만 **생성 시에는 압축 방식을 명시(`-z`/`-j`/`-J`/`-a`)해야 한다** — tar는 만들 때 어떤 압축기를 쓸지 스스로 추측하지 않는다.

### 파일·경로 지정

| 옵션 | 설명 |
|------|------|
| `-f FILE`, `--file FILE` | 아카이브 파일 지정(사실상 필수, `-`는 표준입출력) |
| `-C DIR`, `--directory DIR` | 지정한 디렉터리로 먼저 이동한 뒤 처리(순서에 영향을 받음) |
| `--strip-components N` | 추출 시 경로 앞부분 N단계를 제거 |
| `-v`, `--verbose` | 처리한 파일 이름을 출력 |
| `-p`, `--preserve-permissions` | 원본 권한을 그대로 복원(GNU tar에서 root 실행 시 기본값) |
| `-k`, `--keep-old-files` | 추출 시 기존 파일을 덮어쓰지 않음 |
| `-P`, `--absolute-names`(GNU) / `--absolute-paths`(BSD) | 절대경로·`..` 경로 관련 보안 검사를 끔(뒤의 주의사항 참고) |

## 예시

### 기본 아카이브 (압축 없음)

```bash
# 디렉터리를 압축 없이 아카이브로 묶기
tar -cvf backup.tar dir/

# 추출 전 내용만 확인 (신뢰할 수 없는 아카이브는 반드시 먼저 이렇게 확인한다)
tar -tvf backup.tar

# 묶은 그대로 풀기
tar -xvf backup.tar
```

### 압축 아카이브 (tar + gzip/bzip2/xz)

```bash
# gzip으로 압축한 아카이브 생성 — 개념적으로 tar -cvf - dir/ | gzip > backup.tar.gz와 동일
tar -czvf backup.tar.gz dir/

# xz는 gzip보다 느리지만 대체로 더 작은 결과를 만든다
tar -cJvf backup.tar.xz dir/

# 확장자 자동 인식으로 압축 방식 선택
tar -acvf backup.tar.bz2 dir/
```

### 해제와 대상 디렉터리 지정

```bash
# 압축 형식을 자동 인식하므로 -z 없이도 풀린다
tar -xvf backup.tar.gz -C /target/

# 특정 경로만 추출
tar -xzvf backup.tar.gz path/to/file

# 아카이브 안 최상위 디렉터리 한 단계를 벗겨내고 풀기
tar -xzvf backup.tar.gz --strip-components=1
```

### 파이프 조합과 원격 전송

```bash
# tar를 표준출력으로 흘려보내 SSH로 원격 서버에 바로 풀기 (39장 다음의 curl-wget/scp/ssh 챕터에서 원격 전송을 더 다룬다)
tar -cvf - dir/ | ssh user@remote "tar -xvf - -C /path/to/dest"

# 압축·해제 없이 디렉터리 트리를 그대로 다른 위치로 복제
tar -cf - -C srcdir . | tar -xf - -C destdir
```

## 주의사항 · 함정

**GNU tar와 BSD/macOS tar(bsdtar)는 겉모습이 비슷해도 옵션 체계가 상당히 다르다.** macOS는 Mac OS X 10.6(2009년)부터 기본 `/usr/bin/tar`를 GNU tar가 아니라 libarchive 기반 `bsdtar`로 바꿨다(`bsdtar`의 `--mac-metadata`, `--hfsCompression` 같은 "Mac OS X specific" 옵션이 이를 뒷받침한다). man7.org의 GNU tar(1) 매뉴얼에 따르면 `--catenate`/`--concatenate`, `--compare`/`--diff`, `--delete`, `--test-label`, `--show-defaults`, `--occurrence`, `--restrict`, `--check-device` 같은 다수의 **GNU 전용 장옵션**이 존재하는데, 이 중 `--delete`는 FreeBSD `tar(1)`(bsdtar) 매뉴얼의 옵션 목록에 아예 없다 — bsdtar에는 아카이브에서 멤버를 지우는 기능 자체가 없다. 짧은 옵션 하나가 우연히 같아 보여도 장옵션 이름이 다른 경우도 있다: 절대경로 보호를 끄는 옵션은 GNU tar에서 `-P`/`--absolute-names`지만 bsdtar에서는 같은 `-P`가 `--absolute-paths`다. 스크립트를 여러 플랫폼에 배포한다면 짧은 옵션(`-czf`, `-xzf` 등)과 `-C`/`-f`/`-v` 정도로 좁혀 쓰는 편이 안전하다 — bsdtar 매뉴얼도 "최대 이식성을 위해서는 bundled-argument 형식을 쓰고 c/t/x 모드와 b/f/m/v/w 옵션만 쓰라"고 명시한다.

**신뢰할 수 없는 아카이브를 풀 때 경로 트래버설 위험이 있다.** 아카이브 멤버 이름에 절대경로(`/etc/passwd`)나 상위 디렉터리(`../../etc/passwd`)가 들어 있으면, 순진하게 풀 경우 대상 디렉터리 바깥으로 파일을 덮어쓸 수 있다. 다행히 현재 두 구현 모두 기본값으로 이를 방어한다. <strong>GNU tar 매뉴얼(§6.10.2 "Absolute File Names")</strong>은 "By default, GNU tar drops a leading '/' on input or output, and complains about file names containing a '..' component... tar normally warns you about such files when creating an archive, and rejects attempts to extracts such files"라고 명시한다 — 즉 추출 시 선행 슬래시를 제거해 절대경로를 상대경로처럼 다루고, `..` 컴포넌트가 있는 멤버는 경고와 함께 추출을 거부한다. **FreeBSD `tar(1)`(bsdtar) 매뉴얼의 SECURITY 섹션**도 사실상 동일한 3단계 방어를 명시한다 — 선행 `/` 제거, `..` 컴포넌트 포함 항목 추출 거부, 그리고 추출 경로의 마지막 요소가 심볼릭 링크면 제거 후 아카이브 항목으로 대체(중간 심볼릭 링크는 `-U` 없이는 손대지 않고 추출을 거부). 두 구현 모두 `-P`(GNU: `--absolute-names`, BSD: `--absolute-paths`)를 주면 이 방어를 전부 끄므로, 출처가 불확실한 아카이브에는 `-P`를 쓰지 않아야 하고, 애초에 `tar -tf`로 멤버 목록부터 확인한 후 추출하는 습관이 안전하다. root 권한으로 신뢰할 수 없는 아카이브를 푸는 것은 두 매뉴얼 모두 피하라고 권고한다.

**옵션 앞 대시를 생략하는 구식 스타일은 여전히 동작하지만, 표준 스타일과는 다른 파싱 경로를 탄다.** `tar xvf file.tar`처럼 대시 없이 옵션 문자를 붙여 쓰는 방식은 GNU tar와 bsdtar 모두 지원한다 — bsdtar 매뉴얼은 이를 "bundled-arguments format... supported for compatibility with historic implementations"라고 설명한다. 1979년 Seventh Edition Unix의 tar는 오늘날 표준이 된 `getopt` 스타일 대시 옵션 관례가 자리 잡기 전에 나온 명령어라, 원래부터 옵션 문자를 붙여 쓰는 형태만 있었다. bundled 형식에서는 옵션 문자 각각에 대응하는 인자가 **명령줄에 나열된 순서와 정확히 일치**해야 한다는 제약이 있고(예: `tar tbf 32 file.tar`에서 32는 `b`의 인자, `file.tar`는 `f`의 인자), 장옵션(`--verbose` 등)은 이 형식으로 쓸 수 없다. 표준 대시 옵션(`-xvf file.tar`)은 이 순서 제약이 없고 장옵션과도 자유롭게 섞을 수 있어 스크립트에서는 이쪽이 더 안전하다 — `tar xvf`가 계속 동작하는 것은 우연이 아니라 하위 호환을 위해 의도적으로 남겨둔 별도 파싱 경로이기 때문이다.

## 흔한 오개념

**"tar로 묶으면 파일 크기가 줄어든다"는 착각이 흔하다.** `tar` 자체는 압축을 하지 않는 번들링 도구이므로, `-z`/`-j`/`-J` 없이 만든 `.tar` 파일은 원본 파일들의 크기 합에 헤더 블록 오버헤드(512바이트 단위 정렬)까지 더해져 오히려 원본보다 약간 커진다. 크기를 줄이려면 반드시 압축 필터 옵션을 함께 써야 한다.

**"압축 해제할 때도 `-z`/`-j`/`-J`를 정확히 맞춰야 한다"는 것도 절반만 맞는 말이다.** 생성 시에는 압축 방식을 tar가 추측하지 않으므로 반드시 명시해야 하지만, 추출·목록 모드에서는 GNU tar와 bsdtar 모두 파일의 매직 바이트를 읽어 gzip/bzip2/xz 여부를 자동 인식한다 — bsdtar 매뉴얼도 `-z` 옵션 설명에 "this tar implementation recognizes gzip compression automatically when reading archives"라고 명시한다. 그래서 확장자만 보고 `tar -xf backup.tar.gz`라고만 써도 대개 문제없이 풀리고, `-z`를 빠뜨렸다고 에러가 나는 경우는 드물다. 이 비대칭성(생성 시엔 필요, 추출 시엔 대개 불필요)을 모르면 "왜 압축 해제는 옵션 없이도 되는데 압축은 안 되지"라는 혼란을 겪기 쉽다.

## 다음 장에서는

다음은 [40장: du, df](/post/bashshell/du-df-commands-disk-usage-linux/) — 아카이브·압축으로 파일을 다뤘다면, 이제 그 파일들이 디스크 공간을 실제로 얼마나 차지하고 있는지 확인하는 도구로 넘어간다.

## 평가 기준

- tar와 gzip/bzip2/xz의 역할 분담(번들링 vs 압축)을 설명하고, `-z`/`-j`/`-J`가 왜 "파이프의 단축 문법"인지 설명할 수 있다.
- `-c`/`-x`/`-t`/`-f`/`-C`/`--strip-components` 옵션을 조합해 아카이브를 생성·목록 확인·해제할 수 있다.
- GNU tar와 BSD/macOS tar(bsdtar)의 옵션 차이(GNU 전용 장옵션, `-P`의 서로 다른 장옵션 이름)를 구분하고 이식성 있는 스크립트를 어떻게 좁혀 써야 하는지 설명할 수 있다.
- tar의 경로 트래버설 방어 기본값(선행 슬래시 제거, `..` 컴포넌트 거부)을 설명하고, 신뢰할 수 없는 아카이브를 다루기 전에 왜 `tar -tf`로 먼저 확인해야 하는지 말할 수 있다.
- 구식 bundled 옵션 스타일(`tar xvf file.tar`)과 표준 대시 옵션 스타일(`-xvf`)의 관계와 각각의 제약을 설명할 수 있다.

## 참고

- [GNU tar 매뉴얼 6.10.2 Absolute File Names](https://web.archive.org/web/20260217122214/https://www.gnu.org/software/tar/manual/html_node/absolute.html) — gnu.org 원본 접근이 간헐적으로 막혀 archive.org 스냅샷(2026-02-17)으로 링크
- [GNU tar 매뉴얼 4.2.5 --delete](https://web.archive.org/web/20250926112541/https://www.gnu.org/software/tar/manual/html_node/delete.html)
- [tar(1) - Linux manual page (man7.org)](https://man7.org/linux/man-pages/man1/tar.1.html)
- [tar(1) - FreeBSD General Commands Manual (libarchive/bsdtar)](https://man.freebsd.org/cgi/man.cgi?query=tar&sektion=1)
