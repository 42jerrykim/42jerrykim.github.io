---
title: "[Cpp] AI는 새 알고리즘을 만들지 않았다: Lemire의 여섯 라이브러리 최적화"
description: "ada 2.4배, simdutf ASCII 검증 83→160 GB/s 등 여섯 오픈소스 라이브러리가 한 여름에 빨라졌다. Lemire의 측정을 바탕으로 AI가 바꾼 것이 '시도 비용'임을 짚고, 측정 조건과 한계를 정리한다."
date: 2026-10-17T00:30:00+09:00
lastmod: 2026-10-17
draft: false
categories:
  - Cpp
  - Optimization
tags:
  - Optimization(최적화)
  - Performance(성능)
  - Benchmark
  - SIMD(단일명령다중데이터)
  - Open-Source(오픈소스)
  - Case-Study
  - Deep-Dive
  - Best-Practices
  - Throughput
  - C++
  - Go
  - JSON(JavaScript Object Notation)
  - Parsing(파싱)
  - Unicode
  - UTF-8
  - Base64
  - URL
  - simdjson
  - simdutf
  - ada
  - fast_float
  - Roaring-Bitmap
  - CRoaring
  - Daniel-Lemire
  - AI-Coding(AI코딩)
  - Claude
  - DeepSeek
  - Grok
  - Trade-off
  - Code-Review(코드리뷰)
image: "wordcloud.png"
---

Daniel Lemire는 SIMD 기반 파서 simdjson과 simdutf의 메인테이너로 유명한 성능 엔지니어다. 2026년 9월 22일 그는 자신이 관리하는 여섯 개 오픈소스 라이브러리가 이번 여름 눈에 띄게 빨라졌다는 글 "A Summer of AI Optimization"을 올렸다. 이 글은 그 수치를 정리하고, 수치가 말해 주는 것과 말해 주지 않는 것을 구분해 본다.

## 측정 방식부터 확인하자

숫자를 옮기기 전에 조건을 못 박아 둔다. Lemire는 각 라이브러리의 모든 커밋을 처음부터 다시 빌드해 한 대의 머신(Intel Xeon Gold 6548N)에서 벤치마크했고, 속도는 2024년 8월을 1.0으로 둔 상대값으로 표시했다. 그래프가 계단 모양인 것은 성능이 커밋 시점에서만 바뀌기 때문이다.

그는 변경마다 AI가 얼마나 관여했는지는 모른다고 밝힌다. 코드가 좋으면 어떻게 썼는지는 묻지 않는다는 입장이며, 본인은 Claude, Grok, DeepSeek을 쓴다. 또 AI 기여자 perfloop의 어드바이저라는 이해관계도 글에서 직접 공개했다.

## 라이브러리별 결과

| 라이브러리 | 용도 | 개선 내용 |
|-----------|------|-----------|
| roaring (Go) | 압축 비트맵 | 배열로 디코딩 2.5배, 다중 합집합 FastOr 3.1배, 다중 값 이터레이터 4.5–5.9배 |
| CRoaring (C) | 압축 비트맵 | contains 2.4배, 64비트 카디널리티 4.9배, 순회 1.9배 |
| ada | URL 파싱 | 0.54 → 1.28 GB/s(2.4배), 코어 하나로 초당 약 1,500만 URL |
| fast_float | 숫자 파싱 | canada.txt 43%, mesh.txt 70% 향상 |
| simdjson | JSON(C++26 리플렉션) | 직렬화 1.6–2.1배, 역직렬화 10–14% |
| simdutf | 유니코드·base64 | ASCII 검증 83 → 160 GB/s, UTF-16 검증 62 → 102 GB/s, base64 디코딩 약 17% |

눈여겨볼 점은 변화의 모양이다. ada는 2024년 8월부터 2026년 7월까지 약 550개 커밋이 쌓였는데도 처리량이 0.54 GB/s에서 움직이지 않았고, 이후 6주 만에 1.28 GB/s에 도달했다. fast_float도 약 15개월간 평평하다가 3월부터 7월 사이에 올랐다. 오랫동안 성숙했다고 여겨진 코드에서 한꺼번에 개선 여지가 나온 셈이다.

simdjson 직렬화는 `citm_catalog.json` 기준으로 바이트당 명령어 수가 6.1에서 3.1로 줄었고, 이는 처리량 향상과 거의 같은 비율이다. 속도 향상이 실제로 일을 덜 하는 방향에서 왔다는 점을 보여 주는 지표다.

## 새로운 기법은 없었다

Lemire는 쓰인 기법이 모두 잘 알려진 것이고 "새로 발명된 것은 없다"고 답했다. SIMD 벡터화, 분기 줄이기, 메모리 레이아웃 조정 같은 전통적인 저수준 최적화라는 뜻이다. 그가 보는 AI의 역할은 새 아이디어를 만드는 것이 아니라 아이디어를 시도해 보는 비용을 낮추는 것이다.

이 해석은 성능 작업의 경제학과 맞는다. 최적화 아이디어는 대부분 시도해 보고 벤치마크를 돌려야 맞는지 안다. 구현과 측정에 반나절이 드는 아이디어는 우선순위에서 밀리지만, 비용이 수십 분으로 줄면 후순위 아이디어까지 실제로 시험대에 오른다. 이 수치 가운데 상당수가 몇 주 안에 몰려 나온 것도 같은 맥락이다. 다만 "AI가 비용을 낮췄다"는 것은 저자의 해석이지, 그 인과를 입증하는 실험은 글에 없다.

## 수치를 읽을 때의 한계

- 결과는 특정 데이터셋과 워크로드에 대한 것이다. 글에서도 IP 주소 파싱 개선처럼 이 벤치마크에 드러나지 않는 변화가 있다고 밝힌다.
- AI 없이 같은 시간을 투자한 대조군이 없다. 기여자 구성도 다양해서(Cursor, Claude를 쓴다고 밝힌 기여자, perfloop 등) 어느 향상이 AI 덕인지는 분리할 수 없다.
- 기준점이 2024년 8월이므로 그 사이의 사람 손 개선과 AI 보조 개선이 섞여 있다. simdjson 리플렉션 코드는 2026년 초에 생긴 것이라 이력 자체가 짧다.
- 저자가 AI 도구 생태계와 이해관계가 있다. 이는 숨겨진 것이 아니라 공개된 사실이지만 읽을 때 감안할 요소다.

## 실무에 가져갈 점

이 사례에서 재사용할 수 있는 것은 도구 이름이 아니라 작업 방식이다. 첫째, 모든 커밋을 같은 머신에서 재빌드해 시계열로 보면 어느 변경이 효과가 있었는지 드러난다. 둘째, 빌드와 벤치마크가 자동화되어 있어야 AI가 만든 후보를 싸게 걸러낼 수 있다. 셋째, 정확성 테스트가 탄탄한 라이브러리일수록 공격적인 시도를 안전하게 받아들인다. simdjson, simdutf처럼 퍼징과 테스트 스위트가 두꺼운 프로젝트에서 이런 결과가 나왔다는 점은 우연이 아닐 것이다. 마지막 문장은 필자의 추정이다.

## 참고 및 출처

- [Daniel Lemire, "A Summer of AI Optimization" (2026-09-22)](https://lemire.me/blog/2026/09/22/a-summer-of-ai-optimization/)
- [ada-url/ada](https://github.com/ada-url/ada)
- [fastfloat/fast_float](https://github.com/fastfloat/fast_float)
- [simdjson/simdjson](https://github.com/simdjson/simdjson)
- [simdutf/simdutf](https://github.com/simdutf/simdutf)
- [RoaringBitmap/roaring](https://github.com/RoaringBitmap/roaring)
- [RoaringBitmap/CRoaring](https://github.com/RoaringBitmap/CRoaring)
- [perfloop](https://www.perfloop.com)
