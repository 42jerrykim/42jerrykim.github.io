---
collection_order: 12
date: 2026-03-11
lastmod: 2026-10-21
draft: false
image: wordcloud.png
title: "[Compiler 03] 빌드 병렬화: ccache, distcc, sccache"
slug: build-parallelization-ccache-distcc-sccache
description: "ccache의 해시 구성과 direct·preprocessor 모드, sccache 원격 캐시, distcc의 로컬 전처리·원격 컴파일 구조에서 올바른 설정을 이끌어 내고, 측정 기반 -j 결정과 GitHub Actions 캐시 키·CCACHE_DIR 구성을 다룹니다."
tags:
  - C++
  - Performance(성능)
  - Optimization(최적화)
  - Compiler(컴파일러)
  - CI-CD(Continuous Integration/Continuous Deployment)
  - Automation(자동화)
  - Linux(리눅스)
  - Memory(메모리)
  - Cache
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
  - GCC
  - Clang
  - CMake
  - Ninja
  - ccache
  - sccache
  - distcc
  - GitHub-Actions
  - Build-System
---

C++ 빌드 시간을 줄이는 방법은 크게 세 갈래입니다. 이미 한 번 한 컴파일을 다시 하지 않거나(캐시), 남은 컴파일을 한 머신의 코어에 고르게 나누거나(병렬 `-j`), 여러 머신에 나눠 보내는 것(분산)입니다. 이 챕터에서는 ccache·sccache·distcc가 각각 어떤 원리로 동작하는지, 그 원리에서 나오는 올바른 설정과 흔한 오해, 그리고 CI에서 이들을 조합하는 방법을 다룹니다. 빌드 시스템 설계 자체는 이 트랙의 범위 밖이므로, 여기서는 도구 적용에 집중합니다.

## ccache: 같은 컴파일을 다시 하지 않기

[ccache 공식 사이트](https://ccache.dev/)는 이 도구를 다음과 같이 소개합니다.

> "Ccache is a compiler cache. It speeds up recompilation by caching previous compilations and detecting when the same compilation is being done again." — [ccache](https://ccache.dev/)

핵심은 "같은 컴파일"을 어떻게 알아보느냐입니다. ccache는 컴파일러 호출을 가로채 입력을 해시하고, 같은 해시의 결과가 캐시에 있으면 컴파일러를 실행하지 않고 저장된 오브젝트를 돌려줍니다. [ccache 매뉴얼](https://ccache.dev/manual/latest.html)에 따르면 해시에는 항상 컴파일러의 이름과 크기·수정 시각(또는 `compiler_check`로 지정한 정보)이 들어갑니다. 여기에 더해 기본인 **direct 모드**는 입력 소스 파일과 컴파일러 옵션을 해시하고, 그 해시로 찾은 "manifest"에 기록된 포함 파일들의 해시까지 일치해야 결과를 재사용합니다. direct 모드에서 찾지 못하면 **preprocessor 모드**로 넘어가 컴파일러를 `-E`로 실행해 전처리 결과와 명령줄 옵션을 해시합니다. direct 모드는 전처리기 실행 비용을 아끼므로 더 빠르고, preprocessor 모드는 포함 파일 경로가 바뀐 경우처럼 direct 모드가 놓친 일치를 잡아냅니다.

이 구조에서 중요한 결론이 하나 나옵니다. 컴파일 옵션과 컴파일러 자체가 해시에 들어가므로, `-O2`와 `-O3`, LTO를 켠 빌드와 끈 빌드가 같은 캐시 디렉터리를 써도 **서로의 오브젝트를 잘못 재사용하지 않습니다**. 플래그가 다르면 해시가 달라 그냥 miss가 날 뿐입니다. 그래서 캐시를 구성별로 나누는 이유는 정확성이 아니라 hit율과 용량 관리입니다.

설정은 컴파일러 앞에 ccache를 끼우는 것으로 끝납니다. CMake에서는 `CMAKE_CXX_COMPILER_LAUNCHER`로 모든 컴파일 호출을 감쌉니다.

```bash
# 캐시 위치를 먼저 정한 뒤 크기를 설정 (설정은 해당 캐시 디렉터리에 기록됨)
export CCACHE_DIR=$HOME/.ccache
ccache --max-size=10G            # 기본값은 5GiB

# CMake 빌드에 ccache를 런처로 연결
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_CXX_COMPILER_LAUNCHER=ccache
cmake --build build
```

순서가 중요합니다. 매뉴얼에 따르면 `CCACHE_DIR`을 지정하지 않으면 캐시 위치는 `$HOME/.ccache`가 이미 있을 때만 그곳이고, 없으면 Linux에서는 `$HOME/.cache/ccache`입니다. `--max-size`를 먼저 실행하고 나중에 `CCACHE_DIR`을 바꾸면 크기 설정이 다른 디렉터리에 기록되어, 실제로 쓰는 캐시는 기본값 5GiB로 남습니다.

캐시가 실제로 효과를 내는지는 통계로 확인합니다. 빌드 전에 `ccache -z`로 통계를 초기화하고, 빌드 후 `ccache -s`를 보면 됩니다. ccache 4.x의 `-s` 출력은 "Cacheable calls" 아래에 Hits(그중 Direct·Preprocessed)와 Misses의 개수와 비율을, 이어서 Uncacheable calls와 캐시 크기를 보여 줍니다. hit 비율이 낮다면 원인은 대개 세 가지입니다. 플래그가 빌드마다 바뀌거나, `__DATE__`·`__TIME__`처럼 결과를 바꾸는 요소가 있거나, CI 체크아웃 경로가 매번 달라 절대 경로가 해시에 섞이는 경우입니다. 마지막 경우에는 매뉴얼의 `base_dir`(`CCACHE_BASEDIR`)을 체크아웃 루트로 지정하면, ccache가 그 아래의 절대 경로를 상대 경로로 바꿔 해시하므로 디렉터리가 달라도 캐시를 공유할 수 있습니다.

## sccache: 원격 저장소에 둔 공유 캐시

[sccache](https://github.com/mozilla/sccache)는 ccache와 같은 개념의 컴파일러 캐시이지만, 캐시를 로컬 디스크뿐 아니라 S3·GCS 같은 원격 저장소에 둘 수 있다는 점이 다릅니다. 여러 CI 러너나 개발자가 같은 저장소를 공유하면, 한 곳에서 컴파일한 결과를 다른 곳에서 바로 받아 쓸 수 있습니다. S3 백엔드는 [sccache 문서](https://github.com/mozilla/sccache/blob/main/docs/S3.md)대로 `SCCACHE_BUCKET`과 `SCCACHE_REGION` 환경 변수로 지정합니다.

```bash
export SCCACHE_BUCKET=my-build-cache
export SCCACHE_REGION=ap-northeast-2
cmake -S . -B build -G Ninja -DCMAKE_CXX_COMPILER_LAUNCHER=sccache
cmake --build build
sccache --show-stats
```

원격 캐시는 매 빌드가 깨끗한 환경에서 시작하는 CI에서 특히 유리하지만, hit이 나도 네트워크로 오브젝트를 내려받는 시간이 들고 저장소 비용과 접근 권한 관리가 따라옵니다. 같은 러너가 반복해서 빌드하는 환경이라면 로컬 ccache와 CI 캐시 복원만으로 충분한 경우가 많습니다.

## distcc: 컴파일을 다른 머신에 보내기

캐시는 이미 한 컴파일만 줄여 줍니다. 처음 빌드하거나 많은 파일이 바뀐 경우에는 실제로 컴파일할 작업 자체가 많으므로, 그 작업을 여러 머신에 나누는 분산 빌드가 필요합니다. [distcc](https://www.distcc.org/)는 각 작업의 전처리를 로컬에서 끝낸 뒤 완전히 전처리된 소스를 네트워크로 보내고, 원격 머신은 컴파일만 해서 오브젝트를 돌려줍니다. 그래서 distcc 공식 사이트가 설명하듯 참여 머신들은 파일 시스템을 공유하거나 같은 헤더·라이브러리를 설치할 필요가 없고, `distccd` 데몬과 적절한 컴파일러만 있으면 됩니다. 원격 컴파일러 버전이 로컬과 다르면 생성 코드가 달라질 수 있으므로 같은 버전을 맞추는 것이 실무상 중요합니다. 전처리 자체가 병목이 되는 큰 프로젝트를 위해 헤더를 함께 보내 원격에서 전처리하는 pump 모드도 있습니다.

ccache와 함께 쓸 때는 [ccache 매뉴얼](https://ccache.dev/manual/latest.html)이 권하는 방식대로 `CCACHE_PREFIX`에 distcc를 지정합니다. 그러면 ccache가 먼저 캐시를 확인하고, miss인 경우에만 `distcc 컴파일러 ...` 형태로 실행하므로, hit은 로컬에서 즉시 끝나고 실제 컴파일이 필요한 작업만 원격으로 나갑니다.

```bash
export DISTCC_HOSTS="localhost node1 node2 node3"
export CCACHE_PREFIX=distcc        # 캐시 miss만 distcc로 분산
cmake -S . -B build -G Ninja -DCMAKE_CXX_COMPILER_LAUNCHER=ccache
cmake --build build -j 32          # 로컬+원격 슬롯 합계에 맞춘 값
```

distcc는 컴파일만 분산하므로 전처리와 링크는 여전히 로컬에서 일어납니다. 그래서 노드를 아무리 늘려도 로컬 전처리 속도와 링크 시간, 네트워크 대역폭이 상한이 됩니다. 원격 노드가 많을수록 로컬 머신의 전처리 부담이 병목으로 드러나는 경우가 많습니다.

## 병렬 작업 수(-j) 정하기

`make -j N`이나 `ninja -j N`의 N은 동시에 실행할 컴파일러 프로세스 수입니다. 기본 출발점은 논리 코어 수이며, [Ninja 매뉴얼](https://ninja-build.org/manual.html)대로 Ninja는 별도 지정이 없으면 시스템의 CPU 수에 따라 병렬로 빌드합니다. 문제는 메모리입니다. 컴파일러 프로세스 하나가 쓰는 메모리는 TU 크기·템플릿 사용량·최적화 수준에 따라 크게 달라지고, LTO 링크 단계는 특히 많이 씁니다. N개 프로세스의 메모리 합이 물리 메모리를 넘으면 스왑이 일어나 오히려 느려지거나, 메모리 부족으로 컴파일러가 강제 종료되어 빌드가 실패합니다.

추측 대신 측정으로 정하는 편이 안전합니다. 가장 무거운 TU 몇 개를 `/usr/bin/time -v`로 컴파일해 "Maximum resident set size"를 확인하면 작업당 최대 메모리를 알 수 있고, 가용 메모리를 그 값으로 나눈 수와 코어 수 중 작은 값을 N의 상한으로 잡을 수 있습니다. 같은 매뉴얼의 pool 기능은 큰 실행 파일의 링크처럼 비싼 규칙의 동시 실행 수만 따로 제한하는 용도로 설명되어 있으므로, 컴파일은 코어 수만큼 돌리고 LTO 링크는 1–2개로 묶는 식의 조정이 가능합니다. CI 러너는 사양이 고정되어 있으므로 한 번 측정한 값을 고정해 두면 됩니다.

## CI에서의 캐시 전략

CI 러너는 보통 매번 깨끗한 환경에서 시작하므로, 캐시 디렉터리를 다음 실행으로 넘기지 않으면 매 빌드가 처음부터 다시 컴파일됩니다. GitHub Actions에서는 `actions/cache`로 ccache 디렉터리를 저장·복원합니다. 이때 알아야 할 동작이 두 가지 있습니다. [GitHub 문서](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching)에 따르면 기존 캐시 항목의 내용은 바꿀 수 없고 새 키로 새 항목을 만들어야 하며, `key`가 정확히 일치하지 않으면 `restore-keys`에 나열한 접두사로 가장 가까운 항목을 순서대로 찾아 복원합니다.

그래서 키 끝에 커밋 해시를 붙여 매 실행이 새 항목으로 저장되게 하고, 복원은 `restore-keys`의 접두사로 직전 캐시를 가져오는 패턴을 씁니다. 키 앞부분에 컴파일러·빌드 타입·OS를 넣는 이유는 앞에서 본 것처럼 정확성 때문이 아닙니다. 서로 다른 구성이 같은 접두사를 공유하면 Release 빌드가 Debug 빌드의 캐시를 복원해 hit이 거의 나지 않거나, 여러 구성이 한 캐시를 번갈아 덮어쓰며 용량 제한으로 유용한 항목이 퇴출되기 때문입니다.

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    env:
      CCACHE_DIR: ${{ github.workspace }}/.ccache   # 캐시 경로를 명시해 path와 일치
      CCACHE_BASEDIR: ${{ github.workspace }}       # 체크아웃 경로 차이 흡수
    steps:
      - uses: actions/checkout@v4
      - name: Restore ccache
        uses: actions/cache@v4
        with:
          path: .ccache
          # 구성별로 키를 나눠 hit율을 지키고, 커밋 해시로 매 실행 새 항목 저장
          key: ccache-${{ runner.os }}-gcc14-Release-${{ github.sha }}
          restore-keys: |
            ccache-${{ runner.os }}-gcc14-Release-
      - run: |
          sudo apt-get install -y ccache ninja-build
          ccache -z
          cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release \
                -DCMAKE_CXX_COMPILER_LAUNCHER=ccache
          cmake --build build
          ccache -s
```

`CCACHE_DIR`을 명시하지 않으면 새 러너에는 `~/.ccache`가 없으므로 ccache가 `~/.cache/ccache`를 써서, `path`에 적은 디렉터리와 실제 캐시 위치가 어긋나 아무것도 저장되지 않습니다. 빌드 전후의 `ccache -z`와 `ccache -s`는 이 설정이 실제로 hit을 만들고 있는지 매 실행 로그에 남겨 줍니다. 여러 컴파일러를 빌드 매트릭스로 돌린다면 키의 컴파일러 부분을 매트릭스 변수로 바꾸면 됩니다. 매트릭스로 여러 구성을 병렬로 돌리고 각 구성은 자기 캐시를 쓰는 방식이, CI에 distcc 노드 풀을 운영하는 것보다 대부분의 프로젝트에서 단순합니다.

## 판단 기준: 무엇을 쓸지

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 로컬 반복 빌드·소량 변경 | ccache | 매번 클린 빌드 |
| 여러 CI 러너·개발자 간 공유 | sccache 원격 캐시 또는 CI 캐시 복원 | 러너마다 처음부터 컴파일 |
| 클린 빌드가 잦은 대형 프로젝트 | distcc(+ccache `CCACHE_PREFIX`) | 로컬 코어만으로 버티기 |
| 병렬 작업 수 | 무거운 TU의 최대 메모리를 측정해 상한 결정, LTO 링크는 별도 제한 | 측정 없이 큰 `-j` |

## 자주 하는 실수

- **CI 캐시 키에 플래그를 안 넣으면 잘못된 오브젝트가 재사용된다고 생각하기**: ccache와 sccache는 컴파일러와 옵션을 자체 해시에 넣으므로 오염은 일어나지 않는다. 키를 구성별로 나누는 목적은 hit율과 용량 관리다.
- **distcc 노드에 소스와 헤더가 있어야 한다고 생각하기**: 기본 모드는 로컬에서 전처리한 소스를 보내므로 원격에는 같은 버전의 컴파일러와 `distccd`만 있으면 된다.
- **`-j`는 클수록 빠르다고 생각하기**: 메모리 합이 물리 메모리를 넘는 순간 스왑이나 OOM으로 오히려 느려지거나 실패한다. 작업당 메모리를 측정해 상한을 정한다.

## 학습 성과 목표

이 챕터를 마치면 "캐시를 켜면 빨라진다" 수준을 넘어, 도구가 동작하는 원리에서 설정을 이끌어 낼 수 있어야 합니다.

- ccache의 direct·preprocessor 모드와 해시 구성을 설명하고, 그로부터 캐시 공유가 안전한 이유와 hit율이 떨어지는 원인을 진단할 수 있다.
- sccache 원격 캐시와 distcc 분산 컴파일의 구조(로컬 전처리 후 원격 컴파일)와 한계를 비교할 수 있다.
- GitHub Actions에서 `CCACHE_DIR`·`CCACHE_BASEDIR`·캐시 키·`restore-keys`를 올바르게 구성하고, 측정에 근거해 `-j`를 정할 수 있다.

## 비판적 시각: 한계와 트레이드오프

캐시와 분산은 컴파일 단계만 빠르게 합니다. 링크, 특히 LTO 링크는 캐시되지 않고 분산되지도 않으므로, 컴파일이 빨라질수록 링크가 전체 빌드 시간에서 차지하는 비중이 커집니다. 캐시는 또 "같은 컴파일"이 반복될 때만 효과가 있어서, 공통 헤더 하나를 고치면 그 헤더를 포함하는 모든 TU가 miss가 됩니다. 이 경우에는 캐시보다 헤더 의존성을 줄이는 설계나 [C++20 Modules](/post/compiler-optimization/cpp20-modules-build-performance/)가 근본적인 해결책에 가깝습니다. 원격 캐시와 분산 빌드는 저장소·네트워크·노드 운영 비용과 보안 관리(누가 캐시에 쓸 수 있는가)를 함께 가져오므로, 도입 전에 현재 빌드에서 컴파일·링크·대기가 각각 몇 초인지 먼저 측정해 어디에 투자할지 정하는 것이 합리적입니다.

## 다음 장에서는

**정적 분석기**(Clang Static Analyzer, GCC -fanalyzer)와 성능 관련 경고, CI 연계를 다룹니다.

→ [Static Analyzer](/post/compiler-optimization/static-analyzer-performance/) (챕터 13)
