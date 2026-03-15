---
image: "tmp_wordcloud.png"
categories:
- Proxy
date: "2019-04-02T00:00:00Z"
description: "프록시 환경에서 pip으로 Python 패키지를 설치하는 방법을 설명합니다. pip install --proxy 옵션에 프록시 URL과 패키지 이름을 지정하는 문법, 실제 사용 예시 및 주의사항을 150자 분량으로 정리합니다."
redirect_from:
- /2019/04/02/
tags:
- Shell
- Proxy
- Bash
- Flask
- Design-Pattern
- Python
- Deployment
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
title: PIP 패키지 인스톨 Proxy 환경에서 사용하기
---



## PIP 패키지 인스톨 Proxy 환경에서 사용하기

아래 명령어는 프록시 설정을 추가한 패키지 인스톨 방법이다.

``` bash
pip install --proxy [Proxy http url] [Package name]
```

위와 같이 프록시 값을 먼저 설정한 뒤 설치할 패키지명을 추가한다. 예를 들어 아래와 같이 사용한다.

```bash
pip install --proxy http://000.111.222.333:4444 Flask
```

이제 정상적으로 설치가 수행될 것이다.