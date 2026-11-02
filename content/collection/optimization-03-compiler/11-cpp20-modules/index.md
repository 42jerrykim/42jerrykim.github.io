---
collection_order: 11
date: 2026-03-11
lastmod: 2026-10-21
draft: false
image: wordcloud.png
title: "[Compiler 03] C++20 Modules와 빌드·성능"
slug: cpp20-modules-build-performance
description: "C++20 Modules가 컴파일 시간을 줄이는 원리와 최적화 수준·빌드 순서에 따른 한계, BMI·Reduced BMI가 인라이닝에 주는 영향, Clang·GCC·MSVC·CMake 3.28 빌드 방법과 점진적 도입의 함정을 1차 문서 기준으로 다룹니다."
tags:
  - C++
  - C++20
  - Performance(성능)
  - Optimization(최적화)
  - Compiler(컴파일러)
  - Linux(리눅스)
  - Windows(윈도우)
  - CI-CD(Continuous Integration/Continuous Deployment)
  - Standard(표준)
  - Comparison(비교)
  - Pitfalls(함정)
  - Best-Practices
  - Guide(가이드)
  - Reference(참고)
  - Tutorial(튜토리얼)
  - Advanced
  - Deep-Dive
  - 실습
  - Open-Source(오픈소스)
  - Migration(마이그레이션)
  - GCC
  - Clang
  - MSVC
  - CMake
  - Modules
  - Build-System
  - Ninja
---

C++20 Modules는 헤더를 텍스트로 붙여 넣는 `#include` 대신, 한 번 컴파일한 모듈 인터페이스를 여러 번역 단위가 가져다 쓰는 빌드 모델입니다. 이 챕터에서는 모듈이 컴파일 시간을 줄이는 원리와 그 효과가 최적화 수준에 따라 달라지는 이유, 모듈이 인라이닝과 생성 코드에 주는 영향, 세 컴파일러와 CMake에서 모듈을 빌드하는 방법, 그리고 기존 코드베이스에 점진적으로 도입할 때의 함정을 다룹니다.

## 모듈이 해결하려는 문제

[cppreference의 Modules 문서](https://en.cppreference.com/w/cpp/language/modules)는 모듈을 다음과 같이 소개합니다.

> "Modules are a language feature to share declarations and definitions across translation units. They are an alternative to some use cases of headers." — cppreference, Modules (since C++20)

헤더 방식에서는 `#include`가 헤더의 텍스트를 그 자리에 복사하므로, 같은 헤더를 포함하는 번역 단위(TU)마다 컴파일러가 그 내용을 처음부터 다시 파싱하고 의미 분석합니다. 표준 라이브러리 헤더 몇 개만 포함해도 TU 하나가 수만 줄이 되는 일이 흔하고, 매크로가 헤더 경계를 넘어 새어 나가 포함 순서에 따라 의미가 바뀌는 문제도 있습니다. 모듈은 인터페이스를 한 번 컴파일해 그 결과를 저장하고, `import`하는 쪽은 그 결과를 읽어 들이게 합니다. 매크로는 모듈 경계를 넘지 않으므로 포함 순서에 따른 문제도 사라집니다.

컴파일된 인터페이스를 부르는 이름은 컴파일러마다 다릅니다. Clang은 이를 <strong>BMI(Built Module Interface)</strong>라 부르고 `.pcm` 파일로 저장하며, GCC는 <strong>CMI(Compiled Module Interface)</strong>라 부르고 `gcm.cache` 디렉터리에 `.gcm` 파일로, MSVC는 `.ifc` 파일로 저장합니다. 이름은 달라도 "import할 때 읽는, 컴파일러 전용 이진 인터페이스"라는 역할은 같고, 컴파일러 사이에 호환되지 않습니다.

## 빌드 시간: 효과는 최적화 수준에 따라 다르다

모듈이 빌드를 빠르게 하는 고전적인 설명은 [Clang의 Standard C++ Modules 문서](https://clang.llvm.org/docs/StandardCPlusPlusModules.html)가 잘 정리합니다. 헤더 n개를 소스 m개가 모두 포함하면 컴파일 작업량이 O(n·m)이지만, 모듈 인터페이스 n개를 소스 m개가 import하면 O(n+m)이 된다는 것입니다. 같은 문서는 이 설명이 큰 틀에서는 맞지만 **최적화 수준에 크게 좌우된다**고 덧붙입니다.

`-O0`에서는 import한 코드가 대부분 이름 찾기, 오버로드 해석, 템플릿 인스턴스화 같은 의미 분석에만 쓰이고, 코드 생성과 그 이후 단계는 모듈 단위에서 한 번만 일어나므로 이득이 큽니다. 반면 최적화를 켜면 컴파일러가 현재 TU를 최적화할 때 import한 모듈의 함수 본문을 보고 인라이닝 같은 프로시저 간 최적화를 하려 하므로, import한 코드가 사용하는 TU마다 다시 최적화 단계를 거치게 됩니다. Clang 문서는 IPO와 그 이전 최적화가 컴파일에서 가장 시간이 많이 드는 부분이라, 높은 최적화 수준에서는 `-O0` 경험에서 기대한 만큼 빌드가 빨라지지 않을 수 있지만 대신 최적화 기회는 더 많아진다고 설명합니다.

이득을 깎는 요인이 하나 더 있습니다. 모듈은 import하는 쪽보다 **먼저** 컴파일되어야 합니다. GCC 문서도 import 그래프가 방향성 비순환 그래프(DAG)이며 import 대상을 import하는 쪽보다 먼저 빌드해야 한다고 명시합니다. 헤더 방식에서는 모든 `.cpp`를 서로 독립적으로 병렬 컴파일할 수 있었지만, 모듈 방식에서는 빌드 시스템이 먼저 소스를 스캔해 의존 관계를 알아낸 뒤 그 순서대로 인터페이스를 빌드해야 합니다. 인터페이스 하나에 많은 TU가 매달린 구조라면 그 인터페이스가 끝날 때까지 나머지가 기다리므로, 코어가 많은 머신에서는 병렬성 손실이 파싱 절감분을 상쇄할 수도 있습니다.

| 요인 | 헤더(`#include`) | 모듈(`import`) |
|------|-----------------|----------------|
| 인터페이스 파싱·의미 분석 | TU마다 반복 | 인터페이스당 1회, import 시 BMI 읽기 |
| 최적화 단계(`-O2` 이상) | TU마다 반복 | 인라이닝 등을 위해 importer에서도 수행 |
| 빌드 병렬성 | TU끼리 독립 | 인터페이스 → importer 순서 제약 |
| 매크로 | 헤더 경계를 넘어 전파 | 모듈 경계에서 차단 |

따라서 모듈 전환의 빌드 시간 효과는 "몇 퍼센트 빨라진다"로 일반화할 수 없고, 디버그 빌드에서 크고 최적화 빌드에서 작은 경향이 있으며, 의존 그래프의 모양에 좌우됩니다. 도입 전에 대표 모듈 몇 개를 바꿔 자신의 빌드에서 `-O0`과 `-O2` 모두 측정해 보는 것이 가장 확실합니다.

## 런타임: 인라이닝과 생성 코드에 주는 영향

모듈은 언어의 실행 의미를 바꾸지 않으므로, 같은 코드라면 원칙적으로 같은 성능이 나와야 합니다. 그러나 빌드 모델이 바뀌면서 **인라이닝에 필요한 정보가 어디에 있느냐**가 달라질 수 있고, 이것이 런타임 성능 차이로 이어질 수 있는 유일한 경로입니다.

첫째, 명시적 `inline`의 의미가 바뀌지 않는다는 점입니다. Clang 문서는 호환성을 위해 명시적으로 `inline`인 개체는 모듈에서도 inline으로 남는다고 설명합니다. 반면 헤더에서 클래스 정의 안에 본문을 쓴 멤버 함수처럼 **암묵적으로 inline이던** 개체는 모듈로 옮기면 모듈 단위에서 한 번만 생성될 수 있다고 같은 문서가 설명합니다. 이것은 TU마다 중복 생성되던 코드를 줄여 바이너리 크기와 컴파일 시간에는 유리하지만, 그 함수를 호출하는 쪽에서 인라이닝이 일어나는지는 컴파일러가 import 시점에 본문을 볼 수 있느냐에 달려 있습니다.

둘째, BMI에 무엇이 담기느냐입니다. Clang 문서에 따르면 최적화 수준이 높을 때는 모듈에 정의된 함수의 본문이 importer의 최적화를 위해 제공되므로(그 함수의 코드 자체는 importer의 오브젝트에 들어가지 않음) 모듈 경계를 넘는 인라이닝이 가능합니다. 그런데 Clang의 Reduced BMI는 비-inline 함수와 변수의 정의를 BMI에 넣지 않으며, 문서는 Clang 22.x부터 Reduced BMI가 기본이라고 적고 있습니다. 정의가 BMI에 없으면 importer는 그 본문을 볼 수 없으므로, 헤더에서 선언만 보이던 함수와 같은 처지가 됩니다. 성능상 중요한 작은 함수는 명시적으로 `inline`으로 두거나, LTO로 링크 시점 인라이닝을 기대하는 설계가 필요합니다. 인라이닝이 실제로 일어났는지는 [챕터 05](/post/compiler-optimization/inlining-diagnostics/)의 리포트로 확인할 수 있습니다.

정리하면 "모듈로 바꾸면 빨라진다"도, "모듈은 성능과 무관하다"도 정확하지 않습니다. 실행 성능은 여전히 최적화 플래그와 LTO·PGO가 결정하지만, 모듈 전환이 인라이닝 가시성을 바꿀 수 있으므로 핫 경로 함수에 대해서는 전환 전후 벤치마크와 인라이닝 리포트를 비교해야 합니다.

## 모듈 작성과 빌드

모듈은 <strong>인터페이스 단위(module interface unit)</strong>에서 `export module`로 선언하고, 공개할 선언에 `export`를 붙입니다. 사용하는 쪽은 `import`로 인터페이스를 가져옵니다. 아래는 컴파일 가능한 최소 예제입니다.

```cpp
// math.cppm — 모듈 인터페이스 단위
export module math;

export int add(int a, int b) {
    return a + b;
}
```

```cpp
// main.cpp — 모듈 사용처 (모듈 단위가 아닌 일반 TU)
#include <iostream>
import math;

int main() {
    std::cout << add(2, 3) << '\n';
}
```

모듈 단위 안에서는 `#include`를 함부로 쓰면 안 된다는 점이 중요합니다. cppreference 문서는 모듈 단위에서 전역 모듈 조각(global module fragment, `module;`로 시작하는 영역) 밖에 `#include`를 쓰면 포함된 모든 선언이 모듈의 일부로 간주되므로 그렇게 하지 말라고 설명합니다. 헤더가 필요하면 `module;` 아래, `export module` 선언 위에 포함합니다. 위 `main.cpp`처럼 모듈 단위가 아닌 일반 TU에서는 `#include`와 `import`를 함께 쓸 수 있습니다.

컴파일러별 명령은 인터페이스를 먼저 컴파일해 BMI/CMI를 만들고, 그것을 참조하며 사용처를 컴파일하는 순서입니다. Clang 명령은 Clang 문서의 Quick Start 형식을 따랐습니다.

```bash
# Clang: 인터페이스를 precompile해 BMI(.pcm) 생성 후 사용처와 함께 빌드
clang++ -std=c++20 math.cppm --precompile -o math.pcm
clang++ -std=c++20 main.cpp -fmodule-file=math=math.pcm math.pcm -o app

# GCC: -std=c++20만으로는 모듈이 켜지지 않으므로 옵션을 명시
#      (GCC 14 매뉴얼은 -fmodules-ts, 최신 매뉴얼은 -fmodules)
#      CMI는 gcm.cache/에 생성되며, 인터페이스를 먼저 컴파일해야 함
g++ -std=c++20 -fmodules-ts -c math.cppm
g++ -std=c++20 -fmodules-ts math.o main.cpp -o app
```

GCC [C++ Modules 문서](https://gcc.gnu.org/onlinedocs/gcc/C_002b_002b-Modules.html)는 `-std=c++20`만으로는 모듈 컴파일이 켜지지 않으며 옵션으로 명시해야 한다고 설명합니다. MSVC는 `.ixx`를 모듈 인터페이스로 인식하고, 다른 확장자는 [`/interface` 옵션 문서](https://learn.microsoft.com/en-us/cpp/build/reference/interface)의 예처럼 `cl /c /std:c++latest /interface /TP my-module.cppm`으로 컴파일해 `.ifc`를 만듭니다. `/c`를 빼면 `main`이 없는 인터페이스를 링크하려다 실패합니다.

실제 프로젝트에서는 이 순서를 빌드 시스템에 맡기는 것이 안전합니다. [CMake의 cmake-cxxmodules 문서](https://cmake.org/cmake/help/latest/manual/cmake-cxxmodules.7.html)에 따르면 모듈 지원은 CMake 3.28에서 추가됐고, 소스 스캔을 지원하는 컴파일러는 MSVC 툴셋 14.34(Visual Studio 17.4) 이상, Clang 16 이상, GCC 14 이상입니다. 제너레이터는 Ninja(1.11 이상)와 Ninja Multi-Config, Visual Studio 17 2022 이후만 지원하므로, Linux 기본값인 Unix Makefiles로는 모듈 프로젝트를 빌드할 수 없습니다.

```cmake
cmake_minimum_required(VERSION 3.28)
project(modules_demo CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(app main.cpp)
target_sources(app
  PRIVATE
    FILE_SET CXX_MODULES FILES math.cppm)
```

`FILE_SET CXX_MODULES`에 인터페이스 단위를 등록하면 CMake가 소스를 스캔해 빌드 순서와 BMI 경로를 잡아 줍니다. 구성할 때는 제너레이터를 명시합니다.

```bash
cmake -S . -B build -G Ninja      # ninja 1.11 이상 필요
cmake --build build
```

## 도입 전략과 함정

대형 코드베이스를 한 번에 모듈로 바꾸는 것은 현실적이지 않습니다. 컴파일러·빌드 시스템·IDE·정적 분석 도구가 모두 모듈을 이해해야 하고, 서드파티 라이브러리 대부분은 여전히 헤더로 배포되기 때문입니다. 그래서 의존 그래프의 잎에 해당하는, 자주 포함되지만 자주 바뀌지 않는 자체 라이브러리부터 모듈로 감싸고, 서드파티 헤더는 전역 모듈 조각에서 포함하는 방식으로 시작하는 것이 일반적입니다. Clang 문서의 "Transitioning to modules" 절도 기존 헤더를 유지하면서 모듈 인터페이스로 감싸는 방식을 소개합니다.

전환 과정에서 자주 부딪히는 문제는 세 가지입니다. 첫째, BMI는 컴파일 옵션과 묶여 있습니다. Clang 문서는 BMI를 만들 때와 사용할 때 언어 방언에 영향을 주는 옵션이 다르면 오류가 나며, 최적화 수준처럼 방언과 무관한 옵션은 허용되지만 `NDEBUG` 같은 매크로 불일치는 현재 거부되지 않아 놀라운 결과를 낼 수 있다고 경고합니다. 따라서 빌드 캐시나 CI 아티팩트로 BMI를 재사용할 때는 컴파일러 버전과 옵션을 캐시 키에 넣어야 합니다. 둘째, 앞서 본 것처럼 BMI는 컴파일러 사이에 호환되지 않으므로, 여러 컴파일러로 빌드하는 CI에서는 컴파일러별로 따로 생성해야 합니다. 셋째, BMI에 정의가 빠지면서 인라이닝이 사라지는 경우로, 이것은 빌드가 깨지지 않고 성능만 조용히 바뀌므로 벤치마크로만 발견됩니다.

## 판단 기준: 언제 Modules를 도입할지

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 헤더 파싱이 빌드 시간을 지배하는 대형 프로젝트 | 잎 라이브러리부터 점진적 모듈화, `-O0`·`-O2` 모두 측정 | 디버그 빌드 측정만으로 효과 판단 |
| 빌드 환경 | CMake 3.28+·Ninja 1.11+·지원 컴파일러 확인 | Unix Makefiles 제너레이터로 시도 |
| 핫 경로 함수의 모듈 이전 | 전환 전후 벤치마크·인라이닝 리포트 비교, 필요시 `inline`·LTO | "모듈이면 빠르다"고 가정 |

## 자주 하는 실수

- **모듈 단위에서 전역 모듈 조각 밖에 `#include` 쓰기**: 포함한 헤더의 선언이 모두 모듈 소속이 되어 다른 TU의 같은 헤더와 충돌하거나 예상치 못한 export가 생긴다. 헤더는 `module;` 아래에서 포함한다.
- **BMI를 다른 옵션·컴파일러에서 재사용하기**: BMI는 컴파일러와 언어 옵션에 묶인 산출물이다. 캐시 키에 컴파일러 버전과 옵션을 넣고, 컴파일러별로 따로 만든다.
- **디버그 빌드의 개선 폭을 릴리즈에도 기대하기**: Clang 문서가 설명하듯 최적화 빌드에서는 import한 코드도 importer에서 다시 최적화되므로 빌드 시간 이득이 작아질 수 있다.

## 학습 성과 목표

이 챕터를 마치면 모듈을 "빌드가 빨라지는 기능"이 아니라 빌드 그래프와 인라이닝 가시성을 함께 바꾸는 설계 선택으로 평가할 수 있어야 합니다.

- 헤더 대비 모듈의 컴파일 작업량 모델(O(n·m) → O(n+m))과, 최적화 수준·빌드 순서 제약 때문에 실제 이득이 줄어드는 이유를 설명할 수 있다.
- BMI/CMI/.ifc의 역할과 Reduced BMI가 모듈 경계 너머의 인라이닝에 주는 영향을 설명할 수 있다.
- Clang·GCC·MSVC 명령과 CMake 3.28+(Ninja)로 모듈 프로젝트를 빌드하고, 점진적 도입의 함정을 피할 수 있다.

## 비판적 시각: 한계와 트레이드오프

모듈의 가장 큰 비용은 생태계 성숙도입니다. 빌드 시스템이 의존성 스캔을 지원해야 하고, IDE·정적 분석기·코드 생성 도구가 BMI를 이해해야 하며, 패키지 관리자가 모듈 인터페이스를 배포하는 방식도 아직 정착하지 않았습니다. 컴파일러마다 BMI 형식이 달라 미리 빌드한 모듈을 배포할 수 없으므로, 라이브러리는 결국 인터페이스 소스를 배포하고 사용자가 각자 빌드해야 합니다. 빌드 그래프에 순서 제약이 생겨 분산 빌드나 컴파일 캐시와의 궁합도 헤더 방식보다 복잡해집니다([챕터 12](/post/compiler-optimization/build-parallelization-ccache-distcc-sccache/) 참고). 이런 비용은 헤더 파싱이 빌드 시간의 대부분을 차지하는 프로젝트에서만 확실히 회수되므로, 도입 결정은 자신의 빌드 프로파일을 측정한 결과에 근거해야 합니다.

## 다음 장에서는

**빌드 병렬화**(ccache, sccache, distcc)와 CI 캐시·분산 전략을 다룹니다.

→ [빌드 병렬화 전략](/post/compiler-optimization/build-parallelization-ccache-distcc-sccache/) (챕터 12)
