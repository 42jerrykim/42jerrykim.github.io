---
title: "[Hyper-V] 가상 머신 해상도 설정: Set-VMVideo 활용 가이드"
date: 2025-05-24
description: "Hyper-V 가상 머신의 해상도를 PowerShell의 Set-VMVideo cmdlet으로 설정하는 방법을 설명한다. 기본 세션에서 고해상도 사용을 위한 비디오 어댑터 구성과 ResolutionType 옵션별 특징을 알아본다. Hyper-V를 이용해서 은행 사이트에 접속하는 경우 해상도를 높여서 사용할 수 있도록 만들어 줄 수 있다."
tags:
- Hyper-V
- PowerShell
- 가상화
- 해상도
- Set-VMVideo
- Hyper-V
- PowerShell
- Virtualization
- Resolution
- Set-VMVideo
- Windows
- VM
- VideoAdapter
- Display
- Configuration
- SystemAdministration
- RemoteDesktop
- RDP
- EnhancedSession
- BasicSession
- Gen1VM
- Gen2VM
- VRAM
- GuestOS
- HostOS
- Linux
- WindowsServer
- SystemManagement
- Hyper-V
- PowerShell
- Set-VMVideo
- 가상 머신
- 비디오 어댑터
- 해상도 설정
- 기본 세션
- 향상된 세션
- RDP
- 원격 데스크톱
- 가상 디스플레이
- VRAM
- 합성 어댑터
- 게스트 OS
- 호스트 OS
- 리눅스
- 윈도우 서버
- 시스템 관리
- 스크립팅
- 시스템 관리자
- 가상화 기술
- 윈도우 관리
- Virtualization
categories: 
- Hyper-V
- Windows
- Virtualization
image: image.png
---

Hyper-V의 기본 세션(Basic Session)은 RDP가 아닌 가상화된 콘솔을 통해 연결되므로, 기본 제공되는 표준 해상도(최대 1920×1080)를 벗어나지 못하는 제약이 있다. 향상된 세션(Enhanced Session)을 사용하면 RDP 기반으로 해상도·디바이스 리디렉션을 자유롭게 조절할 수 있지만, 보안이 중요한 은행 사이트나 금융 서비스에 접속할 때는 보안상의 이유로 향상된 세션을 사용할 수 없다. 이럴 때 PowerShell의 `Set-VMVideo`/`Get-VMVideo` cmdlet을 통해 가상 머신에 직접 최대 해상도를 설정함으로써 기본 세션에서도 더 높은 해상도를 사용할 수 있다.

## Hyper-V 비디오 어댑터 이해

Hyper-V는 호스트에 Synthetic Video Adapter를 에뮬레이션하여 게스트 OS에 가상 비디오 어댑터를 제공한다. 기본 세션에서는 이 어댑터를 통해 전달되는 표준 해상도 목록 중 하나만 선택 가능하며, 동적 크기 조절 기능이 없어 연결 시점에 설정된 해상도로 고정된다.
Gen2 VM일수록 합성 비디오 메모리(VRAM) 크기가 충분해 더 높은 해상도를 지원하며, Gen1 VM은 VRAM 크기 제한으로 인해 최대 해상도가 낮아질 수 있다.

## Set-VMVideo 및 Get-VMVideo 개요

`Get-VMVideo` cmdlet은 지정한 VM의 비디오 설정 정보를 조회하는 방법이다. 예를 들어, 현재 설정된 해상도와 모드 확인을 위해 다음과 같이 실행한다.

```powershell
PS> Get-VMVideo -VMName "VM01"
```

이 명령은 VM01의 `ResolutionType`과 `HorizontalResolution`/`VerticalResolution` 속성 등을 출력한다. 반면 `Set-VMVideo`는 VM의 비디오 해상도를 변경할 때 사용한다. 예를 들어 VM01을 2560x1440 해상도로 설정하려면 다음과 같이 실행하면 된다.

```powershell
PS> Set-VMVideo -VMName "VM01" -HorizontalResolution 2560 -VerticalResolution 1440 -ResolutionType Maximum
```

이때 `-ResolutionType` 옵션을 지정하지 않으면 기본(Default) 모드가 적용되는데, 원하는 해상도가 적용되지 않는 문제가 발생할 수 있다. `Maximum` 옵션을 주어서 원하는 해상도로 설정이 가능하도록 한다.

## ResolutionType 옵션 설명

`Set-VMVideo`의 `-ResolutionType` 파라미터는 설정할 해상도의 허용 범위를 결정하는 것이다. 주요 값은 다음과 같다.

* **Single**: 지정한 해상도만 **고정 해상도**로 사용하는 것이다. 예를 들어 `-ResolutionType Single -HorizontalResolution 1920 -VerticalResolution 1080`으로 설정하면 VM은 오직 1920×1080 해상도만 지원하도록 강제된다.
* **Maximum**: 지정한 해상도를 **최대 해상도**로 설정하며, 그 이하의 표준 해상도는 모두 허용한다. 즉, 예를 들어 3840×2160으로 설정하면 4K까지 지원하고 그보다 작은 해상도들도 선택 가능하다.
* **Default**: Microsoft가 정의한 표준 해상도 목록만 지원하며, 입력된 해상도 값은 무시되는 것이다. 이 모드는 입력 값을 기반으로 동작하지 않고 기본 해상도 리스트만 적용된다.

실제로 고정된 한 가지 해상도만 사용하려면 `Single`을, 가능 범위를 넓히고 싶다면 `Maximum`을 선택한다. 예를 들어 `Single` 옵션은 "유일한 해상도"를 설정할 때 사용하며, **단일 고정 해상도**가 필요한 경우에 적합하다. 반면 `Maximum`은 하나의 최댓값과 이하 해상도를 모두 지원하므로, 호스트 디스플레이 크기에 맞춰 여유를 두고 설정할 때 유용하다. `Default` 모드는 특별히 필요 없을 경우 거의 사용하지 않으며, 기본 값으로 두어도 상관없는 것이다.

## VM 전원 상태 및 사전 준비

`Set-VMVideo` 명령은 **VM이 종료(Off)된 상태**에서만 정상 작동한다. 따라서 VM을 먼저 완전히 종료한 후 관리자 권한으로 PowerShell을 실행해야 한다. 예를 들어 다음 순서로 진행한다.

1. Hyper-V 관리 콘솔이나 PowerShell(`Stop-VM`)을 이용해 대상 VM을 종료한다.
2. **관리자 권한**으로 PowerShell을 실행한다.
3. `Get-VMVideo`로 현재 설정을 확인하여 필요한 정보를 미리 기록한다.

아무리 해상도를 높이더라도 호스트가 지원하는 최대 해상도 이상을 설정하면 화면이 깨질 수 있으므로, 실제 모니터/그래픽카드 지원 범위를 고려한다. 또한 게스트 운영체제 측에서 그래픽 드라이버나 게스트 서비스(Integration Services)가 제대로 설치되어 있어야 한다. 예를 들어 Linux의 경우 `hyperv_fb` 드라이버와 `linux-image-extra-virtual` 패키지가 필요할 수 있고, Windows 게스트는 기본 제공되는 Hyper-V 통합 서비스가 활성화되어야 고해상도를 제대로 표시할 수 있다.

## 해상도 설정 실행 단계

해상도를 변경하는 과정은 다음과 같다:

1. **VM 종료**: 먼저 Hyper-V 관리자를 통해 해당 Windows 11 VM을 종료(Shutdown)한다.
2. **현재 설정 확인**: 호스트의 PowerShell에서 `Get-VMVideo -VMName "<VM이름>"`을 실행하여 현재 비디오 설정(해상도, 유형)을 조회한다.
3. **해상도 설정**: `Set-VMVideo` 명령으로 원하는 해상도를 설정한다. 예를 들어 최대 가능한 해상도를 2560x1440로 변경하고 싶다면 아래와 같이 입력한다.

   ```powershell
   PS> Set-VMVideo -VMName "VM01" -HorizontalResolution 2560 -VerticalResolution 1440 -ResolutionType Maximum
   ```

   필요한 경우 해상도나 `ResolutionType` 값을 변경하여 실행하면 된다. 예를 들어 `Single`으로 설정하려면 `-ResolutionType Single`을 지정하면 된다.
4. **VM 시작 및 적용 확인**: 설정이 완료되면 VM을 다시 시작한다. VM이 부팅되면, 가상 머신의 콘솔이 지정한 해상도로 설정되었는지 확인하는 것이다. Windows 11 게스트의 경우, **설정 > 시스템 > 디스플레이**에서 최대 해상도를 확인하거나, 아래 명령으로 PowerShell에서도 검증할 수 있다(`Get-DisplayResolution`은 일부 Windows Server/Hyper-V 환경에서 사용 가능함).

   ```powershell
   PS> (Get-VMVideo -VMName "VM01").HorizontalResolution
   PS> (Get-VMVideo -VMName "VM01").VerticalResolution
   ```

   위 명령의 출력이 설정한 값(예: 2560, 1440)과 일치하면 성공적으로 적용된 것이다. Linux 게스트의 경우 `xrandr`로 화면 해상도를 확인하거나 해당 OS의 디스플레이 설정을 확인하는 것이다.

## 실행 전후 상태 확인

명령 실행 전후 상태를 비교하여 설정이 올바르게 적용됐는지 점검하는 것이다. **호스트 측**에서는 `Get-VMVideo`를 이용하여 변경 전후 설정을 확인할 수 있는 것이다. 예를 들어:

```powershell
# 실행 전 해상도 확인
PS> Get-VMVideo -VMName "VM01"
HorizontalResolution : 1024
VerticalResolution   : 768
ResolutionType       : Default

# Set-VMVideo 실행 (위 참조)
PS> Set-VMVideo -VMName "VM01" -HorizontalResolution 2560 -VerticalResolution 1440 -ResolutionType Maximum

# 실행 후 해상도 확인
PS> Get-VMVideo -VMName "VM01"
HorizontalResolution : 2560
VerticalResolution   : 1440
ResolutionType       : Maximum
```

또한 `Set-VMVideo`에 `-Passthru` 옵션을 붙이면 명령 실행 시 결과를 바로 확인 할 수 있다. 예를 들어 `Set-VMVideo ... -Passthru`를 실행하면 변경된 `VMVideo` 객체가 출력되어 속성값을 즉시 확인할 수 있다. **게스트 OS 측**에서는 Windows의 경우 `dxdiag` 또는 "디스플레이 설정" 화면, Linux는 `xrandr` 등을 통해 해상도를 확인 할 수 있다.

## 주의사항 및 한계

* **실시간 동적 리사이즈**
  Linux VM의 기본 `hyperv_fb` 드라이버는 실행 중 해상도 변경을 지원하지 않아, 매번 VM 재시작을 필요로 한다.
* **Integration Services**
  Windows 게스트에서는 통합 서비스(Integration Services) 최신화를 권장하며, Linux 게스트는 `linux-vm-tools`(xRDP 포함) 설치 후 향상된 세션 모드를 고려할 수 있다.
* **Gen1 vs Gen2**
  Gen1 VM은 VRAM 크기 제한으로 특정 고해상도가 설정되지 않을 수 있으므로, 가능하다면 Gen2 VM을 사용하는 것이 좋을 것이다.

## 문제 발생 시 대응 방법

설정 후에도 해상도가 변경되지 않거나 에러가 발생할 수 있다. 이런 경우 다음 사항을 점검한다:

* **VM 전원 상태**: VM이 반드시 종료된 상태인지 확인한다. 실행 중인 VM에 적용하려 하면 오류가 발생하거나 변경되지 않는다.
* **권한**: PowerShell을 **관리자 권한**으로 실행했는지 확인한다. Hyper-V 관리 권한이 필요하다.
* **해상도 값 유효성**: 입력한 해상도가 호스트/게스트가 지원하는 범위를 벗어나지 않는지 확인한다. 너무 높은 값을 입력하면 화면에 출력되지 않는다.
* **ResolutionType 확인**: `Default` 모드를 사용했다면 입력값이 무시될 수 있으므로, 원하는 값으로 고정하려면 `Single` 또는 `Maximum` 모드를 사용한다.
* **게스트 드라이버**: Windows나 Linux 게스트의 Hyper-V 통합 서비스/드라이버가 최신인지, 특히 Linux VM의 경우 `hyperv_fb` 관련 커널 모듈이 로드되어 있는지 확인한다. 게스트 서비스 미설치는 화면 해상도 인식에 문제를 줄 수 있다.
* **다중 모니터**: 기본 세션 모드는 다중 디스플레이를 지원하지 않으므로, 단일 모니터 환경으로 테스트한다.
* **다시 적용**: 가끔 설정 후 VM을 완전 종료(Shutdown)하고, 호스트를 재부팅하거나 다시 시도하면 정상 적용되는 경우도 있다.

이 외에도 필요 시 **원격 데스크톱(RDP)** 같은 다른 접속 방법을 고려할 수 있는 것이다. 실제로 기본 세션에서 원하는 해상도를 얻지 못하면, 고급 세션 모드나 RDP를 통해 자동 리사이징 기능을 사용하는 것도 한 방법인 것이다.

## 결론

PowerShell의 `Set-VMVideo`/`Get-VMVideo`를 활용하면 Enhanced Session이 지원되지 않는 환경에서도 기본 세션 해상도 제한을 넘어설 수 있다. 해상도를 변경할 때는 VM 종료 후 적용하며, `ResolutionType` 옵션을 적절히 조합해 최적의 사용자 경험을 구현할 수 있다.

## 참고

* [Set-VMVideo (Hyper-V) documentation](https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmvideo?view=windowsserver2025-ps)
* [Get-VMVideo (Hyper-V) documentation](https://learn.microsoft.com/en-us/powershell/module/hyper-v/get-vmvideo?view=windowsserver2025-ps)
* [Limitations of the video driver (hyperv\_fb.c) in Linux Integration Services](https://github.com/LIS/lis-next/issues/318)
* [How to get the right Hyper-V window size in Windows 11 (TechTarget)](https://www.techtarget.com/searchvirtualdesktop/tutorial/How-to-get-the-right-Hyper-V-window-size-in-Windows-11)
