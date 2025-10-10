---
title: "[GCC] -finstrument-functions 사용법"
date: 2025-09-29T00:00:00+09:00
lastmod: 2025-09-29T00:00:00+09:00
description: "GCC 컴파일러의 -finstrument-functions 플래그는 함수 진입과 종료 시 훅 함수를 호출하여 코드 프로파일링과 디버깅을 가능하게 합니다. 이 가이드에서는 기본 사용법부터 고급 기법, 제한사항까지 전문가 수준으로 설명합니다. 성능 분석 도구로서의 활용을 중점으로 다룹니다."
tags:
  - gcc
  - GNU Compiler Collection
  - finstrument-functions
  - function instrumentation
  - code profiling
  - compiler flag
  - __cyg_profile_func_enter
  - __cyg_profile_func_exit
  - performance monitoring
  - debugging tools
  - low-level programming
  - embedded systems
  - optimization techniques
  - dynamic analysis
  - static instrumentation
  - c programming
  - c++
  - 프로파일링
  - 함수 계측
  - 컴파일러 옵션
  - 성능 분석
  - 디버깅
  - 저수준 프로그래밍
  - 임베디드 시스템
  - 최적화 기법
  - 동적 분석
  - 정적 계측
  - C 프로그래밍
  - C++
  - valgrind
  - gprof
  - perf tools
  - linux profiling
  - code instrumentation
  - hook functions
  - function tracing
  - execution flow analysis
  - runtime overhead
  - binary instrumentation
  - source code modification
  - 개발 도구
  - 소프트웨어 엔지니어링
  - 시스템 프로그래밍
  - 컴파일 과정
  - 어셈블리
  - 링커
  - 빌드 시스템
  - 오픈소스
  - GNU 프로젝트
  - 코드 커버리지
  - 테스트 자동화
image: wordcloud.png
---

## 소개

GCC(GNU Compiler Collection)는 C, C++, Fortran 등의 언어를 컴파일하는 강력한 도구입니다. 그 중 `-finstrument-functions` 플래그는 컴파일 시 각 함수의 진입과 종료 지점에 특수 훅 함수 호출을 삽입하여, 코드의 실행 흐름을 추적하고 분석할 수 있게 합니다. 이는 프로파일링, 디버깅, 성능 최적화에 유용하며, 특히 임베디드 시스템이나 저수준 프로그래밍에서 자주 사용됩니다.

이 글에서는 `-finstrument-functions`의 내부 메커니즘부터 실전 예제, 고급 활용법, 그리고 잠재적 제한사항까지 전문가 관점에서 다루겠습니다. 기본 지식이 있는 개발자를 대상으로 하며, GCC 13.x 버전을 기준으로 설명합니다.

## 메커니즘 이해

`-finstrument-functions` 플래그를 사용하면 컴파일러가 각 컴파일 유닛의 함수(비인라인 함수)에 대해 다음과 같은 코드를 자동 삽입합니다:

- 함수 진입 시: `__cyg_profile_func_enter(void *this_fn, void *call_site)` 호출
- 함수 종료 시: `__cyg_profile_func_exit(void *this_fn, void *call_site)` 호출

여기서:
- `this_fn`: 현재 함수의 주소 (함수 포인터)
- `call_site`: 호출 지점의 반환 주소

이 훅 함수들은 사용자가 정의해야 하며, 기본적으로 libgcc에 의해 제공되지 않습니다. 대신, 사용자가 직접 구현하여 로그 출력, 시간 측정, 메모리 사용량 추적 등을 수행할 수 있습니다.

**주의**: 인라인 함수, 생성자/소멸자, 또는 최적화로 제거된 함수에는 삽입되지 않습니다. 또한, `-finstrument-functions-exclude-file-list`나 `-finstrument-functions-exclude-function-list` 옵션으로 특정 파일이나 함수를 제외할 수 있습니다.

## 기본 사용법

### 컴파일

간단한 C 프로그램을 예로 들어보겠습니다. `example.c`:

```c
#include <stdio.h>

void sub_function(int x) {
    printf("Sub function called with %d\n", x);
}

int main() {
    for(int i = i < i++) {
        sub_function(i);
    }
    return 0;
}
```

컴파일 시 플래그 추가:

```bash
gcc -finstrument-functions -g example.c -o example
```

### 훅 함수 구현

훅 함수를 정의한 별도 파일 `hooks.c`를 작성하고 링크합니다:

```c
#include <stdio.h>
#include <dlfcn.h>  // 함수 이름 해석을 위해

void __cyg_profile_func_enter(void *this_fn, void *call_site) __attribute__((no_instrument_function));
void __cyg_profile_func_exit(void *this_fn, void *call_site) __attribute__((no_instrument_function));

Dl_info info;

void __cyg_profile_func_enter(void *this_fn, void *call_site) {
    if (dladdr(this_fn, &info) && info.dli_sname) {
        printf("Entering function: %s at %p\n", info.dli_sname, this_fn);
    }
}

void __cyg_profile_func_exit(void *this_fn, void *call_site) {
    if (dladdr(this_fn, &info) && info.dli_sname) {
        printf("Exiting function: %s at %p\n", info.dli_sname, this_fn);
    }
}
```

**중요**: 훅 함수 자체도 계측되지 않도록 `__attribute__((no_instrument_function))`를 사용합니다. 무한 재귀를 방지합니다.

컴파일 및 링크:

```bash
gcc -finstrument-functions -g example.c hooks.c -ldl -o example
```

실행:

```bash
./example
```

출력 예시:

```
Entering function: main at 0x401136
Entering function: sub_function at 0x4010f0
Sub function called with 0
Exiting function: sub_function at 0x4010f0
Entering function: sub_function at 0x4010f0
Sub function called with 1
Exiting function: sub_function at 0x4010f0
... (반복)
Exiting function: main at 0x401136
```

## 고급 활용법

### 성능 프로파일링

시간 측정을 위해 `clock_gettime`을 사용한 고급 훅:

```c
#include <time.h>

static struct timespec start_time;

void __cyg_profile_func_enter(void *this_fn, void *call_site) __attribute__((no_instrument_function)) {
    Dl_info info;
    if (dladdr(this_fn, &info) && info.dli_sname) {
        printf("ENTER: %s\n", info.dli_sname);
        clock_gettime(CLOCK_MONOTONIC, &start_time);
    }
}

void __cyg_profile_func_exit(void *this_fn, void *call_site) __attribute__((no_instrument_function)) {
    Dl_info info;
    struct timespec end_time;
    if (dladdr(this_fn, &info) && info.dli_sname) {
        clock_gettime(CLOCK_MONOTONIC, &end_time);
        double elapsed = (end_time.tv_sec - start_time.tv_sec) + (end_time.tv_nsec - start_time.tv_nsec) / 1e9;
        printf("EXIT: %s (%.seconds)\n", info.dli_sname, elapsed);
    }
}
```

이로써 각 함수의 실행 시간을 측정할 수 있습니다. 다만, 오버헤드가 발생하니 프로덕션 코드가 아닌 개발/테스트 환경에 적합합니다.

### 제외 옵션 사용

특정 함수나 파일을 제외:

```bash
gcc -finstrument-functions -finstrument-functions-exclude-file-list=main.c -finstrument-functions-exclude-function-list=init,main example.c hooks.c -ldl -o example
```

이 옵션은 불필요한 노이즈를 줄여 분석을 용이하게 합니다.

### 다중 스레드 환경

스레드 안전성을 위해 뮤텍스나 thread-local storage를 사용:

```c
#include <pthread.h>

static pthread_mutex_t log_mutex = PTHREAD_MUTEX_INITIALIZER;

void __cyg_profile_func_enter(void *this_fn, void *call_site) __attribute__((no_instrument_function)) {
    pthread_mutex_lock(&log_mutex);
    // 로그 로직
    pthread_mutex_unlock(&log_mutex);
}
```

### 다른 도구와 결합

- **GDB와 연동**: 계측된 함수 호출을 브레이크포인트로 설정.
- **Valgrind나 Perf와 비교**: `-finstrument-functions`는 소스 레벨 계측으로, 바이너리 계측 도구(예: Pin, DynamoRIO)와 대비됩니다.
- **커스텀 트레이서**: 훅에서 파일 I/O나 네트워크로 데이터를 전송하여 원격 프로파일링 구현.

## 제한사항과 주의점

**오버헤드**: 모든 함수 호출에 훅이 삽입되어 런타임 성능이 10-5저하될 수 있습니다. 특히 빈번한 작은 함수에서 두드러집니다.

**인라인 및 최적화**: `-O이상 최적화 시 일부 함수가 인라인되어 계측되지 않습니다. `-fno-inline`로 테스트 가능하나, 실제 성능 왜곡.

**플랫폼 의존성**: `dladdr`는 Linux/Unix에서 동작; Windows에서는 `SymFromAddr` 등 대체 필요. 크로스 컴파일 시 주의.

**재귀 및 무한 루프**: 훅 함수가 계측되지 않도록 해야 함. 이미 `__attribute__((no_instrument_function))`로 해결.

**대안 도구**: 더 세밀한 제어가 필요 시 Intel VTune, ARM Streamline, 또는 바이너리 계측 프레임워크(예: LLVM의 instrumentation passes) 고려.

## 결론

`-finstrument-functions`는 GCC의 강력한 기능으로, 코드의 내부 동작을 깊이 이해하고 최적화하는 데 필수적입니다. 기본 프로파일링부터 복잡한 시스템 분석까지 폭넓게 적용할 수 있지만, 오버헤드와 제한을 인지하고 사용해야 합니다. 실제 프로젝트에서 이 플래그를 활용해 보시기 바랍니다.

더 많은 GCC 팁과 프로그래밍 지식은 [42jerrykim.github.io](https://42jerrykim.github.io)에서 확인하세요.

---

참고 문헌:
- GCC Documentation: https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html
- Stack Overflow 및 관련 포럼 토론
