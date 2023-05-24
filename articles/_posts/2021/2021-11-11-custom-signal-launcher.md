---
title: "[Linux] Custom Signal을 만드는 방법"
categories:
  - Linux
tags:
  - Cpp
  - C
  - Linux
  - Signal
---

Custom Signal Handler를 만들어서 사용하는 방법에 대해서 알아본다. 

# 시그널의 종류

# Sigaction을 사용하여 Custom Signal Handler 등록하기

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
# async-signal-safe function을 사용해야 한다.

[signal-safety(7) — Linux manual page](https://man7.org/linux/man-pages/man7/signal-safety.7.html)
