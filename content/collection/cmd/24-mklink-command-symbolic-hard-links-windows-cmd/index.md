---
draft: false
slug: mklink-command-symbolic-hard-links-windows-cmd
title: "[CMD] 24. mklink - 심볼릭 링크와 하드 링크 생성"
description: "mklink로 파일·디렉터리 심볼릭 링크, 하드 링크, 디렉터리 정션을 만드는 법과 각 링크 종류의 차이, 관리자 권한이 필요한 이유, 볼륨을 넘나들 수 없는 하드 링크의 제약을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 240
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
- mklink
- 심볼릭링크
- 하드링크
- File-System
- NTFS
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Troubleshooting(트러블슈팅)
- Linux(리눅스)
- Education(교육)
- CLI
- Security(보안)
- Configuration(설정)
- Beginner
image: "wordcloud.png"
---

mklink는 파일 또는 디렉터리에 대한 심볼릭 링크나 하드 링크를 만드는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [23장: fc](/post/cmd/fc-command-compare-files-differences-windows-cmd/)에서 파일 비교 명령을 마친 뒤 이어진다. 지금까지 다룬 명령이 파일의 내용·속성을 조작했다면, mklink는 파일 시스템 안에 "실제 파일이 아니라 다른 대상을 가리키는 항목"을 새로 만든다는 점에서 성격이 다르다.

**이 장의 깊이**: 중급–고급. **다루지 않는 것**: NTFS 압축은 47장(compact)에서, 파일 시스템 저수준 조회는 48장(fsutil)에서 각각 다룬다.

## 개요 + 정신 모델

mklink가 만드는 세 종류의 링크는 각각 가리키는 방식이 다르다. 심볼릭 링크는 경로 문자열을 담은 특수 파일로, 대상이 없어도 만들 수 있고 다른 볼륨·네트워크 경로도 가리킬 수 있다. 하드 링크는 파일 시스템 수준에서 같은 데이터(같은 inode에 해당하는 MFT 항목)를 가리키는 또 다른 이름표이므로, 대상 파일이 지워져도 하드 링크로 그 데이터에 계속 접근할 수 있다. 정션(junction)은 디렉터리 전용 링크로, 심볼릭 링크와 비슷하지만 더 오래된 메커니즘이며 로컬 볼륨끼리만 연결할 수 있다.

## 사용법

```
mklink [[/d] | [/h] | [/j]] <링크> <대상>
```

## 옵션

| 옵션 | 설명 |
|---|---|
| (없음) | 파일에 대한 심볼릭 링크 생성(기본값) |
| `/d` | 디렉터리에 대한 심볼릭 링크 생성 |
| `/h` | 하드 링크 생성(심볼릭 링크 대신) |
| `/j` | 디렉터리 정션 생성 |

## 예시

```
mklink MyLink.txt C:\Data\RealFile.txt
mklink /d C:\LinkDir D:\RealDir
mklink /h hardlink.txt original.txt
mklink /j C:\Junction D:\Target
```

링크를 지울 때는 링크 자체가 파일·디렉터리 형태를 취하므로 각각 del·rd로 지운다.

```
rd \MyFolder
del \MyFile.file
```

## 주의사항·함정

**심볼릭 링크·정션 생성은 관리자 권한이 필요할 수 있다**: 기본적으로 심볼릭 링크를 만들려면 관리자 권한 CMD 세션이 필요하다. Windows 10 이후 "개발자 모드"를 켜면 일반 사용자 권한으로도 디렉터리 심볼릭 링크를 만들 수 있게 완화된다. 이 제약을 모르면 스크립트가 "액세스가 거부되었습니다" 오류로 조용히 실패한 이유를 찾기 어렵다.

**하드 링크는 같은 볼륨 안에서만, 파일에만 만들 수 있다**: 하드 링크는 같은 파일 시스템의 같은 데이터를 가리키는 또 다른 항목이므로, 물리적으로 다른 볼륨(다른 드라이브 문자)을 넘나들 수 없다. 또한 디렉터리에는 하드 링크를 만들 수 없다 — 디렉터리를 링크로 연결하려면 `/d`(심볼릭 링크)나 `/j`(정션)를 써야 한다.

**대상을 지워도 하드 링크는 살아있다**: 심볼릭 링크는 대상 경로 문자열만 담고 있어 대상이 사라지면 "끊어진 링크"가 되지만, 하드 링크는 실제 데이터를 함께 가리키고 있어 원본으로 만든 이름이 삭제돼도 하드 링크로 만든 다른 이름으로는 여전히 같은 데이터에 접근할 수 있다. 데이터가 완전히 사라지는 시점은 그 데이터를 가리키는 모든 이름(원본+모든 하드 링크)이 삭제됐을 때다.

**PowerShell 5.0 이상에서는 `New-Item -ItemType SymbolicLink`로 같은 작업을 한다**: 심볼릭 링크는 `New-Item -ItemType SymbolicLink -Path <링크> -Target <대상>`으로, 하드 링크는 `-ItemType HardLink`로, 정션은 `-ItemType Junction`으로 각각 만든다 — mklink의 옵션 스위치(`/d`, `/h`, `/j`) 대신 `-ItemType` 값으로 종류를 구분하는 방식이다. 위에서 다룬 관리자 권한 요구와 개발자 모드 예외는 mklink만의 특성이 아니라 OS 차원의 정책이므로, `New-Item -ItemType SymbolicLink`를 쓰더라도 관리자 권한이 필요하고 개발자 모드를 켰을 때 완화되는 조건은 동일하게 적용된다.

## 흔한 오개념

<strong>"심볼릭 링크와 정션은 사실상 같은 것이다"</strong>는 오해가 흔하다. 둘 다 디렉터리를 다른 곳으로 연결한다는 결과는 비슷해 보이지만, 정션은 로컬 볼륨끼리만 연결할 수 있고 네트워크 경로를 지원하지 않는 더 오래된 메커니즘인 반면, 심볼릭 링크는 다른 볼륨은 물론 네트워크 UNC 경로까지 가리킬 수 있어 활용 범위가 더 넓다. 새로 작성하는 스크립트라면 특별한 이유가 없는 한 정션(`/j`)보다 디렉터리 심볼릭 링크(`/d`)를 우선 고려하는 것이 일반적이다.

## 다음 장에서는

다음은 25장 — Part 2의 마지막 장으로, 대상 디렉터리의 파일을 원본으로 교체하거나 없는 파일만 추가하는 `replace` 명령을 다룬다.

## 평가 기준

- 심볼릭 링크·하드 링크·정션 세 종류의 차이(가리키는 방식, 볼륨을 넘나들 수 있는지, 파일/디렉터리 대상 여부)를 설명할 수 있다.
- 심볼릭 링크 생성에 관리자 권한이 필요한 이유와, 개발자 모드가 이를 어떻게 완화하는지 안다.
- 원본 파일을 지워도 하드 링크로 데이터에 계속 접근할 수 있는 이유를 설명할 수 있다.
- 정션과 심볼릭 링크 중 새 스크립트에 어느 것을 우선 고려해야 하는지 판단할 수 있다.

## 참고

- [mklink | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/mklink)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
