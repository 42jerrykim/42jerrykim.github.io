---
collection_order: 15
date: 2026-06-01
lastmod: 2026-10-21
draft: false
image: wordcloud.png
title: "[Compiler 03] AutoFDO 워크플로우: 샘플링 기반 프로파일 최적화"
slug: autofdo-workflow-sampling-based
description: "AutoFDO가 프로덕션 샘플을 줄 번호 정보로 소스에 되돌려 컴파일러 프로파일로 쓰는 원리, GCC -fauto-profile·Clang -fprofile-sample-use 절차, 계측 PGO와의 트레이드오프, 프로파일 노후화와 자동화 파이프라인을 1차 문서 기준으로 다룹니다."
tags:
  - C++
  - Performance(성능)
  - Optimization(최적화)
  - Compiler(컴파일러)
  - CPU(Central Processing Unit)
  - Hardware(하드웨어)
  - Profiling(프로파일링)
  - Benchmark
  - Linux(리눅스)
  - CI-CD(Continuous Integration/Continuous Deployment)
  - Automation(자동화)
  - Debugging(디버깅)
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
  - AutoFDO
  - PGO
  - GCC
  - Clang
  - LLVM
  - perf
  - LBR
---

<strong>AutoFDO(Automatic Feedback-Directed Optimization)</strong>는 계측(instrumented) 빌드 없이, 일반 릴리스 바이너리를 실행하면서 하드웨어 성능 카운터 샘플을 모아 컴파일러의 프로파일로 쓰는 방식입니다. [챕터 03](/post/compiler-optimization/pgo-workflow-advanced/)의 계측 기반 PGO가 "계측 빌드 → 대표 실행 → 재컴파일"을 요구하는 반면, AutoFDO는 프로덕션에서 이미 돌고 있는 바이너리의 실행 데이터를 그대로 재사용합니다. 이 챕터에서는 AutoFDO가 해결하려는 운영 문제, 샘플을 소스 위치로 되돌리는 원리, GCC와 Clang의 실제 절차, 계측 PGO와의 트레이드오프, 그리고 프로파일이 "낡는" 문제를 다룹니다.

## 왜 AutoFDO인가

계측 기반 PGO는 정확한 실행 횟수를 주지만, 운영 비용이 큽니다. 계측 바이너리는 모든 분기와 호출에 카운터 갱신이 붙어 일반 바이너리보다 느리므로 프로덕션에 그대로 배포하기 어렵고, 그래서 대표 워크로드를 CI에서 따로 재현해야 합니다. 그 재현이 실제 트래픽을 얼마나 닮았는지가 곧 프로파일의 품질이 되고, 코드가 바뀔 때마다 계측 빌드부터 다시 해야 합니다.

AutoFDO는 이 비용 구조를 바꾸려고 만들어졌습니다. [Google의 AutoFDO 논문(CGO 2016)](https://research.google/pubs/autofdo-automatic-feedback-directed-optimization-for-warehouse-scale-applications/) 초록은 이를 다음과 같이 설명합니다.

> "AutoFDO is a system to simplify real-world deployment of feedback-directed optimization (FDO). The system works by sampling hardware performance monitors on production machines and using those profiles to guide optimization." — Chen, Li, Moseley, CGO 2016

같은 초록에 따르면 이 방식은 Google 벤치마크에서 기하 평균 10.5% 향상을 냈고, 샘플링의 부정확성과 컴파일 파이프라인에서 잃는 정보에도 불구하고 전통적인 FDO 이득의 85%를 얻었습니다. 논문은 또 프로파일이 "설계상 낡은(stale by design)" 상태라는 점을 전제하고, 릴리스가 바뀌어도 안정적인 향상을 내도록 컴파일러 기능을 구현했다고 밝힙니다. 즉 AutoFDO의 본질은 계측 PGO보다 조금 덜 정확한 프로파일을 받아들이는 대신, 프로덕션 트래픽을 지속적으로 반영하는 운영 모델을 얻는 것입니다.

## 동작 원리: 샘플을 소스 위치로 되돌리기

샘플링 프로파일러는 일정 간격으로 "지금 실행 중인 명령 주소"를 기록합니다. 그런데 컴파일러가 다음 빌드에서 쓸 수 있는 것은 주소가 아니라 소스 위치(함수와 줄 번호, 인라인 문맥)입니다. 바이너리는 다시 빌드하면 주소가 모두 바뀌기 때문입니다. 그래서 AutoFDO의 핵심 단계는 수집한 주소를 디버그 정보의 줄 번호 테이블로 소스 위치에 되돌려, 소스 기준의 프로파일로 바꾸는 변환입니다. 이 때문에 프로파일을 수집하는 바이너리에는 줄 번호 정보가 필요합니다. [챕터 10](/post/compiler-optimization/debug-info-and-release-performance/)에서 본 것처럼 같은 최적화 옵션에서 디버그 정보는 생성 코드를 바꾸지 않으므로, 릴리스 빌드에 줄 번호 정보를 넣는 것이 성능 비용 없이 이 요구를 채우는 방법입니다.

단순 주소 샘플만으로는 "어느 분기를 얼마나 탔는지"를 정확히 알기 어렵습니다. 그래서 x86에서는 LBR(Last Branch Record)을 함께 씁니다. LBR은 CPU가 최근에 수행한 분기의 출발·도착 주소를 하드웨어로 기록하는 기능으로, `perf record -b`가 이를 샘플마다 저장합니다. [Clang User's Manual](https://clang.llvm.org/docs/UsersManual.html)의 샘플링 프로파일러 절은 `-b` 플래그가 LBR로 호출 연쇄를 기록하게 하며, 꼭 필요하지는 않지만 더 나은 호출 정보를 제공해 프로파일 정확도를 높인다고 설명합니다.

```mermaid
flowchart LR
  A["릴리스 바이너리<br/>(줄 번호 정보 포함)"] --> B["프로덕션 실행<br/>+ perf record -b"]
  B --> C["perf.data<br/>(샘플 주소·분기 기록)"]
  C --> D["변환 도구<br/>(create_gcov / create_llvm_prof / llvm-profgen)"]
  D --> E["소스 기준 프로파일"]
  E --> F["재컴파일<br/>(-fauto-profile / -fprofile-sample-use)"]
  F --> G["다음 릴리스 바이너리"]
  G --> B
```

마지막 화살표가 다시 수집으로 돌아가는 점이 계측 PGO와 다릅니다. 최적화된 바이너리도 줄 번호 정보만 유지하면 그대로 다음 프로파일의 수집 대상이 되므로, 배포와 수집이 하나의 순환을 이룹니다.

## GCC 워크플로

[GCC Optimize Options](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html)의 `-fauto-profile` 설명은 GCC에서의 절차를 직접 예로 듭니다. 지원되는 GNU/Linux 시스템에서 `perf`로 프로그램을 실행해 원시 프로파일을 만들고, [google/autofdo](https://github.com/google/autofdo)의 `create_gcov` 도구로 GCC가 읽을 수 있는 형식으로 변환하며, 이때 strip하지 않은 바이너리를 함께 넘겨야 합니다.

```bash
# 1. 줄 번호 정보가 있는 릴리스 빌드
g++ -O2 -g main.cc utils.cc -o app

# 2. 분기 기록과 함께 샘플 수집 (GCC 문서의 예시 이벤트)
perf record -e br_inst_retired:near_taken -b -o perf.data -- ./app --workload-args

# 3. GCC용 AutoFDO 프로파일로 변환 (strip하지 않은 바이너리 필요)
create_gcov --binary=./app --profile=perf.data --gcov=profile.afdo

# 4. 프로파일을 반영해 재컴파일
g++ -O2 -fauto-profile=profile.afdo main.cc utils.cc -o app_afdo
```

`-fauto-profile`은 프로파일을 읽는 것만 하지 않습니다. GCC 문서에 따르면 이 옵션은 샘플링 기반 FDO와 함께 `-fbranch-probabilities`, `-funroll-loops`, `-fpeel-loops`, `-finline-functions`, `-ftree-loop-vectorize`, `-fvect-cost-model=dynamic` 등 프로파일이 있을 때 이득이 큰 최적화들을 함께 켭니다. 이 목록에는 `-O3`가 켜는 루프 변환 일부가 포함되어 있으므로, `-O2`와 함께 써도 프로파일이 가리키는 핫 루프에는 더 공격적인 변환이 적용될 수 있습니다. 경로를 생략하면 현재 디렉터리의 `fbdata.afdo`를 읽습니다. 전후 비교는 [챕터 04](/post/compiler-optimization/compiler-comparison-gcc-clang-msvc/)의 벤치마크 절차처럼 같은 입력·같은 머신에서 여러 번 반복해 중앙값과 분산으로 판단합니다.

## Clang 워크플로

Clang은 같은 개념을 "샘플 프로파일"이라는 이름으로 지원하며, Clang User's Manual이 절차를 단계별로 설명합니다. 첫 빌드에서 필요한 것은 줄 번호 정보뿐이므로 `-gline-tables-only`로 충분하고, 매뉴얼은 매핑 품질을 높이기 위해 `-fdebug-info-for-profiling`과 `-funique-internal-linkage-names`를 함께 쓰라고 권합니다.

```bash
# 1. 줄 번호 정보와 프로파일용 디버그 정보로 빌드
clang++ -O2 -gline-tables-only \
        -fdebug-info-for-profiling -funique-internal-linkage-names \
        code.cc -o code

# 2. LBR과 함께 샘플 수집 (매뉴얼의 예시 이벤트, 없으면 branches:u)
perf record -b -e BR_INST_RETIRED.NEAR_TAKEN:uppp ./code

# 3. LLVM 샘플 프로파일로 변환 (둘 중 하나)
create_llvm_prof --binary=./code --out=code.prof
llvm-profgen --binary=./code --output=code.prof --perfdata=perf.data

# 4. 같은 디버그 정보 옵션 + -fprofile-sample-use로 재컴파일
clang++ -O2 \
        -fdebug-info-for-profiling -funique-internal-linkage-names \
        -fprofile-sample-use=code.prof code.cc -o code
```

매뉴얼이 강조하는 세부 사항이 몇 가지 있습니다. `perf`를 `-b` 없이 실행했다면 `create_llvm_prof`에 `--use_lbr=false`를 줘야 하고, `llvm-profgen`은 `-b`로 수집한 데이터가 필요합니다. 재컴파일은 첫 빌드와 같은 인자일 필요는 없지만, 같은 디버그 정보 관련 옵션과 `-fprofile-sample-use`는 있어야 합니다. 또 `-funique-internal-linkage-names`는 소스 경로를 바탕으로 이름을 만들기 때문에, 빌드 시스템이 절대 경로를 쓰고 그 경로가 수집과 재빌드 사이에 바뀌면 프로파일이 쓰이지 않을 수 있습니다. 선택 사항으로 샘플링의 누락을 보정하는 프로파일 추론(`-fsample-profile-use-profi`)과, 디버그 줄 정보 대신 의사 계측점을 기준으로 매핑하는 `-fpseudo-probe-for-profiling`도 있습니다. [Clang 명령줄 레퍼런스](https://clang.llvm.org/docs/ClangCommandLineReference.html)의 `-fprofile-sample-accurate`는 프로파일이 정확하다고 선언하는 옵션으로, 샘플이 없는 호출 지점을 콜드로 표시합니다. 커버리지가 충분한 프로파일에서만 써야 하며, 그렇지 않으면 실제로 쓰이는 코드를 콜드로 취급하게 됩니다.

## 계측 PGO와의 비교

| 항목 | 계측 기반 PGO | AutoFDO(샘플링 기반) |
|------|--------------|---------------------|
| 프로파일 출처 | 계측 바이너리를 대표 워크로드로 실행 | 일반 릴리스 바이너리를 프로덕션에서 샘플링 |
| 정확도 | 실행 횟수가 정확 | 샘플링 오차, 인라인·최적화로 인한 매핑 손실 |
| 수집 비용 | 계측으로 느려진 별도 실행 | 샘플링 비용만 추가, 프로덕션 수집 가능 |
| 파이프라인 | 계측 빌드 → 수집 → 재빌드 | 릴리스 빌드 → 수집 → 다음 릴리스 빌드(순환) |
| 필요 조건 | 대표 워크로드의 재현 | 줄 번호 정보, `perf`(LBR 권장), 변환 도구 |
| 보고된 효과 | – | Google 논문 기준 기하 평균 10.5%, 전통 FDO 이득의 85% |

계측 PGO는 CI에서 대표 워크로드를 재현할 수 있고 최대 성능이 필요한 소수의 핵심 바이너리에 맞고, AutoFDO는 많은 바이너리를 지속적으로 최적화해야 하거나 실제 트래픽이 벤치마크로 재현되지 않는 서비스에 맞습니다. 논문이 보고한 "85%"는 정확도 손실의 크기를 가늠하는 근거이지만, 그 비율은 Google의 워크로드와 컴파일러 기준이므로 자신의 코드에서는 두 방식을 같은 벤치마크로 직접 비교해야 합니다.

## 자동화 파이프라인과 프로파일 노후화

AutoFDO를 지속적으로 운영하려면 수집 → 변환 → 저장 → 다음 빌드에서 사용을 자동화합니다. 이때 가장 중요한 규칙은 변환 도구에 **수집에 사용한 바로 그 바이너리**를 넘기는 것입니다. 변환은 샘플 주소를 그 바이너리의 디버그 정보로 해석하므로, 다른 커밋의 바이너리를 넘기면 주소가 엉뚱한 소스 위치로 매핑됩니다. 그래서 배포한 바이너리를 (strip하기 전 상태로) 빌드 ID와 함께 보관하는 것이 파이프라인의 전제입니다.

```bash
#!/bin/bash
# autofdo_collect.sh: 배포된 서비스에서 프로파일을 모아 저장소에 올리는 예시
set -euo pipefail
BIN=/opt/app/app.unstripped          # 배포본과 같은 빌드의 strip 전 바이너리
STAMP=$(date +%Y%m%d)

perf record -e br_inst_retired:near_taken -b -o perf_${STAMP}.data \
     -p "$(pidof app)" -- sleep 60
create_gcov --binary="$BIN" --profile=perf_${STAMP}.data --gcov=profile_${STAMP}.afdo
aws s3 cp profile_${STAMP}.afdo s3://my-bucket/profiles/
```

수집한 프로파일은 다음 릴리스의 소스에 적용되므로 언제나 조금 낡아 있습니다. 소스가 바뀌면 줄 번호가 밀려 일부 프로파일 정보가 맞지 않게 되고, 컴파일러는 대응되지 않는 정보를 쓰지 않습니다. 논문이 "stale by design"을 전제로 컴파일러 기능을 설계했다고 밝힌 이유가 이것입니다. 실무에서는 프로파일을 정기적으로 갱신하고, 대규모 리팩터링 직후처럼 소스가 크게 바뀐 경우에는 새 프로파일을 모을 때까지 이득이 줄어드는 것을 감안합니다. 프로파일 파일은 빌드 입력이므로, 같은 커밋을 재현하려면 어떤 프로파일로 빌드했는지도 함께 기록해야 합니다.

## 판단 기준: 언제 AutoFDO를 쓸지

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 많은 서비스·바이너리를 지속적으로 최적화 | AutoFDO 수집·빌드 자동화 | 바이너리마다 계측 빌드 운영 |
| 대표 워크로드를 CI에서 재현할 수 있는 소수 핵심 바이너리 | 계측 PGO 우선 | 정확도가 필요한데 샘플링만 사용 |
| 실제 트래픽이 벤치마크와 다른 서비스 | 프로덕션 샘플링 기반 AutoFDO | 벤치 한 번으로 만든 프로파일 재사용 |
| LBR을 쓸 수 없는 VM 환경 | 일반 샘플(`--use_lbr=false`)로 시작하되 이득 축소 감안 | LBR 전제 명령을 그대로 사용 |

## 자주 하는 실수

- **변환 도구에 다른 바이너리를 넘기기**: 주소 해석이 어긋나 프로파일이 잘못된 위치를 가리킨다. 수집한 바이너리의 strip 전 사본을 빌드 ID로 보관해 변환에 쓴다.
- **줄 번호 정보 없이 배포하기**: 샘플 주소를 소스 위치로 되돌릴 수 없어 프로파일을 만들 수 없다. 최소한 줄 번호 테이블(`-g1`, `-gline-tables-only`)은 유지한다.
- **`-fprofile-sample-accurate`를 기본으로 켜기**: 샘플이 없는 호출 지점을 콜드로 취급하므로, 커버리지가 낮은 프로파일에서는 실제로 쓰이는 코드를 느리게 만들 수 있다.

## 학습 성과 목표

이 챕터를 마치면 AutoFDO를 계측 PGO의 대체물이 아니라, 정확도를 조금 내주고 운영성을 얻는 다른 지점의 선택지로 평가할 수 있어야 합니다.

- 샘플 주소를 줄 번호 정보로 소스 위치에 되돌리는 AutoFDO의 원리와, LBR이 프로파일 품질에 주는 영향을 설명할 수 있다.
- GCC(`create_gcov` → `-fauto-profile`)와 Clang(`create_llvm_prof`/`llvm-profgen` → `-fprofile-sample-use`) 절차를 1차 문서대로 실행할 수 있다.
- 계측 PGO와의 트레이드오프, 프로파일 노후화와 바이너리 보관 요구를 근거로 도입 방식을 정할 수 있다.

## 비판적 시각: 한계와 트레이드오프

AutoFDO의 정확도는 수집 환경에 크게 좌우됩니다. 샘플링은 드물게 실행되는 코드를 잘 잡지 못하고, 최적화된 바이너리의 줄 번호 정보는 인라이닝과 코드 이동 때문에 원래 소스 위치를 정확히 대변하지 못합니다. LBR 같은 분기 기록 기능은 하드웨어와 가상화 환경에 따라 쓸 수 없는 경우가 있어, 클라우드 VM에서는 프로파일 품질이 떨어질 수 있습니다. 운영 측면에서도 변환 도구를 빌드·유지하고, 배포 바이너리를 보관하고, 프로파일 저장소를 관리하는 인프라가 필요합니다. 이 인프라는 서비스가 많을수록 바이너리당 비용이 낮아지므로, AutoFDO는 대규모 플릿에서 가장 큰 효과를 내고 소규모 프로젝트에서는 계측 PGO가 더 단순할 수 있습니다.

같은 샘플 프로파일 인프라는 링크 이후 레이아웃 최적화로 확장되기도 합니다. Google의 [Propeller](https://github.com/google/llvm-propeller)는 README에서 스스로를 대규모 애플리케이션을 위한 프로파일 기반 재링킹(relinking) 최적화기로 소개합니다. [챕터 14](/post/compiler-optimization/bolt-post-link-binary-layout-optimization/)의 BOLT가 완성된 바이너리를 다시 쓰는 것과 달리, Propeller는 LLVM 위에서 재링크 과정으로 레이아웃을 바꾸는 접근이라 빌드 파이프라인과의 통합 방식이 다릅니다. 어느 쪽이든 프로파일 수집 인프라를 이미 갖춘 팀에게 추가로 열리는 선택지라는 점에서, AutoFDO는 프로파일 기반 최적화 전반의 기반 시설로 보는 것이 맞습니다.

## 다음 단계

이것으로 **Low-latency 컴파일러·빌드 최적화** 트랙(챕터 00–15)의 본문을 마칩니다. 트랙 전체 목차와 학습 목표는 [컬렉션 소개](/post/compiler-optimization/getting-started-compiler-build-performance-tuning/)에서 확인할 수 있고, 12개 트랙의 전체 로드맵은 [Low-latency 최적화 시리즈 개요](/post/low-latency-optimization-series/getting-started-low-latency-optimization-series-overview/)에서 확인할 수 있습니다.
