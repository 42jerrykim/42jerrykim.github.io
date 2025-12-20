---
image: "tmp_wordcloud.png"
description: "Windows Defender(현 Microsoft Defender)의 보안 기능을 최적으로 설정하는 방법과 추가적인 안티바이러스 프로그램 없이도 안전하게 PC를 보호하는 팁을 설명합니다. 로컬 정책, MAPS, 랜섬웨어 방어 등 실전 활용법을 다룹니다."
categories:
- Windows
date: "2022-03-16T00:00:00Z"
header:
  teaser: /assets/images/undefined/Windows-Defender.jpg
tag:
- Windows
- Defender
- WindowsDefender
- Antivirus
- Virus
- Program
- built-in
- Protection
title: '[Windows] 설정만 잘 한다면 Windows Defender로도 충분하다.'
---

> 원문 : [Windows Defender is enough, if you harden it](https://0ut3r.space/2022/03/06/windows-defender/)

* 설정만 잘 한다면, 추가로 안티바이러스 프로그램 사서 설치할 필요없음
* 로컬 그룹 정책 설정
  * MAPS 활성화(Microsoft Advanced Protection Service)
* 랜섬웨어 보호
* 파워쉘을 통한 추가 설정
  * Signature Update Interval을 1시간으로, 매 스캔마다 강제 업데이트하게
  * MAPS 및 PUA 등도 가능
* 현재는 이름이 Microsoft Defender로 변경