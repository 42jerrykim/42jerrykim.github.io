---
draft: false
slug: ver-command-windows-version-cmd
title: "[CMD] 64. ver - Windows 버전 표시"
description: "ver로 현재 Windows 버전 번호를 한 줄로 확인하는 법과 PowerShell에서는 지원되지 않아 $PSVersionTable을 대신 써야 하는 이유, 상세 정보가 필요할 때 systeminfo로 넘어가야 하는 경계를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 640
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
- ver
- 버전확인
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Comparison(비교)
- Education(교육)
- CLI
- PowerShell
- Batch
- Configuration(설정)
- Productivity(생산성)
- DevOps
- Administration
- Advanced
image: "wordcloud.png"
---

ver는 운영체제 버전 번호를 표시하는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [63장: systeminfo](/post/cmd/systeminfo-command-hardware-os-info-windows-cmd/)에서 전체 시스템 정보를 다룬 뒤 이어진다. systeminfo가 모든 것을 보여준다면, ver는 그중 딱 한 가지(버전 번호)만 가장 빠르게 확인하는 명령이다.

**이 장의 깊이**: 입문. 옵션이 없어 매우 짧다.

## 사용법

```
ver
```

## 옵션

`/?` 외에 별도 옵션은 없다.

## 예시

```
ver
```

출력은 대략 `Microsoft Windows [Version 10.0.19045.1234]` 형태다.

## 주의사항·함정

**PowerShell에서는 지원되지 않는다**: ver는 cmd.exe 전용 명령이다.

> "This command is supported in the Windows Command prompt (Cmd.exe), but not in any version of PowerShell." — Microsoft Learn, "ver"

PowerShell에서 같은 정보를 확인하려면 `$PSVersionTable.BuildVersion`(Windows PowerShell) 또는 `$PSVersionTable.OS`(PowerShell 7.x)를 대신 써야 한다. cmd.exe 배치 스크립트를 PowerShell로 옮길 때 `ver` 호출을 그대로 두면 그 줄에서 실패한다.

**정밀한 빌드·에디션 정보가 필요하면 부족하다**: ver는 버전 번호 한 줄만 보여줄 뿐, 에디션(Pro, Enterprise 등)이나 설치 날짜, 핫픽스 목록 같은 상세 정보는 담지 않는다. 그런 정보가 필요하다면 63장에서 다룬 systeminfo나 68장에서 다룰 wmic(레거시)으로 넘어가야 한다.

## 흔한 오개념

<strong>"ver 출력을 보면 Windows 10인지 11인지 바로 알 수 있다"</strong>는 오해가 있다. ver는 `Microsoft Windows [Version 10.0.19045.1234]`처럼 원시 빌드 번호만 보여줄 뿐 "Windows 10"이나 "Windows 11" 같은 마케팅 이름을 표시하거나 구분해주지 않는다. 두 버전을 구별하려면 빌드 번호가 22000 이상인지를 사용자가 직접 알고 있어야 하는데, ver의 출력 어디에도 이 기준점은 언급되지 않는다.

## 다음 장에서는

다음은 65장 — 설치된 장치 드라이버 목록을 표시하는 `driverquery` 명령을 다룬다.

## 평가 기준

- ver로 현재 Windows 버전 번호를 확인할 수 있다.
- ver가 PowerShell에서는 지원되지 않으며, 대신 `$PSVersionTable`을 써야 한다는 것을 안다.
- 더 상세한 시스템 정보가 필요할 때 systeminfo로 넘어가야 하는 경계를 설명할 수 있다.

## 참고

- [ver | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/ver)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
