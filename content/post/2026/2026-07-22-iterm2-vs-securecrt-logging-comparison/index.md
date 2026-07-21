---
title: "[Terminal] iTerm2 vs SecureCRT 세션 로그 저장 기능 완전 비교"
description: "iTerm2와 SecureCRT의 세션 로그 저장 기능을 비교한다. 로그 활성화 메뉴 경로, Raw·Plain Text·HTML·asciinema 포맷 차이, 자동 로그 vs 수동 로그, 로그 파일명 변수 치환, 무료·유료 여부와 플랫폼 지원 차이까지 실제 설정값으로 정리한다."
date: "2026-07-22T00:00:00Z"
lastmod: "2026-07-22T00:00:00Z"
draft: true
categories:
  - Terminal
tags:
  - Terminal
  - Windows(윈도우)
  - macOS
  - Linux(리눅스)
  - Networking(네트워킹)
  - Comparison(비교)
  - SSH(Secure Shell)
  - Logging(로깅)
  - Configuration(설정)
  - Tutorial(튜토리얼)
  - Guide(가이드)
  - How-To
  - Tips
  - Reference(참고)
  - Best-Practices
  - Documentation(문서화)
  - Open-Source(오픈소스)
  - Productivity(생산성)
  - Automation(자동화)
  - Troubleshooting(트러블슈팅)
  - Case-Study
  - Deep-Dive
  - Beginner
  - Review(리뷰)
  - Technology(기술)
  - Backup
  - RDP(Remote Desktop Protocol)
  - Cloud(클라우드)
  - Self-Hosted(셀프호스팅)
  - Internet(인터넷)
  - Privacy(프라이버시)
  - Security(보안)
image: "wordcloud.png"
---

서버 작업 중 "방금 화면에 뭐가 찍혔더라"를 되짚어야 할 때, 세션 로그 파일이 있고 없고는 문제 해결 속도를 완전히 갈라놓는다. macOS 사용자가 즐겨 쓰는 오픈소스 터미널 <strong>iTerm2</strong>와, 네트워크 엔지니어들이 오랫동안 표준처럼 써온 상용 SSH 클라이언트 <strong>SecureCRT</strong>는 둘 다 세션 로그 저장 기능을 갖추고 있지만, 활성화 방법과 로그 포맷, 파일명 규칙, 가격 정책까지 세부 구현이 상당히 다르다. 이 글은 두 클라이언트의 공식 문서를 기준으로 로그 저장 기능만 집중적으로 비교한다.

---

## 이 글에서 다루는 내용

- iTerm2와 SecureCRT에서 로그를 켜는 정확한 메뉴 경로
- 로그 파일 포맷(Raw/Plain Text/HTML 등) 차이와 각각이 적합한 상황
- 자동 로그와 세션별 수동 로그의 차이
- 로그 파일명에 쓸 수 있는 변수(치환 파라미터) 비교
- 무료·유료 여부와 플랫폼 지원 차이

---

## iTerm2: 프로필 단위 자동 로깅과 세션별 수동 로깅

iTerm2는 macOS 전용 오픈소스 터미널 에뮬레이터로, 소스 코드가 GPL 계열 라이선스로 공개돼 있고 완전히 무료다. 로그 저장은 두 가지 경로로 나뉜다.

### 자동 로깅 활성화 경로

`iTerm2 > Preferences > Profiles > Session` 탭에 들어가면 <strong>"Enable automatic session logging"</strong> 체크박스가 있다. 공식 문서는 이 옵션을 이렇게 설명한다.

> If enabled, every session's output will be logged to a file in the specified directory. The filename format can also be specified here as an interpolated string.

이 체크박스를 켜면 해당 프로필로 여는 모든 세션이 지정한 폴더(Folder)에 자동으로 로그를 남긴다. Folder와 Filename 두 필드 모두 iTerm2의 <strong>Interpolated String(보간 문자열)</strong> 문법을 지원해 세션 정보를 파일명에 동적으로 끼워 넣을 수 있다.

### 세션별 수동 로깅

프로필 전체에 자동 로깅을 걸지 않고 지금 열려 있는 세션 하나만 즉석에서 로그로 남기고 싶다면, 메뉴바의 `Session` 메뉴에서 로그 시작/중지를 개별 토글할 수 있다. 자동 로깅 설정과 별개로 동작하므로, 평소에는 로그를 남기지 않다가 특정 작업을 재현해야 할 때만 임시로 켜는 용도로 쓰기 좋다.

---

## SecureCRT: 세션 옵션의 Log File 카테고리

SecureCRT는 VanDyke Software가 Windows·macOS·Linux용으로 만드는 상용 SSH/텔넷 클라이언트다. 무료 체험판은 있지만 정식 사용에는 라이선스 구매가 필요하다. 로그 설정은 세션 옵션 안에 있다.

### 자동 로깅 활성화 경로

연결한 세션에서 `Options > Session Options`를 열고 `Terminal > Log File` 카테고리로 들어가면 <strong>"Start log upon connect"</strong> 옵션이 있다. 이 옵션을 켜면 해당 세션에 접속하는 즉시 로그 파일 기록이 시작된다. 이 설정을 세션 하나에만 적용하지 않고 전체 세션에 일괄 반영하려면, `Options > Configure > Default Session`에서 같은 옵션을 켠 뒤 "Change ALL sessions" 여부를 묻는 대화상자에서 적용을 선택하면 된다(SecureCRT 9.4 이상 기준).

### 세션별 수동 로깅

특정 접속 하나만 즉석에서 기록하고 싶다면 `File` 메뉴의 <strong>"Log Session"</strong> 항목을 클릭한다. 저장 위치를 묻는 대화상자가 뜨고, 로그가 시작되면 `File` 메뉴를 다시 열었을 때 "Log Session" 옆에 체크 표시가 붙어 현재 로깅 중임을 확인할 수 있다. 같은 항목을 다시 클릭하면 로깅이 꺼진다.

---

## 로그 파일 포맷: iTerm2가 선택지가 더 많다

로그를 열었을 때 그 안에 뭐가 담기는지는 두 클라이언트가 접근 방식 자체가 다르다.

iTerm2는 프로필의 자동 로깅 설정에서 포맷을 명시적으로 고를 수 있다. 공식 문서에 정리된 네 가지 옵션은 다음과 같다.

- <strong>Raw data</strong>: "An exact copy of the input that was received including control sequences." 커서 이동, 색상 코드 같은 제어 시퀀스까지 그대로 남기 때문에 원본을 재생하거나 분석 도구에 넘길 때 유용하다.
- <strong>Plain text</strong>: "Excludes control sequences. Just text and newlines. This is very readable when running CLI apps but becomes utter chaos for interactive programs like vim or emacs." 일반적인 CLI 명령 출력을 나중에 grep하거나 사람이 읽기에는 이 포맷이 가장 편하다.
- <strong>HTML</strong>: "Like Plain text, it excludes control sequences. Colors and various font attributes are preserved. The resulting file can be viewed in a web browser." 색상 정보를 보존하면서도 브라우저로 바로 열어볼 수 있다.
- <strong>asciinema</strong>: "Produces a file viewable with asciinema, which preserves time as well as more font attributes." 타이핑 속도와 화면 변화까지 시간 축으로 재생하고 싶을 때 쓴다.

SecureCRT는 기본적으로 화면에 표시되는 문자를 그대로 텍스트 로그 파일에 순서대로 기록하는 방식이다. 여기에 <strong>"Timestamp each line"</strong> 옵션을 추가로 켜면 로그의 각 줄 앞에 타임스탬프를 붙일 수 있고, 그 표시 형식도 `[%Y-%M-%D %h:%m:%s.%t]`처럼 SecureCRT 고유의 치환 파라미터로 직접 지정한다. 즉 iTerm2가 "포맷 자체를 라디오 버튼으로 고르는" 방식이라면, SecureCRT는 "기본 텍스트 로그에 타임스탬프 유무·형식을 옵션으로 얹는" 방식에 가깝다.

---

## 로그 파일명 변수: 둘 다 치환 문법을 지원한다

세션을 여러 개 반복해서 여는 환경에서는 로그 파일명이 자동으로 세션 정보를 반영해야 매번 덮어쓰기 걱정 없이 쓸 수 있다. 두 클라이언트 모두 이 문제를 치환 변수로 해결한다.

iTerm2는 Folder·Filename 필드 모두에서 <strong>Interpolated String(보간 문자열)</strong> 문법 `\(…)`을 쓴다. 예를 들어 `\(session.username)@\(session.hostname)`처럼 세션의 사용자명·호스트명 같은 내장 변수(Variables)를 문자열 안에 그대로 끼워 넣을 수 있다. 세션 생성 시각을 나타내는 `creationTimeString` 같은 변수도 파일명에 활용할 수 있다.

SecureCRT는 `%` 접두사를 쓴 고유 치환 파라미터를 로그 파일명 입력란에 직접 조합한다. 대표적인 파라미터는 다음과 같다.

| 파라미터 | 의미 |
|---------|------|
| `%H` | 호스트명 |
| `%S` | 세션 이름 |
| `%Y` | 4자리 연도 |
| `%M` | 2자리 월 |
| `%D` | 일 |
| `%P` | 포트 번호 |
| `%h` | 2자리 시 |
| `%m` | 2자리 분 |
| `%s` | 2자리 초 |
| `%t` | 3자리 밀리초 |
| `%F` | Sessions 폴더 기준 하위 디렉터리 경로 |

예를 들어 `C:\Logs\%F\%S(%H)-%Y%M%D-%h%m%s_%t_log.txt` 형태로 지정하면 세션 이름·호스트명·접속 시각이 모두 파일명에 반영된 고유한 로그 파일이 접속마다 새로 생성된다. 로그 파일명에 날짜가 바뀌는 변수를 넣고 자정에 새 파일을 만들도록 설정하면, 장기간 켜 두는 세션의 로그도 하루 단위로 자동 분할할 수 있다.

---

## 무료/유료와 플랫폼 지원

| 항목 | iTerm2 | SecureCRT |
|------|--------|-----------|
| 라이선스 | 오픈소스, 완전 무료 | 상용, 유료 라이선스(체험판 제공) |
| 지원 플랫폼 | macOS 전용 | Windows / macOS / Linux |
| 자동 로깅 설정 위치 | Preferences > Profiles > Session | Session Options > Terminal > Log File |
| 수동 로깅 트리거 | Session 메뉴에서 세션별 토글 | File 메뉴의 Log Session |
| 로그 포맷 선택지 | Raw data / Plain text / HTML / asciinema | 텍스트 로그 + 줄 단위 타임스탬프 옵션 |
| 파일명 변수 문법 | Interpolated String `\(…)` | `%` 접두사 치환 파라미터 |
| 전체 세션 일괄 적용 | 프로필 단위로 자동 상속 | Default Session 수정 후 "Change ALL sessions" |

iTerm2는 macOS 사용자라면 추가 비용 없이 바로 쓸 수 있고, 소스가 공개돼 있어 로깅 동작을 코드 수준까지 확인할 수 있다는 점이 강점이다. 반대로 Windows나 Linux 환경에서 SSH 클라이언트가 필요하거나, 네트워크 장비 접속 이력을 회사 표준 포맷으로 남겨야 하는 조직이라면 크로스플랫폼을 지원하고 세밀한 타임스탬프·치환 파라미터 체계를 갖춘 SecureCRT 쪽이 실무에 더 맞는 경우가 많다.

---

## 어떤 상황에 어떤 클라이언트가 맞을까

- <strong>macOS에서 개인 개발 작업</strong>을 로그로 남기고 싶다면 iTerm2의 자동 로깅으로 충분하다. 특히 색상 그대로 보존한 재생 기록이 필요하면 HTML이나 asciinema 포맷을 쓴다.
- <strong>Windows·Linux를 오가며 여러 서버에 SSH 접속</strong>해야 하고, 접속 이력을 회사 감사(audit) 요건에 맞춰 표준화된 파일명·타임스탬프로 남겨야 한다면 SecureCRT의 Default Session 일괄 설정이 유리하다.
- <strong>제어 시퀀스까지 포함한 원본 그대로의 로그</strong>가 필요하면(로그 재생, 별도 파서 개발 등) iTerm2의 Raw data 포맷을 우선 검토한다.
- <strong>비용 없이 시작</strong>하고 싶다면 iTerm2가 답이고, <strong>플랫폼 이식성</strong>이 우선이라면 SecureCRT 라이선스 구매를 고려한다.

---

## 참고 문헌

1. [Session Profile Preferences — iTerm2 Documentation](https://iterm2.com/documentation-preferences-profiles-session.html) — 자동 로깅 체크박스와 로그 포맷 4종(Raw data/Plain text/HTML/asciinema) 설명.
2. [Variables — iTerm2 Documentation](https://iterm2.com/documentation-variables.html) — 파일명에 쓸 수 있는 내장 변수와 Interpolated String 문법.
3. [iTerm2 공식 사이트](https://iterm2.com/) — 라이선스, 다운로드, 플랫폼 정보.
4. [Menu Items — iTerm2 3.3 Documentation](https://iterm2.com/3.3/documentation-menu-items.html) — Session 메뉴의 로깅 토글 항목.
5. [How To Configure SecureCRT to Automatically Log Session Data to a File — VanDyke Software](https://www.vandyke.com/support/tips/configure-automated-logging-in-securecrt.html) — Log File 카테고리 설정 절차와 치환 파라미터 목록.
6. [SecureCRT — VanDyke Software 제품 페이지](https://www.vandyke.com/products/securecrt/index.html) — 플랫폼 지원, 라이선스 정책.
7. [SecureCRT — Wikipedia](https://en.wikipedia.org/wiki/SecureCRT) — 제품 개요와 개발사 정보.
