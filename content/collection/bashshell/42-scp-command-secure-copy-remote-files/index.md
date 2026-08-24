---
draft: false
slug: scp-command-secure-copy-remote-files
title: "[Bash Shell] 42. scp - 원격 파일 복사"
description: "SSH 프로토콜 위에서 로컬↔원격 간 파일·디렉터리를 복사하는 scp의 사용법과 -r·-P·-3 옵션, 원격-원격 복사 문법을 정리하고 OpenSSH 9.0이 기본 전송 방식을 SFTP로 바꾼 배경과 -O 옵션까지 다룹니다."
date: 2026-03-15
lastmod: 2026-08-24
collection_order: 420
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
- SSH(Secure Shell)
- Networking(네트워킹)
- Security(보안)
- Encryption(암호화)
- Protocol(프로토콜)
- System-Administration(시스템관리)
- Backup
- scp
- SFTP
- rsync
- OpenSSH
- 원격복사
- 파일전송
- CVE-2019-6111
- 재귀복사
- remote-to-remote
- 이식성
- Command-Line-Tool
- 원격접속
image: "wordcloud.png"
---

`scp`(secure copy)는 **SSH**가 맺은 암호화 채널 위에서 로컬↔원격, 또는 원격↔원격 간에 파일·디렉터리를 복사하는 명령어다. 문법은 `cp`와 거의 대칭적이라 로컬 복사에 익숙하다면 새로 배울 개념이 많지 않지만, 내부적으로 쓰는 전송 프로토콜은 OpenSSH 역사에서 실제로 한 번 크게 바뀌었다 — 이 장의 "주의사항·함정"에서 그 배경을 다룬다.

## 이 장을 읽기 전에

직전 챕터인 [41장: curl, wget](/post/bashshell/curl-wget-commands-download-http-files/)에서는 **HTTP** 프로토콜로 원격 서버의 파일을 내려받는 법을 다뤘다. curl·wget이 HTTP 기반 다운로드였다면, 이 장의 `scp`는 **SSH 프로토콜 위에서 동작하는 원격 파일 복사**다 — 인증 방식도, 데이터를 감싸는 암호화 채널도 HTTP와는 완전히 다른 메커니즘을 쓴다. Part 7(네트워크와 원격 접속)의 두 번째 챕터로, [7장: cp, mv, rm](/post/bashshell/cp-mv-rm-commands-copy-move-delete-files/)에서 다룬 로컬 파일 복사 명령과 기본적인 셸 사용법(리다이렉션·파이프 등)을 이미 안다는 전제로 진행한다.

**이 장의 깊이**: 입문–중급이다. `cp`를 다룰 줄 아는 사람이 그 경험을 원격 환경으로 확장하는 수준이며, 별도의 고급 네트워크 지식은 요구하지 않는다. **다루지 않는 것**: SSH 키 쌍 생성·`~/.ssh/config` 설정·포트 포워딩·SSH 자체의 인증 흐름은 다음 장인 [43장: ssh](/post/bashshell/ssh-command-remote-login-secure-shell/)에서 본격적으로 다룬다. 이 장은 `scp` 명령어의 사용법과 함정에 집중한다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| 로컬↔원격 복사가 급한 사람 | "개요 + 정신 모델", "사용법·옵션", "예시"의 기본 복사·재귀 복사 | `scp`로 파일 하나 또는 디렉터리 전체를 로컬과 원격 사이에 옮길 수 있다 |
| 원격 서버 관리·자동화를 하는 사람 | "예시"의 원격-원격 복사·압축·대역폭 제한, "주의사항·함정" 전체 | 두 원격 호스트 간 복사를 설계하고, SFTP 전환에 따른 호환성 문제를 진단·회피할 수 있다 |

## 개요 + 정신 모델

`scp`는 사실상 **`cp`의 원격 버전**이다. `cp [옵션] 소스 대상`이라는 로컬 복사 문법에서, 소스나 대상(혹은 둘 다) 자리에 `[사용자@]호스트:경로` 형태를 그대로 끼워 넣을 수 있게 확장한 것이 `scp`의 전체 그림이다. `cp`가 하나의 파일시스템 트리 안에서 소스 → 대상으로 바이트를 옮기는 도구라면, `scp`는 그 트리 중 하나(또는 둘 다)가 네트워크 너머의 원격 호스트에 있을 수 있다는 점만 다르다.

이 확장에서 인증과 암호화를 `scp`가 처음부터 새로 설계하지 않았다는 점이 중요하다. `scp`는 **SSH 프로토콜의 메커니즘을 그대로 재사용**한다 — 명령을 실행하면 내부적으로 SSH 연결을 맺고, 그 연결이 제공하는 암호화 채널 위에 파일 데이터를 실어 나른다. 그래서 `scp`의 옵션 상당수(`-i` 키 파일, `-P` 포트)가 `ssh` 옵션과 이름·역할이 거의 그대로 대응하고, `~/.ssh/config`에 등록해 둔 `Host` 별칭도 `scp`가 그대로 활용한다. SSH 자체의 키 인증 절차와 설정 파일은 다음 장에서 본격적으로 다룬다.

이 정신 모델에서 한 가지 더 구분해야 할 것이 있다. `scp`라는 **명령어의 이름과 사용법**(문법, 옵션 구성)은 OpenSSH 역사 내내 안정적으로 유지돼 왔지만, 그 명령어가 파일을 실제로 실어 나르는 데 쓰는 **내부 전송 프로토콜**은 도중에 교체됐다. 겉보기 명령은 그대로인데 속 배관이 바뀐 셈이며, 이 차이가 실무에서 실제로 호환성 문제를 일으킨다 — 자세한 내용은 아래 "주의사항·함정"에서 다룬다.

## 사용법 · 옵션

기본 문법은 소스와 대상 중 어느 쪽이 원격인지에 따라 세 가지 형태로 쓴다.

```bash
# 원격 → 로컬
scp [옵션] [사용자@]호스트:원격경로 로컬경로

# 로컬 → 원격
scp [옵션] 로컬경로 [사용자@]호스트:원격경로

# 원격 → 원격 (호스트 간 직접, 또는 로컬을 경유)
scp [옵션] [사용자@]호스트1:경로1 [사용자@]호스트2:경로2
```

### 연결·인증

| 옵션 | 설명 |
|---|---|
| `-i FILE` | 인증에 사용할 개인키 파일을 지정한다 |
| `-P PORT` | 접속할 포트를 지정한다(`ssh`는 소문자 `-p`, `scp`는 대문자 `-P`라는 점에 주의) |
| `-4`, `-6` | IPv4 또는 IPv6 주소만 사용하도록 강제한다 |

### 복사 방식

| 옵션 | 설명 |
|---|---|
| `-r` | 디렉터리를 재귀적으로 복사한다 |
| `-p` | 원본 파일의 수정 시간·접근 시간·권한 비트를 보존한다 |
| `-3` | 두 원격 호스트 간 복사 시 데이터를 로컬 호스트를 경유해 전달한다(현재 기본 동작) |
| `-R` | 두 원격 호스트 간 복사 시 origin 호스트에 접속해 그 호스트에서 직접 `scp`를 실행시켜, 로컬을 거치지 않고 호스트끼리 바로 전송한다 |
| `-l LIMIT` | 대역폭을 킬로비트/초(Kbit/s) 단위로 제한한다 |
| `-C` | `ssh`에 `-C`를 전달해 전송 중 압축을 사용한다 |

### 프로토콜 선택·호환성

| 옵션 | 설명 |
|---|---|
| `-O` | 레거시 SCP/RCP 프로토콜을 강제로 사용한다(OpenSSH 9.0부터 기본값이 된 SFTP 대신) |
| `-T` | 원격이 보낸 파일명이 요청한 파일명과 일치하는지 검증하는 클라이언트 측 점검을 비활성화한다(OpenSSH 8.0에서 추가된 보안 점검을 끄는 옵션, 신뢰할 수 있는 서버와의 호환성 목적 외에는 권장되지 않는다) |

### 출력·기타

| 옵션 | 설명 |
|---|---|
| `-q` | 진행률 표시줄을 숨긴다 |
| `-v` | 상세 디버그 출력을 보여준다(연결 문제 진단용) |

## 예시

### 기본 복사

```bash
# 원격 파일을 현재 디렉터리로
scp user@host:/path/file.txt ./

# 로컬 파일을 원격 경로로
scp ./file.txt user@host:/path/
```

### 디렉터리·속성 보존

```bash
# 디렉터리 전체를 재귀적으로 복사
scp -r user@host:/path/dir ./

# 수정 시간·권한을 보존하며 복사(백업 목적에 유용)
scp -p ./config.yaml user@host:/etc/app/config.yaml
```

### 연결 옵션

```bash
# 표준 포트(22)가 아닌 2222번 포트로 접속
scp -P 2222 user@host:/path/file.txt ./

# 특정 개인키 파일로 인증
scp -i ~/.ssh/mykey user@host:/path/file.txt ./
```

### 원격 → 원격 복사

```bash
# 기본(-3): 데이터가 로컬 호스트를 경유해 host1 -> 로컬 -> host2로 이동
scp user@host1:/path/file.txt user@host2:/path/

# -R: host1에 접속해 그 자리에서 scp를 실행, host1 -> host2로 직접 전송(로컬 경유 없음)
scp -R user@host1:/path/file.txt user@host2:/path/
```

### 성능·호환성

```bash
# 느린 회선에서 압축을 켜서 전송량 줄이기
scp -C ./bigfile.tar user@host:/path/

# 업로드 대역폭을 800Kbit/s로 제한(다른 트래픽에 영향 최소화)
scp -l 800 ./bigfile.tar user@host:/path/

# 오래된 서버와 호환을 위해 레거시 SCP/RCP 프로토콜을 강제 사용
scp -O user@legacy-host:/path/file.txt ./
```

## 주의사항·함정

**OpenSSH는 scp의 레거시 전송 프로토콜을 실제로 SFTP로 교체했다.** `scp`가 오랫동안 써 온 근간 프로토콜(SCP/RCP, `rcp`에서 유래)에는 구조적인 보안 문제가 있었다. OpenSSH 8.0(2019년 4월 17일 릴리스) 릴리스 노트는 원격 서버가 클라이언트가 요청한 것과 다른 파일명을 응답으로 보내 임의 파일을 덮어쓸 수 있는 취약점(CVE-2019-6111)을 완화했다고 밝히며 다음과 같이 명시했다.

> "The scp protocol is outdated, inflexible and not readily fixed. We recommend the use of more modern protocols like sftp and rsync for file transfer instead." — OpenSSH 8.0 Release Notes (2019-04-17)

이 완화 조치로 클라이언트가 서버 응답 파일명을 검증하는 점검이 기본으로 켜졌고, 호환성이 필요할 때 이를 끄는 `-T` 옵션도 이때 추가됐다. 권고는 여기서 그치지 않았다 — OpenSSH 9.0(2022년 4월 8일 릴리스)은 실제로 `scp`의 **기본 전송 방식 자체**를 레거시 SCP/RCP에서 SFTP로 바꿨다.

> "This release switches scp(1) from using the legacy scp/rcp protocol to using the SFTP protocol by default." — OpenSSH 9.0 Release Notes (2022-04-08)

즉 `scp`라는 명령어 이름과 문법(`scp 소스 대상`)은 그대로지만, OpenSSH 9.0 이상에서는 실제 데이터 전송이 내부적으로 SFTP 프로토콜을 통해 이뤄진다. 예전 방식이 필요하면(오래된 서버와의 호환 등) `-O` 옵션으로 레거시 프로토콜로 되돌릴 수 있다. `scp(1)` man 페이지도 이를 명시한다.

> "Since OpenSSH 9.0, scp has used the SFTP protocol for transfers by default." — scp(1) man page

이 전환은 실무에서 두 가지 호환성 함정을 만든다. 첫째, SFTP 모드는 원격 홈 디렉터리 축약 표기(`~user/경로`)를 프로토콜 자체가 지원하지 않아, `scp host:~user/file /tmp` 같은 명령이 레거시 모드와 다르게 동작하거나 실패할 수 있다(서버의 `sftp-server`가 확장 기능을 지원하면 완화된다). 둘째, SFTP 모드는 파일명에 셸 메타문자가 있어도 예전처럼 까다로운 이중 인용이 필요 없어졌지만, 반대로 원격 쪽 와일드카드 확장에 의존하던 스크립트는 레거시 모드와 동작이 달라질 수 있다. 자동화 스크립트를 오래된 OpenSSH 버전과도 호환시켜야 한다면, 어떤 프로토콜을 가정하고 작성된 스크립트인지 점검할 필요가 있다.

**`-r` 없이 디렉터리를 복사하면 실패한다.** `cp`와 마찬가지로 `scp`도 대상이 디렉터리면 재귀 옵션을 명시해야 한다. `scp user@host:/path/dir ./`처럼 `-r`을 빠뜨리면 "not a regular file" 류의 에러로 실패하고, 자동화 스크립트에서는 이 실패가 조용히 다음 단계로 넘어가지 않도록 종료 코드를 반드시 확인해야 한다.

**원격-원격 복사는 기본적으로 로컬을 한 번 거친다.** `scp host1:file host2:file` 형태로 두 원격 호스트 사이를 복사하면, 기본 동작(`-3`)은 데이터를 로컬 머신을 거쳐 전달한다 — 로컬의 네트워크 대역폭과 디스크 I/O를 함께 소모한다는 뜻이다. 로컬을 거치지 않고 host1에서 host2로 직접 전송하려면 `-R`을 명시해야 하며, 이 경우 로컬 머신이 host1에 대한 자격 증명만 있으면 되는 대신 host1이 host2에 직접 접속할 수 있어야 한다(네트워크 경로·방화벽 정책이 다를 수 있다).

## 흔한 오개념

**"scp는 지금도 자체 SCP 프로토콜로 전송한다"는 오해.** `scp`라는 이름과 오래된 습관 때문에 이렇게 생각하기 쉽지만, OpenSSH 9.0 이상 환경에서는 기본적으로 SFTP 프로토콜을 통해 데이터가 오간다. 명령어 이름이 바뀌지 않았을 뿐, 내부 배관이 바뀌었다는 점을 구분해야 위의 호환성 함정을 진단할 수 있다.

**"scp도 rsync처럼 달라진 부분만 다시 보낸다"는 오해.** `scp`는 매번 지정한 파일 전체를 처음부터 끝까지 다시 전송한다. 이미 대상에 같은 파일이 있어도 증분 전송을 하지 않으며, 이 점이 대용량 반복 동기화에는 `scp`보다 `rsync`(`rsync -avz -e ssh ...`)가 더 유리한 이유다.

## 다음 장에서는

다음은 [43장: ssh](/post/bashshell/ssh-command-remote-login-secure-shell/) — 이 컬렉션의 **마지막 챕터**다. `scp`가 그대로 재사용하는 SSH 프로토콜 자체, 키 인증 흐름, `~/.ssh/config` 설정, 포트 포워딩을 본격적으로 다루며 bashshell 컬렉션을 마무리한다.

## 평가 기준

- `scp`의 세 가지 복사 방향(원격→로컬, 로컬→원격, 원격→원격) 문법을 구분해 쓸 수 있다.
- `scp`가 SSH 프로토콜의 인증·암호화 메커니즘을 재사용한다는 점과, `-i`·`-P` 옵션이 `ssh`와 대응한다는 점을 설명할 수 있다.
- OpenSSH가 언제, 왜 scp의 기본 전송 프로토콜을 SFTP로 바꿨는지(OpenSSH 9.0) 설명하고, 필요할 때 `-O`로 레거시 프로토콜로 되돌릴 수 있다.
- 원격-원격 복사에서 `-3`(로컬 경유, 기본)과 `-R`(직접 전송)의 차이를 구분해 상황에 맞게 선택할 수 있다.
- 대용량·반복 동기화에는 `scp`보다 `rsync`가 유리한 이유를 설명할 수 있다.

## 참고

- [OpenSSH 8.0 Release Notes](https://www.openssh.org/txt/release-8.0) — scp 프로토콜의 구조적 한계, CVE-2019-6111 완화, `-T` 옵션 도입
- [OpenSSH 9.0 Release Notes](https://www.openssh.org/txt/release-9.0) — scp 기본 전송 프로토콜을 SFTP로 전환, `-O` 옵션 도입
- [scp(1) - OpenBSD manual page](https://man.openbsd.org/scp.1)
- [scp(1) - Linux man page](https://man7.org/linux/man-pages/man1/scp.1.html)
