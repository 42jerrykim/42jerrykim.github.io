---
draft: false
slug: bcdedit-command-boot-configuration-editor-windows-cmd
title: "[CMD] 80. bcdedit - 부팅 구성 데이터 편집"
description: "bcdedit로 BCD 저장소의 부팅 항목을 조회·생성·수정·삭제하는 법과 부팅 관리자의 기본 항목·타임아웃을 바꾸는 절차, 관리자 권한이 필요한 이유를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 800
categories:
- CMD
tags:
- Windows(윈도우)
- Shell(셸)
- Terminal
- Command
- Guide(가이드)
- Reference(참고)
- Quick-Reference
- How-To
- Tips
- Advanced
- bcdedit
- 부팅구성
- BCD
- Boot(부팅)
- Recovery(복구)
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Administration
- Education(교육)
- CLI
- Configuration(설정)
- System(시스템)
- Scripting(스크립팅)
- Enterprise
image: "wordcloud.png"
---

bcdedit는 BCD(Boot Configuration Data) 저장소를 조회·생성·수정하는 명령줄 도구로, Windows Vista 이후 버전에서 이전의 Boot.ini를 대체하는 부팅 구성을 관리한다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [79장: bcdboot](/post/cmd/bcdboot-command-boot-configuration-data-windows-cmd/)에서 부팅 파일을 시스템 파티션에 배치하는 법을 다룬 뒤 이어진다. bcdboot가 BCD 저장소를 새로 만드는 도구였다면, bcdedit는 이미 존재하는 그 저장소의 항목 하나하나를 세밀하게 편집하는 도구다.

**이 장의 깊이**: 고급. **다루지 않는 것**: 개별 부팅 파일을 시스템 파티션에 배치하는 작업은 79장(bcdboot)이 담당한다.

## 개요 + 정신 모델

bcdedit가 다루는 대상은 파일이 아니라 **저장소(store) 안의 항목(entry)**이다.

> "BCDEdit is a command-line tool for managing BCD stores. It can be used for a variety of purposes, including creating new stores, modifying existing stores, adding boot menu parameters, and so on." — Microsoft Learn, "bcdedit"

BCD 저장소는 부팅 관리자 항목, 각 운영체제의 부팅 로더 항목 등 여러 항목으로 구성된 레지스트리형 데이터베이스다. bcdedit의 모든 하위 명령은 "어느 저장소(`/store`, 기본은 시스템 저장소)의, 어느 항목의, 어느 옵션 값을 조회·변경할 것인가"라는 세 축으로 구조화되어 있다.

## 사용법

```
bcdedit /명령 [<인수1>] [<인수2>] ...
```

## 옵션

### 저장소 자체를 다루는 명령

| 명령 | 설명 |
|---|---|
| `/createstore` | 새 빈 BCD 저장소 생성(시스템 저장소가 아님) |
| `/export` | 시스템 저장소 내용을 파일로 내보내기(복원용 백업) |
| `/import` | `/export`로 만든 백업 파일로 시스템 저장소 복원(기존 항목 전체 삭제 후 가져오기) |
| `/store` | 대상 저장소 지정(생략 시 시스템 저장소) |

### 저장소 안의 항목을 다루는 명령

| 명령 | 설명 |
|---|---|
| `/copy` | 같은 저장소 안에서 부팅 항목 복사 |
| `/create` | 새 항목 생성 |
| `/delete` | 항목 삭제 |

### 항목의 옵션 값을 다루는 명령

| 명령 | 설명 |
|---|---|
| `/set` | 항목 옵션 값 설정 |
| `/deletevalue` | 항목에서 특정 옵션 값 삭제 |

### 출력을 제어하는 명령

| 명령 | 설명 |
|---|---|
| `/enum` | 저장소의 항목 나열(기본 동작 — 인수 없이 `bcdedit`만 실행하면 `/enum active`와 동일) |
| `/v` | 상세 모드(친숙한 축약 식별자 대신 전체 식별자 표시) |

### 부팅 관리자를 제어하는 명령

| 명령 | 설명 |
|---|---|
| `/default` | 타임아웃 만료 시 부팅 관리자가 선택할 기본 항목 지정 |
| `/displayorder` | 부팅 관리자가 항목을 표시하는 순서 지정 |
| `/timeout` | 부팅 관리자가 기본 항목을 선택하기까지 대기할 시간(초) |
| `/bootsequence` | 다음 부팅 1회에만 적용되는 표시 순서 지정 |

## 예시

```
bcdedit
bcdedit /enum
bcdedit /enum all
bcdedit /v
bcdedit /default {current}
bcdedit /timeout 10
bcdedit /set {current} description "My Windows"
bcdedit /export C:\BCD_Backup
```

## 주의사항·함정

**관리자 권한이 필수다**: BCD를 수정하려면 관리자 권한으로 CMD를 실행해야 한다.

> "Administrative privileges are required to use BCDEdit to modify BCD." — Microsoft Learn, "bcdedit"

조회(`/enum`)는 일반 권한으로도 가능하지만, `/set`·`/delete`·`/create` 등 저장소를 변경하는 모든 명령은 관리자 권한 없이 실행하면 실패한다.

**변경 전에 반드시 백업한다**: BCD 항목을 잘못 수정하면 시스템이 부팅되지 않을 수 있다. `/export`로 현재 시스템 저장소를 파일로 내보내 두면, 문제가 생겼을 때 `/import`로 원상 복구할 수 있다. 42장(chkdsk)·79장(bcdboot)과 마찬가지로 이 명령은 실행 전 확인·백업 절차가 필수인 "복구 불가 동작" 범주에 속한다.

**단순 변경에 최적화되어 있다**: Microsoft Learn은 bcdedit가 "표준 데이터 형식에 한정되며 주로 BCD에 대한 단일하고 일반적인 변경을 수행하도록 설계되었다"고 명시한다. 더 복잡한 작업이나 비표준 데이터 형식을 다뤄야 한다면 BCD WMI API를 직접 쓰는 편이 낫다 — 즉 bcdedit는 GUI 없는 환경에서 몇 개 항목을 빠르게 고치는 용도지, 대규모 부팅 구성 자동화 도구는 아니다.

**PowerShell에서도 결국 bcdedit.exe를 그대로 호출한다**: PowerShell 스크립트 안에서 BCD를 조작하려 해도 실무에서는 `Start-Process bcdedit -ArgumentList ...`나 `bcdedit /set ...`처럼 bcdedit.exe 자체를 그대로 부르는 경우가 대부분이다. 앞서 언급한 BCD WMI 공급자(`root\WMI` 네임스페이스의 `BcdObject` 클래스)가 이론적으로는 더 낮은 수준에서 BCD를 다룰 수 있게 해주지만, 문서화가 부실하고 다루기 복잡해 일부 고급 배포 스크립트를 제외하면 거의 쓰이지 않는다. 실용적인 관점에서는 PowerShell 환경에서도 bcdedit.exe가 여전히 사실상 유일한 주력 인터페이스다.

## 흔한 오개념

<strong>"bcdedit는 GUI의 '시스템 구성'(msconfig.exe) '부팅' 탭과 사실상 같은 것이다"</strong>는 오해다. msconfig의 부팅 탭은 타임아웃, 기본 운영체제 선택, 안전 부팅 전환 정도의 단순화된 하위 집합만 노출한다. 반면 bcdedit는 BCD 저장소 전체 — 디버깅 설정, EMS(비상 관리 콘솔), 여러 부팅 로더 항목의 세부 옵션 등 msconfig의 GUI에는 아예 나타나지 않는 항목까지 — 에 접근할 수 있다.

## 다음 장에서는

다음은 81장 — 파일 확장명과 파일 형식의 연결을 다루는 `assoc` 명령을 다룬다.

## 평가 기준

- bcdedit로 BCD 저장소의 항목을 조회(`/enum`)하고 기본 항목·타임아웃을 설정(`/default`, `/timeout`)할 수 있다.
- bcdedit가 관리자 권한을 요구하는 이유와, 변경 전 `/export`로 백업해야 하는 이유를 설명할 수 있다.
- bcdedit가 단순 변경에 최적화된 도구이며 복잡한 작업에는 BCD WMI API가 권장된다는 것을 안다.
- bcdboot(파일 배치)와 bcdedit(항목 편집)의 역할 차이를 재확인할 수 있다.

## 참고

- [bcdedit | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/bcdedit)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
