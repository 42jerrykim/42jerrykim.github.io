---
draft: false
slug: recover-command-recover-damaged-disk-windows-cmd
title: "[CMD] 52. recover - 손상된 디스크에서 데이터 복구"
description: "recover로 배드 섹터가 있는 디스크에서 읽을 수 있는 데이터만 파일 단위로 복구하는 법과 손상된 섹터의 데이터는 영구히 잃는다는 제약, 한 번에 한 파일만 지정해야 하는 이유를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 520
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
- Advanced
- recover
- 데이터복구
- File-System
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Education(교육)
- CLI
- Data-Recovery
- Legacy
- Configuration(설정)
- Beginner
- Administration
- Productivity(생산성)
- Workflow(워크플로우)
image: "wordcloud.png"
---

recover는 불량이거나 결함이 있는 디스크에서 읽을 수 있는 정보를 복구하는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [51장: subst](/post/cmd/subst-command-virtual-drive-letter-windows-cmd/)에서 가상 드라이브 매핑을 다룬 뒤 이어진다. 42장(chkdsk)의 `/r`이 배드 섹터를 "찾아서 표시"하는 명령이었다면, recover는 그 이후 시점에 이미 손상이 확인된 개별 파일에서 "그나마 읽을 수 있는 부분만 살려내는" 명령이다.

**이 장의 깊이**: 입문–중급.

## 사용법

```
recover [<드라이브>:][<경로>]<파일이름>
```

와일드카드는 지원하지 않는다. 파일 이름을 정확히 하나만 지정해야 한다.

## 옵션

`/?` 외에 별도 옵션은 없다.

## 예시

```
recover d:\fiction\story.txt
```

## 주의사항·함정

**손상된 섹터의 데이터는 영구히 사라진다**: recover는 파일을 섹터 단위로 읽어 정상적인 섹터의 데이터만 복구하고, 손상된 섹터에 있던 내용은 복구하지 못한다.

> "This command reads a file, sector-by-sector, and recovers data from the good sectors. Data in bad sectors is lost." — Microsoft Learn, "recover"

즉 recover는 파일을 "완전히 되살리는" 도구가 아니라 "구할 수 있는 만큼만 건지는" 도구다. 결과물은 원본과 다를 수 있고, 손상된 부분은 빈 데이터나 예측 불가능한 값으로 채워질 수 있다.

**한 번에 하나의 파일만 지정해야 한다**: 와일드카드를 지원하지 않는 이유가 여기 있다.

> "Because all data in bad sectors is lost when you recover a file, you should recover only one file at a time." — Microsoft Learn, "recover"

여러 파일을 한꺼번에 처리하려는 배치 스크립트를 짜고 싶더라도, recover 자체는 파일 하나씩만 다루도록 설계되어 있다 — 33장(for)에서 배운 반복문으로 여러 파일에 순서대로 recover를 호출하는 것은 가능하지만, 명령 자체의 한계는 그대로 남는다.

**chkdsk가 표시한 배드 섹터는 recover에 영향을 주지 않는다**: chkdsk가 검사 과정에서 배드 섹터로 표시한 영역은 이미 파일 시스템 준비 단계에서 위험 구역으로 격리된 것으로, recover의 대상이 아니다.

> "Bad sectors reported by the chkdsk command were marked as bad when your disk was prepared for operation. They pose no danger, and recover does not affect them." — Microsoft Learn, "recover"

recover가 다루는 것은 그 이후 실제 사용 중 새로 발생한 물리적 손상이다.

**PowerShell에 직접 대응하는 cmdlet은 없다**: recover.exe가 수행하는, 손상된 파일을 섹터 단위로 읽어 읽을 수 있는 부분만 골라 복사하는 기능은 매우 좁고 특수한 레거시 동작이라 이에 대응하는 PowerShell cmdlet이 없다. Storage 모듈의 `Repair-Volume` 등은 파일 시스템 구조 자체를 복구하는 데 초점을 맞추고 있어 recover의 개별 파일 단위 복구와는 목적이 다르다. 이 좁은 용도의 기능이 필요하면 여전히 CMD의 recover를 직접 실행해야 한다.

## 흔한 오개념

<strong>"recover는 전문 데이터 복구 도구를 대체할 수 있다"</strong>는 오해가 있다. recover는 섹터 단위로 읽을 수 있는 것만 그대로 복사하는 매우 단순한 도구일 뿐, 손상된 섹터를 재구성하거나 파일 시스템 메타데이터가 깨진 상황을 복구하는 기능은 전혀 없다. 중요한 데이터가 걸린 심각한 손상이라면 recover로 1차 시도를 해볼 수는 있지만, 그 결과가 만족스럽지 않다면 전문 복구 서비스나 도구를 고려해야 한다 — 46장(convert)에서도 언급했듯, 애초에 정기적인 백업이 이런 상황 자체를 피하는 가장 확실한 방법이다.

## 다음 장에서는

다음은 53장 — Part 5의 마지막 장으로, 디스크 쓰기 검증 여부를 설정하는 `verify` 명령을 다룬다.

## 평가 기준

- recover로 손상된 디스크에서 파일을 부분적으로 복구할 수 있다.
- 손상된 섹터의 데이터가 영구히 사라진다는 것과, 그 이유로 한 번에 한 파일만 지정해야 한다는 것을 설명할 수 있다.
- chkdsk가 표시하는 배드 섹터와 recover가 다루는 손상이 서로 다른 시점의 문제라는 것을 설명할 수 있다.
- recover가 전문 데이터 복구 도구의 대체재가 아니라는 것을 안다.

## 참고

- [recover | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/recover)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
