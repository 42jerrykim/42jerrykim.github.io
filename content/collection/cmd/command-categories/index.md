---
draft: true
title: "[CMD] 명령어 종류 총정리 - 카테고리별 핵심 명령어 가이드"
description: "Windows CMD 명령어를 파일·디렉터리 조작, 디스크, 프로세스·서비스, 네트워크, 시스템 정보, 사용자·권한, 배치 스크립팅 등 실무 카테고리별로 정리했습니다. 각 명령어의 역할과 기본 사용법을 한눈에 확인할 수 있습니다."
date: 2026-07-22
lastmod: 2026-07-22
categories: CMD
image: "wordcloud.png"
tags:
- Windows(윈도우)
- Shell(셸)
- Terminal
- OS(운영체제)
- Process
- File-System
- Permission
- Automation(자동화)
- Networking(네트워킹)
- PATH
- Environment
- Backup
- Tutorial(튜토리얼)
- Guide(가이드)
- Quick-Reference
- Productivity(생산성)
- Education(교육)
- Troubleshooting(트러블슈팅)
- Workflow(워크플로우)
- Configuration(설정)
- Technology(기술)
- How-To
- Tips
- Comparison(비교)
- Reference(참고)
- Beginner
- Advanced
- Documentation(문서화)
- Best-Practices
---

"cmd 명령어 종류"를 검색해서 이 글을 찾았다면, 아마도 눈에 익은 명령어 몇 개를 넘어 CMD 전체를 체계적으로 파악하고 싶을 것이다. Windows 명령 프롬프트(cmd.exe)는 100개가 넘는 내장 명령어를 가지고 있지만, 실무에서 자주 쓰는 것은 그중 일부이며 나머지는 역할에 따라 몇 개의 큰 카테고리로 묶인다. 이 글은 그 카테고리를 기준으로 명령어를 분류하고, 각 명령어의 역할과 최소한의 사용법을 정리한 색인이다.

개별 명령어의 옵션·예시·주의사항 같은 상세 내용은 이 컬렉션의 각 명령어별 글에서 다루므로, 이 글에서는 "이 작업을 하려면 어떤 명령어를 써야 하는가"를 빠르게 찾는 데 집중한다.

---

## CMD 명령어의 기본 구조

CMD는 크게 두 종류의 명령어를 실행한다. 하나는 cmd.exe 프로세스 안에 내장된 **내부 명령어(internal command)**로, `cd`·`dir`·`echo`·`set`처럼 별도의 실행 파일 없이 셸 자체가 처리한다. 다른 하나는 `xcopy.exe`·`robocopy.exe`·`chkdsk.exe`처럼 `%SystemRoot%\System32` 등 PATH 상의 디렉터리에 실제 실행 파일로 존재하는 **외부 명령어(external command)**다. 사용자 입장에서는 둘 다 프롬프트에 입력해 실행하는 명령어일 뿐이지만, 외부 명령어는 `where robocopy`처럼 파일 경로를 조회할 수 있고 내부 명령어는 그럴 수 없다는 차이가 있다.

이 구분보다 실무에서 더 중요한 것은 **명령어가 다루는 대상이 무엇인가**다. 파일 하나를 다루는지, 디스크 전체를 다루는지, 실행 중인 프로세스를 다루는지, 네트워크 너머의 다른 컴퓨터를 다루는지에 따라 명령어를 찾는 카테고리가 달라진다. 아래 표는 이 기준으로 명령어를 분류한 것이다.

| 카테고리 | 다루는 대상 | 대표 명령어 |
|---|---|---|
| 파일·디렉터리 조작 | 파일 시스템의 파일·폴더 | dir, copy, xcopy, robocopy, move, del, ren |
| 디스크·볼륨 관리 | 물리 디스크·파티션·볼륨 | chkdsk, diskpart, format, fsutil |
| 프로세스·서비스 관리 | 실행 중인 프로그램·백그라운드 서비스 | tasklist, taskkill, sc, schtasks |
| 사용자·권한 관리 | 파일 ACL·접근 권한 | icacls, cacls, openfiles |
| 시스템 정보·구성 | OS 버전·드라이버·환경 설정 | systeminfo, driverquery, mode, wmic |
| 네트워크 | 네트워크 인터페이스·연결 상태 | ipconfig, ping, netstat, nslookup |
| 배치 스크립팅 | 조건 분기·반복·변수 처리 | if, for, call, set, goto |

이제 각 카테고리를 순서대로 살펴본다.

---

## 파일·디렉터리 조작 명령어

파일 시스템에서 파일과 폴더를 만들고, 옮기고, 지우고, 내용을 들여다보는 명령어들이다. 유닉스 계열의 `ls`·`cp`·`mv`·`rm`에 각각 대응하는 명령어가 있다고 생각하면 빠르게 감을 잡을 수 있다.

| 명령어 | 역할 |
|---|---|
| [dir](/post/cmd/dir/) | 디렉터리 안의 파일·하위 디렉터리 목록을 표시 |
| [cd](/post/cmd/cd/) | 현재 디렉터리를 표시하거나 변경 |
| md (mkdir) | 디렉터리를 생성 |
| [rmdir](/post/cmd/rmdir/) (rd) | 디렉터리를 삭제 |
| [copy](/post/cmd/copy/) | 파일을 다른 위치로 복사 |
| [xcopy](/post/cmd/xcopy/) | 디렉터리 트리를 포함해 파일을 복사 |
| [robocopy](/post/cmd/robocopy/) | 재시작·재시도·미러링을 지원하는 고급 복사 유틸리티 |
| [move](/post/cmd/move/) | 파일·디렉터리를 다른 위치로 이동 |
| [del](/post/cmd/del/) (erase) | 파일을 삭제 |
| [ren](/post/cmd/ren/) (rename) | 파일 이름을 변경 |
| [type](/post/cmd/type/) | 텍스트 파일 내용을 화면에 출력 |
| [tree](/post/cmd/tree/) | 디렉터리 구조를 트리 형태로 표시 |
| [attrib](/post/cmd/attrib/) | 파일 속성(읽기 전용·숨김 등)을 표시·변경 |
| [comp](/post/cmd/comp/) | 두 파일을 바이트 단위로 비교 |
| [fc](/post/cmd/fc/) | 두 파일의 내용 차이를 줄 단위로 표시 |
| [find](/post/cmd/find/) | 파일이나 출력에서 문자열을 검색 |
| [findstr](/post/cmd/findstr/) | 정규식을 지원하는 문자열 검색 |
| [mklink](/post/cmd/mklink/) | 심볼릭 링크·하드 링크를 생성 |
| [replace](/post/cmd/replace/) | 대상 디렉터리의 파일을 원본 파일로 교체 |
| [sort](/post/cmd/sort/) | 텍스트 입력을 정렬해 출력 |
| [more](/post/cmd/more/) | 긴 출력을 한 화면씩 나눠 표시 |
| [pushd-popd](/post/cmd/pushd-popd/) | 현재 디렉터리를 스택에 저장하고 복원 |
| [path](/post/cmd/path/) | 실행 파일 검색 경로(PATH)를 표시·설정 |

```
xcopy C:\source D:\backup /s /e /i
del *.tmp /s
findstr /s /i "TODO" *.cpp
```

`del`·`ren`처럼 대상을 되돌릴 수 없는 명령어는 와일드카드(`*`)를 쓰기 전에 `dir` 등으로 대상을 먼저 확인하는 습관을 들이는 것이 안전하다.

## 디스크·볼륨 관리 명령어

파일 하나가 아니라 디스크 전체나 파티션, 파일 시스템 속성을 다루는 명령어들이다. 관리자 권한이 필요한 경우가 많고, 잘못 사용하면 데이터 손실로 이어질 수 있으므로 실행 전 대상 드라이브 문자를 반드시 재확인해야 한다.

| 명령어 | 역할 |
|---|---|
| [chkdsk](/post/cmd/chkdsk/) | 디스크 오류를 검사하고 상태 보고서를 표시 |
| [chkntfs](/post/cmd/chkntfs/) | 부팅 시 디스크 검사 여부를 표시·변경 |
| [diskpart](/post/cmd/diskpart/) | 디스크 파티션을 대화형으로 관리 |
| [format](/post/cmd/format/) | 드라이브를 지정한 파일 시스템으로 포맷 |
| [convert](/post/cmd/convert/) | FAT 볼륨을 NTFS로 변환 |
| [compact](/post/cmd/compact/) | NTFS 파일·폴더의 압축 상태를 표시·변경 |
| [fsutil](/post/cmd/fsutil/) | 파일 시스템 속성을 조회·구성하는 저수준 도구 |
| [label](/post/cmd/label/) | 디스크 볼륨 레이블을 생성·변경·삭제 |
| [vol](/post/cmd/vol/) | 디스크 볼륨 레이블과 일련번호를 표시 |
| [subst](/post/cmd/subst/) | 경로를 가상 드라이브 문자에 연결 |
| [recover](/post/cmd/recover/) | 손상된 디스크에서 읽을 수 있는 데이터를 복구 |
| [verify](/post/cmd/verify/) | 파일이 디스크에 올바로 기록됐는지 검증할지 설정 |

```
chkdsk C: /f
diskpart
> list disk
> select disk 1
> clean
```

`diskpart`의 `clean`처럼 파티션 테이블 자체를 지우는 명령은 대상 디스크 번호를 잘못 선택하면 다른 드라이브의 데이터가 사라진다. 대화형 세션에 진입한 뒤 `list disk`로 대상을 재확인하고 진행하는 것이 원칙이다.

## 프로세스·서비스 관리 명령어

지금 실행 중인 프로그램과 백그라운드에서 동작하는 Windows 서비스를 조회하고 제어하는 명령어들이다. 유닉스의 `ps`·`kill`에 대응한다.

| 명령어 | 역할 |
|---|---|
| [tasklist](/post/cmd/tasklist/) | 현재 실행 중인 프로세스 목록을 표시 |
| [taskkill](/post/cmd/taskkill/) | 실행 중인 프로세스를 종료 |
| [sc](/post/cmd/sc/) | Windows 서비스를 조회·생성·구성 |
| [schtasks](/post/cmd/schtasks/) | 예약 작업을 생성·조회·삭제 |
| [start](/post/cmd/start/) | 프로그램이나 명령을 별도 창에서 실행 |

```
tasklist | findstr /i "chrome"
taskkill /IM notepad.exe /F
sc query wuauserv
```

`taskkill /F`는 프로세스에 종료 신호를 보내지 않고 강제로 끝내므로, 저장하지 않은 작업이 그대로 사라질 수 있다. 가능하면 `/F` 없이 먼저 시도하고, 응답이 없을 때만 강제 종료를 쓰는 편이 안전하다.

## 사용자·권한 관리 명령어

파일과 디렉터리의 접근 제어 목록(ACL), 그리고 원격 사용자가 열어 둔 파일을 다루는 명령어들이다. 유닉스의 `chmod`·`chown`에 해당하지만, NTFS ACL은 단순한 rwx 비트가 아니라 사용자·그룹별 세분화된 권한 목록이라는 점이 다르다.

| 명령어 | 역할 |
|---|---|
| [icacls](/post/cmd/icacls/) | 파일·디렉터리의 ACL을 표시·수정·백업·복원 |
| [cacls](/post/cmd/cacls/) | ACL을 표시·수정하는 구버전 도구(icacls 권장) |
| [openfiles](/post/cmd/openfiles/) | 파일 공유에서 원격 사용자가 열어 둔 파일을 표시 |

```
icacls "C:\data" /grant Jerry:(OI)(CI)F
icacls "C:\data" /remove Guest
```

Microsoft는 `cacls`를 레거시로 분류하고 신규 스크립트에서는 `icacls` 사용을 권장한다. 두 명령의 옵션 문법이 서로 다르므로 예전 배치 파일을 그대로 재사용할 때는 반드시 옵션 표기를 확인해야 한다.

## 시스템 정보·구성 명령어

OS 버전, 설치된 드라이버, 콘솔 장치 설정처럼 시스템 자체의 상태를 조회하거나 구성하는 명령어들이다.

| 명령어 | 역할 |
|---|---|
| [systeminfo](/post/cmd/systeminfo/) | 컴퓨터의 하드웨어·OS 구성 정보를 표시 |
| [ver](/post/cmd/ver/) | Windows 버전을 표시 |
| [driverquery](/post/cmd/driverquery/) | 설치된 장치 드라이버 상태를 표시 |
| [gpresult](/post/cmd/gpresult/) | 적용된 그룹 정책 정보를 표시 |
| [mode](/post/cmd/mode/) | 콘솔·시리얼 포트 등 시스템 장치를 구성 |
| [wmic](/post/cmd/wmic/) | WMI를 통해 시스템 정보를 조회·제어(레거시, PowerShell 권장) |
| [date-time](/post/cmd/date-time/) | 시스템 날짜·시간을 표시·설정 |
| [chcp](/post/cmd/chcp/) | 활성 코드 페이지 번호를 표시·설정 |
| [color](/post/cmd/color/) | 콘솔의 전경·배경색을 설정 |
| [cls](/post/cmd/cls/) | 화면을 지움 |

```
systeminfo | findstr /i "OS Name"
driverquery /fo table
wmic cpu get name
```

`wmic`은 Windows 10 21H1부터 더 이상 기본 배포에 포함되지 않는 서버 버전이 늘고 있어, Microsoft는 신규 스크립트에서 `Get-CimInstance` 등 PowerShell 대체 명령을 권장한다. 기존 배치 스크립트를 유지 보수하는 상황이 아니라면 새로 작성하는 자동화에는 PowerShell을 우선 고려하는 것이 좋다.

## 네트워크 명령어

네트워크 인터페이스 구성, 연결 상태, 이름 해석을 다루는 명령어들이다. 이 컬렉션은 아직 이 카테고리의 명령어별 상세 글을 따로 다루지 않으므로, 여기서는 Microsoft Learn 명령줄 참조를 기준으로 역할만 소개한다.

| 명령어 | 역할 |
|---|---|
| [ipconfig](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/ipconfig) | 로컬 컴퓨터의 TCP/IP 네트워크 구성 값을 표시 |
| [ping](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/ping) | ICMP 에코 요청으로 대상 호스트와의 연결을 확인 |
| [tracert](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/tracert) | 대상 호스트까지 패킷이 거치는 경로를 추적 |
| [netstat](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/netstat) | 활성 연결과 라우팅 테이블 등 네트워크 통계를 표시 |
| [nslookup](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/nslookup) | DNS 서버에 질의해 도메인·IP 정보를 조회 |
| [getmac](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/getmac) | 네트워크 어댑터의 MAC 주소를 표시 |
| [net-user](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/net-user) | 로컬·도메인 사용자 계정을 추가·수정·조회 |

```
ipconfig /all
ping -n 4 8.8.8.8
netstat -ano | findstr :443
```

## 배치 스크립팅 명령어

`.bat` 파일 안에서 조건 분기, 반복, 변수 처리, 서브루틴 호출을 담당하는 명령어들이다. 이 명령어들 자체는 파일이나 디스크가 아니라 **배치 스크립트의 실행 흐름**을 대상으로 한다는 점에서 앞의 카테고리들과 성격이 다르다.

| 명령어 | 역할 |
|---|---|
| [echo](/post/cmd/echo/) | 메시지를 표시하거나 화면 표시 여부를 설정 |
| [if](/post/cmd/if/) | 조건에 따라 분기 처리 |
| [for](/post/cmd/for/) | 파일 집합·범위를 순회하며 명령을 반복 실행 |
| [call](/post/cmd/call/) | 다른 배치 파일이나 레이블을 하위 루틴처럼 호출 |
| [goto](/post/cmd/goto/) | 지정한 레이블로 실행 흐름을 이동 |
| [set](/post/cmd/set/) | 환경 변수를 표시·설정·제거 |
| [setlocal-endlocal](/post/cmd/setlocal-endlocal/) | 환경 변수 변경 범위를 배치 파일 내로 국한 |
| [shift](/post/cmd/shift/) | 배치 매개변수(%1, %2 ...)의 위치를 한 칸씩 이동 |
| [pause](/post/cmd/pause/) | 처리를 일시 중단하고 메시지를 표시 |
| [exit](/post/cmd/exit/) | cmd.exe 세션이나 배치 스크립트를 종료 |
| [title](/post/cmd/title/) | 콘솔 창의 제목을 설정 |
| [prompt](/post/cmd/prompt/) | 명령 프롬프트 표시 형식을 변경 |
| [break](/post/cmd/break/) | 확장된 Ctrl+C 검사를 설정·해제 |
| [doskey](/post/cmd/doskey/) | 명령줄 기록·매크로를 관리 |
| [rem](/post/cmd/rem/) | 배치 파일에 주석을 작성 |

```bat
@echo off
setlocal
for %%f in (*.log) do (
    if exist "%%f" del "%%f"
)
endlocal
```

`if`·`for`의 비교·순회 구문은 PowerShell이나 유닉스 셸의 문법과 크게 다르므로, 다른 셸 경험이 있는 사람일수록 `if "%VAR%"=="value"`처럼 양쪽에 따옴표를 맞추는 CMD 고유 규칙에 걸려 넘어지기 쉽다.

## 기타 유틸리티 명령어

앞의 카테고리에 딱 들어맞지 않지만 자주 쓰이는 명령어들이다.

| 명령어 | 역할 |
|---|---|
| [assoc](/post/cmd/assoc/) | 파일 확장명과 연결된 파일 형식을 표시·수정 |
| [ftype](/post/cmd/ftype/) | 파일 형식에 연결된 실행 명령을 표시·수정 |
| [bcdboot](/post/cmd/bcdboot/) | 시동 구성 데이터(BCD)를 관리 |
| [bcdedit](/post/cmd/bcdedit/) | 부팅 로더 항목을 설정 |
| [cmd](/post/cmd/cmd/) | Windows 명령 인터프리터의 새 인스턴스를 시작 |
| [help](/post/cmd/help/) | Windows 명령에 대한 도움말 정보를 제공 |
| [graftabl](/post/cmd/graftabl/) | 그래픽 모드에서 확장 문자 세트 표시를 설정 |
| [print](/post/cmd/print/) | 텍스트 파일을 프린터로 인쇄 |

---

## 명령어를 못 찾겠다면

이 표에도 없는 명령어를 찾고 있다면, 두 가지를 확인해 보는 것이 빠르다. 첫째, `help` 명령 뒤에 찾는 명령어 이름을 붙여 실행하면(`help robocopy`) CMD가 자체적으로 알고 있는 명령어인지, 그리고 간단한 사용법을 바로 확인할 수 있다. 둘째, CMD 내장 명령어로 존재하지 않는다면 PowerShell 전용 cmdlet이거나 별도로 설치해야 하는 외부 도구일 가능성이 높다 — Microsoft는 새로운 자동화 스크립트를 작성할 때 CMD 명령어보다 PowerShell cmdlet을 우선 고려할 것을 권장한다.

| 확인할 것 | 방법 |
|---|---|
| CMD 내장 명령어인지 | `help <명령어>` 또는 `<명령어> /?` |
| 외부 실행 파일 경로 | `where <명령어>` |
| PowerShell 대체 명령 | `Get-Command *<키워드>*` (PowerShell에서) |

---

## Reference

- [Windows commands - Windows Server | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/windows-commands)
- [Icacls - Windows Server | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/icacls)
- [Systeminfo - Windows Server | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/systeminfo)
