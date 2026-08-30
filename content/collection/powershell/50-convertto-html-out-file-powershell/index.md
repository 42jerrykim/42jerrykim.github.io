---
draft: false
collection_order: 50
slug: convertto-html-out-file-powershell
title: "[PowerShell] 50. ConvertTo-Html과 Out-File"
date: 2026-08-29
lastmod: 2026-08-29
description: "ConvertTo-Html로 객체를 HTML 표·목록으로 바꾸는 법과 -Property/-CssUri/-Fragment 매개변수, Out-File로 화면 서식 그대로 파일에 저장하는 법과 리다이렉션 연산자(>)와의 관계를 정리한 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- Scripting(스크립팅)
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
- ConvertTo-Html
- Out-File
- Redirection
- HTML-Report
- Encoding
- Report-Generation
image: "wordcloud.png"
---

## 개요

`ConvertTo-Html`은 객체를 웹 브라우저로 볼 수 있는 HTML 표·목록으로 바꾸는 cmdlet이고, `Out-File`은 화면에 보이는 것과 같은 서식으로 결과를 파일에 저장하는 cmdlet이다. 둘 다 "PowerShell 안의 결과를 파일로 남긴다"는 공통 목적을 가지지만, `ConvertTo-Html`은 사람이 브라우저로 보기 좋은 보고서를, `Out-File`은 콘솔 화면을 그대로 복사한 텍스트 로그를 만든다는 점이 다르다.

정신 모델은 "`ConvertTo-Html`은 9장에서 배운 `Format-Table`/`Format-List`의 HTML 버전이고, `Out-File`은 리다이렉션 연산자 `>`의 cmdlet 버전"이라는 것이다. 두 cmdlet은 자주 짝을 이뤄 쓰인다 — `ConvertTo-Html`이 만든 문자열은 그 자체로는 화면에 표시될 뿐이므로, 실제로 파일이나 이메일 첨부로 남기려면 결국 `Out-File`(또는 `Set-Content`)로 디스크에 써야 하기 때문이다.

## 사용법

```powershell
ConvertTo-Html [-Property <Object[]>] [-Title <String>] [-CssUri <Uri>] [-As <String>] [-Fragment]
Out-File [-FilePath] <String> [-Encoding <Encoding>] [-Append] [-Width <Int32>] [-NoClobber]
```

## 매개변수

| 매개변수 | 대상 | 설명 |
|---|---|---|
| `-Property` | ConvertTo-Html | 포함할 속성 선택(13장 `Select-Object`와 유사한 역할) |
| `-Title` | ConvertTo-Html | `<title>` 태그 내용 |
| `-CssUri` | ConvertTo-Html | 외부 스타일시트 링크 삽입 |
| `-As` | ConvertTo-Html | `Table`(기본) 또는 `List` 형식 |
| `-Fragment` | ConvertTo-Html | `<html>`/`<head>`/`<body>` 없이 `<table>` 부분만 반환(기존 웹페이지에 끼워 넣을 때) |
| `-PreContent`/`-PostContent` | ConvertTo-Html | 표 앞뒤에 추가할 텍스트(설명, 생성 시각 등) |
| `-Encoding` | Out-File | 파일 인코딩(기본 `utf8NoBOM`, 37장과 동일한 함정) |
| `-Append` | Out-File | 기존 파일 끝에 추가 |
| `-Width` | Out-File | 한 줄 최대 문자 수(기본은 호스트 창 너비, 넘으면 잘림) |
| `-NoClobber` | Out-File | 기존 파일이 있으면 실패시켜 덮어쓰기 방지 |

## 예시

```powershell
Get-Service | ConvertTo-Html | Out-File services.htm
Invoke-Item services.htm                                     # 기본 브라우저로 열기

Get-Process | ConvertTo-Html -Property Name, Path, Company -Title "Process Report" |
    Out-File proc.htm

Get-Service | ConvertTo-Html -As List | Out-File services-list.htm    # 목록 형식

Get-Date | ConvertTo-Html -Fragment                            # <table> 태그만 반환(다른 HTML에 삽입용)

$htmlParams = @{
    Title       = "Windows Services"
    PreContent  = "<p>자동 생성된 보고서</p>"
    PostContent = "문의: IT팀"
}
Get-Service A* | ConvertTo-Html @htmlParams | Out-File services.htm  # 25장 스플래팅 재활용

Get-Process | Out-File -FilePath process.txt -Width 200         # 넓은 표가 잘리지 않도록 너비 지정
Get-ChildItem Env:\ > env.txt                                    # > 연산자는 Out-File과 동등
Get-Process | Out-File -FilePath process.txt -NoClobber          # 기존 파일 보호
```

## 주의사항·함정

**`Out-File`은 화면 서식을 그대로 저장하므로 다시 파싱하기 어렵다**: `Out-File`이 저장하는 내용은 콘솔에 표시되는 그대로의 텍스트 표현이라, 나중에 그 파일을 다시 읽어 프로그램적으로 처리하려면 정규식(47장)으로 힘겹게 파싱해야 한다. 데이터를 다시 읽어 쓸 목적이라면 처음부터 `Export-Csv`(49장)나 `ConvertTo-Json`(48장)을 쓰는 편이 훨씬 안전하다 — `Out-File`은 어디까지나 "사람이 읽을 로그·리포트"용이다.

**`ConvertTo-Html`에 여러 객체를 `-InputObject`로 한 번에 넘기면 예상과 다른 표가 나온다**: `Get-Service | ConvertTo-Html`처럼 파이프라인으로 넘기면 서비스마다 한 행씩 표가 만들어지지만, `ConvertTo-Html -InputObject (Get-Service)`처럼 배열 전체를 매개변수로 넘기면 "배열 객체 자체의 속성"을 표시하는 표가 만들어져 원하는 결과가 나오지 않는다. 여러 객체를 나열하려면 파이프라인을 쓰는 것이 기본이다.

**Windows PowerShell 5.1과 PowerShell 7의 `-Encoding` 기본값 차이는 `Out-File`에도 그대로 적용된다**: 37장에서 언급한 인코딩 기본값 변화(PowerShell 6부터 `utf8NoBOM`)가 `Out-File`에도 동일하게 적용되므로, 두 버전을 오가며 한글이 포함된 리포트를 다루면 인코딩이 깨질 수 있다.

**이식성**: CMD·Bash에는 객체를 HTML로 바로 직렬화하는 내장 기능이 없어 별도 스크립트나 도구가 필요하다. `Out-File`은 개념적으로 셸 리다이렉션(`>`, `>>`)과 거의 동일하며, PowerShell에서는 실제로 `>`가 내부적으로 `Out-File`을 호출하는 문법 설탕(syntactic sugar)이다.

## Reference

- [ConvertTo-Html (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/convertto-html)
- [Out-File (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/out-file)
