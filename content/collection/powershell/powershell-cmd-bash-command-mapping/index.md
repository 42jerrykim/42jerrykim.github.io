---
draft: true
collection_order: 121
slug: powershell-cmd-bash-command-mapping
title: "[PowerShell] 부록. PowerShell ↔ CMD/Bash 명령어 대응표"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell cmdlet과 그에 대응하는 Windows CMD 명령어·Linux Bash 명령어를 파일·프로세스·네트워크·사용자 관리 등 실무 카테고리별로 정리한 부록으로, 세 셸을 오가야 하는 독자를 위한 빠른 색인이다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- CMD
- Bash
- Linux(리눅스)
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
- Command-Line
- Terminal
- Text-Processing
- Rosetta-Stone
image: "wordcloud.png"
---

"파워셸 명령어 cmd 대응"이나 "PowerShell 대신 bash로 뭘 써야 하지"를 검색해서 이 글을 찾았다면, 세 셸(PowerShell, CMD, Bash) 중 하나에는 이미 익숙하고 나머지 하나로 같은 작업을 어떻게 하는지 빠르게 찾고 싶은 상황일 것이다. 이 부록은 [PowerShell 컬렉션](/post/powershell/getting-started-powershell/) 120개 챕터, [CMD 컬렉션](/post/cmd/getting-started-cmd/) 85개 챕터, [Bash Shell 컬렉션](/post/bashshell/getting-started-bash-shell/) 44개 챕터에서 각각 다룬 명령어를 같은 작업 기준으로 나란히 배치한 색인이다.

개별 명령어의 옵션·예시·주의사항 같은 상세 내용은 각 컬렉션의 해당 챕터에서 다루므로, 이 글에서는 "이 작업을 PowerShell/CMD/Bash 각각에서 어떻게 하는가"를 한 표에서 바로 대조하는 데 집중한다.

---

## 세 셸의 근본적인 차이를 먼저 이해해야 이 표가 의미 있다

이 대응표를 "왼쪽 명령어 대신 오른쪽 명령어를 넣으면 똑같이 동작한다"는 뜻으로 읽으면 안 된다. [10장](/post/powershell/powershell-pipeline-object-model-not-text/)에서부터 강조했듯, CMD와 Bash는 명령의 출력을 **텍스트 스트림**으로 주고받는 반면 PowerShell은 **.NET 객체**를 그대로 주고받는다. `Get-ChildItem`이 반환하는 것은 `FileInfo` 객체 목록이지 `dir`이 화면에 찍는 텍스트 줄이 아니며, 이 차이는 파이프라인 뒤에 다른 명령을 연결할 때 특히 두드러진다 — CMD·Bash에서는 `dir`/`ls`의 출력을 다시 파싱해야 파일 크기나 수정 시각을 뽑아낼 수 있지만, PowerShell에서는 `Get-ChildItem | Where-Object Length -gt 1MB`처럼 객체의 속성에 곧바로 접근한다.

또한 CMD와 Bash도 서로 다르다. CMD는 Windows 전용 텍스트 기반 셸이고, Bash는 POSIX 계열 유닉스 셸의 사실상 표준이다. 아래 표에서 "CMD"와 "Bash" 열이 같은 이름의 명령어를 갖는 경우(`dir`처럼)도 있지만, 옵션 문법과 세부 동작은 거의 항상 다르다는 점을 함께 감안해야 한다.

| 구분 | 실행 단위 | 데이터 형식 | 주 사용 환경 |
|---|---|---|---|
| PowerShell | cmdlet(`.NET` 메서드 호출) | 객체(object) | Windows/Linux/macOS(PowerShell 7) |
| CMD | 내부 명령어 + 외부 실행 파일 | 텍스트 | Windows 전용 |
| Bash | 셸 내장 명령어 + 외부 실행 파일 | 텍스트 | Linux/macOS/WSL |

## 파일·디렉터리 조작

세 셸 모두에서 가장 먼저 배우고 가장 자주 쓰는 명령이 모여 있는 범주다. 이름만 다를 뿐 개념 자체는 거의 그대로 대응하지만, PowerShell 쪽 cmdlet 이름은 뒤에서 다룰 별칭(`ls`, `cat` 등)으로도 호출할 수 있다는 점이 CMD·Bash 경험자에게 실질적인 진입 장벽을 낮춰준다.

| 작업 | PowerShell | CMD | Bash |
|---|---|---|---|
| 목록 조회 | `Get-ChildItem`(`gci`, `ls`, `dir`) | `dir` | `ls` |
| 디렉터리 이동 | `Set-Location`(`cd`, `sl`) | `cd` | `cd` |
| 디렉터리 생성 | `New-Item -ItemType Directory` | `mkdir`(`md`) | `mkdir` |
| 디렉터리 삭제 | `Remove-Item -Recurse` | `rmdir /s`(`rd`) | `rm -r` |
| 파일 복사 | `Copy-Item` | `copy`/`xcopy` | `cp` |
| 파일 이동 | `Move-Item` | `move` | `mv` |
| 파일 삭제 | `Remove-Item` | `del`(`erase`) | `rm` |
| 파일 이름 변경 | `Rename-Item` | `ren` | `mv`(원본과 대상이 같은 디렉터리) |
| 내용 출력 | `Get-Content`(`cat`, `gc`) | `type` | `cat` |
| 존재 확인 | `Test-Path` | `if exist` | `test -e`(`[ -e ]`) |
| 트리 구조 표시 | `Get-ChildItem -Recurse \| Format-Wide` | `tree` | `tree`(별도 패키지) |
| 심볼릭 링크 생성 | `New-Item -ItemType SymbolicLink` | `mklink` | `ln -s` |

## 텍스트 검색·처리

이 범주는 PowerShell과 CMD/Bash의 격차가 가장 크게 드러나는 영역이다. `grep`·`sed`·`awk`는 Bash 생태계에서 독립적으로 발전해 온 강력한 텍스트 처리 도구인 반면, CMD는 `findstr` 외에는 표준으로 제공하는 대안이 거의 없다. PowerShell은 `-replace`나 `-split` 같은 연산자를 언어 자체에 내장해, 별도 외부 도구 없이도 비슷한 작업을 처리할 수 있게 한다.

| 작업 | PowerShell | CMD | Bash |
|---|---|---|---|
| 문자열 검색 | `Select-String`(`sls`) | `findstr` | `grep` |
| 텍스트 치환 | `-replace` 연산자([47장](/post/powershell/match-replace-regex-powershell/)) | (내장 없음, `for` + 변수 치환 우회) | `sed` |
| 줄 정렬 | `Sort-Object` | `sort` | `sort` |
| 중복 제거 | `Sort-Object -Unique`(`Get-Unique`) | (내장 없음) | `uniq` |
| 줄 수 세기 | `Measure-Object -Line` | `find /c /v ""` | `wc -l` |
| 필드 추출 | `-split` 연산자 + 인덱싱 | (내장 없음, 별도 파싱 필요) | `awk`/`cut` |
| 페이지 단위 출력 | `Out-Host -Paging` | `more` | `less`/`more` |

## 프로세스·서비스 관리

Windows의 "서비스"와 Linux의 "systemd 유닛"은 이름은 다르지만 둘 다 "부팅 시 자동으로 시작해 백그라운드에서 계속 실행되는 프로그램"이라는 같은 개념을 가리킨다. 다만 Linux 배포판에 따라 systemd 대신 다른 init 시스템(OpenRC 등)을 쓰는 경우도 있어, Bash 열의 명령어가 모든 Linux 환경에 그대로 적용되지는 않는다는 점을 감안해야 한다.

| 작업 | PowerShell | CMD | Bash |
|---|---|---|---|
| 프로세스 목록 | `Get-Process`(`gps`, `ps`) | `tasklist` | `ps` |
| 프로세스 종료 | `Stop-Process`(`kill`) | `taskkill` | `kill` |
| 새 프로세스 시작 | `Start-Process` | `start` | `&`(백그라운드 실행) |
| 서비스 목록·상태 | `Get-Service` | `sc query` | `systemctl status`(systemd 기준) |
| 서비스 시작·중지 | `Start-Service`/`Stop-Service` | `net start`/`net stop` | `systemctl start`/`stop` |
| 예약 작업 등록 | `Register-ScheduledTask` | `schtasks` | `crontab -e` |

## 네트워크

네트워크 진단 명령어는 세 셸 모두 이름 자체는 오래전부터 관습적으로 통일돼 온 편이다(`ping`이 대표적이다). 다만 [109장](/post/powershell/test-connection-ping-powershell/)에서 다뤘듯 PowerShell의 `Test-Connection`은 같은 이름의 결과를 텍스트가 아닌 객체로 반환한다는 차이가 여기서도 그대로 적용된다.

| 작업 | PowerShell | CMD | Bash |
|---|---|---|---|
| ping 테스트 | `Test-Connection` | `ping` | `ping` |
| IP 구성 확인 | `Get-NetIPConfiguration` | `ipconfig` | `ip addr`(`ifconfig`) |
| DNS 조회 | `Resolve-DnsName` | `nslookup` | `dig`/`nslookup` |
| 연결 상태 확인 | `Get-NetTCPConnection` | `netstat` | `netstat`/`ss` |
| 웹 요청 | `Invoke-WebRequest`/`Invoke-RestMethod` | (내장 없음, 별도 도구 필요) | `curl`/`wget` |
| 파일 전송(원격 세션) | `Copy-Item -ToSession` | (내장 없음) | `scp` |

## 사용자·권한 관리

로컬 컴퓨터 하나의 계정을 다루는 명령은 세 셸 모두에 대응 항목이 있지만, [17부](/post/powershell/activedirectory-module-get-aduser-powershell/)에서 다룬 도메인 전체의 Active Directory 계정 관리로 넘어가면 이야기가 달라진다. CMD·Bash 어느 쪽에도 AD에 정확히 대응하는 표준 개념이 없어, 이 부분은 아래 표에서도 "PowerShell만의 영역"으로 남는다.

| 작업 | PowerShell | CMD | Bash |
|---|---|---|---|
| 로컬 사용자 목록 | `Get-LocalUser` | `net user` | `cat /etc/passwd`(`getent passwd`) |
| 사용자 생성 | `New-LocalUser` | `net user /add` | `useradd` |
| 그룹 구성원 추가 | `Add-LocalGroupMember` | `net localgroup` | `usermod -aG` |
| 파일 권한 확인·변경 | `Get-Acl`/`Set-Acl` | `icacls` | `ls -l`/`chmod` |
| 관리자 권한 확인 | `[Security.Principal.WindowsPrincipal]` | (내장 없음, `net session`으로 우회) | `id -u`(0이면 root) |
| 도메인 계정 조회 | `Get-ADUser` | `net user /domain` | (AD 개념 자체가 없음, LDAP 도구 별도) |

## 압축·아카이브

파일 압축은 CMD의 공백이 가장 두드러지는 영역 중 하나다. Windows 탐색기의 GUI 압축 기능과 달리 `cmd.exe` 자체에는 압축·해제를 위한 내장 명령이 전혀 없어, 스크립트에서 압축을 다루려면 PowerShell로 전환하거나 `7-Zip` 같은 외부 도구를 설치해야 한다.

| 작업 | PowerShell | CMD | Bash |
|---|---|---|---|
| 압축 | `Compress-Archive` | (내장 없음, 별도 도구 필요) | `tar -czf`/`zip` |
| 압축 해제 | `Expand-Archive` | (내장 없음, 별도 도구 필요) | `tar -xzf`/`unzip` |

## 환경 변수·시스템 정보

환경 변수를 다루는 문법 자체는 세 셸이 각자 다르게 설계했지만(`$env:`, `%VAR%`, `$VAR`), "현재 세션에서만 유효한 값"이라는 근본 개념은 동일하다. 시스템 정보 조회는 PowerShell의 `Get-ComputerInfo`가 여러 개별 조회를 하나로 요약해 준다는 점에서([97장](/post/powershell/get-computerinfo-system-summary-powershell/)) CMD·Bash의 개별 명령 여러 개를 조합해야 하는 방식과 대조된다.

| 작업 | PowerShell | CMD | Bash |
|---|---|---|---|
| 환경 변수 조회 | `Get-ChildItem Env:` | `set` | `env`/`printenv` |
| 환경 변수 설정(세션 한정) | `$env:VAR = "값"` | `set VAR=값` | `export VAR=값` |
| 시스템 정보 요약 | `Get-ComputerInfo` | `systeminfo` | `uname -a`/`hostnamectl` |
| 설치된 업데이트 | `Get-HotFix` | `wmic qfe list` | `apt list --installed`(배포판별 상이) |
| 디스크 사용량 | `Get-Volume` | `wmic logicaldisk` | `df -h` |

## 패키지·모듈 관리

소프트웨어를 설치하는 방식은 세 셸 중 PowerShell과 Bash가 오히려 더 비슷하다. `winget`·`apt`·`brew` 모두 중앙 저장소에서 패키지를 검색해 의존성까지 함께 설치해 주는 반면, CMD에는 이런 패키지 관리자 개념 자체가 없다.

| 작업 | PowerShell | CMD | Bash |
|---|---|---|---|
| 패키지 설치 | `Install-Package`(PackageManagement)/`winget install` | (내장 없음, `winget`은 별도 실행 파일) | `apt install`/`brew install` |
| 스크립트·모듈 배포 | `Install-Module`(PowerShell Gallery) | (해당 개념 없음) | `pip install`/`npm install`(언어별) |

## 이식성 정리

이 표를 훑어보면 몇 가지 패턴이 드러난다. 첫째, PowerShell은 CMD·Bash 각각의 명령어를 <strong>별칭(alias)</strong>으로 등록해 둔 경우가 많다(`ls`→`Get-ChildItem`, `cat`→`Get-Content`, `ps`→`Get-Process`). 이 별칭 덕분에 CMD·Bash 경험자가 처음 PowerShell을 접했을 때 익숙한 이름으로 최소한의 조작을 시작할 수 있지만, 별칭 뒤에서 실제로 실행되는 것은 텍스트가 아니라 객체를 반환하는 cmdlet이라는 점은 변하지 않는다 — `ls | Where-Object Length -gt 1MB`가 동작하는 것도 이 때문이다.

둘째, CMD 쪽에 "(내장 없음)"으로 표시된 항목이 유독 많다. 압축, 텍스트 치환, HTTP 요청처럼 Bash와 PowerShell에는 표준으로 포함된 기능이 CMD에는 아예 없어 별도 실행 파일이나 우회 스크립트가 필요한 경우다. 이는 CMD가 1980년대 MS-DOS 명령 프롬프트의 연장선에서 최소한의 파일·프로세스 조작만을 목표로 설계됐고, 이후 대대적인 기능 확장 없이 유지보수 모드로 전환됐기 때문이다 — 바로 이 공백을 메우기 위해 등장한 것이 PowerShell이다.

셋째, Active Directory·그룹 정책처럼 조직 전체를 다루는 [17부(엔터프라이즈 디렉터리 관리)](/post/powershell/activedirectory-module-get-aduser-powershell/)의 cmdlet들은 CMD·Bash 어느 쪽에도 직접 대응하는 명령어가 없다. CMD의 `net user /domain`이 부분적으로 비슷한 정보를 보여주지만 어디까지나 조회 수준이고, Bash 진영에는 AD 자체에 대응하는 표준 개념이 없어 LDAP 클라이언트 도구를 별도로 써야 한다. 이런 영역은 애초에 "번역"이 아니라 "PowerShell이 아니면 표준화된 방법이 마땅치 않은 작업"으로 보는 것이 정확하다.

## Reference

- [about_Aliases - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_aliases)
- [PowerShell 컬렉션 00장: PowerShell(파워셸) 완벽 가이드](/post/powershell/getting-started-powershell/)
- [CMD 컬렉션 00장: Windows CMD 완벽 가이드](/post/cmd/getting-started-cmd/)
- [Bash Shell 컬렉션 00장: Bash Shell 완벽 가이드](/post/bashshell/getting-started-bash-shell/)
