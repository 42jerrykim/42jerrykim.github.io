---
draft: false
slug: comp-command-compare-files-byte-windows-cmd
title: "[CMD] 22. comp - 파일 바이트 단위 비교"
description: "comp로 두 파일 또는 두 파일 집합을 바이트 단위로 비교하는 법과 파일 크기가 다르면 비교 자체를 거부하는 기본 동작, /n으로 강제 비교하는 법을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 220
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
- comp
- 파일비교
- File-System
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Troubleshooting(트러블슈팅)
- Comparison(비교)
- Education(교육)
- Batch
- CLI
- QA
- Legacy
- Configuration(설정)
- Advanced
image: "wordcloud.png"
---

comp는 두 파일 또는 두 파일 집합의 내용을 바이트 단위로 비교하는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [21장: attrib](/post/cmd/attrib-command-file-attributes-windows-cmd/)에서 파일 속성을 다룬 뒤 이어진다. attrib가 메타데이터를 다뤘다면, comp와 다음 장(fc)은 파일 내용 자체를 비교하는 두 갈래 명령이다.

**이 장의 깊이**: 입문. **다루지 않는 것**: 줄 단위 비교와 더 다양한 비교 모드는 23장(fc)에서 다룬다. comp는 순수한 바이트 단위 비교에 범위를 한정한다.

## 사용법

```
comp [<데이터1>] [<데이터2>] [/d] [/a] [/l] [/n=<숫자>] [/c]
```

인수 없이 `comp`만 실행하면 비교할 파일을 대화형으로 물어본다.

## 옵션

| 옵션 | 설명 |
|---|---|
| `/d` | 차이를 10진수로 표시(기본은 16진수) |
| `/a` | 차이를 ASCII 문자로 표시 |
| `/l` | 바이트 오프셋 대신 차이가 발생한 줄 번호 표시 |
| `/n=<숫자>` | 파일 크기가 달라도 지정한 줄 수까지만 강제로 비교 |
| `/c` | 대소문자 구분 없이 비교 |

## 예시

```
comp file1.txt file2.txt
comp c:\reports \\sales\backup\april
comp \invoice\*.txt \invoice\backup\*.txt /n=10 /d
comp /a /l a.txt b.txt
```

## 주의사항·함정

**파일 크기가 다르면 기본적으로 비교를 거부한다**: comp는 두 파일의 크기가 다르면 곧바로 다음과 같이 묻는다.

> "Files are different sizes / Compare more files (Y/N)?" — Microsoft Learn, "comp"

이 상태에서 그냥 진행하면 사실상 비교가 무의미해지므로, Microsoft Learn은 `/n`으로 비교할 줄 수를 명시해 파일의 앞부분만 의도적으로 비교하라고 안내한다. 크기가 다른 두 로그 파일에서 "앞부분 100줄까지는 같은가"를 확인하고 싶을 때 이 옵션이 유용하다.

**10번 다르면 비교를 중단한다**: comp는 불일치가 10번 발견되면 더 비교하지 않고 멈춘다.

> "10 Mismatches - ending compare" — Microsoft Learn, "comp"

완전히 다른 두 파일을 비교하면 전체 차이를 다 보여주지 않고 일찍 끝난다는 뜻이다. 파일 전체의 차이를 낱낱이 확인해야 한다면 comp보다 23장에서 다룰 fc가 더 적합하다.

**같은 이름의 파일도 다른 위치에 있으면 비교할 수 있다**: `<데이터1>`과 `<데이터2>`에 드라이브나 디렉터리만 지정하면, comp는 그 안의 파일들을 서로 대응시켜 비교한다.

**PowerShell의 `Compare-Object`는 comp를 그대로 대체하지 않는다**: `Compare-Object`는 이름은 비슷해 보여도 근본적으로 컬렉션·객체 비교 도구다. `Get-Content`로 읽은 줄 배열을 서로 비교하는 텍스트 diff 용도로는 자주 쓰이지만, comp처럼 두 파일을 바이트 단위로 비교하는 기능은 아니다. 이미지나 실행 파일 같은 바이너리가 정확히 동일한지 확인하려면 `Compare-Object`만으로는 부족하고, 각 파일의 `Get-FileHash` 결과를 비교하거나 `[System.IO.File]::ReadAllBytes()`로 바이트 배열을 직접 읽어 비교해야 comp와 동등한 결과를 얻을 수 있다.

## 흔한 오개념

<strong>"comp는 fc의 하위 호환 버전이라 실무에서 쓸 이유가 없다"</strong>는 오해가 있다. comp는 순수한 바이트 단위 비교에 특화되어 있어, 텍스트가 아닌 바이너리 파일(이미지, 실행 파일 등)이 정확히 동일한지만 빠르게 확인하고 싶을 때는 오히려 comp의 단순함이 fc의 재동기화 로직보다 예측하기 쉬운 결과를 준다. 줄 단위 차이를 자세히 보고 싶다면 fc, 바이트 단위로 "같다/다르다"만 빠르게 확인하고 싶다면 comp라는 용도 차이로 구분하는 편이 정확하다.

## 다음 장에서는

다음은 23장 — 텍스트·바이너리 양쪽 모드를 지원하고 줄 단위 차이까지 보여주는 `fc` 명령을 다룬다.

## 평가 기준

- comp로 두 파일 또는 두 파일 집합을 바이트 단위로 비교할 수 있다.
- 파일 크기가 다를 때 comp의 기본 동작과, `/n`으로 강제 비교하는 방법을 설명할 수 있다.
- comp가 10번째 불일치에서 비교를 중단한다는 것을 안다.
- comp와 fc의 용도 차이(바이트 단위 단순 비교 vs 줄 단위 상세 비교)를 설명할 수 있다.

## 참고

- [comp | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/comp)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
