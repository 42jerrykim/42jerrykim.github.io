---
draft: false
slug: curl-wget-commands-download-http-files
title: "[Bash Shell] 41. curl, wget - HTTP 요청과 다운로드"
description: "curl과 wget은 둘 다 HTTP(S)·FTP 클라이언트지만 설계 철학이 다르다. curl은 헤더·인증을 다루는 범용 CLI, wget은 재귀 다운로드·미러링 특화다. -O/-o 차이, curl의 기본 리다이렉트 미추적, wget의 robots.txt 존중, -k 위험을 다룬다."
date: 2026-03-15
lastmod: 2026-08-24
collection_order: 410
categories:
- Bash Shell
tags:
- Bash
- Shell(셸)
- Linux(리눅스)
- Terminal
- Command
- HTTP(HyperText Transfer Protocol)
- HTTPS
- TLS
- Proxy(프록시)
- API(Application Programming Interface)
- Networking(네트워킹)
- Automation(자동화)
- Security(보안)
- curl
- wget
- HTTP-Request(HTTP요청)
- 다운로드
- Download
- FTP
- Redirect(리다이렉트)
- Certificate(인증서)
- Man-In-The-Middle(중간자공격)
- Robots-txt
- Recursive-Download(재귀다운로드)
- Mirroring(미러링)
- Client-Server(클라이언트서버)
image: "wordcloud.png"
---

`curl`과 `wget`은 리눅스·유닉스에서 **URL로 HTTP(S)·FTP 요청을 보내고 응답·파일을 받는** 두 대표 명령줄 클라이언트다. 겉보기엔 둘 다 "URL을 주면 뭔가를 받아온다"는 점이 같아 자주 혼동되지만, 아래에서 볼 것처럼 설계 철학이 근본적으로 다르다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [40장: du, df](/post/bashshell/du-df-commands-disk-usage-linux/)에서 로컬 디스크 사용량을 확인하는 법을 다룬 뒤 이어진다. 여기서부터 <strong>Part 7(네트워크와 원격 접속)</strong>이 시작된다 — 지금까지 다룬 명령어는 전부 지금 이 컴퓨터 안의 파일·프로세스·디스크를 대상으로 했다면, 이제부터는 셸에서 네트워크 너머의 서버·원격 호스트와 데이터를 주고받는 단계로 넘어간다. 파이프(`|`)로 명령 출력을 연결하는 법([19장: 파이프](/post/bashshell/pipe-operator-linux-command-chaining/))과 표준 출력을 파일로 리다이렉트하는 법([20장: 리다이렉션](/post/bashshell/io-redirection-linux-bash-tutorial/))을 알고 있으면 예시를 읽기 더 수월하다.

**이 장의 깊이**: **입문–중급** 난이도다. 파일 다운로드부터 HTTP 메서드·헤더·인증을 다루는 API 호출, 재귀 다운로드·미러링까지 실무에서 자주 쓰는 범위를 다룬다. **다루지 않는 것**: SSH 키 기반의 원격 파일 복사·로그인은 [42장: scp](/post/bashshell/scp-command-secure-copy-remote-files/)와 43장(ssh)에서 다루고, HTTP 프로토콜 자체의 심화(HTTP/2·HTTP/3, 캐싱 헤더 전체 체계)는 범위 밖이다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| 파일 하나 빨리 받거나 API를 한 번 찔러봐야 하는 사람 | "개요 + 정신 모델", "사용법·옵션"의 기본 표, "예시"의 기본 다운로드·API 호출 | `curl -O`/`wget`으로 파일을 받고 `curl -X POST -d`로 간단한 API 요청을 보낼 수 있다 |
| curl과 wget을 제대로 구분해서 스크립트·자동화에 쓰려는 사람 | "옵션" 전체, "주의사항·함정", "흔한 오개념" | 리다이렉트·인증서 검증·robots.txt처럼 조용히 잘못될 수 있는 지점을 미리 알고 방어적으로 스크립트를 짤 수 있다 |

---

## 개요 + 정신 모델

`curl`과 `wget`은 둘 다 URL 하나로 HTTP(S)·FTP 통신을 한다는 공통점이 있지만, <strong>"이 도구가 세상을 무엇으로 보는가"</strong>가 다르다.

`curl`은 **범용 데이터 전송 라이브러리(libcurl) 위에 얹힌 CLI**다. Daniel Stenberg가 1998년 Rafael Sagula의 `httpget`을 이어받아 `curl`로 이름을 바꿔 공개했는데, 이때 이미 GET뿐 아니라 업로드까지 지원해 이름 자체가 바뀔 정도로 "다양한 프로토콜로 데이터를 주고받는 범용 도구"를 지향했다. 그래서 curl은 GET/POST/PUT/DELETE 같은 HTTP 메서드, 커스텀 헤더, 인증, 파일 업로드(멀티파트)까지 세밀하게 제어할 수 있고, 셸 스크립트에서 REST API를 호출하거나 상태 코드만 뽑아내는 용도로도 널리 쓰인다. curl의 핵심은 <strong>"한 번의 요청을 정밀하게 구성해서 보내고 응답을 원하는 형태로 받는 것"</strong>이다.

`wget`은 이와 달리 <strong>"URL 하나에서 시작해 필요한 만큼 계속 따라가며 로컬에 통째로 내려받는 것"</strong>을 정신 모델로 삼는다. Hrvoje Nikšić이 1996년에 발표한 `Geturl`에서 출발해 그해 말 `Wget`으로 이름을 바꿨고, GNU 프로젝트에 편입되면서 지금의 형태로 자리 잡았다. wget은 애초에 배치 다운로드·백그라운드 실행·중단된 다운로드 이어받기·재귀적으로 링크를 따라가며 사이트 전체를 미러링하는 기능에 특화되어 있고, 반대로 HTTP 메서드나 멀티파트 업로드 같은 요청 구성 기능은 curl만큼 세밀하지 않다.

요약하면 curl은 "요청을 얼마나 정밀하게 만들 수 있는가"에, wget은 "얼마나 많은 파일을 얼마나 견고하게 받아올 수 있는가"에 강점을 둔 도구다. 실무에서는 API 호출·헬스체크·스크립트 내 단발성 다운로드에는 curl을, 문서 사이트 전체 백업이나 대용량 파일의 안정적 다운로드에는 wget을 선택하는 경우가 많다.

---

## 사용법 · 옵션

### curl

기본 문법은 `curl [옵션] URL...`이다. URL을 여러 개 주면 순서대로 각각 요청한다.

**요청 방식·데이터**

| 옵션 | 설명 |
|------|------|
| `-X, --request <METHOD>` | HTTP 메서드 지정(GET/POST/PUT/DELETE 등, 생략 시 데이터가 있으면 자동으로 POST) |
| `-d, --data <DATA>` | 요청 본문 전송(기본 `Content-Type: application/x-www-form-urlencoded`) |
| `--data-binary <DATA>` | 데이터를 가공 없이 그대로 전송(개행 등 원본 보존) |
| `-F, --form <NAME=VALUE>` | `multipart/form-data` 전송, 파일은 `-F "file=@경로"`로 첨부 |
| `-G, --get` | `-d`로 지정한 데이터를 URL 쿼리 문자열로 붙여 GET 요청 |

**헤더·인증**

| 옵션 | 설명 |
|------|------|
| `-H, --header <HEADER>` | 커스텀 헤더 추가(여러 번 지정 가능) |
| `-u, --user <user:pass>` | HTTP Basic 인증 |
| `-b, --cookie <DATA/FILE>` | 요청에 쿠키 포함 |
| `-c, --cookie-jar <FILE>` | 응답 `Set-Cookie`를 파일로 저장 |

**출력 제어**

| 옵션 | 설명 |
|------|------|
| `-O, --remote-name` | URL의 파일명 그대로 저장(경로는 잘라내고 파일명만 사용) |
| `-o, --output <FILE>` | 지정한 파일명으로 저장 |
| `-I, --head` | HEAD 요청만 보내 헤더·상태 코드만 확인 |
| `-s, --silent` | 진행률·에러 메시지 숨김(스크립트용) |
| `-v, --verbose` | 요청·응답을 상세히 출력(디버깅용) |
| `-w, --write-out <FORMAT>` | 응답 처리 후 지정한 형식으로 정보 출력(예: `%{http_code}`) |

**전송 제어**

| 옵션 | 설명 |
|------|------|
| `-L, --location` | HTTP 리다이렉트(3xx `Location` 헤더)를 따라감 |
| `--max-redirs <N>` | `-L` 사용 시 최대 추적 횟수(기본값 50) |
| `-k, --insecure` | TLS 인증서 검증을 생략(보안 위험, 아래 주의사항 참고) |
| `--retry <N>` | 일시적 오류 시 재시도 횟수 |
| `-m, --max-time <SEC>` | 전체 요청 제한 시간(초) |

### wget

기본 문법은 `wget [옵션] URL...`이다.

**기본 저장·전송**

| 옵션 | 설명 |
|------|------|
| `-O, --output-document <FILE>` | 저장 파일명 지정(curl의 `-o`와 동일한 역할, 옵션 문자는 다름) |
| `-c, --continue` | 중단된 다운로드를 이어받기 |
| `-q, --quiet` | 진행률·로그 출력 억제 |
| `-b, --background` | 백그라운드로 실행하고 로그를 `wget-log`에 남김 |
| `--limit-rate=RATE` | 다운로드 속도 제한(예: `200k`) |

**재귀·미러링**

| 옵션 | 설명 |
|------|------|
| `-r, --recursive` | 재귀 다운로드 활성화(기본 최대 깊이 5) |
| `-l, --level=N` | 재귀 깊이 지정 |
| `-np, --no-parent` | 상위 디렉터리로 올라가지 않음 |
| `-k, --convert-links` | 다운로드 후 페이지 내 링크를 로컬 경로로 변환 |
| `-m, --mirror` | 미러링에 최적화된 옵션 조합(재귀·타임스탬프 비교·무한 깊이 등을 한 번에 켬) |
| `-e robots=off` | `robots.txt` 규칙을 무시(기본은 준수, 아래 주의사항 참고) |

**접속 제어**

| 옵션 | 설명 |
|------|------|
| `--user=`, `--password=` | 인증 정보 지정 |
| `--no-check-certificate` | TLS 인증서 검증을 생략(보안 위험, curl의 `-k`와 동일한 위험) |
| `-T, --timeout=SEC` | 응답 제한 시간(초) |

## 예시

### curl — 기본 다운로드

```bash
# URL의 파일명 그대로 저장
curl -O https://example.com/file.zip

# 쿼리 문자열이 섞인 URL은 원하는 이름으로 직접 지정
curl -o archive.zip "https://example.com/download?id=42"
```

### curl — 상태·헤더 확인

```bash
# HEAD 요청으로 본문 없이 상태 코드·헤더만 확인
curl -I https://example.com

# 본문은 버리고 상태 코드만 스크립트 변수로 뽑아내기
status=$(curl -s -o /dev/null -w "%{http_code}" https://example.com)
```

### curl — 리다이렉트 추적

```bash
# 리다이렉트를 따라가 최종 페이지를 저장(자세한 이유는 아래 주의사항 참고)
curl -L -o page.html https://example.com/old-path
```

### curl — API 호출

```bash
# JSON 본문으로 POST 요청
curl -X POST -H "Content-Type: application/json" \
  -d '{"name":"test"}' https://api.example.com/users

# 파일을 멀티파트로 업로드
curl -F "file=@report.pdf" https://api.example.com/upload

# Basic 인증이 필요한 API 호출
curl -u user:pass https://api.example.com/secure

# 일시적 오류에 대비해 재시도·전체 시간 제한을 함께 지정
curl --retry 3 -m 10 https://api.example.com/flaky-endpoint
```

### wget — 기본 다운로드·이어받기

```bash
wget https://example.com/file.zip

# 중단된 대용량 다운로드를 이어받기
wget -c https://example.com/large-file.iso

# 조용히 받아 표준 출력으로 흘려보내 다른 명령과 파이프
wget -q -O - https://example.com/status.json | grep '"ok"'
```

### wget — 재귀 다운로드·미러링

```bash
# 문서 사이트를 상위 디렉터리로 올라가지 않고 재귀적으로 내려받고, 링크는 로컬 경로로 변환
wget -r -np -k https://example.com/docs/

# 대역폭을 제한하며 백업 파일 다운로드
wget --limit-rate=200k -O backup.tar.gz https://example.com/backup.tar.gz
```

## 주의사항·함정

**`-O`(대문자)와 `-o`(소문자)를 헷갈리면 파일이 엉뚱한 이름으로 저장된다.** curl에서 `-O`는 URL의 마지막 경로 세그먼트를 그대로 로컬 파일명으로 쓰고, `-o`는 사용자가 이름을 직접 지정한다. URL이 `https://example.com/download?id=42`처럼 쿼리 문자열로 끝나거나 마지막 세그먼트가 없으면(`/`로 끝나는 URL) `-O`가 의도와 다른 이름으로 저장하거나 실패할 수 있으므로, 파일명이 URL에 명확히 드러나지 않는 경우는 `-o`로 직접 지정하는 편이 안전하다. wget은 애초에 옵션 체계가 달라 `-O`(대문자) 하나만 저장 파일명 지정에 쓰인다.

**curl은 기본적으로 HTTP 리다이렉트를 따라가지 않는다.** curl 공식 매뉴얼은 `-L`/`--location`을 이렇게 설명한다.

> "(HTTP) If the server reports that the requested page has moved to a different location (indicated with a Location: header and a 3xx response code), this option will make curl redo the request on the new place." — [curl(1) man page](https://curl.se/docs/manpage.html)

뒤집어 말하면 `-L`을 빠뜨리면 curl은 **에러를 내지 않고** 3xx 응답 자체(리다이렉트 헤더와 아주 짧은 본문)를 정상적으로 받아 저장·출력하고 종료 코드 0으로 끝낸다. `curl -O https://example.com/old-path`처럼 리다이렉트가 걸린 URL을 `-L` 없이 받으면, 원하던 최종 콘텐츠 대신 "Moved" 안내 문구 몇 줄짜리 파일이 조용히 저장되는 흔한 실수가 벌어진다. 실패했다는 신호가 전혀 없기 때문에 결과 파일을 열어보기 전까지는 알아채기 어렵다. `-L`을 쓸 때는 `--max-redirs`(기본 50)로 무한 리다이렉트 루프에 대비하는 것도 함께 고려한다.

**wget의 재귀 다운로드(`-r`)는 기본적으로 `robots.txt`를 존중한다.** [GNU wget 매뉴얼](https://man7.org/linux/man-pages/man1/wget.1.html)은 재귀 검색 시 "Wget respects the Robot Exclusion Standard (`/robots.txt`)"라고 명시한다. 즉 대상 사이트의 `robots.txt`가 특정 경로의 크롤링을 금지하면 `-r`은 그 경로를 자동으로 건너뛴다. `-e robots=off`(또는 `~/.wgetrc`에 `robots = off`)로 이 검사를 끌 수는 있지만, 이는 사이트 운영자가 명시적으로 남긴 크롤링 정책을 무시하는 것이므로 서버 부하·이용 약관 위반 소지를 감수하는 결정이다. 자신이 관리하는 사이트를 백업하는 경우가 아니라면 함부로 끄지 않는다.

**`-k`(curl `--insecure`)와 `--no-check-certificate`(wget)는 TLS 인증서 검증 자체를 생략한다.** curl 매뉴얼은 이렇게 설명한다.

> "(TLS) By default, every SSL connection curl makes is verified to be secure. This option tells curl to skip the verification step and proceed without checking." — [curl(1) man page](https://curl.se/docs/manpage.html)

이 옵션을 쓰면 통신 자체는 여전히 암호화되지만, 상대가 정말 그 도메인의 정당한 서버인지는 확인하지 않는다. 그 결과 중간자가 위조된(자체 서명) 인증서로 통신을 가로채도 클라이언트가 이를 정상으로 받아들이는 <strong>중간자 공격(MITM)</strong>에 그대로 노출된다. 사내 테스트 환경에서 자체 서명 인증서를 쓰는 등 신뢰할 수 있는 경로가 이미 확보된 경우가 아니라면, 특히 운영 스크립트에서는 이 옵션을 쓰지 않는다.

## 흔한 오개념

**"wget으로 사이트를 통째로 미러링할 수 있다"는 절반만 맞다.** `wget -r`/`-m`은 HTML을 파싱해 `<a href>` 같은 정적 링크를 따라가며 파일을 내려받는다. 하지만 자바스크립트가 실행된 뒤에야 콘텐츠를 렌더링하는 SPA(Single Page Application)는 wget이 받는 원본 HTML에는 실제 콘텐츠가 없는 빈 뼈대만 있는 경우가 많다. 이런 사이트를 미러링하려면 wget 대신 헤드리스 브라우저 기반 도구가 필요하다.

**`-k`/`--insecure`는 "그냥 HTTPS를 안 쓰는 것"이 아니다.** 초심자는 이 옵션을 "암호화를 끄는 옵션"으로 오해하기 쉽지만, 실제로는 전송 구간 자체는 여전히 TLS로 암호화된 채 유지되고 **인증서가 신뢰할 수 있는 CA(인증기관)로부터 발급됐는지, 도메인과 일치하는지를 검증하는 단계만 건너뛴다.** 암호화는 되고 있으니 안전하다고 착각하기 쉽지만, 검증을 생략한다는 것 자체가 위조 인증서를 걸러낼 방법이 없다는 뜻이라는 점이 핵심 위험이다.

## 다음 장에서는

다음은 [42장: scp](/post/bashshell/scp-command-secure-copy-remote-files/) — 이번 장이 URL을 통한 HTTP(S) 통신을 다뤘다면, scp는 SSH 인증을 이용해 로컬과 원격 호스트 사이에 파일·디렉터리를 직접 주고받는 법을 다룬다.

## 평가 기준

- curl과 wget의 설계 철학 차이(정밀한 요청 구성 vs 재귀 다운로드·미러링 특화)를 설명할 수 있다.
- curl의 `-O`/`-o`, wget의 `-O` 차이를 구분하고 URL 형태에 맞게 저장 방식을 선택할 수 있다.
- curl이 기본적으로 HTTP 리다이렉트를 따라가지 않으며 실패 신호 없이 조용히 끝난다는 점을 알고, `-L`을 언제 붙여야 하는지 판단할 수 있다.
- wget `-r`이 기본적으로 `robots.txt`를 존중한다는 것과 `-e robots=off`로 이를 끄는 것의 의미·위험을 설명할 수 있다.
- `-k`/`--insecure`·`--no-check-certificate`가 왜 중간자 공격에 노출시키는지 설명하고, 운영 환경에서 피해야 하는 이유를 판단할 수 있다.

## 참고

- [curl(1) man page — 공식 매뉴얼](https://curl.se/docs/manpage.html)
- [wget(1) — Linux manual page (man7.org)](https://man7.org/linux/man-pages/man1/wget.1.html)
