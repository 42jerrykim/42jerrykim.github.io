---
draft: false
collection_order: 17
slug: measure-object-command-aggregate-statistics-powershell
title: "[PowerShell] 17. Measure-Object — 집계·통계"
date: 2026-08-29
lastmod: 2026-08-29
description: "Measure-Object로 파이프라인 객체 개수를 세거나 Sum/Average/Maximum/Minimum/StandardDeviation을 계산하는 법, 텍스트 객체의 -Line/-Word/-Character 집계 모드 차이를 정리한 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
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
- Data-Analysis
- Measure-Object
- Statistics
- Aggregation
- Get-ChildItem
- Data-Science(데이터사이언스)
- Word-Count
image: "wordcloud.png"
---

## 개요

`Measure-Object`는 객체의 개수를 세거나, 숫자 속성의 합계·평균·최댓값·최솟값·표준편차를 계산하는 cmdlet이다. 매개변수 없이 실행하면 단순히 파이프라인을 지나간 객체 개수(`Count`)만 알려주며, 이는 `wc -l`처럼 "일단 몇 개인지"를 확인하는 가장 기본적인 용도다.

정신 모델은 두 가지 서로 다른 집계 대상으로 나뉜다는 것이다 — 숫자 속성에 대한 통계(`-Sum`, `-Average`, `-Maximum`, `-Minimum`, `-StandardDeviation`)와, 문자열 객체에 대한 텍스트 집계(`-Line`, `-Word`, `-Character`)는 서로 다른 매개변수 세트(파라미터 셋)에 속해 있어 섞어 쓸 수 없다.

## 사용법

```powershell
# 숫자 속성 집계
Measure-Object [[-Property] <PSPropertyExpression[]>] [-Sum] [-Average] [-Maximum] [-Minimum] [-StandardDeviation] [-AllStats]

# 텍스트 집계
Measure-Object [-Line] [-Word] [-Character] [-IgnoreWhiteSpace]
```

## 매개변수

| 매개변수 | 설명 |
|---|---|
| `-Property` | 집계할 속성(들). 계산된 속성(스크립트블록)도 가능하고, PowerShell 6+부터 와일드카드도 지원한다 |
| `-Sum` / `-Average` | 지정한 속성 값의 합계·평균 |
| `-Maximum` / `-Minimum` | 최댓값·최솟값 |
| `-StandardDeviation` | 표준편차(PowerShell 6+) — 값이 클수록 데이터가 평균에서 넓게 퍼져 있다는 뜻이다 |
| `-AllStats` | 위 통계를 한 번에 모두 계산(PowerShell 6+) |
| `-Line` / `-Word` / `-Character` | 문자열 입력의 줄·단어·문자 수를 센다(서로 조합 가능) |
| `-IgnoreWhiteSpace` | 문자 수를 셀 때 공백을 제외한다 |

## 예시

```powershell
Get-ChildItem | Measure-Object                                          # 파일·폴더 개수
Get-ChildItem -File | Measure-Object -Property Length -Minimum -Maximum -Sum -Average
Get-Content C:\Temp\tmp.txt | Measure-Object -Character -Line -Word     # 텍스트 파일 통계
1..5 | Measure-Object -AllStats                                          # 합계·평균·표준편차 등 한 번에
Get-Process | Measure-Object -Average -StandardDeviation CPU             # CPU 사용 편차 확인
Get-ChildItem | Measure-Object -Sum { $_.Length / 1MB }                  # 계산된 속성으로 합계(MB 단위)
Get-Process | Measure-Object -Maximum *paged*memory*size                 # 와일드카드로 여러 속성 한 번에 집계
```

## 주의사항·함정

**두 매개변수 세트를 섞으면 오류가 난다**: `-Sum`과 `-Line`을 동시에 쓸 수 없다. 숫자 통계를 낼지, 텍스트 줄·단어·문자를 셀지 먼저 정해야 한다.

**속성을 지정하지 않으면 개수만 나온다**: `-Property` 없이 `-Sum`/`-Average` 등을 쓰면 계산할 대상이 없어 결과가 비어 있다. 반드시 속성을 함께 지정해야 한다.

**PowerShell 7.3부터 속성이 없는 객체를 조용히 건너뛴다**: 이전 버전에서는 지정한 속성이 없는 객체를 만나면 오류가 났지만, 7.3부터는 `StrictMode`가 아닌 한 그냥 건너뛴다. 배치 스크립트에서 이 동작 변화가 결과에 영향을 줄 수 있다는 점을 염두에 두어야 한다.

**이식성**: `Get-Content file.txt | Measure-Object -Line -Word -Character`는 Bash의 `wc -l -w -c`와 거의 같은 결과를 주지만, PowerShell 쪽은 숫자 속성에 대한 통계 집계까지 같은 cmdlet 하나로 처리한다는 점에서 범위가 더 넓다 — Bash에서 숫자 합계를 내려면 `awk '{sum+=$1} END {print sum}'`처럼 별도 도구가 필요하다.

## Reference

- [Measure-Object (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/measure-object)
