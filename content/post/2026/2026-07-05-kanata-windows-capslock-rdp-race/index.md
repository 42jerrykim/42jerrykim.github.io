---
title: "[Windows] RDP CapsLock 토글 버그 - kanata 훅의 한계"
description: "kanata로 리매핑해도 MSTSC에서 CapsLock 토글이 새는 문제를 실측했다. OS가 훅보다 먼저 토글을 확정해 사용자 모드로는 못 막는다."
date: 2026-07-05
lastmod: 2026-07-05
draft: false
categories:
  - Windows
  - Troubleshooting
tags:
  - Windows(윈도우)
  - Shell(셸)
  - Automation(자동화)
  - Kernel
  - OS(운영체제)
  - IO(Input/Output)
  - Signal
  - Permission
  - RDP(Remote Desktop Protocol)
  - Troubleshooting(트러블슈팅)
  - Configuration(설정)
  - Keyboard(키보드)
  - Technology(기술)
  - Terminal
  - kanata
  - CapsLock
  - AltGr
  - Low-Level-Hook
  - Race-Condition
  - MSTSC
  - Registry
  - Scancode-Map
  - Interception-Driver
  - PowerToys
  - Debugging
  - GetKeyState
  - LLKH
  - Windows-API
  - Remote-Desktop
image: "wordcloud.png"
---

## 개요

[kanata](https://github.com/jtroo/kanata)로 키보드를 전면 리매핑해서 쓰고 있다. CapsLock은 탭하면 한/영 전환, 누르고 있으면 마우스 레이어가 뜨도록 완전히 다른 동작으로 바꿔놨다. 그런데 MSTSC(원격 데스크톱)로 접속해서 작업하다 보면, 물리 CapsLock 키를 눌렀을 뿐인데 로컬 PC(HOST)의 CapsLock 잠금 상태(LED)가 같이 켜지는 증상이 있었다. kanata가 그 키를 이미 다른 동작으로 완전히 가로챘는데도 말이다. 이 글은 이 증상을 `--debug` 로그와 직접 만든 PowerShell 폴링 스크립트로 실측 디버깅해서 근본 원인을 찾아낸 과정과, 같은 계열에서 발견한 두 번째 문제(한/영 키를 누르면 Alt가 고정되는 문제)를 kanata 설정 한 줄로 해결한 과정을 정리한다. 환경은 Windows 11, kanata `winIOv2` 빌드다.

## 문제

증상은 두 가지였다.

1. MSTSC로 원격 세션에 접속해 작업 중, 물리 CapsLock 키(kanata가 이미 한/영·마우스 레이어로 리매핑한 키)를 누르면 HOST의 CapsLock 잠금 상태가 켜진다.
2. 키보드 오른쪽 아래의 한/영 키(물리적으로 RAlt 위치)를 누르면 Alt 키가 눌린 채로 고정되는 문제가 있다.

kanata 설정(`bin/kanata.kbd`)에는 이미 다음과 같이 CapsLock과 RAlt를 완전히 다른 동작으로 대체해뒀다.

```lisp
(defsrc
  ...
  caps a    s    d    f    g    h    j    k    l    ;    '    ret
  ...
  lctl lmet lalt           spc            ralt rmet rctl
)

(defalias
  han (arbitrary-code 21)  ;; VK_HANGUL 직접 전송
  cap (tap-hold-press $tap-timeout $hold-timeout (arbitrary-code 21) (layer-toggle mouse))
)

(deflayer base
  @cap ...
  ...           @han rmet rctl
)
```

리매핑이 이미 되어 있는데도 물리 키의 부작용(CapsLock 토글, Alt 고정)이 새어 나온다는 게 이상했다. "kanata가 아직 뭔가를 놓치고 있나?"에서 출발해 실측으로 확인하기로 했다.

## 해결 전략

두 증상을 별개로 다뤘다.

**CapsLock 토글**은 먼저 재현 조건과 타이밍을 정확히 잡아야 했다. kanata가 키 이벤트를 **받는 시점**과 Windows가 CapsLock 잠금 상태를 **바꾸는 시점**을 각각 로그로 남겨서 순서를 비교하면, "kanata가 이벤트를 놓치는 것"인지 "이벤트를 받고도 토글을 못 막는 것"인지 구분할 수 있다고 판단했다. 전자라면 kanata 설정이나 훅 등록 순서를 고치면 되고, 후자라면 사용자 모드 소프트웨어로는 원천적으로 해결이 안 되는 문제라서 접근 자체를 바꿔야 한다.

**Alt 고정**은 kanata 공식 문서에 있는 AltGr 관련 알려진 이슈([`windows-altgr`](https://github.com/jtroo/kanata/blob/main/docs/config.adoc))와 증상이 정확히 일치해서, 문서가 제시하는 설정을 그대로 적용하는 쪽으로 바로 방향을 잡았다.

## 구현

### 1. CapsLock 토글 타이밍 실측

kanata를 `--debug`로 실행해 콘솔에 이벤트 로그를 남기고, 동시에 별도 PowerShell 창에서 CapsLock 잠금 상태를 30ms 간격으로 폴링하는 스크립트를 돌렸다.

```powershell
Add-Type -AssemblyName System.Windows.Forms

$prev = [System.Windows.Forms.Control]::IsKeyLocked('CapsLock')
Write-Host "$(Get-Date -Format 'HH:mm:ss.fff') 초기 상태: $prev"

while ($true) {
    $cur = [System.Windows.Forms.Control]::IsKeyLocked('CapsLock')
    if ($cur -ne $prev) {
        Write-Host "$(Get-Date -Format 'HH:mm:ss.fff') CapsLock 상태 변경: $prev -> $cur" -ForegroundColor Yellow
        $prev = $cur
    }
    Start-Sleep -Milliseconds 30
}
```

물리 CapsLock을 눌러가며 두 로그의 타임스탬프를 나란히 비교했다.

```
# PowerShell 폴링 로그
15:35:08.403  CapsLock 상태 변경: False -> True

# kanata --debug 로그
15:35:08.4838 [DEBUG] event loop: KeyEvent { code: KEY_CAPSLOCK (20), value: Press }
```

CapsLock 잠금 상태가 **먼저** `False -> True`로 바뀌고, 그로부터 약 **80ms 뒤**에야 kanata의 저수준 훅(`llhook`)이 `KEY_CAPSLOCK Press` 이벤트를 받았다. 두 번째 누름도 마찬가지로 토글이 먼저(`True -> False`), kanata 수신이 88ms 뒤였다. 즉 Windows OS가 CapsLock 토글 비트를 훅에 이벤트를 넘기기도 전에 이미 확정해버린다 — kanata가 아무리 완벽하게 이벤트를 가로채도 이 시점 이후이므로 토글 자체는 막을 수 없다는 뜻이다.

이 현상은 kanata만의 문제가 아니었다. Microsoft의 공식 PowerToys 저장소에도 동일한 증상이 이슈로 등록되어 있다([#7302](https://github.com/microsoft/PowerToys/issues/7302)). 거기서 개발자는 KeyTweak·SharpKeys는 이 문제가 없다고 언급했는데, 이 두 도구의 공통점은 레지스트리 Scancode Map(`HKLM\SYSTEM\CurrentControlSet\Control\Keyboard Layout`의 `Scancode Map`)으로 커널의 키보드 클래스 드라이버 단계에서 스캔코드 자체를 치환한다는 것이다. 이 단계에서 바꾸면 Windows는 애초에 그 키를 "CapsLock"으로 인식하지 못하므로 토글이 생성될 여지가 없다. 반면 kanata의 `winIOv2`나 PowerToys Keyboard Manager는 저수준 훅(사용자 모드)이라 OS가 토글을 이미 확정한 뒤에야 이벤트를 받는다 — 구조적으로 더 늦다.

추가로 확인한 것은, kanata 자체가 CapsLock의 토글 상태를 **읽는 기능이 없다**는 점이다(kanata 메인테이너가 [GitHub Discussion #1675](https://github.com/jtroo/kanata/discussions/1675)에서 "Caps Lock state is not detectable by Kanata today"라고 직접 확인). 그래서 "토글이 켜지면 kanata가 자동으로 꺼준다" 같은 설정 자체가 불가능하다. 외부 감시 스크립트로 토글 상태를 폴링하다가 켜지면 다시 눌러 꺼주는 방법도 검토했지만, 그 보정 입력 자체가 다시 물리 CapsLock 스캔코드로 인식되어 kanata의 `defsrc caps` 규칙에 걸려 원래 설정된 동작(한/영 전환)으로 바뀌어버린다. 즉 순수 사용자 모드 소프트웨어로는 확실한 보정이 불가능하다는 결론에 이르렀고, 남은 선택지는 레지스트리 Scancode Map 또는 커널 필터 드라이버(kanata의 `wintercept`, Interception 드라이버 기반) 둘 중 하나뿐이다.

### 2. RAlt(한/영 키) Alt 고정 문제

이 문제는 실측이 필요 없었다. kanata 설정 가이드의 "Windows only: windows-altgr" 항목이 증상을 정확히 설명하고 있었다.

> 많은 non-US 키보드가 AltGr로 취급하는 RAlt는, Windows가 눌릴 때 내부적으로 가짜 LCtrl keydown을 함께 생성한다. `process-unmapped-keys yes`나 `defsrc`에 `ralt`/`lctl`이 있는 상태에서 이 가짜 LCtrl을 정리하지 않으면 Alt/Ctrl이 고정될 수 있다.

원인은 `bin/kanata.kbd`에서 한/영 키를 `ralt` 물리 위치에 매핑하고 `process-unmapped-keys yes`를 켜둔 것이 정확히 이 조건에 해당했기 때문이다. `defcfg`에 한 줄만 추가하면 해결된다.

```lisp
(defcfg
  ...
  process-unmapped-keys yes

  ;; ralt(한/영 키)를 가로챌 때 Windows가 내부적으로 생성하는
  ;; 가짜 lctl press를 정리 (미처리 시 Alt/Ctrl이 눌린 채로 고정)
  windows-altgr add-lctl-release
)
```

`windows-altgr`에는 두 값이 있다. `cancel-lctl-press`는 가짜 LCtrl press 자체를 아예 없애고, `add-lctl-release`는 RAlt를 뗄 때 LCtrl release를 추가로 보내는 방식이다. RAlt를 계속 눌러야 다른 조합키(예: `RA-a`처럼 AltGr+문자)로 특수문자를 입력해야 하는 상황이 아니라면 `add-lctl-release` 쪽이 더 안전하다.

## 대안: 왜 감시 스크립트로 CapsLock을 보정하지 않았나

CapsLock 문제에 대해 레지스트리·드라이버 없이 순수 소프트웨어로 고치는 방법도 시도해보려 했다. PowerShell로 CapsLock 잠금 상태를 폴링하다가 원치 않게 켜지면 즉시 CapsLock을 한 번 더 눌러서 꺼주는 감시 스크립트다. 하지만 위에서 실측한 대로 kanata가 물리 CapsLock 스캔코드를 완전히 가로채는 구조이기 때문에, 감시 스크립트가 보내는 보정용 CapsLock 입력조차 kanata에 의해 다시 한/영 전환 동작으로 치환되어버려 실제 토글은 꺼지지 않는다. 이 접근은 채택하지 않았고, 레지스트리 Scancode Map 또는 Interception 드라이버 중 하나를 선택하는 문제로 남겨뒀다.

## 적용 전후 비교

| 항목 | 적용 전 | 적용 후 |
|------|---------|---------|
| RAlt(한/영 키) 사용 시 Alt 고정 | 발생 | `windows-altgr add-lctl-release` 추가로 해소 |
| MSTSC 원격 세션에서 CapsLock 물리 키 입력 시 HOST CapsLock 토글 | 발생, kanata 훅 도달보다 약 80–90ms 먼저 OS가 토글 확정(실측) | 근본 해결에는 레지스트리 Scancode Map 또는 Interception 드라이버 필요 — 진단 완료, 조치는 다음 단계로 보류 |

## 요약

- kanata·PowerToys Keyboard Manager 같은 **저수준 사용자 모드 훅**은 키 입력의 "동작"은 완전히 바꿀 수 있어도, CapsLock 같은 **토글 키의 잠금 비트**는 OS가 훅보다 먼저 확정해버리기 때문에 막을 수 없다. 이 순서는 `--debug` 로그와 `IsKeyLocked` 폴링 스크립트의 타임스탬프를 나란히 비교하면 직접 실측으로 확인할 수 있다.
- 이 문제의 확실한 해법은 레지스트리 Scancode Map(KeyTweak·SharpKeys 방식)이나 커널 필터 드라이버(Interception, kanata의 `wintercept` 빌드) 둘 중 하나뿐이다. 순수 사용자 모드 소프트웨어(감시·보정 스크립트 포함)로는 원천적으로 불가능하다.
- RAlt(AltGr, 한/영 키)를 리매핑할 때 Alt/Ctrl이 고정되는 문제는 성격이 다르다 — 레이스 컨디션이 아니라 Windows가 생성하는 가짜 LCtrl 이벤트를 정리하지 않은 것이 원인이라, kanata의 `windows-altgr` 옵션 한 줄로 사용자 모드 안에서 완전히 해결된다.
- 같은 "저수준 훅" 카테고리 안에서도 문제의 성격(이벤트 스트림 정리 vs. OS 레벨 상태 레이스)에 따라 해결 가능 여부가 완전히 갈린다는 게 이번 디버깅의 핵심 교훈이었다.

## 참고 문헌

- [KBM: Remapping CapsLock to another key when using RDP incorrectly toggles CapsLock behaviour · Issue #7302, microsoft/PowerToys](https://github.com/microsoft/PowerToys/issues/7302)
- [Caps Lock status change isn't synced to client - Windows Server, Microsoft Learn](https://learn.microsoft.com/en-us/troubleshoot/windows-server/remote/caps-lock-key-status-not-synced-to-client)
- [Best practice for custom shiftable keys · jtroo/kanata Discussion #1675](https://github.com/jtroo/kanata/discussions/1675)
- [kanata 공식 설정 가이드 (config.adoc)](https://github.com/jtroo/kanata/blob/main/docs/config.adoc)
- [kanata GitHub 저장소](https://github.com/jtroo/kanata)
