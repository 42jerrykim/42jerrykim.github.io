---
image: "tmp_wordcloud.png"
categories: Algorithm
date: "2024-09-25T00:00:00Z"

header:
  teaser: /assets/images/undefined/algorithm.png
tags:
- Trie
- Recursion
- StringProcessing
- Optimization
- O(N)
title: '[Algorithm] C++/Python 백준 5670번 : 휴대폰 자판'
---

휴대폰에서 영단어를 입력할 때 버튼을 누르는 횟수를 최소화하기 위해 자동완성 기능을 활용하는 문제이다. 이 문제는 Trie(트라이) 자료 구조 또는 재귀적인 접근 방식을 사용하여 효율적으로 해결할 수 있다.

문제 : [https://www.acmicpc.net/problem/5670](https://www.acmicpc.net/problem/5670)

|![](/assets/images/undefined/algorithm.png)|
|:---:|
||

## 문제 설명

휴대폰에서 길이가 $P$인 영단어를 입력하려면 일반적으로 버튼을 $P$번 눌러야 한다. 그러나 입력 속도를 높이기 위해, 사전에 기반한 자동완성 기능을 사용하는 자판 모듈이 있다. 이 모듈은 다음과 같은 규칙으로 동작한다.

1. **첫 글자는 자동완성되지 않는다.** 사용자는 첫 번째 글자를 반드시 직접 입력해야 한다.
2. **자동입력 조건:** 현재까지 입력된 문자열 $c_1c_2...c_n$이 있을 때, 사전에서 이 문자열로 시작하는 단어들이 모두 다음 글자 $c$를 공유한다면, 모듈은 $c$를 자동으로 입력해준다.

예를 들어, 사전에 "hello", "hell", "heaven", "goodbye"가 있을 때, 사용자가 'h'를 입력하면 모듈은 자동으로 'e'를 입력해준다. 이는 'h'로 시작하는 모든 단어의 다음 글자가 'e'이기 때문이다. 그러나 'he' 다음에는 'l'과 'a'가 올 수 있으므로, 모듈은 다음 입력을 기다린다.

사용자가 'l'을 입력하면, 모듈은 다시 'l'을 자동으로 입력해준다. 여기서 "hell"이 단어의 끝이지만, "hello"는 아직 끝나지 않았으므로, 모듈은 다시 입력을 기다린다. 이처럼 자동완성 기능을 사용하여 각 단어를 입력할 때 버튼을 눌러야 하는 횟수를 계산하고, 그 평균을 구하는 문제이다.

문제에서 입력은 여러 개의 테스트 케이스로 이루어져 있다. 각 테스트 케이스는 사전에 속한 단어의 개수 $N$이 주어지며, 이어서 $N$개의 단어가 주어진다. 각 단어를 입력하기 위해 버튼을 눌러야 하는 횟수의 평균을 소수점 둘째 자리까지 반올림하여 출력해야 한다.

## 접근 방식

이 문제는 Trie 자료 구조를 사용하여 효율적으로 해결할 수 있다. 그러나 파이썬에서는 메모리 제한으로 인해 Trie를 명시적으로 구축하는 것이 비효율적일 수 있다. 따라서 **재귀적인 분할 정복 방법**을 사용하여 메모리 사용량을 줄이면서도 효율적으로 문제를 해결할 수 있다.

**알고리즘 전략:**

1. **단어 그룹화:**
   - 단어들을 현재 위치의 문자에 따라 그룹화한다.
   - 동일한 위치에서 동일한 문자를 가진 단어들을 함께 묶는다.

2. **재귀 처리:**
   - 각 그룹에 대해 공통된 접두사를 최대한 확장한다.
   - 단어들이 갈라지는 지점에서 버튼을 눌러야 하므로 깊이를 증가시킨다.
   - 단어의 끝에 도달하면 현재까지의 버튼 입력 횟수를 저장한다.
   - 남은 단어들에 대해 재귀적으로 동일한 과정을 반복한다.

3. **버튼 입력 횟수 계산:**
   - 각 단어별로 필요한 버튼 입력 횟수를 계산하여 배열에 저장한다.

4. **평균 계산:**
   - 모든 단어의 버튼 입력 횟수의 합을 단어의 수로 나누어 평균을 구한다.
   - 소수점 둘째 자리까지 반올림하여 출력한다.

이 방법은 Trie를 명시적으로 구축하지 않고도 동일한 효과를 낼 수 있으며, 메모리 사용량을 크게 줄일 수 있다.

## C++ 코드와 설명

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <cstring>
#include <iomanip>
#include <cstdio>

using namespace std;

// Trie의 노드를 나타내는 구조체
struct TrieNode {
    bool is_end;               // 이 노드가 단어의 끝인지 표시
    int child_count;           // 자식 노드의 수
    TrieNode* children[26];    // 알파벳 소문자에 대한 자식 노드 포인터 배열

    // 생성자: 초기화
    TrieNode() {
        is_end = false;
        child_count = 0;
        memset(children, 0, sizeof(children));
    }
};

// 단어를 Trie에 삽입하는 함수
void insert(TrieNode* root, const string& word) {
    TrieNode* node = root;
    for (char c : word) {
        int idx = c - 'a';  // 알파벳을 인덱스로 변환
        if (!node->children[idx]) {
            node->children[idx] = new TrieNode();  // 자식 노드가 없으면 생성
            node->child_count++;                   // 자식 수 증가
        }
        node = node->children[idx];  // 다음 노드로 이동
    }
    node->is_end = true;  // 단어의 끝 표시
}

// 단어를 입력하는 데 필요한 버튼 횟수를 계산하는 함수
int count_key_presses(TrieNode* root, const string& word) {
    int key_presses = 1;  // 첫 번째 문자는 항상 입력해야 함
    TrieNode* node = root->children[word[0] - 'a'];  // 첫 번째 문자로 이동
    for (size_t i = 1; i < word.length(); ++i) {
        int idx = word[i] - 'a';
        // 현재 노드가 단어의 끝이거나 자식이 둘 이상이면 버튼 입력 필요
        if (node->is_end || node->child_count > 1) {
            key_presses++;
        }
        node = node->children[idx];  // 다음 노드로 이동
    }
    return key_presses;
}

// Trie를 동적 할당 해제하는 함수
void delete_trie(TrieNode* node) {
    if (!node) return;
    for (int i = 0; i < 26; ++i) {
        if (node->children[i]) {
            delete_trie(node->children[i]);  // 자식 노드들을 재귀적으로 삭제
        }
    }
    delete node;  // 현재 노드 삭제
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    while (cin >> N) {
        vector<string> words(N);
        for (int i = 0; i < N; ++i) {
            cin >> words[i];  // 단어 입력
        }

        TrieNode* root = new TrieNode();  // Trie의 루트 노드 생성

        for (const string& word : words) {
            insert(root, word);  // 단어들을 Trie에 삽입
        }

        int total_presses = 0;
        for (const string& word : words) {
            total_presses += count_key_presses(root, word);  // 각 단어의 버튼 입력 횟수 계산
        }

        double average_presses = (double)total_presses / N + 1e-8;  // 평균 계산 및 부동소수점 보정
        printf("%.2f\n", average_presses);  // 소수점 둘째 자리까지 출력

        delete_trie(root);  // Trie 메모리 해제
    }

    return 0;
}
```

**코드 설명:**

- **TrieNode 구조체:**
  - `is_end`: 해당 노드가 단어의 끝인지 표시한다.
  - `child_count`: 현재 노드의 자식 노드 개수를 저장한다.
  - `children[26]`: 알파벳 소문자에 해당하는 자식 노드 포인터 배열이다.

- **insert 함수:**
  - 단어를 Trie에 삽입하면서, 새로운 노드를 생성할 때마다 `child_count`를 증가시킨다.
  - 이는 각 노드에서 자식 노드의 수를 파악하여 버튼 입력 필요 여부를 결정하기 위함이다.

- **count_key_presses 함수:**
  - 각 단어에 대해 버튼 입력 횟수를 계산한다.
  - 첫 번째 문자는 항상 입력해야 하므로 `key_presses`를 1로 시작한다.
  - 이후 각 문자에서 현재 노드가 단어의 끝(`is_end == true`)이거나 자식 노드가 둘 이상(`child_count > 1`)이면 버튼 입력이 필요하므로 `key_presses`를 증가시킨다.

- **delete_trie 함수:**
  - 동적으로 할당된 Trie 노드를 재귀적으로 삭제하여 메모리 누수를 방지한다.

- **메인 함수:**
  - 테스트 케이스마다 단어를 입력받고 Trie를 구축한다.
  - 각 단어에 대한 버튼 입력 횟수를 계산하여 총합을 구하고, 평균을 계산한다.
  - `printf`를 사용하여 소수점 둘째 자리까지 출력한다.

## C++ without library 코드와 설명

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Trie의 노드를 나타내는 구조체
typedef struct TrieNode {
    int is_end;                // 이 노드가 단어의 끝인지 표시
    int child_count;           // 자식 노드의 수
    struct TrieNode* children[26];  // 알파벳 소문자에 대한 자식 노드 포인터 배열
} TrieNode;

// Trie 노드 생성 함수
TrieNode* create_node() {
    TrieNode* node = (TrieNode*)malloc(sizeof(TrieNode));
    node->is_end = 0;
    node->child_count = 0;
    memset(node->children, 0, sizeof(node->children));
    return node;
}

// 단어를 Trie에 삽입하는 함수
void insert(TrieNode* root, char* word) {
    TrieNode* node = root;
    for (int i = 0; word[i]; ++i) {
        int idx = word[i] - 'a';
        if (!node->children[idx]) {
            node->children[idx] = create_node();  // 자식 노드가 없으면 생성
            node->child_count++;                  // 자식 수 증가
        }
        node = node->children[idx];  // 다음 노드로 이동
    }
    node->is_end = 1;  // 단어의 끝 표시
}

// 단어를 입력하는 데 필요한 버튼 횟수를 계산하는 함수
int count_key_presses(TrieNode* root, char* word) {
    int key_presses = 1;  // 첫 번째 문자는 항상 입력해야 함
    TrieNode* node = root->children[word[0] - 'a'];  // 첫 번째 문자로 이동
    for (int i = 1; word[i]; ++i) {
        int idx = word[i] - 'a';
        // 현재 노드가 단어의 끝이거나 자식이 둘 이상이면 버튼 입력 필요
        if (node->is_end || node->child_count > 1) {
            key_presses++;
        }
        node = node->children[idx];  // 다음 노드로 이동
    }
    return key_presses;
}

// Trie를 동적 할당 해제하는 함수
void delete_trie(TrieNode* node) {
    if (!node) return;
    for (int i = 0; i < 26; ++i) {
        if (node->children[i]) {
            delete_trie(node->children[i]);  // 자식 노드들을 재귀적으로 삭제
        }
    }
    free(node);  // 현재 노드 삭제
}

int main() {
    int N;
    while (scanf("%d", &N) != EOF) {
        char words[N][81];
        for (int i = 0; i < N; ++i) {
            scanf("%s", words[i]);  // 단어 입력
        }

        TrieNode* root = create_node();  // Trie의 루트 노드 생성

        for (int i = 0; i < N; ++i) {
            insert(root, words[i]);  // 단어들을 Trie에 삽입
        }

        int total_presses = 0;
        for (int i = 0; i < N; ++i) {
            total_presses += count_key_presses(root, words[i]);  // 각 단어의 버튼 입력 횟수 계산
        }

        double average_presses = (double)total_presses / N + 1e-8;  // 평균 계산 및 부동소수점 보정
        printf("%.2f\n", average_presses);  // 소수점 둘째 자리까지 출력

        delete_trie(root);  // Trie 메모리 해제
    }

    return 0;
}
```

**코드 설명:**

- C 표준 라이브러리만을 사용하여 Trie를 구현하였다.
- `TrieNode` 구조체와 관련된 함수들은 위의 C++ 코드와 동일한 로직을 따른다.
- `malloc`과 `free`를 사용하여 동적 메모리를 관리한다.
- 입력과 출력은 `scanf`와 `printf`를 사용하여 처리한다.
- 문자열 배열 `words`는 최대 길이 80으로 선언하였다.


## Python 코드와 설명

```python
import sys
input = sys.stdin
print = sys.stdout.write

import decimal
ctx = decimal.getcontext()
ctx.rounding = decimal.ROUND_HALF_UP

def solve(N, words):
    depths = [0] * N  # 각 단어의 버튼 입력 횟수를 저장할 리스트

    def init(indices, i, depth):
        # indices: 현재 처리 중인 단어들의 인덱스 리스트
        # i: 현재 검사할 문자 위치 (0부터 시작)
        # depth: 현재까지 버튼을 누른 횟수
        wordbook = dict()
        for idx in indices:
            if len(words[idx]) == i:
                depths[idx] = depth  # 단어의 끝에 도달하면 깊이 저장
                continue
            c = words[idx][i]
            if c in wordbook:
                wordbook[c].append(idx)
            else:
                wordbook[c] = [idx]

        for c, subindices in wordbook.items():
            # 공통된 문자를 최대한 건너뛰기 위해 j를 사용
            j = i + 1
            while True:
                # 단어의 길이를 넘어가면 중지
                if any(len(words[idx]) == j for idx in subindices):
                    break
                # 다음 문자가 모두 같은지 확인
                target = words[subindices[0]][j]
                if any(words[idx][j] != target for idx in subindices):
                    break
                j += 1

            # 끝에 도달한 단어는 깊이 저장
            subsub = []
            for idx in subindices:
                if len(words[idx]) == j:
                    depths[idx] = depth + 1
                else:
                    subsub.append(idx)

            # 남은 단어들에 대해 재귀적으로 처리
            if subsub:
                init(subsub, j, depth + 1)

    init(range(N), 0, 0)

    # 평균 버튼 입력 횟수 계산
    return round(decimal.Decimal(sum(depths) / N), 2)

while True:
    try:
        N = int(input.readline().strip())
        words = [input.readline().strip() for _ in range(N)]
        ans = solve(N, words)
        print(f"{ans}\n")
    except:
        break
```

**코드 설명:**

- **입력 처리:**
  - `input.readline()`을 사용하여 한 줄씩 입력을 받는다.
  - 입력이 없으면 예외가 발생하여 `break`를 통해 반복문을 종료한다.

- **`solve` 함수:**
  - 각 단어의 버튼 입력 횟수를 계산하여 `depths` 리스트에 저장한다.

- **`init` 함수:**
  - `indices`: 현재 처리할 단어들의 인덱스 리스트.
  - `i`: 현재 검사할 문자 위치.
  - `depth`: 현재까지 버튼을 누른 횟수.
  - 동일한 위치 `i`에서 동일한 문자를 가진 단어들을 그룹화하여 `wordbook` 딕셔너리에 저장한다.
  - 각 그룹에 대해 최대한 공통된 접두사를 찾아내어 한 번에 건너뛴다.
  - 단어의 끝에 도달하면 `depths`에 버튼 입력 횟수를 저장한다.
  - 남은 단어들에 대해 재귀적으로 `init` 함수를 호출한다.

- **버튼 입력 횟수 계산 로직:**
  - 단어들이 갈라지는 지점에서 버튼을 눌러야 하므로, 깊이(`depth`)를 증가시킨다.
  - 공통된 문자가 이어지는 동안은 자동완성이 이루어지므로 버튼을 누를 필요가 없다.

- **평균 계산 및 출력:**
  - `depths` 리스트의 합을 단어의 수 `N`으로 나누어 평균을 계산한다.
  - `decimal` 모듈을 사용하여 소수점 둘째 자리까지 반올림한다.

**왜 이 코드가 효율적인가?**

- **메모리 효율성:** Trie를 명시적으로 구축하지 않고, 재귀적으로 단어를 처리하므로 메모리 사용량을 줄일 수 있다.
- **시간 효율성:** 각 단어를 최대 한 번씩만 처리하므로 시간 복잡도는 $O(NL)$이며, 여기서 $N$은 단어의 수, $L$은 단어의 평균 길이이다.

## 결론

이 문제는 Trie 자료 구조를 활용하여 해결할 수 있지만, 파이썬에서는 메모리 제한으로 인해 재귀적인 분할 정복 방법을 사용하여 메모리 초과 문제를 해결할 수 있었다. 재귀적인 접근 방식은 Trie를 명시적으로 생성하지 않고도 동일한 효과를 낼 수 있으며, 메모리 사용량을 크게 줄일 수 있다.

문제를 해결하면서 자료 구조와 알고리즘의 선택이 메모리와 시간 복잡도에 큰 영향을 미친다는 것을 다시 한 번 깨달았다. 상황에 따라 적절한 방법을 선택하는 것이 중요하며, 특히 제한 사항을 고려한 최적화가 필요하다.

앞으로도 다양한 접근 방식을 고려하여 문제를 해결하는 능력을 키워야겠다.