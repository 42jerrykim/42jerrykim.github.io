---
collection_order: 20
draft: true
title: "2. 안드로이드 아키텍처"
description: "안드로이드 운영체제의 전체 아키텍처와 각 레이어 이해"
---

# 2. 안드로이드 아키텍처

## 학습 전략

### 목표
- 안드로이드 소프트웨어 스택의 전체 구조 이해
- 각 레이어의 역할과 상호작용 파악
- AOSP (Android Open Source Project) 구조 분석

### 학습 접근법
1. **아키텍처 분석 (50%)**
   - 안드로이드 레이어별 구조 학습
   - 각 컴포넌트의 역할과 의존성 이해
   - 데이터 흐름 및 제어 흐름 분석

2. **소스 코드 분석 (30%)**
   - AOSP 소스 코드 구조 파악
   - 핵심 컴포넌트 코드 리뷰
   - 빌드 시스템 이해

3. **실습 개발 (20%)**
   - 커스텀 시스템 서비스 개발
   - 네이티브 라이브러리 연동
   - 시스템 앱 개발

## 핵심 학습 내용

### 안드로이드 소프트웨어 스택 개요
- **아키텍처 레이어**
  - 리눅스 커널 레이어
  - 하드웨어 추상화 계층 (HAL)
  - 안드로이드 런타임 (ART)
  - 네이티브 C/C++ 라이브러리
  - 자바 API 프레임워크
  - 시스템 앱 레이어

- **부트 프로세스**
  - 부트로더 → 커널 → init → Zygote → SystemServer
  - 각 단계별 초기화 과정
  - 서비스 시작 순서 및 의존성

### 리눅스 커널 레이어
- **커널 기능**
  - 프로세스 관리 및 스케줄링
  - 메모리 관리 (LMK, ION)
  - 디바이스 드라이버 관리
  - 전력 관리 (Wakelock, Suspend)

- **안드로이드 전용 커널 기능**
  - Binder IPC 메커니즘
  - ashmem (Anonymous Shared Memory)
  - Logger 서브시스템
  - Paranoid Networking

### 하드웨어 추상화 계층 (HAL)
- **HAL 아키텍처**
  - HAL 인터페이스 정의
  - 벤더 구현 분리
  - HIDL (HAL Interface Definition Language)
  - AIDL (Android Interface Definition Language)

- **주요 HAL 모듈**
  - 카메라 HAL
  - 오디오 HAL
  - 그래픽 HAL (Gralloc, HWC)
  - 센서 HAL
  - GPS HAL

### 네이티브 라이브러리
- **핵심 라이브러리**
  - libc (Bionic C Library)
  - libm (Math Library)
  - liblog (Logging Library)
  - libcutils (Common Utilities)

- **미디어 및 그래픽 라이브러리**
  - OpenGL ES / EGL
  - Skia 그래픽 엔진
  - 미디어 프레임워크
  - 카메라 라이브러리

### 안드로이드 런타임 (ART)
- **런타임 특징**
  - AOT (Ahead-of-Time) 컴파일
  - JIT (Just-in-Time) 컴파일
  - 가비지 컬렉션 최적화
  - 프로파일 가이드 최적화

- **Dalvik vs ART**
  - 성능 비교 분석
  - 메모리 사용량 최적화
  - 배터리 수명 개선

### 자바 API 프레임워크
- **시스템 서비스**
  - Activity Manager Service
  - Package Manager Service
  - Location Manager Service
  - Notification Manager Service

- **프레임워크 아키텍처**
  - MVC 패턴 적용
  - Observer 패턴 활용
  - 이벤트 처리 메커니즘
  - 리소스 관리 시스템

### 애플리케이션 레이어
- **시스템 앱**
  - 런처 (Launcher)
  - 설정 (Settings)
  - 연락처 (Contacts)
  - 전화 (Phone)

- **앱 생명주기**
  - Activity 생명주기
  - Service 생명주기
  - BroadcastReceiver 동작
  - ContentProvider 관리

## 실습 프로젝트

### 프로젝트 1: AOSP 빌드 및 분석
- **목표**: AOSP 소스 코드 빌드 및 구조 분석
- **활동**:
  - AOSP 소스 다운로드 및 빌드
  - 각 레이어별 소스 코드 분석
  - 커스텀 시스템 이미지 생성
  - 에뮬레이터에서 실행 테스트

### 프로젝트 2: 커스텀 시스템 서비스 개발
- **목표**: 새로운 시스템 서비스 개발 및 통합
- **활동**:
  - 시스템 서비스 인터페이스 정의
  - 네이티브 서비스 구현
  - 자바 API 래퍼 개발
  - 시스템 앱에서 서비스 활용

### 프로젝트 3: HAL 모듈 개발
- **목표**: 간단한 HAL 모듈 개발 및 테스트
- **활동**:
  - HAL 인터페이스 정의
  - 하드웨어 추상화 구현
  - 프레임워크 통합
  - 기능 테스트 및 검증

## 평가 방법

### 이론 평가 (40%)
- 안드로이드 아키텍처 이해도 시험
- 각 레이어의 역할과 상호작용 분석
- 부트 프로세스 시퀀스 다이어그램 작성

### 실습 평가 (60%)
- AOSP 빌드 성공 및 분석 보고서
- 커스텀 시스템 서비스 구현 품질
- HAL 모듈 개발 및 테스트 결과

## 학습 리소스

### 필수 도서
- "Android Internals" - Jonathan Levin
- "Embedded Android" - Karim Yaghmour
- "Android System Programming" - Roger Ye

### 온라인 리소스
- Android Open Source Project (AOSP)
- Android Developer Documentation
- Android Source Code Cross Reference
- XDA Developers Forum

### 도구 및 소프트웨어
- Android Studio
- AOSP Build System
- ADB (Android Debug Bridge)
- Systrace, Method Tracing
- DDMS (Dalvik Debug Monitor Server)

## 다음 단계

이 챕터를 완료한 후에는 **3. 커널 개발**로 진행하여 안드로이드 커널의 커스터마이징과 디바이스 드라이버 개발을 학습합니다.

## 체크리스트

- [ ] 안드로이드 소프트웨어 스택 전체 구조 이해
- [ ] 각 레이어의 역할과 상호작용 파악
- [ ] 부트 프로세스 완전 이해
- [ ] HAL 아키텍처 및 HIDL 이해
- [ ] ART 런타임 특징 학습
- [ ] 시스템 서비스 아키텍처 파악
- [ ] AOSP 빌드 환경 구축 완료
- [ ] 커스텀 시스템 서비스 개발 완료
- [ ] HAL 모듈 개발 및 테스트 완료 