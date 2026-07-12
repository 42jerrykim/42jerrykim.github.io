---
collection_order: 4
date: 2026-03-11
lastmod: 2026-07-12
draft: false
image: wordcloud.png
title: "[Compiler 02] GCC vs Clang vs MSVC 최적화 차이"
slug: compiler-comparison-gcc-clang-msvc
description: "동일 소스·플래그에서 GCC/Clang/MSVC의 속도·크기 차이, 벡터화·인라이닝·루프 최적화 영역별 차이, 플랫폼별 선택 기준을 다룹니다. 동일 벤치마크로 컴파일러별 수치 비교 방법과 다중 컴파일러 빌드·회귀 검증 절차를 제시합니다."
tags:
  - C++
  - Performance(성능)
  - Optimization(최적화)
  - Compiler(컴파일러)
  - CPU(Central Processing Unit)
  - Cache
  - Memory(메모리)
  - Benchmark
  - Profiling(프로파일링)
  - CI-CD(Continuous Integration/Continuous Deployment)
  - Testing(테스트)
  - Implementation(구현)
  - Code-Quality(코드품질)
  - Linux(리눅스)
  - Windows(윈도우)
  - OS(운영체제)
  - Concurrency(동시성)
  - Latency
  - Throughput
  - Backend(백엔드)
  - Embedded(임베디드)
  - Debugging(디버깅)
  - Documentation(문서화)
  - Refactoring(리팩토링)
  - Clean-Code(클린코드)
  - Best-Practices
  - Git
  - Automation(자동화)
  - Software-Architecture(소프트웨어아키텍처)
  - Design-Pattern(디자인패턴)
  - Data-Structures(자료구조)
  - Time-Complexity(시간복잡도)
  - Complexity-Analysis(복잡도분석)
  - Edge-Cases(엣지케이스)
  - Pitfalls(함정)
  - Error-Handling(에러처리)
  - Guide(가이드)
  - Reference(참고)
  - Technology(기술)
  - Tutorial(튜토리얼)
  - Advanced
  - Deep-Dive
  - 실습
  - Case-Study
  - Assembly
---

같은 C++ 코드라도 **컴파일러**에 따라 생성 코드와 성능이 달라집니다. **GCC**, **Clang**, **MSVC**는 벡터화·인라이닝·루프 최적화 정책이 달라 동일 소스·동일 플래그에서도 속도·크기 차이가 납니다. 이 챕터에서는 세 컴파일러의 최적화 차이, **언제 어떤 컴파일러를 선택할지** 판단 기준, 동일 벤치마크로 비교하는 방법을 다룹니다.

## 역사·배경

세 컴파일러는 각자 다른 필요와 시대적 요구에서 탄생했으며, 그 설계 철학의 차이가 오늘날의 최적화 차이로 이어집니다.

**GCC(GNU Compiler Collection)**는 1987년 Richard Stallman이 자유 소프트웨어 운동의 일환으로 시작했습니다. GNU 생태계의 기본 컴파일러로, 수십 년에 걸쳐 수많은 아키텍처와 플랫폼을 지원하면서 넓은 호환성이 핵심 설계 목표였습니다. 루프 최적화·벡터화·인라이닝 전략은 실용적이고 안정적인 쪽을 지향하며, 특정 서버 워크로드에서 강점을 보이는 경우가 많습니다.

**Clang**은 2007년 Apple이 LLVM 기반으로 시작했습니다. GCC의 라이선스·아키텍처 제약에서 벗어나 **모듈화된 컴파일러 인프라**를 만들기 위한 시도였으며, 빠른 컴파일 시간·우수한 진단 메시지·라이브러리로서의 재사용성이 설계 목표였습니다. 내부적으로 LLVM IR 최적화 파이프라인을 공유하므로, LLVM 생태계(LTO, PGO, sanitizers, AddressSanitizer 등)와 자연스럽게 연동됩니다.

**MSVC(Microsoft Visual C++)**는 1993년부터 Windows 개발 도구로 발전했습니다. Visual Studio와의 긴밀한 통합, Windows ABI·COM·DLL 모델과의 호환이 최우선입니다. 2015년 이후 C++ 표준 준수가 크게 향상되었고, 최신 버전은 성능 최적화도 적극적으로 개선되고 있습니다.

대부분의 C++ 코드에서 GCC와 Clang은 사실상 호환되지만, 특정 SIMD 패턴이 들어간 수치 커널에서는 생성 코드가 10~30%까지 차이 날 수 있습니다(측정값은 코드·CPU·플래그에 따라 다름). 그래서 컴파일러 선택은 "어느 쪽이 빠르다"는 통념이 아니라 **자신의 워크로드에서의 측정**으로 결정해야 합니다.

이 역사적 배경을 알면 왜 동일 소스에서 다른 코드가 나오는지 이해하기 쉽습니다. GCC는 특정 루프 패턴에서 Clang보다 공격적인 벡터화를 하기도 하고, Clang은 일부 템플릿 중심 코드에서 GCC보다 더 잘 최적화하는 경우가 있습니다.

## 동일 소스·플래그에서의 결과 차이

동일한 C++ 소스에 **같은 최적화 수준**(예: -O2, -O3)을 적용해 GCC, Clang, MSVC로 각각 빌드하면 **실행 속도**와 **바이너리 크기**가 다르게 나오는 경우가 많습니다. 차이는 코드 패턴에 따라 0%에 가깝게 나올 수도 있고, 10~30% 이상 나올 수도 있습니다. 수치·SIMD·템플릿이 많이 쓰인 코드일수록 컴파일러 간 차이가 두드러지는 경향이 있습니다.

- **속도**: 특정 루프에서 GCC가 빠르고 Clang이 느리거나, 그 반대인 경우가 있습니다. 한 컴파일러가 특정 아키텍처·특정 최적화(예: AVX2 활용)에서 강점을 보이는 경우가 있어, 단일 "승자"는 없습니다.
- **크기**: 인라이닝·언롤링 정책 차이로 텍스트 크기가 달라지고, 이는 I-cache 압박으로 이어져 간접적으로 속도에도 영향을 줄 수 있습니다.

따라서 "가능하면 여러 컴파일러로 빌드해 보고, 자신의 워크로드·타겟 플랫폼에서 가장 잘 나오는 조합"을 선택하는 것이 현실적입니다.

## 벡터화·인라이닝·루프 최적화 영역별 차이

- **벡터화**: GCC와 Clang 모두 auto-vectorization을 지원하지만, 루프 형태·데이터 정렬·타입에 따라 한쪽이 더 공격적으로 벡터화하거나 더 나은 명령 시퀀스를 만들 수 있습니다. MSVC도 SIMD 지원이 있으며, x86/x64에서 동작이 다를 수 있습니다.
- **인라이닝**: 인라이닝 임계값·휴리스틱이 컴파일러마다 달라서, 같은 함수가 한 컴파일러에서는 인라인되고 다른 곳에서는 호출로 남을 수 있습니다. LTO를 켜면 크로스-TU 인라이닝 기회가 생겨 컴파일러 간 차이가 더 복잡해질 수 있습니다.
- **루프 최적화**: 언롤링, 루프 융합, 제거 등 정책이 다르므로, 루프가 많은 코드에서 수치 차이가 납니다.

버그나 표준 준수 차이도 있을 수 있어, "빠르기만 하면 된다"가 아니라 정확성·이식성을 함께 확인하는 것이 좋습니다.

## 플랫폼별 선택

- **Linux**: GCC가 기본 설치에 포함되는 경우가 많고, Clang은 LLVM 생태계·도구와의 연동이 좋습니다. 배포 대상이 오래된 glibc를 쓰면 특정 GCC 버전에 맞춰 빌드하는 경우가 많습니다.
- **Windows**: MSVC가 Visual Studio와 통합되어 있고, Windows SDK·ABI와 잘 맞습니다. Clang-cl로 MSVC 호환 모드 빌드도 가능해, 툴체인만 바꿔서 비교할 수 있습니다.
- **타겟 CPU**: 특정 CPU 계열(x86, ARM, 특정 확장 명령)에 최적화된 코드를 원하면, 해당 타겟에서 튜닝이 잘 된 컴파일러·버전을 선택합니다. 크로스 컴파일 시에는 GCC/Clang의 -march, -mtune 등으로 타겟을 지정합니다.

## 어셈블리로 컴파일러 차이 관찰하기

동일한 루프를 각 컴파일러로 컴파일하면 어떤 기계어가 나오는지 직접 확인하는 것이 가장 확실한 비교 방법입니다. 다음은 float 배열의 합산 루프 예시입니다.

```cpp
// sum.cc: 컴파일러별 벡터화 차이를 관찰하기 위한 최소 예시
float sum_array(const float* arr, int n) {
    float s = 0.0f;
    for (int i = 0; i < n; ++i)
        s += arr[i];
    return s;
}
```

위 코드를 `-O2 -march=native`로 각 컴파일러에서 빌드해 어셈블리를 보면 차이가 드러납니다.

```bash
# GCC: -S 로 어셈블리 추출
g++ -O2 -march=native -S sum.cc -o sum_gcc.s

# Clang: 동일한 방법
clang++ -O2 -march=native -S sum.cc -o sum_clang.s

# 비교: vmovups, vaddps(AVX 128bit), vaddpd 등 SIMD 명령 유무 확인
grep -E "(vmov|vadd|vhad|pxor|movss)" sum_gcc.s sum_clang.s
```

**GCC -O2 -march=native** 출력 예시(x86-64 AVX2 머신, 개념적):
```asm
; GCC는 이 루프를 256비트 YMM 레지스터로 벡터화하는 경우가 많음
vxorps  %ymm0, %ymm0, %ymm0        ; 누산기 초기화
.Lloop:
  vmovups (%rdi,%rax,4), %ymm1     ; 8개 float 동시 로드 (256비트)
  vaddps  %ymm1, %ymm0, %ymm0     ; 8개 float 동시 합산
  add     $8, %rax
  cmp     %rsi, %rax
  jl      .Lloop
; 수평 합산(hsum)으로 최종 결과 도출...
```

**Clang -O2 -march=native** 출력 예시:
```asm
; Clang은 같은 코드를 다른 루프 구조 또는 다른 언롤링으로 벡터화하기도 함
vxorps  %xmm0, %xmm0, %xmm0        ; 초기화
vmovups (%rdi), %ymm1               ; Clang은 때로 언롤링을 더 공격적으로 함
vmovups 0x20(%rdi), %ymm2
vaddps  %ymm1, %ymm0, %ymm0
vaddps  %ymm2, %ymm0, %ymm0
; ...
```

핵심은 "어느 쪽이 더 빠른지"가 루프 패턴·데이터 크기·CPU마다 달라진다는 것입니다. GCC가 특정 패턴에서 더 나은 언롤링을 선택하기도 하고, Clang이 특정 접근 패턴에서 더 나은 SIMD 시퀀스를 내기도 합니다.

**Godbolt(Compiler Explorer) 활용**: [godbolt.org](https://godbolt.org)에서 같은 소스를 여러 컴파일러·버전으로 동시에 컴파일해 비교할 수 있습니다. 좌측 패널에 소스, 우측에 여러 컴파일러 탭을 열어 나란히 어셈블리를 보면 차이가 한눈에 들어옵니다.

## 동일 벤치마크로 컴파일러별 수치 비교 방법

이론적 분석(어셈블리 비교)과 함께 **실측 벤치마크**로 실제 성능 차이를 확인하는 절차가 필요합니다.

```bash
# 1. 동일 소스에서 컴파일러별 바이너리 빌드
g++   -O2 -march=native benchmark.cc -o bench_gcc
clang++ -O2 -march=native benchmark.cc -o bench_clang
# Windows MSVC: cl /O2 /arch:AVX2 benchmark.cc /Fe:bench_msvc.exe

# 2. 같은 벤치마크를 각각 N회 실행 (예: Google Benchmark 사용)
./bench_gcc   --benchmark_repetitions=10 --benchmark_report_aggregates_only=true
./bench_clang --benchmark_repetitions=10 --benchmark_report_aggregates_only=true

# 3. 결과를 파일로 저장해 비교
./bench_gcc   --benchmark_out=gcc_result.json   --benchmark_out_format=json
./bench_clang --benchmark_out=clang_result.json --benchmark_out_format=json
```

- **동일 스크립트**: 같은 소스 트리, 같은 의존성, 같은 벤치마크 실행 스크립트를 유지합니다.
- **빌드 변수**: 컴파일러(CC/CXX)와 플래그(-O2, -O3, -flto 등)만 바꿔 가며 여러 바이너리를 만듭니다.
- **측정**: 각 바이너리에 대해 동일한 벤치마크를 여러 번 돌려 평균·표준편차(또는 백분위)를 기록합니다. 환경(CPU 고정(`taskset`·`isolcpus`), 배경 부하 최소화)을 맞추어 재현 가능하게 측정합니다.
- **기록**: 결과를 표나 차트로 남겨 두면, 컴파일러·버전 업그레이드 시 회귀나 개선을 확인하기 쉽습니다. CI에 "다중 컴파일러 벤치마크" 단계를 두면 변경이 특정 컴파일러에서만 성능을 깨는지도 알 수 있습니다.

## 한눈에 보기: 컴파일러별 특징

| 영역 | GCC | Clang | MSVC |
|------|-----|-------|------|
| 벡터화 | auto-vectorization, 아키텍처별 튜닝 | LLVM 벡터화, 루프 형태에 민감 | SIMD 지원, x86/x64 |
| 인라이닝 | -O2/-O3 휴리스틱 | 다른 임계값·정책 | /O2 휴리스틱 |
| 루프 | 언롤링·융합 등 | 유사·세부 차이 | 자체 정책 |
| 플랫폼 | Linux 기본, 크로스 많음 | LLVM 생태계, clang-cl(MSVC 호환) | Windows 통합 |

## 컴파일러 버전과 최신 동향

컴파일러는 지속적으로 최적화 능력이 향상되므로, 특정 버전에서의 "GCC가 빠르다" 또는 "Clang이 빠르다"는 결론이 다음 메이저 릴리즈에서 역전될 수 있습니다.

- **GCC 12/13/14**: 자동 벡터화·루프 최적화 개선, C++20 완성도 향상
- **Clang 15/16/17+**: LLVM 벡터화 파이프라인 강화, C++20 모듈 지원 개선
- **MSVC (VS 2022+)**: 최근 버전에서 성능 최적화 품질이 크게 향상, `/arch:AVX512` 지원 강화

따라서 **사용 중인 컴파일러 버전을 명시**하고, 툴체인 업그레이드 시에는 동일 벤치마크로 재측정하는 것이 좋습니다.

## 실전 시나리오: 컴파일러 선택 결정 과정

새 프로젝트에서 Linux 서버용 릴리즈를 준비한다고 가정합니다.

1. **기본 빌드**: GCC와 Clang 각각으로 빌드해 두 바이너리를 준비합니다.
2. **핵심 벤치마크 실행**: 핫패스를 잘 커버하는 벤치마크를 각 바이너리에서 10회 이상 실행합니다.
3. **어셈블리 확인**: 핫 함수를 `-S`로 뽑아 벡터화 여부와 루프 구조를 비교합니다.
4. **결과 기록**: GCC vs Clang의 평균·표준편차를 기록하고 차이가 유의미한지 판단합니다.
5. **선택**: 수치가 비슷하면 팀의 도구·CI 환경에 더 잘 맞는 쪽을 선택합니다. 유의미한 차이(5% 이상)가 있으면 더 빠른 쪽을 채택합니다.
6. **CI에 반영**: 선택한 컴파일러·버전을 고정하고, 주기적으로 벤치마크를 돌려 회귀를 감지합니다.

## 용어 정리

| 용어 | 설명 |
|------|------|
| **auto-vectorization** | 컴파일러가 루프 등을 자동으로 SIMD 명령으로 바꾸는 최적화 |
| **I-cache** | Instruction cache; 코드 크기가 크면 캐시 미스 증가로 간접적으로 속도에 영향 |
| **YMM** | 256비트 AVX 레지스터; 8개의 float 또는 4개의 double을 동시에 처리 |
| **Godbolt** | Compiler Explorer; 브라우저에서 여러 컴파일러로 동시에 컴파일해 어셈블리를 비교하는 도구 |

## 판단 기준: 언제 어떤 컴파일러를 쓸지

| 상황 | 권장 | 비권장 |
|------|------|--------|
| Linux 배포 | GCC 또는 Clang, 벤치로 선택 | 단일 컴파일러 고정(비교 없이) |
| Windows 네이티브 | MSVC 또는 clang-cl | 이식성 무시한 플랫폼 전용 최적화만 |
| 극한 성능 | 여러 컴파일러로 빌드 후 벤치 비교 | "한 컴파일러가 항상 빠르다" 가정 |
| 표준 준수·버그 | 다중 컴파일러 빌드로 검증 | 한 컴파일러만 신뢰 |

## 자주 하는 실수

- **한 컴파일러만 고정·비교 생략**: "GCC가 빠르다" 또는 "Clang이 무난하다"는 말은 특정 코드·플랫폼에서의 경험일 뿐이다. 자신의 워크로드·타겟에서 여러 컴파일러로 빌드해 보지 않고 한 가지만 쓰면, 더 나은 선택을 놓칠 수 있다.
- **플랫폼 차이 무시**: Linux에서만 벤치한 결과를 Windows·다른 아키텍처에 그대로 적용하면 안 된다. 배포 대상 플랫폼에서 실제로 사용할 컴파일러·플래그로 측정해야 한다.
- **컴파일러 전환 시 검증 생략**: 툴체인을 바꾼 뒤 단위 테스트만 하고 성능 회귀를 측정하지 않으면, 특정 컴파일러에서만 느려지는 경로를 놓친다. 전환 후 동일 벤치로 전/후 수치를 비교한다.

## 학습 성과 목표

- 동일 소스·플래그에서 **GCC/Clang/MSVC**의 속도·크기 차이를 설명할 수 있다.
- **벡터화·인라이닝·루프** 영역별 차이를 말하고, 플랫폼별 선택 근거를 제시할 수 있다.
- 동일 벤치마크로 컴파일러별 수치를 비교하는 절차를 적용할 수 있다.

## 비판적 시각: 한계와 트레이드오프

"한 컴파일러가 항상 빠르다"는 **거짓**에 가깝다. 코드 패턴·아키텍처·최적화 플래그에 따라 GCC·Clang·MSVC 중 어느 쪽이 유리한지 달라진다. 단일 승자를 정하는 것이 아니라, 자신의 환경에서 **측정 기반으로 선택**해야 한다. 버그나 표준 준수 차이도 있으므로, 속도만 보지 말고 다중 컴파일러 빌드로 정확성·이식성을 함께 확인하는 것이 전문가다운 판단이다.

## 핵심 요약

| 항목 | 요약 |
|------|------|
| 차이 | 동일 소스라도 컴파일러에 따라 0~30% 이상 속도·크기 차이 가능 |
| 선택 | 자신의 워크로드·타겟에서 벤치로 비교 후 선택 |
| 검증 | 다중 컴파일러 빌드·벤치로 회귀·정확성 확인 |

## 다음 장에서는

**인라이닝 실패** 원인(가시성, ODR/ABI, 코드 크기), 인라이닝 리포트 확인 방법, Tr.01 연계를 다룹니다.

→ [인라이닝 실패 진단](/post/compiler-optimization/inlining-diagnostics/) (챕터 05)
