---
draft: false
slug: pushd-popd-command-directory-stack-windows-cmd
title: "[CMD] 11. pushd, popd - 디렉터리 스택"
description: "pushd로 현재 디렉터리를 스택에 저장하고 다른 경로로 이동한 뒤 popd로 되돌아가는 법과, 네트워크 UNC 경로를 임시 드라이브 문자에 자동으로 연결하는 CMD 고유 동작을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 110
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
- pushd
- popd
- 디렉터리스택
- File-System
- UNC
- Networking(네트워킹)
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Comparison(비교)
- Command-Extensions
- Linux(리눅스)
- Education(교육)
- Batch
- CLI
image: "wordcloud.png"
---

pushd와 popd는 현재 디렉터리를 스택에 저장했다가 나중에 복원하는 한 쌍의 내장 명령이다. pushd는 현재 경로를 스택에 넣고 지정한 경로로 이동하며, popd는 스택 맨 위에서 경로를 꺼내 그곳으로 되돌아간다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [10장: tree](/post/cmd/tree-command-directory-structure-windows-cmd/)에서 디렉터리 구조를 시각화하는 법을 다룬 뒤 이어지며, Part 1(CMD 기초와 탐색)의 마지막 장이다. 08장(cd)이 단순히 위치를 옮기는 명령이었다면, pushd·popd는 "어디서 왔는지"를 기억했다가 되돌아가는 기능을 더한다.

**이 장의 깊이**: 입문–중급. **다루지 않는 것**: 스택 관리는 대화형·배치 양쪽에서 쓰이지만, 배치 파일 안에서 변수 유효범위를 제한하는 setlocal/endlocal과의 상호작용은 40장에서 다시 다룬다.

## 개요 + 정신 모델

pushd·popd는 후입선출(LIFO) 스택 하나를 CMD 세션이 유지한다는 정신 모델로 이해하면 된다. Microsoft Learn은 이 스택의 동작을 다음과 같이 설명한다.

> "The directories are stored sequentially in a virtual stack, so if you use the **pushd** command once, the directory in which you use the command is placed at the bottom of the stack. If you use the command again, the second directory is placed on top of the first one." — Microsoft Learn, "pushd"

즉 `pushd`를 여러 번 실행할수록 스택이 쌓이고, `popd`를 실행할 때마다 가장 최근에 쌓인 항목부터 하나씩 꺼내 그 디렉터리로 돌아간다. 04장(prompt)에서 다룬 `$+` 메타 문자를 프롬프트에 넣어두면 지금 스택이 몇 단계 쌓여 있는지 항상 확인할 수 있다.

## 사용법

```
pushd [<경로>]
popd
```

## 옵션

| 사용 | 설명 |
|---|---|
| `pushd <경로>` | 현재 디렉터리를 스택에 저장하고 지정한 경로로 이동. 상대 경로 지원 |
| `pushd`(경로 없이) | 인수 없이 쓸 수 없음 — 반드시 이동할 경로가 필요 |
| `popd` | 스택 맨 위 항목을 꺼내 그 디렉터리로 이동하고 스택에서 제거 |

## 예시

```
pushd C:\Projects
popd

pushd C:\A
pushd C:\B
pushd C:\C
popd
popd
popd
```

```
pushd \\server\share
dir
popd
```

## 주의사항·함정

**네트워크 경로는 임시 드라이브 문자로 자동 매핑된다**: pushd만의 독특한 동작이다. 명령 확장이 켜져 있으면(01장 참고) pushd에 UNC 경로(`\\서버\공유`)를 주었을 때, 사용하지 않는 가장 높은 드라이브 문자(Z:부터 역순으로)를 그 네트워크 자원에 임시로 할당한 뒤 그 드라이브로 이동한다.

> "If you specify a network path, the **pushd** command temporarily assigns the highest unused drive letter (starting with Z:) to the specified network resource. ... If you use the **popd** command with command extensions enabled, the **popd** command removes the drive-letter assignment created by **pushd**." — Microsoft Learn, "pushd"

이 드라이브 할당은 popd로 되돌아갈 때 자동으로 해제된다. 즉 pushd로 만든 임시 드라이브 문자를 다른 목적으로 계속 쓰려는 계획이라면 popd를 실행하는 순간 그 드라이브 문자 자체가 사라진다는 점을 미리 알아야 한다.

**반드시 쌍으로 맞춰야 한다**: popd를 pushd보다 많이 실행하면 스택이 비어 오류가 난다. 배치 파일에서 조건 분기에 따라 pushd 실행 여부가 갈리는 구조라면, 모든 경로에서 popd 호출 수가 pushd 호출 수와 일치하는지 반드시 검토해야 한다.

**setlocal과 함께 쓰면 스택도 자동 정리된다**: 40장(setlocal, endlocal)에서 다루는 환경 변수 범위 제한 블록 안에서 pushd를 실행하면, `endlocal`을 만났을 때(또는 배치 파일이 끝날 때) 그 블록 안에서 쌓인 pushd 스택도 함께 정리된다. popd 호출을 깜빡 잊더라도 setlocal 블록을 벗어나면 디렉터리 상태가 어긋난 채로 남지 않는다는 뜻이므로, 여러 단계로 디렉터리를 옮기는 배치 파일은 setlocal 블록 안에서 pushd를 쓰는 편이 안전하다.

**PowerShell도 네이티브 `Push-Location`/`Pop-Location`을 가지고 있다**: PowerShell에는 pushd·popd에 대응하는 `Push-Location`/`Pop-Location`이 있고, PowerShell 자체가 `pushd`·`popd`라는 별칭까지 미리 지정해 두어 명령 이름을 그대로 입력해도 동작한다. 다만 동작 방식에는 차이가 있다 — CMD의 pushd는 명령 확장이 켜져 있을 때 UNC 네트워크 경로(`\\server\share`)를 사용하지 않는 드라이브 문자(Z:부터 역순)에 임시로 매핑해야만 그 경로로 이동할 수 있지만, PowerShell의 Push-Location(및 Set-Location)은 UNC 경로를 별도 드라이브 매핑 없이 직접 탐색할 수 있어 이 드라이브 문자 우회가 애초에 필요 없다.

## 흔한 오개념

<strong>"pushd·popd는 cd와 완전히 같은 명령이다"</strong>는 오해가 있다. cd는 "어디로 갈지"만 다루고 이전 위치를 기억하지 않지만, pushd·popd는 이동 이력을 스택으로 관리한다는 점이 본질적으로 다르다. 유닉스 Bash에도 같은 이름의 `pushd`/`popd`가 있지만, Bash는 UNC 경로 개념이 없으므로 네트워크 경로를 임시 드라이브 문자에 매핑하는 이 장의 동작은 CMD 고유의 기능이다.

## 다음 장에서는

다음은 12장 — 지금까지 Part 1에서 탐색해온 디렉터리를 실제로 만드는 `md`(`mkdir`) 명령으로 Part 2(파일과 디렉터리 조작)가 시작된다.

## 평가 기준

- pushd로 디렉터리를 스택에 저장하고 popd로 되돌아가는 흐름을 설명하고 재현할 수 있다.
- 명령 확장이 켜져 있을 때 pushd가 UNC 경로를 임시 드라이브 문자에 매핑하고, popd가 그 할당을 해제한다는 것을 설명할 수 있다.
- pushd·popd 호출 수를 맞추지 않으면 어떤 오류가 나는지, setlocal 블록과 함께 쓰면 왜 더 안전한지 설명할 수 있다.
- pushd·popd와 cd의 근본적인 차이(이동 이력의 스택 관리 여부)를 설명할 수 있다.

## 참고

- [pushd | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/pushd)
- [popd | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/popd)
