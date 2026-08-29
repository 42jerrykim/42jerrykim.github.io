---
draft: false
slug: vol-command-display-volume-label-windows-cmd
title: "[CMD] 50. vol - 볼륨 레이블과 일련번호 표시"
description: "vol로 드라이브의 볼륨 레이블과 일련번호를 조회하는 법과 49장 label과의 역할 분담(조회 전용 vs 변경), 배치 스크립트에서 디스크를 식별하는 용도로 일련번호를 쓰는 법을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 500
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
- vol
- 볼륨정보
- File-System
- Documentation(문서화)
- Best-Practices
- Education(교육)
- CLI
- Comparison(비교)
- Batch
- Automation(자동화)
- Configuration(설정)
- Troubleshooting(트러블슈팅)
- Advanced
- Administration
- Productivity(생산성)
image: "wordcloud.png"
---

vol은 지정한 드라이브의 볼륨 레이블과 볼륨 일련번호를 표시하는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [49장: label](/post/cmd/label-command-volume-label-windows-cmd/)에서 레이블을 만들고 바꾸는 법을 다룬 뒤 이어진다. label이 "쓰기"였다면 vol은 "읽기 전용"이다 — 이 둘의 역할 분담이 이 장의 핵심이다.

**이 장의 깊이**: 입문. 옵션이 없어 짧다.

## 사용법

```
vol [<드라이브>:]
```

드라이브를 생략하면 현재 드라이브의 정보를 표시한다.

## 옵션

`/?` 외에 별도 옵션은 없다.

## 예시

```
vol
vol C:
vol D:
```

## 주의사항·함정

**레이블을 바꾸려면 vol이 아니라 label을 써야 한다**: vol은 순수 조회 명령이라 값을 바꾸는 옵션 자체가 없다. 볼륨 이름을 바꾸고 싶다면 49장에서 다룬 label로 넘어가야 한다.

**일련번호는 레이블과 다른 정보다**: vol이 함께 보여주는 볼륨 일련번호는 사람이 지정하는 레이블과 달리, 볼륨을 포맷할 때 시스템이 자동으로 생성하는 고유 값이다. 레이블은 label로 언제든 바꿀 수 있지만, 일련번호는 45장(format)에서 다시 포맷하지 않는 한 바뀌지 않는다 — 그래서 배치 스크립트에서 "이 디스크가 맞는 디스크인가"를 사람이 바꿀 수 있는 레이블보다 더 신뢰성 있게 식별할 때 일련번호를 참조하기도 한다.

**읽기 전용·네트워크 드라이브에서도 정보는 표시된다**: vol은 값을 바꾸지 않고 조회만 하므로, 쓰기 권한이 없는 드라이브나 네트워크로 연결된 드라이브에서도 문제없이 동작한다.

**PowerShell 대응 cmdlet은 `Get-Volume`이다**: vol이 레이블과 일련번호만 보여주는 것과 달리, `Get-Volume`은 파일 시스템 종류·상태·전체 및 여유 용량까지 한 번에 반환해 vol의 단순 텍스트 출력보다 훨씬 풍부한 정보를 준다. 다만 vol이 표시하는 볼륨 일련번호는 `Get-Volume`의 기본 출력에는 나타나지 않으므로, 일련번호가 필요하면 `Get-Partition`이나 `Get-CimInstance Win32_LogicalDisk`의 `VolumeSerialNumber` 속성을 별도로 조회해야 한다.

## 흔한 오개념

<strong>"vol과 label은 볼륨 레이블을 다루는 같은 명령이라 서로 바꿔 써도 된다"</strong>는 오해가 있다. vol은 49장에서 다룬 label과 달리 레이블을 조회만 하는 읽기 전용 명령으로, 값을 바꾸거나 지우는 옵션이 아예 없다. 레이블을 실제로 만들거나 바꾸거나 삭제하려면 vol이 아니라 label을 써야 하며, vol을 아무리 반복 실행해도 볼륨의 이름표는 바뀌지 않는다.

## 다음 장에서는

다음은 51장 — 로컬 경로를 가상 드라이브 문자에 연결하는 `subst` 명령을 다룬다.

## 평가 기준

- vol로 볼륨 레이블과 일련번호를 조회할 수 있다.
- vol(조회 전용)과 label(변경 가능)의 역할 분담을 설명할 수 있다.
- 볼륨 레이블과 일련번호가 서로 다른 성격의 정보(사람이 바꾸는 이름 vs 포맷 시 자동 생성되는 고유값)라는 것을 설명할 수 있다.

## 참고

- [vol | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/vol)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
