---
image: "wordcloud.png"
slug: encryption-and-hashing
collection_order: 23
draft: false
title: "[Computer Terms] 암호화와 해싱 (Encryption, Hashing)"
date: 2026-07-21
last_modified_at: 2026-07-21
categories: ComputerTerms
description: "암호화는 되돌릴 수 있게 데이터를 숨기고, 해싱은 되돌릴 수 없게 지문을 만듭니다. 대칭키·비대칭키 암호화와, 비밀번호를 안전하게 저장하는 솔팅된 해시를 비교합니다."
tags:
- Technology(기술)
- Education(교육)
- Security(보안)
- Encryption(암호화)
- Hashing(해싱)
- Cryptography(암호학)
- TLS
- Password(비밀번호)
- Reference(참고)
- Documentation(문서화)
- Tutorial(튜토리얼)
- Guide(가이드)
- Beginner
- Computer-Science(컴퓨터과학)
- Fundamentals(기초)
- Best-Practices
- Comparison(비교)
- Deep-Dive
- Case-Study
- Software-Engineering(소프트웨어공학)
- Data-Integrity(데이터무결성)
- Hash-Table(해시테이블)
- Debugging(디버깅)
- Performance(성능)
- Advanced
---

## 이 장을 읽기 전에

[HTTP와 HTTPS](/post/computerterms/http-and-https/)에서 언급한 TLS 핸드셰이크의 "비대칭키로 대칭키를 교환한다"는 설명을 이 챕터에서 자세히 풀어 다룬다. 또한 [해시테이블](/post/computerterms/hash-tables/)에서 다룬 해시 함수 개념을 전제로, 이번에는 그 해시 함수를 보안 목적으로 쓸 때 무엇이 달라지는지를 다룬다.

## 암호화: 되돌릴 수 있게 숨기기

**암호화(Encryption)**는 원본 데이터(평문)를 키를 모르면 읽을 수 없는 형태(암호문)로 바꾸되, 올바른 키가 있으면 다시 원본으로 되돌릴 수 있는(복호화) 변환이다. 암호화는 크게 두 방식으로 나뉜다. **대칭키 암호화**(AES 등)는 암호화와 복호화에 같은 키를 쓴다 — 계산이 빠르지만, 통신 양쪽이 안전하게 같은 키를 미리 공유해야 한다는 문제가 있다. **비대칭키 암호화**(RSA 등)는 공개키로 암호화하고 그 짝인 개인키로만 복호화할 수 있다(또는 반대) — 공개키는 누구에게나 공개해도 안전하지만, 계산 비용이 대칭키보다 훨씬 크다.

[HTTP와 HTTPS](/post/computerterms/http-and-https/)의 TLS 핸드셰이크가 두 방식을 조합하는 이유가 여기 있다. 비대칭키로 안전하게 대칭키(세션키)를 교환한 뒤, 실제 데이터는 훨씬 빠른 대칭키로 암호화한다 — 매 요청마다 비대칭키 연산을 쓰면 계산 비용이 감당하기 어렵기 때문이다.

## 해싱: 되돌릴 수 없는 지문 만들기

**해싱(Hashing)**은 [해시테이블](/post/computerterms/hash-tables/)에서 다룬 것과 같은 "임의 길이 데이터를 고정 길이 값으로 바꾸는" 연산이지만, 목적이 다르다. 해시테이블의 해시 함수는 충돌만 적당히 분산시키면 충분했다. 보안용 해시 함수(SHA-256 등)는 **암호학적 해시 함수**라 불리며, 다음 세 성질을 추가로 만족해야 한다. **역상 저항성**: 해시값에서 원본을 역산하는 것이 계산적으로 불가능해야 한다. **충돌 저항성**: 같은 해시값을 내는 서로 다른 두 입력을 찾는 것이 계산적으로 어려워야 한다. **눈사태 효과**: 입력을 1비트만 바꿔도 해시값이 완전히 달라져야 한다.

```c
#include <stdio.h>
#include <string.h>
#include <openssl/sha.h>

void print_sha256(const char *input) {
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256((unsigned char *)input, strlen(input), hash);

    for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
        printf("%02x", hash[i]);
    }
    printf("\n");
}

int main(void) {
    print_sha256("password123");
    print_sha256("password124");   /* 1글자만 다른데도 해시값은 완전히 다름 */
    return 0;
}
```

`gcc sha_demo.c -lcrypto -o sha_demo`로 컴파일하면(OpenSSL 라이브러리 필요), 입력이 한 글자만 달라도 두 해시값 사이에 아무런 규칙성이 없다는 것을 확인할 수 있다.

## 비밀번호는 왜 암호화가 아니라 해싱으로 저장하는가

비밀번호를 암호화해서 저장하면, 그 암호화 키가 유출될 경우 모든 비밀번호가 그대로 복호화될 수 있다. 반면 해싱은 애초에 되돌릴 수 없으므로, 데이터베이스가 유출돼도 공격자는 해시값만 얻을 뿐 원본 비밀번호를 직접 계산해낼 수 없다 — 이것이 로그인 시스템이 비밀번호를 "암호화"가 아니라 "해싱"해서 저장하는 이유다.

다만 단순 해싱만으로는 부족하다. 공격자가 흔한 비밀번호들을 미리 해싱해 둔 **레인보우 테이블(Rainbow Table)**과 비교하면, 해시값만으로도 원본 비밀번호를 빠르게 추정할 수 있다. 이를 막기 위해 각 비밀번호에 무작위 값(**솔트, Salt**)을 덧붙여 해싱한다 — 같은 비밀번호라도 사용자마다 다른 솔트 때문에 해시값이 달라져, 미리 계산해 둔 레인보우 테이블이 무력화된다.

```c
#include <stdio.h>
#include <string.h>
#include <openssl/sha.h>

void hash_password(const char *password, const char *salt, unsigned char *out) {
    char combined[256];
    snprintf(combined, sizeof(combined), "%s%s", salt, password);   /* 솔트 + 비밀번호 결합 */
    SHA256((unsigned char *)combined, strlen(combined), out);
}

int main(void) {
    unsigned char hash1[SHA256_DIGEST_LENGTH], hash2[SHA256_DIGEST_LENGTH];

    hash_password("password123", "salt_for_alice", hash1);
    hash_password("password123", "salt_for_bob", hash2);   /* 같은 비밀번호, 다른 솔트 */

    /* hash1과 hash2는 서로 다른 값 → 레인보우 테이블 대조가 무력화됨 */
    printf("두 해시가 같은가: %s\n", memcmp(hash1, hash2, SHA256_DIGEST_LENGTH) == 0 ? "예" : "아니오");
    return 0;
}
```

## 비교: 암호화 vs 해싱

| 특성 | 암호화 | 해싱 |
|---|---|---|
| 되돌릴 수 있는가 | 가능 (올바른 키로 복호화) | 불가능 (설계상 역산 불가) |
| 출력 길이 | 입력 길이에 비례 | 항상 고정 길이 |
| 대표 용도 | 통신 내용 보호(TLS), 저장 데이터 보호 | 비밀번호 저장, 데이터 무결성 검증 |
| 필요한 것 | 키(대칭 또는 비대칭) | 없음(솔트는 키가 아니라 무작위값) |

## 흔한 오개념

**"SHA-256은 원래 비밀번호 저장용으로 충분히 안전하다"** — SHA-256 같은 범용 암호학적 해시는 애초에 **빠르게 계산되도록** 설계됐다. 이 "빠름"은 공격자가 초당 수십억 개의 후보 비밀번호를 대입해보는 무차별 대입 공격에는 오히려 유리하게 작용한다. 그래서 실무 비밀번호 저장에는 SHA-256을 직접 쓰기보다, 의도적으로 계산을 느리게 만든 bcrypt·scrypt·Argon2 같은 **비밀번호 전용 해시 함수**를 쓴다.

**"솔트는 비밀로 보관해야 한다"** — 솔트의 역할은 "같은 비밀번호도 다른 해시값을 갖게" 만드는 것이지, 그 자체를 숨기는 것이 아니다. 솔트는 보통 해시값과 함께 평문으로 저장되며, 안전성은 솔트를 숨기는 데서 오는 것이 아니라 사용자마다 다른 무작위 값이라는 데서 온다.

## 다른 개념과의 연결

이 챕터의 대칭키/비대칭키 조합은 [HTTP와 HTTPS](/post/computerterms/http-and-https/)의 TLS 핸드셰이크를 완성하는 마지막 조각이다. 다음 챕터에서는 이 암호화·해싱을 실제로 "누가 접근할 수 있는가"를 결정하는 인증·인가 문제로 확장한다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 암호화와 해싱의 근본적인 차이(되돌릴 수 있는가)와 각각의 적합한 용도를 설명할 수 있다. 대칭키와 비대칭키를 TLS가 함께 쓰는 이유를 설명할 수 있다. 비밀번호를 SHA-256으로 직접 해싱하는 것이 왜 충분히 안전하지 않은지, 솔트와 느린 해시 함수가 각각 어떤 공격을 막는지 설명할 수 있다.

## 참고 자료

> Katz, J., & Lindell, Y. (2020). *Introduction to Modern Cryptography* (3rd ed.), Chapter 1: Introduction. CRC Press.

- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) — bcrypt/Argon2 선택 기준과 솔팅 실무 가이드
- [NIST FIPS 180-4: Secure Hash Standard](https://csrc.nist.gov/publications/detail/fips/180/4/final) — SHA-256을 포함한 표준 해시 함수 사양
