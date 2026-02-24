---
image: "tmp_wordcloud.png"
description: "리눅스에서 Custom Signal Handler를 만드는 방법과 sigaction 함수 활용법, 시그널 종류, 안전하게 시그널을 처리하는 팁, 실전 예제 코드를 포함해 개발자가 알아야 할 핵심 내용을 150자 분량으로 쉽게 정리합니다."
categories:
- Linux
date: "2021-11-11T00:00:00Z"
tags:
- C++
- C
- Linux
- Action
- HTML
- Async
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
- 액션
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
title: '[Linux] Custom Signal을 만드는 방법'
---

Custom Signal Handler를 만들어서 사용하는 방법에 대해서 알아본다. 

## 시그널의 종류

## Sigaction을 사용하여 Custom Signal Handler 등록하기

``` c
#include <signal.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

void handler(int signo, siginfo_t *info, void *context)
{
    struct sigaction oldact;

    if (sigaction(SIGSEGV, NULL, &oldact) == -1 || (oldact.sa_flags & SA_UNSUPPORTED) || !(oldact.sa_flags & SA_EXPOSE_TAGBITS))
    {
        _exit(EXIT_FAILURE);
    }
    _exit(EXIT_SUCCESS);
}

int main(void)
{
    struct sigaction act = { 0 };

    act.sa_flags = SA_SIGINFO | SA_UNSUPPORTED | SA_EXPOSE_TAGBITS;
    act.sa_sigaction = &handler;
    if (sigaction(SIGSEGV, &act, NULL) == -1)
    {
        perror("sigaction");
        exit(EXIT_FAILURE);
    }

    raise(SIGSEGV);
}
```
## async-signal-safe function을 사용해야 한다.

[signal-safety(7) — Linux manual page](https://man7.org/linux/man-pages/man7/signal-safety.7.html)
