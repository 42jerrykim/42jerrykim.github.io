---
draft: false
collection_order: 48
slug: convertto-convertfrom-json-powershell
title: "[PowerShell] 48. ConvertTo-Json/ConvertFrom-Json"
date: 2026-08-29
lastmod: 2026-08-29
description: "ConvertTo-Json으로 객체를 JSON 문자열로 바꾸는 법과 -Depth 기본값 함정, ConvertFrom-Json으로 JSON을 PSCustomObject나 -AsHashtable로 되돌리는 법, REST API 연동에서 두 cmdlet이 하는 역할을 정리한 챕터다."
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
- JSON
- ConvertTo-Json
- ConvertFrom-Json
- REST-API
- Serialization
- Data-Format
image: "wordcloud.png"
---

## 개요

`ConvertTo-Json`/`ConvertFrom-Json`은 PowerShell 객체와 **JSON**(JavaScript Object Notation) 문자열을 상호 변환하는 cmdlet 쌍이다. 27장에서 만든 `[PSCustomObject]`나 44장의 해시테이블을 파일로 저장하거나 웹 API로 주고받으려면, 결국 이 두 cmdlet을 거쳐 텍스트 형태로 직렬화(serialize)·역직렬화(deserialize)해야 한다.

정신 모델은 "`ConvertTo-Json`은 메모리 안의 객체 트리를 사람도 읽을 수 있는 텍스트로 평평하게 펼치고, `ConvertFrom-Json`은 그 텍스트를 다시 객체 트리로 복원한다"는 것이다. 이 왕복 변환이 정확히 대칭이 되려면 뒤에서 설명할 `-Depth`, `-AsHashtable` 같은 매개변수를 신경 써야 한다.

## 사용법

```powershell
ConvertTo-Json [-InputObject] <Object> [-Depth <Int32>] [-Compress] [-AsArray] [-EnumsAsStrings]
ConvertFrom-Json [-InputObject] <String> [-AsHashtable] [-Depth <Int32>] [-NoEnumerate]
```

## 매개변수

| 매개변수 | 대상 | 설명 |
|---|---|---|
| `-Depth` | 둘 다 | 중첩 객체를 몇 단계까지 직렬화·역직렬화할지(`ConvertTo-Json` 기본값 2, `ConvertFrom-Json` 기본값 1024) |
| `-Compress` | ConvertTo-Json | 들여쓰기·줄바꿈 없이 한 줄로 압축 출력 |
| `-AsArray` | ConvertTo-Json | 요소가 하나뿐이어도 항상 JSON 배열(`[...]`)로 감싸기 |
| `-EnumsAsStrings` | ConvertTo-Json | 열거형(enum) 값을 숫자가 아니라 이름 문자열로 출력 |
| `-AsHashtable` | ConvertFrom-Json | `PSCustomObject` 대신 해시테이블(44장)로 반환, 대소문자만 다른 중복 키 등 예외 상황 회피 |
| `-NoEnumerate` | ConvertFrom-Json | 배열을 파이프라인에 낱개로 풀어내지 않고 하나의 배열 객체로 유지 |

## 예시

```powershell
$user = [PSCustomObject]@{
    Name = "jsmith"
    Age  = 30
    Roles = @("Admin", "User")
}
$json = $user | ConvertTo-Json          # 객체 → JSON 문자열
$json
$json | ConvertFrom-Json                 # JSON 문자열 → PSCustomObject로 복원

Get-Process | Select-Object Name, Id, CPU -First 3 | ConvertTo-Json -Compress   # 한 줄로 압축

'{ "key":"value1", "Key":"value2" }' | ConvertFrom-Json -AsHashtable   # 대소문자만 다른 키 처리

Get-Content -Raw config.json | ConvertFrom-Json                        # 파일에서 읽어 변환(37장)

# 깊이 3단계 이상 중첩된 객체는 기본값으로 잘릴 수 있다
$deep = @{ a = @{ b = @{ c = @{ d = "너무 깊음" } } } }
$deep | ConvertTo-Json -Depth 4          # -Depth를 명시적으로 늘려야 끝까지 직렬화됨

# REST API 호출 시 전형적인 조합(16부에서 Invoke-RestMethod와 함께 다시 등장)
$body = @{ name = "test"; value = 123 } | ConvertTo-Json
```

## 주의사항·함정

**`-Depth`의 기본값이 얕아서, 3단계 이상 중첩된 객체는 조용히 잘린다**: `ConvertTo-Json`의 `-Depth` 기본값은 2다. 해시테이블 안에 해시테이블을 여러 겹 넣은 복잡한 설정 구조를 그대로 직렬화하면, 일부 하위 수준이 `"System.Collections.Hashtable"` 같은 타입 이름 문자열로 뭉개져 출력된다. 오류 없이 조용히 정보가 손실되므로, 중첩 구조를 다룰 때는 항상 `-Depth`를 필요한 만큼 명시적으로 늘려야 한다.

**`ConvertFrom-Json`의 기본 출력은 파이프라인으로 배열을 풀어 흘려보낸다**: JSON 배열이 요소를 하나만 담고 있으면, 기본 동작상 `ConvertFrom-Json | ConvertTo-Json`으로 왕복했을 때 배열이 아니라 단일 값으로 바뀌어 버린다. 배열 구조 자체를 정확히 보존해야 하는 라운드트립 작업이라면 `-NoEnumerate`가 필요하다.

**대소문자만 다른 키가 있는 JSON은 기본 변환에서 예외가 날 수 있다**: `PSCustomObject`는 속성 이름의 대소문자를 구분하지 않으므로, `{"key":"a", "Key":"b"}`처럼 대소문자만 다른 두 키가 있는 JSON은 기본 `ConvertFrom-Json`에서 오류를 일으키거나 마지막 키만 남는다. 이런 데이터를 다뤄야 한다면 `-AsHashtable`을 쓰는 것이 안전하다.

**이식성**: Bash/CMD에는 JSON을 다루는 내장 문법이 없어 `jq` 같은 외부 도구에 의존해야 한다. PowerShell은 객체 파이프라인(10장)의 자연스러운 연장으로 JSON 직렬화가 코어 cmdlet에 내장돼 있다는 점이 근본적으로 다르다 — 이는 `Invoke-RestMethod`(16부)가 웹 API 응답을 자동으로 객체로 파싱해 주는 것과 같은 설계 철학이다.

## Reference

- [ConvertTo-Json (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/convertto-json)
- [ConvertFrom-Json (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/convertfrom-json)
