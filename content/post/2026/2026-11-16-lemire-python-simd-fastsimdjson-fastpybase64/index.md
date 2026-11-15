---
title: "[Python] Python SIMD 바인딩: fastsimdjson과 fastpybase64가 빠른 이유"
description: "Lemire가 공개한 fastsimdjson·fastpybase64 벤치마크를 정리한다. 파싱 속도보다 Python 객체 생성 비용이 병목이라는 점과 free-threaded 빌드 병렬화, 수치의 한계를 함께 짚는다."
date: 2026-11-16T00:30:00+09:00
lastmod: 2026-11-16
draft: false
categories:
  - Python
  - Optimization
tags:
  - Python
  - Python-3.14
  - SIMD(단일명령다중데이터)
  - simdjson
  - simdutf
  - Base64
  - JSON(JavaScript Object Notation)
  - JSON-Parsing
  - Daniel-Lemire
  - Free-Threaded-Python
  - GIL
  - Python-Bindings
  - Lazy-Evaluation
  - Performance(성능)
  - Optimization(최적화)
  - Benchmark(벤치마크)
  - Throughput
  - Latency
  - Parallel-Computing(병렬컴퓨팅)
  - Concurrency(동시성)
  - Multithreading
  - Vectorization(벡터화)
  - Memory(메모리)
  - C++
  - Native-Extension
  - Open-Source(오픈소스)
  - Software-Engineering(소프트웨어공학)
  - Deep-Dive
  - orjson
  - msgspec
  - 파이썬
  - 성능 최적화
  - 병렬 처리
image: "wordcloud.png"
---

JSON 파서를 SIMD로 아무리 빠르게 만들어도, 결과를 전부 Python 객체로 바꾸는 순간 속도는 객체 생성 비용에 묶인다. Daniel Lemire가 2026년 10–11월에 올린 세 편의 블로그 글은 이 점을 수치로 보여준다. 대상은 simdjson의 Python 바인딩 fastsimdjson(저장소 이름은 fastpysimdjson)과 simdutf의 base64 바인딩 fastpybase64다. 이 글은 그 수치와 설계 아이디어를 정리하고, 어디까지 믿을 수 있는지 함께 따진다. 모든 숫자는 Lemire 본인의 벤치마크이며 필자가 재측정한 값이 아니다.

## 배경: 두 라이브러리가 하는 일

**simdjson**은 SIMD(Single Instruction, Multiple Data, 단일 명령 다중 데이터) 명령으로 JSON을 파싱하는 C++ 라이브러리이고, **simdutf**는 같은 방식으로 UTF 인코딩 변환과 base64를 처리하는 C++ 라이브러리다. 두 라이브러리의 핵심은 한 번에 여러 바이트를 벡터 레지스터에 올려 처리하는 것이다. Python에서 이를 쓰려면 바인딩이 필요하고, 바인딩의 설계가 곧 사용자가 체감하는 속도를 결정한다.

## fastsimdjson: lazy view와 free-threaded 병렬화

벤치마크 환경은 Python 3.14.6 free-threaded 빌드(`python3.14t`), fastsimdjson 0.6.0, Xeon Gold 6548N 2소켓(64코어)이다. 입력은 GH Archive 8시간치 GitHub 이벤트로, 압축을 푼 NDJSON이 약 7.6GB, 이벤트가 약 220만 건이다. `map_many`에 `lazy=True`, `threads=64`를 지정해 처리했다.

| 방식 | 1코어 (GB/s) | 64스레드 (GB/s) |
|---|---|---|
| json (표준) | 0.18 | 3.17 |
| orjson | 0.42 | - |
| msgspec (타입 지정) | 1.29 | 24.6 |
| fastsimdjson map_many | 0.63 | 29.8 |
| fastsimdjson lazy | 2.13 | 65.7 |

lazy 방식은 7.6GB를 약 0.12초에 처리했고, 표준 json 단일 코어는 약 42초 걸렸다. 단일 코어 대비 약 31배 확장됐다. lazy view는 이벤트 전체를 파싱해 구조를 파악하되, 사용자가 접근한 필드만 Python 객체로 만든다. 같은 simdjson을 쓰는 비lazy `map_many`가 lazy보다 크게 느린 이유를 저자는 곧바로 버려질 Python 객체를 만드는 비용으로 설명한다.

```mermaid
flowchart LR
    raw["JSON 바이트"] --> simd["SIMD 파싱"]
    simd --> eager["전체를 Python 객체로 변환"]
    simd --> lazyView["lazy view 유지"]
    lazyView --> access["접근한 필드만 객체 생성"]
    eager --> cost["객체 생성 비용이 병목"]
    access --> fast["파싱 속도에 근접"]
```

msgspec은 필드를 미리 선언한 스키마가 필요해 이 벤치마크에서 유리한 조건이었다. 즉 "스키마를 알고 있다"는 정보를 주면 객체 생성을 줄일 수 있는데, lazy view는 스키마 선언 없이 비슷한 효과를 노리는 접근이다. 한편 느린 방식은 1회만 측정했다는 점은 감안해야 한다.

### 후속 측정: 192코어

2026-11-14 글에서는 AWS `c8a.metal-48xl`(AMD EPYC 9R45 2소켓, 192코어), Python 3.14.10 free-threaded 빌드로 같은 데이터를 다시 측정했다. "가장 별을 많이 받은 저장소" 집계에서 `map_many`에 읽을 필드 경로(`/type`, `/repo/name`)만 지정했더니 1코어 약 8GB/s(msgspec 대비 약 3.5배), 192스레드 55ms(약 138GB/s)였다. msgspec 프로세스 풀 최고치는 약 116GB/s(프로세스 96개)였고, 저자는 프로세스 수를 늘릴수록 msgspec이 오히려 느려졌다고 보고한다. Pison 파일 6종(각 약 1GB)의 twitter 쿼리에서는 최대 약 277GB/s가 나왔고 4종이 100GB/s를 넘었다.

여기서 중요한 전제는 free-threaded 빌드다. GIL(Global Interpreter Lock)이 없어야 스레드로 C++ 쪽 파싱을 실제 병렬 실행할 수 있다. 277GB/s는 특정 파일과 쿼리의 값이고, 앞 절의 64코어 수치와는 하드웨어가 달라 직접 비교할 수 없다.

## fastpybase64: simdutf 기반 base64 디코딩

fastpybase64 v0.1.0은 simdutf의 SIMD base64 구현을 Python에 처음 연결한 바인딩으로, 표준 `base64`의 대체재(drop-in replacement)를 표방한다. 브라우저가 쓰는 "forgiving" 디코딩, 즉 공백과 줄바꿈을 무시하는 방식을 구현한다. 단일 코어, Python 3.14.6, 76자마다 줄바꿈이 있는 MIME 스타일 입력에서 디코딩 속도(디코딩된 GB/초)는 다음과 같다.

| 입력 크기 | base64 (표준) | pybase64 | fastpybase64 |
|---|---|---|---|
| 1 KiB | 0.44 | 1.5 | 4.4 |
| 64 KiB | 0.49 | 3.1 | 13.3 |
| 1 MiB | 0.49 | 3.2 | 13.1 |

표준 대비 약 27배, pybase64 대비 약 4배다. 입력이 1KiB로 작아도 표준 대비 약 10배가 나오는 점이 눈에 띈다. 다만 디코딩만 측정했고 인코딩은 다루지 않았으며, 단일 CPU·단일 입력 형식이다. 또한 0.1.0 초기 릴리스다. 지원 범위는 Linux·macOS·Windows 휠, Python 3.10–3.14(free-threaded 포함)다.

## 시사점과 적용 판단

두 사례가 공통으로 보여주는 것은 인터페이스가 성능 상한을 정한다는 점이다.

- 파서가 GB/s 단위로 빨라져도 결과를 모두 Python 객체로 만들면 그 비용이 지배한다. 필요한 필드만 만드는 lazy 접근이나 읽을 경로를 미리 지정하는 방식이 효과적이다.
- 스레드 병렬화는 GIL이 없는 free-threaded 빌드가 전제다. 일반 빌드에서 같은 확장이 같은 확장성을 낸다고 보장하는 근거는 이 자료에 없다.
- 바인딩이 표준 라이브러리 API를 흉내 내는 drop-in 방식이면 도입 비용이 낮지만, 입력 정규화 같은 세부 동작이 달라지지 않는지 확인해야 한다.

실무에서 판단할 기준은 단순하다. 병목이 정말 JSON 파싱이나 base64 디코딩인지 프로파일링으로 먼저 확인하고, 처리량이 수 GB/s 규모의 로그·이벤트 스트림처럼 큰 입력일 때만 도입 이득이 커진다. 요청당 수 KB의 JSON을 가끔 읽는 서비스라면 표준 라이브러리나 orjson으로도 충분하다. 두 수치 모두 단일 저자의 특정 하드웨어·입력 측정이므로, 자신의 데이터로 재측정한 뒤 결정하는 것이 안전하다.

## 참고 및 출처

- [Parsing JSON at tens of gigabytes per second… in Python (2026-10-12)](https://lemire.me/blog/2026/10/12/parsing-json-at-tens-of-gigabytes-per-second-in-python/)
- [Decoding base64 in Python at 10 gigabytes per second (2026-10-17)](https://lemire.me/blog/2026/10/17/decoding-base64-in-python-at-10-gigabytes-per-second/)
- [Reading JSON at 277 GB/s in Python (2026-11-14)](https://lemire.me/blog/2026/11/14/reading-json-at-277-gb-s-in-python/)
- [fastpysimdjson (GitHub)](https://github.com/simdjson/fastpysimdjson)
- [fastpybase64 (GitHub)](https://github.com/simdutf/fastpybase64)
- [simdutf (GitHub)](https://github.com/simdutf/simdutf)
