---
draft: false
collection_order: 10
slug: hardware-fundamentals
title: "[Android Hardware] 01. 하드웨어 기초"
date: 2026-07-18
last_modified_at: 2026-07-18
description: "SoC와 Cortex-A big.LITTLE 구조, GPU·NPU, LPDDR·UFS 메모리 계층, 무선 연결성, 센서·디스플레이, DVFS·열 관리까지 안드로이드 단말 하드웨어의 핵심 구성 요소를 이론 중심으로 정리한다."
categories: Android Hardware Development
tags:
- Android
- Embedded(임베디드)
- Hardware(하드웨어)
- Kernel
- Linux(리눅스)
- Mobile(모바일)
- Performance(성능)
- Memory(메모리)
- CPU(Central Processing Unit)
- Networking
- System-Design
- Deep-Dive
- Advanced
- SoC
- ARM-Architecture
- Cortex-A
- big.LITTLE
- GPU
- NPU
- Mali
- Adreno
- PowerVR
- LPDDR5
- UFS
- eMMC
- 5G
- Wi-Fi
- Bluetooth
- NFC
- OLED
- DVFS
- Thermal-Management
- HAL
- NNAPI
---

## 이 장을 읽기 전에

이 장은 이 컬렉션의 첫 기술 챕터다. 바로 앞서 읽어야 할 챕터는 [00장: 과정 개요와 커리큘럼](/post/android-hardware-development/getting-started-android-hardware-development/)이며, 그 장에서 제시한 전체 로드맵 중 "Phase 1: 기초 이론"의 출발점이 이 장이다.

난이도는 입문(초급)에서 시작해 절 후반부(전력 관리, 실전 적용)로 갈수록 중급 수준까지 올라간다. ARM 어셈블리나 리눅스 커널 소스를 직접 읽어본 경험이 없어도 따라갈 수 있도록 개념을 정의하지만, C/C++ 문법과 기본적인 운영체제 개념(프로세스, 스레드, 인터럽트)은 이미 안다고 가정한다.

이 장은 하드웨어 구성 요소가 "무엇이고 왜 그렇게 설계되었는가"를 다룬다. 그 하드웨어 위에서 안드로이드 소프트웨어 스택이 어떻게 구동되는지(부트 프로세스, HAL, ART, Zygote 등)는 [02장: 안드로이드 아키텍처](/post/android-hardware-development/android-architecture/)의 범위이고, 커널 드라이버를 직접 작성하는 방법은 3장과 7장, 전력 관리 정책을 커널 레벨에서 튜닝하는 방법은 9장(성능 최적화)에서 다룬다. 이 장에서 SoC나 DVFS를 언급할 때는 어디까지나 "이런 하드웨어 메커니즘이 존재한다"는 지식이지, 그것을 조작하는 코드 작성법은 아니다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| 처음 접하는 독자 | 도입, 핵심 개념 전체, 흔한 오개념 | SoC·GPU·NPU·메모리·무선·센서·전력이라는 7개 축으로 하드웨어를 분해해서 볼 수 있게 된다 |
| 임베디드/모바일 경험자 | 핵심 개념(빠르게 훑기), 비교/트레이드오프, 실전 적용, 비판적 시각 | 안드로이드 생태계 특유의 제약(HAL 경계, Treble, 열 상태 API)을 기존 지식에 연결한다 |
| 하드웨어 스펙 결정권자 | 비교/트레이드오프, 비판적 시각 | 벤치마크 수치 이면의 트레이드오프를 읽고 스펙 문서의 과장을 걸러낼 판단 기준을 얻는다 |

## 도입

스마트폰 하드웨어 스펙 시트를 처음 읽는 사람은 "옥타코어 3.2GHz", "12GB RAM", "AI 엔진 45TOPS" 같은 숫자의 나열에 압도되기 쉽다. 문제는 이 숫자들이 서로 독립적이지 않다는 데 있다. 코어 개수를 늘리면 전력 소모와 발열이 늘고, 발열이 늘면 DVFS(Dynamic Voltage and Frequency Scaling, 동적 전압-주파수 조정)가 개입해 정작 그 코어의 실사용 클럭을 낮춰버린다. NPU 연산 성능(TOPS)이 아무리 높아도 그 위에서 도는 모델이 양자화되지 않았다면 병목은 여전히 CPU에 남는다. 안드로이드 하드웨어 개발자, 또는 안드로이드 위에서 하드웨어 성능을 최대한 끌어내야 하는 애플리케이션·시스템 엔지니어에게 필요한 것은 개별 부품의 스펙 암기가 아니라, 이 부품들이 왜 지금과 같은 형태로 설계되었고 서로 어떻게 제약을 주고받는지에 대한 구조적 이해다.

이 장은 안드로이드 단말을 구성하는 하드웨어를 SoC(연산), 메모리·스토리지(데이터), 연결성(통신), 센서·디스플레이(입출력), 전력 관리(제약 조건)라는 다섯 축으로 나누어 각각의 설계 원칙을 다룬다. 이후 장에서 커널 드라이버를 작성하거나 HAL을 구현하거나 성능을 튜닝할 때, "이 레지스터가 왜 존재하는가", "이 API가 왜 이런 제약을 두는가"에 대한 답은 대부분 이 장에서 다루는 하드웨어 특성에서 나온다.

## 핵심 개념

### SoC와 CPU 코어 설계: ARM Cortex-A와 big.LITTLE

**SoC(System on Chip, 시스템온칩)**는 CPU, GPU, NPU, 모뎀, 이미지 신호 처리기(ISP), 메모리 컨트롤러 등 과거 별도 칩으로 존재하던 기능 블록들을 하나의 다이(die) 위에 집적한 반도체다. 스마트폰이 데스크톱 PC와 달리 손바닥 크기의 배터리 구동 기기 안에 이 모든 연산 자원을 담을 수 있는 이유는, 각 기능 블록 사이의 데이터 이동 거리가 짧아져 전력 소모와 지연시간이 줄어드는 SoC 특유의 집적 이점 때문이다. 현재 안드로이드 SoC 시장은 Qualcomm(Snapdragon), Samsung(Exynos), MediaTek(Dimensity), Google(Tensor) 등이 주도하며, 이들 대부분이 CPU 코어 설계는 Arm의 IP(지적재산)를 라이선스하거나 그 명령어 집합 아키텍처(ISA)를 구현한다.

**Cortex-A(코어텍스-A)**는 Arm이 설계해 라이선스하는 애플리케이션 프로세서용 코어 제품군이다. 스마트폰 SoC 안의 CPU 코어는 이 Cortex-A 설계를 그대로 쓰거나(예: Cortex-X/A 시리즈), 또는 Arm의 ISA 라이선스를 받아 벤더가 직접 마이크로아키텍처를 설계한 커스텀 코어(예: Qualcomm의 Oryon, 과거 Kryo)를 쓴다. 어느 쪽이든 명령어 집합은 Armv8-A 이상(대부분 AArch64, 64비트)을 따르므로, 안드로이드 네이티브 코드를 작성할 때 타깃 ABI는 사실상 `arm64-v8a`로 통일되어 있다고 봐도 무방하다.

**big.LITTLE**은 서로 다른 성능·전력 특성을 가진 두 종류 이상의 코어 클러스터를 한 SoC에 함께 배치하고, 워크로드에 따라 스케줄러가 작업을 적절한 클러스터로 옮기는 이기종 멀티프로세싱(heterogeneous multi-processing) 아키텍처다. "big" 코어는 더 깊은 파이프라인과 더 넓은 실행 유닛으로 높은 단일 스레드 성능을 내지만 그만큼 전력을 많이 쓰고, "LITTLE" 코어는 성능은 낮지만 유휴 상태에 가까운 저전력 작업(백그라운드 동기화, 알림 처리 등)을 효율적으로 처리한다. 최신 모바일 SoC는 이를 한 단계 더 세분화해 Prime(초고성능) - Performance(고성능) - Efficiency(저전력) 3단 구조를 쓰는 경우가 많으며, 이 구조를 리눅스 커널이 CPU 토폴로지 정보로 인식하고 스케줄러(대표적으로 EAS, Energy Aware Scheduling)가 태스크별 부하를 예측해 코어를 배정한다. 이 배정 로직은 커널 영역이라 앱 개발자가 직접 건드릴 일은 드물지만, NDK 레벨에서 스레드를 특정 코어에 고정(affinity)하려는 시도를 할 때는 이 클러스터 구조를 반드시 이해하고 있어야 한다.

### GPU: Mali·Adreno·PowerVR와 그래픽 파이프라인

**GPU(Graphics Processing Unit)**는 수천 개의 단순 연산 유닛을 병렬로 동작시켜 픽셀·정점 연산이나 행렬 연산처럼 대규모로 병렬화 가능한 작업을 처리하는 프로세서다. 안드로이드 생태계의 모바일 GPU는 크게 세 계보로 나뉜다. Arm이 설계해 여러 SoC 벤더(삼성 Exynos, MediaTek 등)에 라이선스하는 **Mali**, Qualcomm이 Snapdragon에 자체 통합하는 **Adreno**, 그리고 Imagination Technologies가 설계하고 과거 Apple·삼성 일부 라인업과 현재도 일부 MediaTek·전용 임베디드 SoC에서 쓰이는 **PowerVR**이다. 세 계보 모두 타일 기반 지연 렌더링(Tile-Based Deferred Rendering, TBDR) 방식을 채택하는데, 이는 화면을 작은 타일로 나눠 각 타일에 필요한 그리기 연산만 온칩 메모리에서 처리한 뒤 결과를 외부 메모리(LPDDR)에 한 번에 기록하는 방식으로, 데스크톱 GPU의 즉시 모드 렌더링(Immediate Mode Rendering)보다 메모리 대역폭 소모가 훨씬 적다. 모바일 기기가 배터리로 구동되면서도 고해상도 그래픽을 처리할 수 있는 것은 이 TBDR 구조 덕분이다.

안드로이드 프레임워크는 GPU 벤더가 어떤 하드웨어를 쓰든 동일한 방식으로 그래픽을 요청할 수 있도록 **OpenGL ES**와 **Vulkan**이라는 표준 API를 제공한다. 각 SoC 벤더는 이 API 표준에 맞춰 자사 GPU용 드라이버를 HAL 형태로 구현해 공급하며, 실제 성능은 같은 API 호출이라도 드라이버 최적화 수준에 따라 벤더별로 상당한 차이가 난다. Vulkan은 OpenGL ES 대비 CPU 드라이버 오버헤드를 낮추고 멀티스레드 커맨드 생성을 명시적으로 지원하도록 설계되어, 고성능 게임 엔진일수록 Vulkan 채택 비중이 높아지는 추세다.

### NPU: 온디바이스 AI 가속

**NPU(Neural Processing Unit)**는 신경망 추론에 흔히 쓰이는 행렬 곱셈과 컨볼루션 연산을 저정밀도(INT8, FP16 등)로 대량 병렬 처리하도록 특화된 전용 연산 유닛이다. CPU는 범용성이 높지만 이런 반복적 텐서 연산에는 비효율적이고, GPU는 병렬성은 뛰어나지만 여전히 그래픽 파이프라인에 최적화된 구조라 전력 대비 추론 효율에서 NPU에 못 미친다. 그래서 최신 SoC는 카메라의 실시간 장면 인식, 음성 인식의 웨이크워드 감지, 카메라 이미지 후처리(야간모드 합성 등)처럼 지연시간과 전력 효율이 모두 중요한 작업을 NPU로 오프로드한다.

다만 NPU 하드웨어가 있다고 해서 모델이 자동으로 빨라지지는 않는다는 점이 중요하다. 안드로이드는 NPU·GPU·DSP 같은 다양한 가속기를 앱이 벤더 종속 없이 활용할 수 있도록 Neural Networks API(NNAPI)라는 추상화 계층을 오랫동안 제공해 왔지만, 안드로이드 공식 문서는 NNAPI가 Android 15부터 지원 중단(deprecated)되었으며 성능이 중요한 워크로드는 LiteRT(과거 명칭 TensorFlow Lite)의 GPU/NPU 델리게이트 같은 대체 경로로 이전할 것을 권장한다고 명시한다. 즉 "NPU 탑재"라는 스펙 문구는 하드웨어 존재를 의미할 뿐, 그 가속기에 도달하는 소프트웨어 경로(모델 포맷, 양자화, 델리게이트 지원 여부)가 갖춰져 있는지는 별도로 확인해야 하는 문제다.

### 메모리 계층: LPDDR4/5

**LPDDR(Low Power Double Data Rate)**는 모바일·임베디드 기기를 위해 표준화된 저전력 DRAM 규격으로, JEDEC(반도체 표준화 기구)이 세대별 규격을 정의한다. 데스크톱용 DDR 메모리와 근본 원리(양쪽 에지에서 데이터를 전송하는 더블 데이터 레이트)는 같지만, 배터리 구동 환경에 맞춰 동작 전압을 낮추고, 사용하지 않는 뱅크를 빠르게 저전력 상태로 전환하는 절전 모드를 세분화했다는 점이 다르다. LPDDR5는 LPDDR4 대비 핀당 데이터 전송 속도(대역폭)를 크게 끌어올리면서 동작 전압은 더 낮췄고, 이는 고해상도 카메라 버스트 촬영이나 다중 앱 전환처럼 순간적으로 큰 메모리 대역폭을 요구하는 워크로드에서 체감 성능 차이로 이어진다.

메모리 성능을 이야기할 때 대역폭(bandwidth)과 지연시간(latency)을 혼동하지 않는 것이 중요하다. 대역폭은 단위 시간당 옮길 수 있는 데이터양이고, 지연시간은 요청 후 첫 데이터가 도착하기까지 걸리는 시간이다. 그래픽 렌더링처럼 연속된 대량 데이터를 순차적으로 처리하는 워크로드는 대역폭에 민감하고, 포인터를 따라가며 흩어진 메모리를 무작위로 접근하는 워크로드(예: 가비지 컬렉션의 객체 그래프 순회)는 지연시간에 더 민감하다. 안드로이드 런타임(ART)의 GC 튜닝이나 게임 엔진의 메모리 배치 전략이 서로 다른 이유 중 하나가 여기에 있다.

### 스토리지: UFS와 eMMC

**UFS(Universal Flash Storage)**와 **eMMC(embedded MultiMediaCard)**는 모두 NAND 플래시 메모리를 SoC에 내장 실장하는 규격이지만, 데이터 전송 인터페이스의 구조가 근본적으로 다르다. eMMC는 데스크톱 저장장치의 조상 격인 병렬 버스 기반 프로토콜을 계승해 명령을 하나씩 순차 처리하는 반면, UFS는 SCSI 계열 프로토콜을 차용해 직렬(시리얼) 인터페이스 위에서 다중 명령 큐(Command Queuing)를 지원한다. 다중 명령 큐가 있으면 저장장치 컨트롤러가 여러 읽기/쓰기 요청을 동시에 받아 내부적으로 우선순위를 재정렬하고 병렬 처리할 수 있어, 특히 여러 앱이 동시에 파일 I/O를 요청하는 멀티태스킹 환경에서 체감 반응성이 크게 개선된다. 이 차이 때문에 최근 중가·플래그십 안드로이드 단말은 대부분 UFS를 채택하고, eMMC는 원가에 더 민감한 보급형 기기나 임베디드 제품에 남아 있다.

### 무선 연결성: 4G/5G, Wi-Fi, 블루투스, NFC

이동통신 모뎀은 SoC와 물리적으로 통합되거나(통합 모뎀) 별도 칩으로 붙는(외장 모뎀) 두 형태로 존재하며, **4G(LTE)**와 **5G**는 무선 접속 기술 세대를 가리키는 표준 규격 명칭이다. 5G는 데이터 처리량과 지연시간 개선에 더해, 저주파 대역(Sub-6GHz)과 초고주파 대역(mmWave)을 모두 정의하는데, mmWave는 이론상 훨씬 빠른 속도를 내지만 직진성이 강해 장애물에 매우 취약하므로 실제 상용 단말의 커버리지 전략에서 채택 비중이 지역별로 갈린다. **Wi-Fi**는 IEEE 802.11 표준 계열을 따르며 세대가 올라갈수록(예: 이전 세대 대비 최신 세대) 다중 사용자 환경에서의 동시 처리 효율과 지연시간이 개선되는 방향으로 발전해 왔다. **블루투스(Bluetooth)**는 저전력 근거리 무선 통신 표준으로, 특히 Bluetooth Low Energy(BLE)는 웨어러블 기기나 IoT 센서처럼 배터리 수명이 최우선인 기기와의 연결에 널리 쓰인다. **NFC(Near Field Communication)**는 통신 거리가 수 센티미터로 극히 짧은 대신 페어링 절차 없이 즉시 통신이 시작되는 특성 때문에 모바일 결제나 기기 간 즉석 페어링(태그 앤 커넥트)에 활용된다.

이 무선 모듈들은 모두 안테나·전력 증폭기 같은 RF(무선 주파수) 프론트엔드를 공유하거나 인접 배치하기 때문에, 여러 모듈이 동시에 송수신하면 상호 간섭이 발생할 수 있다. SoC와 모뎀 벤더가 안테나 튜닝과 공존(coexistence) 알고리즘에 상당한 엔지니어링 자원을 투입하는 이유가 여기에 있으며, 이는 순수 소프트웨어 계층에서는 잘 드러나지 않는 하드웨어 설계의 숨은 난제다.

### 센서와 디스플레이

스마트폰에 흔히 탑재되는 센서로는 가속도계(움직임), 자이로스코프(회전), 지자기 센서(방위), 근접 센서(화면 근접 여부), 조도 센서(주변 밝기), 지문 인식 센서, 그리고 카메라 모듈의 핵심인 이미지 센서(CMOS)가 있다. 안드로이드 프레임워크는 이 물리 센서들의 원시 데이터를 결합해 방향(orientation), 걸음 수(step counter)처럼 더 높은 수준의 의미를 갖는 값을 만들어내는데, 이 결합 과정을 **센서 퓨전(sensor fusion)**이라 부른다. 센서 퓨전의 상당 부분은 저전력 보조 프로세서(센서 허브)에서 처리되어, AP(애플리케이션 프로세서)가 매번 깨어나지 않고도 백그라운드 모션 감지 같은 저빈도 작업을 처리할 수 있게 한다.

디스플레이는 크게 **LCD(Liquid Crystal Display)**와 **OLED(Organic Light Emitting Diode)** 두 방식으로 나뉜다. LCD는 백라이트가 패널 전체를 비추고 액정이 빛을 선택적으로 차단해 화면을 구성하는 방식이라 완전한 검은색을 표현할 때도 백라이트가 켜져 있어야 하지만, OLED는 픽셀 하나하나가 스스로 발광하므로 검은 화면에서는 해당 픽셀을 아예 꺼서 이론상 완전한 검은색과 더 높은 명암비를 얻을 수 있다. 이 차이는 전력 소비 패턴에도 그대로 반영되어, 어두운 배경 위주의 UI(다크 모드)에서는 OLED가 LCD보다 소비 전력이 낮아지는 경향이 있는 반면 밝고 흰 화면이 많은 콘텐츠에서는 그 격차가 줄거나 역전될 수 있다.

## 비교와 트레이드오프

앞서 다룬 구성 요소들은 하나의 정답이 있는 것이 아니라, 목표로 하는 제품 포지션(플래그십, 중가형, 웨어러블 등)에 따라 서로 다른 선택이 합리적인 트레이드오프 영역이다. 아래 표는 스토리지 규격 선택의 판단 기준을 정리한 것이다.

| 항목 | UFS | eMMC |
|---|---|---|
| 인터페이스 | 직렬(SCSI 계열), 전이중(Full-Duplex) | 병렬 버스, 반이중(Half-Duplex) |
| 명령 처리 | 다중 명령 큐(동시 처리) | 단일 명령 순차 처리 |
| 랜덤 I/O 성능 | 상대적으로 높음 | 상대적으로 낮음 |
| 원가 | 상대적으로 높음 | 상대적으로 낮음 |
| 주 사용처 | 플래그십·중가형 스마트폰 | 보급형 기기, 임베디드·IoT |

스토리지를 선택할 때의 판단 기준은 단순히 "더 빠른 쪽"이 아니라 워크로드 패턴이다. 앱 전환이 잦고 여러 프로세스가 동시에 파일에 접근하는 범용 스마트폰 UX에서는 UFS의 다중 큐가 체감 반응성에 직결되지만, 정해진 소수의 프로세스가 순차적으로 데이터를 기록하는 임베디드 로깅 기기라면 eMMC로도 병목이 거의 발생하지 않으면서 원가를 절감할 수 있다.

CPU 코어 구성에서도 유사한 판단이 필요하다. big.LITTLE(또는 3단 Prime/Performance/Efficiency) 구조에서 big 코어 비중을 늘리면 벤치마크 점수는 올라가지만 다이 면적과 발열 예산을 더 많이 소모하므로, 실사용 시간의 대부분을 차지하는 저강도 작업(스크롤, 메시징, 백그라운드 동기화)의 효율이 오히려 희생될 수 있다. 반대로 LITTLE 코어 비중이 지나치게 높으면 배터리 수명은 늘지만 카메라 버스트 촬영이나 앱 콜드 스타트처럼 순간적인 고성능이 필요한 구간에서 체감 지연이 커진다. SoC 설계사가 코어 구성을 발표할 때 함께 공개하는 "예상 사용 시나리오별 부하 분포" 데이터가 바로 이 트레이드오프를 어떻게 절충했는지 보여주는 지표다.

## 실전 적용

카메라 버스트 촬영 기능을 만드는 상황을 가정해 보자. 이 기능은 짧은 시간에 다수의 프레임을 캡처하고 각 프레임에 후처리(HDR 합성 등)를 적용해야 하므로, 순간적으로 CPU big 코어와 메모리 대역폭을 크게 요구한다. 동시에 이 작업이 오래 지속되면 발열이 누적되어 열 조절(thermal throttling)이 개입할 수 있으므로, 애플리케이션이 열 상태를 감지하고 그에 맞춰 촬영 파이프라인의 강도를 조절하는 것이 바람직하다.

안드로이드 프레임워크는 `PowerManager`를 통해 기기의 열 상태 변화를 구독할 수 있는 공식 API를 제공한다. 아래 코드는 열 상태가 `THERMAL_STATUS_SEVERE` 이상으로 올라가면 버스트 촬영의 프레임 수를 줄이도록 반응하는 리스너를 등록하는 예다.

```kotlin
import android.content.Context
import android.os.Build
import android.os.PowerManager
import java.util.concurrent.Executor

class ThermalAwareBurstController(
    private val context: Context,
    private val executor: Executor
) {
    private val powerManager: PowerManager =
        context.getSystemService(Context.POWER_SERVICE) as PowerManager

    // 열 상태에 따라 버스트 촬영 프레임 수를 결정한다.
    @Volatile
    var burstFrameCount: Int = 8
        private set

    private val thermalListener = PowerManager.OnThermalStatusChangedListener { status ->
        burstFrameCount = when (status) {
            PowerManager.THERMAL_STATUS_NONE,
            PowerManager.THERMAL_STATUS_LIGHT -> 8
            PowerManager.THERMAL_STATUS_MODERATE -> 4
            PowerManager.THERMAL_STATUS_SEVERE,
            PowerManager.THERMAL_STATUS_CRITICAL,
            PowerManager.THERMAL_STATUS_EMERGENCY,
            PowerManager.THERMAL_STATUS_SHUTDOWN -> 1
            else -> burstFrameCount
        }
    }

    fun start() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            powerManager.addThermalStatusListener(executor, thermalListener)
        }
    }

    fun stop() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            powerManager.removeThermalStatusListener(thermalListener)
        }
    }
}
```

이 리스너는 Android 10(API 29)부터 제공되는 `addThermalStatusListener` API를 사용하며, 기기가 `THERMAL_STATUS_SEVERE` 이상으로 판단되면 즉시 버스트 프레임 수를 1로 줄여 SoC의 부하를 낮춘다. 여기서 중요한 점은 이 API가 벤더마다 다른 실제 온도 센서 값을 직접 노출하지 않고, Thermal HAL이 산출한 추상화된 심각도 등급만 앱에 전달한다는 것이다. 즉 어떤 SoC를 쓰든 앱 코드는 동일하게 동작하며, 실제 임계 온도값 튜닝은 기기 제조사가 Thermal HAL 설정으로 담당한다.

프레임워크 API로 열 상태에 "반응"하는 것과 별개로, NDK 레벨에서 특정 워크로드를 big 코어에 우선 배치하고 싶을 때는 리눅스의 CPU 어피니티(affinity) 메커니즘을 사용할 수 있다. 아래는 `sched_setaffinity`로 현재 스레드를 지정한 CPU 코어 집합에 고정하는 예다. 실제 어떤 코어 번호가 big 클러스터인지는 기기마다 다르므로, 프로덕션 코드에서는 `/sys/devices/system/cpu/cpu*/cpufreq/cpuinfo_max_freq`를 읽어 최대 클럭이 높은 코어를 동적으로 판별해야 하며, 여기서는 판별 로직을 함수로 분리해 흐름만 보여준다.

```c
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

// /sys/devices/system/cpu/cpu{N}/cpufreq/cpuinfo_max_freq 값을 비교해
// 최대 클럭이 가장 높은 코어 번호 집합을 채운다고 가정한 판별 함수.
// 실제 구현은 파일 파싱이 필요하므로 여기서는 시그니처만 제공한다.
int find_big_cores(int *out_core_ids, int max_count);

int pin_current_thread_to_big_cores(void) {
    int big_cores[8];
    int found = find_big_cores(big_cores, 8);
    if (found <= 0) {
        return -1;
    }

    cpu_set_t cpu_set;
    CPU_ZERO(&cpu_set);
    for (int i = 0; i < found; i++) {
        CPU_SET(big_cores[i], &cpu_set);
    }

    // pid 0은 "현재 호출 스레드"를 의미한다.
    if (sched_setaffinity(0, sizeof(cpu_set_t), &cpu_set) != 0) {
        perror("sched_setaffinity");
        return -1;
    }
    return 0;
}
```

이 방식은 즉각적인 제어가 가능하지만 두 가지 주의점이 있다. 첫째, 코어 어피니티를 과도하게 강제하면 안드로이드 스케줄러(EAS)의 전역 최적화 판단을 무력화해 오히려 시스템 전체의 전력 효율이 떨어질 수 있으므로, 실시간성이 극도로 중요한 짧은 구간에서만 제한적으로 쓰는 것이 안전하다. 둘째, 코어 번호와 클러스터의 대응 관계는 SoC와 안드로이드 버전에 따라 달라지는 구현 정의 영역이므로, 코어 번호를 하드코딩하지 않고 반드시 런타임에 판별해야 한다.

## 흔한 오개념

**"코어 개수가 많을수록, 클럭이 높을수록 무조건 빠르다"**는 가장 흔한 오해다. 실제 체감 성능은 그 코어들이 얼마나 오래 최대 클럭을 유지할 수 있는지(지속 성능, sustained performance)에 더 크게 좌우된다. 발열 예산이 부족한 얇은 폼팩터의 기기는 스펙 시트상 클럭이 높아도 DVFS가 몇 초 만에 클럭을 끌어내리는 경우가 흔하며, 이는 짧은 벤치마크 점수와 실사용 체감 성능이 크게 벌어지는 대표적 원인이다.

**"NPU/AI 엔진이 있으면 온디바이스 AI 기능이 자동으로 빨라진다"**도 흔한 착각이다. NPU는 특정 연산 패턴(양자화된 텐서 연산 등)에 최적화된 하드웨어일 뿐이며, 그 위에서 돌아갈 모델이 해당 하드웨어의 델리게이트를 지원하는 포맷으로 변환·양자화되어 있지 않으면 실행은 자동으로 CPU 또는 GPU로 폴백된다. 게다가 안드로이드는 NNAPI를 Android 15부터 지원 중단했으므로, "NPU 탑재 = AI 가속 보장"이 아니라 "NPU에 도달하는 소프트웨어 경로가 갖춰졌는가"를 함께 확인해야 한다.

**"OLED는 항상 LCD보다 전력 효율이 좋다"**는 절반만 맞는 말이다. OLED는 어두운 화면에서 유리하지만, 흰 배경이 많은 문서 뷰어나 밝은 사진 편집 화면에서는 모든 픽셀이 최대 밝기로 발광해야 하므로 오히려 LCD의 균일한 백라이트 방식보다 전력을 더 소비할 수 있다. 두 방식의 우열은 패널 자체의 절대적 성능이 아니라 실제로 표시되는 콘텐츠의 성격에 좌우된다.

## 비판적 시각

이 장에서 다룬 스펙들은 제조사 발표 자료의 최댓값(peak) 기준인 경우가 대부분이라는 한계를 감안해서 읽어야 한다. GPU의 이론적 최대 연산 성능(TFLOPS)이나 모뎀의 이론적 최대 다운로드 속도는 실험실 조건에서의 상한선이며, 실사용 환경에서는 발열, 전파 환경, 동시 실행 앱 개수 같은 변수 때문에 그 수치에 도달하는 경우가 오히려 드물다. 특히 지속 성능(sustained performance)과 순간 최대 성능(burst performance)을 구분하지 않고 스펙을 비교하는 관행은 업계 전반에서 자주 지적되어 온 문제이며, 벤치마크 앱을 감지해 그 순간에만 성능 제한을 완화하는 최적화 관행이 여러 차례 언론과 커뮤니티의 논란 대상이 되기도 했다. 하드웨어를 다루는 개발자라면 제조사가 공개한 단일 수치보다, 지속 워크로드에서의 클럭 추이나 프레임 타임 분포처럼 시간축을 포함한 데이터를 신뢰하는 습관을 들이는 편이 낫다.

또한 이 장에서 소개한 벤더 구도(Mali/Adreno/PowerVR, Qualcomm/Samsung/MediaTek 등)는 시장 상황에 따라 계속 바뀐다는 점도 유념해야 한다. 특정 세대에 특정 벤더가 우위를 점했다는 평가는 그 시점의 공정 미세화 수준, 드라이버 성숙도, 발열 설계에 따라 다음 세대에 뒤집히는 일이 잦았다. 따라서 이 장의 목적은 "어느 벤더가 낫다"를 암기하는 것이 아니라, 어떤 기준(지속 성능, 전력 효율, 소프트웨어 생태계 지원)으로 하드웨어를 평가해야 하는지를 익히는 데 있다.

## 다음 장에서는

[02장: 안드로이드 아키텍처](/post/android-hardware-development/android-architecture/)에서는 이 장에서 다룬 하드웨어 위에 안드로이드 소프트웨어 스택이 어떻게 얹히는지, 리눅스 커널부터 HAL, ART, 프레임워크, 시스템 앱까지 이어지는 레이어 구조와 부트 프로세스를 다룬다.

## 평가 기준

이 장을 읽은 후에는 다음을 할 수 있어야 한다.

- SoC, GPU, NPU가 각각 어떤 연산 패턴에 최적화되어 있는지 설명할 수 있다.
- big.LITTLE(또는 3단 코어) 구조가 왜 필요한지, 그리고 스케줄링이 커널·프레임워크 어느 계층의 책임인지 구분할 수 있다.
- UFS와 eMMC의 구조적 차이를 명령 큐 관점에서 설명하고, 어떤 제품 시나리오에 어느 쪽이 적합한지 판단할 수 있다.
- LPDDR 메모리에서 대역폭과 지연시간이 서로 다른 워크로드에 어떻게 영향을 주는지 구분할 수 있다.
- `PowerManager`의 열 상태 API가 왜 실제 온도값이 아닌 추상화된 등급을 노출하는지 설명할 수 있다.
- 스펙 시트의 최대 성능 수치와 실사용 지속 성능이 왜 다를 수 있는지, DVFS와 열 관리의 관점에서 설명할 수 있다.

## 참고 및 출처

- Google, "Hardware Abstraction Layer (HAL)", Android Open Source Project, source.android.com/docs/core/architecture/hal
- Google, "Thermal Mitigation", Android Open Source Project, source.android.com/docs/core/power/thermal-mitigation
- Google, "Power Profiles for Android", Android Open Source Project, source.android.com/docs/core/power
- Google, "Neural Networks API", Android NDK 문서, developer.android.com/ndk/guides/neuralnetworks
- Arm, "big.LITTLE Technology", arm.com/technologies/big-little
