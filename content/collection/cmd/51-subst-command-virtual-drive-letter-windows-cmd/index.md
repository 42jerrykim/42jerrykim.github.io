---
draft: false
slug: subst-command-virtual-drive-letter-windows-cmd
title: "[CMD] 51. subst - 경로를 가상 드라이브 문자에 연결"
description: "subst로 긴 로컬 경로를 짧은 가상 드라이브 문자에 연결하는 법과 chkdsk·format·label 등을 subst 드라이브에 쓸 수 없는 제약, 재부팅하면 연결이 사라지는 세션 한정 특성을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 510
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
- Beginner
- subst
- 가상드라이브
- File-System
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Education(교육)
- CLI
- Productivity(생산성)
- Comparison(비교)
- Configuration(설정)
- Advanced
- Administration
- Workflow(워크플로우)
- System(시스템)
image: "wordcloud.png"
---

subst는 로컬 경로를 가상 드라이브 문자에 연결하는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [50장: vol](/post/cmd/vol-command-display-volume-label-windows-cmd/)에서 볼륨 정보를 조회하는 법을 다룬 뒤 이어진다. 11장(pushd, popd)에서 명령 확장이 켜져 있을 때 pushd가 네트워크 UNC 경로를 임시 드라이브 문자로 매핑한다고 다뤘는데, subst는 그 개념을 로컬 경로에 대해 더 직접적으로 제공하는 명령이다.

**이 장의 깊이**: 입문–중급.

## 사용법

```
subst [<드라이브1>: [<드라이브2>:]<경로>]
subst <드라이브1>: /d
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `<드라이브1>:` | 연결할 가상 드라이브 문자 |
| `[<드라이브2>:]<경로>` | 연결 대상이 될 실제 드라이브와 경로 |
| `/d` | 지정한 가상 드라이브 연결 해제 |

인수 없이 실행하면 현재 활성화된 모든 가상 드라이브 연결 목록을 표시한다.

## 예시

```
subst
subst z: b:\user\betty\forms
z:
dir
subst z: /d
```

## 주의사항·함정

**일부 명령은 subst 드라이브에서 쓸 수 없다**: Microsoft Learn은 subst로 만든 드라이브에서 동작하지 않는 명령 목록을 명시한다.

> "The following commands don't work and must not be used on drives specified in the subst command: chkdsk, diskcomp, diskcopy, format, label, recover." — Microsoft Learn, "subst"

42장(chkdsk), 45장(format), 49장(label), 52장(recover)에서 배운 명령들이 여기 포함된다. subst 드라이브는 물리 드라이브를 흉내 낸 가상 매핑일 뿐이라, 물리 디스크 구조를 직접 다루는 이 명령들은 애초에 대상을 찾지 못한다.

**드라이브 문자는 lastdrive 범위 안에 있어야 한다**: 지정한 가상 드라이브 문자가 시스템에 설정된 사용 가능 드라이브 문자 범위를 벗어나면 오류가 난다.

> "The `<drive1>` parameter must be within the range that is specified by the **lastdrive** command. If not, **subst** displays the following error message: Invalid parameter - drive1:" — Microsoft Learn, "subst"

**세션 한정이며 재부팅하면 사라진다**: subst로 만든 연결은 현재 로그온 세션에만 유지되고, 재부팅하면 사라진다. 매번 같은 매핑이 필요하다면 로그인 스크립트나 시작 프로그램에서 subst를 실행하도록 등록해야 한다.

**PowerShell의 느슨한 대응은 `New-PSDrive`다**: `New-PSDrive -Name Z -PSProvider FileSystem -Root <경로>`로 비슷한 매핑을 만들 수 있지만, 이렇게 만든 드라이브는 해당 PowerShell 세션에서만 보이는 논리적 드라이브일 뿐, subst가 만드는 것과 같은 실제 Win32 드라이브 문자가 아니다 — 탐색기나 다른 프로그램에서는 보이지 않는다. 시스템 전역에서 다른 애플리케이션도 인식하는 드라이브 문자가 필요하다면 여전히 subst를 써야 한다.

## 흔한 오개념

<strong>"subst는 pushd의 네트워크 드라이브 매핑과 완전히 같은 기능이다"</strong>는 오해가 있다. 11장에서 다룬 pushd의 UNC 경로 자동 매핑은 popd로 스택에서 빠져나올 때 자동으로 해제되는 임시적 부수 기능인 반면, subst는 로컬 경로를 대상으로 사용자가 명시적으로 만들고 명시적으로(`/d`) 해제해야 하는 독립적인 명령이다. 대상도 다르다 — pushd는 주로 네트워크 UNC 경로를 다루고, subst는 로컬 디스크의 긴 경로를 짧게 줄이는 데 주로 쓰인다.

## 다음 장에서는

다음은 52장 — 손상된 디스크에서 읽을 수 있는 데이터만 복구하는 `recover` 명령을 다룬다.

## 평가 기준

- subst로 로컬 경로를 가상 드라이브 문자에 연결하고 `/d`로 해제할 수 있다.
- subst 드라이브에서 chkdsk·format·label 등이 동작하지 않는 이유를 설명할 수 있다.
- subst 연결이 세션 한정이며 재부팅하면 사라진다는 것을 안다.
- subst와 pushd의 UNC 자동 매핑이 서로 다른 용도의 기능이라는 것을 설명할 수 있다.

## 참고

- [subst | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/subst)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
