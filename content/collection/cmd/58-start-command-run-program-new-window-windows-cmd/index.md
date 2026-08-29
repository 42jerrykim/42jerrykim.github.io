---
draft: false
slug: start-command-run-program-new-window-windows-cmd
title: "[CMD] 58. start - 새 창에서 프로그램 실행"
description: "start로 프로그램·문서·URL을 새 창에서 실행하는 법과 첫 인용 문자열이 창 제목으로 오인되는 함정, /wait로 완료를 기다리는 법, PATHEXT 확장자 탐색 순서를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 580
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
- start
- 새창실행
- Process
- Batch
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Comparison(비교)
- Education(교육)
- CLI
- Automation(자동화)
- Configuration(설정)
- Workflow(워크플로우)
- Productivity(생산성)
- DevOps
image: "wordcloud.png"
---

start는 프로그램이나 명령을 별도의 새 명령 프롬프트 창에서 실행하는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [57장: schtasks](/post/cmd/schtasks-command-scheduled-tasks-windows-cmd/)에서 예약 작업을 다룬 뒤 이어진다. schtasks가 "미래의 특정 시점"에 실행하는 명령이었다면, start는 "지금 당장" 새 창(또는 비동기)으로 프로그램을 실행하는 명령이다. 01장(cmd)에서 `start cmd /k "..."` 예시로 이미 한 번 등장했던 명령이 이 장의 본격적인 주제다.

**이 장의 깊이**: 입문–중급.

## 사용법

```
start "<제목>" [/d <경로>] [/i] [/min | /max] [/wait] [/b] [<명령> [<인수>...] | <프로그램> [<인수>...]]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `"<제목>"` | 새 명령 프롬프트 창의 제목 표시줄 문자열 |
| `/d <경로>` | 시작 디렉터리 지정 |
| `/i` | 현재 환경 대신 cmd.exe의 시작 시점 환경을 새 창에 전달 |
| `/min` \| `/max` | 최소화·최대화 상태로 시작 |
| `/wait` | 시작한 애플리케이션을 실행하고 종료될 때까지 대기 |
| `/b` | 새 창을 열지 않고 실행(CTRL+C 처리는 애플리케이션이 자체 구현하지 않는 한 무시됨. 중단하려면 CTRL+BREAK) |

## 예시

```
start notepad
start "" /wait myprogram.exe
start /min cmd /k dir
start /d C:\Projects myapp.exe
start "Bing" "https://www.bing.com"
start /max start /?
```

## 주의사항·함정

**첫 따옴표 문자열은 항상 창 제목으로 해석된다**: start의 문법에서 `<"title">`은 첫 번째 매개변수 자리에 고정되어 있다. 그래서 공백이 포함된 프로그램 경로를 따옴표로 감싸 첫 인자로 주면, start는 그것을 실행할 프로그램이 아니라 창 제목으로 오인한다. 이 문제를 피하려면 위 예시처럼 빈 제목 `""`을 항상 맨 앞에 명시적으로 넣는 습관이 필요하다 — `start "" /wait myprogram.exe`가 그 관용구다. 반대로 URL을 열 때는 이 성질을 역이용해, 창 제목에 사람이 알아볼 설명("Bing")을 넣고 그다음 인자로 실제 URL을 준다.

**비실행 파일은 파일 연결로 열린다**: 실행 파일이 아니라 등록된 파일 형식(`.txt`, `.pdf`, URL 등)의 이름을 그대로 넘기면, start는 그 형식에 연결된 프로그램으로 연다. URL은 자동으로 감지되어 기본 브라우저에서 열린다.

**확장자를 생략하면 PATHEXT 순서로 찾는다**: 첫 토큰이 명령도 아니고 확장자가 있는 기존 파일 경로도 아니면, `PATHEXT` 환경 변수에 나열된 순서(`.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC`가 기본값)로 확장자를 붙여가며 찾는다. 07장(path)에서 다룬 `.exe → .com → .bat → .cmd` 순서와 원리는 비슷하지만, start는 PATHEXT라는 별도의 환경 변수를 기준으로 삼는다는 차이가 있다.

**32비트 GUI 애플리케이션은 cmd가 종료를 기다리지 않는다**: 배치 스크립트가 아니라 대화형 프롬프트에서 32비트 GUI 프로그램을 실행하면, cmd는 그 프로그램이 끝날 때까지 기다리지 않고 곧바로 다음 프롬프트를 표시한다. 배치 스크립트 안에서 실행하면 이 동작이 달라질 수 있으므로, 순서를 보장해야 한다면 `/wait`를 명시적으로 지정해야 한다.

**"CMD"로 시작하는 명령은 COMSPEC 값으로 치환된다**: 사용자가 현재 디렉터리에 `cmd`라는 이름의 프로그램을 몰래 놓아두고 그것이 실행되게 하는 것을 막기 위한 보안 장치다. 문자열 CMD가 확장자·경로 없이 첫 토큰으로 오면, 항상 `COMSPEC` 환경 변수가 가리키는 진짜 cmd.exe로 대체된다.

**PowerShell에서는 `Start-Process`가 대응 명령이다**: `Start-Process -FilePath <경로> -ArgumentList <인수>`처럼 실행 파일 경로와 인수가 애초에 분리된 매개변수로 주어지기 때문에, start처럼 "따옴표로 감싼 첫 문자열이 제목인지 경로인지" 헷갈릴 여지가 구조적으로 없다. 다만 `Start-Process`는 새 창의 제목 표시줄 문자열을 직접 지정하는 매개변수를 기본으로 제공하지 않으므로, start의 `"<제목>"` 인자와 똑같은 기능을 원한다면 별도 방법을 찾아야 한다.

## 흔한 오개념

<strong>"start에 따옴표로 감싼 첫 문자열은 항상 실행할 프로그램 경로다"</strong>는 오해가 있다. 실제로는 정반대다 — start 문법에서 첫 번째 자리는 항상 창 제목으로 고정되어 있어서, 공백이 든 프로그램 경로를 따옴표로 감싸 그대로 첫 인자로 주면 start는 그 경로 문자열 전체를 제목으로 취급하고 정작 실행할 프로그램은 찾지 못한다. 그래서 `start "" /wait "C:\Program Files\App\app.exe"`처럼 빈 제목 `""`을 항상 앞에 명시적으로 넣는 것이 관용구가 됐다.

## 다음 장에서는

다음은 59장 — 로컬 또는 원격 컴퓨터를 종료·재시작하는 `shutdown` 명령을 다룬다.

## 평가 기준

- start로 프로그램·문서·URL을 새 창 또는 비동기로 실행할 수 있다.
- 첫 따옴표 문자열이 항상 창 제목으로 해석된다는 함정과, 빈 제목 `""` 관용구가 필요한 이유를 설명할 수 있다.
- start가 확장자를 생략한 명령을 PATHEXT 순서로 찾는다는 것을 안다.
- 32비트 GUI 애플리케이션 실행 시 `/wait`가 왜 필요할 수 있는지 설명할 수 있다.

## 참고

- [start | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/start)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
