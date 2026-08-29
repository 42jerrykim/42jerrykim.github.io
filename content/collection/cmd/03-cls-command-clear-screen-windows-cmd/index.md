---
draft: false
slug: cls-command-clear-screen-windows-cmd
title: "[CMD] 03. cls - 화면 지우기"
description: "cls 명령으로 CMD 창의 화면을 지우는 방법과, 화면 버퍼·스크롤 기록·명령 히스토리는 지워지지 않는다는 점, 배치 파일에서 cls를 쓰는 관례를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 30
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
- cls
- 화면지우기
- Console
- Batch
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Comparison(비교)
- Productivity(생산성)
- Configuration(설정)
- Workflow(워크플로우)
- Troubleshooting(트러블슈팅)
- Education(교육)
- Tutorial(튜토리얼)
- CLI
image: "wordcloud.png"
---

cls는 CMD 창에 표시된 내용을 전부 지우고 빈 화면으로 되돌리는 내장 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [02장: help](/post/cmd/help-command-list-command-help-windows-cmd/)에서 도움말을 조회하는 법을 다룬 뒤 이어진다. cls는 Part 1에서 가장 단순한 명령이므로, 이 장을 발판 삼아 "옵션이 거의 없는 명령"의 최소 문서 구조를 확인하고 다음 장(04장: prompt)의 조금 더 복잡한 옵션 체계로 넘어간다.

**이 장의 깊이**: 입문. 옵션이 사실상 없어 매우 짧다. **다루지 않는 것**: 화면을 정리하는 다른 방법(콘솔 버퍼 크기 조정 등)은 다루지 않는다.

## 사용법

```
cls
```

## 옵션

이 명령은 `/?`를 제외하면 별도 옵션이 없다.

| 옵션 | 설명 |
|---|---|
| `/?` | 명령 프롬프트에서 도움말 표시 |

## 예시

```
cls
```

배치 파일에서 여러 단계를 거치는 메뉴나 진행 상황을 보여주기 전에 화면을 비울 때 자주 쓴다.

```bat
@echo off
:menu
cls
echo 1. 시작
echo 2. 종료
choice /c 12
```

## 주의사항·함정

**지워지는 것은 화면뿐이다**: cls는 현재 화면에 표시된 내용만 지운다. Windows Terminal이나 일부 콘솔 호스트 설정에 따라 스크롤을 올려 이전 출력을 다시 볼 수 있는 경우가 있고, 명령 히스토리(위/아래 화살표로 불러오는 과거 입력)는 06장(doskey)에서 다루는 별도의 버퍼이므로 cls로 지워지지 않는다.

**유닉스 `clear`와 이름은 다르지만 역할은 같다**: PowerShell에도 `cls`라는 별칭이 있어(`Clear-Host`를 가리킴) 명령 자체는 그대로 통하지만, 이는 우연히 같은 이름을 쓸 뿐 서로 다른 구현이다. CMD의 `cls`를 PowerShell 스크립트 안에서 그대로 재사용해도 문제는 없지만, 이는 PowerShell이 하위 호환을 위해 별칭을 제공하기 때문이지 CMD 명령이 PowerShell에서 직접 동작하기 때문이 아니다.

## 흔한 오개념

<strong>"cls를 실행하면 화면에 표시됐던 민감한 정보가 완전히 사라진다"</strong>는 오해가 있다. 예를 들어 실수로 비밀번호를 평문으로 입력해 화면에 노출됐을 때 cls로 지웠다고 안심하기 쉽지만, 위 주의사항에서 다뤘듯 스크롤을 올리면 이전 출력이 그대로 다시 보일 수 있다. 화면 뒤에 있는 사람이 스크롤만 올려도 방금 지운 내용을 볼 수 있다는 뜻이므로, 민감한 정보를 다루는 세션이라면 cls에 의존하지 말고 애초에 화면에 그런 정보를 띄우지 않는 편이 안전하다.

## 다음 장에서는

다음은 04장 — 프롬프트에 표시되는 문자열 형식을 바꾸는 `prompt` 명령을 다룬다.

## 평가 기준

- cls가 화면 버퍼만 지우고 명령 히스토리는 지우지 않는다는 것을 설명할 수 있다.
- 배치 파일에서 cls를 반복 메뉴 출력 앞에 두는 관례적 용법을 이해한다.

## 참고

- [cls | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cls)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
