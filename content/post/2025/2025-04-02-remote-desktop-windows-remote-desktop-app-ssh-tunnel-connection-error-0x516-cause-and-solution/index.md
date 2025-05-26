---
title: "[Remote Desktop] Windows 원격 데스크톱 앱에서 SSH 터널 연결 시 오류 0x516 발생 원인 및 해결"
categories:
- Remote Desktop
tags: 
  - Windows
  - Remote Desktop
  - SSH
  - UWP
  - 오류 코드
  - 원격 데스크톱
  - SSH
  - 터널링
  - UWP
  - 오류 코드
  - 0x516
  - 포트 포워딩
  - MSTSC
  - 클라이언트
  - RDP
  - 로컬
  - 루프백
  - Microsoft Store
  - 앱
  - 보안
  - 샌드박스
  - 기술 커뮤니티
  - 문제 해결
  - 명령 프롬프트
  - PowerShell
  - 관리자 권한
  - CheckNetIsolation
  - 예외 설정
  - 개발자 도구
  - 커뮤니티 보고
  - 네트워크 고립
  - 원인 분석
  - Remote
  - Desktop
  - SSH
  - Tunneling
  - Error
  - Code
  - 0x516
  - Windows
  - UWP
  - Microsoft
  - Network
  - Isolation
  - Loopback
  - CheckNetIsolation
  - PowerShell
  - Command
  - Prompt
  - Administrator
  - Exception
  - Security
  - Sandbox
  - Community
  - Troubleshooting
  - Developer
  - Tools
date: 2025-04-02
last_modified_at: 2025-04-02
description: Windows 원격 데스크톱 UWP 앱에서 SSH 터널링 연결 시 발생하는 0x516 오류의 원인과 해결 방법을 설명한다. UWP 앱의 네트워크 격리 정책으로 인해 localhost 접근이 차단되어 발생하는 문제이며, CheckNetIsolation 도구를 사용한 루프백 예외 설정으로 해결할 수 있다.
image: index.png
---


Windows 11 환경에서 SSH 터널링으로 원격지 네트워크에 연결한 뒤 원격 PC로 RDP 접속을 시도할 때 문제가 발생했다. 예를 들어, 로컬 PC에서 `ssh -L 3389:원격PC:3389 사용자명@서버` 명령으로 로컬 포트 3389를 원격 PC의 3389번 포트로 포워딩한 뒤, Microsoft Store 버전의 Remote Desktop(UWP) 앱에서 `localhost:3389`로 접속을 시도하면 “다른 연결로 인해 원격 컴퓨터와의 연결이 종료되었습니다. 오류 코드: 0x516, 확장 오류 코드: 0x0”라는 메시지와 함께 연결이 실패했다. 반면 기존의 mstsc.exe(데스크톱 RDP 클라이언트)로 동일하게 `localhost:3389`에 연결하면 정상 접속된다. 즉, 전통적인 Win32 RDP 클라이언트는 SSH 포워딩된 로컬 포트로 접속이 가능하지만, Microsoft Store에서 제공하는 UWP RDP 앱에서는 동일한 구성으로 연결이 안되는 문제가 발생한다..

## 오류 코드 0x516의 의미

오류 코드 0x516(Extended error code 0x0)는 RDP 연결 실패 시 나타나는 일반적인 오류 코드다. Microsoft Q\&A에 따르면 “오류 코드 0x516은 서버와 클라이언트 간 통신 문제로 발생하는 경우가 많으며, 잘못된 IP, 비활성 또는 차단된 포트, 인증 프로토콜 불일치, 또는 다른 사용자의 이미 연결된 세션” 등이 원인이 될 수 있다고 한다. 즉, 오류 메시지에 적힌 “다른 연결이 이루어져 연결이 종료되었다”는 문구는 원격 PC에 다른 사용자의 접속이 감지되었음을 의미하는 듯 보이지만, 실제로는 네트워크 연결 자체가 이루어지지 않았을 때도 이 메시지가 출력될 수 있다. Extended error code 0x0은 추가적인 상세 오류 정보가 없음을 나타낸다.

## MSTSC와 UWP 앱의 차이점: AppContainer 격리와 루프백 제한

왜 mstsc.exe 클라이언트에서는 문제가 없고 UWP 앱에서만 실패할까? 그 원인은 UWP 앱의 네트워크 격리 때문이다. UWP 앱은 **AppContainer**라는 샌드박스 환경에서 실행되며, 기본적으로 자신이 설치된 장치의 네트워크(특히 루프백 주소)에 접근할 수 없도록 되어 있다. 공식 문서에도 “보안상의 이유로, 일반적인 방법으로 설치된 UWP 앱은 자신이 설치된 디바이스로의 네트워크 호출을 할 수 없다”라고 명시되어 있다. 즉, UWP 앱은 개발 환경이 아닌 상태에서는 `127.0.0.1` 같은 로컬 주소로 접속이 차단된다. 반면 mstsc.exe는 Win32 애플리케이션으로 이런 격리 규칙을 받지 않으므로, SSH 터널로 만들어진 로컬 포트에도 정상 접근이 가능하다. 이 때문에 동일한 포트 번호로 RDP를 시도해도, UWP 앱 쪽에서는 네트워크 연결이 막혀 0x516 오류가 발생하는 것이다.

이러한 네트워크 격리 문제는 Microsoft 테크 커뮤니티와 StackOverflow 등 여러 곳에서 언급되었다. 예를 들어 StackOverflow 답변에서는 “AppContainer 네트워크 격리는 기능이지 버그이며, 기본적으로 UWP 앱은 자신이 설치된 장치로 네트워크 호출을 할 수 없다”라고 설명하고 있다. 또한 Microsoft Learn 공식 문서도 디버깅 옵션에서 “로컬 네트워크 루프백 허용(Allow local network loopback)” 설정을 통해 예외를 적용할 수 있음을 안내하고 있다. 이처럼 UWP 앱의 기본 동작이 루프백을 차단하는 것이 문제의 원인임이 여러 경로로 확인되었다.

## 해결 방법: 루프백 예외 부여

해결책은 UWP 앱에 로컬 루프백 접근 권한을 부여하는 것이다. Windows에는 **CheckNetIsolation** 도구로 개별 앱에 루프백 예외를 설정할 수 있다. 콘솔에서 관리자 권한으로 다음 명령을 실행하면 된다:

```bat
checknetisolation LoopbackExempt -a -n=Microsoft.RemoteDesktop_8wekyb3d8bbwe
```

여기서 `Microsoft.RemoteDesktop_8wekyb3d8bbwe`는 Microsoft Store版 Remote Desktop 앱의 패키지 가족 이름(PackageFamilyName)이다. 이 명령은 해당 앱을 루프백 예외 대상에 추가한다. 만약 정확한 패키지 이름을 모른다면 PowerShell에서 `Get-AppxPackage *RemoteDesktop*` 등을 실행하여 FamilyName을 확인할 수 있다. 명령이 정상 실행되었다면, `checknetisolation LoopbackExempt -s`로 현재 설정된 예외 목록을 확인해 볼 수 있다.

루프백 예외 부여 후 UWP 앱을 재실행하여 다시 접속을 시도하면, 이제는 로컬 포트(127.0.0.1)를 통한 RDP 연결이 정상적으로 이루어진다. 즉, AppContainer 격리 정책으로 인해 차단되던 네트워크가 허용되기 때문에 기존 오류가 발생하지 않는다.

## 문제 재현 및 확인 절차

1. **SSH 터널 설정**: 로컬 머신에서 `ssh -L 3389:원격PC:3389 사용자@호스트` 명령으로 로컬 포트 3389를 원격 PC의 3389번 포트로 포워딩한다.
2. **mstsc 테스트**: `mstsc /v:127.0.0.1:3389` 명령으로 mstsc를 통해 로컬 포트(127.0.0.1:3389)로 접속해본다. 이때는 정상적으로 원격 데스크톱 화면이 나타나야 한다.
3. **Store 앱 테스트**: Microsoft Store 버전 Remote Desktop 앱을 열고 동일하게 `127.0.0.1:3389`로 연결을 시도한다. 이 과정에서 “오류 코드 0x516” 메시지와 함께 연결이 종료되는 것을 확인할 수 있다.
4. **루프백 예외 설정**: 앞서 설명한 `checknetisolation LoopbackExempt -a -n=Microsoft.RemoteDesktop_8wekyb3d8bbwe` 명령을 관리자 권한으로 실행하여, UWP 앱에 루프백 예외를 추가한다.
5. **재접속 확인**: 예외 적용 후 동일하게 Store 앱에서 `127.0.0.1:3389`로 다시 연결하면, 정상적으로 원격지 PC에 접속됨을 확인할 수 있다.

## 결론

본 사례의 핵심 원인은 **UWP 앱의 루프백 주소 접근 제한**이다. Windows의 AppContainer 격리 정책으로 인해, Microsoft Store 버전의 Remote Desktop 앱은 기본 설정으로 로컬호스트(127.0.0.1) 연결이 차단된다. 전통적인 mstsc.exe 클라이언트는 이런 제약이 없으므로 SSH 터널링 환경에서도 정상 동작하는 반면, UWP 앱은 연결 시도를 할 수 없다. 해결 방법은 CheckNetIsolation 도구를 사용하여 해당 UWP 앱에 루프백 예외를 부여하는 것이다. 이 단계를 거치면 UWP 앱에서도 로컬 포트를 통한 RDP 연결이 가능해져 오류 0x516가 해결된다.

## 참고

Microsoft 공식 문서 및 기술 Q\&A/커뮤니티 사례를 참고하여 작성했다.

* https://serverfault.com/questions/1098656/remote-desktop-app-store-version-cant-connect-to-localhost
* https://learn.microsoft.com/en-us/answers/questions/1166478/what-other-connection-causes-error-code-0x516-usin
* https://stackoverflow.com/questions/34589522/cant-see-localhost-from-uwp-app
* https://learn.microsoft.com/en-us/windows/uwp/debug-test-perf/deploying-and-debugging-uwp-apps
* https://serverfault.com/questions/1098656/remote-desktop-app-store-version-cant-connect-to-localhost
* https://stackoverflow.com/questions/33259763/uwp-enable-local-network-loopback
* https://www.reddit.com/r/Windows10/comments/nhw6kn/microsoft_remote_desktop_ignores_ipv4_when_ipv6/