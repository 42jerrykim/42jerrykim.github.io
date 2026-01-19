---
draft: true
collection_order: 390
image: "wordcloud.png"
description: "임베디드 소프트웨어에 Clean Architecture를 적용하는 방법을 다룹니다. 하드웨어에서 소프트웨어를 분리하고, 펌웨어를 최소화하는 전략을 설명합니다."
title: "[Clean Architecture] 39. 클린 임베디드 아키텍처"
date: 2026-01-18
categories: CleanArchitecture
tags: [Clean Architecture, 클린 아키텍처, Embedded, 임베디드, Firmware, 펌웨어, Hardware, 하드웨어, HAL, Hardware Abstraction Layer, 하드웨어 추상화 계층, OSAL, Operating System Abstraction Layer, OS 추상화 계층, Target Hardware, 타겟 하드웨어, Microcontroller, 마이크로컨트롤러, Device Driver, 디바이스 드라이버, Software Architecture, 소프트웨어 아키텍처, Testability, 테스트 용이성, Portability, 이식성, Off Target Testing, 오프 타겟 테스팅, On Target Testing, 온 타겟 테스팅, App titude test, 앱티튜드 테스트, Processor, 프로세서, GPIO, I2C, SPI, UART, Dependency Inversion, 의존성 역전, Interface, 인터페이스, Abstraction, 추상화]
---

임베디드 소프트웨어는 **하드웨어와 밀접**하다. 그러나 Clean Architecture의 원칙은 임베디드에도 적용된다. 핵심은 **하드웨어에서 소프트웨어를 분리**하는 것이다.

## 임베디드의 특수성

임베디드 소프트웨어는:
- 특정 **하드웨어에 종속**
- **리소스 제약** (메모리, CPU)
- **실시간 요구사항**

하지만 이것이 **나쁜 구조**의 변명이 되어선 안 된다.

## 펌웨어 vs 소프트웨어

| 구분 | 펌웨어 | 소프트웨어 |
|------|--------|-----------|
| 의존성 | 하드웨어에 종속 | 하드웨어 독립 |
| 테스트 | 타겟에서만 가능 | PC에서 테스트 가능 |
| 이식성 | 낮음 | 높음 |

목표: **펌웨어를 최소화**, 소프트웨어를 최대화.

## HAL (Hardware Abstraction Layer)

```mermaid
flowchart TB
    subgraph Software [소프트웨어 - 하드웨어 독립]
        APP[Application]
        HAL_I[HAL Interface]
        APP --> HAL_I
    end
    
    subgraph Firmware [펌웨어 - 하드웨어 종속]
        HAL_IMPL[HAL Implementation]
        HW[Hardware]
        HAL_IMPL --> HW
    end
    
    HAL_IMPL -->|구현| HAL_I
```

```c
// HAL 인터페이스
typedef struct {
    void (*led_on)(void);
    void (*led_off)(void);
    bool (*button_pressed)(void);
} HardwareAPI;

// 애플리케이션 - HAL 사용
void app_main(HardwareAPI* hw) {
    if (hw->button_pressed()) {
        hw->led_on();
    }
}
```

## 오프 타겟 테스팅

HAL 덕분에 **PC에서 테스트**:

```c
// 테스트용 HAL 구현
bool test_button_state = false;
bool led_state = false;

void test_led_on() { led_state = true; }
void test_led_off() { led_state = false; }
bool test_button() { return test_button_state; }

void test_app() {
    HardwareAPI hw = { test_led_on, test_led_off, test_button };
    
    test_button_state = true;
    app_main(&hw);
    
    assert(led_state == true);  // PC에서 실행!
}
```

## OSAL (OS Abstraction Layer)

OS도 추상화:

```c
// OSAL 인터페이스
typedef struct {
    void (*delay_ms)(uint32_t ms);
    void (*create_task)(void (*func)(void*), void* arg);
    void (*mutex_lock)(Mutex* m);
} OSAL;
```

## 핵심

> "임베디드 소프트웨어도 Clean Architecture를 적용할 수 있다. HAL과 OSAL로 하드웨어와 OS를 추상화하고, 비즈니스 로직을 독립시켜라."
