---
draft: false
collection_order: 114
slug: new-guid-get-random-utility-powershell
title: "[PowerShell] 114. New-Guid/Get-Random — 유틸리티 모음"
date: 2026-08-29
lastmod: 2026-08-29
description: "고유 식별자를 생성하는 New-Guid와 난수·무작위 선택을 담당하는 Get-Random을 함께 정리한 Part 16 마지막 챕터로, -Minimum/-Maximum/-InputObject/-Shuffle/-SetSeed 사용법을 다룬다."
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
- New-Guid
- Get-Random
- GUID
- UUID
- Random-Number
- Testing(테스트)
- Unique-Identifier
image: "wordcloud.png"
---

## 개요

<strong>New-Guid</strong>와 <strong>Get-Random</strong>은 서로 다른 문제를 풀지만 둘 다 "값을 만들어내는" 유틸리티 cmdlet이라는 공통점으로 Part 16(네트워크와 웹)을 마무리하는 이 장에 함께 묶었다. 98장에서 환경 변수와 드라이브를 한 챕터로 묶었던 것과 같은 방식이다 — 네트워크 자체를 다루지는 않지만, API 요청 본문에 고유 ID를 채우거나(113장과 조합) 테스트 데이터를 무작위로 생성하는 등 스크립팅 전반에서 반복적으로 필요한 두 도구다.

정신 모델은 "`New-Guid`는 '전 세계 어디서도 겹치지 않을 이름표를 하나 뽑는 기계'이고, `Get-Random`은 '주사위를 굴리거나 상자에서 카드를 뽑는 기계'"라는 것이다. 전자는 고유성이 핵심이고, 후자는 무작위성이 핵심이다.

두 cmdlet은 겉보기엔 단순해 보이지만, 테스트 데이터 생성이나 API 요청 식별자 부여처럼 자동화 스크립트 전반에서 은근히 자주 등장하는 반복 작업을 표준화해 준다는 공통점이 있다. 이런 유틸리티 cmdlet을 매번 `.NET` 클래스를 직접 호출해 재구현하는 대신, 이미 검증된 표준 cmdlet으로 처리하면 스크립트의 가독성과 일관성이 함께 올라간다.

## 사용법

```powershell
New-Guid [-Empty] [-InputObject <문자열>]
Get-Random [-Minimum <값>] [-Maximum <값>] [-InputObject <컬렉션>] [-Count <n>]
```

## 종류

| cmdlet | 매개변수 | 동작 |
|---|---|---|
| `New-Guid` | (없음) | 무작위 버전 4 GUID 생성 |
| `New-Guid` | `-Empty` | 전부 0인 빈 GUID(`00000000-...`) 생성 |
| `New-Guid` | `-InputObject <문자열>` | 문자열을 GUID 객체로 변환(파이프라인 입력도 가능) |
| `Get-Random` | (없음) | `0`–`Int32.MaxValue` 범위의 정수 무작위 반환 |
| `Get-Random` | `-Minimum`/`-Maximum` | 지정 범위(최댓값 미포함) 내 무작위 정수·실수 반환 |
| `Get-Random` | `-InputObject` + `-Count` | 컬렉션에서 무작위로 n개 선택(중복 없음) |
| `Get-Random` | `-Shuffle`(PS 7.1+) | 컬렉션 전체를 무작위 순서로 재배열해 반환 |
| `Get-Random` | `-SetSeed` | 재현 가능한 의사난수 시퀀스로 고정(디버깅용) |

## 예시

```powershell
New-Guid                                                            # 무작위 GUID 하나 생성

New-Guid -Empty                                                     # 00000000-0000-0000-0000-000000000000

$id = [guid]::NewGuid().ToString()                                   # .NET을 직접 호출하는 것과 동일한 결과(114장 방식이 더 PowerShell다움)

$body = @{ id = (New-Guid); name = "test" } | ConvertTo-Json         # 113장 REST API 요청 본문에 고유 ID 채우기

Get-Random -Maximum 100                                             # 0~99 사이 무작위 정수

Get-Random -Minimum -100 -Maximum 100                                # 음수 포함 범위 지정

1, 2, 3, 5, 8, 13 | Get-Random                                        # 배열에서 무작위로 1개 선택

1, 2, 3, 5, 8, 13 | Get-Random -Count 3                                # 배열에서 무작위로 3개 선택(순서도 무작위, 중복 없음)

1, 2, 3, 5, 8, 13 | Get-Random -Shuffle                                # 컬렉션 전체를 무작위로 뒤섞어 반환(PS 7.1+)

Get-Random -Maximum 100 -SetSeed 23                                  # 시드 고정 — 같은 시드면 항상 같은 값(디버깅·테스트 재현용)

$Files = Get-ChildItem -Path C:\* -Recurse                            # 89장 방식으로 파일 목록 수집
$Sample = $Files | Get-Random -Count 50                                # 그중 무작위로 50개 표본 추출
```

## 주의사항·함정

**`Get-Random`은 암호학적으로 안전한 난수를 보장하지 않는다**: 내부적으로 의사난수 생성기(PRNG)를 쓰기 때문에, 토큰·비밀번호·암호화 키처럼 보안이 걸린 값을 만드는 데 `Get-Random`을 쓰면 안 된다. PowerShell 7.4부터 추가된 `Get-SecureRandom`이 암호학적으로 안전한 난수를 제공하므로, 보안이 중요한 상황에서는 이를 대신 사용해야 한다. 100장에서 다룬 `SecureString`처럼 보안이 걸린 값을 다룰 때는 "무작위처럼 보이는가"가 아니라 "예측 불가능함이 수학적으로 증명됐는가"를 기준으로 도구를 골라야 한다.

**`-SetSeed`는 한 번 설정하면 세션이 끝날 때까지 그 세션의 모든 `Get-Random` 호출에 영향을 준다**: 되돌릴 수 있는 기본값이 따로 없어서, 디버깅을 위해 시드를 고정했다가 잊어버리면 이후 스크립트의 "무작위" 값이 실제로는 예측 가능한 값이 되어버린다. 재현이 끝났으면 새 PowerShell 세션을 시작해 시드를 초기화하는 것이 안전하다.

**`-Maximum`은 그 값을 포함하지 않는다**: `Get-Random -Maximum 100`은 0부터 99까지만 반환하고 100은 나오지 않는다. 1부터 100까지를 원한다면 `-Minimum 1 -Maximum 101`처럼 범위를 한 칸 넓혀야 하며, 이 "미포함" 규칙을 놓치면 경계값에서 오프바이원 오류가 생긴다.

**`New-Guid`가 만드는 GUID는 전역적으로 유일함을 통계적으로 보장할 뿐, 절대적 보장이 아니다**: 버전 4 GUID는 128비트 무작위 값이라 실질적으로 충돌 가능성이 무시할 수 있는 수준이지만, 데이터베이스의 기본 키처럼 정말로 절대 겹치지 않아야 하는 경우라도 이 통계적 성격 자체를 이해하고 쓰는 것이 좋다. 충돌 확률이 사실상 0에 가깝다는 것과 수학적으로 절대 0이라는 것은 다른 이야기이므로, 규제가 엄격한 금융·의료 시스템의 식별자 설계에서는 이 차이를 명시적으로 문서화해 두는 편이 나중의 논쟁을 줄여준다.

**이식성**: 이 두 cmdlet은 플랫폼 종속적인 API가 아니라 .NET 표준 라이브러리 위에 얇게 얹힌 래퍼이므로, PowerShell 7 기준으로는 Windows·Linux·macOS 어디에서나 동일하게 동작한다는 점이 앞선 여러 장의 Windows 전용 cmdlet들과 다르다. Linux/macOS의 `uuidgen` 명령이 `New-Guid`와 정확히 대응하고, Bash의 `$RANDOM` 변수나 `shuf` 명령이 `Get-Random`과 개념적으로 유사하다. 다만 `$RANDOM`은 0–32767 범위의 정수만 반환하는 반면 `Get-Random`은 `-Minimum`/`-Maximum`으로 임의 범위와 실수까지 다룰 수 있고, 컬렉션에서 직접 무작위 표본을 뽑는 `-Count`·`-Shuffle` 기능까지 통합돼 있어 셸 내장 기능보다 표현력이 넓다.

## Reference

- [New-Guid (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/new-guid?view=powershell-7.5)
- [Get-Random (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/get-random?view=powershell-7.5)
