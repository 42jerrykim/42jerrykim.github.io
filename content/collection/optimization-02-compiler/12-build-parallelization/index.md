---
collection_order: 12
date: 2026-03-11
lastmod: 2026-06-01
draft: true
title: "[Compiler 02] 빌드 병렬화: ccache, distcc, sccache"
slug: build-parallelization-ccache-distcc-sccache
description: "ccache·sccache로 재컴파일 감소, distcc 분산 빌드, -j와 메모리·캐시 균형, CI에서의 캐시 아티팩트·캐시 키·분산 전략을 다룹니다. LTO·PGO와 캐시 키 관계와 언제 ccache/distcc를 쓸지 판단 기준을 제시합니다."
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

빌드 시간을 줄이려면 캐시와 병렬·분산이 필수입니다. 이 챕터에서는 ccache, sccache, distcc와 CI 전략을 다룹니다.

## ccache / sccache로 재컴파일 감소

> "Ccache is a compiler cache. It speeds up recompilation by caching previous compilations and detecting when the same compilation is being done again." — [ccache 공식 문서](https://ccache.dev/)

**ccache**는 컴파일러(gcc, g++, clang 등)를 감싸서, **동일한 소스·플래그**로 컴파일할 때 이전 결과를 재사용합니다. 캐시 hit이 나면 컴파일을 건너뛰고 이전 오브젝트를 복사하므로, 변경이 적은 TU는 거의 즉시 끝나고 **전체 빌드 시간**이 크게 줄어듭니다. 재빌드·CI에서 코드가 조금만 바뀌었을 때 효과가 큽니다.

**sccache**는 비슷한 개념으로, 캐시를 **로컬**뿐 아니라 **S3, GCS** 등 원격 저장소에 두어 여러 머신·CI 노드가 공유할 수 있게 합니다. 분산 팀이나 CI 팜에서 "다른 브랜치/다른 머신이 이미 같은 TU를 컴파일해 두었으면 그걸 쓰자"라는 전략에 적합합니다. ccache와 마찬가지로 **캐시 키**에는 소스 해시·컴파일러·플래그가 포함되어야 하므로, LTO·PGO 등 플래그가 다른 빌드와는 캐시가 공유되지 않습니다.

ccache는 컴파일러 앞에 끼워 넣어 사용합니다. CMake에서는 `CMAKE_CXX_COMPILER_LAUNCHER`로 모든 컴파일 호출을 ccache로 감쌀 수 있습니다.

```bash
# ccache 설치 후 캐시 크기·경로 설정
ccache --max-size=10G
export CCACHE_DIR=$HOME/.ccache

# CMake 빌드에 ccache를 런처로 연결
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_CXX_COMPILER_LAUNCHER=ccache
cmake --build build -j$(nproc)

# sccache는 원격 백엔드(S3 등)를 환경 변수로 지정
export SCCACHE_BUCKET=my-build-cache SCCACHE_REGION=ap-northeast-2
cmake -S . -B build -DCMAKE_CXX_COMPILER_LAUNCHER=sccache
```

캐시 효과는 `ccache -s` 통계로 확인합니다. hit률이 낮으면 플래그가 자주 바뀌거나 클린 빌드가 많은 것이므로, 캐시 키 구성을 점검합니다.

```text
$ ccache -s
cache hit (direct)                  1842
cache hit (preprocessed)             137
cache miss                           421
cache hit rate                     82.45 %
cache size                          3.1 GB / 10.0 GB
```

## distcc 등 분산 빌드

**distcc**는 컴파일 **작업**을 여러 머신에 나눠 보냅니다. 한 머신이 make -j를 돌리면, 로컬뿐 아니라 distcc로 연결된 원격 노드들도 컴파일 작업을 받아 수행하고, 생성된 오브젝트를 돌려줍니다. 단일 머신의 코어 수보다 **총 컴파일 노드 수**가 많으면 이론상 빌드 시간을 더 줄일 수 있습니다. 네트워크 지연·공유 스토리지(소스/인클루드 경로) 설정이 필요하고, Windows 지원은 제한적일 수 있습니다. **Icecream** 등 대안도 있으며, 개념은 비슷합니다.

distcc는 참여 노드를 환경 변수로 지정하고, ccache와 함께 쓰려면 `CCACHE_PREFIX=distcc`로 캐시 미스만 분산에 보냅니다. 이렇게 하면 캐시 hit는 로컬에서 즉시 끝나고, 실제 컴파일이 필요한 작업만 원격으로 나갑니다.

```bash
# 분산 노드 목록 지정 후, 노드 총합에 맞춰 -j를 크게 설정
export DISTCC_HOSTS="localhost node1 node2 node3"
export CCACHE_PREFIX=distcc        # 캐시 미스만 distcc로 분산
cmake --build build -j40           # 노드 총 코어 수에 맞춰 크게
```

분산 빌드는 **캐시가 잘 안 먹는** 클린 빌드나 대규모 프로젝트에서 유리합니다. 캐시 hit률이 높은 환경에서는 ccache/sccache만으로도 충분한 경우가 많습니다.

## 병렬 jobs 수(-j)와 메모리·캐시

**make -j N**, **ninja -j N** 등으로 **동시에 돌릴 컴파일 작업 수**를 정합니다. N을 코어 수에 맞추거나 그보다 조금 크게 두면 CPU를 잘 쓰지만, **메모리**는 작업당 1~2GB 넘게 쓸 수 있어, N이 너무 크면 메모리 부족(OOM)으로 빌드가 실패할 수 있습니다. **캐시**도 여러 작업이 동시에 돌면 공유 캐시를 나눠 쓰므로, 지나치게 큰 -j는 오히려 개별 컴파일이 느려질 수 있습니다. 머신 메모리와 코어 수를 보고 N을 조정하고(예: 코어 수와 같거나 코어 수의 1.5배), CI에서는 해당 러너의 리소스에 맞춰 -j를 고정하는 것이 좋습니다.

아래 표는 메모리·코어에 따른 `-j` 선택의 **예시 기준**입니다. 작업당 메모리는 코드(특히 무거운 템플릿·LTO)와 컴파일러에 따라 1~2GB를 넘기도 하므로, 실제로는 빌드 중 메모리 사용을 관찰해 조정합니다.

| 머신 | 코어 | RAM | 권장 -j(예시) | 위험 |
|------|------|-----|--------------|------|
| 로컬 노트북 | 8 | 16GB | 6~8 | 큰 -j 시 OOM |
| CI 러너 | 4 | 8GB | 3~4 | LTO 빌드에서 OOM 주의 |
| 빌드 서버 | 32 | 128GB | 32~48 | 캐시 경합 |

## CI에서의 캐시·분산 전략

CI에서 빌드 시간을 줄이는 핵심은 **상태를 다음 실행으로 넘기는 것**입니다. 로컬과 달리 CI 러너는 매번 깨끗한 환경에서 시작하므로, 캐시를 아티팩트로 저장·복원하지 않으면 매 빌드가 풀 빌드가 됩니다. 그래서 보통 캐시(상태 재사용)를 먼저 적용하고, 그것만으로 부족한 대규모 클린 빌드에서 분산을 추가합니다.

- **캐시**: CI 러너에서 ccache 또는 sccache 디렉터리를 **캐시 아티팩트**로 저장하고, 다음 파이프라인에서 복원합니다. 캐시 키에는 커밋 해시·빌드 타입(Release/Debug)·컴파일러 버전을 넣어, 변경이 없으면 이전 캐시를 그대로 씁니다. 캐시 크기 제한이 있으면 오래된 항목부터 지워지므로, 중요한 브랜치만 오래 유지하는 정책을 둘 수 있습니다.
- **분산**: CI에서 distcc를 쓰려면 여러 러너를 "컴파일 노드"로 두고, 오케스트레이션과 네트워크 설정이 필요합니다. 대신 **빌드 매트릭스**(여러 컴파일러·플랫폼을 병렬로 빌드)로 동시에 여러 구성을 돌리고, 각 구성은 단일 러너에서 ccache/sccache로 최대한 캐시를 활용하는 방식이 더 단순한 경우가 많습니다.
- **점진적 빌드**: PR에서는 변경된 파일만 빌드하거나, 메인 브랜치 빌드 산출물을 기반으로 증분 빌드하는 방식으로 CI 시간을 줄일 수 있습니다. 이때 캐시와 증분 빌드가 잘 맞물리도록 설계하면 됩니다.

## 실전 시나리오: CI에서 캐시 키 설계

캐시 키에는 **소스 해시**(또는 커밋)·**컴파일러 종류·버전**·**빌드 타입**(Release/Debug)·**주요 플래그**(-O2, -flto 등)를 포함해야 합니다. LTO·PGO를 켜면 오브젝트 내용이 달라지므로, 이들을 켠 빌드와 끈 빌드는 캐시를 공유하지 않도록 키를 구분합니다. sccache를 쓰면 원격 저장소(S3 등)에 캐시를 두어 여러 CI 러너가 공유할 수 있습니다.

GitHub Actions에서는 ccache 디렉터리를 캐시 아티팩트로 저장·복원하고, **캐시 키에 컴파일러·빌드 타입·OS를 포함**해 잘못된 재사용을 막습니다. `restore-keys`로 부분 일치 폴백을 두면 키가 약간 달라도 이전 캐시를 기반으로 시작할 수 있습니다.

```yaml
- name: Restore ccache
  uses: actions/cache@v4
  with:
    path: ~/.ccache
    # 컴파일러·빌드타입·OS를 키에 포함 (플래그가 다르면 키 분리)
    key: ccache-${{ runner.os }}-gcc13-Release-${{ github.sha }}
    restore-keys: |
      ccache-${{ runner.os }}-gcc13-Release-
```

## 한눈에 보기: 도구별 역할

| 도구 | 역할 | 적합한 상황 |
|------|------|-------------|
| ccache | 로컬 컴파일 결과 캐시 | 재빌드·소량 변경 |
| sccache | 원격 공유 캐시(S3 등) | CI·분산 팀 |
| distcc | 컴파일 작업 분산 | 클린 빌드·대규모 |

## 판단 기준: 언제 무엇을 쓸지

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 로컬·CI 재빌드 | ccache 또는 sccache | 캐시 없이 매번 풀 빌드 |
| CI 캐시 | 캐시 키에 소스·컴파일러·플래그 포함 | LTO 등 플래그 누락 시 오염 |
| -j 수 | 메모리·코어 고려(코어 수~1.5배) | 과다 -j로 OOM |

## 자주 하는 실수

- **캐시 키에 플래그 누락**: LTO·PGO·-O2/-O3 등 플래그가 바뀌면 산출물이 달라지므로, 캐시 키에 이들을 넣지 않으면 잘못된 오브젝트가 재사용되어 빌드가 깨지거나 이상 동작할 수 있다. 소스 해시·컴파일러·버전·주요 플래그를 모두 캐시 키에 포함한다.
- **-j 과다 설정**: 메모리가 부족한 머신에서 -j를 코어 수보다 훨씬 크게 두면 OOM으로 빌드가 실패한다. 작업당 1~2GB를 쓰는 경우가 있으므로, 메모리와 코어 수를 보고 -j를 조정한다. CI 러너 리소스에 맞춰 -j를 고정해 두는 것이 안전하다.

## 학습 성과 목표

- **ccache·sccache·distcc**의 역할과 차이를 설명할 수 있다.
- CI에서 캐시·분산 전략을 설계하고, 캐시 키와 -j 설정을 적용할 수 있다.
- LTO·PGO와 캐시 키의 관계를 설명할 수 있다.

## 비판적 시각: 한계와 트레이드오프

ccache/sccache는 **동일한 소스·플래그**일 때만 hit이 난다. 플래그를 자주 바꾸거나 클린 빌드가 많으면 캐시 이득이 작다. distcc는 네트워크·스토리지 설정이 필요하고, -j를 너무 크게 잡으면 OOM으로 실패할 수 있다. "캐시와 병렬만 켜면 빌드가 빨라진다"가 아니라, 자신의 CI·로컬 패턴에 맞춰 캐시 키와 -j를 설계하는 것이 중요하다.

## 핵심 요약

| 항목 | 요약 |
|------|------|
| ccache/sccache | 동일 소스·플래그 재사용으로 빌드 시간 감소 |
| distcc | 컴파일 작업 분산; 클린·대규모에 유리 |
| CI | 캐시 아티팩트·캐시 키·-j 설정 |

## 다음 장에서는

**정적 분석기**(Clang Static Analyzer, GCC -fanalyzer)와 성능 관련 경고, CI 연계를 다룹니다.

→ [Static Analyzer](/post/compiler-optimization/static-analyzer-performance/) (챕터 13)
