---
collection_order: 10
date: 2026-03-11
lastmod: 2026-10-21
draft: false
image: wordcloud.png
title: "[Compiler 03] 디버그 정보와 릴리즈 성능"
slug: debug-info-and-release-performance
description: "심볼 테이블과 DWARF 디버그 정보의 차이, -g가 생성 코드를 바꾸지 않음을 확인하는 방법, -Og와 최적화 코드의 디버깅 품질, objcopy 심볼 분리·Split DWARF·perf 콜그래프 조건을 1차 문서와 실제 결과로 정리합니다."
tags:
  - C++
  - Performance(성능)
  - Optimization(최적화)
  - Compiler(컴파일러)
  - Debugging(디버깅)
  - Profiling(프로파일링)
  - Linux(리눅스)
  - Low-Level(로우레벨)
  - Assembly(어셈블리)
  - CI-CD(Continuous Integration/Continuous Deployment)
  - Reliability
  - Pitfalls(함정)
  - Best-Practices
  - Guide(가이드)
  - Reference(참고)
  - Tutorial(튜토리얼)
  - Advanced
  - Deep-Dive
  - 실습
  - Comparison(비교)
  - Open-Source(오픈소스)
  - Standard(표준)
  - GCC
  - Clang
  - DWARF
  - GDB
  - perf
  - CMake
---

릴리즈 바이너리에서도 크래시 덤프를 해석하고 프로파일러로 핫스팟의 소스 줄을 보려면 디버그 정보가 필요합니다. 그런데 "`-g`를 켜면 느려진다"는 오해와 "심볼이 없으면 함수 이름도 안 보인다"는 혼동 때문에, 릴리즈 빌드에서 디버그 정보를 빼 버리거나 반대로 무엇을 지워야 하는지 모른 채 배포하는 일이 흔합니다. 이 챕터에서는 디버그 정보가 바이너리 안에서 무엇인지, 코드 생성에 영향을 주는지를 실제 컴파일 결과로 확인하고, 최적화 코드의 디버깅 품질, 심볼 분리·Split DWARF·perf 워크플로를 정리합니다.

## 심볼 테이블과 디버그 정보는 다르다

ELF 실행 파일에서 "심볼"이라고 부르는 정보는 두 층으로 나뉩니다. 첫째는 **심볼 테이블**(`.symtab`)로, 함수와 전역 변수의 이름과 주소를 담습니다. 이것은 `-g`가 없어도 링커가 기본으로 남기며, `perf report`나 `gdb`가 함수 이름을 보여 주는 근거입니다. 둘째는 **디버그 정보**(DWARF)로, `-g`를 주었을 때 `.debug_info`, `.debug_line`, `.debug_abbrev` 같은 별도 섹션에 들어갑니다. 소스 파일과 줄 번호, 지역 변수와 그 위치, 타입, 인라인된 함수의 호출 관계가 여기에 담깁니다. [DWARF 표준](https://dwarfstd.org/)은 이 형식을 다음과 같이 소개합니다.

> "DWARF is a debugging information file format used by many compilers and debuggers to support source level debugging." — [DWARF Debugging Standard](https://dwarfstd.org/)

이 구분이 실무에서 중요한 이유는 제거 도구가 지우는 범위가 다르기 때문입니다. `strip`은 기본적으로 심볼 테이블까지 지우므로(`--strip-all`), 그 결과물에서는 프로파일러가 주소만 보여 줍니다. 반면 `objcopy --strip-debug`나 `strip --strip-debug`는 DWARF 섹션만 지우고 심볼 테이블은 남기므로, 함수 이름은 그대로 보이고 소스 줄과 변수 정보만 사라집니다. "디버그 정보를 지웠더니 프로파일이 주소만 나온다"는 경험은 대개 `--strip-all`을 썼기 때문입니다.

GCC는 디버그 정보의 양을 레벨로 조절합니다. [GCC Debugging Options](https://gcc.gnu.org/onlinedocs/gcc/Debugging-Options.html)에 따르면 기본 `-g`는 레벨 2로 지역 변수와 typedef까지 포함하고, `-g1`은 함수 설명과 외부 변수, 줄 번호 테이블만 담아 스택 추적에 충분한 최소 정보를 만들며, `-g3`는 매크로 정의까지 추가합니다. Clang의 `-gline-tables-only`도 줄 번호 테이블만 생성해 함수 이름·파일·줄이 들어간 스택 추적을 얻는 용도로, 프로덕션 크래시 분석에는 이 정도로 충분한 경우가 많습니다.

## `-g`는 생성 코드를 바꾸지 않는다

디버그 정보는 별도 섹션에 들어가는 메타데이터이므로, 같은 최적화 옵션에서 `-g`를 더해도 실행되는 기계어는 같아야 합니다. GCC는 이를 스스로 검증하는 옵션까지 제공합니다. [GCC Developer Options](https://gcc.gnu.org/onlinedocs/gcc/Developer-Options.html)의 `-fcompare-debug`는 컴파일을 한 번 더 하면서 기본적으로 `-g`를 토글하고, 두 컴파일의 최종 내부 표현이 다르면 오류를 냅니다. 즉 GCC는 "`-g` 여부가 코드 생성에 영향을 주면 버그"라는 기준으로 테스트됩니다.

아래 프로그램으로 직접 확인해 볼 수 있습니다. 이후의 perf 실습도 이 파일을 씁니다.

```cpp
// main.cc: 디버그 정보·심볼·perf 실습용 최소 프로그램
#include <cstdio>
#include <vector>

__attribute__((noinline))
long hot_function(const std::vector<int>& v) {
    long s = 0;
    for (int x : v) s += static_cast<long>(x) * x;   // 대부분의 시간이 여기서 소비됨
    return s;
}

__attribute__((noinline))
long cold_function(int n) {
    return n * 3L;
}

int main() {
    std::vector<int> v(1 << 20, 3);
    long total = 0;
    for (int rep = 0; rep < 200; ++rep) total += hot_function(v) + cold_function(rep);
    std::printf("%ld\n", total);
}
```

2026년 10월 [Compiler Explorer](https://godbolt.org)의 x86-64 gcc 14.2에서 이 파일을 `-O2`와 `-O2 -g`로 각각 컴파일해 어셈블리를 비교하면 명령이 한 줄도 다르지 않았고, `-O2 -fcompare-debug`도 오류 없이 끝났습니다. 로컬에서는 다음처럼 두 오브젝트의 `.text` 섹션만 뽑아 비교할 수 있습니다.

```bash
g++ -O2    -c main.cc -o nodbg.o
g++ -O2 -g -c main.cc -o dbg.o
objcopy -O binary --only-section=.text nodbg.o nodbg.text
objcopy -O binary --only-section=.text dbg.o   dbg.text
cmp nodbg.text dbg.text && echo "같은 기계어"
```

예외는 빌드 시스템 쪽에서 생깁니다. 대표적인 예가 CMake의 기본 빌드 타입입니다. CMake의 GNU 컴파일러 설정 파일(`Modules/Compiler/GNU.cmake`)은 `Release`에 `-O3`를, `RelWithDebInfo`에 `-O2 -g`를 기본 플래그로 지정합니다. 그래서 `Release`와 `RelWithDebInfo`를 비교하면 `-g`의 효과가 아니라 **`-O3`와 `-O2`의 차이**를 재게 됩니다. 디버그 정보가 성능에 영향을 주는지 확인하려면 최적화 플래그를 명시적으로 같게 맞춘 두 빌드를 비교해야 합니다.

## 최적화 코드의 디버깅 품질

`-g`가 코드를 바꾸지 않는다는 것은 반대로 말하면 **최적화가 디버깅 경험을 바꾼다**는 뜻이기도 합니다. GCC 매뉴얼은 `-g`와 `-O`를 함께 쓸 수 있다고 하면서, 최적화된 코드에서는 선언한 변수가 아예 존재하지 않거나, 실행 흐름이 예상치 못한 곳으로 잠시 이동하거나, 루프 밖으로 옮겨진 문장이 다른 위치에서 실행될 수 있다고 경고합니다. gdb에서 지역 변수를 출력했을 때 `<optimized out>`이 나오는 것이 이 경우로, 변수가 레지스터에만 잠시 존재했다가 사라졌거나 계산 자체가 다른 식에 합쳐졌다는 뜻입니다.

GCC는 이 절충을 위해 `-Og`를 제공합니다. [GCC Optimize Options](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html)는 `-Og`를 디버깅 경험을 고려하며 최적화하는 수준으로, 일반적인 편집-컴파일-디버그 주기에 권하는 선택이라고 설명합니다. 따라서 개발 중 디버깅에는 `-Og -g`, 릴리즈와 프로덕션 크래시 분석에는 `-O2 -g`(또는 `-g1`·`-gline-tables-only`)처럼 목적에 따라 나누는 것이 현실적입니다. 릴리즈 빌드의 크래시 덤프에서 변수 값이 일부 `<optimized out>`으로 보이는 것은 정상이며, 그 대가로 실제 배포된 코드와 똑같은 바이너리를 분석할 수 있다는 점이 더 중요합니다.

## 릴리즈 빌드에서 심볼을 보관하는 방법

프로덕션 크래시를 분석하려면 배포한 바이너리와 정확히 같은 빌드의 디버그 정보가 있어야 합니다. 그렇다고 디버그 정보를 배포 바이너리에 넣어 두면 파일이 커지고 내부 구조가 노출되므로, 빌드 시 `-O2 -g`로 만든 뒤 디버그 정보만 별도 파일로 떼어 보관하는 방식을 씁니다. [GNU objcopy 문서](https://sourceware.org/binutils/docs/binutils/objcopy.html)가 설명하는 표준 절차는 세 단계입니다.

```bash
# (1) 디버그 섹션만 남긴 별도 파일 생성
objcopy --only-keep-debug app app.debug
# (2) 배포용 바이너리에서 디버그 섹션 제거 (심볼 테이블은 유지)
objcopy --strip-debug app
# (3) 배포용 바이너리에 디버그 파일 이름과 체크섬을 기록
objcopy --add-gnu-debuglink=app.debug app
```

`--only-keep-debug`는 디버그 섹션만 남기고 나머지 섹션은 헤더만 보존해, 나중에 도구가 디버그 파일과 실행 파일을 짝지을 수 있게 합니다. 2단계에서 `--strip-debug` 대신 `--strip-all`을 쓰면 배포 파일이 더 작아지지만, 심볼 테이블까지 사라져 디버그 파일 없이 받은 프로파일은 주소만 보이게 됩니다. 3단계의 debuglink가 있으면 gdb는 [별도 디버그 파일 규칙](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Separate-Debug-Files.html)에 따라 같은 디렉터리나 전역 디버그 디렉터리에서 `app.debug`를 찾아 씁니다. 같은 문서가 설명하는 build ID 방식(`.build-id` 하위 디렉터리)을 쓰면 파일 이름이 바뀌어도 정확한 빌드를 찾을 수 있어, 여러 버전을 보관하는 심볼 서버에 적합합니다.

## Split DWARF로 링크 부담 줄이기

대형 프로젝트에서는 디버그 정보가 오브젝트 파일의 대부분을 차지해, 링커가 이를 모두 읽고 합치는 데 시간과 메모리를 씁니다. GCC 문서의 `-gsplit-dwarf`는 디버그 정보를 가능한 한 많이 확장자 `.dwo`인 별도 파일로 빼서, 빌드 시스템이 디버그 정보를 링크하지 않아도 되게 하는 옵션입니다. 대신 `.dwo`를 읽을 수 있는 디버거가 필요합니다.

```bash
# 컴파일: foo.o에는 코드와 작은 연결 정보, foo.dwo에는 상세 디버그 정보
g++ -O2 -g -gsplit-dwarf -c foo.cc -o foo.o
# 링크: .dwo는 링크 입력이 아니므로 링커가 처리할 디버그 데이터가 줄어든다
g++ -O2 foo.o -o app
```

`-gsplit-dwarf`만으로는 디버그 정보가 켜지지 않는 GCC 버전이 있으므로 `-g`를 함께 명시하는 편이 안전합니다. 실행 파일에는 각 `.dwo`의 이름과 경로가 기록되므로, 빌드 디렉터리 그대로라면 gdb가 `.dwo`를 찾아 읽습니다. 하지만 CI 산출물로 보관하거나 다른 머신에서 분석하려면 흩어진 `.dwo`를 `dwp` 도구로 하나의 `.dwp` 패키지로 묶어 실행 파일과 함께 보관해야 합니다. 이 단계를 빠뜨리면 빌드 디렉터리가 지워진 뒤에는 디버그 정보를 되찾을 수 없습니다.

## perf와 심볼: 무엇에 무엇이 필요한가

샘플링 프로파일러 `perf`로 핫스팟을 찾을 때 필요한 정보는 보고 싶은 것에 따라 다릅니다. 함수별 비율(`perf report`)은 심볼 테이블만 있으면 되고, 디스어셈블리 위에 샘플 비율을 표시하는 `perf annotate`도 디버그 정보 없이 동작합니다. 디버그 정보가 필요한 것은 annotate 화면에 **소스 줄**을 섞어 보여 주거나, 인라인된 함수를 원래 함수 이름으로 풀어 보여 줄 때입니다.

```bash
g++ -O2 -g main.cc -o app
perf record -g ./app          # -g: 콜그래프 기록 (컴파일러 -g와 다른 옵션)
perf report                   # 함수별 비율 (심볼 테이블로 충분)
perf annotate hot_function    # 명령별 비율, -g 빌드면 소스 줄도 표시
```

여기서 흔한 함정은 `perf record -g`의 `-g`가 컴파일러의 `-g`와 전혀 다른 옵션이라는 점입니다. [perf-record 매뉴얼](https://man7.org/linux/man-pages/man1/perf-record.1.html)에 따르면 이 옵션은 콜그래프(호출 스택) 기록을 켜고, 사용자 공간의 기본 스택 해석 방식은 프레임 포인터(`fp`)입니다. 그런데 GCC는 `-O1` 이상에서 `-fomit-frame-pointer`를 켜므로, 일반 릴리즈 빌드를 기본 방식으로 기록하면 호출 스택이 잘려 보입니다. 같은 매뉴얼은 이런 경우 `--call-graph dwarf`를 쓰라고 안내하는데, 이 방식은 스택 일부를 복사해 DWARF의 호출 프레임 정보로 해석하므로 디버그 정보(또는 최소한 `.eh_frame`)가 있어야 하고 기록 데이터가 커집니다. 다른 방법은 빌드에 `-fno-omit-frame-pointer`를 주는 것으로, 레지스터 하나를 프레임 포인터로 묶어 두는 작은 성능 비용을 받아들이는 대신 가벼운 `fp` 방식을 그대로 쓸 수 있게 합니다.

## PGO·LTO와 디버그 정보

PGO에서 디버그 정보가 필요한지는 방식에 따라 다릅니다. 계측 기반 PGO(`-fprofile-generate`/`-fprofile-use`)는 컴파일러가 삽입한 카운터가 프로파일을 코드 구조에 직접 연결하므로 `-g`가 없어도 됩니다. 반면 샘플링 기반 AutoFDO는 `perf`로 수집한 명령 주소를 소스 줄로 되돌려 매핑해야 하므로, 프로파일을 수집하는 바이너리에 줄 번호 테이블이 필요합니다([챕터 15](/post/compiler-optimization/autofdo-workflow-sampling-based/) 참고). LTO 빌드에서 `-g`를 쓰면 디버그 정보도 링크 시점 최적화를 거쳐 합쳐지므로 링크 시간과 메모리가 늘어날 수 있습니다. 이 경우에도 생성 코드에 대한 원칙은 같고, 늘어나는 것은 빌드 비용입니다.

## 판단 기준: 빌드 목적별 디버그 정보

| 목적 | 권장 | 비권장 |
|------|------|--------|
| 개발 중 디버깅 | `-Og -g` | `-O2`에서 변수 값이 안 보인다고 `-O0`으로 성능 측정 |
| 릴리즈 + 크래시 분석 | `-O2 -g` 빌드 후 `--only-keep-debug`로 분리 보관 | 디버그 정보 없이 빌드해 사후 분석 불가 |
| 프로덕션 프로파일링 | 심볼 테이블 유지(`--strip-debug`), 콜그래프는 `--call-graph dwarf` 또는 `-fno-omit-frame-pointer` | `--strip-all` 바이너리로 프로파일 |
| `-g` 성능 영향 확인 | 최적화 플래그를 같게 맞춘 두 빌드 비교 | CMake `Release`와 `RelWithDebInfo` 비교 |

## 자주 하는 실수

- **`-g`가 성능을 낮춘다고 생각하기**: 같은 최적화 플래그라면 생성 코드는 같다. 차이가 보인다면 CMake 빌드 타입처럼 다른 플래그가 함께 바뀐 것이다.
- **함수 이름이 보이려면 `-g`가 필요하다고 생각하기**: 함수 이름은 심볼 테이블에서 온다. `-g`가 더하는 것은 소스 줄, 지역 변수, 타입, 인라인 정보다.
- **`perf record -g`가 디버그 정보를 쓴다고 생각하기**: perf의 `-g`는 콜그래프 기록이며 기본은 프레임 포인터 방식이다. 프레임 포인터가 생략된 릴리즈 빌드에서는 `--call-graph dwarf`나 `-fno-omit-frame-pointer`가 필요하다.

## 학습 성과 목표

이 챕터를 마치면 디버그 정보를 성능 문제가 아니라 빌드·배포 설계의 문제로 다룰 수 있어야 합니다. 구체적으로는 다음 세 가지입니다.

- 심볼 테이블과 DWARF 디버그 정보의 차이, `-g` 레벨과 `--strip-debug`/`--strip-all`의 범위를 설명할 수 있다.
- `-fcompare-debug`나 `.text` 비교로 `-g`가 생성 코드를 바꾸지 않음을 확인하고, `-Og`와 `-O2 -g`를 목적에 맞게 고를 수 있다.
- `objcopy` 분리·debuglink·Split DWARF·`dwp`로 릴리즈 심볼을 보관하고, perf 콜그래프에 필요한 조건을 갖출 수 있다.

## 비판적 시각: 한계와 트레이드오프

`-g`가 실행 코드를 바꾸지 않는다고 해서 비용이 없는 것은 아닙니다. 디버그 정보는 컴파일·링크 시간과 메모리를 늘리고, 빌드 캐시와 CI 산출물 저장 공간을 차지하며, 심볼 서버를 운영하는 수고가 따릅니다. Split DWARF는 링크 비용을 줄이는 대신 `.dwo`와 `.dwp`를 관리하는 절차를 하나 더 만듭니다. 또 최적화된 코드의 디버그 정보는 본질적으로 불완전해서, `-O2 -g` 크래시 덤프에서 원하는 변수가 `<optimized out>`인 경우가 흔합니다. 프로파일링을 위해 `-fno-omit-frame-pointer`를 켜는 결정은 반대로 작지만 실제 실행 비용을 받아들이는 선택이므로, 자신의 워크로드에서 측정해 보고 정해야 합니다. 디버그 정보 전략은 "켤까 말까"가 아니라 이런 비용을 어디에 지불할지 정하는 일입니다.

## 다음 장에서는

**C++20 Modules**가 빌드 시간과 런타임에 미치는 영향, 도입 단계별 전략을 다룹니다.

→ [C++20 Modules](/post/compiler-optimization/cpp20-modules-build-performance/) (챕터 11)
