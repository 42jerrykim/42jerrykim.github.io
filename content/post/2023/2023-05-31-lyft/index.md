---
image: "tmp_wordcloud.png"
categories: Lyft
date: "2023-05-31T00:00:00Z"
header:
  teaser: /assets/images/2023/LyftMaps_ImageHeader_01.jpg
tags:
- Lyft
- Maps
- OpenStreetMap
- Google Maps
- In-house development
- Navigation
- Drivers
- Passengers
- Experience
- Features
- Cost efficiency
- Safety
- Real-time updates
- Feedback
- Route optimization
title: '[Lyft] Lyft의 비밀스러운 계획: 자체 지도와 미래를 통제하다'
---

안녕하세요, 여러분! 오늘은 Lyft와 OpenStreetMap에 대한 흥미로운 주제를 다루려고 합니다. Lyft가 자체 지도 시스템을 구축하려는 이유와 그 방법, 그리고 이것이 어떻게 회사의 미래에 영향을 미칠 것인지에 대해 알아보겠습니다. 또한, 이 모든 것이 가능하게 한 OpenStreetMap에 대해서도 이야기하겠습니다.

![](/assets/images/2023/LyftMaps_ImageHeader_01.jpg)

> [https://www.lyft.com/rev/posts/lyfts-secret-plan-to-take-control-of-its-maps-and-its-future](https://www.lyft.com/rev/posts/lyfts-secret-plan-to-take-control-of-its-maps-and-its-future)의 내용을 참고 하였습니다.

## Lyft와 Google Maps

Lyft 앱을 사용하는 수백만 명의 운전자와 승객들은 매일 지도를 보며 이동 경로를 파악하거나 목적지까지 얼마나 걸릴지, 운전자가 얼마나 멀리 떨어져 있는지 등을 확인합니다. 그러나, Lyft는 최근까지 이러한 내비게이션 경험을 통제할 수 없었습니다. 왜냐하면 이 모든 것이 Google Maps를 기반으로 구축되었기 때문입니다.

Lyft는 승객이나 운전자 경험을 향상시킬 수 있는 수백 가지 이상의 기능 목록을 수집했지만, 그것들을 실행하는 데 있어서는 무력했습니다. 게다가, 제3자 기술에 의존하는 것은 비용이 많이 들었습니다. Lyft는 자체 알고리즘을 사용하여 탑승 시간과 비용을 예측했지만, 탑승이 승인되면 Google이 내비게이션을 인수하고 때때로 그 경로가 Lyft가 계산한 경로와 다를 때가 있었습니다.

## Lyft의 자체 지도 계획

2019년, Lyft 엔지니어들은 회사가 내비게이션 경로를 제안하면 큰 절약을 가져올 수 있다고 판단했습니다. 이는 Google에 지불하는 돈을 절약하거나 더 안전한 라이드쉐어 경험을 만드는 잠재적인 효과를 포함하지 않았습니다. 자체 제작 지도는 Lyft가 매일 플랫폼 전체에서 발생하는 수백만 건의 탑승을 곱하면 엄청난 양의 돈을 절약할 수 있었습니다.

그러나 Lyft의 역사 대부분 동안 해결책은 없었습니다. Google과 Apple은 수십억 달러를 투자하고 여러 년에 걸쳐 자신들의 지도를 만들었습니다. 상대적으로 작은 회사인 Lyft가 그 노력을 복제하는 것은 부담스러웠습니다. 그러나 몇 년 전, Lyft는 자체 지도를 만드는데 성공하였고, 그 이후로 Lyft 플랫폼에서 모든 탑승의 70%를 지원하게 되었습니다.

## OpenStreetMap의 역할

2019년에 돌파구가 왔습니다. Lyft 팀은 OpenStreetMap (OSM) 플랫폼이 드디어 Lyft의 지도를 지원하기에 충분히 견고해졌다고 판단했습니다. OSM은 2004년에 영국 학자가 만든 무료이며 오픈소스인 Google과 Apple Maps의 대안이었습니다. 이는 지도의 위키백과와 같은 것으로, 자원봉사자들이 지리적 정보를 중앙 데이터베이스에 기여하고, 그 정보를 누구나 무료로 접근할 수 있게 하는 시스템이었습니다.

Lyft는 또한 매일 가장 많이 이용되는 거리를 여러 번 운행하는 Lyft 탑승의 데이터라는 또 다른 귀중한 자원을 가지고 있었습니다. 이를 통해 회사는 도로 폐쇄, 공사, 또는 다른 장애물에 대한 정보를 업데이트하는 데 필요한 데이터를 수집할 수 있었습니다.

## Lyft의 지도 시스템 구축

2019년 말에는, 팀은 "불가능한" 것을 해내기 위해 준비가 되었습니다 - 자체 제작 지도 시스템을 만들기 위해 준비가 되었던 것이죠. 그들은 앱의 경험을 운전자와 승객에게 더욱 원활하게 만들기 위해 열심히 일했습니다.

Lyft는 지도를 재구성하여 운전자가 내비게이션에 집중하고 승객을 픽업할 수 있도록 불필요한 상점, 레스토랑, 근처 목적지 등의 혼란스러운 요소를 제거했습니다. 또한 실제 세계의 업데이트를 통합하여, 예를 들어, 운전자가 교통 체증에 빠져 있다면 승객에게 이를 알리는 등의 기능을 추가했습니다.

## Lyft 맵의 새로운 기능과 개선

이제 팀이 성공적인 매핑 제품을 만들었으므로, 그들은 어떤 다른 타기 공유 특화 기능들이 이를 독특하게 만들 수 있을지, 그리고 운전 및 탑승 경험을 어떻게 개선할 수 있을지에 대해 생각하기 시작하였습니다. 그들이 추구하고 있는 몇 가지 아이디어들 중에는 기사들이 사고, 교통 체증, 승객 하차 구역 등에 대한 정보를 공유할 수 있는 기능, 탑승자들이 가장 효율적인 루트 대신에 '경치 좋은 루트'를 선택할 수 있는 옵션, 그리고 많은 사람들이 찾는 목적지로의 승차 및 하차 안내 등이 있습니다.

## 결론

Lyft의 지도와 미래를 통제하기 위한 계획은 매우 흥미롭습니다. Lyft는 자체 지도를 만들고, 이를 통해 더 나은 운전자 경험을 제공하려는 계획을 세우고 있습니다. 이를 위해 Lyft는 OpenStreetMap(OSM)과 실시간 데이터를 활용하여 매우 정확한 지도를 만드는 방법을 개발하였습니다. 또한, Lyft는 OpenStreetMap이 라이드쉐어링을 위한 가장 최신의 지도임을 발견하였습니다. 이 모든 것은 Lyft가 운전자와 승객에게 더 나은 경험을 제공하기 위한 노력의 일부입니다. 앞으로 Lyft가 어떻게 발전해 나갈지 기대해 봅니다.

## 참고

* "Lyft's Secret Plan to Take Control of Its Maps and Its Future." Lyft. https://www.lyft.com/rev/posts/lyfts-secret-plan-to-take-control-of-its-maps-and-its-future
* "How Lyft Creates Hyper-Accurate Maps from Open-Source Maps and Real-Time Data." Lyft Engineering. https://eng.lyft.com/how-lyft-creates-hyper-accurate-maps-from-open-source-maps-and-real-time-data-8dcf9abdd46a
* "How Lyft discovered OpenStreetMap is the Freshest Map for Rideshare." Lyft Engineering. https://eng.lyft.com/how-lyft-discovered-openstreetmap-is-the-freshest-map-for-rideshare-a7a41bf92ec