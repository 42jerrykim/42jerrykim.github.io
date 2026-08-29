---
draft: false
slug: taskkill-command-terminate-process-windows-cmd
title: "[CMD] 55. taskkill - 프로세스 종료"
description: "taskkill로 PID나 이미지 이름으로 프로세스를 종료하는 법과 /f 강제 종료·/t 자식 프로세스까지 종료하는 옵션, 원격 프로세스는 /f 여부와 무관하게 항상 강제 종료된다는 함정을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 550
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
- taskkill
- 프로세스종료
- Process
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Comparison(비교)
- Linux(리눅스)
- Education(교육)
- CLI
- Security(보안)
- Configuration(설정)
- Workflow(워크플로우)
- Productivity(생산성)
- DevOps
image: "wordcloud.png"
---

taskkill은 하나 이상의 작업(프로세스)을 종료하는 명령이다. 54장(tasklist)으로 확인한 PID나 이미지 이름을 지정해 사용한다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [54장: tasklist](/post/cmd/tasklist-command-list-running-processes-windows-cmd/)에서 실행 중인 프로세스를 조회하는 법을 다룬 뒤 이어진다. tasklist가 "무엇이 실행 중인가"였다면, taskkill은 "그중 무엇을 멈출 것인가"다.

**이 장의 깊이**: 입문–중급.

## 사용법

```
taskkill [/s <컴퓨터> [/u [<도메인>\]<사용자> [/p [<비밀번호>]]]] {[/fi <필터>] [...] [/pid <PID> | /im <이미지이름>]} [/f] [/t]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `/pid <PID>` | 종료할 프로세스 ID |
| `/im <이미지이름>` | 종료할 프로세스의 이미지 이름. 와일드카드(`*`) 지원(필터와 함께일 때만) |
| `/f` | 강제 종료. 원격 프로세스에는 이 옵션과 무관하게 항상 강제 적용됨 |
| `/t` | 지정한 프로세스와 그 자식 프로세스 모두 종료 |
| `/fi <필터>` | 54장과 같은 필터 체계로 대상 선별 |

54장에서 다룬 필터 이름·연산자는 taskkill에도 거의 동일하게 적용된다(STATUS·WINDOWTITLE은 원격 조회에서 지원되지 않는 제약도 동일하다).

## 예시

```
taskkill /im notepad.exe
taskkill /pid 1234 /f
taskkill /im myapp.exe /f /t
taskkill /pid 1230 /pid 1241 /pid 1253
taskkill /f /fi "USERNAME eq NT AUTHORITY\SYSTEM" /im notepad.exe
taskkill /pid 2134 /t /fi "username eq administrator"
taskkill /f /fi "PID ge 1000" /im *
```

## 주의사항·함정

**원격 프로세스는 `/f` 여부와 무관하게 항상 강제 종료된다**: 이 장의 가장 중요한 함정이다.

> "Ending a remote process is always carried out forcefully, regardless whether the **/f** option is specified." — Microsoft Learn, "taskkill"

로컬에서는 `/f` 없이 실행하면 프로세스에 종료 요청만 보내고 응답이 없어도 강제 종료하지 않지만, `/s`로 원격 컴퓨터의 프로세스를 종료할 때는 이 정중한 절차 자체가 없다 — 항상 강제 종료다. 원격 서버에서 taskkill을 실행하기 전에는 로컬보다 더 신중해야 하는 이유다.

**`/im *`는 필터와 함께일 때만 와일드카드로 동작한다**: 이미지 이름에 와일드카드를 쓰려면 반드시 `/fi` 필터를 함께 지정해야 한다. 필터 없이 `taskkill /im *`만 실행하는 것은 지원되지 않는다 — 시스템의 모든 프로세스를 실수로 종료하는 것을 막는 안전장치에 가깝다.

**컴퓨터 이름을 hostname 필터에 넣으면 시스템 전체가 종료될 수 있다**: Microsoft Learn은 특정 필터에 컴퓨터 이름을 잘못 제공하면 그 컴퓨터의 모든 프로세스를 멈추는 셧다운으로 이어질 수 있다고 경고한다. 필터 값에는 정확히 어떤 값이 기대되는지(사용자 이름인지, 이미지 이름인지) 표를 다시 확인하는 습관이 필요하다.

**`/t`로 자식 프로세스까지 종료하되, 필터와 조합하면 조건이 좁아진다**: `/t`는 지정한 프로세스와 그 자식들을 함께 종료하지만, `/fi`로 사용자 조건을 추가하면(위 예시의 `/pid 2134 /t /fi "username eq administrator"`) 그 조건에 맞는 프로세스만 대상이 된다 — 조건에 맞지 않는 자식 프로세스는 그대로 남을 수 있다.

**PowerShell에서는 `Stop-Process`가 대응 명령이다**: `Stop-Process -Name notepad`처럼 이미지 이름으로, 또는 `-Id`로 PID를 지정해 종료한다. `-Force` 매개변수가 taskkill의 `/f`와 대략 대응하지만, 기본 동작(강제 없이 종료를 시도하는 방식)의 세부는 서로 다르므로 스크립트를 그대로 옮겨 쓰기보다는 대상 프로세스가 정상 종료 요청을 어떻게 처리하는지 먼저 확인하는 편이 안전하다.

## 흔한 오개념

<strong>"`taskkill /im notepad.exe`를 실행하면 메모장 창 하나만 닫힌다"</strong>는 오해가 있다. `/im`은 이미지 이름이 일치하는 프로세스를 전부 대상으로 삼는다 — 메모장 창을 세 개 띄워놓고 `taskkill /im notepad.exe`를 실행하면 세 프로세스가 모두 종료된다. 특정 창 하나만 닫고 싶다면 `/im` 대신 tasklist로 확인한 정확한 `/pid` 값을 지정하거나, `/fi` 필터로 대상을 좁혀야 한다.

## 다음 장에서는

다음은 56장 — 백그라운드에서 실행되는 Windows 서비스를 조회·구성하는 `sc` 명령을 다룬다.

## 평가 기준

- taskkill로 PID·이미지 이름·필터를 조합해 프로세스를 종료할 수 있다.
- 원격 프로세스가 `/f` 여부와 무관하게 항상 강제 종료된다는 것을 설명할 수 있다.
- `/im`에 와일드카드를 쓰려면 필터가 함께 필요하다는 제약을 안다.
- `/t`로 자식 프로세스까지 종료할 때 필터 조건이 어떻게 영향을 주는지 설명할 수 있다.

## 참고

- [taskkill | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/taskkill)
- [tasklist | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/tasklist)
