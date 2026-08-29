---
draft: false
slug: chcp-command-active-code-page-windows-cmd
title: "[CMD] 70. chcp - 활성 코드 페이지 표시와 변경"
description: "chcp로 콘솔의 활성 코드 페이지를 조회·변경하는 법과 949(한국어)·65001(UTF-8) 설정 시 한글이 여전히 깨지는 이유, chcp 변경 전에 이미 실행 중이던 프로그램에는 반영되지 않는 함정을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 700
categories:
- CMD
tags:
- Windows(윈도우)
- Shell(셸)
- Terminal
- Command
- Guide(가이드)
- Reference(참고)
- Quick-Reference
- How-To
- Tips
- Beginner
- chcp
- 코드페이지
- Encoding
- Documentation(문서화)
- Best-Practices
- Comparison(비교)
- Education(교육)
- CLI
- Troubleshooting(트러블슈팅)
- Internationalization
- Configuration(설정)
- Productivity(생산성)
- DevOps
- Administration
- Advanced
image: "wordcloud.png"
---

chcp는 활성 콘솔 코드 페이지를 변경하는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [69장: date, time](/post/cmd/date-time-command-system-clock-windows-cmd/)에서 시스템 시각을 다룬 뒤 이어진다. 20장(type)에서 "인코딩이 맞지 않으면 한글이 깨질 수 있다"고 예고했던 것이 바로 이 장의 chcp다.

**이 장의 깊이**: 입문–중급.

## 사용법

```
chcp [<nnn>]
```

인수 없이 실행하면 현재 활성 코드 페이지 번호를 표시한다.

## 옵션

`/?` 외에 별도 옵션은 없다.

### 주요 코드 페이지

| 코드 페이지 | 국가·지역·언어 |
|---|---|
| 437 | 미국 |
| 850 | 다국어(라틴 I) |
| 852 | 슬라브어(라틴 II) |
| 855 | 키릴 문자(러시아어) |
| 857 | 터키어 |
| 866 | 러시아어 |
| 936 | 중국어 |

한국어(949)와 UTF-8(65001)은 Microsoft Learn의 공식 지원 코드 페이지 표에는 나오지 않지만, Windows 콘솔에서 널리 쓰이는 값이다.

## 예시

```
chcp
chcp 850
chcp 949
chcp 65001
```

## 주의사항·함정

**Raster 글꼴에서는 OEM 코드 페이지만 정확히 표시된다**: 콘솔 창이 Raster 글꼴을 쓰고 있으면, Windows와 함께 설치된 원래 OEM 코드 페이지만 올바르게 나타난다.

> "Only the original equipment manufacturer (OEM) code page that is installed with Windows appears correctly in a Command Prompt window that uses Raster fonts. Other code pages appear correctly in full-screen mode or in Command Prompt windows that use TrueType fonts." — Microsoft Learn, "chcp"

즉 `chcp 65001`(UTF-8)로 바꿔도 콘솔 글꼴이 여전히 Raster 계열(고정폭 비트맵 글꼴)이면 문자가 깨질 수 있다. Consolas 같은 TrueType 글꼴로 먼저 바꾼 뒤에야 chcp 설정이 실제로 의미를 갖는다.

**chcp 변경 전에 이미 실행 중이던 프로그램에는 반영되지 않는다**: 새 코드 페이지를 지정한 뒤 시작하는 프로그램은 그 코드 페이지를 쓰지만, 이미 실행 중이던 프로그램(cmd.exe 자신은 예외)은 원래 코드 페이지를 계속 쓴다.

> "Programs that you start after you assign a new code page use the new code page. However, programs (except Cmd.exe) that you started before assigning the new code page will continue to use the original code page." — Microsoft Learn, "chcp"

**잘못된 코드 페이지 번호는 즉시 오류로 알려준다**: 지원하지 않는 번호를 지정하면 "Invalid code page" 메시지가 나온다 — 어떤 번호가 유효한지 확신이 없다면 인수 없이 `chcp`를 먼저 실행해 현재 값을 확인하고, 공식 코드 페이지 식별자 문서를 참고하는 것이 안전하다.

**type·echo의 출력 인코딩과 항상 맞춰야 한다**: chcp만 바꾼다고 모든 것이 해결되지는 않는다. 20장(type)에서 파일을 출력할 때, 그 파일 자체의 저장 인코딩과 현재 콘솔의 코드 페이지가 일치해야 문자가 올바르게 보인다 — 둘 중 하나만 맞으면 여전히 깨진 문자가 나올 수 있다.

**PowerShell에서는 `[Console]::OutputEncoding`이 비슷한 역할을 한다**: 이는 cmdlet이 아니라 .NET의 정적 속성으로, PowerShell 프로세스가 텍스트를 어떤 인코딩으로 콘솔에 내보낼지를 제어한다. 다만 chcp가 바꾸는 것은 Windows 콘솔 서브시스템 자체의 활성 코드 페이지인 반면 `[Console]::OutputEncoding`은 PowerShell 프로세스 쪽의 출력 인코딩 설정이라 성격이 다르다 — 둘이 서로 어긋나 한쪽만 맞춰서는 여전히 문자가 깨지는 경우가 있으니, 문제가 생기면 두 값을 함께 확인해 보는 편이 안전하다.

## 흔한 오개념

<strong>"chcp로 코드 페이지만 바꾸면 콘솔에 어떤 글꼴을 쓰든 문자가 제대로 보인다"</strong>는 오해가 있다. 실제로는 콘솔 창이 Raster(비트맵) 글꼴을 쓰고 있으면 OEM 코드 페이지 외에는 올바르게 표시되지 않으므로, TrueType 글꼴로 먼저 바꾸지 않으면 chcp 설정 자체가 무의미해질 수 있다.

## 다음 장에서는

다음은 71장 — Part 7의 마지막 장으로, 콘솔의 전경·배경 색을 설정하는 `color` 명령을 다룬다.

## 평가 기준

- chcp로 활성 코드 페이지를 조회·변경할 수 있다.
- Raster 글꼴에서는 OEM 코드 페이지만 정확히 표시된다는 제약을 설명할 수 있다.
- chcp 변경이 이미 실행 중이던 프로그램에는 반영되지 않는다는 것을 안다.
- 콘솔 코드 페이지와 파일 인코딩이 함께 맞아야 문자가 제대로 보인다는 것을 설명할 수 있다.

## 참고

- [chcp | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/chcp)
- [Code Page Identifiers | Microsoft Learn](https://learn.microsoft.com/en-us/windows/win32/intl/code-page-identifiers)
