---
image: "tmp_wordcloud.png"
categories: MachineLearning
date: "2024-08-19T00:00:00Z"
header: null

tags:
- PyTorch
- JAX
- Machine Learning
- Deep Learning
- Scientific Computing
- Framework Comparison
- Performance
- Scalability
- Flexibility
- Technical Debt
- Compiler
- XLA
- Functional Programming
- Reproducibility
- Distributed Computing
- GPU
- TPU
- Research
- Development
- API Design
- Code Quality
- Optimization
- Auto-Parallelization
- Ecosystem
- Community
- Open Source
- Governance
- Software Engineering
- Technical Challenges
- User Experience
- Code Portability
- Multi-Backend
- Debugging
- Experimentation
- Innovation
- Productivity
- Research Workloads
- Development Hours
- Code Maintenance
- Integration
- Documentation
- User Adoption
- Best Practices
- Software Architecture
- Design Philosophy
- Code Complexity
- Error Handling
- Community Support
- Ecosystem Fragmentation
- Development Tools
- Research Efficiency
teaser: /assets/images/undefined/teaser.jpg
title: '[MachineLearning] PyTorch vs JAX: A Critical Analysis'
---

최근 머신러닝 연구자들 사이에서 PyTorch와 JAX의 비교가 활발히 이루어지고 있다. PyTorch는 그 유연성과 직관적인 API 덕분에 많은 연구자들에게 사랑받아 왔지만, 최근 JAX의 등장으로 인해 그 입지가 흔들리고 있는 상황이다. JAX는 DeepMind에서 개발한 프레임워크로, 성능과 확장성을 중시하며, 특히 대규모 실험을 지원하는 데 강점을 보인다. PyTorch는 초기에는 프로토타입 제작에 최적화된 프레임워크로 설계되었지만, 대규모 분산 시스템에서의 성능 저하와 기술 부채 문제로 인해 많은 연구자들이 JAX로의 전환을 고려하고 있다. 이 글에서는 PyTorch와 JAX의 철학적 차이, 성능, 확장성, 그리고 코드의 재현 가능성 등 다양한 측면에서 두 프레임워크를 비교하고, JAX가 왜 현재의 머신러닝 연구에 더 적합한 선택인지에 대해 논의할 것이다. PyTorch의 유연성은 매력적이지만, JAX의 컴파일러 중심 접근 방식은 연구자들이 더 나은 성과를 내는 데 기여할 수 있다. 이러한 논의는 머신러닝 커뮤니티의 발전에 중요한 기여를 할 것으로 기대된다.


|![]()|
|:---:|
||


<!--
##### Outline #####
-->

<!--
# 블로그 포스트 아웃라인

---

## 서론
**PyTorch와 JAX의 비교**  
**과학 컴퓨팅에서의 생산성 문제**  
**JAX의 필요성과 목표**  

## 철학
**PyTorch의 유연성과 동적 접근**  
**TensorFlow와의 철학적 차이**  
**JAX의 컴파일러 중심 접근**  

## 성능과 확장성
**PyTorch의 성능 문제**  
**JAX의 자동 병렬화**  
**대규모 실험에서의 JAX의 이점**  

## 컴파일러 기반 개발
**JAX의 XLA 컴파일러 활용**  
**PyTorch의 컴파일러 통합 문제**  
**코드의 간결성과 효율성**  

## 기능적 프로그래밍
**JAX의 순수 함수 개념**  
**PyTorch의 복잡성 문제**  
**JAX의 함수 조합 가능성**  

## 재현성
**재현성 위기와 그 해결책**  
**PyTorch의 시드 관리 문제**  
**JAX의 명시적 키 사용**  

## 이식성 및 자동 스케일링
**PyTorch의 이식성 문제**  
**JAX의 하드웨어 호환성**  
**자동 스케일링의 중요성**  

## 단점
**JAX의 거버넌스 구조 문제**  
**XLA의 오픈 소스 전환**  
**JAX 생태계의 통합 문제**  

## 결론
**PyTorch의 한계와 JAX의 장점**  
**연구 코드베이스의 전환 필요성**  
**JAX 사용을 권장하는 이유**  

--- 

이 아웃라인은 블로그 포스트의 구조를 제시하며, 각 섹션은 주제에 대한 깊이 있는 논의를 포함할 것입니다. 각 섹션은 독자들이 PyTorch와 JAX의 차이점을 이해하고, JAX의 장점을 인식할 수 있도록 돕는 내용을 담고 있습니다.
-->

<!--
## 서론
**PyTorch와 JAX의 비교**  
**과학 컴퓨팅에서의 생산성 문제**  
**JAX의 필요성과 목표**  
-->

## 서론

**PyTorch와 JAX의 비교**  

PyTorch와 JAX는 현대 머신러닝 및 과학 컴퓨팅에서 널리 사용되는 두 가지 주요 라이브러리이다. PyTorch는 그 유연성과 직관적인 API로 인해 많은 연구자와 개발자에게 사랑받고 있으며, JAX는 자동 미분과 GPU/TPU 가속을 통해 성능을 극대화하는 데 중점을 두고 있다. 이 두 라이브러리는 각각의 장단점이 있으며, 특정 작업에 따라 선택이 달라질 수 있다.

**과학 컴퓨팅에서의 생산성 문제**  

과학 컴퓨팅 분야에서는 코드의 생산성이 매우 중요하다. 연구자들은 복잡한 수학적 모델을 구현하고 실험을 수행해야 하며, 이 과정에서 코드의 가독성과 유지보수성이 필수적이다. PyTorch는 동적 계산 그래프를 제공하여 이러한 요구를 충족시키지만, JAX는 함수형 프로그래밍 패러다임을 통해 더 나은 생산성을 제공할 수 있다.

**JAX의 필요성과 목표**  

JAX는 특히 대규모 데이터와 복잡한 모델을 다루는 데 필요한 도구로 자리 잡고 있다. JAX의 목표는 연구자들이 더 쉽게 실험하고, 더 나은 성능을 얻을 수 있도록 돕는 것이다. 이를 위해 JAX는 자동 미분, GPU/TPU 가속, 그리고 함수형 프로그래밍을 지원하여 연구자들이 효율적으로 작업할 수 있도록 설계되었다.

<!--
## 철학
**PyTorch의 유연성과 동적 접근**  
**TensorFlow와의 철학적 차이**  
**JAX의 컴파일러 중심 접근**  
-->

## 철학

**PyTorch의 유연성과 동적 접근**  

PyTorch는 동적 계산 그래프를 사용하여 유연성을 극대화한다. 이는 사용자가 코드를 작성하는 동안 즉시 결과를 확인할 수 있게 해주며, 디버깅 과정에서도 큰 장점을 제공한다. 이러한 동적 접근 방식은 연구자들이 실험을 진행할 때 매우 유용하다. 예를 들어, 모델의 구조를 변경하거나 새로운 아이디어를 테스트할 때, 즉각적인 피드백을 받을 수 있어 개발 속도가 빨라진다. 

**TensorFlow와의 철학적 차이**  

TensorFlow는 정적 계산 그래프를 기반으로 하여, 모델을 정의한 후에 그래프를 컴파일하고 실행하는 방식이다. 이는 성능 최적화에 유리하지만, 개발 과정에서의 유연성은 떨어진다. PyTorch는 이러한 정적 접근 방식의 한계를 극복하기 위해 동적 그래프를 채택하였으며, 이는 연구자들이 더 자유롭게 실험할 수 있도록 돕는다. 

**JAX의 컴파일러 중심 접근**  

JAX는 컴파일러 중심의 접근 방식을 채택하여, NumPy와 유사한 API를 제공하면서도 GPU 및 TPU에서의 성능을 극대화한다. JAX는 XLA(Accelerated Linear Algebra) 컴파일러를 사용하여, 사용자가 작성한 코드를 최적화하고 자동으로 병렬화한다. 이러한 방식은 연구자들이 복잡한 수학적 계산을 수행할 때, 성능을 크게 향상시킬 수 있는 기회를 제공한다. 

---

이와 같이 각 섹션은 PyTorch와 JAX의 철학적 차이를 명확히 하고, 각 프레임워크의 장단점을 비교하는 데 중점을 두고 있다. 독자들은 이러한 내용을 통해 각 프레임워크의 특성을 이해하고, 자신에게 적합한 도구를 선택하는 데 도움을 받을 수 있다.

<!--
## 성능과 확장성
**PyTorch의 성능 문제**  
**JAX의 자동 병렬화**  
**대규모 실험에서의 JAX의 이점**  
-->

## 성능과 확장성

**PyTorch의 성능 문제**  

PyTorch는 많은 연구자와 개발자에게 인기가 있지만, 대규모 모델을 훈련할 때 성능 문제가 발생할 수 있다. 특히, GPU와 같은 하드웨어 자원을 효율적으로 활용하지 못하는 경우가 많다. 이는 메모리 사용량이 많아지고, 훈련 속도가 느려지는 결과를 초래한다. 또한, PyTorch의 동적 계산 그래프는 유연성을 제공하지만, 이로 인해 성능 최적화가 어려워질 수 있다. 이러한 문제는 대규모 데이터셋을 다루는 연구에서 특히 두드러진다.

**JAX의 자동 병렬화**  

JAX는 자동 미분과 함께 자동 병렬화 기능을 제공하여 성능을 극대화할 수 있다. JAX의 `jit` 기능을 사용하면, 함수의 실행을 컴파일하여 성능을 향상시킬 수 있다. 이 과정에서 JAX는 XLA(Accelerated Linear Algebra) 컴파일러를 활용하여 GPU와 TPU에서 최적화된 코드를 생성한다. 이를 통해 JAX는 대규모 모델 훈련 시 성능을 크게 향상시킬 수 있으며, 연구자들은 더 빠른 실험을 통해 결과를 도출할 수 있다.

**대규모 실험에서의 JAX의 이점**  

JAX는 대규모 실험을 수행할 때 여러 가지 이점을 제공한다. 첫째, JAX는 자동 미분과 병렬화를 통해 실험의 반복성을 높인다. 둘째, JAX의 함수형 프로그래밍 접근 방식은 코드의 가독성을 높이고, 유지보수를 용이하게 한다. 셋째, JAX는 TPU와 같은 고성능 하드웨어에서 최적화된 성능을 발휘할 수 있어, 대규모 데이터셋을 다루는 연구에서 매우 유용하다. 이러한 이점들은 연구자들이 더 빠르고 효율적으로 실험을 수행할 수 있도록 돕는다. 

이와 같은 이유로, JAX는 성능과 확장성 측면에서 PyTorch보다 더 나은 선택이 될 수 있다.

<!--
## 컴파일러 기반 개발
**JAX의 XLA 컴파일러 활용**  
**PyTorch의 컴파일러 통합 문제**  
**코드의 간결성과 효율성**  
-->

## 컴파일러 기반 개발

**JAX의 XLA 컴파일러 활용**  

JAX는 XLA(Accelerated Linear Algebra)라는 컴파일러를 활용하여 고성능의 수치 계산을 가능하게 한다. XLA는 JAX의 연산을 최적화하여 GPU와 TPU와 같은 하드웨어에서 실행할 때 성능을 극대화한다. JAX의 함수는 기본적으로 NumPy와 유사한 방식으로 작성되지만, XLA를 통해 JIT(Just-In-Time) 컴파일을 수행함으로써 실행 속도를 크게 향상시킬 수 있다. JAX의 JIT 컴파일 기능은 복잡한 수치 계산을 수행할 때 특히 유용하며, 반복적인 연산을 최적화하여 실행 시간을 단축시킨다.

**PyTorch의 컴파일러 통합 문제**  

PyTorch는 최근에 TorchScript라는 기능을 도입하여 모델을 최적화하고, C++로 변환할 수 있는 기능을 제공하고 있다. 그러나 PyTorch의 컴파일러 통합은 JAX에 비해 상대적으로 복잡하다. TorchScript는 정적 그래프를 생성하는 방식으로 작동하지만, PyTorch의 동적 특성을 완전히 활용하지 못하는 경우가 많다. 이로 인해 PyTorch의 성능 최적화는 JAX에 비해 제한적일 수 있으며, 특히 대규모 모델을 다룰 때 성능 저하가 발생할 수 있다.

**코드의 간결성과 효율성**  

JAX는 함수형 프로그래밍 패러다임을 채택하여 코드의 간결성과 효율성을 높인다. JAX의 API는 NumPy와 유사하여 사용자가 쉽게 접근할 수 있으며, 함수형 프로그래밍의 장점을 통해 코드의 재사용성과 가독성을 높인다. 예를 들어, JAX에서는 변수를 변경하는 대신 새로운 변수를 생성하는 방식을 사용하여 부작용을 최소화하고, 코드의 예측 가능성을 높인다. 이러한 접근은 복잡한 수치 계산을 수행할 때 코드의 유지보수성을 높이는 데 기여한다.

JAX의 컴파일러 기반 개발은 성능과 효율성을 극대화하는 데 중요한 역할을 하며, 이는 연구자와 개발자들이 대규모 모델을 효과적으로 다룰 수 있도록 돕는다. JAX의 XLA 컴파일러는 특히 고성능 컴퓨팅 환경에서 그 진가를 발휘하며, PyTorch의 컴파일러 통합 문제는 앞으로의 발전 방향에 대한 중요한 논의가 필요하다.

<!--
## 기능적 프로그래밍
**JAX의 순수 함수 개념**  
**PyTorch의 복잡성 문제**  
**JAX의 함수 조합 가능성**  
-->

## 기능적 프로그래밍

**JAX의 순수 함수 개념**  

JAX는 함수형 프로그래밍의 원칙을 따르며, 순수 함수를 중심으로 설계되었다. 순수 함수란 동일한 입력에 대해 항상 동일한 출력을 반환하며, 외부 상태에 영향을 미치지 않는 함수를 의미한다. 이러한 특성 덕분에 JAX는 코드의 예측 가능성을 높이고, 디버깅을 용이하게 한다. 또한, 순수 함수는 병렬 처리와 최적화에 유리하여, JAX의 성능을 극대화하는 데 기여한다.

**PyTorch의 복잡성 문제**  

반면, PyTorch는 동적 계산 그래프를 사용하여 유연성을 제공하지만, 이로 인해 코드의 복잡성이 증가할 수 있다. 특히, 상태를 변경하는 부작용이 발생할 수 있는 경우, 코드의 흐름을 이해하기 어려워질 수 있다. 이러한 복잡성은 특히 대규모 프로젝트에서 유지보수의 어려움을 초래할 수 있으며, 이는 연구자들이 실험을 반복하고 결과를 재현하는 데 방해가 된다.

**JAX의 함수 조합 가능성**  

JAX는 함수 조합을 통해 복잡한 연산을 간결하게 표현할 수 있는 기능을 제공한다. 함수 조합이란 여러 개의 함수를 결합하여 새로운 함수를 만드는 과정을 의미한다. JAX에서는 `jax.vmap`, `jax.jit`와 같은 고급 기능을 사용하여 함수 조합을 쉽게 수행할 수 있다. 이러한 기능은 코드의 재사용성을 높이고, 실험의 효율성을 증가시킨다. 결과적으로, JAX는 연구자들이 더 나은 성능을 가진 코드를 작성할 수 있도록 돕는다.

이와 같이 JAX는 함수형 프로그래밍의 장점을 활용하여 코드의 간결성과 효율성을 높이고, PyTorch의 복잡성 문제를 해결하는 데 기여하고 있다. 이러한 특성은 JAX를 선택하는 중요한 이유 중 하나가 된다.

<!--
## 재현성
**재현성 위기와 그 해결책**  
**PyTorch의 시드 관리 문제**  
**JAX의 명시적 키 사용**  
-->

## 재현성

**재현성 위기와 그 해결책**  

재현성은 과학 연구에서 매우 중요한 요소이다. 연구 결과가 다른 연구자들에 의해 동일하게 재현될 수 있어야만 그 결과의 신뢰성이 확보된다. 그러나 머신러닝 분야에서는 재현성이 종종 문제로 지적된다. 이는 다양한 요인, 예를 들어 데이터셋의 불일치, 하이퍼파라미터의 차이, 그리고 무작위성에 의해 발생할 수 있다. 이러한 문제를 해결하기 위해서는 명확한 실험 조건과 환경을 설정하고, 이를 문서화하는 것이 필수적이다. 

JAX는 이러한 재현성 문제를 해결하기 위해 명시적 키를 사용한다. 이는 무작위성을 제어하고, 실험의 일관성을 유지하는 데 도움을 준다. JAX의 키 시스템은 각 실험에 대해 고유한 시드를 생성할 수 있도록 하여, 연구자가 동일한 조건에서 실험을 반복할 수 있게 한다. 

**PyTorch의 시드 관리 문제**  

PyTorch는 무작위성을 다루는 데 있어 몇 가지 한계가 있다. 기본적으로 PyTorch는 시드를 설정하는 기능을 제공하지만, 이 시드가 모든 무작위성 요소에 대해 일관되게 적용되지 않을 수 있다. 예를 들어, 데이터 로딩, 모델 초기화, 그리고 훈련 과정에서 발생하는 무작위성은 각각 독립적으로 관리되기 때문에, 연구자가 의도한 대로 실험을 재현하기 어려운 경우가 많다. 

이러한 문제는 특히 여러 실험을 비교하거나, 하이퍼파라미터 튜닝을 수행할 때 더욱 두드러진다. 따라서 PyTorch를 사용할 때는 시드 관리에 대한 주의가 필요하며, 이를 통해 재현성을 높이기 위한 추가적인 노력이 요구된다. 

**JAX의 명시적 키 사용**  

JAX는 무작위성을 다루는 데 있어 명시적 키를 사용하여 재현성을 보장한다. JAX의 무작위성 API는 각 무작위 작업에 대해 고유한 키를 생성하고, 이를 통해 무작위성을 제어할 수 있다. 연구자는 실험을 수행할 때마다 동일한 키를 사용하여 실험을 반복할 수 있으며, 이를 통해 결과의 일관성을 확보할 수 있다. 

이러한 접근 방식은 연구자가 실험을 설계하고 실행하는 데 있어 더 많은 유연성을 제공한다. 또한, JAX의 명시적 키 시스템은 코드의 가독성을 높이고, 실험의 재현성을 보장하는 데 기여한다. 따라서 JAX는 머신러닝 연구에서 재현성 문제를 해결하는 데 있어 매우 유용한 도구가 될 수 있다. 

이와 같이, JAX는 재현성 문제를 해결하기 위한 다양한 기능을 제공하며, 이는 연구자들이 보다 신뢰할 수 있는 결과를 도출하는 데 도움을 준다.

<!--
## 이식성 및 자동 스케일링
**PyTorch의 이식성 문제**  
**JAX의 하드웨어 호환성**  
**자동 스케일링의 중요성**  
-->

## 이식성 및 자동 스케일링

**PyTorch의 이식성 문제**  

PyTorch는 다양한 플랫폼에서 사용될 수 있지만, 이식성에 있어 몇 가지 문제점이 존재한다. 특히, PyTorch의 특정 기능이나 라이브러리는 특정 하드웨어에 최적화되어 있어, 다른 환경에서 실행할 때 성능 저하가 발생할 수 있다. 예를 들어, GPU와 CPU 간의 전환이 원활하지 않거나, 특정 CUDA 버전과의 호환성 문제로 인해 코드가 제대로 작동하지 않을 수 있다. 이러한 문제는 연구자들이 다양한 환경에서 실험을 수행할 때 큰 장애물이 된다.

**JAX의 하드웨어 호환성**  

JAX는 하드웨어 호환성에 있어 매우 유연한 접근 방식을 취하고 있다. JAX는 NumPy와 유사한 API를 제공하면서도, 다양한 하드웨어에서 최적화된 성능을 발휘할 수 있도록 설계되었다. JAX는 XLA(Accelerated Linear Algebra) 컴파일러를 사용하여, 코드가 실행되는 하드웨어에 맞춰 자동으로 최적화된다. 이로 인해, JAX는 CPU, GPU, TPU 등 다양한 하드웨어에서 일관된 성능을 제공할 수 있다. 연구자들은 JAX를 사용하여 코드의 이식성을 높이고, 다양한 환경에서 동일한 결과를 얻을 수 있다.

**자동 스케일링의 중요성**  

자동 스케일링은 대규모 데이터 처리 및 모델 학습에서 매우 중요한 요소이다. PyTorch는 사용자가 수동으로 스케일링을 설정해야 하는 경우가 많아, 대규모 실험을 수행할 때 불편함을 초래할 수 있다. 반면, JAX는 자동으로 스케일링을 지원하여, 사용자가 복잡한 설정을 하지 않고도 대규모 데이터셋을 처리할 수 있도록 돕는다. JAX의 자동 스케일링 기능은 연구자들이 더 많은 실험을 수행하고, 더 빠르게 결과를 도출할 수 있게 해준다. 이는 연구의 생산성을 크게 향상시키는 요소로 작용한다. 

이와 같이, JAX는 이식성과 자동 스케일링 측면에서 PyTorch보다 더 나은 성능을 제공하며, 연구자들이 다양한 환경에서 효율적으로 작업할 수 있도록 돕는다.

<!--
## 단점
**JAX의 거버넌스 구조 문제**  
**XLA의 오픈 소스 전환**  
**JAX 생태계의 통합 문제**  
-->

## 단점

**JAX의 거버넌스 구조 문제**  

JAX는 오픈 소스 프로젝트로, 그 발전과 유지보수는 커뮤니티에 의존하고 있다. 그러나 JAX의 거버넌스 구조는 명확하지 않아서, 프로젝트의 방향성과 우선순위에 대한 결정이 불투명할 수 있다. 이는 개발자들이 JAX를 사용할 때 불안감을 느끼게 할 수 있으며, 장기적인 지원에 대한 의구심을 불러일으킬 수 있다. 이러한 문제는 JAX의 사용자 기반이 성장함에 따라 더욱 두드러질 수 있으며, 커뮤니티의 참여와 피드백이 중요해진다.

**XLA의 오픈 소스 전환**  

JAX는 XLA(Accelerated Linear Algebra)라는 컴파일러를 활용하여 성능을 극대화한다. 그러나 XLA의 오픈 소스 전환 과정에서 여러 가지 문제가 발생할 수 있다. XLA는 복잡한 컴파일러 기술을 기반으로 하며, 이를 오픈 소스로 전환하는 과정에서 발생하는 기술적 문제나 문서화 부족은 사용자들에게 혼란을 초래할 수 있다. 또한, XLA의 발전이 JAX의 발전에 직접적인 영향을 미치기 때문에, XLA의 안정성과 성능이 JAX의 신뢰성에 큰 영향을 미친다.

**JAX 생태계의 통합 문제**  

JAX는 다양한 라이브러리와 도구와의 통합이 필요하다. 그러나 현재 JAX 생태계는 상대적으로 초기 단계에 있으며, 다른 머신러닝 프레임워크와의 호환성 문제로 인해 사용자가 원하는 기능을 쉽게 찾기 어려울 수 있다. 예를 들어, PyTorch나 TensorFlow와 같은 다른 프레임워크에서 제공하는 다양한 기능이나 라이브러리를 JAX에서 동일하게 사용할 수 없는 경우가 많다. 이러한 통합 문제는 JAX의 사용성을 제한할 수 있으며, 사용자들이 JAX로 전환하는 데 장애물이 될 수 있다.

---

이와 같이 JAX의 단점에 대한 논의는 JAX를 사용하는 데 있어 고려해야 할 중요한 요소들을 제시한다. 각 단점은 JAX의 발전과 커뮤니티의 참여가 필요함을 강조하며, 사용자들이 JAX를 선택할 때 신중하게 판단해야 함을 알린다.

<!--
## 결론
**PyTorch의 한계와 JAX의 장점**  
**연구 코드베이스의 전환 필요성**  
**JAX 사용을 권장하는 이유**  
-->

## 결론

**PyTorch의 한계와 JAX의 장점**  

PyTorch는 많은 연구자와 개발자에게 사랑받는 프레임워크이다. 그러나 몇 가지 한계가 존재한다. 첫째, PyTorch는 동적 그래프를 사용하여 유연성을 제공하지만, 이로 인해 성능 최적화가 어려울 수 있다. 둘째, 대규모 분산 학습에서의 성능 저하 문제도 있다. 반면, JAX는 XLA(Accelerated Linear Algebra) 컴파일러를 통해 성능을 극대화하고, 자동 병렬화를 지원하여 대규모 실험에서의 이점을 제공한다. 이러한 점에서 JAX는 PyTorch의 한계를 극복할 수 있는 가능성을 지닌다.

**연구 코드베이스의 전환 필요성**  

연구자들은 종종 새로운 아이디어를 실험하고 검증하기 위해 코드베이스를 전환해야 하는 상황에 직면한다. PyTorch에서 JAX로의 전환은 이러한 과정에서 많은 이점을 제공할 수 있다. JAX는 함수형 프로그래밍 패러다임을 채택하여 코드의 재사용성과 가독성을 높인다. 또한, JAX의 명시적 키 사용은 실험의 재현성을 보장하는 데 큰 도움이 된다. 따라서 연구자들은 JAX로의 전환을 고려해야 할 필요성이 있다.

**JAX 사용을 권장하는 이유**  

JAX는 현대의 과학 컴퓨팅 요구에 부합하는 여러 가지 장점을 제공한다. 첫째, JAX는 자동 미분과 GPU/TPU 지원을 통해 복잡한 수학적 계산을 간편하게 수행할 수 있다. 둘째, JAX의 함수형 프로그래밍 접근 방식은 코드의 유지보수성을 높이고, 버그를 줄이는 데 기여한다. 마지막으로, JAX는 다양한 하드웨어에서의 이식성을 제공하여 연구자들이 다양한 환경에서 실험을 수행할 수 있도록 돕는다. 이러한 이유로 JAX의 사용을 권장한다.

<!--
##### Reference #####
-->

## Reference


* [https://neel04.github.io/my-website/blog/pytorch_rant/](https://neel04.github.io/my-website/blog/pytorch_rant/)


<!--
**Assumed audience:** ML researchers who frequently work with ` PyTorch ` ,
but are interested in trying out ` JAX ` or have yet to be convinced.

* * *

#  Introduction

Usually, people start these ‘critiques’ with a disclaimer that they are not
trying to trash the framework, and talk about how it’s a tradeoff. However,
this is assumed - I’m not going to waste your time with that.

Instead, I’ll focus on why PyTorch has been a net negative for all (if not
most) scientific computing efforts, causing billions of dollars in lost
productivity and thousands of wasted dev-hours.

This is not because its a _bad_ framework per-se, but rather - it simply
because it wasn’t designed for the use-cases it’s being employed in right now.

Ever since [ LuaTorch ](http://torch.ch/) , PyTorch was supposed to be a
“production ready, easy-to-use framework for quick prototyping”.

It wasn’t meant to be deployed onto huge, distributed clusters comprising of
thousands of interconnected nodes and GPUs and scale _well_ in a fault-
tolerant and robust matter.

The guiding philosophy of ` Torch ` was never about scale - despite what their
marketing may have you believe - but _flexibility_ .

In response to the rising need of a scalable and performant framework,
DeepMind developed ` JAX ` to meet a simple goal:

> “&mldr; Supporting state-of-the-art AI research [by] balancing rapid
> prototyping and quick iteration with the ability to deploy experiments at a
> scale &mldr;” - [ ` JAX ` blogpost ](https://arc.net/l/quote/cumgnsor)

This post is about convincing you how important this idea/philosophy is not
only for Deep Learning, but for all scientfic computing that needs to happen
at scale.

I believe that all infrastructure built on ` Torch ` is just a huge pile of
technical debt, that will haunt the field for a long, long time.

#  The Philosophy

PyTorch’s philosophy has always, in some ways, been antithetical to that of
Tensorflow’s.

Where ` TF 1.x ` tried to be a static but performant framework by making
strong use of the ` XLA ` compiler, ` PyTorch ` instead focused on being
dynamic, easily debuggable and pythonic.

Early on, the TF devs realized their mistakes when they came to realize how
much the community hated the old ` 1.x ` API, which was counter-intuitive and
introduced anti-pythonic patterns that were difficult to grasp for beginners.

This prompted the core decision to use ` Keras ` as the main interface for
TensorFlow and downplay the role of [ ` XLA `
](https://en.wikipedia.org/wiki/Accelerated_Linear_Algebra) compiler that was
at TF’s core. The main focus was on cleaning up the frontend as much as
possible.

This was a huge mistake.

Sure, the API did improve and worked well for some people - but only as long
as your workloads were standard. Any deviations from the norm were punished by
stacktrace dumps that were often literal pages of just garbled ` XLA-HLO `
that were a nightmare to debug unless you had a strong grasp on the internals
of the framework/compiler - which you **didn’t** because ` XLA ` was a closed
source, internal Google project at the time.

In short, it had every hallmark of a typical Google product.

Thus it comes as no surprise that people who switched over to PyTorch thought
they had discovered literal heaven:

PyTorch stuck to its roots. Unlike TensorFlow’s static & lazy approach, they
took the bolder, more dynamic “eager” approach wherein all ` torch.Tensor ` s
were evaluated immediately, leading to a much more cleaner abstraction than
TensorFlow’s.

Clearly, they understood that complexity is the enemy of productivity. Instead
of tacking on band-aids, they had pursued a fresh new path which paid off.

Unsurprisingly, almost serious research moved to PyTorch:

PyTorch vs. Tensorflow usage in research repos

But in 2021 [ ` GPT-3 ` ](https://arxiv.org/abs/2005.14165) hit the scene and
suddenly things started getting serious. All of a sudden, performance and
scalability became the primary concern.

` PyTorch ` accomodated for this rising demand _decently_ well, but because it
wasn’t designed around this philosophy - slowly the debt starting catching up
and the foundations started crumbling. It’s hard to reconcile flexibility with
performance. Clearly, a tradeoff needed to be made.

Either they could give their biggest and richest users exactly what they
wanted - a clean & scalable ecosystem that prioritized performance - which
would be a static-oriented ` TF ` -like design - or they could try to hold on
to what made ` Torch ` so special in the first place - being dynamic and
“eager” at the expense of performance, and somehow delegate those large-scale
workloads to an entirely seperate technological stack.

So the devs, being the smart and rational engineers they are, choose an
appropriate compromise which was . . . . to pursue both paths simultaneously.

They were unwilling to make any tradeoffs. They wanted their cake and were
going to eat it too.

The new approach was ultimately a chaotic mishmash of competing features. You
have on one hand, PyTorch’s committment to eventually use _some_ compiler
(likely ` XLA ` ) as a performant and reliable default backend and on the
other, to build up their own entire [ ` torch.compile `
](https://pytorch.org/docs/stable/torch.compiler.html) stack that somehow
meshes well with the eager, dynamic philosophy by giving users the freedom to
invoke a compiler if need be.

This lack of real long-term strategy is a serious issue.

Take the ` torch.compile ` stack and the new [ ` DTensor `
](https://github.com/pytorch/pytorch/blob/main/torch/distributed/_tensor/README.md)
API as an example. The documentation is transparent about the inspiration for
this feature. It tries to bring the sharding model of parallelization from `
JAX ` to ` PyTorch ` .

> &mldr; When using ` DTensor ` in a [distributed] fashion it might be &mldr;
> **slower** compared to existing solutions like DDP/FSDP. This is mainly
> because DDP/FSDP have a global view of the entire model &mldr; [and can
> thus] optimize for data parallel specifically &mldr; [whereas]
> DistributedTensor &mldr; can only optimize within individual tensor
> operations.

> To improve efficiency of ` DTensor ` -based data parallel training, we are
> exploring a **compiler-based** solution on top of ` DTensor ` .

Leaning on the compiler is diametrically opposed to torch’s dynamic philosophy
- because at each step, you’re restricted by the constraints placed by the
compiler which you _must_ obey.

` PyTorch ` clearly doesn’t want to commit to a compiler-centric philosophy
(like ` JAX ` ) but I don’t see any good alternative solutions - and frankly,
I doubt the devs do either.

Instead, what you end up getting getting is a fragmented suite of tools
that’re barely usable without significant dev-hours sunk in just setting them
up and coaxing them to work with each other.

It’s considerable friction for research teams who often spend more of their
time babysitting the codebase and triangulating random errors rather than
running more experiments.

I feel there is a stronger incentive internally on _marketing_ and shipping
‘features’ rather than actually ensuring they integrate well into the
ecosystem. It’s true that maintaining such a huge ecosystem will always have
it’s problems, but the considering the case where devs shipped a built-in
implementation of ` FSDP ` , and it didn’t work at _all_ with their own `
torch.compile ` stack for months, really goes to show where their priorities
lie.

There is simply no excuse for two of your most core, critical features not
working together at all. Users had to wait [ weeks ](https://dev-
discuss.pytorch.org/t/torch-compile-fsdp-dec-8th/1718) before it was
officially patched and the bugs were ironed out to the point of it being in a
ususable state where is stands now.

My point is that all these failures are systemic due to: a) bad organization
and b) bad design decisions.

So what is the competition’s solution to this problem?

##  Compiler-driven development

` JAX ` leverages TensorFlow’s formidable compiler stack, [ ` XLA `
](https://en.wikipedia.org/wiki/Accelerated_Linear_Algebra) . ` XLA ` is a
pretty powerful compiler, but the beauty is that it’s all abstracted away for
the end user. For any function you have, as long as the function is **pure**
(more on this later) you can use the simple ` @jax.jit ` decorator to JIT
compile your function and make it available to ` XLA ` .

You can ` jit ` any JAX code - ` XLA ` handles the rest. This is what makes
JAX such a great framework for scientific computing - its effectively an eDSL
built entirely around ` XLA ` . The compiler handles and abstracts away a lot
of the heavy lifting for us - verifying that the generated graph is correct, `
GSPMD ` partitioner that handles the auto-parallelization w/ sharding in JAX,
the graph optimizations, operator and kernel fusion, Latency hiding
Scheduling, overlapping asynchronous comms, codegeneration to other backends
such as [ ` triton ` ](https://openai.com/index/triton/) etc. are all handled
by ` XLA ` behind the scenes.

This is a powerful approach. As long as your code obeys some simple JAX
restrictions, ` XLA ` does this automatically for you. For example, you don’t
need ` torch.distributed.barrier() ` and other comms primitives when doing
parallelization. DDP support is as simple as:

    
    
    # Create a Sharding object to distribute a value across devices:
    sharding = PositionalSharding(mesh_utils.create_device_mesh((8,)))   
    x = JAX.random.normal(JAX.random.key(0), (8192, 8192))
    y = JAX.device_put(x, sharding.reshape(4, 2))
    

which you can also visualize with the built in utilities:

    
    
    >>> JAX.debug.visualize_array_sharding(z)
    
    +---------------------+
    |  TPU 0   |  TPU 1   |
    |----------|----------|
    |  TPU 2   |  TPU 3   |
    |----------|----------|
    |  TPU 6   |  TPU 7   |
    |----------|----------|
    |  TPU 4   |  TPU 5   |
    +---------------------+
    

` XLA ` ’s approach is that computation follows sharding. Therefore, if the
input array is sharded across some axis, ` XLA ` handles that automatically
for any downstream computation. No other code changes needed. No need to add
communication collections or anything. ` Pytorch ` on the other hand requires
a ton of boilerplate and modifications just to get a basic DDP setup working
correctly.

This idea of “compiler driven development” is similar to how rust’s compiler
works - helping you write better, cleaner code without worrying about a lot of
mundane things.

You focus on the computation, the compiler does the rest.

I believe that comitting to a philosophy gives a framework a certain design
skeleton and structure, that can simplify the code and create a smooth and
wondeful experience for a developer.

Which is why I’m unhappy with the choice made by the ` PyTorch ` devs to
integrate and rely on a compiler stack for the cool new features rather than
keeping the core philosophy of _flexibility_ and _freedom_ alive.

For example, according to the official [ roadmap
](https://pytorch.org/blog/pytorch-2.0-xla-path-forward/) for ` PyTorch ` `
2.x ` , they clearly outline their long-term plans of fully integrating ` XLA
` with ` Torch ` :

> “PyTorch/ ` XLA ` is set to migrate to the open source ` OpenXLA ` as its
> **default** downstream compiler”

This is an awful idea. It’s like saying that shoehorning C++ code in the rust
compiler, would somehow be a better experience than using rust itself.

Torch simply wasn’t _designed_ around ` XLA ` , unlike ` JAX ` . The reason `
JAX ` ’s’ ecosystem is so much more stable and well-integrated is precisely
because they uphold it’s core values rather than working around them.

If, god forbid, ` Pytorch ` does end up going with the plan and commits to an
` XLA ` based compiler stack, then wouldn’t the ideal framework be the one
that was _specifically_ designed and built around it, as opposed to the one
where it has just been crammed in with little thought and care?

And even **if** ` Pytorch ` ends up pursuing a ‘multi-backend’ approach,
wherein you would be able choose whatever compiler backend you wish, wouldn’t
that worsen the fragmentation problem and absolutely nuke the API, as it tries
to respect the restrictions of every compiler stack?

This isn’t just baseless theorizing either — look at ` Torch/XLA ` . Anyone
who’s ever dared to use it on TPUs suffers from a PTSD so severe that they’re
eligible for benefits. The mere sight of “XLA” sends them into a state of cold
sweat and nightmares to the caffeine-fuelled days spent debugging hundred-line
` XLA ` errors. The only path to recovery at such moments is to reassure the
victim that they’ll always have their GPUs, and an ` A100 ` may be placed
beside them for emotional support.

##  Multi-backend is doomed

` Pytorch ` ’s root problem is that it tries to do everything at once and
fails miserably.

The “multi-backend” design decision makes this problem exponentially worse. In
_theory_ , it sounds like an amazing idea to be able to choose whichever stack
you prefer - but in reality, its a tangled mess of obscure tracebacks and
incompatibility issues.

It’s not that its _hard_ to get these backends working. Rather, there are some
constraints that these backends expect which are hard to mesh with the
flexible and pythonic API of ` PyTorch ` .

There’s a tradeoff between keeping most of the API consistent vs. obeying the
restrictions of the backends you leverage. As a result, the devs are seeking
to rely more on codegen (say converting torch code to ` triton ` which then
you can manually work with and leverage it’s compiler & JIT stack) as opposed
to actually integrating/comitting to a single backend - which is arguably the
worse option for ` torch ` .

Every decision ` torch ` takes somehow always feels like a compromise because
it refuses to make meaningful tradeoffs. There’s no coherence, no overall
strategy. It ends up feeling more like a mishmash of features that don’t mesh
well together and ultimately cause a lot of frustration for the user.

There is no faster way to kill an ecosystem.

IMHO PyTorch should not follow the ` JAX ` “integrated compiler and backend”
approach for a very simple reason: Jax was explcitly designed from the ground
up to work **with** ` XLA ` . Not **against** it. That is why ` TensorFlow `
never really took off, and why it’s attempts at integrating ` Keras ` crashed
and burned.

Your strategy simply cannot be to just replace the entire ` PyTorch ` frontend
with ` JAX ` ’s, because then you just have a shittier version of ` JAX ` !
It’s virtually impossible to come up with a neat, functional API based on `
XLA ` that’s somehow better than ` JAX ` ’s, and carries on ` Torch ` ’s
flexible nature.

I don’t blame the devs for trying new and different ideas - those are always
welcome. However, if they want ` PyTorch ` to stand the test of time, more
focus has to be put in shoring up the foundations than shipping shiny new
features that immediately crumble outside ideal tutorial conditions.

##  Fragmentation & Functional Programming

` JAX ` has a “functional” API. Earlier, I mentioned that ` JAX ` functions
have to be pure (i.e they cannot have any global side effect. Just like
mathematical functions, given the same data the function will always return
the same output no matter the context of it’s execution.)

This design philosophy is what makes ` JAX ` stand out. Due to the functional
roots of ` JAX ` , ` JAX ` functions are often composable and interoperate
well with each other. It reduces the development complexity as functions are
defined with specific signatures and a well-defined, concrete task. If the
types are respected, then the function is guranteed* to work out-of-the-box.

This is well suited to the kinds of workloads that one needs in scientific
computing. In Deep Learning especially, since NNs are just a static functions,
this functional paradigm makes writing even complex codebases easy.

For example, let’s look at the ` optax ` API from the ` JAX ` ecosystem.

Due to the functional approach, ` optax ` has what we call a “chain” that
involves a bunch of functions sequentially applied on the gradients. So the
fundamental building blocks are ` GradientTransformation ` s.

This makes it a really powerful but expressive API to work with.

    
    
    optimizer = optax.adam(1e-2)
    

If I wanted to clip the grads here for example, I could do it trivially:

    
    
    optimiser = optax.chain(
        optax.clip_by_global_norm(1.0),
        optax.adam(1e-2),
    )
    

If I wanted to do a simple operation such as take the ` EMA ` of my grads, in
PyTorch that would’ve required setting up objects and then manually digging
through the codebases to place methods appropriately. But with ` optax ` ,

    
    
    optimiser = optax.chain(
        optax.clip_by_global_norm(1.0),
        optax.adam(1e-2),
        optax.ema(decay=0.999)
    )
    

A similar approach goes for combining optimizers, meta-learning approaches,
gradient accumulation etc. It’s simply much more cleaner than ` PyTorch ` .

Another cool consequence of a functional design is ` vmap ` . This stands for
‘vectorized’ map which accurately describes what it does. You can ` map `
anything and as long as its a ` vmap ` , then ` XLA ` will automatically fuse
and optimize it.

This means that when you write functions, you **don’t think about the batch
dimension!** You just ` vmap ` all you code and this simplifies things.

For one, you need less ` ein-* ` ops. While ` einops ` are great and all -
it’s simply more intuitive to grasp 2D/3D tensor manipulations, and are also
much more readable IMO. Let’s take an extremely limited example operation, and
compare the difference:

    
    
    arr: Array = jnp.ones((batch_size, seqlen, h_dim))
    
    def vanilla_func(arr: Array) -> Array:
      '''
      We want to do a: '(b s h, b s h) -> (b s s, b s h) -> b h s' operation.
      '''
      return ((arr @ arr.transpose(0, 2, 1)) @ arr).transpose(0, 2, 1)
    
    @jax.vmap
    def vmapped_func(arr: Array) -> Array:
      '''
      We want to do a: '(s h, s h) -> (s s, s h) -> h s' operation.
      '''
      return ((arr @ arr.T) @ arr).T
    

Even for this toy operation, you can immediately see how much more instantly
readable the function is. Now imagine that with the more complex tensor
manipulations, like the ones used in ` MHSA ` .

Subscribing to the functional paradigm means that it’s easier to write complex
code that works _well_ , since you only have to reason about individual
components in isolation. It’s both clean and performant because you can `
@jax.jit ` any pure function without worrying about anything else. It. Just.
Works.

In the functional world, as long as you respect the purity constraints and
have the right signature, you enjoy all the other benefits - such as
composability.

With ` torch ` however, there is a non-trivial chance that whatever stack you
use - say doing ` FSDP + multi-node + torch.compile + ... ` something will
_always_ break due to the sheer complexity involved. Multiple things have to
work correctly together, and if any component fails due to edge case, then you
would be debugging till 3 a.m.

And because there would **always** be bugs that weren’t caught during
development simply because it’s not possible to test each and every
combination of the dozens of features ` Pytorch ` offers, It’s simply
impossible to write code that works well without significant effort.

This has meant that the ` torch ` ecosystem has become very bloated and buggy
- things don’t interoperate well together, so contributors often come up with
new libraries and frameworks to solve specific issues (like say HuggingFace’s
` accelerate ` for distributed training) which in turn aren’t designed to
interface with other such “solutions” due to having no shared abstraction, so
it quickly devolves into a mess of dependencies and ` requirements.txt ` and a
training loop that looks like it was the scene of Guido Van Rossum’s murder.

I’d go on to say from my anecdotal experience about 70-80% of those GitHub
issues or forum discussions are simply due to various libraries erorring out
on each other.

Unfortunately, few solutions exist to fix it. This is very much an OOP as well
as a design problem. I _think_ having a fundamental, ` PyTorch ` ~y object
(like ` JAX ` ’s ` PyTree ` ) might’ve helped build a common base for
abstraction, but I’m not an SWE so I’m not sure how much it’d have _really_
helped.

Nor can you just adopt a functional programming paradigm, at which point you’d
have converged to a worse version of ` JAX ` while breaking all backwards
compatibility for every existing ` torch ` codebase.

The way I see it - ` PyTorch ` is well and truly fucked in this department.

##  Reproducibility

The “reproducility crisis” is an oft discussed problem in science, and AI/DL
has been no exception. Despite the existence of containerized environments and
version control, researchers refuse to use them and journals/conferences place
no requirements on them either. Even upholding your pledge to open-source the
code isn’t verified by academic institutions.

However, there are some design choices that nudge users to write code that
facilitates reproduction, with minimal effort. This incentivizes users to put
that little effort in and gain masive advantages in return - such as being
able to validate their older experiments at any point and ensure that
randomness is not a factor in any their results.

I believe such oversights are usually because of laziness/carelessness than
malicious intent. So such small decisions can ultimately add up to saving
potentially dozens of dev-hours and a lot of cussing.

###  Seeding

` torch ` ’s handling of something as simple as seeding is&mldr; not ideal.
Typically, you’d have to do:

    
    
    import torch
    import numpy as np
    
    np.random.seed(0) # if you're using numpy
    torch.manual_seed(0)
    torch.cuda.manual_seed_all(args.seed)
    torch.use_deterministic_algorithms(True)
    torch.utils.deterministic.fill_uninitialized_memory(True)
    

Which let’s be honest, isn’t really the end of the world coming at barely half
a dozen loc - But on the flipside, is easily forgettable/misconfigured
especially in the heat of deadlines.

I’ve personally known researchers who set the seeds in the wrong file at the
wrong place and they weren’t even used by ` torch ` at all - instead, were
just silently ignored, thus invalidating all their experiments. (That
researcher was me)

` JAX ` on the other hand forces you to create an explicit ` key ` which gets
passed to any function that required randomness. This approach completely
eliminates this problem as the RNG at all points is statically seeded. And
because ` jax ` has its own version of numpy ( ` jax.numpy ` ) you don’t need
to remember to seed it seperately.

This is a small fry - but I feel such small QoL decisions can end up making
the whole framework’s UX a whole lot better.

###  Portability

One of the biggest banes of using torch codebases is the lack of portability -
codebases written for running on CUDA/GPUs don’t really work well when run on
non-Nvidia hardware like TPUs, NPUs, AMD GPUs etc.

Worse, it’s hard to port torch code written for 1x (one) node and port it to
be multi-node. Multi-node often involves dozens of dev-hours and substantial
code changes to manually integrate it in the correct places. Unsurprisingly,
this quickly devolves into a horror story of errors, crashes and incorrect
comms that leech performance.

` JAX ` ’s compiler-centric approach however gives it a win in this
department. ` XLA ` handles switching between device backends for us - and it
already works well out-of-the-box on GPUs/TPUs/multi-node/multi-slice with
minimal to no code changes. (Support for AMD GPUs is also coming, however
anecdotally it’s not in a great place right now - which seems more reflective
of AMD than ` XLA ` .)

One only needs to implement a device backend for ` XLA ` to use, and it
automatically takes care of the intermediate steps of extracting computation
from graph as specified in a framework (Jax/TF/PyTorch), produce an HLO, and
then eventually emit a lower-level IR that hardware backends can then execute
during runtime.

Jax's hardware compatibility matrix, as of _Aug 2024_

This way makes it easier for hardware vendors to support their devices, as
well as make the transition between devices more easier.

I think this is an often overlooked, but important issue. Not everyone has
access to the same hardware, so codebases that are portable across different
types of hardware can be a small step towards making Deep Learning more
accessible to beginners/intermediates as well as preventing a lot of
frustration.

###  Auto Scaling

This point ties in with the idea of portability. Codebases that can
_autoscale_ well on their own are massively helpful during reproduction. In an
ideal case, this should happen automatically with minimal code changes,
unfetterd by networking boundaries.

As we’ve come to expect, ` JAX ` does this well. When writing ` JAX ` code,
you don’t need to specify communication primitives or do `
torch.distributed.barrier() ` everywhere - ` XLA ` automatically inserts that
for us, taking the available hardware in account.

This philosophy means that whatever devices ` JAX ` can _detect_ are
automatically used, irrespective of networking, topology, configuration etc.
You do not need to specify ranks or a central co-ordinator host. ` JAX `
automagically synchronizes and stages all the computations for you, as well as
apply optimization passes to maximize asynchronous execution of the kernels
and minimize latency.

All a person has to do is specify the sharding of the tensors you want to
distribute across, such as sharding the batch dimension of the input arrays
and due to ` XLA ` ’s “computation follows sharding” approach, it
automatically figures out the rest. This is due to the [ GSPMD
](https://arxiv.org/abs/2105.04663) partitioner in the XLA compiler stack.

This is really powerful, as experiments that have been validated at scale can
be run by hobbyists easily to play around with them and potentially iterate on
them - and vice-versa.

I feel this could help in discovery of forgotten ideas more easily, and
encourage the field to be more ‘ [ bitter
](http://www.incompleteideas.net/IncIdeas/BitterLesson.html) ’ - as ideas
could be easily tested as a function at bigger scales with minimal effort,
thus incentivizing such experiments.

##  The Cons

I have been disproportionately covering only the problems plaguing torch so
far. But it’s not all roses with ` JAX ` either. There are a few major
concerns that I wish are given far more attention among ` JAX/XLA ` devs:

###  Governance structure

Currently, ` XLA ` is under TF governance, and while talk has been made of
establishing a seperate organizing body to manage all affairs, similar to
torch, not much concrete efforts have been made - atleast publicly.

Unfortunately, there isn’t a lot of trust in Google at the moment due to its
reputation to axe unpopular products. Now, ` JAX ` is technically a DeepMind
project and of core significance to Google’s entire AI push, but still I feel
that having a seperate governing body would be of great long-term benefit for
the ecosystem as a whole by providing guidance to the development of the
project.

This would give it a concrete structure, and decouple it with Google’s
infamous bureaucracy - thus avoiding a whole host of problems in a single
sweep.

I don’t think ` JAX ` necessary _needs_ an official structure of this sort,
but rather it’d be nice to have a gurantee that ` JAX ` development will take
place for a long time regardless of Google upper-management’s decisions.

It would definitely help its case in adoption among companies and big labs as
well, who are hesitant to spend resources incorporating tools that might stop
being maintained at some point.

###  Open source transition of ` XLA `

For the longest time, ` XLA ` was a closed-source project. However, efforts
have been made to open source it, and now [ ` OpenXLA `
](https://openxla.org/) is at well outperforms the internal XLA build.

However, documentation about the internals of ` XLA ` is still sparse. Most of
the resources are just live talks and the occasional paper, which are often
out-of-date.

Having a publicly accessible roadmap of upcoming features would make it easier
for people to track progress and contribute to things they find particularly
interesting.

I think it’d be nice to give practitioners a way to better gauge what ` XLA `
can and can’t do through [ Edward Yang styled
](http://blog.ezyang.com/2019/05/pytorch-internals/) mini-blogposts that
breakdown each stage of the ` XLA ` compiler stack and explain the nitty-
gritty details.

I understand that this is resource intensive, which could be better directed
elsewhere but I feel that people trust the tools more when they understand
them, and there’s a positive spillover effect across the entire ecosystem that
ends up benefitting everyone.

###  Coalescing ecosystem

For various reasons outside the scope of this blog, I heartily dislike ` flax
` . It’s a bane on the ` JAX ` ecosystem. It has an unintuitive API, terse
syntax and is absolutely hell for beginners transitioning from ` PyTorch ` .

Just use ` equinox ` .

There have been attempts to fix ` flax ` ’s shortcomings from the dev team,
namely by using [ ` NNX `
](https://flax.readthedocs.io/en/v0.8.3/experimental/nnx/index.html) which is
supposed to be a more “equinox-y” wrapper ontop of ` flax ` .

However, I think it’s ultimately a waste of time. If you want an ` equinox `
-styled API, then just use ` equinox ` . There isn’t a lot ` flax ` does
especially better that’s hard to replicate with ` equinox ` . Plus, having
little to no abstraction makes implementing things in ` equinox ` much easier
and faster.

Right now, a lot of the ` JAX ` ecosystem is designed around ` flax ` . `
equinox ` , because it fundamentally interfaces with ` PyTree ` s is cross-
compatible with all libraries, however you do have to do a little `
eqx.partition ` -ing and ` filter ` -ing, which can be a bit annoying.

I want to change the status quo. It should be the other way around - ` equinox
` should have first class support everywhere. Considering its popularity, I
think this decision would objectively make thigns easier for the vast majority
of serious ` JAX ` users and big codebases.

I know this is a controversial opinion simply because a lot of resources have
been poured into ` flax ` \- But this is classic [ sunk-cost fallacy
](https://en.wikipedia.org/wiki/Sunk_cost) . ` equinox ` just does it better,
in the way a ` JAX ` framework should always have been like. It may not be
perfect, but its better than the alternatives by a mile.

` equinox ` vs. ` flax ` : as neatly summarized in the [ equinox docs ](url) .

It’s good to see that maintainers of the ` JAX ` ecosystem are realizing the
popularity of ` equinox ` and adjusting accordingly - however, I’d love to see
a bit more love officially from Google and the ` flax ` team as well.

If you want to try out ` JAX ` \- it’s not even a question. Use ` equinox ` .
You’ll thank me.

> “I’ve been using ` equinox ` for a few months now and I’ve never felt
> better. I have more energy. My skin is clearer. My eye sight has improved.”
> – Me

###  Sharp edges

Due to some of the API design decisions and ` XLA ` restrictions, ` JAX ` has
some “sharp edges” that you should be careful of. The well-written
documentation explains this very concisely:

[ Common Gotchas in Jax.
](https://jax.readthedocs.io/en/latest/notebooks/Common_Gotchas_in_JAX.html)

So go give that a read atleast once before using ` JAX ` . It’ll save you a
lot of time and energy (as RTFM-ing always does).

##  Conclusion

This blogpost was to correct the often-parotted myth that ` PyTorch ` is
simply the best for any real research workloads - especially on GPUs. That
simply isn’t the case anymore.

Infact, I’d go as far as to argue that porting all ` Torch ` code to ` JAX `
would be _immensely_ beneficial to the field as a whole. These are not minor
features - having autoparallelization, reproducibility, a clean functional API
etc. would be a godsend for a lot of research codebases.

So if you want to make this field a little bit better, consider rewriting your
codebases in ` JAX ` .

Shoutout to [ Patrick Kidger ](https://kidger.site/) as well for developing `
equinox ` . If you’re coming from ` PyTorch ` , I cannot recommend it enough!


-->

<!--






-->

