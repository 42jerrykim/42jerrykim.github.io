---
draft: false
slug: move-command-move-files-directories-windows-cmd
title: "[CMD] 17. move - 파일·디렉터리 이동과 이름 변경"
description: "move로 파일과 디렉터리를 이동하는 법과, 같은 드라이브 내 이동은 메타데이터만 바뀌는 즉시 처리인 반면 다른 드라이브 간 이동은 내부적으로 복사 후 삭제로 처리된다는 성능 차이를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 170
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
- move
- 파일이동
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
- Administration
image: "wordcloud.png"
---

move는 파일이나 디렉터리를 다른 위치로 옮기거나, 같은 디렉터리 안에서 이름을 바꾸는 내장 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [16장: robocopy](/post/cmd/robocopy-command-mirror-copy-files-windows/)에서 복사 계열 명령을 마친 뒤 이어진다. 복사와 이동의 차이 — 원본이 남는지 사라지는지 — 가 이 장의 출발점이다.

**이 장의 깊이**: 입문–중급. **다루지 않는 것**: 이동 없이 이름만 바꾸는 전용 명령은 19장(ren)에서 다룬다. move도 같은 디렉터리 내 이름 변경을 지원하지만, 두 명령의 관계는 이 장의 "흔한 오개념"에서 정리한다.

## 사용법

```
move [{/y|/-y}] [<원본>] [<대상>]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `/y` | 덮어쓸 때 확인 메시지 없이 진행(`COPYCMD` 환경 변수에 미리 설정 가능) |
| `/-y` | 덮어쓸 때 항상 확인 메시지 표시 |

디렉터리를 이동하거나 이름을 바꿀 때는 원본에 현재 디렉터리 경로와 이름을, 대상에 원하는 경로와 이름을 그대로 지정한다.

## 예시

```
move report.txt D:\Backup\
move \data\*.xls \second_q\reports\
move oldname.txt newname.txt
move C:\Data\*.log C:\Logs\
move C:\OldFolderName C:\NewFolderName
```

마지막 줄처럼 move에 디렉터리를 지정하면 디렉터리 자체를 이동하거나(다른 경로를 대상으로 지정) 이름을 바꿀 수 있다(같은 위치에서 새 이름을 대상으로 지정).

## 주의사항·함정

**같은 드라이브 안에서는 메타데이터만 바뀐다**: NTFS 같은 파일 시스템에서 같은 드라이브 내 이동은 파일 내용을 실제로 복사하지 않고, 파일이 어느 디렉터리에 속하는지를 가리키는 디렉터리 항목(메타데이터)만 바꾼다. 그래서 대용량 파일이라도 같은 드라이브 안에서는 이동이 거의 즉시 끝난다.

**다른 드라이브 간 이동은 복사 후 삭제로 처리된다**: 반면 서로 다른 드라이브(예: C: → D:) 사이의 이동은 파일 시스템이 물리적으로 분리되어 있어 메타데이터만 바꿀 방법이 없다. 이 경우 move는 내부적으로 대상에 전체 복사를 수행한 뒤 원본을 삭제하는 방식으로 동작한다. 대용량 파일을 다른 드라이브로 옮길 때 예상보다 오래 걸린다면 이 차이 때문이다 — 진행 중 전원이 꺼지거나 스크립트가 중단되면 원본과 사본이 동시에 존재하거나, 최악의 경우 둘 다 온전하지 않은 상태로 남을 수 있어 중요한 파일은 복사 완료를 확인한 뒤 원본을 지우는 방식(예: robocopy `/mov`처럼 검증이 포함된 도구)을 고려할 만하다.

**암호화된 파일을 EFS 미지원 볼륨으로 옮기면 오류**: Microsoft Learn은 암호화 파일 시스템(EFS)을 지원하지 않는 볼륨으로 암호화된 파일을 이동하면 오류가 난다고 명시한다. 이 경우 먼저 복호화하거나 EFS를 지원하는 볼륨으로 옮겨야 한다.

**PowerShell의 대응 명령은 `Move-Item`이다**: 파일·디렉터리를 옮기고 이름을 바꾸는 기본 동작은 move와 동일하게 지원하며, 같은 드라이브 내 이동과 다른 드라이브 간 이동의 내부 동작 차이(메타데이터만 변경 vs 복사 후 삭제)도 그대로 이어받는다.

## 흔한 오개념

<strong>"move로 이름을 바꾸는 것과 ren으로 이름을 바꾸는 것은 완전히 같다"</strong>는 오해가 있다. 같은 디렉터리 안에서 이름만 바꾸는 결과는 동일하지만, move는 대상에 다른 경로를 지정해 이동까지 함께 처리할 수 있는 반면 19장에서 다룰 ren은 애초에 경로 지정을 허용하지 않아 이름 변경 전용으로 범위가 좁다. "이동도 하고 이름도 바꾸고 싶다"면 move 하나로 충분하지만, "실수로 다른 위치로 옮겨질 걱정 없이 이름만 바꾸고 싶다"면 ren이 더 안전한 선택일 수 있다.

## 다음 장에서는

다음은 18장 — move·copy와 달리 파일을 완전히 없애는 `del`(`erase`) 명령을 다룬다.

## 평가 기준

- move로 파일·디렉터리를 이동하고 이름을 바꿀 수 있다.
- 같은 드라이브 내 이동과 다른 드라이브 간 이동의 내부 동작 차이(메타데이터 변경 vs 복사 후 삭제)를 설명할 수 있다.
- 다른 드라이브로 대용량 파일을 옮길 때 왜 시간이 더 걸리고, 중단 시 어떤 위험이 있는지 설명할 수 있다.
- move와 ren의 범위 차이를 설명할 수 있다.

## 참고

- [move | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/move)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
