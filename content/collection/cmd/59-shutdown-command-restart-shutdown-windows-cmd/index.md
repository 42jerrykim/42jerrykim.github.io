---
draft: false
slug: shutdown-command-restart-shutdown-windows-cmd
title: "[CMD] 59. shutdown - 시스템 종료·재시작·로그오프"
description: "shutdown으로 로컬·원격 컴퓨터를 종료·재시작·로그오프하는 법과 /t 지연 시간 안에 /a로 취소하는 절차, /l이 다른 옵션과 함께 쓸 수 없는 제약, /f 강제 종료 시 데이터 손실 위험을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 590
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
- Advanced
- shutdown
- 시스템종료
- Process
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Comparison(비교)
- Education(교육)
- CLI
- Security(보안)
- Networking(네트워킹)
- Configuration(설정)
- Beginner
- Workflow(워크플로우)
- Productivity(생산성)
image: "wordcloud.png"
---

shutdown은 로컬 또는 원격 컴퓨터를 종료·재시작하는 명령이다. Part 6(프로세스·서비스와 권한 관리) 중 시스템 전체의 생명주기를 다루는 유일한 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [58장: start](/post/cmd/start-command-run-program-new-window-windows-cmd/)에서 프로그램을 새로 실행하는 법을 다룬 뒤 이어진다. start가 무언가를 "시작"했다면, shutdown은 시스템 전체를 "끝내는" 명령이라는 점에서 대비된다.

**이 장의 깊이**: 중급. 시스템을 끄는 명령이므로 주의사항 비중이 크다. **사용자 권한**: 로컬·원격 컴퓨터를 종료하려면 "시스템 종료" 사용자 권한이 필요하다.

## 사용법

```
shutdown [/i | /l | /s | /r | /a | /p | /h | /e] [/f] [/m \\<컴퓨터>] [/t <초>] [/d [p|u:]<주>:<부>] [/c "<메시지>"]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `/i` | 원격 종료 대화상자 표시(다른 모든 옵션 무시, 반드시 첫 매개변수여야 함) |
| `/l` | 즉시 로그오프(다른 매개변수와 함께 쓸 수 없음) |
| `/s` | 컴퓨터 종료 |
| `/r` | 종료 후 재시작 |
| `/a` | 예약된 종료·재시작 취소(대기 시간 중 새 명령 프롬프트에서 별도 실행) |
| `/p` | 로컬 컴퓨터만, 지연 없이 즉시 전원 끔(`/d`나 `/f`와 함께만 사용) |
| `/h` | 최대 절전 모드로 전환 |
| `/f` | 실행 중인 애플리케이션을 경고 없이 강제 종료 |
| `/m \\<컴퓨터>` | 대상 컴퓨터 지정 |
| `/t <초>` | 종료 전 대기 시간(기본 30, 0–315360000). 0보다 크면 `/f`가 자동 적용됨 |
| `/d [p\|u:]<주>:<부>` | 종료 이유 코드(계획됨 p, 사용자 정의 u) |
| `/c "<메시지>"` | 종료 사유 설명(최대 512자) |

## 예시

```
shutdown /s /t 60
shutdown /r /f /t 0
shutdown /a
shutdown /s /m \\server01 /t 0
shutdown /r /t 60 /c "Reconfiguring myapp.exe" /f /d p:4:1
shutdown.exe /s /t 600 /d p:0:0 /e /c "Scheduled maintenance"
```

## 주의사항·함정

**`/t`로 지연을 두면 그 사이 `/a`로 취소할 수 있다**: 즉시 종료(`/t 0`)가 아닌 이상, 지정한 초 동안 카운트다운이 진행되고 그 창은 별도의 새 명령 프롬프트에서 `shutdown /a`를 실행하면 취소된다.

> "Aborts a pending system shutdown. This must be run as a separate command in a new command prompt window during the time-out period (for example, shutdown /a)." — Microsoft Learn, "shutdown"

원격 서버를 재시작하는 예약을 걸어두고 마음이 바뀌었을 때, 카운트다운이 끝나기 전이라면 이 명령으로 되돌릴 수 있다.

**`/l`은 다른 옵션과 절대 함께 쓸 수 없다**: 로그오프는 독립적으로 동작하도록 설계되어 있다.

> "The **/l** parameter works independently and can't be combined with any other parameters. Attempts to combine **/l** with any other parameter is ignored." — Microsoft Learn, "shutdown"

`shutdown /l /f`처럼 다른 옵션을 함께 주면 그 옵션은 조용히 무시된다 — 오류로 알려주지 않는다는 점에 유의해야 한다.

**`/f`는 저장하지 않은 작업을 잃을 수 있다**: 강제 종료는 실행 중인 애플리케이션에 저장할 기회를 주지 않고 닫는다.

> "Caution: Using the **/f** option might result in loss of unsaved data." — Microsoft Learn, "shutdown"

`/t`로 0보다 큰 지연을 지정하면 `/f`가 암묵적으로 함께 적용된다는 점도 함께 기억해야 한다 — 지연 시간을 넉넉히 두었다고 해서 강제 종료가 아니라고 안심할 수 없다.

**원격 종료에는 대상 컴퓨터에 대한 권한이 필요하다**: `/m \\컴퓨터`로 원격 시스템을 대상으로 지정할 때는 그 컴퓨터에서 시스템 종료 권한을 가진 계정으로 인증되어야 한다. 도메인에 참여한 컴퓨터라면 Domain Admins 그룹 구성원이 이 절차를 수행할 수 있다.

**PowerShell에서는 `Restart-Computer`·`Stop-Computer`가 대응 명령이다**: 두 cmdlet 모두 shutdown의 `/m`처럼 `-ComputerName`으로 원격 컴퓨터를 대상으로 지정할 수 있고, 여러 컴퓨터 이름을 배열로 한 번에 넘길 수도 있다. 다만 shutdown의 `/t` 지연이나 `/a` 취소에 해당하는 매개변수는 기본 제공되지 않으므로, 지연 후 취소 가능한 종료가 필요하다면 shutdown.exe를 그대로 호출하거나 별도의 예약·취소 로직을 직접 구성해야 한다.

## 흔한 오개념

<strong>"`/t`로 넉넉하게 지연 시간을 주면 애플리케이션이 저장할 시간을 벌 수 있어 강제 종료를 피할 수 있다"</strong>는 오해가 있다. 실제로는 0보다 큰 `/t` 값을 지정하는 순간 `/f`가 암묵적으로 함께 적용된다 — 즉 카운트다운이 끝나는 시점에는 지연 시간의 길고 짧음과 무관하게 실행 중인 애플리케이션이 저장하지 않은 채로 강제 종료된다. "친절하게 기다려주는 종료"를 기대했다가 지연 시간이 끝나는 순간 저장하지 않은 문서를 잃는 사고가 여기서 나온다.

## 다음 장에서는

다음은 60장 — 파일·디렉터리의 ACL을 표시·수정하는 `icacls` 명령으로 권한 관리 영역이 시작된다.

## 평가 기준

- shutdown으로 로컬·원격 컴퓨터를 종료·재시작·로그오프할 수 있다.
- `/t`로 지연을 두고 `/a`로 취소하는 흐름을 재현할 수 있다.
- `/l`이 다른 옵션과 함께 쓰일 수 없고 조용히 무시된다는 것을 안다.
- `/f`의 데이터 손실 위험과, `/t`가 0보다 크면 `/f`가 암묵적으로 적용된다는 것을 설명할 수 있다.

## 참고

- [shutdown | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/shutdown)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
