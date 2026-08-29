---
draft: true
collection_order: 0
slug: getting-started-powershell
title: "[PowerShell] 00. 과정 개요와 커리큘럼"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell 121챕터 커리큘럼의 과정 개요. 텍스트가 아닌 객체 파이프라인이라는 정신 모델, 18개 Part 학습 순서의 설계 근거, 00-120장 전체 목차, 선수 지식과 완주 후 실무자가 갖추는 원격 관리·보안 역량까지 정리한 과정 개요 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Windows(윈도우)
- Shell(셸)
- Terminal
- .NET
- Automation(자동화)
- DevOps
- CI-CD(Continuous Integration/Continuous Deployment)
- Security(보안)
- SSH(Secure Shell)
- System-Design
- Guide(가이드)
- Education(교육)
- Career(커리어)
- Productivity(생산성)
- Beginner
- Advanced
- Networking(네트워킹)
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
- Cmdlet
- Object-Pipeline
- Remoting
- 커리큘럼
- 로드맵
image: "wordcloud.png"
---

## 이 장을 읽기 전에

이 챕터는 "PowerShell" 컬렉션의 첫 챕터이므로 선행 챕터가 없다. 필요한 선수 지식은 이 장의 "선수 지식" 절에서 별도로 정리한다.

난이도는 입문(PowerShell 콘솔을 처음 열어보는 수준)에서 중급(18개 Part의 순서 논리와 CMD·Bash 셸과의 위치 관계를 판단할 수 있는 수준) 사이를 오간다. 특정 cmdlet의 매개변수나 실행 예시는 다루지 않는다. 이 장은 지도(map)이지 cmdlet 레퍼런스가 아니다.

이 장이 다루지 않는 것은 다음과 같다. `Get-ChildItem`·`Where-Object`처럼 개별 cmdlet의 매개변수와 예시는 01장 이후 각 번호 챕터에서 다룬다. 원격 관리(11부), 보안·자격 증명(14부), DSC(15부)처럼 별도의 정신 모델이 필요한 영역은 각각 독립된 Part로 다룬다. 이 장에서는 "왜 이런 순서로 배워야 하는가"와 "PowerShell이 CMD·Bash와 근본적으로 무엇이 다른가"만 설명한다. 이 컬렉션은 Windows PowerShell 5.1과 PowerShell 7(pwsh)을 함께 다루되, Azure PowerShell·Exchange Online 관리 셸처럼 별도의 거대한 생태계를 이루는 클라우드 서비스 전용 모듈은 이 컬렉션의 범위 밖이며, 필요한 경우에만 각 챕터에서 짧게 언급한다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| PowerShell 콘솔이 처음인 완전 초보자 | 전체를 순서대로 | 객체 파이프라인이 왜 중요한지, 어디서부터 시작해야 하는지 이해한다 |
| CMD·Bash 등 다른 커맨드라인 경험자 | 도입, 핵심 개념, 비교/트레이드오프 | 텍스트 기반 셸에서 쓰던 습관이 객체 기반 파이프라인에서 어떻게 달라지는지 파악한다 |
| cmdlet을 몇 개 알고 레퍼런스를 찾으러 온 실무자 | 커리큘럼 전체 구성 표 | 자신이 아는 cmdlet이 몇 장인지, Part별로 빠르게 찾을 cmdlet이 무엇인지 확인한다 |
| 기존 PowerShell 스크립트를 유지 보수해야 하는 담당자 | 6부(스크립팅), 7부(에러 처리), 9부(모듈) | 기존 `.ps1` 스크립트와 모듈을 읽고 안전하게 수정할 최소 지식을 갖춘다 |
| Windows 서버·AD 환경을 관리하는 인프라 담당자 | 11부(원격 관리), 12부(프로세스·서비스), 17부(디렉터리 관리) | 원격 시스템과 Active Directory를 PowerShell로 관리하는 데 필요한 지식을 확인한다 |

## 도입

PowerShell은 명령줄 셸(shell)과 스크립팅 언어, 구성 관리 프레임워크를 한데 묶은 크로스플랫폼 작업 자동화 솔루션으로, Windows·Linux·macOS에서 모두 실행된다. 2006년 Windows 전용 "Windows PowerShell"로 시작했지만, 2016년 .NET Core 기반의 오픈소스 "PowerShell Core"(현재의 PowerShell 7)로 재설계되면서 크로스플랫폼 도구가 됐다. 이 배경 때문에 실무에서는 두 갈래를 동시에 마주친다 — Windows에 기본 내장된 Windows PowerShell 5.1(.NET Framework 기반, Windows 전용)과, 별도로 설치하는 PowerShell 7(pwsh, .NET 기반, 크로스플랫폼)이다. 신규 자동화는 PowerShell 7을 권장하지만, 일부 Windows 전용 모듈(오래된 서버 관리 도구 등)은 여전히 Windows PowerShell 5.1에서만 완전하게 동작해, 실무자는 두 버전의 차이를 알아야 한다.

CMD가 텍스트를 주고받는 인터프리터라면, PowerShell은 명령이 텍스트가 아니라 **.NET 객체**를 주고받는 셸이다. 이 차이가 이 컬렉션 전체의 뼈대를 이룬다. `Get-Process`가 반환하는 결과는 화면에 찍힌 문자열이 아니라 `System.Diagnostics.Process` 객체의 컬렉션이며, 이 객체를 `Where-Object`로 거르고 `Sort-Object`로 정렬하고 `Select-Object`로 원하는 속성만 추릴 수 있다. 텍스트를 파싱해 필요한 값을 잘라내야 했던 CMD·전통적 Bash 스크립팅과 근본적으로 다른 지점이다.

PowerShell을 배우는 일은 Windows 환경에 국한된 취미가 아니라 현대 인프라 자동화의 공용어에 가깝다. 첫째, Microsoft는 Azure, Windows Server, Exchange, SQL Server 등 자사 플랫폼 대부분의 관리 인터페이스를 PowerShell 모듈로 제공한다. 둘째, AWS·VMware·Oracle Cloud 같은 서드파티 플랫폼도 PowerShell 모듈을 함께 배포해, 하나의 셸로 여러 클라우드·가상화 환경을 다룰 수 있다. 셋째, PowerShell Desired State Configuration(DSC)은 인프라를 코드로 선언하고 구성 드리프트를 감지·교정하는 구성 관리 프레임워크를 셸 자체에 내장하고 있어, 별도 도구 없이도 선언적 배포를 시작할 수 있다. 이 세 가지가 이 컬렉션이 18개 Part로 나뉘는 이유이기도 하다 — 각 Part는 이 역량들을 순서대로 습득하도록 설계되어 있다.

## 핵심 개념

<strong>PowerShell</strong>은 명령줄 셸, 스크립팅 언어, 구성 관리 프레임워크로 구성된 크로스플랫폼 작업 자동화 솔루션이다. 대부분의 셸이 텍스트만 주고받는 것과 달리, PowerShell은 .NET 객체를 입력·출력으로 받아들이고 반환한다. 이 객체는 강력한 명령줄 히스토리, 탭 완성과 명령 예측(PSReadLine), 명령·매개변수 별칭, 파이프라인, `man` 페이지와 유사한 콘솔 내 도움말 시스템을 함께 제공한다.

PowerShell을 처음 배우는 사람이 가장 먼저 정리해야 할 구분은 <strong>cmdlet(명령릿)</strong>의 이름 규칙이다. PowerShell의 거의 모든 명령은 `Verb-Noun` 형태를 따른다 — `Get-Process`, `Set-Location`, `New-Item`처럼 동사(Get, Set, New, Remove 등 승인된 동사 목록)와 명사(Process, Location, Item 등 대상)를 하이픈으로 연결한다. 이 규칙 덕분에 cmdlet 이름만 보고도 "무엇을, 어떻게" 하는지 유추할 수 있고, `Get-Command -Verb Get -Noun Process`처럼 동사·명사로 명령을 검색할 수 있다. 이 구분은 03장에서 `Get-Command`를 다루며 더 자세히 짚는다.

이 정신 모델이 커리큘럼 순서를 결정한다. 콘솔을 열고 도움말을 찾는 법(1부)을 모르면 무엇이 가능한지조차 알 수 없고, 파이프라인이 객체를 다룬다는 사실(2부)을 모르면 파일 시스템(4부)이나 데이터(5부)를 다뤄도 결과를 제대로 활용할 수 없다. 연산자와 자동 변수(3부)는 파이프라인 안에서 조건을 표현하는 문법적 기초를 채운다. 스크립팅(6부)과 에러 처리(7부)는 낱개 명령을 재사용 가능한 자동화로 묶고, 테스트(8부)와 모듈(9부)은 그 자동화를 검증하고 배포 가능한 단위로 포장한다. 패키지 관리(10부)부터는 시선이 로컬 세션을 넘어 원격 시스템(11부), 프로세스·서비스(12부), 스토리지(13부)로 확장되고, 보안(14부)과 DSC(15부)는 그 확장된 관리 능력에 필요한 권한·선언적 구성 모델을 더한다. 마지막으로 네트워크(16부)와 엔터프라이즈 디렉터리 관리(17부)는 로컬 시스템을 넘어 네트워크와 조직 전체로 시야를 넓힌다.

## 비교/트레이드오프

PowerShell을 배우는 방식에는 두 갈래가 있고, 이 컬렉션은 둘 다를 지원하도록 설계됐다.

| 구분 | 필요할 때 검색해서 익히기 | 커리큘럼을 순서대로 읽기 |
|---|---|---|
| 장점 | 당장 급한 자동화 문제를 가장 빠르게 해결한다 | 빠진 개념 없이 체계적으로 습득하고, 객체 파이프라인이라는 기초 없이 응용부터 배우다 막히는 상황을 피한다 |
| 위험 | 파이프라인·프로바이더 같은 기초 개념 없이 예제 코드를 복사해 쓰다가 응용이 막힌다 | 초반 진입 비용이 검색보다 크다 |
| 적합한 상황 | 이미 기초가 있고 특정 cmdlet의 매개변수만 확인하려는 경우 | 처음 PowerShell을 배우거나, 기존 스크립트·모듈 전체를 체계적으로 이해하려는 경우 |

또 다른 트레이드오프는 Windows PowerShell 5.1과 PowerShell 7(pwsh) 사이에 있다. Windows PowerShell 5.1은 .NET Framework 위에서 동작하며 Windows에만 존재하지만, 일부 레거시 서버 관리 모듈은 지금도 5.1에서만 완전하게 동작한다. PowerShell 7은 .NET 위에서 동작해 Windows·Linux·macOS를 모두 지원하고 병렬 처리(`ForEach-Object -Parallel`) 같은 새 기능을 제공하지만, 5.1 전용으로 작성된 일부 모듈은 호환성 문제를 겪을 수 있다. Microsoft는 신규 자동화에 PowerShell 7을 권장하지만, 그것이 Windows PowerShell 5.1을 당장 걷어내야 한다는 뜻은 아니다 — 이 컬렉션은 두 버전의 차이가 실제로 드러나는 지점(실행 정책, 원격 관리, 모듈 호환성)을 각 챕터에서 짚어주는 데 집중한다.

아래 다이어그램은 18개 Part가 어떤 순서로 서로를 전제하는지 요약한 것이다.

```mermaid
flowchart LR
    basics["Part 1</br>기초 환경과 콘솔"]
    pipeline["Part 2</br>객체 파이프라인 핵심"]
    operators["Part 3</br>연산자·자동 변수와 커스텀 객체"]
    filesystem["Part 4</br>파일 시스템과 프로바이더"]
    data["Part 5</br>데이터 구조와 텍스트/구조화 데이터"]
    scripting["Part 6</br>스크립팅과 흐름 제어"]
    errors["Part 7</br>에러 처리와 진단"]
    testing["Part 8</br>테스트와 코드 품질"]
    modules["Part 9</br>모듈과 병렬 처리"]
    packages["Part 10</br>패키지·업데이트 관리"]
    remoting["Part 11</br>원격 관리(Remoting)"]
    processes["Part 12</br>프로세스·서비스·예약 작업"]
    storage["Part 13</br>스토리지와 시스템 구성"]
    security["Part 14</br>보안과 자격 증명"]
    dsc["Part 15</br>DSC(Desired State Configuration)"]
    network["Part 16</br>네트워크와 웹"]
    directory["Part 17</br>엔터프라이즈 디렉터리 관리"]
    wrapup["Part 18</br>마무리와 크로스플랫폼"]

    basics --> pipeline --> operators --> filesystem --> data --> scripting --> errors --> testing --> modules --> packages --> remoting --> processes --> storage --> security --> dsc --> network --> directory --> wrapup
```

이 화살표는 물리적으로 강제되는 순서가 아니라 학습 효율을 위한 권장 순서다. 예를 들어 이미 CMD 배치 스크립팅을 다뤄본 독자는 6부(스크립팅과 흐름 제어)의 "조건 분기·반복문이 있다"는 개념 자체는 낯설지 않겠지만, `if ($x -eq 1)`처럼 비교 연산자를 부호(`==`)가 아니라 접두어(`-eq`)로 쓰는 PowerShell 고유 문법과, 파이프라인으로 전달된 객체가 함수 매개변수에 자동으로 바인딩되는 방식(6부 61장)은 2부에서 파이프라인을 실제로 다뤄봐야 그 필요성이 체감된다.

## 흔한 오개념

<strong>"PowerShell도 결국 명령어를 외워서 쓰는 텍스트 셸 아닌가"</strong>는 가장 흔한 오해다. `dir`, `ls`, `cat` 같은 익숙한 별칭이 있다 보니 CMD·Bash와 사용법이 비슷하다고 착각하기 쉽지만, `Get-Command -Name dir` 결과가 보여주듯 `dir`은 실제로는 `Get-ChildItem`을 가리키는 별칭이고, 그 결과는 화면에 찍히는 문자열이 아니라 `System.IO.FileInfo`·`System.IO.DirectoryInfo` 객체다. 이 차이를 모르면 `Get-ChildItem`의 결과를 `Where-Object`로 거르거나 특정 속성만 뽑아내는 다음 단계로 넘어갈 수 없다.

<strong>"PowerShell 7이 나왔으니 Windows PowerShell 5.1은 몰라도 된다"</strong>는 오해도 흔하다. PowerShell 7은 크로스플랫폼이고 성능·기능 면에서 대체로 앞서지만, 일부 Windows 전용 관리 모듈(오래된 하드웨어 벤더 도구, 일부 사내 레거시 모듈)은 여전히 .NET Framework 기반의 Windows PowerShell 5.1에서만 완전하게 동작한다. 두 버전이 함께 설치된 Windows 시스템에서 스크립트가 예상과 다르게 동작한다면, 어느 버전에서 실행되고 있는지(`$PSVersionTable`)부터 확인해야 하는 이유가 여기에 있다.

<strong>"별칭을 쓰면 스크립트가 더 간결해지니 항상 별칭을 쓰는 게 좋다"</strong>는 오해도 있다. `dir`, `ls`, `%`(ForEach-Object), `?`(Where-Object) 같은 별칭은 대화형 콘솔에서 타이핑을 줄이는 데는 유용하지만, 재사용·공유되는 스크립트에서는 전체 cmdlet 이름을 쓰는 것이 권장된다 — 별칭은 셸·로캘에 따라 다르게 정의될 수 있고, 다른 사람이 스크립트를 읽을 때 `Get-ChildItem`이 `dir`보다 즉시 명확하기 때문이다.

## 커리큘럼 전체 구성

이 과정은 18개 Part, 총 121개 챕터(00장 포함)와 부록 1개로 구성된다. Part 구분은 임의의 분류가 아니라 "도움말·별칭을 다룰 수 있다 → 파이프라인 객체를 다룰 수 있다 → 연산자로 조건을 표현할 수 있다 → 파일 시스템에 적용할 수 있다 → 데이터를 가공할 수 있다 → 자동화로 묶을 수 있다 → 에러를 처리할 수 있다 → 테스트할 수 있다 → 모듈로 재사용할 수 있다 → 패키지를 관리할 수 있다 → 원격으로 확장할 수 있다 → 시스템을 관리할 수 있다 → 스토리지를 다룰 수 있다 → 보안을 통제할 수 있다 → 선언적으로 구성할 수 있다 → 네트워크까지 확장할 수 있다 → 조직 전체를 관리할 수 있다"라는 의존성 순서를 따른다.

이 컬렉션은 이 표를 목차이자 진행 상황판으로 함께 쓴다. 이 글을 쓰는 시점에는 00장부터 120장까지, 즉 1부(기초 환경과 콘솔)부터 18부(마무리와 크로스플랫폼)까지 전체 121개 챕터와 번호 시퀀스 밖의 부록까지 모두 작성됐다.

| Part | 챕터 | 제목 |
|---|---|---|
| 0. 개요 | 00 | 과정 개요와 커리큘럼 |
| 1. 기초 환경과 콘솔 | 01 | [PowerShell 소개 — Windows PowerShell vs PowerShell 7(pwsh), 시작과 종료](/post/powershell/powershell-pwsh-introduction-cross-platform-shell/) |
| 1. 기초 환경과 콘솔 | 02 | [Get-Help — 도움말 조회와 Update-Help](/post/powershell/get-help-command-powershell-help-system/) |
| 1. 기초 환경과 콘솔 | 03 | [Get-Command — 명령어(cmdlet) 검색](/post/powershell/get-command-cmdlet-search-powershell/) |
| 1. 기초 환경과 콘솔 | 04 | [Get-Alias/Set-Alias/New-Alias — 별칭 시스템](/post/powershell/get-set-new-alias-command-powershell/) |
| 1. 기초 환경과 콘솔 | 05 | [Get-ExecutionPolicy/Set-ExecutionPolicy — 실행 정책](/post/powershell/execution-policy-command-powershell-security/) |
| 1. 기초 환경과 콘솔 | 06 | [$PROFILE — 프로파일 스크립트](/post/powershell/profile-variable-powershell-startup-script/) |
| 1. 기초 환경과 콘솔 | 07 | [PSReadLine — 탭 완성과 명령 히스토리](/post/powershell/psreadline-module-tab-completion-history/) |
| 1. 기초 환경과 콘솔 | 08 | [Clear-Host와 콘솔 창 제목·색상 설정](/post/powershell/clear-host-command-console-title-color/) |
| 1. 기초 환경과 콘솔 | 09 | [Format-Table/Format-List/Format-Wide — 출력 형식 제어](/post/powershell/format-table-list-wide-command-output/) |
| 2. 객체 파이프라인 핵심 | 10 | [파이프라인 정신 모델 — 텍스트가 아닌 객체](/post/powershell/powershell-pipeline-object-model-not-text/) |
| 2. 객체 파이프라인 핵심 | 11 | [Get-Member — 객체 구조 탐색](/post/powershell/get-member-command-object-structure-powershell/) |
| 2. 객체 파이프라인 핵심 | 12 | [Where-Object — 필터링](/post/powershell/where-object-command-filter-pipeline-powershell/) |
| 2. 객체 파이프라인 핵심 | 13 | [Select-Object — 속성 선택과 투영](/post/powershell/select-object-command-property-projection-powershell/) |
| 2. 객체 파이프라인 핵심 | 14 | [Sort-Object — 정렬](/post/powershell/sort-object-command-sort-pipeline-powershell/) |
| 2. 객체 파이프라인 핵심 | 15 | [ForEach-Object — 파이프라인 반복 처리](/post/powershell/foreach-object-command-pipeline-loop-powershell/) |
| 2. 객체 파이프라인 핵심 | 16 | [Group-Object — 그룹화](/post/powershell/group-object-command-grouping-powershell/) |
| 2. 객체 파이프라인 핵심 | 17 | [Measure-Object — 집계·통계](/post/powershell/measure-object-command-aggregate-statistics-powershell/) |
| 2. 객체 파이프라인 핵심 | 18 | [Tee-Object — 파이프라인 분기](/post/powershell/tee-object-command-pipeline-branch-powershell/) |
| 2. 객체 파이프라인 핵심 | 19 | [Compare-Object — 객체 비교(diff)](/post/powershell/compare-object-command-diff-powershell/) |
| 3. 연산자·자동 변수와 커스텀 객체 | 20 | [비교 연산자 — -eq/-like/-contains/-in](/post/powershell/comparison-operators-eq-like-contains-in-powershell/) |
| 3. 연산자·자동 변수와 커스텀 객체 | 21 | [논리 연산자와 조건식 조합 — -and/-or/-not](/post/powershell/logical-operators-and-or-not-powershell/) |
| 3. 연산자·자동 변수와 커스텀 객체 | 22 | [-split/-join 연산자](/post/powershell/split-join-operators-powershell-strings/) |
| 3. 연산자·자동 변수와 커스텀 객체 | 23 | [타입 캐스팅과 [type] 접근자](/post/powershell/type-casting-type-accelerator-powershell/) |
| 3. 연산자·자동 변수와 커스텀 객체 | 24 | [자동 변수 총정리 — $_, $null, $Error, $LASTEXITCODE](/post/powershell/automatic-variables-powershell-underscore-null/) |
| 3. 연산자·자동 변수와 커스텀 객체 | 25 | [공통 매개변수 — -Verbose/-Debug/-ErrorAction/-OutVariable](/post/powershell/common-parameters-verbose-debug-erroraction-powershell/) |
| 3. 연산자·자동 변수와 커스텀 객체 | 26 | [-WhatIf/-Confirm과 ShouldProcess](/post/powershell/whatif-confirm-shouldprocess-powershell/) |
| 3. 연산자·자동 변수와 커스텀 객체 | 27 | [New-Object와 [PSCustomObject]](/post/powershell/new-object-pscustomobject-powershell/) |
| 3. 연산자·자동 변수와 커스텀 객체 | 28 | [Add-Member — 커스텀 객체에 속성·메서드 추가](/post/powershell/add-member-command-custom-object-properties-powershell/) |
| 3. 연산자·자동 변수와 커스텀 객체 | 29 | [Write-Host vs Write-Output — 출력 스트림 오개념 정리](/post/powershell/write-host-vs-write-output-streams-powershell/) |
| 4. 파일 시스템과 프로바이더 | 30 | [PSDrive와 프로바이더 개념](/post/powershell/psdrive-provider-concept-powershell/) |
| 4. 파일 시스템과 프로바이더 | 31 | [Get-ChildItem — 파일·디렉터리 목록](/post/powershell/get-childitem-command-file-directory-list-powershell/) |
| 4. 파일 시스템과 프로바이더 | 32 | [Set-Location/Push-Location/Pop-Location](/post/powershell/set-location-push-pop-location-powershell/) |
| 4. 파일 시스템과 프로바이더 | 33 | [New-Item — 파일·디렉터리 생성](/post/powershell/new-item-command-create-file-directory-powershell/) |
| 4. 파일 시스템과 프로바이더 | 34 | [Copy-Item — 복사](/post/powershell/copy-item-command-copy-file-powershell/) |
| 4. 파일 시스템과 프로바이더 | 35 | [Move-Item/Rename-Item](/post/powershell/move-rename-item-command-powershell/) |
| 4. 파일 시스템과 프로바이더 | 36 | [Remove-Item — 삭제](/post/powershell/remove-item-command-delete-powershell/) |
| 4. 파일 시스템과 프로바이더 | 37 | [Get-Content/Set-Content/Add-Content](/post/powershell/get-set-add-content-command-powershell/) |
| 4. 파일 시스템과 프로바이더 | 38 | [Get-ItemProperty/Set-ItemProperty](/post/powershell/get-set-itemproperty-command-powershell/) |
| 4. 파일 시스템과 프로바이더 | 39 | [Test-Path — 경로 존재 확인](/post/powershell/test-path-command-check-path-powershell/) |
| 4. 파일 시스템과 프로바이더 | 40 | [레지스트리 프로바이더(Registry:) 다루기](/post/powershell/registry-provider-hklm-hkcu-powershell/) |
| 5. 데이터 구조와 텍스트/구조화 데이터 | 41 | [변수와 데이터 타입](/post/powershell/variables-data-types-powershell/) |
| 5. 데이터 구조와 텍스트/구조화 데이터 | 42 | [배열과 컬렉션 기초](/post/powershell/arrays-collections-powershell/) |
| 5. 데이터 구조와 텍스트/구조화 데이터 | 43 | [ArrayList와 Generic List(List&lt;T&gt;)](/post/powershell/arraylist-generic-list-powershell/) |
| 5. 데이터 구조와 텍스트/구조화 데이터 | 44 | [해시테이블(Hashtable) 다루기](/post/powershell/hash-tables-powershell/) |
| 5. 데이터 구조와 텍스트/구조화 데이터 | 45 | [문자열 서식과 Here-String](/post/powershell/string-formatting-here-string-powershell/) |
| 5. 데이터 구조와 텍스트/구조화 데이터 | 46 | [Select-String — 텍스트에서 패턴 찾기](/post/powershell/select-string-command-powershell/) |
| 5. 데이터 구조와 텍스트/구조화 데이터 | 47 | [-match/-replace 연산자와 정규식](/post/powershell/match-replace-regex-powershell/) |
| 5. 데이터 구조와 텍스트/구조화 데이터 | 48 | [ConvertTo-Json/ConvertFrom-Json](/post/powershell/convertto-convertfrom-json-powershell/) |
| 5. 데이터 구조와 텍스트/구조화 데이터 | 49 | [Import-Csv/Export-Csv/ConvertTo-Csv](/post/powershell/import-export-csv-command-powershell/) |
| 5. 데이터 구조와 텍스트/구조화 데이터 | 50 | [ConvertTo-Html과 Out-File](/post/powershell/convertto-html-out-file-powershell/) |
| 5. 데이터 구조와 텍스트/구조화 데이터 | 51 | [Out-String과 Out-Null](/post/powershell/out-string-out-null-command-powershell/) |
| 5. 데이터 구조와 텍스트/구조화 데이터 | 52 | [Get-Date와 TimeSpan](/post/powershell/get-date-timespan-powershell/) |
| 6. 스크립팅과 흐름 제어 | 53 | [스크립트 작성과 실행(.ps1)](/post/powershell/script-execution-ps1-powershell/) |
| 6. 스크립팅과 흐름 제어 | 54 | [if/elseif/else — 조건 분기](/post/powershell/if-elseif-switch-condition-powershell/) |
| 6. 스크립팅과 흐름 제어 | 55 | [switch 고급 모드 — 와일드카드/정규식/파일 처리](/post/powershell/switch-wildcard-regex-file-powershell/) |
| 6. 스크립팅과 흐름 제어 | 56 | [foreach/for/while/do-while — 반복문](/post/powershell/foreach-for-while-loop-powershell/) |
| 6. 스크립팅과 흐름 제어 | 57 | [함수 정의와 매개변수](/post/powershell/function-parameter-definition-powershell/) |
| 6. 스크립팅과 흐름 제어 | 58 | [CmdletBinding()과 고급 함수](/post/powershell/cmdletbinding-advanced-function-powershell/) |
| 6. 스크립팅과 흐름 제어 | 59 | [매개변수 검증(Validate 속성군)](/post/powershell/parameter-validation-attributes-powershell/) |
| 6. 스크립팅과 흐름 제어 | 60 | [매개변수 스플래팅(Splatting)](/post/powershell/splatting-parameter-powershell/) |
| 6. 스크립팅과 흐름 제어 | 61 | [파이프라인 입력 매개변수(ValueFromPipeline 등)](/post/powershell/pipeline-input-parameter-powershell/) |
| 6. 스크립팅과 흐름 제어 | 62 | [스코프(Scope) — 전역/지역/스크립트](/post/powershell/scope-global-local-script-powershell/) |
| 6. 스크립팅과 흐름 제어 | 63 | [스크립트 블록과 클로저](/post/powershell/script-block-closure-powershell/) |
| 6. 스크립팅과 흐름 제어 | 64 | [#Requires 지시문과 스크립트 메타데이터](/post/powershell/requires-directive-metadata-powershell/) |
| 7. 에러 처리와 진단 | 65 | [try/catch/finally — 예외 처리](/post/powershell/try-catch-finally-exception-powershell/) |
| 7. 에러 처리와 진단 | 66 | [$ErrorActionPreference와 -ErrorAction/-ErrorVariable](/post/powershell/erroractionpreference-command-powershell/) |
| 7. 에러 처리와 진단 | 67 | [trap — 레거시 예외 처리](/post/powershell/trap-legacy-exception-powershell/) |
| 7. 에러 처리와 진단 | 68 | [Write-Verbose/Debug/Warning/Information](/post/powershell/write-verbose-debug-warning-powershell/) |
| 7. 에러 처리와 진단 | 69 | [Start-Transcript — 세션 기록](/post/powershell/start-transcript-session-record-powershell/) |
| 7. 에러 처리와 진단 | 70 | [Set-PSBreakpoint — 스크립트 디버깅](/post/powershell/set-psbreakpoint-debugging-powershell/) |
| 8. 테스트와 코드 품질 | 71 | [Pester 소개 — Describe/It/Should](/post/powershell/pester-describe-it-should-powershell/) |
| 8. 테스트와 코드 품질 | 72 | [PSScriptAnalyzer — 정적 분석과 코딩 규칙](/post/powershell/psscriptanalyzer-static-analysis-powershell/) |
| 8. 테스트와 코드 품질 | 73 | [Measure-Command — 성능 측정과 벤치마킹](/post/powershell/measure-command-benchmark-powershell/) |
| 9. 모듈과 병렬 처리 | 74 | [모듈 개념과 구조(.psm1/.psd1)](/post/powershell/module-structure-psm1-psd1-powershell/) |
| 9. 모듈과 병렬 처리 | 75 | [Import-Module/Get-Module/Remove-Module](/post/powershell/import-get-remove-module-powershell/) |
| 9. 모듈과 병렬 처리 | 76 | [PowerShell Gallery — Install-Module/Find-Module](/post/powershell/powershell-gallery-install-find-module-powershell/) |
| 9. 모듈과 병렬 처리 | 77 | [PowerShell 클래스(class 키워드)](/post/powershell/powershell-class-keyword-powershell/) |
| 9. 모듈과 병렬 처리 | 78 | [Start-Job/Get-Job/Receive-Job — 백그라운드 작업](/post/powershell/start-job-get-job-receive-job-powershell/) |
| 9. 모듈과 병렬 처리 | 79 | [ForEach-Object -Parallel(PowerShell 7+)](/post/powershell/foreach-object-parallel-threadjob-powershell/) |
| 10. 패키지·업데이트 관리 | 80 | [PackageManagement — Get-Package/Install-Package](/post/powershell/packagemanagement-get-install-package-powershell/) |
| 10. 패키지·업데이트 관리 | 81 | [winget과 PowerShell 통합](/post/powershell/winget-powershell-integration-powershell/) |
| 10. 패키지·업데이트 관리 | 82 | [PSWindowsUpdate — Windows 업데이트 관리 모듈](/post/powershell/pswindowsupdate-module-powershell/) |
| 11. 원격 관리(Remoting) | 83 | [PowerShell Remoting 개념과 WinRM 활성화](/post/powershell/powershell-remoting-winrm-enable-powershell/) |
| 11. 원격 관리(Remoting) | 84 | [Enter-PSSession — 대화형 원격 세션](/post/powershell/enter-pssession-interactive-remote-powershell/) |
| 11. 원격 관리(Remoting) | 85 | [Invoke-Command — 원격 명령 실행](/post/powershell/invoke-command-remote-execution-powershell/) |
| 11. 원격 관리(Remoting) | 86 | [New-PSSession — 지속 세션 관리](/post/powershell/new-pssession-persistent-session-powershell/) |
| 11. 원격 관리(Remoting) | 87 | [Copy-Item -ToSession/-FromSession — 원격 파일 전송](/post/powershell/copy-item-tosession-fromsession-powershell/) |
| 11. 원격 관리(Remoting) | 88 | [SSH 기반 PowerShell Remoting(크로스플랫폼)](/post/powershell/ssh-remoting-cross-platform-powershell/) |
| 12. 프로세스·서비스·예약 작업 | 89 | [Get-Process/Stop-Process — 프로세스 관리](/post/powershell/get-stop-process-command-powershell/) |
| 12. 프로세스·서비스·예약 작업 | 90 | [Start-Process — 외부 프로그램 실행](/post/powershell/start-process-external-program-powershell/) |
| 12. 프로세스·서비스·예약 작업 | 91 | [Get-Service와 서비스 시작/중지/재시작](/post/powershell/get-start-stop-restart-service-powershell/) |
| 12. 프로세스·서비스·예약 작업 | 92 | [ScheduledTasks 모듈 — 예약 작업 등록](/post/powershell/scheduledtasks-module-register-task-powershell/) |
| 12. 프로세스·서비스·예약 작업 | 93 | [Get-WinEvent/Get-EventLog — 이벤트 로그 조회](/post/powershell/get-winevent-get-eventlog-powershell/) |
| 12. 프로세스·서비스·예약 작업 | 94 | [Get-CimInstance/Get-WmiObject — CIM/WMI 조회](/post/powershell/get-ciminstance-get-wmiobject-powershell/) |
| 12. 프로세스·서비스·예약 작업 | 95 | [Get-Counter — 성능 카운터 조회](/post/powershell/get-counter-performance-powershell/) |
| 13. 스토리지와 시스템 구성 | 96 | [Storage 모듈 — Get-Disk/Get-Partition/Get-Volume](/post/powershell/storage-module-disk-partition-volume-powershell/) |
| 13. 스토리지와 시스템 구성 | 97 | [Get-ComputerInfo — 시스템 정보 종합 조회](/post/powershell/get-computerinfo-system-summary-powershell/) |
| 13. 스토리지와 시스템 구성 | 98 | [Env: 드라이브와 환경 변수 관리](/post/powershell/env-drive-environment-variable-powershell/) |
| 13. 스토리지와 시스템 구성 | 99 | [Get-HotFix — 설치된 업데이트 조회](/post/powershell/get-hotfix-installed-update-powershell/) |
| 14. 보안과 자격 증명 | 100 | [Get-Credential과 PSCredential 객체](/post/powershell/get-credential-pscredential-object-powershell/) |
| 14. 보안과 자격 증명 | 101 | [Get-Acl/Set-Acl — 접근 제어 목록](/post/powershell/get-set-acl-access-control-powershell/) |
| 14. 보안과 자격 증명 | 102 | [Set-AuthenticodeSignature — 스크립트 코드 서명](/post/powershell/set-authenticodesignature-code-signing-powershell/) |
| 14. 보안과 자격 증명 | 103 | [Constrained Language Mode와 실행 정책 심화](/post/powershell/constrained-language-mode-execution-policy-powershell/) |
| 14. 보안과 자격 증명 | 104 | [Microsoft.PowerShell.SecretManagement](/post/powershell/secretmanagement-module-powershell/) |
| 14. 보안과 자격 증명 | 105 | [Just Enough Administration(JEA) 개요](/post/powershell/just-enough-administration-jea-overview-powershell/) |
| 15. DSC(Desired State Configuration) | 106 | [DSC 개념과 아키텍처](/post/powershell/dsc-concept-architecture-powershell/) |
| 15. DSC(Desired State Configuration) | 107 | [DSC 구성(Configuration) 작성과 적용](/post/powershell/dsc-configuration-write-apply-powershell/) |
| 15. DSC(Desired State Configuration) | 108 | [DSC 리소스와 로컬 구성 관리자(LCM)](/post/powershell/dsc-resource-lcm-powershell/) |
| 16. 네트워크와 웹 | 109 | [Test-Connection — ping 대응](/post/powershell/test-connection-ping-powershell/) |
| 16. 네트워크와 웹 | 110 | [Test-NetConnection — 포트·경로 진단](/post/powershell/test-netconnection-port-diagnostic-powershell/) |
| 16. 네트워크와 웹 | 111 | [Resolve-DnsName — DNS 질의](/post/powershell/resolve-dnsname-dns-query-powershell/) |
| 16. 네트워크와 웹 | 112 | [Get-NetIPConfiguration/Get-NetAdapter](/post/powershell/get-netipconfiguration-get-netadapter-powershell/) |
| 16. 네트워크와 웹 | 113 | [Invoke-WebRequest/Invoke-RestMethod — HTTP 요청과 REST API](/post/powershell/invoke-webrequest-invoke-restmethod-powershell/) |
| 16. 네트워크와 웹 | 114 | [New-Guid/Get-Random — 유틸리티 cmdlet 모음](/post/powershell/new-guid-get-random-utility-powershell/) |
| 17. 엔터프라이즈 디렉터리 관리 | 115 | [ActiveDirectory 모듈 개요와 Get-ADUser](/post/powershell/activedirectory-module-get-aduser-powershell/) |
| 17. 엔터프라이즈 디렉터리 관리 | 116 | [New-ADUser/Set-ADUser — 계정 생성·수정](/post/powershell/new-aduser-set-aduser-powershell/) |
| 17. 엔터프라이즈 디렉터리 관리 | 117 | [Get-ADGroup/Add-ADGroupMember — 그룹 관리](/post/powershell/get-adgroup-add-adgroupmember-powershell/) |
| 17. 엔터프라이즈 디렉터리 관리 | 118 | [Get-GPO — 그룹 정책 조회(GroupPolicy 모듈)](/post/powershell/get-gpo-grouppolicy-module-powershell/) |
| 18. 마무리와 크로스플랫폼 | 119 | [PowerShell 7의 크로스플랫폼 특징과 새 기능](/post/powershell/powershell-7-cross-platform-features/) |
| 18. 마무리와 크로스플랫폼 | 120 | [PowerShell ISE에서 VS Code로 — 개발 환경 전환](/post/powershell/powershell-ise-to-vscode-transition/) |

번호 시퀀스 밖의 부록으로 [PowerShell ↔ CMD/Bash 명령어 대응표](/post/powershell/powershell-cmd-bash-command-mapping/)를 함께 작성했다 — [CMD 컬렉션](/post/cmd/getting-started-cmd/)·[Bash Shell 컬렉션](/post/bashshell/getting-started-bash-shell/)에서 각각 다룬 명령어를 같은 작업 기준으로 나란히 대조한 색인이다.

## Part별 설계 근거

Part 1(기초 환경과 콘솔, 01–09장)은 PowerShell 자체를 시작하고(01), 도움을 구하고(02 `Get-Help`), 명령어를 검색하고(03 `Get-Command`), 별칭·실행 정책·프로파일·탭 완성·출력 형식(04–09)을 정리하는 최소 조작 능력으로 구성했다. 이후 모든 Part의 예제는 이 콘솔 위에서 실행되므로, 이 최소 조작 능력이 없으면 뒤의 예제를 재현할 수조차 없다.

Part 2(객체 파이프라인 핵심, 10–19장)는 CMD·Bash 경험자가 가장 크게 사고를 전환해야 하는 구간이다. `Get-Member`로 객체 구조를 들여다보고(11), `Where-Object`/`Select-Object`/`Sort-Object`/`ForEach-Object`/`Group-Object`/`Measure-Object`(12–17)로 그 객체를 가공하는 법을 배운다. 이 Part를 건너뛰고 3부 이후로 넘어가면, 이후 모든 챕터의 예제가 왜 그렇게 동작하는지 이해할 수 없다.

Part 3(연산자·자동 변수와 커스텀 객체, 20–29장)은 파이프라인 안에서 조건을 표현하는 연산자(`-eq`, `-and` 등)와 자동 변수(`$_`, `$Error` 등), 그리고 `[PSCustomObject]`로 직접 객체를 만드는 법을 다룬다. `Write-Host`와 `Write-Output`의 차이(29장)를 이 Part의 마지막에 배치한 이유는, 출력 스트림의 차이가 객체 파이프라인을 어느 정도 이해한 뒤에야 왜 문제가 되는지 체감되기 때문이다.

이 Part의 순서 자체도 의존 관계를 따른다. 비교·논리 연산자(20–21장)와 문자열 분리·결합(22장)을 먼저 다룬 뒤에야 타입 캐스팅(23장)에서 "왜 값의 타입이 비교·연산 결과를 좌우하는지"를 구체적인 예로 이해할 수 있고, 자동 변수(24장)와 공통 매개변수(25장)를 알아야 26장의 `-WhatIf`/`-Confirm`이 다른 공통 매개변수와 어떻게 다른 취급을 받는지 대조할 수 있다. `New-Object`(27장)와 `Add-Member`(28장)를 나란히 배치한 이유는 "객체를 새로 만드는 법"과 "이미 있는 객체를 확장하는 법"이 서로 다른 문제라는 점을 짝지어 보여주기 위해서다.

Part 4(파일 시스템과 프로바이더, 30–40장)는 2–3부에서 배운 파이프라인 조작 능력을 실제 대상(파일, 레지스트리)에 처음으로 적용한다. `PSDrive`와 프로바이더 개념(30)을 먼저 배치해, 파일 시스템뿐 아니라 레지스트리(40)·인증서 저장소도 같은 `Get-ChildItem`/`Get-Item` 인터페이스로 다룰 수 있다는 통일성을 먼저 이해하게 했다. 탐색(31–32)에서 조작(33–36)으로, 다시 내용(37)과 속성(38)으로 옮겨가는 순서는 CMD 컬렉션의 2부(파일과 디렉터리 조작)와 논리적으로 같은 흐름을 따르되, 39장의 `Test-Path`로 존재 여부를 미리 확인하는 습관과 40장의 레지스트리 적용 사례로 이 순서가 프로바이더 전반에 그대로 통한다는 점을 마지막에 확인시킨다. 이 Part를 마치고 나면 독자는 "파일에 이 cmdlet을 어떻게 쓰는가"라는 질문 대신 "이 프로바이더에서 컨테이너와 항목 속성이 각각 무엇에 대응하는가"라는 더 일반적인 질문을 던질 수 있게 된다. 이런 일반화 능력은 이후 Part에서 새로운 프로바이더(예: 원격 세션의 파일 시스템)를 마주쳤을 때도 그대로 재사용되며, 낯선 데이터 저장소를 다뤄야 할 때마다 매번 새 명령을 배우는 대신 이미 아는 cmdlet 집합으로 접근할 수 있다는 확신을 준다.

Part 5(데이터 구조와 텍스트/구조화 데이터, 41–52장)는 변수·배열·해시테이블 같은 기본 데이터 구조부터 JSON·CSV 같은 구조화 데이터 변환까지 다룬다. 파일 시스템(4부)에서 읽어온 내용을 실제로 가공하려면 이 Part의 도구가 필요하므로 그 다음에 배치했다. 이 Part의 내부 순서도 의존 관계를 따른다 — 변수와 타입 캐스팅(41)을 먼저 다뤄야 배열(42)과 해시테이블(44) 예제에서 왜 특정 타입으로 값이 저장되는지 설명할 수 있고, 42장에서 배열 `+=`의 성능 문제를 먼저 짚어야 43장의 `ArrayList`/`List<T>`가 어떤 문제를 해결하는 도구인지 자연스럽게 이어진다. 문자열 서식(45)을 정규식(46–47)보다 앞에 둔 이유는, `-match`/`-replace`의 치환 문자열에서 `$` 기호가 문자열 전개와 충돌하는 함정(47장)을 이해하려면 45장의 따옴표 규칙을 먼저 알아야 하기 때문이다. 마지막 세 챕터(48–50)는 JSON·CSV·HTML이라는 서로 다른 구조화 형식으로 객체를 내보내는 법을 나란히 배치해, "형식은 다르지만 파이프라인 끝에서 객체를 텍스트로 직렬화한다"는 공통 패턴을 반복해서 확인시킨다.

Part 6(스크립팅과 흐름 제어, 53–64장)은 1–5부에서 낱개로 실행하던 명령을 반복 가능한 `.ps1` 스크립트와 함수로 묶는다. 스크립트 실행·점 소싱(53)을 먼저 배치해 "스크립트는 자신만의 스코프를 가진다"는 원칙을 먼저 세운 뒤, 조건 분기·반복문(54–56)으로 흐름 제어의 기본기를 다지고, 함수와 고급 함수(57–58), 매개변수 검증·스플래팅·파이프라인 바인딩(59–61)으로 이어지며 함수를 cmdlet처럼 동작하게 만드는 법을 다룬다. 62장의 스코프를 뒤쪽에 배치한 이유는, 53장에서 예고만 해 둔 스코프 규칙을 함수·스크립트 블록 예제가 충분히 쌓인 뒤에야 구체적인 사례로 설명할 수 있기 때문이다. 63장(스크립트 블록과 클로저)이 62장 바로 다음에 오는 것도 같은 이유다 — 클로저는 스코프 규칙의 예외적인 활용이므로, 일반 규칙을 먼저 이해해야 클로저가 왜 특별한지 납득할 수 있다. 마지막 64장의 `#Requires`는 이 Part 전체가 다룬 "실행 가능한 스크립트·함수"라는 결과물에 실행 전제 조건을 거는 안전장치로 배치해, Part 7의 에러 처리로 넘어가기 전 "애초에 잘못된 환경에서 시작하지 않게 막는 법"을 마지막으로 짚는다. 이 흐름 전체를 관통하는 하나의 원칙은, 낱개 명령을 재사용 가능한 단위로 승격시킬수록 그 단위가 지켜야 할 약속(스코프 경계, 입력 검증, 실행 전제 조건)도 함께 늘어난다는 것이며, 이는 뒤이은 Part 7의 에러 처리와 Part 8의 테스트가 왜 필요한지에 대한 직접적인 동기가 된다.

Part 7(에러 처리와 진단, 65–70장)은 6부에서 만든 스크립트가 실패했을 때 무엇을 할지 다룬다. `try`/`catch`/`finally`(65)를 먼저 배치해 표준 예외 처리 모델을 세운 뒤, 66장에서 `$ErrorActionPreference`/`-ErrorAction`으로 비종료 오류를 종료 오류로 전환하는 법을 이어 붙인다 — 이 순서가 뒤바뀌면 "왜 `try`/`catch`가 오류를 못 잡는지"를 설명할 언어가 아직 없는 상태에서 65장을 마쳐야 한다. 67장의 레거시 `trap`은 65–66장으로 표준 처리 방식을 완전히 이해한 뒤에야 "이전에는 어떻게 처리했고 왜 대체됐는지"를 비교할 수 있어 의도적으로 뒤에 놓았다. 이후 68장(진단 출력)·69장(세션 기록)·70장(디버깅)은 오류가 발생하기 전에 상황을 미리 파악하는 도구들로, "오류가 난 뒤 처리"에서 "오류가 나기 전에 관찰"로 이 Part의 관심사가 자연스럽게 옮겨가는 흐름을 만든다.

Part 8(테스트와 코드 품질, 71–73장)은 6–7부에서 작성한 스크립트·함수가 실제로 의도대로 동작하는지 검증하는 세 가지 서로 다른 질문을 순서대로 다룬다 — 71장 Pester는 "정답을 내는가", 72장 PSScriptAnalyzer는 "관례를 지키는가", 73장 `Measure-Command`는 "충분히 빠른가"를 각각 검사한다. 스크립트를 작성하고 에러를 처리할 줄 알아야 그 결과를 테스트할 대상이 생기므로 6–7부 다음에 이 Part를 배치했다. 세 챕터의 순서도 의도적이다 — Pester(71)로 동작의 정확성부터 확인해야, 72장의 PSScriptAnalyzer가 지적하는 관례 위반이 "일단 돌아가는 코드를 더 안전하게 다듬는 문제"이지 정답 자체를 바꾸는 문제가 아니라는 관계가 분명해진다. 73장의 성능 측정을 마지막에 둔 이유는, 42–43장에서 배열과 `List<T>`의 성능 차이를 말로만 설명했던 것을 이 시점에서 실제로 측정해 확인함으로써 이전 Part의 내용을 되짚는 역할도 겸하기 때문이다.

Part 9(모듈과 병렬 처리, 74–79장)는 검증된 함수를 재사용 가능한 모듈(`.psm1`/`.psd1`)로 포장하고, PowerShell Gallery에서 배포·설치하는 법, 그리고 PowerShell 7의 병렬 처리 기능을 다룬다. 74장(모듈 구조)과 75장(임포트·제거)을 먼저 배치해 "내가 만든 모듈을 세션에 불러오는 법"을 익힌 뒤에야, 76장에서 "남이 만들어 배포한 모듈"을 PowerShell Gallery에서 가져오는 것이 같은 임포트 메커니즘 위에서 동작한다는 점이 자연스럽게 이해된다. 77장의 클래스를 그 다음에 둔 이유는, 모듈이 단순히 함수 묶음을 넘어 사용자 정의 **타입**까지 배포하는 단위가 될 수 있음을 보여주기 위해서다. 마지막 78–79장(백그라운드 작업과 병렬 처리)은 이 Part의 결이 살짝 다른 주제이지만, 62장의 스코프 규칙이 프로세스·스레드 경계를 넘을 때 어떻게 더 엄격해지는지(`$using:` 스코프 수정자, Job의 상태 비공유)를 보여주는 사례로서 함께 묶었다 — 이 두 챕터를 마치면 "동시에 여러 일을 처리한다"는 것이 스코프 규칙의 예외가 아니라 확장이라는 관점을 갖게 된다.

Part 10(패키지·업데이트 관리, 80–82장)은 PowerShell 모듈을 넘어 시스템 패키지(PackageManagement, winget)와 Windows 업데이트까지 관리 대상을 넓힌다. 80장을 먼저 배치한 이유는, 76장에서 이미 쓴 `Install-Module`이 사실 PackageManagement라는 더 큰 프레임워크 위의 한 프로바이더에 불과했다는 사실을 짚어, 9부에서 배운 지식이 이 Part에서도 그대로 확장된다는 연결고리를 보여주기 위해서다. 81장의 winget은 PowerShell cmdlet이 아니라 네이티브 실행 파일이라는 점에서 성격이 다른 도구지만, "애플리케이션을 설치·관리한다"는 같은 문제를 다루므로 80장 바로 다음에 배치해 두 접근의 차이(구조화된 객체 vs. 텍스트 출력)를 대조하게 했다. 마지막 82장(Windows 업데이트)은 "애플리케이션"에서 "운영체제 자체"로 관리 대상이 한 단계 더 깊어지는 것을 보여주며 이 Part를 마무리한다.

Part 11(원격 관리, 83–88장)은 지금까지 로컬 세션에서 실행하던 모든 명령을 원격 컴퓨터로 확장한다. WinRM 활성화(83)부터 대화형 세션(84), 일회성 명령 실행(85), 지속 세션(86), 파일 전송(87), SSH 기반 원격(88) 순으로 다룬다. 84장(대화형)을 85장(팬아웃 실행)보다 먼저 배치한 이유는, 한 대의 컴퓨터에 직접 "들어가는" 감각을 먼저 익혀야 그 다음 "여러 컴퓨터에 명령만 보내고 결과를 모은다"는 `Invoke-Command`의 추상화가 왜 필요한지 체감되기 때문이다. 86장의 지속 세션을 84–85장 다음에 배치한 것은, `-ComputerName` 방식의 한계(매 호출마다 상태가 초기화됨)를 먼저 경험해야 `New-PSSession`이 해결하는 문제가 명확해지기 때문이다. 87장(파일 전송)이 지속 세션 바로 다음에 오는 이유는 `-ToSession`/`-FromSession`이 실제로 86장에서 만든 세션 객체를 인자로 받기 때문이며, 마지막 88장(SSH)은 83–87장 전체가 WinRM이라는 하나의 전송 계층 위에서 동작했다는 사실을 드러내면서 "같은 cmdlet들이 전송 계층만 바뀌면 크로스플랫폼으로 확장된다"는 결론으로 이 Part를 마무리한다.

Part 12(프로세스·서비스·예약 작업, 89–95장)는 원격 세션(11부) 위에서 실제로 수행하는 관리 작업 — 프로세스·서비스 제어, 예약 작업, 이벤트 로그·CIM 조회, 성능 카운터 — 을 다룬다. 89장(프로세스)과 91장(서비스)을 나란히 배치한 이유는 둘 다 "지금 실행 중인 것을 조회·제어한다"는 같은 패턴을 공유하되, 서비스에는 프로세스에 없는 의존 관계(-DependentServices)라는 개념이 추가된다는 차이를 대조하기 위해서다. 92장(예약 작업)이 그다음에 오는 것은, 89·91장이 "지금"을 다뤘다면 92장은 "미래에 자동으로 실행될 것"을 다뤄 시간 축을 한 단계 넓히기 때문이다. 마지막 93–95장(이벤트 로그, CIM/WMI, 성능 카운터)은 조회 대상만 다를 뿐 모두 "시스템이 스스로 기록하거나 노출하는 데이터를 구조화된 객체로 읽어온다"는 하나의 패턴을 세 번 반복해서 보여주며, 이 반복을 통해 89–92장에서 배운 개별 cmdlet 지식이 "시스템 조회는 결국 이런 형태를 띤다"는 일반화된 감각으로 굳어지게 한다.

Part 13(스토리지와 시스템 구성, 96–99장)은 디스크·볼륨, 환경 변수, 설치된 업데이트 조회처럼 시스템 구성 상태를 점검하는 도구를 모은다. 96장(스토리지 계층)을 먼저 배치한 이유는, 12부에서 "실행되는 것"을 다뤘다면 이 Part는 "저장되는 공간"으로 시선을 옮긴다는 전환을 분명히 하기 위해서다. 97장의 `Get-ComputerInfo`를 그다음에 둔 것은, 94장의 개별 CIM 클래스 조회와 96장의 개별 스토리지 cmdlet을 각각 배운 뒤에야 "이 여러 조회를 하나로 요약해 주는 cmdlet도 있다"는 사실이 실용적인 지름길로 느껴지기 때문이다. 98장(환경 변수)은 성격이 조금 다르지만, 30장의 프로바이더 개념이 레지스트리·파일 시스템에 이어 환경 변수에도 똑같이 적용된다는 점을 다시 확인시키는 자리로 여기 배치했다. 마지막 99장(설치된 업데이트)은 10부에서 다룬 패키지 관리, 82장의 PSWindowsUpdate와 자연스럽게 연결되며, "설치는 능동적 행위, 조회는 감사 행위"라는 구분으로 이 Part를 마무리한다.

Part 14(보안과 자격 증명, 100–105장)는 지금까지 다룬 모든 관리 작업에 필요한 인증·권한 요소(`PSCredential`, ACL, 코드 서명, 제약된 언어 모드, 비밀 관리, JEA)를 다룬다. 관리 작업의 실체를 먼저 이해해야 그 작업에 필요한 권한 모델이 왜 그렇게 설계됐는지 이해할 수 있어 이 위치에 배치했다. 이 Part의 내부 순서는 신뢰의 층위를 하나씩 쌓아 올린다 — 100장(자격 증명)은 "누가 요청하는가"를, 101장(ACL)은 "그 사람이 이 리소스에 접근할 수 있는가"를, 102장(코드 서명)은 "이 코드 자체를 신뢰할 수 있는가"를 각각 묻는다. 103장의 언어 모드를 그 다음에 둔 이유는, 102장까지의 서명·권한 검증을 통과하지 못한 코드가 실행되더라도 언어 모드가 그 피해 범위를 한 번 더 제한하는 마지막 방어선이기 때문이다. 마지막 104–105장(비밀 관리, JEA)은 이 모든 개별 요소(자격 증명 저장, 권한 위임, 실행 제약)를 실전 아키텍처로 조합하는 사례로 마무리하며, 특히 JEA는 100–103장에서 배운 요소 전부(자격 증명 위임, 세션 구성의 권한 경계, `NoLanguage` 모드)가 하나로 합쳐진 결과라는 점에서 이 Part의 자연스러운 종착점이다.

Part 15(DSC, 106–108장)는 지금까지 명령형으로("이렇게 해라") 수행하던 관리 작업을, "이 상태여야 한다"고 선언하는 구성 관리 프레임워크로 확장한다. 보안 모델(14부)을 이해한 뒤에야 DSC의 리소스 권한·로컬 구성 관리자(LCM) 동작을 온전히 이해할 수 있다. 106장(개념)에서 "정의와 적용이 분리된다"는 DSC의 핵심 아이디어를 먼저 세운 뒤, 107장에서 그 분리된 단계(작성→컴파일→적용→검증)를 실제로 하나씩 밟아 보게 한 순서다. 108장(LCM)을 마지막에 둔 이유는, 107장까지는 "한 번 적용하고 끝"이라는 인상을 줄 수 있는데, LCM의 `ConfigurationMode` 설정이 그 인상을 뒤집어 "적용은 끝이 아니라 지속적인 감시의 시작"이라는 DSC 고유의 관점을 마지막에 각인시키기 위해서다. 이 지속적 감시라는 개념은 69장의 세션 기록, 92장의 예약 작업과도 맞닿아 있지만, DSC는 그 감시와 교정을 사람의 개입 없이 노드 스스로 수행한다는 점에서 이 컬렉션이 다뤄 온 자동화 도구들 중 가장 자율적인 축에 속한다.

Part 16(네트워크와 웹, 109–114장)은 로컬·원격 시스템(11–15부)을 넘어 네트워크 진단과 웹 API 호출로 시야를 넓힌다. 109장(`Test-Connection`)을 가장 먼저 배치한 이유는, 어떤 네트워크 문제든 "일단 살아있는가"라는 가장 기초적인 질문에서 출발하는 진단 순서를 그대로 따르기 위해서다. 110장(`Test-NetConnection`)이 그 바로 다음에 오는 것은 두 cmdlet이 "ping 테스트"라는 같은 문제를 다루되, 전자는 크로스플랫폼 범용 도구이고 후자는 Windows 전용의 더 상세한 진단 도구라는 대조를 곧바로 이어 붙이기 위해서다. 111장(`Resolve-DnsName`)을 그다음에 둔 이유는, 109–110장의 연결성 확인이 실패했을 때 다음으로 의심해야 할 지점이 "이름이 애초에 올바른 주소로 풀리는가"이기 때문이다 — 연결 문제의 상당수가 실제로는 이름 해석 단계에서 발생한다. 112장(`Get-NetIPConfiguration`/`Get-NetAdapter`)은 지금까지 "다른 컴퓨터"를 향했던 시선을 "이 컴퓨터 자체의 네트워크 구성"으로 되돌려, 진단의 출발점이 되는 로컬 설정 확인법을 짚는다. 113장(`Invoke-WebRequest`/`Invoke-RestMethod`)은 연결·이름 해석이 끝난 다음 단계인 "실제로 데이터를 주고받는" 문제로 넘어가며, 이 두 cmdlet을 나란히 배치해 "원시 응답을 다룰 것인가, 파싱된 객체를 다룰 것인가"라는 선택 기준을 대조한다. 마지막 114장(`New-Guid`/`Get-Random`)은 네트워크 주제에서는 살짝 벗어나지만, 113장에서 다룬 API 요청 본문에 고유 식별자를 채우는 등 스크립팅 전반에서 반복적으로 필요한 유틸리티를 Part의 끝에 실용적으로 묶어 배치했다.

Part 17(엔터프라이즈 디렉터리 관리, 115–118장)은 시야를 한 대의 컴퓨터에서 도메인 전체로 넓혀, Active Directory·그룹 정책처럼 조직 전체의 계정·그룹·정책을 관리하는 모듈을 다룬다. 원격 관리(11부)와 보안(14부) 지식이 전제되어야 실제 운영 환경에서 안전하게 계정을 생성·수정할 수 있어 뒤쪽에 배치했다. 내부 순서는 "누가"(115장 `Get-ADUser`로 계정 조회) → "그 계정을 어떻게 만들고 바꾸는가"(116장 `New-ADUser`/`Set-ADUser`) → "여러 계정을 어떻게 묶는가"(117장 `Get-ADGroup`/`Add-ADGroupMember`) → "그 묶음에 무엇을 강제하는가"(118장 `Get-GPO`)로, 개별 계정에서 시작해 점점 더 넓은 단위로 관리 대상을 확장하는 흐름을 따른다. 115장을 조회 전용으로 먼저 배치한 이유는, 116장의 생성·수정처럼 되돌리기 어려운 작업에 들어가기 전에 먼저 안전한 읽기 전용 조작으로 AD의 필터 문법(`-Filter`, `-LDAPFilter`)에 익숙해지게 하기 위해서다. 117장이 116장 바로 다음에 오는 것은, 실무에서 권한이 거의 항상 개별 계정이 아니라 그룹 단위로 부여되기 때문에 "계정을 만들었으면 곧바로 적절한 그룹에 넣는다"는 실제 작업 순서를 그대로 반영한 것이다. 마지막 118장(GPO)은 성격이 사용자·그룹 관리와는 다르지만, "이 조직 구조에 무엇이 적용되는가"라는 세 번째 축을 더해 Part 17이 다루는 엔터프라이즈 디렉터리 관리의 세 요소(계정·그룹·정책)를 모두 갖추며 마무리한다.

Part 18(마무리와 크로스플랫폼, 119–120장)은 이 컬렉션 전체를 지탱해 온 실행 기반 자체로 돌아가 과정을 닫는다. 119장은 지금까지 곳곳에서 "이 cmdlet은 Windows 전용"이라고 짚었던 경계선(94장 CIM/WMI, 110–112장 NetTCPIP/NetAdapter, 115–118장 ActiveDirectory/GroupPolicy)의 근본 원인이 Windows PowerShell 5.1(.NET Framework)과 PowerShell 7(.NET) 사이의 런타임 차이에 있다는 점을 마지막으로 종합해 보여준다 — 1부에서 당연하게 시작했던 `pwsh` 콘솔이 사실은 그 자체로 하나의 독립된 재구현이었다는 사실을 이 시점에 되짚는 것이다. 120장을 그 바로 다음에 둔 이유는, 119장에서 정리한 5.1/7 공존 현실이 실무에서 결국 "어떤 편집기로 이 두 버전을 동시에 다룰 것인가"라는 도구 선택의 문제로 이어지기 때문이다 — ISE가 더 이상 신규 기능을 받지 않는 것도, 119장에서 배운 것과 같은 이유(.NET Framework 전용, PowerShell 6 이상 미지원)에서 비롯된 결과다. 이 마지막 Part는 새로운 cmdlet을 가르치기보다, 1–17부에서 익힌 지식을 계속 실무에 적용해 나갈 실행 환경 자체를 점검하며 컬렉션을 마무리한다.

## 선수 지식

이 과정을 시작하는 데 필요한 사전 지식은 많지 않다. Windows나 크로스플랫폼 터미널에서 PowerShell 콘솔(`pwsh.exe` 또는 `powershell.exe`)을 열고 텍스트로 명령을 입력하는 것에 거부감이 없으면 충분하며, 프로그래밍 경험은 필수가 아니다. 다만 6부(스크립팅과 흐름 제어)에 들어가면 변수·조건문·반복문·함수 같은 프로그래밍의 기본 개념을 다루므로, 다른 언어나 셸(Bash, Python 등)에서 비슷한 구문을 써본 경험이 있으면 그 구간을 훨씬 빠르게 소화할 수 있다.

CMD·Bash를 먼저 배운 독자라면 이 컬렉션과 짝을 이루는 [Windows CMD 컬렉션](/post/cmd/getting-started-cmd/)·[Bash Shell 컬렉션](/post/bashshell/getting-started-bash-shell/)에서 텍스트 기반 셸의 기본 조작을 이미 다뤘을 수 있다. 세 컬렉션은 서로를 대체하지 않는다 — CMD·Bash 경험자는 이 컬렉션의 2부(객체 파이프라인 핵심)에서 "텍스트 파싱 대신 객체를 다룬다"는 가장 큰 사고 전환을 특히 주의 깊게 읽으면 되고, PowerShell을 먼저 배운 독자가 CMD·Bash 컬렉션을 참고할 때는 반대로 "객체가 아니라 텍스트를 다룬다"는 차이를 염두에 두면 된다.

## 완주 시 갖추는 역량

이 컬렉션을 끝까지 따라가면 "cmdlet을 안다"는 수준을 넘어, Windows·크로스플랫폼 인프라 환경에 던져졌을 때 스스로 상황을 진단하고 자동화·원격 관리를 안전하게 수행하는 실무 역량을 갖추는 것을 목표로 한다.

- 객체 파이프라인의 동작 원리를 이해하고, `Where-Object`/`Select-Object`/`Sort-Object`/`ForEach-Object`로 원하는 데이터를 즉석에서 가공할 수 있다.
- 재사용 가능한 함수·스크립트·모듈을 작성하고, `try`/`catch`로 에러를 처리하며 Pester로 그 동작을 검증할 수 있다.
- `Invoke-Command`·`Enter-PSSession`으로 원격 시스템에 접속해 프로세스·서비스·이벤트 로그를 조회·제어할 수 있다.
- `PSCredential`·ACL·코드 서명 같은 PowerShell 보안 모델을 이해하고, 안전하게 자격 증명을 다룰 수 있다.
- DSC로 인프라 상태를 선언적으로 정의하고, Active Directory 모듈로 조직의 계정·그룹을 관리할 수 있다.
- Windows PowerShell 5.1과 PowerShell 7의 차이를 구분해, 상황에 맞는 버전을 선택할 수 있다.

## 다음 장에서는

다음 장인 [01장: PowerShell 소개](/post/powershell/powershell-pwsh-introduction-cross-platform-shell/)에서는 Windows PowerShell과 PowerShell 7(pwsh)의 관계, 콘솔을 시작·종료하는 법을 다룬다. 이로써 00–120장 전체 121개 챕터와 [PowerShell ↔ CMD/Bash 명령어 대응표](/post/powershell/powershell-cmd-bash-command-mapping/) 부록까지 이 컬렉션의 전체 커리큘럼이 완성됐다.

## 평가 기준

이 장을 읽은 후 다음을 할 수 있어야 한다.

- 체계적으로 순서대로 학습하는 방식과 필요할 때 cmdlet을 검색해서 익히는 방식의 장단점을 설명하고, 자신의 상황에 맞게 선택할 수 있다.
- PowerShell이 CMD·전통적 Bash 스크립팅과 근본적으로 다른 지점(텍스트가 아닌 .NET 객체 파이프라인)을 설명할 수 있다.
- 18개 Part(기초-파이프라인-연산자-파일시스템-데이터-스크립팅-에러처리-테스트-모듈-패키지-원격-프로세스-스토리지-보안-DSC-네트워크-디렉터리-마무리)가 왜 이 순서인지 말할 수 있다.
- Windows PowerShell 5.1과 PowerShell 7(pwsh)의 차이(플랫폼, 기반 런타임)를 설명할 수 있다.
- `dir` 같은 별칭이 실제로는 어떤 cmdlet을 가리키는지 `Get-Command`로 확인하는 방법을 설명할 수 있다.

## 참고 및 출처

- [What is PowerShell? - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/scripting/overview)
- [Differences between Windows PowerShell 5.1 and PowerShell 7.x | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/scripting/whats-new/differences-from-windows-powershell)
