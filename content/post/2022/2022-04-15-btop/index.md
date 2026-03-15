---
image: "tmp_wordcloud.png"
description: "btop++은 리눅스에서 CPU, 메모리, 디스크, 네트워크, 프로세스 등 다양한 시스템 자원을 한눈에 확인할 수 있는 고급 리소스 모니터링 툴입니다. 직관적인 UI와 다양한 커스터마이징 기능, 마우스 지원, 실시간 그래프를 제공하여 서버와 PC 환경 모두에서 효율적인 시스템 관리가 가능합니다."
categories:
- Linux
- Monitor
- Util
date: "2022-04-15T00:00:00Z"
header:
  teaser: /assets/images/2022/2022-04-15-122101.png
tags:
- Linux
- CPU
- Memory
- Networking
- 모니터링
- 메모리
- 리눅스
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
- C++
- Bash
- Shell
- Git
- GitHub
- Graph
- 그래프
- Process
- AI
- Gaming
- 게임
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
- Cloud
- 클라우드
- Mobile
- 모바일
- Deployment
- Performance
- 성능
title: '[Linux] btop++ 시스템 리소스 모니터 소개'
---

리눅스를 사용할 때 `top` 명령어로 CPU를 모니터링해 본 적이 있는가? 너무 보잘것없는 UI에 실망한 적이 있는가? 다른 리소스 사용량도 확인해 보고 싶은 생각은 없었는가? 본 글에서는 PC 자원을 한 화면에서 확인할 수 있는 btop++에 대해 소개한다.

btop++을 사용하면 아래 그림처럼 예쁜 UI와 함께 다양한 리소스 사용량을 모니터링할 수 있다.

|![/assets/images/2022/2022-04-15-122101.png](/assets/images/2022/2022-04-15-122101.png)|
|:---:|
|Main UI showing details for a selected process|

## btop++

[aristocratos/btop](https://github.com/aristocratos/btop)에 접속 하면 다양한 정보를 확인 할 수 있다.

아래와 같은 대표적인 특징을 가지고 있다.

- bashtop/bpytop 의 C++ 재작성 버전
- 프로세서, 메모리, 디스크, 네트워크, 프로세스 등의 리소스 모니터링 툴
- 사용하기 쉬운 게임 형태의 메뉴 시스템
- 전체 마우스 조작 지원
- 프로세스 필터링 및 소팅, 시그널 보내기 지원
- 네트웍 사용량 그래프, IO