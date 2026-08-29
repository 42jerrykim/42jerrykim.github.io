---
draft: false
collection_order: 0
slug: getting-started-cmd
title: "[CMD] 00. 과정 개요와 커리큘럼"
date: 2026-08-28
lastmod: 2026-08-28
description: "Windows CMD 85챕터 커리큘럼의 과정 개요. PowerShell 시대에도 CMD를 알아야 하는 이유, 9개 Part 학습 순서의 설계 근거, 00-84장 전체 목차, 선수 지식과 완주 후 갖추는 실무 역량을 정리한 과정 개요 챕터다."
categories:
- CMD
tags:
- Windows(윈도우)
- Shell(셸)
- Terminal
- Command
- Automation(자동화)
- File-System
- Process
- System-Design
- Guide(가이드)
- Education(교육)
- Career(커리어)
- Productivity(생산성)
- Beginner
- DevOps
- Networking(네트워킹)
- PowerShell
- Configuration(설정)
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Quick-Reference
- Best-Practices
- Workflow(워크플로우)
- Comparison(비교)
- Reference(참고)
- How-To
- Tips
- Curriculum
- Command-Line
- 커리큘럼
- 배치스크립팅
- 명령프롬프트
- 윈도우입문
- 로드맵
image: "wordcloud.png"
---

## 이 장을 읽기 전에

이 챕터는 "CMD" 컬렉션의 첫 챕터이므로 선행 챕터가 없다. 필요한 선수 지식은 이 장의 "선수 지식" 절에서 별도로 정리한다.

난이도는 입문(명령 프롬프트를 처음 열어보는 수준)에서 중급(9개 Part의 순서 논리와 PowerShell·유닉스 셸과의 위치 관계를 판단할 수 있는 수준) 사이를 오간다. 특정 명령어의 옵션이나 실행 예시는 다루지 않는다. 이 장은 지도(map)이지 명령어 레퍼런스가 아니다.

이 장이 다루지 않는 것은 다음과 같다. `dir`·`copy`처럼 개별 명령어의 옵션과 예시는 01장 이후 각 번호 챕터에서 다룬다. 배치 스크립팅 문법(`if`, `for`, 변수 확장 등)은 4부(30–41장)에서, 디스크·파티션 조작처럼 되돌리기 어려운 명령은 5부(42–53장)에서 각각 독립된 챕터로 다룬다. 이 장에서는 "왜 이런 순서로 배워야 하는가"와 "PowerShell이 있는데도 왜 CMD를 배워야 하는가"만 설명한다. 이 컬렉션은 대화형 CMD 사용과 배치 스크립팅 기초에 범위를 한정한다 — PowerShell cmdlet 문법이나 WMI/CIM 심화 조회처럼 별도의 거대한 생태계를 이루는 주제는 이 컬렉션의 범위 밖이며, 각 챕터의 "이식성" 절에서 PowerShell 대응 명령을 짧게 언급하는 선에서 그친다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| 명령 프롬프트가 처음인 완전 초보자 | 전체를 순서대로 | CMD가 왜 필요한지, 어디서부터 시작해야 하는지 이해한다 |
| Bash/PowerShell 등 다른 커맨드라인 경험자 | 도입, 핵심 개념, 비교/트레이드오프 | 이미 아는 커맨드라인 개념이 CMD 생태계 어디에 대응하는지 파악한다 |
| 명령어를 몇 개 알고 레퍼런스를 찾으러 온 실무자 | 커리큘럼 전체 구성 표, 또는 [명령어 종류 총정리](/post/cmd/command-categories/) | 자신이 아는 명령어가 몇 장인지, 카테고리별로 빠르게 찾을 명령어가 무엇인지 확인한다 |
| 레거시 배치 스크립트를 유지 보수해야 하는 담당자 | 4부(배치 스크립팅), 5부(디스크 관리) | 기존 `.bat` 파일을 읽고 안전하게 수정할 최소 지식을 갖춘다 |

## 도입

"CMD는 죽은 기술 아닌가"라는 질문을 자주 받지만, cmd.exe는 여전히 모든 Windows 설치본(Server Core 포함)에 기본 탑재되어 있고, 수십 년간 쌓인 `.bat`/`.cmd` 빌드·배포 스크립트가 지금도 조직 곳곳에서 그대로 실행되고 있다. PowerShell이 객체 기반 파이프라인과 풍부한 cmdlet으로 새 자동화의 기본값이 된 것은 사실이지만, 그것이 CMD를 읽고 고칠 줄 아는 능력을 불필요하게 만들지는 않는다. 레거시 배치 파일 하나가 배포 파이프라인 한가운데 끼어 있을 때, PowerShell만 아는 사람은 그 스크립트가 왜 조용히 실패하는지 진단할 방법이 없다.

이 컬렉션은 84개 챕터를 명령어 사전순으로 나열하지 않고, 각 챕터가 이전 챕터의 지식을 전제하고 다음 챕터로 자연스럽게 이어지도록 하나의 학습 경로로 설계했다. 내부 명령어와 외부 명령어의 구분, `PATH`와 `doskey` 매크로, 디렉터리 스택(`pushd`/`popd`), ACL 기반 권한 모델, `ERRORLEVEL`과 배치 제어 흐름처럼 개별 명령어만 훑어서는 놓치기 쉬운 핵심 개념도 별도 챕터로 포함했다.

CMD를 배우는 일은 특정 시대의 유물을 익히는 것이 아니라 Windows 환경에서 반복적으로 요구되는 실무 역량이다. 첫째, Windows 서버·CI 러너에서 여전히 대량으로 실행되는 배치 스크립트를 읽고 고치려면 `if`/`for`/`call`/`goto`의 CMD 고유 문법을 알아야 한다. 둘째, GUI가 없거나 원격 세션으로만 접근하는 서버에서 디스크 상태를 점검하고(`chkdsk`, `diskpart`), 서비스를 제어하고(`sc`, `schtasks`), 프로세스를 정리하는(`tasklist`, `taskkill`) 작업은 지금도 CMD 명령이 가장 빠른 경로인 경우가 많다. 셋째, PowerShell을 주력으로 쓰더라도 `cmd /c`로 배치 명령을 호출하거나 레거시 도구와 상호운용해야 하는 상황은 피할 수 없다. 이 세 가지가 이 컬렉션이 9개 Part로 나뉘는 이유이기도 하다 — 각 Part는 이 역량들을 순서대로 습득하도록 설계되어 있다.

## 핵심 개념

<strong>명령 프롬프트(Command Prompt)</strong>는 cmd.exe라는 실행 파일이 제공하는 Windows NT 계열의 명령줄 인터프리터다. MS-DOS·Windows 9x의 COMMAND.COM을 계승하면서도 독립된 프로세스로 동작하며, `SETLOCAL`/`ENDLOCAL`, 지연된 환경 변수 확장 같은 확장 기능을 추가로 제공한다. CMD를 처음 배우는 사람이 가장 먼저 정리해야 할 구분은 <strong>내부 명령어(internal command)</strong>와 <strong>외부 명령어(external command)</strong>다. `cd`·`dir`·`echo`·`set`처럼 cmd.exe 프로세스 안에 내장되어 별도 실행 파일 없이 처리되는 명령이 내부 명령어이고, `xcopy.exe`·`robocopy.exe`·`chkdsk.exe`처럼 `%SystemRoot%\System32` 등 `PATH` 상의 디렉터리에 실제 파일로 존재하는 명령이 외부 명령어다. 이 구분은 `where` 명령으로 실전에서 바로 확인할 수 있다(`where dir`은 실패하고 `where robocopy`는 경로를 반환한다) — 01장에서 이 구분을 CMD 자체를 다루며 더 자세히 짚는다.

이 정신 모델이 커리큘럼 순서를 결정한다. 프롬프트를 오가고 파일을 찾지 못하면(1부) 조작할 대상 자체를 찾을 수 없고, 파일·디렉터리를 다루는 법(2부)과 텍스트를 검색하는 법(3부)을 모르면 배치 스크립트(4부)에서 무엇을 자동화할지 예제로 쓸 재료가 없다. 디스크·파일시스템을 관리하는 법(5부)과 프로세스·권한을 제어하는 법(6부)은 시선을 파일 하나에서 시스템 전체로 넓히고, 시스템 정보를 조회하는 법(7부)은 그 시스템이 지금 어떤 상태인지 진단하는 도구를 더한다. 마지막으로 네트워크(8부)와 부팅·기타 유틸리티(9부)는 로컬 환경을 넘어 원격 시스템과 부팅 구성까지 다루는 영역으로 확장한다.

## 비교/트레이드오프

CMD를 배우는 방식에는 두 갈래가 있고, 이 컬렉션은 둘 다를 지원하도록 설계됐다.

| 구분 | 필요할 때 검색해서 익히기 | 커리큘럼을 순서대로 읽기 |
|---|---|---|
| 장점 | 당장 급한 문제를 가장 빠르게 해결한다 | 빠진 개념 없이 체계적으로 습득하고, PowerShell로 옮겨갈 때 무엇이 대응하는지 미리 파악한다 |
| 위험 | 이미 아는 명령어에만 의존해 더 나은 대안(예: `copy` 대신 `robocopy`)을 놓치기 쉽다 | 초반 진입 비용이 검색보다 크다 |
| 적합한 상황 | 이미 기초가 있고 특정 옵션만 확인하려는 경우 — [명령어 종류 총정리](/post/cmd/command-categories/)로 바로 이동 | 처음 CMD를 배우거나, 레거시 배치 스크립트 전체를 체계적으로 이해하려는 경우 |

또 다른 트레이드오프는 CMD 자체와 PowerShell 사이에 있다. CMD는 모든 입출력을 텍스트로 다루고 배우기 쉬운 대신 구조화된 데이터 처리나 원격 관리 기능이 약하다. PowerShell은 객체 파이프라인과 방대한 cmdlet으로 강력하지만 학습 곡선이 가파르고, 문법이 CMD의 배치 스크립트와 호환되지 않는다. Microsoft 자신도 신규 자동화 스크립트에는 PowerShell을 권장하지만, 그것이 기존 CMD 스크립트를 당장 걷어내야 한다는 뜻은 아니다 — 이 컬렉션은 "새로 쓸 때는 무엇을 고려해야 하는가"를 각 챕터의 이식성 절에서 짚어주는 데 집중한다.

아래 다이어그램은 9개 Part가 어떤 순서로 서로를 전제하는지 요약한 것이다.

```mermaid
flowchart LR
    explore["Part 1</br>CMD 기초와 탐색"]
    files["Part 2</br>파일과 디렉터리 조작"]
    text["Part 3</br>텍스트 검색과 출력 제어"]
    batch["Part 4</br>배치 스크립팅"]
    disk["Part 5</br>디스크와 파일 시스템 관리"]
    process["Part 6</br>프로세스·서비스와 권한 관리"]
    sysinfo["Part 7</br>시스템 정보와 구성"]
    network["Part 8</br>네트워크와 원격 진단"]
    misc["Part 9</br>부팅 구성과 기타 유틸리티"]

    explore --> files --> text --> batch --> disk --> process --> sysinfo --> network --> misc
```

이 화살표는 물리적으로 강제되는 순서가 아니라 학습 효율을 위한 권장 순서다. 예를 들어 이미 리눅스 셸을 다뤄본 독자는 4부(배치 스크립팅)의 "조건 분기·반복문이 있다"는 개념 자체는 낯설지 않겠지만, `if "%VAR%"=="value"`처럼 양쪽에 따옴표를 맞추는 CMD 고유 구문과 `%%f`(배치 파일 안) vs `%f`(대화형 프롬프트)의 `for` 변수 표기 차이는 2–3부에서 파일·텍스트를 실제로 다뤄봐야 그 필요성이 체감된다.

## 흔한 오개념

<strong>"CMD는 레거시라 몰라도 된다"</strong>는 가장 흔한 오해다. PowerShell로 새 자동화를 짤 수 있다는 이유로 CMD를 건너뛰는 경우가 많지만, 실제로는 오래된 배포 스크립트, 서드파티 설치 프로그램이 내부적으로 실행하는 `.bat` 파일, Windows 서버의 예약 작업(`schtasks`)에 등록된 명령 대부분이 지금도 CMD 문법으로 짜여 있다. PowerShell만 알고 CMD 배치 문법을 모르면, 그 스크립트가 실패했을 때 `%ERRORLEVEL%` 한 줄도 스스로 해석할 수 없다.

<strong>"CMD 명령어는 PowerShell에서도 똑같이 동작한다"</strong>는 오해도 흔하다. `dir`, `copy`, `cd`처럼 PowerShell에도 같은 이름의 별칭(alias)이 있는 명령어가 많아 착각하기 쉽지만, PowerShell의 `dir`은 실제로는 `Get-ChildItem`을 가리키는 별칭이라 CMD 전용 스위치(`/A`, `/S`, `/B` 등)를 그대로 넘기면 인식되지 않거나 다르게 동작한다. `if`, `for`처럼 배치 제어 구문 자체는 PowerShell에 대응하는 명령이 아예 없고 문법이 완전히 다르므로, CMD 스크립트를 PowerShell로 그대로 옮겨 붙이는 방식은 통하지 않는다. 이 컬렉션의 각 챕터가 "주의사항·함정" 절에 CMD-PowerShell 이식성을 필수로 다루는 이유가 여기에 있다.

## 커리큘럼 전체 구성

이 과정은 9개 Part, 총 85개 챕터(00장 포함)로 구성된다. Part 구분은 임의의 분류가 아니라 "탐색 가능 → 파일 조작 가능 → 텍스트 검색 가능 → 자동화 가능 → 디스크 관리 가능 → 프로세스·권한 관리 가능 → 시스템 파악 가능 → 네트워크까지 확장 가능 → 부팅·고급 영역까지 확장 가능"이라는 의존성 순서를 따른다.

이 컬렉션은 이 표를 목차이자 진행 상황판으로 함께 썼다. 9개 Part, 85개 챕터(00장 포함) 전체가 사람의 검수를 거쳐 `draft: false`로 전환되어 실제로 공개됐다.

| Part | 챕터 | 제목 |
|---|---|---|
| 0. 개요 | 00 | 과정 개요와 커리큘럼 |
| 1. CMD 기초와 탐색 | 01 | [cmd - 새 인스턴스 시작과 내부·외부 명령어](/post/cmd/cmd-command-interpreter-new-instance-windows/) |
| 1. CMD 기초와 탐색 | 02 | [help - 명령어 도움말 조회](/post/cmd/help-command-list-command-help-windows-cmd/) |
| 1. CMD 기초와 탐색 | 03 | [cls - 화면 지우기](/post/cmd/cls-command-clear-screen-windows-cmd/) |
| 1. CMD 기초와 탐색 | 04 | [prompt - 프롬프트 표시 형식 변경](/post/cmd/prompt-command-customize-command-line-windows/) |
| 1. CMD 기초와 탐색 | 05 | [title - 콘솔 창 제목 설정](/post/cmd/title-command-set-console-window-title-windows/) |
| 1. CMD 기초와 탐색 | 06 | [doskey - 명령줄 편집과 매크로](/post/cmd/doskey-command-line-editing-macros-history-windows/) |
| 1. CMD 기초와 탐색 | 07 | [path - 실행 파일 검색 경로](/post/cmd/path-command-executable-search-path-windows/) |
| 1. CMD 기초와 탐색 | 08 | [cd, chdir - 디렉터리 이동과 현재 위치](/post/cmd/cd-chdir-command-change-directory-windows-cmd/) |
| 1. CMD 기초와 탐색 | 09 | [dir - 파일·디렉터리 목록 조회](/post/cmd/dir-command-list-files-directories-windows-cmd/) |
| 1. CMD 기초와 탐색 | 10 | [tree - 디렉터리 구조 트리 표시](/post/cmd/tree-command-directory-structure-windows-cmd/) |
| 1. CMD 기초와 탐색 | 11 | [pushd, popd - 디렉터리 스택](/post/cmd/pushd-popd-command-directory-stack-windows-cmd/) |
| 2. 파일과 디렉터리 조작 | 12 | [md, mkdir - 디렉터리 생성](/post/cmd/md-mkdir-command-create-directory-windows-cmd/) |
| 2. 파일과 디렉터리 조작 | 13 | [rmdir, rd - 디렉터리 삭제](/post/cmd/rmdir-rd-command-remove-directory-windows-cmd/) |
| 2. 파일과 디렉터리 조작 | 14 | [copy - 파일 복사](/post/cmd/copy-command-copy-files-windows-cmd/) |
| 2. 파일과 디렉터리 조작 | 15 | [xcopy - 디렉터리 트리 복사](/post/cmd/xcopy-command-copy-directory-tree-windows-cmd/) |
| 2. 파일과 디렉터리 조작 | 16 | [robocopy - 재시도·미러링 지원 고급 복사](/post/cmd/robocopy-command-mirror-copy-files-windows/) |
| 2. 파일과 디렉터리 조작 | 17 | [move - 파일·디렉터리 이동](/post/cmd/move-command-move-files-directories-windows-cmd/) |
| 2. 파일과 디렉터리 조작 | 18 | [del, erase - 파일 삭제](/post/cmd/del-erase-command-delete-files-windows-cmd/) |
| 2. 파일과 디렉터리 조작 | 19 | [ren, rename - 이름 변경](/post/cmd/ren-rename-command-rename-files-windows-cmd/) |
| 2. 파일과 디렉터리 조작 | 20 | [type - 텍스트 파일 내용 출력](/post/cmd/type-command-display-file-contents-windows-cmd/) |
| 2. 파일과 디렉터리 조작 | 21 | [attrib - 파일 속성 표시·변경](/post/cmd/attrib-command-file-attributes-windows-cmd/) |
| 2. 파일과 디렉터리 조작 | 22 | [comp - 파일 바이트 단위 비교](/post/cmd/comp-command-compare-files-byte-windows-cmd/) |
| 2. 파일과 디렉터리 조작 | 23 | [fc - 파일 줄 단위 차이 비교](/post/cmd/fc-command-compare-files-differences-windows-cmd/) |
| 2. 파일과 디렉터리 조작 | 24 | [mklink - 심볼릭 링크·하드 링크 생성](/post/cmd/mklink-command-symbolic-hard-links-windows-cmd/) |
| 2. 파일과 디렉터리 조작 | 25 | [replace - 대상 파일을 원본으로 교체](/post/cmd/replace-command-replace-files-windows-cmd/) |
| 3. 텍스트 검색과 출력 제어 | 26 | [find - 파일·출력 문자열 검색](/post/cmd/find-command-search-text-string-windows-cmd/) |
| 3. 텍스트 검색과 출력 제어 | 27 | [findstr - 정규식 지원 문자열 검색](/post/cmd/findstr-command-regex-search-windows-cmd/) |
| 3. 텍스트 검색과 출력 제어 | 28 | [sort - 텍스트 입력 정렬](/post/cmd/sort-command-sort-text-lines-windows-cmd/) |
| 3. 텍스트 검색과 출력 제어 | 29 | [more - 출력을 화면 단위로 표시](/post/cmd/more-command-page-output-windows-cmd/) |
| 4. 배치 스크립팅 | 30 | [echo - 메시지 출력과 에코 설정](/post/cmd/echo-command-display-message-windows-cmd/) |
| 4. 배치 스크립팅 | 31 | [set - 환경 변수 표시·설정·제거](/post/cmd/set-command-environment-variables-windows-cmd/) |
| 4. 배치 스크립팅 | 32 | [if - 조건 분기](/post/cmd/if-command-conditional-batch-windows-cmd/) |
| 4. 배치 스크립팅 | 33 | [for - 파일 집합·범위 반복](/post/cmd/for-command-loop-batch-windows-cmd/) |
| 4. 배치 스크립팅 | 34 | [call - 배치 파일·레이블 호출](/post/cmd/call-command-batch-subroutine-windows-cmd/) |
| 4. 배치 스크립팅 | 35 | [goto - 레이블로 실행 흐름 이동](/post/cmd/goto-command-batch-label-jump-windows-cmd/) |
| 4. 배치 스크립팅 | 36 | [shift - 배치 매개변수 위치 이동](/post/cmd/shift-command-batch-parameters-windows-cmd/) |
| 4. 배치 스크립팅 | 37 | [pause - 처리 일시 중단](/post/cmd/pause-command-suspend-batch-windows-cmd/) |
| 4. 배치 스크립팅 | 38 | [exit - 세션·배치 스크립트 종료](/post/cmd/exit-command-terminate-cmd-windows/) |
| 4. 배치 스크립팅 | 39 | [rem - 배치 파일 주석](/post/cmd/rem-command-batch-comments-windows-cmd/) |
| 4. 배치 스크립팅 | 40 | [setlocal, endlocal - 환경 변수 유효 범위](/post/cmd/setlocal-endlocal-command-variable-scope-windows-cmd/) |
| 4. 배치 스크립팅 | 41 | [break - 확장된 Ctrl+C 검사 설정](/post/cmd/break-command-extended-ctrl-c-windows-cmd/) |
| 5. 디스크와 파일 시스템 관리 | 42 | [chkdsk - 디스크 오류 검사](/post/cmd/chkdsk-command-check-disk-errors-windows-cmd/) |
| 5. 디스크와 파일 시스템 관리 | 43 | [chkntfs - 부팅 시 디스크 검사 설정](/post/cmd/chkntfs-command-disk-check-boot-windows-cmd/) |
| 5. 디스크와 파일 시스템 관리 | 44 | [diskpart - 대화형 파티션 관리](/post/cmd/diskpart-command-manage-partitions-windows-cmd/) |
| 5. 디스크와 파일 시스템 관리 | 45 | [format - 드라이브 포맷](/post/cmd/format-command-format-disk-windows-cmd/) |
| 5. 디스크와 파일 시스템 관리 | 46 | [convert - FAT 볼륨을 NTFS로 변환](/post/cmd/convert-command-fat-to-ntfs-windows-cmd/) |
| 5. 디스크와 파일 시스템 관리 | 47 | [compact - NTFS 압축 상태 표시·변경](/post/cmd/compact-command-ntfs-compression-windows-cmd/) |
| 5. 디스크와 파일 시스템 관리 | 48 | [fsutil - 파일 시스템 저수준 조회·구성](/post/cmd/fsutil-command-file-system-utility-windows-cmd/) |
| 5. 디스크와 파일 시스템 관리 | 49 | [label - 볼륨 레이블 관리](/post/cmd/label-command-volume-label-windows-cmd/) |
| 5. 디스크와 파일 시스템 관리 | 50 | [vol - 볼륨 레이블·일련번호 표시](/post/cmd/vol-command-display-volume-label-windows-cmd/) |
| 5. 디스크와 파일 시스템 관리 | 51 | [subst - 경로를 가상 드라이브 문자에 연결](/post/cmd/subst-command-virtual-drive-letter-windows-cmd/) |
| 5. 디스크와 파일 시스템 관리 | 52 | [recover - 손상 디스크에서 데이터 복구](/post/cmd/recover-command-recover-damaged-disk-windows-cmd/) |
| 5. 디스크와 파일 시스템 관리 | 53 | [verify - 디스크 기록 검증 설정](/post/cmd/verify-command-verify-file-writes-windows-cmd/) |
| 6. 프로세스·서비스와 권한 관리 | 54 | [tasklist - 실행 중인 프로세스 목록](/post/cmd/tasklist-command-list-running-processes-windows-cmd/) |
| 6. 프로세스·서비스와 권한 관리 | 55 | [taskkill - 프로세스 종료](/post/cmd/taskkill-command-terminate-process-windows-cmd/) |
| 6. 프로세스·서비스와 권한 관리 | 56 | [sc - Windows 서비스 조회·구성](/post/cmd/sc-command-manage-windows-services-cmd/) |
| 6. 프로세스·서비스와 권한 관리 | 57 | [schtasks - 예약 작업 관리](/post/cmd/schtasks-command-scheduled-tasks-windows-cmd/) |
| 6. 프로세스·서비스와 권한 관리 | 58 | [start - 별도 창에서 프로그램 실행](/post/cmd/start-command-run-program-new-window-windows-cmd/) |
| 6. 프로세스·서비스와 권한 관리 | 59 | [shutdown - 로컬·원격 시스템 종료](/post/cmd/shutdown-command-restart-shutdown-windows-cmd/) |
| 6. 프로세스·서비스와 권한 관리 | 60 | [icacls - 파일·디렉터리 ACL 관리](/post/cmd/icacls-command-file-directory-acl-windows-cmd/) |
| 6. 프로세스·서비스와 권한 관리 | 61 | [cacls - ACL 관리(레거시, icacls 권장)](/post/cmd/cacls-command-legacy-acl-windows-cmd/) |
| 6. 프로세스·서비스와 권한 관리 | 62 | [openfiles - 원격 사용자가 연 파일 조회](/post/cmd/openfiles-command-remote-open-files-windows-cmd/) |
| 7. 시스템 정보와 구성 | 63 | [systeminfo - 하드웨어·OS 구성 정보](/post/cmd/systeminfo-command-hardware-os-info-windows-cmd/) |
| 7. 시스템 정보와 구성 | 64 | [ver - Windows 버전 표시](/post/cmd/ver-command-windows-version-cmd/) |
| 7. 시스템 정보와 구성 | 65 | [driverquery - 장치 드라이버 상태](/post/cmd/driverquery-command-device-driver-status-windows-cmd/) |
| 7. 시스템 정보와 구성 | 66 | [gpresult - 그룹 정책 정보 표시](/post/cmd/gpresult-command-group-policy-info-windows-cmd/) |
| 7. 시스템 정보와 구성 | 67 | [mode - 콘솔·장치 구성](/post/cmd/mode-command-configure-system-devices-windows-cmd/) |
| 7. 시스템 정보와 구성 | 68 | [wmic - WMI 조회(레거시, PowerShell 권장)](/post/cmd/wmic-command-wmi-query-legacy-windows-cmd/) |
| 7. 시스템 정보와 구성 | 69 | [date, time - 시스템 날짜·시간](/post/cmd/date-time-command-system-clock-windows-cmd/) |
| 7. 시스템 정보와 구성 | 70 | [chcp - 활성 코드 페이지 설정](/post/cmd/chcp-command-active-code-page-windows-cmd/) |
| 7. 시스템 정보와 구성 | 71 | [color - 콘솔 전경·배경색 설정](/post/cmd/color-command-console-colors-windows-cmd/) |
| 8. 네트워크와 원격 진단 | 72 | [ipconfig - TCP/IP 네트워크 구성 확인](/post/cmd/ipconfig-command-network-configuration-windows/) |
| 8. 네트워크와 원격 진단 | 73 | [ping - 대상 호스트 연결 확인](/post/cmd/ping-command-test-network-connectivity-windows-cmd/) |
| 8. 네트워크와 원격 진단 | 74 | [tracert - 패킷 경로 추적](/post/cmd/tracert-command-trace-route-windows-cmd/) |
| 8. 네트워크와 원격 진단 | 75 | [netstat - 연결·라우팅 통계 표시](/post/cmd/netstat-command-network-connections-windows-cmd/) |
| 8. 네트워크와 원격 진단 | 76 | [nslookup - DNS 질의](/post/cmd/nslookup-command-dns-query-windows-cmd/) |
| 8. 네트워크와 원격 진단 | 77 | [getmac - 네트워크 어댑터 MAC 주소 표시](/post/cmd/getmac-command-mac-address-windows-cmd/) |
| 8. 네트워크와 원격 진단 | 78 | [net user - 로컬·도메인 사용자 계정 관리](/post/cmd/net-user-command-manage-user-accounts-windows-cmd/) |
| 9. 부팅 구성과 기타 유틸리티 | 79 | [bcdboot - 시동 구성 데이터 복사](/post/cmd/bcdboot-command-boot-configuration-data-windows-cmd/) |
| 9. 부팅 구성과 기타 유틸리티 | 80 | [bcdedit - 부팅 구성 데이터 편집](/post/cmd/bcdedit-command-boot-configuration-editor-windows-cmd/) |
| 9. 부팅 구성과 기타 유틸리티 | 81 | [assoc - 파일 확장명 연결 표시·수정](/post/cmd/assoc-command-file-extension-association-windows-cmd/) |
| 9. 부팅 구성과 기타 유틸리티 | 82 | [ftype - 파일 형식 실행 명령 표시·수정](/post/cmd/ftype-command-file-type-open-command-windows-cmd/) |
| 9. 부팅 구성과 기타 유틸리티 | 83 | [graftabl - 그래픽 모드 확장 문자 세트](/post/cmd/graftabl-command-extended-character-set-windows-cmd/) |
| 9. 부팅 구성과 기타 유틸리티 | 84 | [print - 텍스트 파일 인쇄](/post/cmd/print-command-send-file-printer-windows-cmd/) |

번호 시퀀스 밖에서 카테고리별로 명령어를 빠르게 찾고 싶다면 [명령어 종류 총정리](/post/cmd/command-categories/)를 부록처럼 활용할 수 있다.

## Part별 설계 근거

Part 1(CMD 기초와 탐색, 01–11장)은 CMD 자체를 시작하고(`cmd`), 도움을 구하고(`help`), 화면·창·프롬프트를 정리하고(`cls`/`title`/`prompt`), 과거 명령을 다시 불러내고(`doskey`), 명령어가 어디서 실행되는지 이해하고(`path`), 디렉터리를 오가는(`cd`/`dir`/`tree`/`pushd`-`popd`) 최소 동작으로 구성했다. 이후 모든 Part의 예제는 프롬프트 위에서 실행되므로, 이 최소 조작 능력이 없으면 뒤의 예제를 재현할 수조차 없다.

Part 2(파일과 디렉터리 조작, 12–25장)는 디렉터리를 만들고 지우는 것부터(`md`/`rmdir`) 파일을 복사·이동·삭제·이름 변경하고(`copy`/`xcopy`/`robocopy`/`move`/`del`/`ren`), 내용과 속성을 확인하는(`type`/`attrib`/`comp`/`fc`) 명령까지 담는다. 복사 계열 세 명령(`copy`/`xcopy`/`robocopy`)을 나란히 배치해 파일 하나를 옮길 때, 디렉터리 트리를 통째로 옮길 때, 네트워크 드라이브처럼 중간에 끊길 수 있는 대용량 작업을 미러링할 때 각각 무엇을 선택해야 하는지 비교하며 배우도록 했다.

Part 3(텍스트 검색과 출력 제어, 26–29장)은 `find`/`findstr`로 문자열을 찾고 `sort`/`more`로 결과를 정렬·페이지 단위로 다듬는 최소한의 텍스트 처리 도구를 모은다. 유닉스 셸의 `grep`/`sort`/`less`에 각각 느슨하게 대응하지만, 파이프 문화가 깊지 않은 CMD에서는 이 네 개 명령이 조합 가능한 텍스트 처리의 사실상 전부라는 점이 다르다.

Part 4(배치 스크립팅, 30–41장)는 1–3부에서 낱개로 실행하던 명령을 반복 가능한 `.bat` 파일로 묶는다. 메시지 출력과 변수(`echo`/`set`)를 먼저 배치하고, 조건 분기와 반복(`if`/`for`), 서브루틴 호출과 흐름 제어(`call`/`goto`/`shift`), 사용자 상호작용과 종료(`pause`/`exit`), 마지막으로 변수 유효범위와 신호 처리(`setlocal`-`endlocal`/`break`) 순으로 이어진다. `if`/`for`를 모르면 `call`로 호출할 서브루틴 자체를 조건부로 만들 수 없어 이 순서를 지켰다.

Part 5(디스크와 파일 시스템 관리, 42–53장)는 시선을 파일 하나에서 디스크 전체로 옮긴다. `chkdsk`/`chkntfs`로 상태를 검사하고, `diskpart`/`format`/`convert`로 구조를 바꾸고, `compact`/`fsutil`/`label`/`vol`/`subst`/`recover`/`verify`로 세부 속성을 다룬다. 이 Part의 상당수 명령은 되돌릴 수 없으므로, 각 챕터의 "주의사항·함정" 절에서 실행 전 확인 절차를 특히 강조한다.

Part 6(프로세스·서비스와 권한 관리, 54–62장)은 실행 중인 프로그램(`tasklist`/`taskkill`), 백그라운드 서비스와 예약 작업(`sc`/`schtasks`), 그리고 파일 접근 권한(`icacls`/`cacls`/`openfiles`)을 다룬다. 디스크 관리(5부) 다음에 배치한 이유는, 실무에서 이 작업 대부분이 "디스크 공간이 부족해 특정 프로세스를 종료하고 관련 서비스를 재시작한다"처럼 앞서 배운 지식과 이어지는 시나리오로 등장하기 때문이다.

Part 7(시스템 정보와 구성, 63–71장)은 `systeminfo`/`ver`/`driverquery`/`gpresult`로 시스템 상태를 조회하고, `mode`/`wmic`/`date`-`time`/`chcp`/`color`로 장치·환경을 구성하는 명령을 모은다. 지금까지 배운 조작·관리 능력을 바탕으로 "이 시스템이 지금 어떤 상태인가"를 진단하는 시야로 확장하는 단계다.

Part 8(네트워크와 원격 진단, 72–78장)은 `ipconfig`/`ping`/`tracert`/`netstat`/`nslookup`/`getmac`/`net user`로 로컬 시스템을 넘어 네트워크 너머의 대상을 다룬다. 가장 마지막에 가까이 배치한 이유는 원격 문제를 진단하려면 그 이전에 로컬 파일·프로세스·시스템 상태를 스스로 확인할 수 있어야 "이 문제가 로컬 문제인지 네트워크 문제인지"를 먼저 좁혀나갈 수 있기 때문이다.

Part 9(부팅 구성과 기타 유틸리티, 79–84장)는 `bcdboot`/`bcdedit`처럼 부팅 데이터베이스를 다루는 저수준·고위험 도구와, `assoc`/`ftype`/`graftabl`/`print`처럼 어느 카테고리에도 딱 들어맞지 않는 명령을 묶은 부록 성격의 Part다. 사용 빈도는 낮지만 부팅 복구나 파일 연결 문제를 진단할 때는 대체할 도구가 없어 커리큘럼에 남겼다.

## 선수 지식

이 과정을 시작하는 데 필요한 사전 지식은 많지 않다. Windows에서 명령 프롬프트(`cmd.exe`)를 열고 텍스트로 명령을 입력하는 것에 거부감이 없으면 충분하며, 프로그래밍 경험은 필수가 아니다. 다만 4부(배치 스크립팅)에 들어가면 변수·조건문·반복문 같은 프로그래밍의 기본 개념을 다루므로, 다른 언어나 셸(Bash, PowerShell 등)에서 `if`/`for`를 써본 경험이 있으면 그 구간을 훨씬 빠르게 소화할 수 있다.

리눅스·유닉스 셸을 먼저 배운 독자라면 이 컬렉션과 짝을 이루는 [Bash Shell 컬렉션](/post/bashshell/getting-started-bash-shell/)에서 같은 개념의 유닉스 대응 명령을 이미 다뤘을 수 있다. 두 컬렉션은 서로를 대체하지 않는다 — Bash 컬렉션의 00장이 안내하듯, CMD/PowerShell 경험자는 Bash 쪽에서 "이미 아는 개념이 어디에 대응하는지" 확인하는 용도로 이 컬렉션을 참고할 수 있고, 반대로 리눅스 경험자는 이 컬렉션의 각 챕터에서 CMD 고유의 구문 차이(따옴표 규칙, `%%`/`%` 변수 표기 등)에 특히 주의를 기울이면 된다.

## 완주 시 갖추는 역량

이 컬렉션을 끝까지 따라가면 "명령어를 안다"는 수준을 넘어, Windows 서버·워크스테이션 환경에 던져졌을 때 스스로 상황을 진단하고 레거시 자동화를 안전하게 유지 보수하는 실무 역량을 갖추는 것을 목표로 한다.

- 낯선 Windows 서버에 원격 접속해 파일·디렉터리를 탐색하고, 필요한 파일의 속성과 ACL을 확인·조정할 수 있다.
- 기존 `.bat` 배치 스크립트를 읽고, `if`/`for`/`call`/`goto`의 흐름을 추적해 실패 원인을 `%ERRORLEVEL%` 기준으로 진단할 수 있다.
- 디스크 상태를 점검하고(`chkdsk`), 되돌릴 수 없는 파티션 작업(`diskpart`)을 실행하기 전에 대상을 안전하게 재확인하는 습관을 갖춘다.
- 실행 중인 프로세스와 백그라운드 서비스를 조회·제어하고, 예약 작업의 동작을 확인할 수 있다.
- `ipconfig`/`ping`/`nslookup`으로 네트워크 문제를 로컬·원격 중 어느 쪽인지 좁혀나갈 수 있다.
- CMD 명령과 PowerShell 대응 명령의 차이를 구분해, 어느 쪽으로 새 자동화를 작성해야 할지 판단할 수 있다.

## 다음 장에서는

다음은 [01장: cmd](/post/cmd/cmd-command-interpreter-new-instance-windows/) — `cmd` 명령 자체와 내부·외부 명령어 구분을 시작으로 CMD 기초와 탐색(1부)을 다룬다. 00장부터 [84장: print](/post/cmd/print-command-send-file-printer-windows-cmd/)까지 9개 Part, 85개 챕터 전체가 사람의 최종 검수를 거쳐 게시됐다.

## 평가 기준

이 장을 읽은 후 다음을 할 수 있어야 한다.

- 체계적으로 순서대로 학습하는 방식과 필요할 때 카테고리 색인([명령어 종류 총정리](/post/cmd/command-categories/))으로 찾는 방식의 장단점을 설명하고, 자신의 상황에 맞게 선택할 수 있다.
- CMD가 여전히 실무에서 쓰이는 세 가지 이유(레거시 배치 스크립트, GUI 없는 서버 관리, PowerShell과의 상호운용)를 설명할 수 있다.
- 9개 Part(탐색-파일 조작-텍스트 검색-배치 스크립팅-디스크 관리-프로세스·권한-시스템 정보-네트워크-부팅/기타)가 왜 이 순서인지 말할 수 있다.
- 내부 명령어와 외부 명령어의 차이를 `where` 명령으로 구분하는 방법을 설명할 수 있다.
- CMD 명령어가 PowerShell에서 이름은 같아도 다르게 동작할 수 있다는 점과, 그 이유(별칭 vs 실제 cmdlet, 배치 구문의 부재)를 설명할 수 있다.

## 참고 및 출처

- [Windows commands - Windows Server | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/windows-commands)
- [Deprecated features in the Windows client | Microsoft Learn](https://learn.microsoft.com/en-us/windows/whats-new/deprecated-features)
