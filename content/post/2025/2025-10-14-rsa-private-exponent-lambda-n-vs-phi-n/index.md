---
title: "RSA 개인키는 왜 λ(n) 기준으로 정의될까? RCF와 NIST로 확인한 변화"
date: 2025-10-14T00:00:00+09:00
lastmod: 2025-10-14T16:03:23+09:00
categories:
  - Cryptography
  - Math
tags:
  - RSA
  - PKCS1
  - PKCS #1 v2.2
  - RFC 8017
  - NIST SP 800-56B
  - Carmichael Function
  - Carmichael Lambda
  - λ(n)
  - Euler Totient
  - φ(n)
  - Totient
  - Modular Inverse
  - Modular Arithmetic
  - Public Key
  - Private Key
  - Exponent
  - 65537
  - Key Generation
  - CRT
  - Garner Algorithm
  - Chinese Remainder Theorem
  - Cryptography Standards
  - IETF
  - NIST
  - IEEE 1363
  - ASN.1
  - RSASSA-PSS
  - RSAES-OAEP
  - Security Proofs
  - Performance
  - Decryption Speed
  - lcm
  - gcd
  - prime
  - modulus
  - factorization
  - keypair
  - key establishment
  - OAEP
  - PSS
  - CMS
  - X.509
  - Crypto Engineering
  - Practical Cryptography
  - 수학
  - 암호학
  - 공개키암호
  - 개인키
  - 공개키
  - 카르마이클 함수
  - 오일러 피함수
  - 모듈러 역원
  - 키 생성
  - 성능 최적화
  - 정수론
description: "현대 RSA에서 개인지수 d는 φ(n)이 아닌 λ(n)=lcm(p−1,q−1,…) 기준에서 e의 모듈러 역원으로 정의된다. IETF RFC 8017과 NIST SP 800-56B의 정확한 조항을 인용해 이 변화를 확인하고, 왜 λ(n)가 채택되었는지(작은 d, 약간의 복호화 이득, CRT·Garner와의 관계), 실무적 영향과 보안 측면을 전문가 관점에서 정리한다."
image: "wordcloud.png"
---

현대 RSA의 개인키 정의는 조용히 바뀌었다. 고전적인 교과서 표현처럼 φ(n) 기준으로 d를 잡는 것이 아니라, 표준은 λ(n)=lcm(p−1,q−1,…)에 대해 `e · d ≡ 1 (mod λ(n))`를 만족하는 d를 사용한다. 이 글은 해당 변화가 실제 표준에 어떻게 명시되는지와, 이를 선택한 이유 및 실무 영향까지 한 번에 정리한다.

## 표준에서의 명시

- RFC 8017(PKCS #1 v2.2)
  - §3.1: 공개키 조건에 “GCD(e, λ(n)) = 1, where λ(n) = LCM(r1−1, …, ru−1)”를 명시한다.
  - §3.2: 개인키 조건에 “d satisfies e · d ≡ 1 (mod λ(n))”를 명시한다.
  - 참조: RFC 8017 §3.1, §3.2

- NIST SP 800-56B Rev.2
  - RSA 기반 정수분해 암호에서 키 조건을 λ(n) 기준으로 두고, e와 λ(n)이 서로소이며 d ≡ e⁻¹ (mod λ(n))가 되도록 정의한다.
  - 참조: NIST SP 800-56B Rev.2 문서 본문

위 두 문서는 오늘날 실무 표준이 λ(n) 정의를 채택한다는 점을 직접 확인해 준다. 전통적 φ(n) 정의와의 차이는 개념이 바뀐 것이 아니라, 올바른 최소 주기(λ(n))에 대한 모듈러 역원을 쓰도록 정리되었다는 데 있다.

## 카르마이클 함수 λ(n) 한눈에 보기

- 정의: λ(n)은 모든 \(gcd(a,n)=1\)인 정수 a에 대해 \(a^{\lambda(n)} \equiv 1 \pmod n\)를 만족하는 가장 작은 양의 정수다. 이는 \((\mathbb{Z}/n\mathbb{Z})^{\times}\)의 지수(exponent)이기도 하다.
- 성질:
  - 항상 \(\lambda(n)\mid\varphi(n)\)이며, \(n=pq\) (서로 다른 홀수 소수)일 때 \(\lambda(n)=\operatorname{lcm}(p-1, q-1)\).
  - 일반적으로 소인수 분해가 \(n=\prod p_i^{r_i}\)이면 \(\lambda(n)=\operatorname{lcm}(\lambda(p_1^{r_1}),\dots,\lambda(p_k^{r_k}))\).
  - 중국인의 나머지 정리(CRT)와 결합해 \(a^{\lambda(n)}\equiv 1\pmod n\)가 도출된다.
- RSA와의 연관: RSA에서 개인지수는 `e · d ≡ 1 (mod λ(n))`로 두는 것이 표준이며, 이때 \(\lambda(n)\)은 φ(n)보다 작거나 같아 d가 더 작아지는 경향이 있다.


## 왜 φ(n) 대신 λ(n)인가?

- 최소 지수 성질: λ(n)는 “모든 a(\(gcd(a,n)=1\))에 대해 a^{λ(n)} ≡ 1 (mod n)”을 만족하는 **최소** 양의 정수다. φ(n)은 이를 보장하는(대개 더 큰) 상한이다.
- 작은 d 유도: λ(n) | φ(n)이므로, 같은 e에 대해 d는 보통 더 작게 나와 복호화가 근소하게 빨라질 수 있다.
- CRT/가너와의 궁합: 실제 속도 이득은 λ(n) 자체보다 CRT 분해와 Garner 알고리즘을 통한 구현 최적화에서 더 크게 난다. 표준도 CRT 지표(dP, dQ 등)와 Garner를 일관되게 정의한다.

실험적으로 gcd(p−1, q−1)의 기대 크기가 커지지 않아 λ(n)/φ(n) 차이에 따른 체감 성능 이득은 작다. 하지만 수학적으로 더 타이트한 지표를 쓰는 것이 정의상 깔끔하며, CRT 계보와도 자연스럽게 맞물린다.

## 키 생성 관행 업데이트

- e 고정, d 계산: 현대 구현은 보통 e=65537을 고정하고, `d = e^{-1} mod λ(n)`을 계산한다. e의 선택 이유는 안전성과 성능의 균형(짧은 해밍 무게, 적절한 보안 관행)이다.
- 검증 조건: 표준은 `gcd(e, λ(n)) = 1`을 요구하며, 개인키 표현은 (n,d) 또는 CRT 형태(p,q,dP,dQ,qInv, …)를 모두 허용한다.

## 보안과 성능 관점의 정리

- 보안 수준: λ(n) 기반 정의는 RSA의 안전 가정(인수분해/지수 역상 불가능성)과 양립하며, OAEP·PSS 같은 상위 스킴의 안전성 증명과도 충돌하지 않는다.
- 성능: λ(n) 사용만으로의 이득은 제한적. 실무 성능은 CRT 분해, 모듈러 거듭제곱 최적화, 상수시간 구현 및 캐시/분기 완화가 좌우한다.

## 구현 체크리스트

- 키 검증: n이 서로 다른 홀수 소수의 곱인지, gcd(e, λ(n))=1인지 확인한다.
- CRT 경로: dP=d mod (p−1), dQ=d mod (q−1), qInv=q^{−1} mod p를 정확히 세팅한다.
- 타이밍/에러 채널: 복호·검증 실패 경로를 통합하고, 블라인딩 등 부채널 완화를 적용한다.

## 참고 링크

- [RFC 8017: PKCS #1 v2.2 — §3.1, §3.2](https://www.rfc-editor.org/rfc/rfc8017)
- [NIST SP 800-56B Rev.2](https://csrc.nist.gov/pubs/sp/800/56/b/r2/final)
- [Wikipedia: Carmichael function](https://en.wikipedia.org/wiki/Carmichael_function)


