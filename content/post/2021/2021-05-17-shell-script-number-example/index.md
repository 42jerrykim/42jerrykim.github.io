---
image: "tmp_wordcloud.png"
description: "이 글에서는 숫자를 입력하여 다양한 명령어를 실행할 수 있는 셸 스크립트 예제를 소개합니다. 사용자가 숫자를 선택해 ls, ls -al, ls -a 등의 명령을 실행하는 기본 인터페이스와 구현법을 설명합니다."
categories:
- Shell
date: "2021-05-17T00:00:00Z"
tags:
- Shell
- Bash
- Linux
- Terminal
- Networking
- Technology
- Blog
- 블로그
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
title: '[Shell] 숫자로 메뉴 실행하는 셸스크립트 예제'
---

숫자를 이용해서 여러 명령어를 실행 할 수 있는 셸스크립트

## 코드

```bash
while (true) ; do
clean
echo '
1. cmd 1
2. cmd 2
3. cmd 3
q. end
'
echo -n "select:"
read no
case $no in
"1" )
 ls;;
"2" )
 ls -al;;
"3" )
    ls -a;;
"q" )
 exit 0;;
esac
done
```
