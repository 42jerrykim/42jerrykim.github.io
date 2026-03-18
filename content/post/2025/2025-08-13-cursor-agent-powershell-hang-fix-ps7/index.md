---
title: "[Troubleshooting] Cursor Agent PowerShell 멈춤 해결 - PS7 전환 가이드"
description: "Windows에서 Cursor Agent 모드 사용 시 PowerShell 명령 실행 후 멈춤·출력 동기화 실패가 자주 보고된다. PowerShell 7 전환, 터미널 설정 초기화, CMD·Git Bash·WSL 대안, MCP 우회까지 단계별 해결법을 정리한 트러블슈팅 가이드다. 증상·원인·해결 흐름도와 참고 포럼 링크를 포함하며, Windows에서 Agent 모드를 쓰는 개발자에게 권장한다."
date: 2025-08-13
lastmod: 2026-03-17
categories:
- "Troubleshooting"
- "DevTools"
tags:
- IDE
- PowerShell
- Windows
- 윈도우
- 터미널
- Terminal
- 설정
- Configuration
- 문제해결
- Problem-Solving
- 비동기
- Async
- Tutorial
- 튜토리얼
- Guide
- 가이드
- Troubleshooting
- 트러블슈팅
- Shell
- Git
- GitHub
- Prompt-Engineering
- 프롬프트엔지니어링
- AI
- Command
- Design-Pattern
- 디자인패턴
- Productivity
- 생산성
- Education
- 교육
- Reference
- 참고
- Best-Practices
- Documentation
- 문서화
- Open-Source
- 오픈소스
- Technology
- 기술
- Web
- 웹
- Markdown
- 마크다운
- Review
- 리뷰
- Blog
- 블로그
- Code-Quality
- 코드품질
- Error-Handling
- 에러처리
- Debugging
- 디버깅
- Workflow
- 워크플로우
- Migration
- 마이그레이션
- How-To
- Tips
- Comparison
- 비교
- VSCode
- DevOps
- Automation
- 자동화
- Networking
- 네트워킹
- Beginner
- Case-Study
- IO
- Performance
- 성능
- Pitfalls
- 함정
- Clean-Code
- 클린코드
- Implementation
- 구현
- Testing
- 테스트
- Deployment
- 배포
- Linux
- 리눅스
- Bash
image: "wordcloud.png"
draft: false
---

## 개요

Windows에서 **Cursor Agent** 모드를 사용할 때, PowerShell로 명령을 실행한 뒤 터미널이 멈춘 것처럼 보이거나, 에이전트가 명령 완료를 기다리지 못하고 실패로 오판하는 현상이 빈번히 보고되고 있습니다. 특히 **Windows PowerShell 5.1** 환경에서 `&&` 체이닝 미지원, 출력 동기화 문제, PSReadLine 예외 등으로 작업이 중단되거나 재시도가 반복되는 경우가 많습니다.

이 글은 **가장 재현성이 높은 해결책부터 순서대로** 정리한 트러블슈팅 가이드입니다. Cursor를 Windows에서 Agent 모드로 쓰는 개발자, PowerShell 5.1을 기본 쉘로 쓰는 사용자, 터미널 출력 동기화 이슈로 에이전트가 잘못된 판단을 하는 경우에 참고하면 됩니다.

---

## 문제 상황

### 증상

- Agent가 PowerShell 명령을 실행한 뒤 **완료를 기다리지 않고** 실패로 간주하고 다음 동작(재시도·스크립트 수정 등)을 함.
- 터미널이 **멈춘 것처럼** 보이거나, 출력이 에이전트에게 제때 전달되지 않음.
- `&&`로 연결한 명령이 **PowerShell 5.1**에서 동작하지 않아 에러로 처리됨.
- `term '-1' is not recognized` 등 터미널 관련 오류로 명령 실행이 중단됨.

### 원인 요약

- Windows PowerShell 5.1과 Cursor 통합 터미널 간 **출력·완료 신호 동기화** 이슈.
- 5.1에서는 `&&`가 기본 지원되지 않아, 에이전트가 생성한 체이닝 명령이 실패함.
- 터미널 설정이 이전(VSCode 등)에서 이전되어 **호환되지 않는 옵션**이 남아 있는 경우.

---

## 해결 흐름 요약

아래 다이어그램은 권장하는 대응 순서를 요약한 것입니다. 가능하면 **PowerShell 7 전환**부터 적용하는 것이 가장 효과적입니다.

```mermaid
flowchart LR
  subgraph problem["문제 감지"]
    A[Agent 실행]
    B["PowerShell 5.1"]
    C["멈춤 또는 오판"]
    A --> B --> C
  end
  subgraph step1["1차 권장"]
    D["PS7 설치"]
    E["Cursor에서 pwsh 지정"]
    F["재시작"]
    D --> E --> F
  end
  subgraph step2["2차 대안"]
    G["터미널 설정 초기화"]
    H["CMD 또는 Git Bash 전환"]
    I["MCP 서버 우회"]
    G --> H
    H --> I
  end
  C --> D
  F -->|"해결 안 되면"| G
```

- **노드**: `problem`, `step1`, `step2`는 subgraph ID이며, 내부 노드 A~I는 camelCase·일반 단어로 예약어를 쓰지 않음.
- **라벨**: 특수문자·등호가 없는 문구는 따옴표 없이, 있으면 `"..."` 로 감쌈.

---

## 빠른 결론 (TL;DR)

- **PowerShell 7(pwsh)** 로 기본 쉘을 바꾸면 체이닝·동기화·잘못된 플래그 문제가 대부분 크게 완화됩니다.
- 5.1을 유지해야 한다면: **터미널 설정 초기화**, `&&` 대신 **`;` 체이닝** 사용, 또는 **CMD / Git Bash / WSL** 로 기본 쉘 전환을 고려하세요.
- 통합 터미널 불안정이 계속되면 **PowerShell MCP 서버**로 명령 실행을 우회하는 방법이 유효합니다.

---

## 1. PowerShell 버전 확인

현재 사용 중인 PowerShell 버전과 에디션을 확인합니다.

```powershell
# 42jerrykim.github.io에서 더 많은 정보를 확인할 수 있다
$PSVersionTable.PSVersion
$PSVersionTable.PSEdition
```

PowerShell 7이 설치되어 있는지 확인하려면:

```powershell
pwsh --version
```

---

## 2. PowerShell 7 설치

권장: **winget**으로 PowerShell 7을 설치합니다.

```powershell
# 42jerrykim.github.io에서 더 많은 정보를 확인할 수 있다
winget install --id Microsoft.PowerShell --source winget -e
```

설치 후 새 터미널에서 `pwsh` 실행 가능 여부와 `$PSVersionTable.PSEdition` 이 `Core` 인지 확인하세요.

---

## 3. Cursor에서 기본 쉘을 pwsh로 지정

설정 파일에 직접 넣으려면 `%APPDATA%\Cursor\User\settings.json` 에 다음 항목을 추가하거나 수정합니다.

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

- `path` 는 실제 pwsh.exe 경로에 맞게 조정하세요 (예: 사용자 전용 설치 시 다른 경로).
- 적용 후 **Cursor를 재시작**하는 것을 권장합니다.

---

## 4. PowerShell 5.1을 계속 써야 할 때

- **터미널 설정 초기화**: 설정에서 `@feature:terminal @modified` 로 검색한 뒤, `terminal.integrated.*` 항목을 하나씩 **Reset** 합니다. (다른 IDE에서 가져온 설정이 꼬인 경우에 특히 유효.)
- **체이닝**: `&&` 대신 **`;`** 를 사용하도록 에이전트에게 명시하거나, 기본 쉘을 **Command Prompt** / **Git Bash** 로 바꿉니다.
- **인라인 출력**: Terminal 설정에서 **Use Preview Box** 토글을 켜면 출력 가시성이 나아질 수 있습니다.

---

## 5. 추가 팁

- **실행 정책** 때문에 `.ps1` 실행이 막히는 경우:
  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force
  ```
- **관리자 권한**으로 Cursor를 실행했을 때 문제가 줄어든 사례가 있습니다.
- 인라인 터미널이 “멈춘” 것처럼 보일 때: 해당 박스에 **포커스 후 Enter** 를 누르거나, 출력만 복사해 대화에 붙여 넣어 에이전트에게 전달할 수 있습니다.

---

## 6. 통합 터미널 우회: PowerShell MCP 서버

통합 터미널의 출력 동기화·대기 문제가 반복되면, **PowerShell MCP 서버**를 구성해 에이전트의 명령 실행을 MCP 경로로 우회할 수 있습니다. 프로젝트에 종속되지 않는 **전역 MCP 서버**로 두면 새 프로젝트에서도 재사용할 수 있습니다.

---

## 참고 자료

- [Agent does not wait for powershell commands](https://forum.cursor.com/t/agent-does-not-wait-for-powershell-commands/48866) — Cursor 포럼: Agent가 PowerShell 완료를 기다리지 않는 현상.
- [Cursor AI uses incorrect command separator in Agent mode on PowerShell](https://forum.cursor.com/t/cursor-ai-uses-incorrect-command-separator-in-agent-mode-on-powershell/93389) — PowerShell에서 `&&` 대신 `;` 가 필요한 논의.
- [Agent terminal commands stop working (term '-1' is not recognized)](https://forum.cursor.com/t/agent-terminal-commands-stop-working-the-term-1-is-not-recognized/36603) — 터미널 설정 초기화·PS7 전환으로 해결된 사례.

이 글의 핵심은 **PS7 전환과 터미널 설정 정리**만으로도 Agent 모드 실패율이 체감될 정도로 줄어든다는 점입니다. CMD·Git Bash·WSL 전환이나 MCP 서버 우회는 환경 제약이 있을 때 선택적으로 적용하면 됩니다.
