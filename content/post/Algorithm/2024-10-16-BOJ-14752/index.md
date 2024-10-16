---
title: "[Algorithm] C++ 백준 14572번 : 스터디 그룹"
categories: Algorithm
tags:
- Two Pointers
- Sliding Window
- Greedy
- Optimization
- Time Complexity O(NK)
- Data Structures
- Algorithm
image: "tmp_wordcloud.png"
date: 2024-10-16
---

알고리즘 문제를 풀다 보면 다양한 조건을 만족하면서 최대 혹은 최소 값을 구하는 문제가 자주 등장한다. 이번에 살펴볼 문제는 백준 온라인 저지의 14572번 "스터디 그룹"이다. 이 문제는 주어진 조건 하에서 스터디 그룹의 효율성을 최대화하는 그룹을 찾는 것이다.

문제 : [https://www.acmicpc.net/problem/14572](https://www.acmicpc.net/problem/14572)

## 문제 설명

신입생 현우는 알고리즘 공부가 정말 재미있어서 스터디 그룹을 만들어 더욱 열심히 공부하려고 한다. 하지만 그룹에 참여하는 학생이 너무 많으면 효율이 떨어질 것을 우려하여 아래와 같은 조건을 내걸었다.

- **조건 1**: 그룹 내에서 가장 잘하는 학생과 가장 못하는 학생의 실력 차이가 \( D \) 이하이어야 한다.
- **조건 2**: 그룹의 효율성 \( E \)는 다음과 같이 정의된다.
  
  \(
  E = (\text{그룹 내의 학생들이 아는 모든 알고리즘의 수} - \text{그룹 내의 모든 학생들이 아는 알고리즘의 수}) \times \text{그룹원의 수}
  \)

현우는 각 학생들의 실력을 수치화하고, 중요한 알고리즘 \( K \)개에 대해 각 학생들이 어떤 알고리즘을 알고 있는지 조사하였다. 이때, 위의 두 가지 조건을 만족하는 학생들의 부분집합 중 효율성이 최대가 되는 그룹을 찾아야 한다.

**입력 조건**:

- 첫 줄에 학생의 수 \( N \), 알고리즘의 수 \( K \), 그리고 실력 차이의 최대값 \( D \)가 주어진다. \( (1 \leq N \leq 10^5, 1 \leq K \leq 30, 0 \leq D \leq 10^9) \).
- 다음 \( N \)개의 줄에는 각 학생에 대한 정보가 주어진다.
  - 각 줄은 먼저 해당 학생이 알고 있는 알고리즘의 수 \( M \)과 실력 \( d \)가 주어진다. \( (0 \leq M \leq K, 0 \leq d \leq 10^9) \).
  - 다음 줄에 \( M \)개의 정수로 해당 학생이 알고 있는 알고리즘 번호 \( A_i \)가 주어진다. \( (1 \leq A_i \leq K) \).

**출력 조건**:

- 조건을 만족하는 그룹 중 효율성이 최대가 되는 그룹의 효율성을 출력한다.

## 접근 방식

이 문제는 두 가지 주요한 조건을 만족하면서 효율성을 최대화해야 하므로, 효율적인 알고리즘이 필요하다. 우선, 학생들의 실력 차이가 \( D \) 이하인 그룹을 찾아야 하므로, 실력 기준으로 학생들을 정렬하고 슬라이딩 윈도우를 사용하여 조건을 만족하는 그룹을 찾을 수 있다.

또한, 알고리즘의 수 \( K \)가 최대 30이므로, 각 학생이 알고 있는 알고리즘을 비트마스크나 배열로 관리할 수 있다. 그러나 비트마스크를 사용하면 두 집합의 교집합이나 합집합 연산이 필요할 때 시간이 많이 걸릴 수 있으므로, 배열을 사용하는 것이 더 효율적이다.

따라서, 다음과 같은 전략을 사용한다.

1. **학생들을 실력 기준으로 정렬**한다.
2. **투 포인터**를 사용하여 슬라이딩 윈도우를 확장하고 축소하면서 실력 차이가 \( D \) 이하인 그룹을 찾는다.
3. 현재 윈도우 내의 학생들이 알고 있는 알고리즘을 관리하기 위해 **카운트 배열**을 사용한다.
   - 각 알고리즘에 대해 현재 윈도우에서 알고 있는 학생 수를 저장한다.
4. 그룹의 효율성 \( E \)를 계산하기 위해 다음을 유지한다.
   - **total_known**: 현재 그룹에서 알고 있는 모든 알고리즘의 수 (중복 제거).
   - **total_known_by_all**: 현재 그룹의 모든 학생이 알고 있는 알고리즘의 수.
5. 윈도우를 이동할 때마다 \( E \)를 계산하고 최대값을 갱신한다.

이러한 접근 방식은 시간 복잡도가 \( O(NK) \)로, 제한 시간 내에 해결할 수 있다.

## C++ 코드와 설명

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

struct Student {
    int skill;                // 학생의 실력
    vector<int> algorithms;   // 학생이 알고 있는 알고리즘 목록
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, K;
    long long D;
    cin >> N >> K >> D;

    vector<Student> students(N);

    // 학생 정보 입력
    for (int i = 0; i < N; ++i) {
        int M;
        cin >> M >> students[i].skill;
        students[i].algorithms.resize(M);
        for (int j = 0; j < M; ++j) {
            cin >> students[i].algorithms[j];
            --students[i].algorithms[j]; // 알고리즘 번호를 0부터 시작하도록 조정
        }
    }

    // 학생들을 실력 기준으로 정렬
    sort(students.begin(), students.end(), [](const Student &a, const Student &b) {
        return a.skill < b.skill;
    });

    vector<int> algorithm_counts(K, 0); // 각 알고리즘을 알고 있는 학생 수
    int total_known = 0;                // 그룹에서 알고 있는 알고리즘의 총 수
    int total_known_by_all = 0;         // 그룹의 모든 학생이 알고 있는 알고리즘의 수
    int left = 0;                       // 슬라이딩 윈도우의 왼쪽 포인터
    int group_size = 0;                 // 현재 그룹의 크기
    long long max_E = 0;                // 최대 효율성

    // 오른쪽 포인터를 이동하며 슬라이딩 윈도우 확장
    for (int right = 0; right < N; ++right) {
        group_size++; // 그룹 크기 증가

        // 새로운 학생의 알고리즘 정보를 업데이트
        for (int alg : students[right].algorithms) {
            if (algorithm_counts[alg] == 0) {
                total_known++; // 새로운 알고리즘 발견
            }
            algorithm_counts[alg]++;
        }

        // 실력 차이가 D를 초과하면 왼쪽 포인터 이동하여 윈도우 축소
        while (students[right].skill - students[left].skill > D) {
            // 왼쪽 학생의 알고리즘 정보를 업데이트
            for (int alg : students[left].algorithms) {
                algorithm_counts[alg]--;
                if (algorithm_counts[alg] == 0) {
                    total_known--; // 알고리즘을 아는 학생이 더 이상 없음
                }
            }
            group_size--; // 그룹 크기 감소
            left++;
        }

        // total_known_by_all을 재계산
        total_known_by_all = 0;
        for (int alg = 0; alg < K; ++alg) {
            if (algorithm_counts[alg] == group_size) {
                total_known_by_all++; // 모든 학생이 알고 있는 알고리즘
            }
        }

        // 현재 그룹의 효율성 계산
        long long E = (total_known - total_known_by_all) * group_size;
        if (E > max_E) {
            max_E = E; // 최대 효율성 갱신
        }
    }

    cout << max_E << '\n'; // 결과 출력

    return 0;
}
```

### 코드 설명

- **학생 정보 입력 및 전처리**:
  - 각 학생의 알고리즘 목록을 입력받고, 알고리즘 번호를 0부터 시작하도록 조정한다.
  - 학생들을 실력 기준으로 정렬하여 슬라이딩 윈도우를 사용할 수 있도록 준비한다.

- **슬라이딩 윈도우를 사용한 그룹 탐색**:
  - 오른쪽 포인터 `right`를 이동하면서 그룹에 학생을 추가한다.
  - 새로운 학생의 알고리즘을 `algorithm_counts`에 반영하고, 새로운 알고리즘을 발견하면 `total_known`을 증가시킨다.
  - 실력 차이가 \( D \)를 초과하면 왼쪽 포인터 `left`를 이동하여 그룹에서 학생을 제거한다.
  - 그룹에서 제거된 학생의 알고리즘을 `algorithm_counts`에서 감소시키고, 알고리즘을 아는 학생이 없으면 `total_known`을 감소시킨다.

- **효율성 계산 및 최대값 갱신**:
  - `total_known_by_all`을 각 알고리즘에 대해 그룹의 모든 학생이 알고 있는지 확인하여 계산한다.
  - 현재 그룹의 효율성 \( E \)를 계산하고, 최대값을 갱신한다.

## 결론

이 문제는 슬라이딩 윈도우와 투 포인터 기법을 사용하여 효율적으로 해결할 수 있었다. 알고리즘의 수가 적다는 점을 이용하여 각 알고리즘의 카운트를 배열로 관리함으로써 시간 복잡도를 \( O(NK) \)로 줄일 수 있었다. 문제를 풀면서 슬라이딩 윈도우를 적용하는 방법과 카운트를 효율적으로 관리하는 방법에 대해 다시 한 번 생각해볼 수 있었다.

추가적으로, 알고리즘 번호를 0부터 시작하도록 조정하여 배열 인덱싱을 간단하게 만들었다. 이러한 작은 최적화가 전체 코드의 가독성과 효율성을 높이는 데 도움이 된다.

이번 문제를 통해 투 포인터와 슬라이딩 윈도우 기법이 다양한 상황에서 활용될 수 있음을 알게 되었으며, 앞으로도 이러한 기법을 적절히 활용하여 문제를 효율적으로 해결할 수 있도록 노력해야겠다.