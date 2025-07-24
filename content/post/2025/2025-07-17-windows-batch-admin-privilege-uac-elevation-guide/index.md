---
title: "[CMD] BatchGotAdmin 스크립트로 Windows 관리자 권한 획득하기"
date: 2025-07-17
description: "Windows 환경에서 배치 파일(.bat)이 관리자 권한(Administrator Privilege)을 자동으로 요청하도록 하는 BatchGotAdmin 스크립트의 원리와 실제 동작 과정을 상세히 설명한다. UAC(User Account Control) 동작 방식, 스크립트 내부 구조, 실전 적용 방법, 주의사항까지 단계별로 안내하여, Windows 시스템 관리 자동화에 실질적으로 활용할 수 있도록 돕는다."
tags:
  - Windows
  - CMD
  - Batch
  - 관리자 권한
categories:
  - Windows
  - CMD
image: index.png
---


Windows 환경에서 여러 시스템 설정을 변경하거나 보호된 파일에 접근해야 할 때, 관리자 권한이 필요합니다. 그러나 일반 사용자 권한으로 실행된 배치 파일(.bat)은 이러한 작업을 수행할 수 없습니다. 이번 글에서는 **BatchGotAdmin**이라 불리는 간단한 배치 스크립트를 통해 사용자에게 관리자 권한 획득 팝업(UAC prompt)을 자동으로 띄우고, 이후 스크립트를 관리자 권한으로 실행하는 방법을 단계별로 살펴보겠습니다.

## Windows 관리자 권한(UAC)이란?

Windows Vista 이후 도입된 사용자 계정 컨트롤(User Account Control, UAC)은, 시스템 보안을 강화하기 위해 사용자 계정에 따라 프로그램 실행 권한을 제한하고, 중요한 작업을 수행할 때마다 사용자의 명시적 승인을 요구합니다.

* **표준 사용자(Standard User)**: 시스템 파일 변경, 서비스 설치 등 고권한 작업이 제한됩니다.
* **관리자(Administrator)**: UAC를 통해 승인을 받은 후에만 시스템 전체에 영향을 주는 작업을 수행할 수 있습니다.

UAC 창이 뜨는 이유는, 악의적인 코드가 의도치 않게 시스템에 손상을 가하는 것을 방지하고 사용자의 의도적인 동의 없이는 중요한 작업을 수행할 수 없도록 하기 위함입니다.

## BatchGotAdmin 스크립트 전체 코드

```batch
@REM 관리자 권한을 획득하는 팝업을 보여주는 스크립트
:: BatchGotAdmin
:-------------------------------------
REM  --> Check for permissions
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

REM --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else (
    goto gotAdmin
)

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
    pushd "%CD%"
    CD /D "%~dp0"
:--------------------------------------

@REM "아래쪽에 수행할 명령어를 시작하면 된다."
dir
pause
```

## 코드 동작 원리

1. **권한 확인 (`cacls.exe` 사용)**

   ```batch
   >nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
   ```

   * `cacls.exe`는 파일 ACL(Access Control List)을 조회하는 명령어입니다.
   * 시스템 폴더(`%SYSTEMROOT%\system32\config\system`)에 접근 권한이 있는지 확인해보고, 권한이 부족하면 오류(`errorlevel` ≠ 0)를 발생시킵니다.

2. **관리자 권한 요청 분기 처리**

   ```batch
   if '%errorlevel%' NEQ '0' (
       echo Requesting administrative privileges...
       goto UACPrompt
   ) else (
       goto gotAdmin
   )
   ```

   * `errorlevel`이 0이 아니면(= 관리자 권한이 없으면) `:UACPrompt` 레이블로 점프하여 UAC 팝업을 실행합니다.
   * 이미 관리자 권한이라면 `:gotAdmin`으로 건너뛰어 바로 본문을 실행합니다.

3. **UAC 팝업 생성 및 실행 (`.vbs` 파일 활용)**

   ```batch
   echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
   echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
   "%temp%\getadmin.vbs"
   exit /B
   ```

   * 임시 `.vbs`(VBScript) 파일을 만들어 `ShellExecute` 메서드를 통해 원본 배치 파일(`%~s0`)을 \*\*관리자 권한(runas)\*\*으로 다시 실행하도록 호출합니다.
   * 스크립트를 재실행하기 전 `exit /B`로 현재 권한 세션을 종료합니다.

4. **관리자 권한 상태에서 작업 수행**

   ```batch
   :gotAdmin
       if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
       pushd "%CD%"
       CD /D "%~dp0"
   ```

   * 임시로 생성된 VBS 파일을 삭제하여 깔끔하게 정리합니다.
   * `pushd` 및 `CD /D "%~dp0"` 명령을 통해 원본 스크립트의 위치로 경로를 변경하고, 이후 관리자 권한으로 실행될 작업들을 안전하게 수행할 준비를 마칩니다.

5. **실제 명령어 실행 부분**

   ```batch
   dir
   pause
   ```

   * 여기부터 사용자가 원하는 시스템 변경, 파일 복사, 레지스트리 수정 등 **관리자 권한이 필요한 작업**을 자유롭게 추가할 수 있습니다.

## 사용 예시

1. 위 코드를 `BatchGotAdmin.bat`로 저장합니다.
2. 배치 파일에 관리자 권한이 필요한 실제 명령(예: `xcopy`, `reg add`, 서비스 제어 등)을 `dir`과 `pause` 부분 대신 삽입합니다.
3. 파일을 더블 클릭하거나, 다른 스크립트에서 호출하면 자동으로 UAC 창이 뜨고 관리자로 실행됩니다.

```batch
:: 예시: system32 폴더에 파일 복사
copy "mydriver.sys" "%SYSTEMROOT%\system32\drivers\mydriver.sys"
```

## 주의 사항

* UAC 설정을 완전히 끈 환경에서는 이 스크립트가 동작하지 않습니다.
* `%temp%` 경로에 쓰기 권한이 필요하며, 보안 솔루션에 따라 임시 `.vbs` 파일이 차단될 수 있습니다.
* 반드시 신뢰할 수 있는 환경에서만 관리자 권한을 요청하고, 사용자에게 무분별한 권한 요청을 하지 않도록 작성해야 보안 사고를 방지할 수 있습니다.

## 결론

이번 글에서는 Windows 배치 파일(.bat) 내에서 손쉽게 관리자 권한을 요청할 수 있는 **BatchGotAdmin** 스크립트의 구조와 작동 원리를 단계별로 설명했습니다. CMD 환경에 익숙하지 않은 개발자라도, 위 템플릿을 활용하여 필요한 관리자 권한 작업을 간편하게 자동화할 수 있으니, 여러분의 워크플로우에 적극 활용해 보시기 바랍니다.
