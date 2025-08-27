---
title: "[Windows] Windows 11 RDP 작업표시줄 오류 해결"
description: "Windows 에서 MSTSC 원격 접속/해제 후 작업 표시줄 아이콘 불일치, 작업표시줄 미표시 문제를 즉시 복구하고, RDP 이벤트 기반 Explorer 자동 재시작으로 재발을 방지하는 안전한 자동화 가이드를 제공합니다."
date: 2025-08-27
lastmod: 2025-08-27
categories:
- "Windows"
- "Troubleshooting"
tags:
- "windows-11"
- "mstsc"
- "rdp"
- "remote-desktop"
- "taskbar"
- "explorer"
- "icon-cache"
- "tray-icons"
- "rdp-event-logs"
- "localsessionmanager"
- "terminalservices"
- "operational-log"
- "event-id-24"
- "event-id-25"
- "1149"
- "automation"
- "scheduled-tasks"
- "powershell"
- "cmd"
- "shell"
- "windows-update"
- "graphics-driver"
- "resolution"
- "display-scale"
- "rpc"
- "lsm"
- "event-log"
- "logging"
- "monitoring"
- "remediation"
- "workaround"
- "bug"
- "fix"
- "best-practices"
- "enterprise"
- "policy"
- "security"
- "admin"
- "it-ops"
- "한국어"
- "가이드"
- "윈도우11"
- "원격데스크톱"
- "작업표시줄"
- "아이콘불일치"
- "아이콘캐시"
- "트레이아이콘"
- "자동화"
- "이벤트"
- "재시작"
- "탐색기"
- "재연결"
- "연결끊김"
- "콘솔로그온"
- "해상도"
- "스케일링"
- "드라이버"
- "업데이트"
image: "wordcloud.png"
---

원격 데스크톱(MSTSC)로 PC1 → PC2 접속 시 다음 문제가 반복될 수 있습니다.
- 문제 1: 원격 연결 상태에서 작업표시줄 아이콘과 실제 실행 프로그램이 불일치
- 문제 2: 원격 종료 후 PC2 로컬 로그인 시에도 아이콘과 실제 프로그램이 불일치
- 문제 3: 작업표시줄 자체가 보이지 않음(자동 숨김 아님). 재현 시 `Explorer` 재시작으로만 복구됨

이 글은 즉시 복구 방법과 근본 수리(아이콘/트레이 캐시 정리), 그리고 RDP 연결/해제 이벤트를 이용한 자동 복구(작업 스케줄러)까지 정리합니다. 정책상 MSTSC만 허용되는 환경을 전제로 합니다.

## 핵심 원인
- RDP 전환 과정에서 `explorer.exe`(셸/작업표시줄)가 글리치 상태로 남아 아이콘 매핑/표시가 꼬임
- 아이콘/트레이 캐시 손상으로 빈 아이콘, 잘못된 아이콘 지속
- 해상도/스케일 불일치와 일부 셸 커스터마이저가 문제를 증폭

## 문제 줄이는 방법: Persistent bitmap caching 끄기
- mstsc → 옵션 표시(Show Options) → 환경(Experience) 탭 → Persistent bitmap caching 체크 해제 → 저장.
- 오래된 비트맵을 재사용하는 캐시가 UI 잔상·틀린 툴바/작업표시줄을 유발할 수 있어, 문제 시 해제를 권장합니다. 참고: Microsoft Q&A 권장 사항.

## 즉시 복구(수동)
작업관리자(Ctrl+Shift+Esc) → `Windows Explorer` 우클릭 → 재시작. 또는 다음 명령으로 동일 처리:

```powershell
Stop-Process -Name explorer -Force; Start-Sleep -Milliseconds 800; Start-Process explorer.exe
```

또는 

```cmd
powershell -NoProfile -WindowStyle Hidden -Command "Stop-Process -Name explorer -Force; Start-Sleep -Milliseconds 800; Start-Process explorer.exe"
```

위 한 줄은 문제 1~3 모두에 효과적입니다.

## 자동 복구(권장): RDP 연결/해제 시 Explorer 자동 재시작
RDP 이벤트를 트리거로 `explorer.exe`를 자동 재시작하면 재발 시에도 사용자가 개입할 필요가 없습니다.

- 이벤트 로그: `Microsoft-Windows-TerminalServices-LocalSessionManager/Operational`
- 주요 이벤트 ID:
  - 24: 세션 연결 끊김(Disconnect)
  - 25: 세션 재연결(Reconnect)

작업 스케줄러에서 사용자 세션 기준으로 동작하도록 “사용자가 로그온한 경우에만 실행”과 “최고 권한으로 실행”을 설정하세요.

PowerShell/명령줄로 바로 등록하려면:

```cmd
schtasks /Create /TN "FixTaskbar_OnRDP_Disconnect" /TR "powershell.exe -NoProfile -WindowStyle Hidden -Command \"Stop-Process -Name explorer -Force; Start-Sleep -Milliseconds 800; Start-Process explorer.exe\"" /SC ONEVENT /EC "Microsoft-Windows-TerminalServices-LocalSessionManager/Operational" /MO "<QueryList><Query Id='0' Path='Microsoft-Windows-TerminalServices-LocalSessionManager/Operational'><Select Path='Microsoft-Windows-TerminalServices-LocalSessionManager/Operational'>*[System[(EventID=24)]]</Select></Query></QueryList>" /IT /RL HIGHEST /F

schtasks /Create /TN "FixTaskbar_OnRDP_Reconnect" /TR "powershell.exe -NoProfile -WindowStyle Hidden -Command \"Stop-Process -Name explorer -Force; Start-Sleep -Milliseconds 800; Start-Process explorer.exe\"" /SC ONEVENT /EC "Microsoft-Windows-TerminalServices-LocalSessionManager/Operational" /MO "<QueryList><Query Id='0' Path='Microsoft-Windows-TerminalServices-LocalSessionManager/Operational'><Select Path='Microsoft-Windows-TerminalServices-LocalSessionManager/Operational'>*[System[(EventID=25)]]</Select></Query></QueryList>" /IT /RL HIGHEST /F
```

설명:
- `/IT`로 대화형 사용자 세션에서만 실행되게 하여 서비스 세션에서의 불필요한 실행을 방지합니다.
- `/RL HIGHEST`로 권한 부족으로 인한 재시작 실패를 예방합니다.

## 아이콘 불일치/빈 아이콘의 근본 수리(1회성)
아이콘 캐시와 트레이 아이콘 캐시를 재구축하면 작업표시줄 아이콘 불일치가 해소됩니다.

1) 아이콘 캐시 재구축
```powershell
Stop-Process -Name explorer -Force
Remove-Item "$env:LOCALAPPDATA\Microsoft\Windows\Explorer\iconcache_*" -Force -ErrorAction SilentlyContinue
Remove-Item "$env:LOCALAPPDATA\IconCache.db" -Force -ErrorAction SilentlyContinue
Start-Process explorer.exe
```

2) 트레이(알림 영역) 아이콘 캐시 초기화
```cmd
taskkill /f /im explorer.exe
reg delete "HKCU\Software\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\TrayNotify" /v IconStreams /f
reg delete "HKCU\Software\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\TrayNotify" /v PastIconsStream /f
start explorer.exe
```

## 예방 팁
- PC1/PC2 해상도·스케일을 가급적 맞추면 RDP 전환 시 셸 글리치가 줄어듭니다.
- Windows 업데이트와 GPU 드라이버를 최신 유지.
- `Remote Procedure Call (RPC)` 서비스가 자동/실행인지 확인.
- StartAllBack/ExplorerPatcher 등 셸 커스터마이저는 문제 재현 시 일시 비활성 후 검증.

## 참고 자료
- 작업표시줄 미표시/재시작으로 해결 가이드: [AnyViewer](https://www.anyviewer.com/how-to/remote-desktop-connection-cannot-see-taskbar-8657.html), [TheWindowsClub](https://www.thewindowsclub.com/taskbar-not-visible-in-remote-desktop-on-windows-10)
- 아이콘 캐시 재구축: [ElevenForum](https://www.elevenforum.com/t/rebuild-icon-cache-in-windows-11.2049/), [Winhelponline](https://www.winhelponline.com/blog/how-to-rebuild-the-icon-cache-in-windows/)
- 트레이 아이콘 캐시 초기화: [How‑To Geek](https://www.howtogeek.com/fix-hidden-taskbar-icons-windows-11/)
- RDP 이벤트 로그와 ID: [Cyber Triage](https://www.cybertriage.com/artifact/terminalservices_localsessionmanager_log/), [Windows OS Hub](https://woshub.com/rdp-connection-logs-forensics-windows/)
- Persistent bitmap caching: [Microsoft Q&A - remote desktop cache \\ Permanently caching bitmaps](https://learn.microsoft.com/en-us/answers/questions/430008/remote-desktop-cache-permanently-caching-bitmaps), [Microsoft Q&A - How to fix the black screen issue in VM connecting through RDP](https://learn.microsoft.com/en-us/answers/questions/1159876/how-to-fix-the-black-screen-issue-in-vm-connecting)


