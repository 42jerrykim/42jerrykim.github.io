---
draft: false
slug: tree-command-directory-structure-windows-cmd
title: "[CMD] 10. tree - 디렉터리 구조 트리 표시"
description: "tree 명령으로 드라이브나 경로의 디렉터리 구조를 그래픽 트리로 표시하는 법과 /f(파일 포함)·/a(ASCII 문자) 옵션, 깊이 제한이 없어 대형 트리에서 more와 파이프로 조합해야 하는 이유를 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 100
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
- tree
- 디렉터리구조
- File-System
- Visualization
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Comparison(비교)
- Linux(리눅스)
- Command-Line
- Education(교육)
- Productivity(생산성)
- Troubleshooting(트러블슈팅)
- CLI
- Configuration(설정)
image: "wordcloud.png"
---

tree는 지정한 드라이브 또는 경로의 디렉터리 구조를 계층적인 그림으로 표시하는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [09장: dir](/post/cmd/dir-command-list-files-directories-windows-cmd/)에서 한 디렉터리의 내용을 평면적으로 나열하는 법을 다룬 뒤 이어진다. dir이 "한 층"을 보여준다면 tree는 여러 층의 관계를 한 번에 시각화한다.

**이 장의 깊이**: 입문. 옵션이 두 개뿐이라 짧다.

## 사용법

```
tree [<드라이브>:][<경로>] [/f] [/a]
```

드라이브나 경로를 지정하지 않으면 현재 드라이브의 현재 디렉터리를 기준으로 트리를 그린다.

## 옵션

| 옵션 | 설명 |
|---|---|
| `/f` | 각 디렉터리 안의 파일 이름도 함께 표시 |
| `/a` | 확장 그래픽 문자 대신 ASCII 문자로 연결선을 표시(호환성용) |

## 예시

```
tree
tree \
tree C:\Projects
tree /f
tree c:\ /f | more
tree D:\Data /f /a
tree c:\ /f > C:\reports\tree.txt
```

`/a`는 콘솔 폰트나 원격 터미널이 확장 그래픽 문자(선 그리기 문자)를 제대로 표시하지 못할 때, 또는 출력을 다른 시스템으로 옮겨야 할 때 유용하다.

## 주의사항·함정

**깊이를 제한하는 옵션이 없다**: tree는 지정한 경로 이하 모든 하위 디렉터리를 예외 없이 그린다. 대형 프로젝트나 `node_modules`처럼 파일 수가 많은 디렉터리에서 `/f`까지 함께 쓰면 출력이 감당하기 어려울 만큼 길어질 수 있다. 특정 깊이까지만 보고 싶다면 tree 자체의 옵션으로는 불가능하고, 출력을 다른 도구로 가공해야 한다 — Microsoft Learn도 대형 출력을 `more`와 파이프로 연결하거나 파일로 리다이렉션하는 예시만 제시할 뿐, 깊이 제한 옵션은 애초에 제공하지 않는다.

**한 화면씩 보려면 파이프 조합이 필수**: `tree c:\ /f | more`처럼 3부에서 다룰 `more` 페이저와 조합하는 것이 사실상 유일한 화면 제어 수단이다. dir의 `/p`에 해당하는 자체 옵션이 tree에는 없다.

**숨김·시스템 파일·폴더는 기본적으로 보이지 않는다**: tree도 [09장(dir)](/post/cmd/dir-command-list-files-directories-windows-cmd/)과 마찬가지로 숨김 속성이나 시스템 속성이 붙은 디렉터리·파일을 기본 출력에서 제외한다. 그런데 dir은 `/a:h`처럼 속성을 지정해 숨김 항목을 강제로 표시할 수 있는 스위치가 있는 반면, tree에는 이에 대응하는 옵션이 전혀 없어 숨김 폴더를 트리에 포함시킬 CMD 네이티브 방법이 없다. 프로젝트 폴더에 숨김 속성이 붙은 디렉터리가 섞여 있다면 tree의 결과만 보고 전체 구조를 파악했다고 착각하지 않아야 한다.

**PowerShell에는 동일한 트리 그림을 만드는 내장 cmdlet이 없다**: PowerShell 자체에는 tree가 그리는 것과 같은 ASCII 트리 다이어그램을 출력하는 네이티브 cmdlet이 없다. `tree.exe`(또는 `tree.com`)는 외부 실행 파일이므로 PowerShell 세션에서도 그대로 호출할 수 있고, 이를 대신하려는 사람들은 `Get-ChildItem -Recurse`의 결과를 직접 들여쓰기 형식으로 가공하는 스크립트를 짜서 흉내 내는 경우가 많다. 즉 tree와 완전히 같은 출력을 내는 표준 cmdlet은 존재하지 않는다.

## 흔한 오개념

<strong>"tree를 실행하면 디렉터리의 전체 구조를 빠짐없이 볼 수 있다"</strong>는 오해가 있다. 앞서 살펴본 것처럼 tree는 숨김·시스템 속성이 붙은 폴더를 dir과 똑같이 기본에서 조용히 건너뛴다. 화면에 나온 트리가 완전하다고 믿고 숨김 폴더 안의 내용을 놓친 채 구조를 파악하면, 실제로는 존재하는 디렉터리를 못 본 채 판단하게 되는 셈이다.

## 다음 장에서는

다음은 11장 — 지금까지 다닌 디렉터리를 스택에 기록해두고 되돌아가는 `pushd`, `popd` 명령을 다룬다.

## 평가 기준

- `/f`와 `/a` 두 옵션의 차이를 설명하고 상황에 맞게 조합할 수 있다.
- tree에 깊이 제한 옵션이 없다는 것과, 대형 트리를 다룰 때 `more`나 리다이렉션과 조합해야 하는 이유를 설명할 수 있다.

## 참고

- [tree | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/tree)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
