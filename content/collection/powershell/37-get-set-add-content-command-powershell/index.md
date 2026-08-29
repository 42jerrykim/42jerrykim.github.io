---
draft: true
collection_order: 37
slug: get-set-add-content-command-powershell
title: "[PowerShell] 37. Get-Content/Set-Content/Add-Content"
date: 2026-08-29
lastmod: 2026-08-29
description: "Get-Content로 파일 내용을 줄 배열로 읽는 법과 -Raw/-Tail/-Wait 매개변수, Set-Content(덮어쓰기)와 Add-Content(추가)의 차이, -NoNewline·인코딩 매개변수를 정리한 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- File-System
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
- Get-Content
- Set-Content
- Add-Content
- Log-Tailing
- Text-Encoding
- Export-Clixml
image: "wordcloud.png"
---

## 개요

이 세 cmdlet은 파일(또는 다른 프로바이더 항목)의 내용을 읽고 쓰는 기본 도구다. `Get-Content`는 내용을 읽고, `Set-Content`는 기존 내용을 지우고 새로 쓰며, `Add-Content`는 기존 내용 뒤에 이어 붙인다. 세 cmdlet 모두 문자열 처리에 특화되어 있어, 객체를 그대로 저장하고 싶다면(19부에서 다룰) `Export-Clixml`이나 `Out-File`을 대신 검토해야 한다.

세 cmdlet의 역할 분담은 30장에서 다룬 프로바이더 개념과 그대로 이어진다 — `Get-ChildItem`이 어떤 프로바이더에서든 목록을 조회하는 창구였듯, 이 셋은 어떤 프로바이더에서든 "내용"이라는 개념을 다루는 공통 창구다. FileSystem 드라이브에서는 파일 텍스트가, `Function:` 드라이브에서는 함수 본문이 "내용"에 해당한다.

## 사용법

```powershell
Get-Content [-Path] <String[]> [-Raw] [-Tail <Int32>] [-TotalCount <Int64>] [-Wait] [-Encoding <Encoding>]
Set-Content [-Path] <String[]> [-Value] <Object[]> [-NoNewline] [-Encoding <Encoding>]
Add-Content [-Path] <String[]> [-Value] <Object[]> [-NoNewline] [-Encoding <Encoding>]
```

## 매개변수

| 매개변수 | 대상 | 설명 |
|---|---|---|
| `-Raw` | Get-Content | 줄 배열이 아니라 파일 전체를 줄바꿈이 보존된 문자열 하나로 반환 |
| `-Tail`(별칭 `-Last`) | Get-Content | 파일 끝에서부터 지정한 줄 수만 읽는다(전체를 변수에 담아 `[-1]`로 접근하는 것보다 빠르다) |
| `-TotalCount`(별칭 `-First`/`-Head`) | Get-Content | 파일 앞에서부터 지정한 줄 수만 읽는다 |
| `-Wait` | Get-Content | 파일을 계속 열어 두고 초당 한 번씩 새 줄이 추가됐는지 확인(로그 실시간 확인, `-Raw`와 병용 불가) |
| `-Delimiter` | Get-Content | 줄바꿈 대신 다른 구분자로 항목을 나눈다(FileSystem 전용) |
| `-Value` | Set-Content, Add-Content | 쓸(또는 추가할) 내용 |
| `-NoNewline` | Set-Content, Add-Content | 항목 사이·마지막에 줄바꿈을 넣지 않는다 |
| `-Encoding` | 셋 다 | 파일 인코딩(기본 `utf8NoBOM`) |
| `-AsByteStream` | Get-Content, Set-Content, Add-Content | 바이트 스트림으로 읽거나 쓴다(이진 파일 처리, `-Raw`와 함께 쓰면 `[byte[]]` 하나로 반환) |

## 예시

```powershell
Get-Content -Path .\LineNumbers.txt                     # 줄 배열로 읽기
Get-Content -Path .\LineNumbers.txt -Raw                 # 하나의 문자열로(줄바꿈 보존)
Get-Content -Path .\LineNumbers.txt -Tail 1               # 마지막 줄만(빠름)
Get-Content -Path .\app.log -Wait -Tail 10                # tail -f처럼 실시간 확인

Set-Content -Path .\Test*.txt -Value 'Hello, World'        # 여러 파일 내용 한 번에 덮어쓰기
Add-Content -Path .\LineNumbers.txt -Value "This is line $_."   # 한 줄 추가

# 파일 내용을 가공해 같은 파일에 다시 쓰기
(Get-Content -Path .\Notice.txt) |
    ForEach-Object { $_ -replace 'Warning', 'Caution' } |
    Set-Content -Path .\Notice.txt

# 이진 파일을 바이트 배열로 읽고 그대로 쓰기
$bytes = Get-Content -Path C:\temp\test.bin -AsByteStream -Raw
Set-Content -Path C:\temp\copy.bin -Value $bytes -AsByteStream
```

## 주의사항·함정

**기본 반환값은 배열이지, 하나의 문자열이 아니다**: `Get-Content`는 줄마다 잘라 배열로 반환하므로, `.Length`나 `.Contains()` 같은 문자열 메서드를 파일 전체에 바로 적용하면 예상과 다르게 동작한다. 파일 전체를 하나의 문자열로 다루고 싶다면 반드시 `-Raw`를 붙여야 한다.

**같은 파일을 읽으면서 동시에 쓸 수는 없다**: `Get-Content .\a.txt | Set-Content .\a.txt`처럼 파일을 읽는 도중 같은 파일에 쓰려고 하면 오류가 나거나 내용이 손상될 수 있다. 파이프라인은 10장에서 봤듯 객체를 한 번에 하나씩 흘려보내는데, `Set-Content`가 파일을 열어 쓰기 시작하는 시점에 `Get-Content`가 아직 같은 파일을 읽는 중이면 두 작업이 충돌한다. 예시처럼 `Get-Content`를 괄호로 감싸 먼저 전체를 읽어들여 파이프라인을 완료시킨 뒤, 그 결과를 다시 `Set-Content`로 써야 안전하다.

**`Set-Content`는 문자열 처리 전용이다**: 문자열이 아닌 객체를 `Set-Content`에 넘기면 각 객체를 문자열로 변환(대개 기본 표시 형식)해 저장한다. 나중에 원래 객체로 정확히 복원해야 한다면 `Set-Content` 대신 `Export-Clixml`을 써야 한다.

**인코딩 기본값 변화에 유의한다**: PowerShell 6부터 `-Encoding`의 기본값이 `utf8NoBOM`으로 바뀌었다(Windows PowerShell 5.1은 지역별 기본 인코딩을 썼다). 같은 스크립트를 Windows PowerShell 5.1과 PowerShell 7 양쪽에서 돌려야 한다면, 파일을 쓰는 쪽과 읽는 쪽의 기본 인코딩이 서로 달라 한글 등 비ASCII 문자가 깨질 수 있다. 크로스플랫폼 스크립트나 다른 도구와 파일을 주고받을 때는 양쪽 모두 `-Encoding`을 명시하는 편이 안전하다.

**이식성**: CMD의 `type`(읽기)·리다이렉션(`>`/`>>`), Bash의 `cat`(읽기)·`>`/`>>`(쓰기/추가)에 각각 대응한다. Bash의 `tail -f`가 `Get-Content -Wait -Tail`과 정확히 같은 역할을 한다.

## Reference

- [Get-Content (Microsoft.PowerShell.Management) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-content)
- [Set-Content (Microsoft.PowerShell.Management) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/set-content)
- [Add-Content (Microsoft.PowerShell.Management) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/add-content)
