---
draft: false
slug: cd-chdir-command-change-directory-windows-cmd
title: "[CMD] 08. cd, chdir - 디렉터리 이동과 현재 위치"
description: "cd(chdir)로 현재 디렉터리를 표시·변경하는 법과 /d 스위치가 필요한 이유, 드라이브마다 별도로 기억되는 현재 디렉터리라는 CMD 고유의 동작 방식을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 80
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
- cd
- chdir
- 디렉터리이동
- File-System
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Troubleshooting(트러블슈팅)
- Comparison(비교)
- Command-Extensions
- Linux(리눅스)
- Education(교육)
- Productivity(생산성)
- Configuration(설정)
- CLI
image: "wordcloud.png"
---

cd(또는 chdir)는 현재 작업 디렉터리를 표시하거나 지정한 디렉터리로 이동하는 내장 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [07장: path](/post/cmd/path-command-executable-search-path-windows/)에서 실행 파일을 찾는 경로를 다룬 뒤 이어진다. path가 "명령을 어디서 찾는가"였다면, cd는 "지금 내가 어디에 있는가"를 다룬다 — 이 둘이 갖춰져야 09장(dir)에서 그 자리의 내용을 들여다볼 수 있다.

**이 장의 깊이**: 입문. **다루지 않는 것**: 디렉터리 자체를 만들고 지우는 것은 12장(md)·13장(rmdir)에서, 이전 위치로 돌아가는 스택 기반 이동은 11장(pushd, popd)에서 각각 다룬다.

## 사용법

```
cd [/d] [<드라이브>:][<경로>]
cd [..]
chdir [/d] [<드라이브>:][<경로>]
```

경로 없이 `cd`만 입력하면 현재 드라이브와 디렉터리를 표시한다 — 유닉스의 `pwd`에 해당하는 동작이 CMD에서는 별도 명령이 아니라 `cd`를 인수 없이 호출하는 것이다.

## 옵션

| 옵션 | 설명 |
|---|---|
| `/d` | 드라이브와 디렉터리를 동시에 변경 |
| `<드라이브>:` | 표시하거나 변경할 드라이브 지정(현재 드라이브와 다를 때) |
| `<경로>` | 이동할 디렉터리 경로 |
| `..` | 상위 폴더로 이동 |

## 예시

```
C:\Users> cd
C:\Users

C:\Users> cd \Windows\System32
C:\Windows\System32> cd ..
C:\Windows>

D:\> cd /d C:\Projects
C:\Projects>

D:\> cd C:\Projects
D:\>
D:\> cd C:
C:\Projects>
```

마지막 세 줄이 이 장에서 가장 중요한 예시다. `D:` 드라이브에 있는 상태에서 `/d` 없이 `cd C:\Projects`를 실행하면 화면상 아무 변화가 없어 보이지만, 실제로는 C: 드라이브가 "기억하는" 현재 디렉터리만 `C:\Projects`로 바뀌고 프롬프트는 여전히 `D:\`에 머문다. 그 상태에서 `cd C:`만 입력하면 그제서야 C: 드라이브로 전환되면서 방금 기억해둔 `C:\Projects`로 이동한 결과가 나타난다.

## 주의사항·함정

**드라이브별로 별도의 "현재 디렉터리"가 있다**: 이것이 CMD의 가장 잘 알려진 함정이다. Windows는 프로세스마다 드라이브 문자 각각에 대해 독립적인 현재 디렉터리를 유지한다. `/d` 없이 `cd <다른드라이브>:<경로>`를 실행하면 그 드라이브의 "기억된 현재 디렉터리"만 갱신될 뿐, 실제로 그 드라이브로 전환되지는 않는다. 드라이브 전환과 디렉터리 이동을 한 번에 하려면 반드시 `/d`를 써야 한다.

**공백이 포함된 경로**: 명령 확장이 켜져 있으면(01장 참고) `cd username\programs\start menu`처럼 공백이 있는 경로를 따옴표 없이 그대로 받아들인다.

> "Spaces aren't treated as delimiters, so `<path>` can contain spaces without enclosing quotation marks." — Microsoft Learn, "cd"

다만 명령 확장이 꺼져 있으면 이 동작이 사라지고 반드시 `cd "C:\Program Files"`처럼 따옴표로 감싸야 한다. 이식성을 고려한다면(명령 확장이 꺼진 환경까지 가정한다면) 공백이 있는 경로는 항상 따옴표로 감싸는 습관을 들이는 편이 안전하다.

**대소문자 정규화**: 명령 확장이 켜져 있으면 `cd c:\temp`처럼 입력해도 디스크에 저장된 실제 대소문자(`C:\Temp`)로 현재 디렉터리 문자열이 맞춰진다.

**PowerShell의 `Set-Location`은 파일 시스템을 넘어서는 공급자 모델을 쓴다**: PowerShell에서 cd에 대응하는 명령은 `Set-Location`(별칭 `cd`, `sl`)이다. CMD의 cd가 오직 파일 시스템 드라이브만 다루는 것과 달리, PowerShell의 Set-Location은 PSProvider라는 추상화 위에서 동작해 `Set-Location HKLM:\`처럼 레지스트리로, `Set-Location Env:\`처럼 환경 변수 목록으로도 "이동"할 수 있다. 다만 이 장에서 다룬 CMD 고유의 드라이브별 현재 디렉터리 기억 동작(`C:`만 입력했을 때 그 드라이브가 기억하던 위치로 돌아가는 것)은 PowerShell에 그대로 대응하는 개념이 없다.

## 흔한 오개념

<strong>"cd로 드라이브를 옮길 수 없다"</strong>는 오해가 흔하다. 정확히는 "경로만 주면" 드라이브가 안 바뀔 뿐이고, `/d` 스위치를 쓰거나 드라이브 문자만 단독으로 입력(`C:`)하면 드라이브 전환이 정상적으로 일어난다. 이 오해는 위에서 설명한 드라이브별 현재 디렉터리 기억 방식을 모를 때 생긴다.

## 다음 장에서는

다음은 09장 — 지금 있는 디렉터리 안의 파일·하위 디렉터리 목록을 보여주는 `dir` 명령을 다룬다.

## 평가 기준

- `cd`(인수 없음)로 현재 위치를 확인하고, `cd ..`로 상위 폴더로 이동할 수 있다.
- `/d` 스위치가 왜 필요한지, 드라이브별로 별도의 현재 디렉터리가 유지된다는 CMD의 동작 방식을 설명할 수 있다.
- 명령 확장이 켜졌을 때와 꺼졌을 때 공백 포함 경로를 다루는 방식이 어떻게 다른지 안다.
- 유닉스의 `pwd`에 해당하는 동작이 CMD에서는 `cd`를 인수 없이 호출하는 것이라는 대응 관계를 설명할 수 있다.

## 참고

- [cd | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cd)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
