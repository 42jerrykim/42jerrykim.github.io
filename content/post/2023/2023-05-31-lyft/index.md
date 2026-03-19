---
description: "Lyft가 Google Maps에서 벗어나 OpenStreetMap 기반 자체 지도를 구축한 배경, 비용·데이터 통제 효과, OSM 활용 전략, 승객·기사 경험 개선, 70% 탑승 지원까지의 기술 사례를 정리한 리뷰."
categories: Lyft
date: "2023-05-31T00:00:00Z"
lastmod: "2026-03-17T00:00:00Z"
header:
  teaser: /assets/images/2023/LyftMaps_ImageHeader_01.jpg
tags:
  - Technology
  - 기술
  - Innovation
  - 혁신
  - Mobile
  - 모바일
  - Open-Source
  - 오픈소스
  - Review
  - 리뷰
  - Case-Study
  - Data-Science
  - 데이터사이언스
  - Networking
  - 네트워킹
  - API
  - Backend
  - 백엔드
  - Cloud
  - 클라우드
  - Algorithm
  - 알고리즘
  - Problem-Solving
  - 문제해결
  - Best-Practices
  - Documentation
  - 문서화
  - Tutorial
  - 가이드
  - Guide
  - How-To
  - Comparison
  - 비교
  - Reference
  - 참고
  - Productivity
  - 생산성
  - Education
  - 교육
  - History
  - 역사
  - Web
  - 웹
  - Markdown
  - 마크다운
  - Blog
  - 블로그
  - Troubleshooting
  - 트러블슈팅
  - Configuration
  - 설정
  - Tips
  - Career
  - 커리어
  - Workflow
  - 워크플로우
  - Migration
  - 마이그레이션
  - Deep-Dive
  - Git
  - GitHub
  - DevOps
  - Automation
  - 자동화
  - Scalability
  - 확장성
  - Performance
  - 성능
  - Security
  - 보안
  - Database
  - 데이터베이스
  - JSON
  - Design-Pattern
  - 디자인패턴
  - Software-Architecture
  - 소프트웨어아키텍처
  - Microservices
  - 마이크로서비스
  - Monitoring
  - 모니터링
  - Deployment
  - 배포
  - Caching
  - 캐싱
  - Latency
  - Throughput
  - Real-Time
  - 실시간
  - GIS
  - 지도
  - Rideshare
  - 라이드쉐어
title: "[Tech] Lyft의 비밀스러운 계획: 자체 지도와 미래를 통제하다"
image: "wordcloud.png"
---

## 개요

Lyft 앱을 쓰는 수백만 운전자와 승객은 매일 지도를 보며 경로, 소요 시간, 기사와의 거리를 확인한다. 그런데 Lyft는 2020년대 초까지 이 내비게이션 경험을 **직접 통제하지 못했다**. 모든 것이 **Google Maps** 위에 올라가 있었기 때문이다. 이 글은 Lyft가 Google에 대한 의존을 줄이고 **OpenStreetMap(OSM)** 기반 **자체 지도 시스템**을 구축한 배경, 기술적 선택, 그리고 그 결과를 정리한 기술 사례다.

**추천 대상**: 모빌리티·지도·오픈소스 기반 제품을 다루는 기획자·엔지니어, 제3자 지도 API 비용과 데이터 주권을 고민하는 팀.

![Lyft Maps 헤더 이미지](/assets/images/2023/LyftMaps_ImageHeader_01.jpg)

---

## Lyft와 Google Maps: 의존의 대가

Lyft는 승객·기사 경험을 높일 수 있는 **수백 개의 기능 아이디어**를 쌓아 두었지만, 실제로 구현할 수 있는 비중은 제한적이었다. 사용자가 보는 화면의 상당 부분이 Google Maps에 의해 점유되어 있었고, Lyft는 그 "픽셀"을 바꿀 권한이 없었다.

또한 **비용과 경로 불일치** 문제가 있었다. Lyft는 자체 알고리즘으로 탑승 시간과 요금을 예측해 승객·기사에게 보여 주지만, 탑승이 확정되면 **내비게이션은 Google이 담당**한다. Google이 제안하는 경로가 Lyft가 계산한 경로와 다를 때가 있어, 통행료가 더 나가는 경로로 안내되거나 예상과 다른 비용이 발생할 수 있었다. 이는 플랫폼 전체 비용과 사용자 경험에 직결되는 이슈였다.

---

## 전환점: 자체 지도로의 결단

2019년, Lyft 엔지니어링 팀은 **회사가 직접 내비게이션 경로를 제안**할 경우 상당한 절감과 경험 개선이 가능하다고 판단했다. Google에 지불하는 비용 절감, 더 일관된 ETA·요금 예측, 그리고 더 안전하고 예측 가능한 라이드 경험까지 포함한 효과를 고려한 결과였다.

다만 Google과 Apple은 수십억 달러와 수년을 들여 자사 지도를 만들었다. Lyft처럼 상대적으로 작은 규모의 회사가 그 수준을 그대로 재현하는 것은 현실적이지 않았다. **2019년에 돌파구가 열렸다.** 팀은 **OpenStreetMap(OSM)** 플랫폼이 드디어 Lyft 규모의 서비스를 지탱할 만큼 **견고해졌다**고 평가했다.

---

## OpenStreetMap의 역할

**OpenStreetMap(OSM)**은 2004년 영국 학자가 시작한 **무료·오픈소스** 지도 프로젝트로, Google·Apple Maps의 대안이다. 위키백과처럼 자원봉사자들이 지리 정보를 중앙 데이터베이스에 기여하고, 누구나 무료로 이용할 수 있다. 2012년 Google이 기업용 Maps API 요금을 인상한 뒤 Amazon, Meta, Snapchat 등 많은 기업이 OSM 기반 지도 제품을 만들었고, 이 과정에서 OSM 데이터 품질과 커버리지가 크게 향상되었다.

Lyft는 여기에 더해 **매일 수백만 건의 탑승**으로 쌓이는 **실제 주행 데이터**를 보유하고 있었다. 가장 많이 달리는 도로를 반복적으로 지나가므로, 도로 폐쇄, 공사, 장애물 등의 변화를 감지하고 지도에 반영하는 데 필요한 신호를 얻을 수 있었다. OSM의 "최신성(freshness)"을 Lyft가 실측 데이터로 검증한 사례는 Lyft Engineering 블로그에 정리되어 있다.

---

## Lyft 자체 지도 구축 흐름

아래는 Lyft가 Google 의존에서 자체 지도로 전환하기까지의 핵심 단계를 요약한 흐름이다.

```mermaid
flowchart LR
  subgraph Before["과거 상태"]
    A[Google Maps 의존]
  end
  subgraph Decision["전환 결정"]
    B["OSM 품질 검증"]
    C["자체 경로 제안으로 비용 절감"]
  end
  subgraph Build["구축"]
    D["자체 지도 팀 및 카토그래퍼 편성"]
    E["OSM 기반 베이스맵"]
    F["실시간 탑승 데이터 반영"]
  end
  subgraph Result["결과"]
    G["Lyft Maps 출시"]
    H["전체 탑승의 약 70% 지원"]
  end
  A --> B
  B --> C
  C --> D
  D --> E
  E --> F
  F --> G
  G --> H
```

- **노드 ID**: 공백 없이 PascalCase/camelCase 사용, 예약어 미사용.
- **라벨**: 특수문자·등호가 없어 따옴표는 선택적. 서브그래프 라벨에 한글 사용.

---

### 2019년 말: "불가능한 것"에 도전

2019년 말, Lyft는 **자체 매핑 시스템**을 만드는 프로젝트를 본격화했다. 약 250명 규모의 팀(최초 카토그래퍼 및 매핑 경험 팀 포함)이 투입되어, 기사와 승객 앱 경험을 **라이드쉐어에 맞게** 재설계했다.

Google·Apple 지도는 범용 내비게이션에 강점이 있지만, **픽업·하차 지점**, **로딩 존·버스 정류장** 같은 제약, **CarPlay·Android Auto**와의 통합 등은 라이드쉐어 전용 요구사항에 가깝다. Lyft는 이런 부분을 직접 설계할 수 있게 되었다.

**Lyft Maps**의 주요 설계 방향은 다음과 같다.

- **시각 단순화**: 기사가 내비게이션과 픽업에 집중할 수 있도록 불필요한 상점·레스토랑·주변 POI를 줄였다.
- **픽업 구역 사진**: 기사가 승객을 기다리는 동안 픽업 구역 주변 사진을 볼 수 있게 해 낯선 거리에서의 혼란을 줄였다.
- **실시간 반영**: 기사가 교통 정체에 갇혀 있으면 승객에게 알림을 보내는 등, 실세계 변화를 경험에 반영했다.
- **CarPlay·Android Auto 지원**: 차량 내 디스플레이에서 Lyft 지도를 사용할 수 있도록 했다.

공개된 수치에 따르면, Lyft Maps를 써 본 기사의 **98%가 타 서비스(Google, Apple, Waze 등)로 되돌아가지 않고** Lyft 지도를 계속 사용한다고 한다. Lyft는 기사에게 선택권을 주고 피드백을 수집해, 강제가 아닌 **선호**로 자체 지도를 쓰게 만든 전략을 취했다.

---

## Lyft Maps의 확장 아이디어

자체 지도가 안정화된 뒤 Lyft는 **라이드쉐어 전용 기능**으로 차별화하는 방향을 탐색하고 있다. 예를 들면 다음과 같다.

- **기사 간 정보 공유**: 사고, 정체, 승객 하차 구역 등에 대한 정보를 기사들이 공유하는 기능.
- **경치 좋은 경로**: 승객이 "가장 빠른 경로" 대신 "경치 좋은 경로"를 선택하는 옵션.
- **대형 목적지 가이드**: 공항, 경기장, 공원 등 승하차가 빈번한 곳에 대한 픽업·하차 안내.

"하루에 수백만 번 일어나는 미세한 경험"을 개선하는 것이, 결국 "스트레스 많고 별점을 낮게 주는 탑승"과 "편하고 재이용으로 이어지는 탑승"을 나누는 요인이 될 수 있다는 인식이 담겨 있다.

---

## 정리

- Lyft는 **Google Maps 의존**으로 인한 비용·경로 불일치·제품 통제 한계를 해결하기 위해 **자체 지도** 구축을 결정했다.
- **OpenStreetMap(OSM)**이 충분히 견고해진 시점(2019년 전후)을 활용해, OSM을 베이스로 하고 **실제 탑승 데이터**로 보강하는 방식으로 Lyft Maps를 만들었다.
- 자체 지도로 전환한 뒤 **전체 탑승의 약 70%**를 Lyft Maps로 처리하고 있으며, 기사 만족도(98% 유지율)와 라이드쉐어 전용 기능 확장으로 경험과 비용을 동시에 관리하고 있다.

제3자 지도에 의존하는 제품을 만들거나 비용·데이터 주권을 고민하는 팀에게, Lyft의 OSM 기반 자체 지도 사례는 좋은 참고가 된다.

---

## 참고 문헌

1. **Lyft's Secret Plan to Take Control of Its Maps — And Its Future.** Lyft.  
   [https://www.lyft.com/rev/posts/lyfts-secret-plan-to-take-control-of-its-maps-and-its-future](https://www.lyft.com/rev/posts/lyfts-secret-plan-to-take-control-of-its-maps-and-its-future)

2. **How Lyft Creates Hyper-Accurate Maps from Open-Source Maps and Real-Time Data.** Lyft Engineering.  
   [https://eng.lyft.com/how-lyft-creates-hyper-accurate-maps-from-open-source-maps-and-real-time-data-8dcf9abdd46a](https://eng.lyft.com/how-lyft-creates-hyper-accurate-maps-from-open-source-maps-and-real-time-data-8dcf9abdd46a)

3. **How Lyft discovered OpenStreetMap is the Freshest Map for Rideshare.** Lyft Engineering.  
   [https://eng.lyft.com/how-lyft-discovered-openstreetmap-is-the-freshest-map-for-rideshare-a7a41bf92ec](https://eng.lyft.com/how-lyft-discovered-openstreetmap-is-the-freshest-map-for-rideshare-a7a41bf92ec)
