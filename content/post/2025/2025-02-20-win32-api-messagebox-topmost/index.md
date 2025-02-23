---
title: "[Win32] Win32 API에서 메시지 박스를 최상단에 표시하는 방법"
date: 2025-02-20T12:00:00+09:00
categories:
  - Win32
  - Programming
tags:
  - Win32 API
  - Windows
  - MessageBox
  - CBT Hook
  - SetForegroundWindow
  - Win32 API
  - 메시지 박스
  - 최상단
  - 포커스
  - CBT 후크
  - AllowSetForegroundWindow
  - SetForegroundWindow
  - 창 활성화
  - Windows
  - 프로그래밍
  - MessageBox
  - Topmost
  - Focus
  - CBT Hook
  - AllowSetForegroundWindow
  - SetForegroundWindow
  - Window Activation
  - Windows
  - Programming
description: "Win32 API 환경에서 메시지 박스가 최상단에 포커스를 강제로 획득하도록 실행하는 방법에 대해 알아보겠다이다. CBT 후크와 AllowSetForegroundWindow API를 활용한 두 가지 해결 방안을 소개한다."
image: messagebox_02.png
---

이번 포스트에서는 Win32 API 환경에서 메시지 박스가 최상단에 포커스를 강제로 획득하는 방법에 대해 알아보겠다.  
기본적으로 MB_SETFOREGROUND 플래그를 사용하면 어느 정도 효과가 있지만, Windows의 창 활성화 정책과 포커스 관리 로직에 따라 의도한 대로 동작하지 않는 경우가 많다. 이에 대해 CBT 후크와 AllowSetForegroundWindow API를 활용한 두 가지 방법을 소개하겠다.


## 문제의 배경

윈도우 환경에서는 다른 응용 프로그램이 실행 중일 경우 포그라운드 창 변경에 제약이 있다.  
따라서 단순히 MB_SETFOREGROUND 플래그만 사용하는 경우, 호출 프로세스가 이미 포그라운드 상태여야 하는 등 여러 조건이 충족되어야 한다.  
이러한 제한 사항으로 인해 메시지 박스가 최상단에 배치되지 않거나 포커스를 획득하지 못하는 문제가 발생할 수 있다.

## 해결 방법 1: CBT 후크 이용

CBT(Computer-Based Training) 후크를 사용하면 메시지 박스가 생성될 때 창의 스타일을 강제로 조정할 수 있다.  
아래 코드는 WH_CBT 후크를 설정하여 메시지 박스가 활성화되면 HWND_TOPMOST로 창을 배치하고 후크를 해제하는 예제이다.

```cpp
#include <windows.h>

HHOOK g_hHook = NULL;

LRESULT CALLBACK CBTProc(int nCode, WPARAM wParam, LPARAM lParam)
{
    if(nCode == HCBT_ACTIVATE)
    {
        HWND hMsgBox = (HWND)wParam;
        // 메시지 박스를 최상단에 배치한다.
        SetWindowPos(hMsgBox, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE);
        UnhookWindowsHookEx(g_hHook);
    }
    return CallNextHookEx(g_hHook, nCode, wParam, lParam);
}

void ShowTopMostMessageBox(HWND hParent)
{
    // CBT 후크를 설정한다.
    g_hHook = SetWindowsHookEx(WH_CBT, CBTProc, NULL, GetCurrentThreadId());
    // MB_SETFOREGROUND 플래그를 포함하여 메시지 박스를 생성한다.
    MessageBox(hParent, L"메시지 내용", L"타이틀", MB_OK | MB_SETFOREGROUND);
    // 후크는 CBTProc에서 해제된다.
}
```

이 코드는 메시지 박스가 생성되자마자 후크 콜백 함수가 호출되어 창을 최상단으로 이동시키는 방식이다.  
그러나 이 방법도 시스템의 보안 정책이나 현재 프로세스의 상태에 따라 제약을 받을 수 있으므로, 모든 환경에서 100% 동작을 보장하지는 않는다.


## 해결 방법 2: AllowSetForegroundWindow API 활용

AllowSetForegroundWindow 함수는 다른 프로세스나 현재 프로세스가 포그라운드 창을 설정할 수 있도록 권한을 부여하는 API이다.  
이 API를 사용하면, 호출 시점에 현재 프로세스가 포그라운드 창 설정 권한을 얻어 메시지 박스가 올바르게 포커스를 획득하도록 할 수 있다.

```cpp
#include <windows.h>

void ShowMyMessageBox()
{
    // 현재 프로세스에게 포그라운드 창 설정 권한을 부여한다.
    AllowSetForegroundWindow(ASFW_ANY);
    
    // MB_SETFOREGROUND 플래그를 사용하여 메시지 박스를 생성한다.
    MessageBox(NULL, L"메시지 내용", L"타이틀", MB_OK | MB_SETFOREGROUND);
}
```

이 코드에서는 AllowSetForegroundWindow에 ASFW_ANY를 전달하여 모든 프로세스가 포그라운드 창을 설정할 수 있도록 허용하였다.  
단, 이 방법 역시 호출 시점의 환경(예: 현재 포그라운드 상태 등)에 따라 동작이 제한될 수 있음을 유의하여야 한다.


## 결론

Win32 API 환경에서 메시지 박스가 최상단에 포커스를 획득하도록 하는 방법은 여러 가지가 있으며, 단순히 MB_SETFOREGROUND 플래그만 사용하는 것으로는 충분하지 않은 경우가 많다.  
CBT 후크를 이용하면 창 생성 시점을 포착하여 최상단에 배치할 수 있지만, 시스템의 보안 정책에 따라 제약이 있을 수 있다.  
또한 AllowSetForegroundWindow API를 활용하여 포그라운드 창 설정 권한을 부여하는 방법도 고려해볼 만하다.  
상황에 맞는 방법을 선택하여 최적의 사용자 경험을 제공하는 것이 중요하다.