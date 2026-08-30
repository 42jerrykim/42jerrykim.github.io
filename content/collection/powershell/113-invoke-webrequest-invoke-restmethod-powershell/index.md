---
draft: false
collection_order: 113
slug: invoke-webrequest-invoke-restmethod-powershell
title: "[PowerShell] 113. Invoke-WebRequest/Invoke-RestMethod"
date: 2026-08-29
lastmod: 2026-08-29
description: "HTTP 응답 전체를 객체로 돌려주는 Invoke-WebRequest와 JSON/XML을 자동으로 파싱해 주는 Invoke-RestMethod의 차이, -Method/-Body/-Headers 매개변수로 REST API를 호출하는 방법을 정리한 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- Network(네트워크)
- Guide(가이드)
- Education(교육)
- Beginner
- Documentation(문서화)
- Quick-Reference
- Best-Practices
- Comparison(비교)
- Reference(참고)
- How-To
- Tips
- Automation(자동화)
- DevOps
- Invoke-WebRequest
- Invoke-RestMethod
- REST-API
- HTTP-Request
- JSON
- HTTP-Client
image: "wordcloud.png"
---

## 개요

<strong>Invoke-WebRequest</strong>와 <strong>Invoke-RestMethod</strong>는 PowerShell에서 HTTP·HTTPS 요청을 보내는 두 개의 핵심 cmdlet이다. 지금까지 Part 16에서 ping·포트·DNS로 "연결이 되는가"를 확인했다면, 이 장은 그 연결 위에서 실제로 "데이터를 주고받는" 단계로 넘어간다 — curl이나 웹 브라우저의 역할을 PowerShell 객체 파이프라인 안에서 수행하는 것이다.

정신 모델은 "`Invoke-WebRequest`가 HTTP 응답을 있는 그대로(상태 코드, 헤더, 원본 본문, 링크·폼 목록) 객체로 포장해 돌려주는 범용 웹 클라이언트라면, `Invoke-RestMethod`는 그 본문이 JSON이나 XML이라는 것을 알고 있다고 가정하고 곧바로 PowerShell 객체로 역직렬화해 주는 REST API 전용 클라이언트"라는 것이다. 둘 다 같은 내부 엔진을 쓰지만, "응답을 파싱해서 쓸 것인가, 원본 그대로 다룰 것인가"에 따라 선택이 갈린다.

실무에서는 어느 API를 처음 다룰 때 응답 구조를 모르는 상태에서 `Invoke-RestMethod`를 먼저 호출했다가 예상과 다른 형태의 객체가 나와 당황하는 경우가 흔한데, 이럴 때는 `Invoke-WebRequest`로 원본 `Content` 문자열을 먼저 눈으로 확인한 뒤 `Invoke-RestMethod`로 전환하는 순서가 안전하다.

## 사용법

```powershell
Invoke-WebRequest -Uri <URL> [-Method Get|Post|...] [-Body <내용>] [-OutFile <경로>]
Invoke-RestMethod -Uri <URL> [-Method Get|Post|...] [-Body <내용>] [-Headers <해시테이블>]
```

## 종류

| cmdlet | 반환 값 | 적합한 상황 |
|---|---|---|
| `Invoke-WebRequest` | `BasicHtmlWebResponseObject`(`StatusCode`, `Content`, `Headers`, `Links`, `Forms` 등) | HTML 페이지 크롤링, 파일 다운로드, 응답 헤더·상태 코드 자체를 검사해야 할 때 |
| `Invoke-RestMethod` | JSON/XML을 역직렬화한 `PSCustomObject`(또는 배열) | REST API 호출, 응답 본문을 곧바로 PowerShell 객체로 다뤄야 할 때 |

| 공통 매개변수 | 의미 |
|---|---|
| `-Method` | `Get`(기본)/`Post`/`Put`/`Delete`/`Patch` 등 HTTP 메서드 |
| `-Body` | 요청 본문(문자열, 해시테이블, 또는 `ConvertTo-Json`한 객체) |
| `-Headers` | 요청 헤더를 담은 해시테이블(`Authorization`, `Accept` 등) |
| `-ContentType` | 요청 본문의 MIME 타입(예: `application/json`) |
| `-OutFile` | 응답 본문을 화면 대신 파일로 저장 |

## 예시

```powershell
$response = Invoke-WebRequest -Uri "https://www.microsoft.com"        # HTML 페이지 요청
$response.StatusCode                                                     # 200
$response.Links | Select-Object -First 5 href                            # 페이지 내 링크 목록 추출

Invoke-WebRequest -Uri "https://example.com/file.zip" -OutFile "file.zip"  # 파일 다운로드(curl -O에 대응)

$data = Invoke-RestMethod -Uri "https://api.github.com/repos/PowerShell/PowerShell"   # JSON 응답이 곧바로 객체로
$data.stargazers_count                                                   # 역직렬화된 속성에 바로 접근

$body = @{ name = "test"; value = 42 } | ConvertTo-Json                   # 요청 본문을 JSON 문자열로 구성
Invoke-RestMethod -Uri "https://api.example.com/items" -Method Post `
    -Body $body -ContentType "application/json"                          # POST 요청으로 REST API 호출

$headers = @{ Authorization = "Bearer $token" }                          # 100장 자격 증명 개념과 조합
Invoke-RestMethod -Uri "https://api.example.com/secure" -Headers $headers  # 인증 토큰을 헤더에 담아 요청
```

## 주의사항·함정

**`Invoke-RestMethod`가 응답 헤더나 상태 코드에 직접 접근할 방법이 기본적으로 없다는 것을 놓치기 쉽다**: `Invoke-RestMethod`는 본문을 곧바로 객체로 반환하기 때문에, `Invoke-WebRequest`처럼 `.StatusCode`나 `.Headers`에 자연스럽게 접근할 수 없다. PowerShell 7.4부터는 `-ResponseHeadersVariable`로 헤더를 별도 변수에 담을 수 있지만, 이를 모르면 REST API 호출 결과에서 상태 코드를 확인하려다 막힐 수 있다.

**PowerShell 7.4부터 요청 인코딩 기본값이 ASCII에서 UTF-8로 바뀌었다**: 이전 버전 스크립트를 최신 pwsh로 옮길 때, 비ASCII 문자(한글 등)가 포함된 요청 본문의 인코딩 방식이 달라져 API 서버가 다르게 해석할 수 있다. 다른 인코딩이 필요하면 `-Headers`의 `Content-Type`에 `charset` 속성을 명시적으로 지정해야 한다.

**`-Body`에 해시테이블을 그냥 넘기면 JSON이 아니라 폼 인코딩(`application/x-www-form-urlencoded`)으로 전송된다**: REST API 대부분은 JSON 본문을 기대하므로, JSON을 보내려면 `$body | ConvertTo-Json`으로 명시적으로 변환한 뒤 `-ContentType "application/json"`을 함께 지정해야 한다. 이 변환을 빠뜨리면 서버가 요청 본문을 파싱하지 못해 400 오류가 돌아온다.

**대량의 페이지네이션된 API 응답을 반복 호출할 때 매번 새 TCP 연결을 맺는 비용을 간과하기 쉽다**: `-SessionVariable`로 세션을 만들어 재사용하면(`Invoke-WebRequest -SessionVariable session` 이후 `-WebSession $session`으로 후속 요청에 전달) 쿠키·연결을 유지할 수 있어, 로그인 세션이 필요한 API를 반복 호출할 때 효율적이다.

**이식성**: `curl`(Linux/macOS 및 Windows 10+ 기본 포함)은 명령줄 옵션이 훨씬 세분화돼 있고 원시 텍스트 응답을 그대로 출력하는 반면, `Invoke-RestMethod`는 JSON을 자동으로 객체로 바꿔줘 `jq` 같은 별도 파싱 도구가 필요 없다. 다만 `curl`은 사실상 모든 유닉스 계열 시스템의 표준 도구라 이식성 자체는 더 넓고, 셸 스크립트 간 공유가 쉽다는 장점이 있다 — PowerShell 환경 안에서 객체로 후처리할 계획이 없다면 `curl`이 더 간결할 수 있다.

## Reference

- [Invoke-WebRequest (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-webrequest?view=powershell-7.5)
- [Invoke-RestMethod (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-restmethod?view=powershell-7.5)
