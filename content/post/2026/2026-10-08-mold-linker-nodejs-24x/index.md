---
title: "[Cpp] mold 링커로 Node.js 링킹 2.5초를 0.11초로"
description: "Lemire가 160MB짜리 Node.js 실행 파일을 링크해 보니 GNU ld 2.52초, gold 1.46초, mold 0.11초였다. 링커가 하는 일과 mold가 빠른 이유, -fuse-ld=mold와 mold -run 적용법, 벤치마크를 읽을 때의 한계를 정리한다."
date: 2026-10-08T00:30:00+09:00
lastmod: 2026-10-08
draft: false
categories:
  - Cpp
  - Optimization
tags:
  - Optimization(최적화)
  - Performance(성능)
  - Benchmark
  - Compiler(컴파일러)
  - Linux(리눅스)
  - Rust
  - Parallel-Computing(병렬컴퓨팅)
  - Multithreading
  - Thread(스레드)
  - Productivity(생산성)
  - Guide(가이드)
  - Tutorial(튜토리얼)
  - Open-Source(오픈소스)
  - Case-Study
  - Best-Practices
  - Deep-Dive
  - Trade-off
  - C++
  - mold
  - Linker
  - GNU-ld
  - gold
  - lld
  - GCC
  - Node.js
  - Build-Time
  - Daniel-Lemire
  - Developer-Experience
  - Incremental-Build
---

C++ 프로젝트에서 소스 한 줄을 고치고 다시 빌드하면, 컴파일은 바뀐 파일만 다시 하지만 링크는 매번 처음부터 다시 한다. 파일이 많고 실행 파일이 클수록 이 마지막 단계가 개발 루프의 대기 시간을 좌우한다. Daniel Lemire는 2026년 10월 6일 블로그 글에서 Node.js를 여러 링커로 링크해 비교했고, mold 3.0.0이 GNU ld 대비 멀티스레드에서 약 24배 빨랐다고 보고했다(출처: [Faster software linking with mold](https://lemire.me/blog/2026/10/06/linking-node-js-with-mold/)). 이 글은 그 숫자가 의미하는 바와, 내 프로젝트에 적용할 때 무엇을 확인해야 하는지를 정리한다.

## 링커는 무엇을 하는가

컴파일러는 소스 파일을 하나씩 오브젝트 파일로 바꾼다. 이 시점의 오브젝트 파일은 다른 파일에 있는 함수나 변수를 이름으로만 가리키는 미완성 상태다. 링커는 모든 오브젝트 파일과 라이브러리를 읽어 어떤 이름이 어디에 정의되어 있는지 풀어 주고(심볼 해석), 각 코드와 데이터를 최종 주소에 배치하며, 그 주소에 맞춰 참조 위치를 고쳐 쓴(재배치) 뒤 하나의 실행 파일로 내보낸다. 일은 단순하지만 입력이 수천 개의 파일이고 출력이 수백 MB이면 읽기·해시 조회·메모리 복사가 모두 대규모가 된다.

리눅스의 기본 링커는 GNU ld(bfd)다. 2008년 Google이 만든 gold가 더 빠른 대안으로 등장했고, 이후 LLVM의 lld가 나왔다. mold는 Rui Ueyama가 2021년에 시작한 드롭인 대체 링커로, 속도에 집중한다(출처: Lemire 원문). 프로젝트 README는 mold의 속도가 "전면적인 병렬성과 효율적인 자료구조·알고리즘"에서 나온다고 설명한다(출처: [rui314/mold](https://github.com/rui314/mold)). 기존 링커가 대체로 한 스레드에서 단계를 순서대로 처리하는 데 비해, mold는 파일 읽기와 심볼 해석, 섹션 처리 등을 여러 코어에 나눠 맡긴다.

## Lemire의 측정

측정 대상은 main 브랜치의 Node.js이고, 결과물인 `node` 실행 파일은 약 160MB다. 서버는 2소켓 Intel Xeon Gold 6548N(64코어·128스레드), 컴파일러는 GCC 14.3이며, 링크 명령을 따로 뽑아 링커별로 6번 실행한 중앙값을 적었다.

| 링커 | 링크 시간 | GNU ld 대비 |
|------|-----------|-------------|
| GNU ld (bfd) 2.41 | 2.52초 | 1배 |
| GNU gold 2.41 | 1.46초 | 약 1.7배 |
| mold 3.0.0, 1스레드 | 0.49초 | 약 5배 |
| mold 3.0.0, 8스레드 | 0.13초 | 약 19배 |
| mold 3.0.0, 128스레드 | 0.11초 | 약 24배 |

배율은 위 시간으로 계산한 값이며, 원문도 멀티스레드 mold가 ld보다 약 24배, gold보다 약 14배 빠르다고 적는다. 눈여겨볼 대목이 두 가지다. 첫째, 스레드를 1개로 제한해도 mold는 ld보다 5배 가까이 빠르다. 즉 속도의 상당 부분은 병렬화가 아니라 자료구조와 알고리즘 자체에서 나온다. 둘째, 8스레드만으로 128스레드 이득의 대부분을 얻는다. 링크에는 병렬로 쪼개기 어려운 직렬 구간이 남아 있어 코어를 늘릴수록 수확이 급격히 줄어든다고 해석할 수 있다. 이는 이 글의 추론이며 원문이 명시한 설명은 아니다.

```mermaid
flowchart LR
  A["오브젝트 파일 수천 개"] --> B["파일 읽기"]
  B --> C["심볼 해석"]
  C --> D["섹션 배치와 재배치"]
  D --> E["실행 파일 출력"]
  B -. "mold: 병렬 처리" .-> C
  C -. "일부 직렬 구간" .-> D
```

## 적용하는 방법

가장 간단한 방법은 컴파일러 드라이버에 링커를 지정하는 것이다. clang과 GCC 12.1 이상은 링크 옵션에 `-fuse-ld=mold`를 주면 된다. GCC 12.1 미만은 mold가 설치된 `libexec/mold` 디렉터리를 `-B`로 지정한다(출처: [rui314/mold README](https://github.com/rui314/mold)).

```bash
# CMake 예: 링커 플래그로 지정
cmake -S . -B build -DCMAKE_EXE_LINKER_FLAGS="-fuse-ld=mold"

# 빌드 스크립트를 건드리고 싶지 않다면 전체를 감싼다
mold -run make -j128
```

`mold -run`은 `LD_PRELOAD`를 이용해 빌드 중 `ld`, `ld.bfd`, `ld.lld`, `ld.gold` 호출을 mold로 돌려 준다. 리눅스와 FreeBSD에서 지원된다. Rust는 `.cargo/config.toml`의 리눅스 타깃 `rustflags`에 `-C link-arg=-fuse-ld=mold`를 넣으면 된다. 실제로 mold가 쓰였는지는 `readelf -p .comment <파일>` 출력에 mold 문자열이 있는지로 확인한다. 라이선스는 MIT다.

## 숫자를 내 프로젝트에 옮기기 전에

이 벤치마크는 한 대의 서버, 한 개의 프로젝트에서 나온 결과이므로 일반화에는 단서가 붙는다. 먼저 절대 시간의 차이는 2.4초 남짓이다. 한 번 빌드하는 입장에서는 무시할 만하고, Lemire의 논지도 하루에 수십 번 증분 빌드를 돌리는 개발 루프에서 누적 효과가 크다는 것이다. 다음으로 이 측정은 LTO 없이 이뤄졌다. 원문 댓글에서 LTO를 묻자 Lemire는 LTO 작업이 링커가 아니라 컴파일러에서 일어난다고 답했다. 즉 LTO를 켠 빌드에서는 링크 단계의 이득이 전체 시간에서 차지하는 비중이 달라질 수 있다. 디버그 정보의 양에 따라서도 링크 시간 구성이 달라지므로, 디버그 빌드와 릴리스 빌드를 나눠 직접 재보는 편이 안전하다.

대안 비교도 필요하다. 같은 댓글란에서 한 독자는 대형 C++ 프로젝트에 lld가 도입하기 더 쉬웠고 성능도 mold와 비슷했다고 전했다. mold README는 최근 자체 벤치마크(2026년 8월, 세 번 실행 중앙값)에서 중앙값 기준 lld보다 4.9배, wild보다 1.9배 빠르다고 주장한다. 예컨대 Threadripper 7980X에서 디버그 빌드 Chromium 145는 lld 16.64초, mold 1.65초이고, TensorFlow 2.21 디버그 빌드는 lld 50.73초, mold 3.15초다. 다만 이는 프로젝트 제작자가 직접 공개한 수치이므로, 팀의 툴체인에서 재현해 보기 전에는 참고치로만 삼는 것이 좋다. 한편 Lemire가 공개한 스크립트와 원시 결과는 [GitHub 저장소](https://github.com/lemire/Code-used-on-Daniel-Lemire-s-blog/tree/master/2026/10/mold)에 있으나, 원문 댓글에서 문서 부족이 지적되었다.

## 도입 체크리스트

- 현재 빌드에서 링크가 전체 증분 빌드 시간의 몇 퍼센트인지 먼저 잰다. 링크가 1초 안팎이면 이득도 그만큼이다.
- `-fuse-ld=mold` 한 줄을 별도 브랜치나 CI 잡에 넣어 ld, lld, mold를 같은 머신에서 각각 6회 이상 돌려 중앙값을 비교한다.
- 디버그·릴리스·LTO 조합별로 나눠서 잰다. 한 조합의 결과를 다른 조합에 적용하지 않는다.
- 결과물이 동작이 같은지 테스트 스위트로 확인하고, `readelf -p .comment`로 어떤 링커가 쓰였는지 CI 로그에 남긴다.
- 스레드 수는 코어 전부를 쓰지 않아도 된다. 8스레드에서 이미 대부분의 이득이 나온 사례가 있으므로, CI처럼 코어가 공유되는 환경에서는 적게 잡아도 된다.

## 정리

링크는 컴파일에 가려 눈에 띄지 않지만 증분 빌드에서는 항상 처음부터 다시 도는 단계다. Lemire의 측정에서 mold는 같은 160MB짜리 Node.js를 GNU ld의 2.52초에서 0.11초로 줄였고, 단일 스레드만으로도 5배 가까이 빨랐다. 적용 비용은 컴파일 플래그 한 줄이라 시험해 볼 가치가 크지만, 한 대의 서버에서 나온 숫자이므로 내 프로젝트의 빌드 구성에서 재측정한 뒤 도입을 결정해야 한다.

## 참고 자료

- [Daniel Lemire, "Faster software linking with mold" (2026-10-06)](https://lemire.me/blog/2026/10/06/linking-node-js-with-mold/)
- [rui314/mold (README: 설계, 사용법, 벤치마크)](https://github.com/rui314/mold)
- [Lemire 벤치마크 스크립트·원시 결과](https://github.com/lemire/Code-used-on-Daniel-Lemire-s-blog/tree/master/2026/10/mold)
