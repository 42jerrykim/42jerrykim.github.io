---
title: "[Troubleshooting] Cursor Agent PowerShell 멈춤 - PS7 전환 가이드"
description: "Windows에서 Cursor Agent 모드가 PowerShell 명령 실행 후 멈추거나 출력 동기화가 되지 않는 문제를 해결하는 가이드입니다. PS7 전환, 터미널 설정 초기화, CMD/Git Bash/WSL 대안, MCP 우회까지 핵심만 단계별로 정리했습니다."
date: 2025-08-13
lastmod: 2025-08-13
categories:
- "Troubleshooting"
- "DevTools"
tags:
- "Cursor"
- "Agent Mode"
- "PowerShell"
- "Windows"
- "Windows 11"
- "pwsh"
- "PSReadLine"
- "execution policy"
- "터미널"
- "인라인 터미널"
- "미리보기 박스"
- "Use Preview Box"
- "설정"
- "settings.json"
- "defaultProfile"
- "profiles"
- "Git Bash"
- "WSL"
- "Command Prompt"
- "cmd"
- "&&"
- "세미콜론"
- "semicolon"
- "체이닝"
- "chaining"
- "output"
- "hang"
- "no response"
- "timeout"
- "background"
- "move to background"
- "MCP"
- "PowerShell MCP Server"
- "Cursor 포럼"
- "GitHub"
- "레딧"
- "버그"
- "해결"
- "워크어라운드"
- "문제 해결"
- "Windows PowerShell 5.1"
- "PowerShell 7"
- "pwsh.exe"
- "winget"
- "RemoteSigned"
- "관리자 권한"
- "admin"
- "terminal.integrated"
- "defaultProfile.windows"
- "profiles.windows"
- "args"
- "NoProfile"
- "NoLogo"
- "Cursor Agent"
- "개발 생산성"
- "Dev Environment"
- "IDE"
- "통합 터미널"
- "출력 동기화"
- "명령 체이닝"
- "비동기"
- "stuck"
- "stability"
image: "wordcloud.png"
---

Windows에서 Cursor Agent 모드를 사용할 때 PowerShell 명령 실행이 멈추거나, 에이전트가 완료를 기다리지 못하고 오판하는 현상이 빈번히 보고되고 있습니다. 특히 Windows PowerShell 5.1 환경에서 `&&` 체이닝, 출력 동기화, PSReadLine 예외 등으로 작업이 중단되거나 재시도가 남발되는 문제가 있습니다. 이 글은 가장 재현성이 높은 해결책부터 순서대로 정리합니다.

## 빠른 결론
- PowerShell 7(pwsh)로 기본 쉘을 전환하면 대부분의 문제(체이닝/동기화/잘못된 플래그)가 크게 완화됩니다.
- 5.1을 써야 한다면 터미널 설정 초기화, `;` 체이닝 강제, 또는 CMD/Git Bash/WSL로 전환하세요.
- 통합 터미널 불안정이 계속되면 PowerShell MCP 서버로 명령 실행을 우회하는 방법이 유효합니다.

## PowerShell 버전 확인
```powershell
$PSVersionTable.PSVersion
$PSVersionTable.PSEdition
```

```powershell
pwsh --version
```

## PowerShell 7 설치
```powershell
# 더 많은 정보: 42jerrykim.github.io
winget install --id Microsoft.PowerShell --source winget -e
```

## Cursor에서 기본 쉘을 pwsh로 지정

직접 설정하려면 `%APPDATA%\Cursor\User\settings.json`에 다음 항목을 추가/수정하세요.

```json
{
  "terminal.integrated.defaultProfile.windows": "PowerShell",
  "terminal.integrated.profiles.windows": {
    "PowerShell": {
      "path": "C:\\Program Files\\PowerShell\\7\\pwsh.exe",
      "args": ["-NoLogo", "-NoProfile"],
      "icon": "terminal-powershell"
    }
  }
}
```

적용 후 Cursor를 재시작하는 것을 권장합니다.

## PowerShell 5.1을 계속 써야 한다면
- 터미널 설정 초기화: 설정에서 `@feature:terminal @modified` 검색 → `terminal.integrated.*` 값들을 Reset
- 체이닝은 `&&` 대신 `;` 사용하도록 프롬프트에 명시하거나, 기본 쉘을 `Command Prompt`/`Git Bash`로 전환
- 인라인 출력 가시성 개선: Terminal > “Use Preview Box” 토글

## 추가 팁
- 실행 정책으로 `.ps1` 실행이 막히는 경우:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force
```
- 관리자 권한으로 Cursor 실행이 도움이 된 사례 존재
- 인라인 터미널이 “멈춘” 듯 보이면 해당 박스에 포커스 후 Enter, 또는 백그라운드로 보내고 출력만 복사해 대화로 전달

## 통합 터미널 우회: PowerShell MCP 서버
통합 터미널의 출력 동기화/대기 문제가 빈번하다면, PowerShell MCP 서버를 구성해 에이전트 명령을 MCP 경로로 우회할 수 있습니다. 프로젝트에 종속되지 않는 전역 MCP 서버로 만들면 새 프로젝트에서도 재활용 가능합니다.

## 참고 자료
- GitHub: [PowerShell Command Execution Bug (Issue #2669)](https://github.com/cursor/cursor/issues/2669)
- 포럼: [Agent가 PowerShell 완료 대기 안 함](https://forum.cursor.com/t/agent-does-not-wait-for-powershell-commands/48866)
- 포럼: [터미널 출력 처리 이슈](https://forum.cursor.com/t/terminal-output-handling-issues-in-agent-mode/58317)
- 포럼: [PowerShell에서 `&&` 대신 `;` 필요](https://forum.cursor.com/t/cursor-ai-uses-incorrect-command-separator-in-agent-mode-on-powershell/93389)
- 포럼: [설정 초기화로 해결된 사례](https://forum.cursor.com/t/agent-terminal-commands-stop-working-the-term-1-is-not-recognized/36603)

이 글의 핵심은 “PS7 전환 + 터미널 설정 정리”만으로도 Agent 모드의 실패율이 체감될 정도로 줄어든다는 점입니다. 나머지 대안(CMD/Git Bash/WSL 전환, MCP 서버 우회)은 환경 제약이 있을 때 선택적으로 적용하세요.
