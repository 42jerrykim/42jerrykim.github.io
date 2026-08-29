---
draft: false
slug: robocopy-command-mirror-copy-files-windows
title: "[CMD] 16. robocopy - 재시도와 미러링을 지원하는 고급 복사"
description: "robocopy로 파일·디렉터리를 견고하게 복사·미러링하는 법과 /mir가 대상의 여분 파일을 삭제한다는 위험, /r·/w 재시도 옵션, 8단계로 세분화된 종료 코드 해석법을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 160
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
- robocopy
- 미러링
- File-System
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Troubleshooting(트러블슈팅)
- ERRORLEVEL
- Batch
- Deployment(배포)
- Backup
- CLI
- Comparison(비교)
- Configuration(설정)
- Beginner
image: "wordcloud.png"
---

robocopy(Robust File Copy)는 파일 데이터를 한 위치에서 다른 위치로 복사하는 명령이다. copy·xcopy보다 재시도·로깅·미러링 기능이 훨씬 풍부해 실무 백업·배포 스크립트의 기본값으로 널리 쓰인다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [15장: xcopy](/post/cmd/xcopy-command-copy-directory-tree-windows-cmd/)에서 디렉터리 트리 복사를 다룬 뒤 이어지며, 복사 계열 3장(14–16장)의 마지막이다. copy(파일 단위) → xcopy(트리 단위) → robocopy(견고성·동기화)로 다루는 범위와 신뢰성이 단계적으로 넓어지는 흐름의 종착점이다.

**이 장의 깊이**: 중급–고급. 옵션이 매우 많으므로 자주 쓰는 것 위주로 다루고 전체 옵션은 참고 링크로 안내한다. **다루지 않는 것**: I/O 스로틀링(`/ipg`, `/iorate`)처럼 대규모 네트워크 환경 전용 옵션은 이 장의 범위 밖이다.

## 사용법

```
robocopy <원본> <대상> [<파일>...] [<옵션>]
```

## 옵션

### 복사 범위

| 옵션 | 설명 |
|---|---|
| `/s` | 하위 디렉터리 복사(빈 디렉터리 자동 제외) |
| `/e` | 하위 디렉터리 복사(빈 디렉터리 포함) |
| `/lev:n` | 원본 트리의 상위 n단계까지만 복사 |
| `/mir` | 미러링. `/e`에 `/purge`를 더한 것과 같음 |
| `/mov` | 파일을 이동(복사 후 원본에서 삭제) |
| `/move` | 파일과 디렉터리를 이동 |

### 견고성

| 옵션 | 설명 |
|---|---|
| `/z` | 재시작 가능 모드로 복사(중단되면 이어서 진행) |
| `/zb` | 재시작 가능 모드로 시도하고, 접근 거부 시 백업 모드로 전환 |
| `/mt:n` | n개 스레드로 다중 스레드 복사(기본 8, 최대 128) |
| `/r:n` | 실패 시 재시도 횟수(기본 100만) |
| `/w:n` | 재시도 대기 시간(초, 기본 30) |

### 로깅

| 옵션 | 설명 |
|---|---|
| `/log:파일` | 상태 출력을 로그 파일에 기록(기존 내용 덮어씀) |
| `/log+:파일` | 로그 파일에 이어서 기록 |
| `/eta` | 예상 완료 시각 표시 |
| `/np` | 진행 상황(복사된 파일·디렉터리 수) 표시 안 함 |

### 필터

| 옵션 | 설명 |
|---|---|
| `/xd <디렉터리>` | 지정 이름·경로와 일치하는 디렉터리 제외 |
| `/xf <파일>` | 지정 이름과 일치하는 파일 제외 |
| `/maxage:n` | n일보다 오래된 파일 제외 |

## 예시

```
robocopy C:\Users\Admin\Records D:\Backup /E /ZB /LOG:C:\Logs\Backup.log
robocopy C:\Users\Admin\Records D:\Backup /MIR /R:2 /W:5 /LOG:C:\Logs\Backup.log
robocopy C:\Users\Admin\Records D:\Backup /S /E /COPY:DAT /MT:16 /LOG:C:\Logs\Backup.log
robocopy C:\Users\Admin\Records D:\Backup /S /MAXAGE:7 /MOV /LOG:C:\Logs\Backup.log
```

## 주의사항·함정

**`/mir`(그리고 `/purge`)는 대상의 파일을 삭제한다**: robocopy에서 가장 위험한 함정이다. `/mir`는 원본에 없는 파일·디렉터리를 대상에서 지워 두 트리를 완전히 동일하게 맞춘다. 대상 경로를 잘못 지정하면 그 경로에 있던, 원본과 무관한 파일까지 함께 사라진다. 실행 전 원본·대상 경로 순서를 반드시 재확인하고, 처음에는 `/l`(목록만 표시, 실제로 복사·삭제하지 않음)로 미리 확인하는 습관을 들이는 것이 안전하다.

**종료 코드는 비트 플래그다**: robocopy의 종료 코드는 성공/실패 하나로 끝나지 않고, 여러 상태를 비트 조합으로 나타낸다.

| 값 | 의미 |
|---|---|
| 0 | 복사한 파일 없음, 실패 없음(대상에 이미 존재해 건너뜀) |
| 1 | 모든 파일이 성공적으로 복사됨 |
| 2 | 대상에만 있는 추가 파일 존재, 복사된 파일 없음 |
| 3 | 일부 복사됨, 추가 파일도 존재, 실패 없음 |
| 8 이상 | 하나 이상의 복사 실패 발생 |

> "Any value equal to or greater than **8** indicates that there was at least one failure during the copy operation." — Microsoft Learn, "Robocopy"

xcopy처럼 단순히 "0이면 성공, 그 외는 실패"로 해석하면 안 된다. 2·3처럼 실패 없이도 0이 아닌 코드가 흔히 나오므로, 배치 스크립트에서는 보통 `if %ERRORLEVEL% geq 8`처럼 8 이상인지만 검사해 진짜 실패만 걸러낸다.

**`/mt`(다중 스레드)와 `/log` 조합을 권장한다**: 다중 스레드로 복사하면 콘솔 출력 순서가 뒤섞이므로, Microsoft Learn은 `/mt`를 쓸 때 `/log`로 출력을 파일에 남기는 것을 권장한다. `/mt`는 `/ipg`(대역폭 제한), `/efsraw`(EFS 원시 복사)와 함께 쓸 수 없다는 제약도 있다.

**PowerShell에는 robocopy를 대체할 네이티브 명령이 없다**: `Copy-Item -Recurse`는 robocopy의 실패 시 자동 재시도(`/r`, `/w`), 미러링(`/mir`로 대상의 여분 파일까지 삭제해 두 트리를 일치시키는 것), 다중 스레드 복사 같은 기능을 전혀 갖고 있지 않다. 그래서 실무에서 견고한 파일 동기화가 필요한 PowerShell 스크립트조차 이 부분만은 `robocopy.exe`를 외부 프로세스로 그대로 호출하는 경우가 많다 — PowerShell 진영에 robocopy의 핵심 가치를 대신할 네이티브 대안이 아직 없기 때문이다. 참고로 PowerShell 스크립트 안에서 robocopy를 호출할 때는 `/MIR`처럼 `/`로 시작하는 스위치가 PowerShell 자체의 파서에 의해 매개변수로 오인되는 경우가 있으니, 필요하면 따옴표로 감싸는 등 인용 처리에 주의해야 한다.

## 흔한 오개념

<strong>"robocopy는 항상 xcopy의 상위 호환이라 무조건 더 안전하다"</strong>는 오해가 있다. 재시도·다중 스레드·로깅 면에서는 확실히 더 견고하지만, `/mir`처럼 대상을 원본에 맞춰 파괴적으로 정리하는 옵션은 xcopy에 없는 위험이기도 하다. "더 강력한 도구"가 곧 "더 안전한 도구"를 뜻하지 않는다는 점을 이 장에서 특히 강조하는 이유다.

## 다음 장에서는

다음은 17장 — 복사가 아니라 실제로 파일·디렉터리 위치를 옮기는 `move` 명령을 다룬다.

## 평가 기준

- `/s`, `/e`, `/mir`의 차이와 `/mir`가 대상 파일을 삭제할 수 있다는 위험을 설명할 수 있다.
- `/r`, `/w`로 재시도 동작을 조정하고, `/mt`로 다중 스레드 복사를 구성할 수 있다.
- robocopy 종료 코드가 비트 플래그이며 8 이상만 진짜 실패를 뜻한다는 것을 설명할 수 있다.
- robocopy가 xcopy보다 견고하지만 그만큼 더 위험한 옵션도 가지고 있다는 트레이드오프를 설명할 수 있다.

## 참고

- [Robocopy | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/robocopy)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
