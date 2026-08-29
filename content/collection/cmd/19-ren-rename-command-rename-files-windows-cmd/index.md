---
draft: false
slug: ren-rename-command-rename-files-windows-cmd
title: "[CMD] 19. ren, rename - 파일·디렉터리 이름 변경"
description: "ren(rename)으로 파일·디렉터리 이름을 바꾸는 법과 새 드라이브·경로를 지정할 수 없는 제약, 와일드카드로 여러 파일을 한 번에 일괄 변경하는 문자 대응 규칙을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 190
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
- ren
- rename
- 이름변경
- File-System
- Wildcard
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Troubleshooting(트러블슈팅)
- Comparison(비교)
- Education(교육)
- Batch
- CLI
- Configuration(설정)
- Advanced
image: "wordcloud.png"
---

ren(또는 rename)은 파일이나 디렉터리의 이름을 바꾸는 내장 명령이다. 이동은 지원하지 않고 이름 변경만 담당한다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [18장: del, erase](/post/cmd/del-erase-command-delete-files-windows-cmd/)에서 파일을 삭제하는 법을 다룬 뒤 이어진다. 17장(move)에서 예고했던 "이동 없이 이름만 바꾸는 전용 명령"이 바로 이 장의 ren이다.

**이 장의 깊이**: 입문. **다루지 않는 것**: 다른 위치로 옮기면서 이름도 바꾸는 것은 17장(move)에서 이미 다뤘다.

## 사용법

```
ren [<드라이브>:][<경로>]<원본이름> <새이름>
rename [<드라이브>:][<경로>]<원본이름> <새이름>
```

## 옵션

별도 옵션 없이 원본 이름과 새 이름만 지정한다. 원본 이름에는 와일드카드(`*`, `?`)를 쓸 수 있다.

## 예시

```
ren report.txt report_2026.txt
ren *.txt *.doc
ren chap10 part10
rename "Old Folder" "New Folder"
```

두 번째 예시(`ren *.txt *.doc`)처럼 원본·새 이름 양쪽에 와일드카드를 함께 쓰면, 원본 이름에서 와일드카드가 매칭한 부분이 새 이름의 같은 위치에 그대로 대응되어 여러 파일의 확장자를 한 번에 일괄 변경할 수 있다.

## 주의사항·함정

**새 드라이브나 경로를 지정할 수 없다**: ren의 가장 중요한 제약이다.

> "You can't specify a new drive or path when renaming files. You also can't use this command to rename files across drives or to move files to a different directory." — Microsoft Learn, "ren"

새 이름에 경로를 포함해봐야 무시되거나 오류가 나며, 이동까지 하려는 시도는 항상 실패한다. 이동이 필요하다면 17장에서 다룬 move를 써야 한다.

**대상 이름이 이미 있으면 오류**: 새 이름이 같은 디렉터리의 기존 파일명과 겹치면 다음 메시지와 함께 실패한다.

> "Duplicate file name or file not found" — Microsoft Learn, "ren"

이 메시지는 "새 이름이 이미 존재한다"와 "원본 파일을 찾지 못했다"는 두 경우를 구분 없이 알려주므로, 어느 쪽이 원인인지는 09장(dir)에서 배운 `dir`로 직접 확인해야 한다.

**PowerShell의 `Rename-Item`은 와일드카드 일괄 변경을 직접 지원하지 않는다**: PowerShell에서 ren에 대응하는 명령은 `Rename-Item`이지만, `ren *.txt *.doc`처럼 원본·새 이름 양쪽에 와일드카드를 써서 여러 파일의 확장자를 한 번에 바꾸는 방식은 그대로 통하지 않는다. `Rename-Item`은 한 번에 하나의 항목만 이름을 바꾸도록 설계되어 있어, 같은 작업을 하려면 `Get-ChildItem *.txt | Rename-Item -NewName { $_.Name -replace '\.txt$','.doc' }`처럼 `Get-ChildItem`으로 대상을 먼저 나열한 뒤 파이프로 넘겨야 한다. CMD 스크립트를 PowerShell로 옮기면서 이 차이를 놓치면 와일드카드 이름 변경 줄이 조용히 실패하거나 첫 번째 파일에만 적용되는 문제가 생길 수 있다.

## 흔한 오개념

<strong>"ren \*.txt \*.doc는 파일 내용까지 바꿔준다"</strong>는 오해가 있다. ren은 이름(확장자 포함)만 바꿀 뿐 파일의 실제 내용이나 형식은 전혀 건드리지 않는다. 텍스트 파일의 확장자를 `.doc`로 바꾼다고 워드 문서가 되는 것이 아니듯, 확장자 변경은 파일 시스템에 붙은 이름표를 바꾸는 것에 불과하다.

## 다음 장에서는

다음은 20장 — 텍스트 파일의 내용을 화면에 그대로 출력하는 `type` 명령을 다룬다.

## 평가 기준

- ren으로 파일·디렉터리 이름을 바꾸고, 와일드카드로 여러 파일을 일괄 변경할 수 있다.
- ren이 새 드라이브·경로를 지정할 수 없다는 제약과, 이동이 필요하면 move를 써야 하는 이유를 설명할 수 있다.
- 이름 변경이 파일 내용이나 형식에는 영향을 주지 않는다는 것을 안다.

## 참고

- [ren | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/ren)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
