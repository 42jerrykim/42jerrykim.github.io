---
draft: false
slug: verify-command-verify-file-writes-windows-cmd
title: "[CMD] 53. verify - 디스크 쓰기 검증 설정"
description: "verify로 디스크에 쓴 데이터를 읽어서 검증할지 전역 설정을 켜고 끄는 법과 copy 명령의 개별 /v 옵션과의 관계, 검증이 쓰기 속도를 늦추는 트레이드오프를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 530
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
- verify
- 디스크쓰기검증
- File-System
- Documentation(문서화)
- Best-Practices
- Education(교육)
- CLI
- Legacy
- Comparison(비교)
- Configuration(설정)
- Troubleshooting(트러블슈팅)
- Performance
- Advanced
- Administration
- Productivity(생산성)
image: "wordcloud.png"
---

verify는 cmd.exe가 파일을 디스크에 올바르게 기록했는지 검증할지 여부를 설정하는 명령이다. Part 5(디스크와 파일 시스템 관리)의 마지막 장이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [52장: recover](/post/cmd/recover-command-recover-damaged-disk-windows-cmd/)에서 손상 데이터 복구를 다룬 뒤 이어지며, Part 5의 마지막 장이다. 검증(verify)을 켜두면 애초에 이런 손상을 더 빨리 알아챌 수 있다는 점에서, 이 장은 자연스럽게 Part 5 전체를 마무리한다.

**이 장의 깊이**: 입문. 옵션이 단순하지만 무엇을 검증하는지 정확히 아는 사람은 드물다.

## 사용법

```
verify [on | off]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `on` | 쓰기 후 검증 사용 |
| `off` | 쓰기 후 검증 사용 안 함 |

인수 없이 `verify`만 실행하면 현재 설정을 표시한다.

## 예시

```
verify
verify on
verify off
```

## 주의사항·함정

**전역 설정이며 copy의 `/v`와는 범위가 다르다**: 14장(copy)에서 다룬 `/v` 옵션은 그 한 번의 복사 명령에만 검증을 적용하는 반면, verify 명령으로 켠 설정은 그 이후 실행되는 모든 디스크 쓰기 작업에 전역으로 적용된다. `copy /v`를 매번 붙이는 대신 `verify on`을 한 번 실행해두면 이후 모든 쓰기 작업이 검증 대상이 된다.

**검증은 쓰기 속도를 늦춘다**: 디스크에 기록한 모든 섹터를 다시 읽어 비교하는 추가 작업이 필요하므로, verify가 켜져 있으면 파일 쓰기 작업 전반이 느려진다. 14장(copy)의 `/v` 설명에서도 같은 트레이드오프를 이미 언급했다 — 안정성과 속도 사이의 선택이라는 점에서 CMD 전역에도 동일하게 적용된다.

**현대 저장 장치에서는 기본값이 꺼져 있는 경우가 많다**: 이 검증 메커니즘은 신뢰성이 낮았던 오래된 저장 매체(플로피 디스크 등) 시절에 더 중요했던 기능이다. 현대 NTFS와 SSD·HDD 환경에서는 하드웨어 자체의 오류 검출·정정 기능이 훨씬 발전해, verify를 기본으로 켜두는 실익이 예전만큼 크지 않다. 정말 중요한 백업이라면 verify를 켜는 것보다 별도의 체크섬 비교나 전용 백업 검증 도구를 쓰는 경우가 많다.

**PowerShell에 직접 대응하는 cmdlet은 없다**: verify가 켜고 끄는 것은 cmd.exe 프로세스 자체의 전역 쓰기 검증 설정이라, 이에 대응하는 PowerShell cmdlet이 없다. PowerShell에서 파일 쓰기 후 무결성을 확인하려면 `Get-FileHash`로 체크섬을 직접 비교하는 식으로 별도의 검증 로직을 스크립트로 작성해야 하며, verify는 여전히 CMD·DOS 시절부터 내려온 세션 전역 설정으로만 남아 있다.

## 흔한 오개념

<strong>"verify on을 켜두면 이미 디스크에 있는 파일들의 무결성도 검사해준다"</strong>는 오해가 있다. verify는 어디까지나 앞으로 일어날 쓰기 작업에 대해서만 사후 검증을 수행하는 설정이지, 42장(chkdsk)처럼 기존에 저장된 파일이나 파일 시스템 구조를 검사하는 기능이 아니다. 이미 저장된 데이터의 무결성이 궁금하다면 chkdsk나 체크섬 비교 같은 별도 도구가 필요하다.

## 다음 장에서는

다음은 54장 — 현재 실행 중인 프로세스 목록을 표시하는 `tasklist` 명령으로 Part 6(프로세스·서비스와 권한 관리)가 시작된다.

## 평가 기준

- verify로 디스크 쓰기 검증을 전역으로 켜고 끌 수 있다.
- verify(전역 설정)와 copy의 `/v`(개별 명령 옵션)의 범위 차이를 설명할 수 있다.
- 검증이 쓰기 속도를 늦추는 트레이드오프와, 현대 저장 장치에서 이 기능의 실익이 줄어든 이유를 설명할 수 있다.
- verify가 기존 파일의 무결성을 검사하는 기능이 아니라는 것을 안다.

## 참고

- [verify | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/verify)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
