---
image: "tmp_wordcloud.png"
categories:
- LattePanda
date: "2018-12-06T00:00:00Z"
description: "LattePanda Alpha에 Ubuntu 16.04 LTS를 설치하는 방법을 단계별로 안내합니다. Ubuntu ISO 다운로드, 부팅 USB 제작, Secure Boot 비활성화, UEFI 부팅 선택부터 설치 유형 선택까지 실무 절차를 150자 분량으로 정리합니다."
redirect_from:
- /2018/12/06/
tags:
- linux
- Go
- Windows
- Security
- Process
- http
- Blog
- 블로그
- Technology
- 기술
- Web
- 웹
- Tutorial
- 가이드
- Review
- 리뷰
- Markdown
- 마크다운
- Guide
- Productivity
- 생산성
- Education
- 교육
- Reference
- 참고
- Best-Practices
- Documentation
- 문서화
- Open-Source
- 오픈소스
- Innovation
- 혁신
- Troubleshooting
- 트러블슈팅
- Configuration
- 설정
- How-To
- Tips
- Comparison
- 비교
- Career
- 커리어
- Workflow
- 워크플로우
- Migration
- 마이그레이션
- Hardware
- 하드웨어
- Mobile
- 모바일
- Cloud
- 클라우드
title: Install Ubuntu 16.04 on LattePanda Alpha
---

라테판다에 이미지 설치 하는 방법

## Get Ubuntu 16.04 LTS
Get a Ubuntu ISO from: http://releases.ubuntu.com/xenial/ -amd64.iso
## Make booting USB
Use your favourite disk writing tool (Etcher, Rufus, etc) to burn the ISO on to the USB or SD Card.
## Install Ubuntu 
1. Once that is done, boot on to your LattePanda, press the <kbd>DEL</kbd> key until you see the BIOS and disable secure boot in Security->Secure Boot->Secure Boot Enable = Disabled and set Secure Boot Mode to Custom.
2. Save changes and exit.
2. Insert your USB/SD Card and press <kbd>F7</kbd> for the boot menu and select the ubuntu UEFI entry (Should come up as 'UEFI Generic....')
3. Select 'Install Ubuntu'.
4. Once it boots to the desktop, go through the options that you need until you hit 'Installation Type' (You can either wipe Windows or Install along side it if you want to keep Windows.)
5. After this step, it seems to be a typical Ubuntu Installation process.
