---
image: "tmp_wordcloud.png"
date: "2023-01-11T00:00:00Z"
header:
  teaser: /assets/images/2023/cover.jpg
tag:
- Atomics
- Rust
- Free
title: '[Rust] Rust Atomics and Locks'
---

Rust를 사용하여 동시성(Concurrency)을 가진 프로그램을 작성할 때 도움이 되는 내용을 담고 있다.

[https://marabos.nl/atomics/](https://marabos.nl/atomics/) 에서 무료로 내용을 볼 수 있다.

|![](/assets/images/2023/cover.jpg)|
|:---:|
|책 표지|

## 책 소개

Rust는 동시성에 잘 맞는 프로그래밍 언어이다. Rust 생태계안에는 동시성을 위한 자료구조, Lock등 많은 라이브러리가 있다. 그러나 이런 라이브러리를 적용하는것은 어려운일이다. 잘 사용되는 라이브러리 조차도 메모리 순서(Memory ordering) 버그가 드물지 않게 발생한다.

이 책에서 Mara Bos(Rust 라이브러리 개발팀장)는 모든 수준의 Rust 프로그래머가 저수준 동시성에 대한 명확한 이해를 얻을 수 있도록 도와준다. 기본 운영 체제 API와 결합하여 뮤텍스 및 조건 변수와 같은 공통 프리미티브를 구축하는 방법과 원자(Atomics) 및 메모리 순서에 대한 모든 것을 배우게 된다. 이 책을 통하여 Rust의 메모리 모델, 프로세서 및 운영 체제의 역할이 모두 어떻게 조화를 이루는지 확실하게 파악할 수 있다.

이 가이드를 통해 다음을 배울 수 있다.

* 동시성을 올바르게 프로그래밍하기 위해 Rust의 유형 시스템이 예외적으로 잘 작동하는 방법
* 뮤텍스, 조건 변수, Atomics 및 메모리 순서에 관한 모든 것
* Intel 및 ARM 프로세서에서 원자적 연산으로 실제로 일어나는 일
* 운영 체제의 지원으로 잠금을 구현하는 방법
* 동시성, 원자성 및 잠금을 포함하는 올바른 코드를 작성하는 방법
* 자신만의 잠금 및 동기화 프리미티브를 올바르게 빌드하는 방법

## 예제 코드

책에 있는 예제 코드는 GitHub에서도 확인 할 수 있다. [https://github.com/m-ou-se/rust-atomics-and-locks](https://github.com/m-ou-se/rust-atomics-and-locks)
