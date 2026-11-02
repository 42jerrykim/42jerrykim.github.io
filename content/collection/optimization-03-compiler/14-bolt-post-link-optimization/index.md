---
collection_order: 14
date: 2026-03-24
lastmod: 2026-10-21
draft: false
image: wordcloud.png
title: "[Compiler 03] BOLT·후링크(post-link) 최적화"
slug: bolt-post-link-binary-layout-optimization
description: "BOLT 후링크 최적화의 동작 원리(CFG 재구성·블록/함수 재배치·핫/콜드 분할)와 입력 바이너리 요구 사항, perf→perf2bolt→llvm-bolt 절차, PGO·LTO와의 순서, 프로파일 대표성과 CI 재현성 문제를 1차 문서 기준으로 정리합니다."
tags:
  - C++
  - Performance(성능)
  - Optimization(최적화)
  - Compiler(컴파일러)
  - CPU(Central Processing Unit)
  - Cache
  - Memory(메모리)
  - Hardware(하드웨어)
  - Low-Level(로우레벨)
  - Profiling(프로파일링)
  - Benchmark
  - Linux(리눅스)
  - CI-CD(Continuous Integration/Continuous Deployment)
  - Reliability
  - Debugging(디버깅)
  - Pitfalls(함정)
  - Best-Practices
  - Guide(가이드)
  - Reference(참고)
  - Advanced
  - Deep-Dive
  - 실습
  - Comparison(비교)
  - Open-Source(오픈소스)
  - BOLT
  - LLVM
  - Clang
  - GCC
  - perf
  - PGO
  - LTO
  - Linker
---

본 장은 **전문** 난이도입니다. <strong>후링크(post-link) 최적화</strong>는 링크가 끝난 실행 파일을 입력으로 받아, 실행 프로파일을 근거로 함수와 기본 블록의 배치를 다시 짜는 기법입니다. 소스를 다시 컴파일하지 않고 기계어의 **위치**만 바꿔 명령 캐시(I-cache)와 iTLB, 분기 예측기의 압력을 줄입니다. 이 분야의 대표 도구는 LLVM 프로젝트의 **BOLT**이며, 이 장에서는 BOLT가 무엇을 하는지, 입력 바이너리가 갖춰야 할 조건과 실제 명령, PGO·LTO와의 순서, 그리고 프로파일 대표성과 CI 재현성처럼 운영에서 깨지기 쉬운 지점을 다룹니다.

BOLT는 Meta(당시 Facebook)에서 시작해 현재는 [LLVM 프로젝트 저장소의 `bolt` 디렉터리](https://github.com/llvm/llvm-project/tree/main/bolt)에서 개발됩니다. 아래의 명령과 요구 사항은 같은 저장소의 BOLT README를 기준으로 했으며, 옵션 이름은 버전에 따라 바뀔 수 있으므로 적용할 때는 사용하는 버전의 `llvm-bolt -help`로 확인해야 합니다.

## 후링크가 하는 일

컴파일러와 링커도 이미 레이아웃을 결정합니다. 컴파일러는 함수 안의 기본 블록 순서를 정하고, PGO가 있으면 자주 실행되는 블록을 앞쪽에 모읍니다. 링커는 함수들을 섹션 단위로 이어 붙입니다. 그러나 이 결정들은 함수 경계나 번역 단위 경계에 묶여 있어서, 서로 다른 파일에 있는 두 함수가 항상 함께 실행되더라도 실행 파일 안에서는 멀리 떨어져 있을 수 있습니다. 대형 서버 바이너리처럼 핫 코드가 수 메가바이트에 흩어져 있으면, 이 흩어짐 자체가 I-cache 미스와 iTLB 미스의 원인이 됩니다.

[BOLT README](https://github.com/llvm/llvm-project/blob/main/bolt/README.md)는 BOLT를 대형 애플리케이션을 빠르게 하려고 만든 후링크 최적화기로 소개하고, `perf` 같은 샘플링 프로파일러로 모은 실행 프로파일에 근거해 코드 레이아웃을 최적화한다고 설명합니다. 동작 방식은 다음과 같습니다. BOLT는 바이너리의 함수를 디스어셈블해 제어 흐름 그래프(CFG)를 다시 만들고, 프로파일에서 얻은 분기 빈도를 그 그래프에 입힙니다. 그런 다음 함수 안에서는 자주 이어서 실행되는 블록끼리 붙이고(`-reorder-blocks`), 함수 사이에서는 자주 함께 호출되는 함수끼리 모으며(`-reorder-functions`), 거의 실행되지 않는 블록은 함수 밖의 콜드 영역으로 떼어 냅니다(`-split-functions`). 결과적으로 핫 경로가 몇 개의 연속된 영역으로 압축되어, 같은 양의 캐시로 더 많은 핫 코드를 담게 됩니다.

## 입력 바이너리 요구 사항

BOLT가 바이너리를 다시 쓰려면 몇 가지 조건이 필요합니다. README에 따르면 BOLT는 x86-64와 AArch64의 ELF 바이너리를 대상으로 하며, 최소한 심볼 테이블이 strip되지 않아야 하고, 최대 효과를 얻으려면 링커의 `--emit-relocs`(`-q`)로 재배치 정보를 남겨야 합니다. README는 BOLT가 함수 안의 코드뿐 아니라 함수 자체를 재배치하려면 링커의 도움이 필요하다며 최종 링크에 `--emit-relocs`를 추가하라고 안내합니다. 즉 아래 명령의 `-reorder-functions`가 효과를 내려면 재배치 정보가 사실상 필수입니다. [챕터 10](/post/compiler-optimization/debug-info-and-release-performance/)에서 본 `strip --strip-all`을 BOLT 이전에 적용하면 안 되는 이유가 여기에 있습니다.

GCC로 빌드할 때는 함정이 하나 더 있습니다. README는 BOLT가 현재 `-freorder-blocks-and-partition`과 호환되지 않고, GCC 8부터 이 옵션이 기본으로 켜지므로 `-fno-reorder-blocks-and-partition`으로 명시적으로 꺼야 한다고 경고합니다. 또 BOLT는 디스어셈블과 CFG 재구성에 휴리스틱을 쓰므로, 함수 포인터 간 거리처럼 코드 배치 자체에 의존하는 코드나 코드와 데이터가 섞인 손으로 쓴 어셈블리는 처리하지 못할 수 있습니다.

## 실행 절차: 수집 → 변환 → 최적화

README가 설명하는 표준 흐름은 세 단계입니다. 먼저 재배치 정보를 남겨 빌드하고, 대표 입력으로 분기 정보가 포함된 프로파일을 수집합니다.

```bash
# 빌드: 재배치 정보 유지, GCC라면 블록 파티셔닝 끄기
g++ -O2 -fno-reorder-blocks-and-partition main.cc -o app -Wl,--emit-relocs
readelf -S app | grep rela.text          # 재배치 섹션이 남았는지 확인

# (1) 프로파일 수집: cycles 이벤트 + 분기 스택(-j any,u)
perf record -e cycles:u -j any,u -o perf.data -- ./app < representative_input

# (2) perf 데이터를 BOLT 형식(.fdata)으로 변환
perf2bolt -p perf.data -o perf.fdata ./app

# (3) 레이아웃 최적화
llvm-bolt ./app -o ./app.bolt -data=perf.fdata \
  -reorder-blocks=ext-tsp -reorder-functions=cdsort \
  -split-functions -split-all-cold -split-eh -dyno-stats
```

`-j any,u`는 x86의 LBR(Last Branch Record)처럼 하드웨어가 기록한 최근 분기 목록을 샘플마다 함께 저장하라는 뜻입니다. README는 VM처럼 분기 기록을 쓸 수 없는 환경에서는 일반 샘플만으로도 진행할 수 있지만(이때 `perf2bolt`에 `-ba`를 추가), 프로파일 품질이 떨어져 이득도 작아진다고 설명합니다. 서버처럼 상시 실행되는 프로그램은 배포하고 워밍업한 뒤 `perf record -e cycles:u -j any,u -a -o perf.data -- sleep 180`처럼 일정 시간 시스템 전체를 기록하며, README는 `-dyno-stats` 기준으로 약 10억 명령을 덮는 프로파일을 권장합니다. `perf`를 쓸 수 없다면 `llvm-bolt -instrument`로 계측 바이너리를 만들어 실행하는 방법도 있습니다.

최적화된 `app.bolt`는 원본과 다른 바이너리입니다. README에 따르면 BOLT가 수정한 바이너리에는 `.note.bolt_info` 노트와 이름에 `bolt`가 들어간 섹션이 생기므로, `readelf -S app.bolt | grep bolt`로 배포 산출물이 실제로 BOLT를 거쳤는지 확인할 수 있습니다. 디버그 정보도 갱신하려면 `-update-debug-sections`를 추가해야 하며, 그렇지 않으면 디버거가 보는 주소와 실제 코드 위치가 어긋납니다.

## PGO·LTO와의 순서

PGO와 BOLT는 둘 다 프로파일을 쓰지만 다루는 층이 다릅니다. PGO([챕터 03](/post/compiler-optimization/pgo-workflow-advanced/))는 컴파일 시점에 인라이닝, 분기 배치, 레지스터 할당 같은 **코드 생성** 자체를 바꾸고, LTO([챕터 02](/post/compiler-optimization/lto-thinlto-practical/))는 번역 단위 경계를 넘어 최적화합니다. BOLT는 그렇게 생성된 기계어의 **배치**만 다시 짭니다. 그래서 순서는 PGO·LTO로 코드를 먼저 확정하고, 그 최종 바이너리에 BOLT를 적용하는 것이 자연스럽습니다.

| 기법 | 적용 시점 | 입력 | 바꾸는 것 | 소스 재컴파일 |
|------|----------|------|----------|--------------|
| PGO | 컴파일 | 계측 또는 샘플 프로파일 | 인라이닝·분기 배치·레지스터 할당 등 코드 생성 | 필요 |
| LTO | 링크 | 모든 TU의 중간 표현 | TU 경계를 넘는 인라이닝·제거 | 링크 단계에서 코드 생성 |
| BOLT | 링크 이후 | 완성된 바이너리 + perf 프로파일 | 함수·블록의 배치, 핫/콜드 분할 | 불필요 |

이 순서가 실제로 이득을 내는지는 1차 자료가 보여 줍니다. [BOLT 논문(CGO 2019)](https://arxiv.org/abs/1807.06735)의 초록은 BOLT가 FDO와 LTO로 빌드한 고도로 최적화된 바이너리에서도 성능을 올리며, 후링크 개선이 기존 컴파일러 최적화와 보완 관계라고 밝힙니다. 같은 초록에 따르면 Facebook 데이터센터 애플리케이션에서는 프로파일 기반 함수 재정렬과 LTO 위에서 최대 8.0%, GCC와 Clang 컴파일러 바이너리에서는 FDO와 LTO 위에서 최대 20.4%의 속도 향상을 얻었습니다. 이 값은 대형 바이너리에서의 "최대" 수치이므로 일반적인 기대치로 읽으면 안 되지만, PGO·LTO와 BOLT가 서로를 대체하지 않는다는 근거로는 충분합니다. LLVM 자신도 [Advanced Builds 문서](https://llvm.org/docs/AdvancedBuilds.html)에서 PGO와 (Thin)LTO 위에 BOLT를 적용하는 3단계 빌드 구성(`BOLT-PGO.cmake`)을 제공합니다.

```mermaid
flowchart LR
  A["소스"] --> B["컴파일(PGO 적용)"]
  B --> C["링크(LTO, --emit-relocs)"]
  C --> D["바이너리"]
  D --> E["perf 프로파일 수집"]
  E --> F["llvm-bolt 레이아웃 최적화"]
  F --> G["배포 바이너리"]
```

## 프로파일 대표성이 결과를 좌우한다

후링크 최적화는 입력 프로파일이 보여 주는 실행만 최적화합니다. 벤치마크에서는 핫하지만 프로덕션에서는 거의 실행되지 않는 코드를 앞으로 당기면, 실제로 핫한 코드가 밀려나 오히려 캐시 효율이 떨어질 수 있습니다. 서비스가 배치 처리, 온라인 요청, 관리 명령처럼 여러 모드로 동작한다면 모드별로 프로파일을 모아 합쳐야 합니다. README는 모드마다 프로파일을 만든 뒤 `merge-fdata *.fdata > combined.fdata`로 합쳐, 프로파일끼리 모순되지 않는다면 모든 모드에 이득이 되는 단일 바이너리를 만들 수 있다고 설명합니다.

버전 차이도 중요합니다. README에 따르면 최적화할 바이너리가 프로파일을 수집한 바이너리와 100% 같을 필요는 없지만, 다를수록 프로파일이 오래되어(stale) 무효가 되고, BOLT는 오래된 프로파일을 가진 함수의 수를 보고하며 그 수가 클수록 성능 향상은 작아집니다. 같은 문서는 릴리스 브랜치에서는 `.fdata`를 반드시 갱신하라고 강조합니다. 따라서 도입 문서에는 "평균 몇 % 빨라졌다"보다 어떤 트래픽 구성으로 수집했는지, 어느 바이너리 버전에서 수집했는지, 평균뿐 아니라 꼬리 지연(p99)까지 비교했는지를 먼저 적는 편이 안전합니다.

## CI·릴리스 파이프라인에서의 현실

BOLT를 릴리스 파이프라인에 넣으면 빌드가 결정론적이지 않게 될 수 있습니다. 같은 커밋이라도 다른 프로파일을 넣으면 다른 바이너리가 나오므로, 재현 가능한 빌드나 바이너리 서명을 요구하는 조직에서는 사용한 `.fdata`를 산출물과 함께 버전 관리해야 합니다. 디버깅도 달라집니다. 함수가 핫 부분과 콜드 부분으로 쪼개지면 한 함수의 코드가 바이너리의 서로 먼 두 위치에 놓이고, 디버그 정보를 갱신하지 않으면 주소와 소스 줄의 매핑이 어긋납니다. 심볼 서버에는 원본이 아니라 BOLT 처리 후의 바이너리와 갱신된 디버그 정보를 올려야 합니다.

검증은 BOLT 전후 바이너리를 같은 하드웨어, 같은 벤치마크로 비교하는 것이 기본입니다. `-dyno-stats` 출력은 실행된 명령 수와 분기 수의 변화를 보여 주므로 레이아웃 변화가 의도대로 일어났는지 확인하는 데 쓰고, 실제 효과는 `perf stat`의 I-cache·iTLB 미스와 실행 시간으로 확인합니다. 회귀가 생겼을 때 BOLT 단계만 끌 수 있는 스위치와, 전후 바이너리를 모두 보존하는 정책을 미리 두어야 원인을 빠르게 가를 수 있습니다.

## 적용 판단 기준

| 상황 | 권장 | 비권장 |
|------|------|--------|
| PGO·LTO 이후에도 I-cache·iTLB 미스가 프로파일에서 뚜렷한 대형 바이너리 | BOLT 도입 검토, 전후 비교 벤치마크 | 레이아웃 문제를 확인하지 않고 도입 |
| 작은 바이너리, 핫 코드가 캐시에 이미 들어가는 경우 | 도입 보류 | 효과 측정 없이 파이프라인 추가 |
| 프로파일 수집 경로 | 대표 트래픽을 자동 수집, 모드별 프로파일 병합, 릴리스마다 갱신 | 개발자 PC 벤치 한 번의 프로파일 재사용 |
| GCC 빌드 | `-fno-reorder-blocks-and-partition`, `--emit-relocs` | 기본 옵션 그대로 BOLT 적용 |

## 흔한 오해

- **"BOLT가 PGO를 대체한다"**: BOLT는 이미 생성된 코드의 배치만 바꾼다. 인라이닝과 코드 생성은 PGO의 몫이고, 논문이 보여 주듯 둘은 보완 관계다.
- **"strip된 배포 바이너리에 나중에 적용하면 된다"**: BOLT는 최소한 strip되지 않은 심볼 테이블이 필요하고, 함수 재배치에는 `--emit-relocs`가 필요하다. 빌드 단계에서부터 준비해야 한다.
- **"한 번 만든 프로파일을 계속 쓴다"**: 코드가 바뀔수록 프로파일은 오래되어 효과가 줄어든다. 릴리스마다 갱신한다.

## 학습 성과 목표

이 장을 마치면 BOLT를 "켜는 옵션"이 아니라 프로파일과 릴리스 절차를 함께 설계해야 하는 빌드 단계로 평가할 수 있어야 합니다.

- BOLT가 CFG 재구성과 블록·함수 재배치로 I-cache·iTLB 압력을 줄이는 원리와, 입력 바이너리 요구 사항(심볼 테이블, `--emit-relocs`, GCC 블록 파티셔닝 비활성화)을 설명할 수 있다.
- `perf record -j any,u` → `perf2bolt` → `llvm-bolt`로 이어지는 절차를 실행하고, `.note.bolt_info`와 `-dyno-stats`로 결과를 확인할 수 있다.
- PGO·LTO와의 순서, 프로파일 대표성·갱신 주기, 재현성·디버깅 영향을 근거로 도입 여부를 판단할 수 있다.

## 비판적 시각: 한계와 트레이드오프

BOLT의 이득은 핫 코드가 넓게 흩어진 대형 바이너리에서 크고, 작은 프로그램이나 짧게 실행되고 끝나는 프로세스에서는 미미할 수 있습니다. 논문의 수치도 데이터센터 서비스와 컴파일러처럼 코드 크기가 큰 대상에서 나온 것입니다. 비용은 운영 쪽에 쌓입니다. 프로파일 수집 인프라, 분기 기록을 지원하는 하드웨어나 커널 설정, 릴리스마다의 프로파일 갱신, 비결정적 빌드에 대한 감사 대응, 디버깅 도구 체인의 조정이 모두 필요합니다. 또 BOLT는 디스어셈블 휴리스틱에 의존하므로, 일반적이지 않은 코드 패턴이 있는 바이너리에서는 처리 실패나 잘못된 변환 가능성을 검증으로 배제해야 합니다. PGO와 LTO를 아직 적용하지 않았다면, 같은 프로파일 인프라로 얻을 수 있는 이득이 그쪽에 먼저 있으므로 BOLT는 그다음 단계로 두는 것이 합리적입니다.

## 다음 장에서는

**AutoFDO(Automatic Feedback-Directed Optimization)** 워크플로우, 샘플링 기반 프로파일 수집·변환·적용, PGO(instrumented)와의 운영 비용 비교를 다룹니다.

→ [AutoFDO 워크플로우](/post/compiler-optimization/autofdo-workflow-sampling-based/) (챕터 15)
