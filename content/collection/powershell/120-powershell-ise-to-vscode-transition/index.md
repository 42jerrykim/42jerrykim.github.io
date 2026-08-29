---
draft: true
collection_order: 120
slug: powershell-ise-to-vscode-transition
title: "[PowerShell] 120. PowerShell ISE에서 VS Code로 — 개발 환경 전환"
date: 2026-08-29
lastmod: 2026-08-29
description: "더 이상 신규 기능 개발이 없는 PowerShell ISE 대신 VS Code와 PowerShell 확장으로 개발 환경을 전환하는 이유와 방법을 정리한 이 컬렉션의 마지막 챕터로, 120개 챕터의 학습 여정을 마무리한다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- Cross-Platform
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
- PowerShell-ISE
- VSCode
- PowerShell-Extension
- IntelliSense
- Development-Environment
- Editor(에디터)
image: "wordcloud.png"
---

## 개요

<strong>PowerShell ISE(통합 스크립팅 환경)</strong>는 Windows PowerShell 2.0부터 제공된 전용 편집기였지만, PowerShell 7과 함께 등장한 시대의 흐름 속에서 더 이상 신규 기능 개발이 이뤄지지 않는 상태다. 119장에서 PowerShell 7이 완전히 새로운 크로스플랫폼 런타임 위에 지어졌다고 배운 것과 같은 이유로, ISE도 .NET Framework 기반 Windows 전용 애플리케이션이라 PowerShell 6 이상에서는 아예 지원되지 않는다. 이 컬렉션의 마지막 장으로서, 1장부터 지금까지 콘솔에서 직접 명령을 실행하며 배운 모든 내용을 실제로 어떤 편집기에서 스크립트로 작성해 나갈 것인지 실용적으로 정리한다.

정신 모델은 "ISE가 PowerShell 하나만을 위해 지어진 전용 작업실이었다면, VS Code는 여러 언어를 위한 범용 작업대에 PowerShell 확장이라는 전문 공구함을 얹은 것"이라는 것이다. 전용 작업실은 더 이상 새 공구가 들어오지 않지만, 범용 작업대는 그 자체로 계속 발전하고 PowerShell 공구함도 독립적으로 업데이트된다.

## 사용법

```powershell
code .                    # 현재 폴더를 VS Code로 열기(PowerShell 확장 설치 후)
```

## 종류

| 비교 항목 | PowerShell ISE | VS Code + PowerShell 확장 |
|---|---|---|
| 지원 PowerShell 버전 | Windows PowerShell 5.1까지만 | Windows PowerShell 5.1과 PowerShell 7 모두 |
| 지원 운영체제 | Windows만 | Windows, Linux, macOS |
| 개발 상태 | 신규 기능 개발 중단(보안 수정만) | 활발히 개발 중 |
| 확장성 | 없음(고정된 기능) | 수천 개의 확장으로 자유롭게 확장 |
| 디버깅 | 기본적인 중단점 지원 | 중단점, 변수 조사, 호출 스택 등 완전한 디버거 |
| 버전 관리 통합 | 없음 | Git 통합 내장 |
| IntelliSense | 기본적인 탭 완성 | cmdlet·매개변수·변수 타입까지 인식하는 정교한 자동완성 |

## 예시

```powershell
# VS Code 설치 후 PowerShell 확장(ms-vscode.PowerShell)을 마켓플레이스에서 검색해 설치

code MyScript.ps1                             # 특정 스크립트 파일을 VS Code로 바로 열기

# VS Code 통합 터미널(Ctrl+`)에서 pwsh 세션을 그대로 사용 가능 — 편집기와 콘솔을 오가지 않아도 됨
# F5로 전체 스크립트 실행, F8로 선택한 줄만 실행(ISE의 "선택 영역 실행"과 동일한 워크플로)

# settings.json에 다음을 추가하면 기본 터미널을 pwsh로 지정할 수 있다
# "terminal.integrated.defaultProfile.windows": "PowerShell"
```

## 주의사항·함정

**ISE 프로필 스크립트(`$PROFILE`)는 VS Code로 그대로 옮겨지지 않는다**: ISE와 콘솔(`powershell.exe`/`pwsh`)은 서로 다른 프로필 파일 경로를 쓰며, VS Code의 PowerShell 확장은 또 별도의 호스트 이름(`Visual Studio Code Host`)으로 프로필을 구분한다. `$PROFILE.CurrentUserCurrentHost`가 편집기마다 다른 경로를 가리킨다는 점을 모르고 있으면, ISE에서 설정한 별칭·함수가 VS Code에서 갑자기 사라진 것처럼 보인다.

**PowerShell 7이 설치돼 있어도 VS Code의 기본 통합 터미널이 자동으로 pwsh를 쓰는 것은 아니다**: PowerShell 확장을 설치한 뒤에도 VS Code의 터미널 프로필 설정에서 명시적으로 `pwsh`를 기본으로 지정해야 하며, 그렇지 않으면 운영체제 기본 셸(Windows에서는 여전히 Windows PowerShell 5.1일 수 있음)이 열릴 수 있다.

**ISE 전용 기능 중 일부는 VS Code에 그대로 대응되지 않는다**: ISE의 "Show-Command" GUI(cmdlet 매개변수를 양식으로 채워 넣는 기능)처럼 ISE에만 있던 일부 보조 도구는 VS Code 확장에 동일한 형태로 존재하지 않는다. 다만 그 자리를 IntelliSense와 `Get-Help -ShowWindow`가 상당 부분 대체하므로, 기능이 완전히 사라졌다기보다 다른 방식으로 재구현됐다고 보는 편이 정확하다.

**"ISE가 아직 실행되니 계속 써도 된다"는 판단은 장기적으로 위험하다**: ISE는 보안 및 우선순위가 높은 수정 사항만 받는 유지보수 상태이며, PowerShell 7의 신규 언어 기능(119장의 삼항 연산자 등)은 ISE의 구문 강조·IntelliSense에서 인식되지 않는다. 5.1과 7을 함께 다뤄야 하는 실무 환경일수록 VS Code 하나로 두 버전을 모두 다루는 편이 유지보수 부담을 줄인다.

**이식성**: VS Code와 PowerShell 확장의 조합은 Windows·Linux·macOS 어디서나 동일한 개발 경험을 제공한다는 점에서, ISE가 갖지 못했던 이식성을 그대로 갖는다. Bash·Python 등 다른 언어의 확장과 같은 편집기 안에서 나란히 쓸 수 있다는 점도, 여러 언어를 오가며 자동화 스크립트를 작성하는 실무 환경에서 실질적인 이점이다.

## 마치며

이 컬렉션은 여기서 120개 챕터를 마무리한다. 1부(콘솔 조작)에서 시작해 2부(객체 파이프라인)로 CMD·Bash와의 가장 큰 사고 전환을 거치고, 파일 시스템·데이터 구조·스크립팅·에러 처리·테스트·모듈화(3–9부)로 재사용 가능한 코드를 만드는 능력을 쌓은 뒤, 패키지·원격 관리·시스템 관리·보안·DSC·네트워크·엔터프라이즈 디렉터리(10–17부)로 그 능력을 실제 인프라 운영 범위까지 확장했다. 이 장에서 다룬 개발 환경 전환은 이 모든 여정을 계속 이어갈 도구를 정리하는 실용적인 마침표다. [00장의 커리큘럼 표](/post/powershell/getting-started-powershell/)로 돌아가면 전체 구성을 한눈에 다시 확인할 수 있다.

## Reference

- [Introducing the Windows PowerShell ISE - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/scripting/windows-powershell/ise/introducing-the-windows-powershell-ise)
