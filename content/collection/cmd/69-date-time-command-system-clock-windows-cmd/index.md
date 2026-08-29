---
draft: false
slug: date-time-command-system-clock-windows-cmd
title: "[CMD] 69. date, time - 시스템 날짜와 시간 표시·설정"
description: "date와 time으로 시스템 날짜·시간을 조회·변경하는 법과 2자리 연도가 80-99는 1980년대로 해석되는 함정, 관리자 권한이 필요한 이유, 배치에서 %date%·%time%을 파일명에 그대로 쓰면 안 되는 이유를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 690
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
- date
- time
- 날짜시간
- Batch
- Documentation(문서화)
- Best-Practices
- Comparison(비교)
- Education(교육)
- CLI
- Troubleshooting(트러블슈팅)
- Configuration(설정)
- Productivity(생산성)
- DevOps
- Administration
- Advanced
image: "wordcloud.png"
---

date와 time은 시스템 날짜와 시간을 표시하거나 설정하는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [68장: wmic](/post/cmd/wmic-command-wmi-query-legacy-windows-cmd/)에서 레거시 조회 도구를 다룬 뒤 이어진다. 지금까지 시스템의 정적인 상태(버전, 드라이버, 정책)를 조회했다면, 이 장은 시간이 지나면서 계속 바뀌는 값을 다룬다.

**이 장의 깊이**: 입문–중급. **중요**: 날짜·시간을 변경하려면 관리자 권한이 필요하다.

## 사용법

```
date [/t | <월-일-년>]
time [/t | <시>[:<분>[:<초>]] [am|pm]]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `/t` | 새 값을 묻지 않고 현재 날짜(또는 시간)만 표시 |
| `<월-일-년>` | 마침표·하이픈·슬래시로 구분한 새 날짜 |
| `<시>[:분[:초]] [am\|pm]` | 새 시간. am/pm 생략 시 24시간제 |

## 예시

```
date
date /t
date 08.03.2027
date 08-03-27
time /t
time 17:30:00
time 5:30 pm
echo %date% %time%
```

## 주의사항·함정

**2자리 연도의 80–99는 1980년대로 해석된다**: 날짜를 2자리 연도로 입력할 때 이 규칙을 모르면 엉뚱한 해로 설정될 수 있다.

> "Be mindful if you use 2 digits to represent the year, the values 80-99 correspond to 1980 through 1999." — Microsoft Learn, "date"

`27`처럼 79 이하 값은 2000년대(2027년)로 해석되어 문제가 없지만, `date 08.03.85`처럼 80 이상 값을 쓰면 2085년이 아니라 1985년으로 해석된다 — 스크립트에서 날짜를 직접 조립할 때는 가능하면 4자리 연도를 쓰는 것이 안전하다.

**`%time%`은 소수점을 포함해 파일명에 그대로 쓰면 문제가 된다**: `%time%`은 밀리초 단위까지 포함한 `HH:MM:SS.mm` 형식을 담고 있어, 콜론과 마침표가 그대로 파일명에 들어가면 Windows 파일 시스템이 허용하지 않는 문자와 충돌한다. 로그 파일 이름 등에 타임스탬프를 넣으려면 콜론·마침표·공백을 다른 문자(밑줄, 하이픈)로 치환하는 처리가 배치 스크립트에서 흔히 필요하다.

**관리자 권한이 필요하다**: date와 time 둘 다 값을 변경하려면 관리자 권한이 필요하다고 Microsoft Learn이 명시한다. 조회(`/t`)만 할 때는 이 제약이 없다.

**형식은 지역 설정에 따라 달라진다**: 날짜 구분자와 월-일-년 순서는 시스템의 지역(로케일) 설정을 따른다. 특정 지역에서 통하던 형식(`MM.DD.YYYY`)이 다른 지역 설정의 시스템에서는 다르게 해석되거나 거부될 수 있다 — 여러 지역의 서버를 대상으로 하는 스크립트라면 이 차이를 염두에 둬야 한다.

**PowerShell 대안은 `Get-Date`·`Set-Date`다**: 현재 날짜·시간을 문자열이 아니라 완전한 DateTime 객체로 읽으려면 `Get-Date`를, 시스템 시간을 변경하려면 `Set-Date`를 쓴다. `Set-Date`도 date·time과 마찬가지로 관리자 권한이 필요하다. 중요한 차이는, `Get-Date`/`Set-Date`가 다루는 DateTime 객체는 연도를 항상 4자리로 유지하므로, 위에서 설명한 2자리 연도의 80–99 세기 추정 같은 모호함 자체가 애초에 발생하지 않는다.

## 흔한 오개념

<strong>"2자리 연도를 입력하면 CMD가 현재 연도에 가장 가까운 세기로 알아서 추정해준다"</strong>는 오해가 있다. 실제로는 79 이하냐 80 이상이냐를 가르는 고정된 규칙(80–99는 무조건 1980년대)일 뿐 "가장 가까운 연도"를 계산하는 것이 아니어서, 예를 들어 `date 08.03.85`는 2085년이 아니라 1985년으로 해석된다.

## 다음 장에서는

다음은 70장 — 콘솔의 활성 코드 페이지를 표시·변경하는 `chcp` 명령을 다룬다.

## 평가 기준

- date·time으로 현재 값을 조회하고 새 값을 설정할 수 있다.
- 2자리 연도의 80–99가 1980년대로 해석되는 함정을 설명할 수 있다.
- `%time%`을 파일명에 그대로 쓰면 안 되는 이유와 일반적인 해결 방법을 안다.
- 날짜·시간 변경에 관리자 권한이 필요하고 형식이 지역 설정에 따라 달라진다는 것을 안다.

## 참고

- [date | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/date)
- [time | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/time)
