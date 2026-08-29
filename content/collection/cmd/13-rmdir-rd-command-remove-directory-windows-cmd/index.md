---
draft: false
slug: rmdir-rd-command-remove-directory-windows-cmd
title: "[CMD] 13. rmdir, rd - 디렉터리 삭제"
description: "rmdir(rd)로 빈 디렉터리를 지우는 법과 /s로 하위 파일까지 통째로 지우는 법, 숨김·시스템 파일이 있으면 삭제가 막히는 이유, 현재 디렉터리는 지울 수 없는 제약을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 130
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
- rmdir
- rd
- 디렉터리삭제
- File-System
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Troubleshooting(트러블슈팅)
- Comparison(비교)
- Linux(리눅스)
- Education(교육)
- Batch
- CLI
- Configuration(설정)
- Advanced
image: "wordcloud.png"
---

rmdir(또는 rd)는 디렉터리를 삭제하는 내장 명령이다. 기본적으로 빈 디렉터리만 지울 수 있다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [12장: md, mkdir](/post/cmd/md-mkdir-command-create-directory-windows-cmd/)에서 디렉터리를 만드는 법을 다룬 뒤 이어진다. 만드는 명령과 지우는 명령을 바로 짝지어 배치해, "생성-삭제" 대칭을 확인할 수 있게 했다.

**이 장의 깊이**: 입문–중급. **다루지 않는 것**: 디렉터리가 아니라 파일을 지우는 것은 18장(del)에서 다룬다.

## 사용법

```
rmdir [<드라이브>:]<경로> [/s [/q]]
rd [<드라이브>:]<경로> [/s [/q]]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `/s` | 지정한 디렉터리와 그 안의 모든 하위 디렉터리·파일을 통째로 삭제(디렉터리 트리 삭제) |
| `/q`(`/s`와 함께) | 조용한 모드. 디렉터리 트리 삭제 확인 메시지를 표시하지 않음 |

## 예시

```
cd ..
rmdir test
rmdir /s test
rmdir /s /q test
```

첫 번째 줄(`cd ..`)은 삭제 대상 디렉터리 밖으로 먼저 이동하는 관례다 — 아래 "주의사항·함정"에서 그 이유를 설명한다.

## 주의사항·함정

**현재 디렉터리는 지울 수 없다**: rmdir로 지금 있는 디렉터리 자체를 지우려 하면 오류가 난다.

> "You can't use the **rmdir** command to delete the current directory. If you attempt to delete the current directory, the following error message appears: 'The process can't access the file because it is being used by another process.'" — Microsoft Learn, "rmdir"

이 오류 메시지는 마치 다른 프로세스가 파일을 잠그고 있는 것처럼 보이지만, 실제 원인은 cmd.exe 프로세스 자신이 그 디렉터리를 현재 위치로 참조하고 있기 때문이다. 해결책은 예시에서 보인 것처럼 `cd ..`로 상위 디렉터리로 먼저 이동한 뒤 다시 시도하는 것이다.

**숨김·시스템 파일이 있으면 "디렉터리가 비어 있지 않습니다"로 막힌다**: rmdir(옵션 없이)는 숨김·시스템 파일을 포함해 파일이 하나라도 있으면 삭제를 거부한다.

> "You can't delete a directory that contains files, including hidden or system files. ... Use the **dir /a** command to list all files (including hidden and system files). Then use the **attrib** command with **-h** to remove hidden file attributes, **-s** to remove system file attributes, or **-h -s** to remove both." — Microsoft Learn, "rmdir"

09장(dir)의 `/a` 옵션으로 숨겨진 내용물을 먼저 확인하고, 21장(attrib)에서 다룰 `-h`/`-s`로 속성을 벗겨야 일반적인 `rmdir`로 지울 수 있다. 물론 실무에서는 아래의 `/s`를 쓰는 편이 더 빠르다.

**`/s /q`는 확인 없이 통째로 지운다**: `/s`는 하위 트리 전체를 지우고, `/q`는 그 삭제를 확인 없이 진행한다. 되돌릴 수 없는 조합이므로, 09장(dir)에서 다룬 것처럼 삭제 전에 같은 경로로 `dir /s`를 먼저 실행해 지워질 대상을 확인하는 습관이 중요하다.

**명령 확장이 꺼지면 `/s`의 출력이 달라진다**: 명령 확장이 꺼져 있으면 `/s`는 삭제되는 파일 이름이 아니라 찾지 못한 파일 이름을 표시하는 것으로 동작이 바뀐다. 스크립트가 rmdir 출력을 파싱한다면 이 차이로 예상과 다른 결과를 얻을 수 있다.

**심볼릭 링크·정션을 rmdir로 지우면 링크만 사라지고 대상은 그대로 남는다**: 24장(mklink)에서 다룰 `mklink /d`(심볼릭 링크)나 `mklink /j`(정션)로 만든 디렉터리를 대상으로 rmdir를 실행하면, 그 링크 항목 자체만 제거될 뿐 링크가 가리키던 실제 대상 디렉터리와 그 안의 내용물은 전혀 건드려지지 않는다. "폴더처럼 보이는 것을 지우면 안의 내용까지 다 지워진다"는 직관과 어긋나기 쉬운 지점이며, 같은 종류의 링크를 파일 탐색기에서 삭제할 때의 동작(대상까지 함께 삭제될 위험이 더 모호하게 남아 있는 경우)과 대비해서 기억해두면 실수를 줄일 수 있다.

**PowerShell의 대응 명령은 `Remove-Item -Recurse`다**: 대략 `rmdir /s`에 대응하며, 여기에 `-Confirm`(항목마다 확인)이나 `-WhatIf`(실제로 지우지 않고 무엇이 지워질지만 미리 보여줌)를 붙이면 CMD의 rmdir에는 없는 사전 점검 안전장치를 얻을 수 있다. `/s /q`처럼 되돌릴 수 없는 일괄 삭제가 걱정되는 상황이라면, `Remove-Item -Recurse -WhatIf`로 먼저 삭제 대상을 확인하는 습관이 rmdir보다 안전한 대안이 된다.

## 흔한 오개념

<strong>"rmdir로 지운 디렉터리도 휴지통(Recycle Bin)으로 이동해 나중에 복구할 수 있다"</strong>는 오해가 있다. 파일 탐색기에서 폴더를 Delete 키로 지우면 보통 휴지통을 거치지만, `rmdir`(과 `/s`)은 명령줄에서 파일 시스템 API를 직접 호출해 즉시 영구 삭제하며 휴지통을 전혀 거치지 않는다. `/s /q`로 확인 메시지까지 끈 상태에서 잘못된 경로를 지정하면 되돌릴 방법이 없다는 뜻이므로, 실행 전 대상 경로를 다시 한번 확인하는 습관이 중요하다.

## 다음 장에서는

다음은 14장 — 파일을 다른 위치로 복사하는 `copy` 명령을 다룬다.

## 평가 기준

- rmdir로 빈 디렉터리를 지우고, `/s`로 트리 전체를 지우는 차이를 설명할 수 있다.
- 현재 디렉터리를 지울 수 없는 이유와 `cd ..`로 먼저 빠져나와야 하는 이유를 설명할 수 있다.
- 숨김·시스템 파일이 있는 디렉터리를 지우려면 무엇을 먼저 해야 하는지 안다.
- `/s /q` 조합의 위험성과, 삭제 전 `dir /s`로 대상을 먼저 확인하는 습관의 중요성을 설명할 수 있다.

## 참고

- [rmdir | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/rmdir)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
