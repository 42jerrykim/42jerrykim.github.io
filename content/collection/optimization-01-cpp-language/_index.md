---
collection_order: 11
draft: true
title: "[Optimization(C++)] 01. Low-latency C++ 언어 최적화 트랙"
slug: cpp-optimization
description: "C++ 언어 레벨에서 추상화 비용을 측정하고 줄이는 트랙입니다. 가상 함수·RTTI·예외, STL 컨테이너·문자열, 객체 수명·임시·템플릿/constexpr, 코루틴·variant·span·람다·SBO·파라미터 전달을 다루며, 마이크로벤치마크 기반 검증과 전문가 판단 기준을 제시합니다. CPU/OS/동시성 영역은 별도 트랙에서 다룹니다."
tags:
  - Performance
  - Profiling
  - Optimization
  - C++
  - Memory
  - Compiler
  - Assembly
  - CPU
  - Cache
  - Concurrency
  - Linux
  - Windows
  - OS
  - Testing
  - CI-CD
  - 성능
  - 프로파일링
  - 최적화
  - 컴파일러
  - 메모리
  - 동시성
  - 운영체제
  - 코드품질
  - Software-Architecture
  - Latency
  - Throughput
  - Backend
  - 백엔드
  - Embedded
  - 임베디드
  - Code-Quality
  - Benchmark
  - Refactoring
  - 리팩토링
  - Best-Practices
  - Clean-Code
  - 클린코드
  - Implementation
  - 구현
  - Design-Pattern
  - 디자인패턴
  - Data-Structures
  - 자료구조
  - Time-Complexity
  - 시간복잡도
  - Documentation
  - 문서화
  - Git
  - Deep-Dive
  - Guide
  - 가이드
  - Reference
  - 참고
  - Technology
  - 기술
  - Tutorial
  - 튜토리얼
  - Abstraction
  - 추상화
  - String
  - 문자열
  - Error-Handling
  - 에러처리
  - Type-Safety
  - Advanced
---


이 트랙은 **Low-latency C++** 언어 최적화를 다룹니다. 마이크로초(µs) 단위 지연이 중요한 환경에서, 가상 함수·STL·문자열·객체 수명·임시·템플릿/constexpr·코루틴·variant·span·람다·SBO·파라미터 전달 등 "C++를 더 잘 쓰면 줄일 수 있는" 비용을 추상화 1개 단위로 격리 측정하고 대체하는 방법을 체계적으로 다룹니다. CPU 파이프라인·OS·동시성 구조는 별도 트랙에서 다루며, 여기서는 언어·라이브러리 수준만 취급합니다.

자세한 커리큘럼, 학습 목표, 측정·검증 방법론은 **[00. Introduction: Low-latency C++ 언어 최적화](/collection/optimization-01-cpp-language/00-introduction/)**를 참조하세요.
