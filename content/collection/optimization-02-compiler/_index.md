---
collection_order: 12
draft: true
title: "[Optimization(Compiler)] 02. Low-latency 컴파일러·빌드 최적화 트랙"
slug: compiler-optimization
description: "같은 C++ 코드도 빌드 설정과 컴파일러 최적화에 따라 성능이 달라집니다. 이 트랙에서는 최적화 옵션 설계, LTO/PGO 적용·검증, 인라이닝 실패 원인과 코드 생성 형태를 다루며, 알고리즘·동시성 설계는 경계 밖에 둡니다."
tags:
  - C++
  - Performance
  - Optimization
  - Compiler
  - CPU
  - Cache
  - Memory
  - Benchmark
  - Profiling
  - CI-CD
  - Testing
  - 성능
  - 최적화
  - 컴파일러
  - 프로파일링
  - 테스트
  - Implementation
  - 구현
  - Code-Quality
  - 코드품질
  - Linux
  - Windows
  - OS
  - 운영체제
  - Concurrency
  - 동시성
  - Latency
  - Throughput
  - Backend
  - 백엔드
  - Embedded
  - 임베디드
  - Debugging
  - 디버깅
  - Documentation
  - 문서화
  - Refactoring
  - 리팩토링
  - Clean-Code
  - 클린코드
  - Best-Practices
  - Git
  - Automation
  - 자동화
  - Software-Architecture
  - 소프트웨어아키텍처
  - Design-Pattern
  - 디자인패턴
  - Data-Structures
  - 자료구조
  - Time-Complexity
  - 시간복잡도
  - Complexity-Analysis
  - 복잡도분석
  - Edge-Cases
  - 엣지케이스
  - Pitfalls
  - 함정
  - Error-Handling
  - 에러처리
  - Guide
  - 가이드
  - Reference
  - 참고
  - Technology
  - 기술
  - Tutorial
  - 튜토리얼
  - Advanced
  - Deep-Dive
  - 실습
  - Case-Study
  - Assembly
  - Deployment
  - 배포
  - Workflow
  - 워크플로우
  - Configuration
  - 설정
  - Troubleshooting
  - 트러블슈팅
  - Comparison
  - 비교
---

이 트랙은 **코드를 바꾸지 않고도** 최적화 플래그·LTO·PGO·컴파일러 선택으로 성능을 바꾸는 영역을 다룹니다. 인라이닝·벡터화·코드 생성 형태가 µs 단위 수치에 직결됩니다.

**커리큘럼**(난이도 포함)·학습 목표·측정 기준·평가 체크리스트·선행·병행 트랙은 **[00. Introduction: Low-latency 컴파일러·빌드 최적화](/collection/optimization-02-compiler/00-introduction/)**에서 모두 다룹니다. 01(최적화 플래그)부터 순서대로 읽거나, 해당 챕터만 골라 읽어도 됩니다.

12개 트랙의 권장 순서·심화 진입 조건은 **[Low-latency 최적화 시리즈 개요](/collection/optimization-00-series-overview/00-introduction/)**를 참고하세요.
