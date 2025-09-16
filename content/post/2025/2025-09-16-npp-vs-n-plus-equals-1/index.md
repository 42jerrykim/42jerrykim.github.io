---
title: "[Programming] n++ vs n = n + 1: 성능과 최적화의 진실"
subtitle: "현대 컴파일러/JIT, ++i vs i++, 그리고 올바른 벤치마킹"
description: "n++와 n = n + 1는 현대 컴파일러와 JIT에서 거의 동일한 기계어로 최적화됩니다. 오래된 ‘n++가 더 빠르다’는 속설의 배경, ++i vs i++의 차이(반복자 비용), 올바른 벤치마킹 방법을 간결히 정리합니다."
date: 2025-09-16
lastmod: 2025-09-16
categories:
- "Programming"
- "Performance"
- "C/C++"
- "Java"
tags:
- "performance"
- "optimization"
- "compiler"
- "JIT"
- "C"
- "C++"
- "Java"
- "C#"
- "Go"
- "Rust"
- "x86"
- "assembly"
- "add instruction"
- "inc instruction"
- "IR"
- "SSA"
- "peephole optimization"
- "strength reduction"
- "dead code elimination"
- "microbenchmark"
- "benchmark"
- "JMH"
- "BenchmarkDotNet"
- "Google Benchmark"
- "iterator"
- "pre-increment"
- "post-increment"
- "prefix increment"
- "postfix increment"
- "operator"
- "semantics"
- "undefined behavior"
- "aliasing"
- "register allocation"
- "pipeline"
- "branch prediction"
- "hot path"
- "JIT warmup"
- "codegen"
- "decompilation"
- "disassembly"
- "performance myths"
- "coding style"
- "readability"
- "best practices"
- "low-level"
- "machine code"
- "flags"
- "carry flag"
- "overflow flag"
- "zero flag"
- "CPU"
- "compiler optimization"
- "optimization barrier"
- "성능"
- "최적화"
- "컴파일러"
- "어셈블리"
- "증가 연산자"
- "전위 증가"
- "후위 증가"
- "반복자"
- "가독성"
- "의미론"
- "미시 벤치마크"
- "벤치마크"
- "기계어"
- "레지스터"
- "파이프라인"
- "분기 예측"
- "플래그"
- "코딩 스타일"
- "모범 사례"
---

개발 커뮤니티에서는 오래전부터 “`n++`가 `n = n + 1`보다 빠르다”는 속설이 회자됩니다. 그러나 현대 컴파일러/런타임은 두 표현을 거의 동일한 기계어(예: x86의 `add reg, 1`)로 낮추므로, 기본 정수형에서는 체감 가능한 성능 차이가 사실상 없습니다. 그럼에도 불구하고 이 믿음이 남아 있는 이유는 과거 ISA 인코딩 차이, 플래그 처리, 그리고 언어별 의미론 차이에서 비롯된 오해가 적지 않기 때문입니다.

이 글에서는 그 속설의 배경을 CPU/ISA 관점(inc vs add), 컴파일러/JIT 관점(최적화, 레지스터 할당, 핫 패스)에서 짚어보고, **언어별 주의사항**(특히 C++ 반복자에서 `++i` 권장 이유, 멀티스레드에서 원자성 문제)을 정리합니다. 더불어 잘못된 측정으로 인한 결론 왜곡을 막기 위해 **올바른 마이크로벤치마크 방법**과 실무에서의 **우선순위**(알고리즘·캐시·메모리 레이아웃)를 제시합니다.

핵심 요지는 간단합니다. 기본 정수형 증가에서는 연산자 형태가 성능을 좌우하지 않습니다. 가독성과 코드 의미가 먼저이며, 진짜 성능은 더 큰 구조적 결정이 좌우합니다.

## 요약
- **결론**: 기본 정수형에서는 `n++`와 `n = n + 1`(또는 `n += 1`)이 현대 컴파일러/JIT에서 **동일한 기계어**로 최적화되어 보통 **성능 차이가 없다**.
- **왜 그렇게 되나**: x86 등에서 모두 `add reg, 1`로 생성되는 경우가 일반적이며, 과거의 `inc`/`dec` 미세 차이는 플래그 처리 차이 때문에 오늘날엔 오히려 잘 쓰이지 않는다.
- **예외**: C++ 반복자/사용자 정의 타입에서는 `i++`(후위)가 이전 값 보존을 위해 **불필요한 복사 비용**이 생길 수 있어, **`++i`(전위)**를 권장한다.

## 오래된 속설과 현대 최적화
과거에는 `n++`가 더 빠르다는 주장이 있었지만, 현대의 C/C++/Java/C#/Go/Rust 컴파일러와 런타임 JIT는 모두 간단한 증가 연산을 **동일한 수준의 기계어로 축약**한다. 특히 x86에서는 상태 플래그 처리 특성 때문에 `inc`보다 `add`가 더 일관적인 선택이며, 대부분의 컴파일러가 **`add reg, 1`**을 선호한다.

## 같은 의미면 같은 코드가 나온다
아래 C/C++ 예시는 보통 동일한 코드로 컴파일된다(최적화 켠 경우).

```cpp
int f(int n) {
  n++;
  return n;
}

int g(int n) {
  n = n + 1;
  return n;
}
```

둘 모두 대개 레지스터에 대해 `add` 한 번으로 표현된다. Java/C# 같은 JIT 환경에서도 JIT 워밍업 후 **핫 패스**에 동일한 증분이 배치된다.

## 언제 차이가 날 수 있나: C++ 반복자와 사용자 정의 타입
기본 정수형과 달리, 반복자나 사용자 정의 타입에서는 **후위 증가(`i++`)가 이전 값을 반환**해야 하므로 임시 객체 생성/복사 비용이 발생할 수 있다. 이 때문에 C++ 커뮤니티에서는 범용적으로 **전위 증가(`++i`)** 습관을 권장한다. 단, 기본 정수형에서는 `i++`와 `++i`가 같은 코드가 되어 성능 차이는 없다.

```cpp
// vector<int>::iterator에서 ++i 권장 관례
for (auto it = v.begin(); it != v.end(); ++it) {
  // ...
}
```

## 마이크로벤치마크 주의 사항
미세 차이를 직접 재려고 하면, 측정 자체가 더 큰 오차를 만든다. 올바른 방법은 다음과 같다.

- **최적화 옵션**: C/C++는 `-O2`/`-O3`를 사용하고 릴리즈 빌드에서 측정.
- **워밍업**: JIT 언어(Java/C#)는 워밍업 후 steady-state를 측정.
- **프레임워크**: Java는 JMH, .NET은 BenchmarkDotNet, C++는 Google Benchmark를 권장.
- **소거 방지**: 결과를 관측하거나 `DoNotOptimize`/`ClobberMemory` 같은 도구로 **DCE**(dead code elimination)를 방지.

간단히 말해, 이 주제는 **알고리즘 선택**이나 **메모리 접근 패턴** 같은 큰 요인에 비해 영향이 미미하다.

## 추천 가이드
- **기본 정수형**: 가독성에 맞게 아무 것이나 사용해도 무방.
- **C++ 반복자/사용자 정의 타입**: 관례적으로 **`++i`** 사용.
- **성능 최적화의 우선순위**: 자료구조 선택, 캐시 적중률, 분기 예측, 메모리 레이아웃 개선이 훨씬 중요.

## CPU/ISA 관점: INC vs ADD, 왜 ADD가 보편적인가
현대 x86에서 정수 1 증가를 표현하는 방식은 대개 `add reg, 1`이다. 과거에는 `inc reg`가 더 짧은 인코딩을 제공해 미세하게 유리하다는 인식이 있었지만, 최근 컴파일러는 다음 이유로 `add`를 선호한다.

- **플래그(FLAGS) 일관성**: `inc`/`dec`는 `CF`(Carry Flag)를 변경하지 않지만, `add`/`sub`는 변경한다. 많은 최적화와 패턴 매칭이 `CF` 포함 전체 플래그语를 전제로 하기에 `add`가 더 예측 가능하다.
- **마이크로아키텍처 고려**: 일부 마이크로아키텍처에서 `inc`/`dec`는 부분 플래그 업데이트로 인해 플래그 의존성 추적이 까다로워질 수 있다. 반면 `add`는 일반적으로 플래그 처리 경로가 잘 최적화되어 있다.
- **타 ISA에서도 유사**: AArch64(ARM64)에는 별도의 `inc`가 없고 즉치수 더하기(`add xN, xN, #1`)로 표현한다. 결국 “증가=더하기”가 보편적이다.

핵심은, 오늘날 대부분의 컴파일러/어셈블러가 **간결성과 일관성**을 위해 `add`를 선택하고, 그 결과 `n++`, `n += 1`, `n = n + 1`이 모두 같은 기계어로 수렴한다는 점이다.

## 컴파일러/JIT 관점: 어떤 코드가 생성되나
- **GCC/Clang/MSVC**: 최적화(`-O2`/`-O3`)에서 단순 정수 증가를 `add` 한 번으로 내보낸다. 인라이닝/레지스터 할당에 따라 메모리 대신 레지스터에서 수행된다.
- **HotSpot(.java), RyuJIT(.NET)**: JIT 워밍업 후 핫 루프에서 동일하게 “더하기 1”로 낮아진다. 초기 인터프리터/ tiered JIT 단계에서는 다소 다른 형태가 보일 수 있으나 steady-state에서는 동일해진다.
- **확인 방법**: 컴파일러가 생성한 어셈블리는 Compiler Explorer(`https://godbolt.org`) 같은 도구에서 쉽게 확인할 수 있다.

## 언어별 주의사항
- **C/C++**: 서브식에서의 중복 수정/접근은 정의되지 않은 동작이 될 수 있다. 예: `a = a++`는 피해야 한다. 반복자/사용자 정의 타입은 `i++`가 이전 값 보존을 위해 임시를 만들 수 있어 **`++i` 권장**.
- **Java/C#**: `n++`는 원자적이지 않다. 다중 스레드에서 원자적 증가가 필요하면 `AtomicInteger.incrementAndGet()`(Java), `Interlocked.Increment` 또는 `AtomicInteger`/`long`(C#의 경우 `Interlocked`) 같은 원자 연산을 사용한다. 성능상 `n++` vs `n = n + 1` 차이는 JIT 후 사실상 없다.
- **Go/Rust**: Rust는 `++` 연산자가 없고 `n += 1`를 쓴다. Go는 `n++`는 문(statement)이며 표현식에 쓸 수 없다. 의미 차이를 이해하고 스타일 가이드를 따른다.
- **Python/JS**: 동적/고수준 언어에서는 객체 불변성(Py int)과 런타임 오버헤드가 지배적이므로 미시적 연산자 선택은 의미가 없다.

## 마이크로벤치마크 템플릿
아래 예시들은 “같은 의미면 같은 코드가 나온다”를 직접 확인하는 데 도움을 준다. 반드시 릴리즈 빌드와 워밍업을 고려하라.

```cpp
// Google Benchmark (C++)
#include <benchmark/benchmark.h>

static void BM_PostInc(benchmark::State& state) {
  int n = 0;
  for (auto _ : state) {
    benchmark::DoNotOptimize(n++);
  }
}
BENCHMARK(BM_PostInc);

static void BM_AddAssign(benchmark::State& state) {
  int n = 0;
  for (auto _ : state) {
    benchmark::DoNotOptimize(n = n + 1);
  }
}
BENCHMARK(BM_AddAssign);

BENCHMARK_MAIN();
```

```java
// JMH (Java)
import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;

@State(Scope.Thread)
public class IncBench {
  int n;

  @Benchmark
  public void postInc(Blackhole bh) { bh.consume(n++); }

  @Benchmark
  public void addAssign(Blackhole bh) { bh.consume(n = n + 1); }
}
```

```csharp
// BenchmarkDotNet (.NET)
using BenchmarkDotNet.Attributes;
using BenchmarkDotNet.Running;

public class IncBench {
  private int n;

  [Benchmark]
  public int PostInc() => n++;

  [Benchmark]
  public int AddAssign() => n = n + 1;
}

public class Program { public static void Main() => BenchmarkRunner.Run<IncBench>(); }
```

## FAQ
- **Q. 무엇이 더 빠른가?** A. 기본 정수형에선 보통 동일하다. 컴파일러/JIT가 같은 기계어로 만든다.
- **Q. 그럼 왜 `++i`가 권장되나?** A. 반복자/사용자 정의 타입에서 후위 증가가 임시를 만들 수 있기 때문. 정수형에는 영향 거의 없음.
- **Q. 원자적 증가가 필요한가?** A. 언어별 원자 연산 API를 사용하라. `n++` 자체는 원자적이지 않다.
- **Q. 오버플로는?** A. C/C++에서 서명 있는 정수 오버플로는 정의되지 않은 동작이다. 연산자 형태와 무관하게 주의해야 한다. 필요하면 더 넓은 타입이나 모듈러 연산을 사용.

## 핵심 정리
- 같은 의미라면 오늘날 컴파일러/JIT는 같은 기계어로 수렴한다.
- 반복자/사용자 정의 타입에서는 `++i`를 습관적으로 사용하자.
- 마이크로차이보다 알고리즘/캐시/메모리 레이아웃이 성능을 좌우한다.

## 참고 링크
- [Quora: Why is n++ faster than n = n + 1?](https://www.quora.com/Why-is-n++-faster-than-n-n+1)
- [Compiler Explorer](https://godbolt.org)

