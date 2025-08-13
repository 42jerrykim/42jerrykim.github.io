---
title: "[Algorithm] C++ 백준 13727번 : 5차원 구사과 초콜릿"
description: "백준 13727 5차원 구사과 초콜릿은 2×2×2×2×n 격자를 1×1×1×1×2 도미노로 채우는 가짓수를 구하는 문제입니다. 비트마스크 DP로 초항을 만들고 Berlekamp–Massey로 선형 점화를 복원해 O(log n)으로 n번째 항을 구하는 C++ 풀이를 정리합니다."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "Algorithm"
- "BOJ"
tags:
- "BOJ"
- "Baekjoon"
- "백준"
- "13727"
- "5차원"
- "구사과"
- "초콜릿"
- "도미노 타일링"
- "Domino Tiling"
- "타일 채우기"
- "Perfect Matching"
- "완전 매칭"
- "Grid Graph"
- "격자 그래프"
- "P2"
- "Pn"
- "P2xP2xP2xP2xPn"
- "Cartesian Product"
- "카르테시안 곱"
- "Berlekamp–Massey"
- "BM"
- "선형 점화"
- "Linear Recurrence"
- "Minimal Polynomial"
- "Linear Algebra"
- "다항식 거듭제곱"
- "Polynomial Exponentiation"
- "빠른 거듭제곱"
- "Exponentiation by Squaring"
- "C++"
- "CPP"
- "GNU++17"
- "mod"
- "모듈러"
- "나머지 연산"
- "O(log n)"
- "시간복잡도"
- "시간 복잡도"
- "수열"
- "Sequence"
- "Bitmask DP"
- "비트마스크"
- "상태 압축"
- "State Compression"
- "DP"
- "Dynamic Programming"
- "그래프 이론"
- "Graph Theory"
- "Matching"
- "Perfect Matchings"
- "High-dimensional"
- "고차원"
- "컴페티티브 프로그래밍"
- "Competitive Programming"
- "Problem Solving"
- "PS"
- "Solution Code"
- "정답 코드"
image: "wordcloud.png"
---

문제: [BOJ 13727 - 5차원 구사과 초콜릿](https://www.acmicpc.net/problem/13727)

### 아이디어 요약
- 대상 그래프는 `P2×P2×P2×P2×Pn` 격자이며, 이는 5차원 2×2×2×2×n 보드의 도미노 타일링(완전 매칭) 개수입니다.
- 4차원 단면(2×2×2×2=16칸)의 인접 관계를 미리 구성해 한 열에서 다음 열로 넘어가는 전이(`state -> next_state`)를 비트마스크 DFS로 생성합니다.
- 나이브 전이 DP로 초항을 충분히 구한 뒤, Berlekamp–Massey(BM)로 수열의 최소 선형 점화를 복원합니다.
- 점화가 복원되면 다항식 빠른 제곱으로 `O(log n)`에 n번째 항을 계산합니다. 최종 결과는 `1e9+7`로 모듈러 연산합니다.

### C++ 풀이

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있습니다.
#include <bits/stdc++.h>
using namespace std;

using int64 = long long;
static const int64 MOD = 1000000007;

static inline int64 modPow(int64 base, int64 exp) {
  int64 result = 1 % MOD;
  base %= MOD;
  while (exp > 0) {
    if (exp & 1) result = (result * base) % MOD;
    base = (base * base) % MOD;
    exp >>= 1;
  }
  return result;
}

// Berlekamp–Massey: 최소 선형 점화계수 rec 반환
// s[n] = sum_{i=1..L} rec[i-1] * s[n-i] (mod MOD)
static vector<int64> berlekamp_massey(const vector<int64>& s) {
  vector<int64> ls, cur; // ls: last successful, cur: current
  int lf = 0;            // last fail index
  int64 ld = 1;          // last delta
  for (int i = 0; i < (int)s.size(); i++) {
    int64 t = 0;
    for (int j = 0; j < (int)cur.size(); j++) {
      t = (t + s[i - j - 1] * cur[j]) % MOD;
    }
    int64 delta = (t - s[i]) % MOD;
    if (delta < 0) delta += MOD;
    if (delta == 0) continue;
    if (cur.empty()) {
      cur.assign(i + 1, 0);
      lf = i;
      ld = delta;
      continue;
    }
    int64 k = delta * modPow(ld, MOD - 2) % MOD;
    vector<int64> c(i - lf - 1, 0);
    c.push_back(k);
    for (auto &x : ls) c.push_back((MOD - x) * k % MOD);
    if ((int)c.size() < (int)cur.size()) c.resize(cur.size(), 0);
    for (int j = 0; j < (int)cur.size(); j++) {
      c[j] = (c[j] + cur[j]) % MOD;
    }
    if (i - lf + (int)ls.size() >= (int)cur.size()) {
      ls = cur;
      lf = i;
      ld = delta;
    }
    cur.swap(c);
  }
  for (auto &x : cur) { x %= MOD; if (x < 0) x += MOD; }
  return cur;
}

// rec(길이 m), 초기 s[0..m-1]로 n번째 항 계산 (O(m^2 log n))
static int64 get_nth(const vector<int64>& rec, const vector<int64>& init, long long n) {
  int m = (int)rec.size();
  if (n < (long long)init.size()) return init[(size_t)n];

  auto combine = [&](const vector<int64>& a, const vector<int64>& b) {
    // 다항식 곱셈 후 rec로 나머지
    vector<int64> res(2 * m + 1, 0);
    for (int i = 0; i < m; i++) {
      for (int j = 0; j < m; j++) {
        res[i + j] = (res[i + j] + a[i] * b[j]) % MOD;
      }
    }
    for (int i = 2 * m - 1; i >= m; --i) {
      for (int j = 1; j <= m; j++) {
        res[i - j] = (res[i - j] + res[i] * rec[j - 1]) % MOD;
      }
    }
    res.resize(m);
    return res;
  };

  vector<int64> pol(m, 0), e(m, 0);
  pol[0] = 1;           // 단위 다항식
  if (m == 1) e[0] = rec[0]; else e[1] = 1; // x

  long long k = n;
  while (k > 0) {
    if (k & 1) pol = combine(pol, e);
    e = combine(e, e);
    k >>= 1;
  }

  int64 ans = 0;
  for (int i = 0; i < m; i++) {
    ans = (ans + pol[i] * init[i]) % MOD;
  }
  return ans;
}

// 초기 항 s가 주어질 때, n번째 항
static int64 guess_nth_term(const vector<int64>& s, long long n) {
  if (n < (long long)s.size()) return s[(size_t)n];
  vector<int64> rec = berlekamp_massey(s);
  if (rec.empty()) return 0;
  return get_nth(rec, s, n);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  // s[n] = 2x2x2x2xn 5D 초콜릿을 1x1x1x1x2 도미노로 채우는 경우의 수 (n=0부터)
  // n=1 -> 272, n=2 -> 589185, n=3 -> 930336768 ...
  const vector<int64> s = {
    1, 272, 589185, 930336768, 853401154, 217676188, 136558333, 415722813, 985269529,
    791527976, 201836136, 382110354, 441223705, 661537677, 641601343, 897033284, 816519670,
    365311407, 300643484, 936803543, 681929467, 462484986, 13900203, 657627114, 96637209,
    577140657, 600647073, 254604056, 102389682, 811580173, 592550067, 587171680, 526467503,
    265885773, 951722780, 219627841, 371508152, 283501391, 159234514, 439380999, 722868959,
    125599834, 351398134, 456317548, 365496182, 614778702, 502680047, 193063685, 309004764,
    743901785, 870955115, 312807829, 160375015, 691844624, 137034372, 350330868, 895680450,
    282610535, 317897557, 28600551, 583305647, 539409363, 327406961, 627805385, 680183978,
    681299085, 954964592, 743524009, 788048339, 699454626, 666369521, 857206425, 490463127,
    477198247, 599963928, 21247982, 107843532, 753662937, 239039324, 608530376, 523383010,
    654448101, 801430395, 393034561, 93313778, 983052766, 240336620, 825539982, 525118275,
    563899476, 706271688, 547405697, 477082486, 664058071, 353207278, 729486413, 795704637,
    999271072, 540749624, 411451016, 736422999, 879369181, 918733916, 982303557, 512499644,
    261033810, 391766409, 334092786, 931794834, 854181848, 821090190, 751839258, 433126935,
    571194155, 52438113, 552977155, 320805296, 173355929, 969659468, 258854248, 159509877,
    374487748, 401382023, 44060530, 510164669, 336596764, 652050424, 373872552, 517226592,
    719871041, 43959496, 235333335, 304962191, 253114421, 43638769, 361871585, 8060121,
    147014624, 114846460, 430864038, 368951246, 863795701, 36066788, 971606149, 935875286,
    486724123, 73790652, 236936530, 307697424, 753314001, 40450345, 529462842, 166162047,
    974102330, 600865526, 63237062, 749041914, 670937123, 806399597, 776678839, 842565920,
    608499253, 469062485, 842196981, 247762946, 778570576, 237951782, 286343384, 988318575,
    147255879, 905747089, 711062313, 21396079, 826846622, 443781794, 786474911, 400737121,
    844768961, 686214818, 590050845, 855473150, 18501778, 33258755, 398169058, 811192244,
    710397887, 591757177, 775311969, 168256434, 509615161, 489764304, 605188191, 498085780,
    164388183, 524662873, 322602324, 853641480, 205349527, 308211944, 93153206
  };

  long long n;
  if (!(cin >> n)) return 0;
  cout << guess_nth_term(s, n) << '\n';
  return 0;
}
```

### 복잡도
- 전처리(BM용 초항 생성)는 별도이며, 점화 복원 이후 `O(m^2 log n)`에서 `m`은 점화 차수(상수 수십 내외)입니다.
- 메모리: `O(m)`.

### 참고
- 문제: `https://www.acmicpc.net/problem/13727`
- 아이디어: 4차원 단면 상태 전이 + BM로 점화 복원 + 다항식 제곱으로 항 계산


