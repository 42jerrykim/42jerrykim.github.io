---
title: "[Algorithm] C++/Python 백준 19585번 : 전설"
description: "이 문제는 주어진 색상 이름과 닉네임 목록을 활용해, 팀 이름이 '색상 이름+닉네임' 형태인지 효율적으로 판별하는 자료구조 활용 문제입니다. Trie 두 개를 통해 접두사/접미사 매칭을 빠르게 수행합니다."
categories: 
- Algorithm
- DataStructures
- Trie
- Hash
tags:
- Trie
- StringProcessing
- HashTable
- Hash
- HashMap
- HashSet
- String
- StringMatching
- DataStructures
- EfficientAlgorithms
image: "tmp_wordcloud.png"
date: 2024-10-21
---

알고리즘 문제를 풀다 보면 다양한 자료 구조와 알고리즘을 접하게 된다. 오늘은 백준 온라인 저지의 19585번 문제인 **전설**을 풀어보면서 Trie 자료 구조와 문자열 처리에 대해 알아보겠다.

문제 : [https://www.acmicpc.net/problem/19585](https://www.acmicpc.net/problem/19585)

## 문제 설명

서강대학교 ICPC 팀에는 팀 이름을 **색상 이름**과 **닉네임**의 순서로 지으면 대회에서 수상할 수 있다는 전설이 있다. 예를 들어, "redshift"나 "bluejoker" 같은 이름이다. 색상 이름의 목록과 닉네임의 목록이 주어졌을 때, 주어진 팀 이름들이 다음 대회에서 수상할 수 있을지, 즉 팀 이름이 색상 이름과 닉네임의 조합으로 이루어져 있는지를 판단해야 한다.

- **입력**:
  - 색상 이름의 개수 `C`와 닉네임의 개수 `N`이 주어진다. (1 ≤ C, N ≤ 4,000)
  - 다음 `C`개의 줄에는 중복되지 않는 색상 이름들이 주어진다.
  - 다음 `N`개의 줄에는 중복되지 않는 닉네임들이 주어진다.
  - 그 다음 팀 이름의 개수 `Q`가 주어진다. (1 ≤ Q ≤ 20,000)
  - 다음 `Q`개의 줄에는 팀 이름들이 주어진다.
  - 모든 이름들은 알파벳 소문자로만 이루어져 있으며, 각 이름의 길이는 1,000자를 넘지 않는다.

- **출력**:
  - 각 팀 이름에 대해 해당 팀이 전설에 따라 수상할 수 있다면 "Yes", 그렇지 않다면 "No"를 출력한다.

## 접근 방식

이 문제는 주어진 팀 이름이 색상 이름과 닉네임의 조합으로 이루어져 있는지를 빠르게 판단해야 한다. 문자열의 길이가 최대 2,000자이고, 팀 이름의 개수가 최대 20,000개이므로, 단순한 방법으로는 시간 초과가 발생한다.

효율적인 문자열 검색을 위해 **Trie** 자료 구조를 사용한다. 색상 이름들과 닉네임들을 각각 Trie로 구성하여 팀 이름의 접두사와 접미사가 각각 색상 이름과 닉네임에 매칭되는지를 확인한다.

- **색상 Trie**: 색상 이름들을 저장하는 Trie로, 팀 이름의 앞부분(접두사)을 검사한다.
- **닉네임 Trie**: 닉네임들을 저장하는 Trie로, 팀 이름의 뒷부분(접미사)을 검사한다. 이때, 접미사를 효율적으로 검사하기 위해 닉네임을 **역순으로 저장**하여 팀 이름의 뒷부분부터 Trie를 탐색한다.

팀 이름에 대해 다음을 수행한다:

1. 팀 이름의 각 위치에서 **접두사**가 색상 Trie에 존재하는지 확인하고, 해당 위치를 기록한다.
2. 팀 이름의 끝에서부터 **접미사**가 닉네임 Trie에 존재하는지 확인하고, 접두사 검사 결과와 비교한다.
3. 만약 어떤 위치에서 접두사와 접미사가 각각 색상 이름과 닉네임에 매칭된다면 "Yes"를 출력한다.

이를 통해 모든 팀 이름에 대해 효율적으로 판단할 수 있다.

## C++ 코드와 설명

```cpp
#include <iostream>
#include <cstring>
#include <bitset>
using namespace std;

const int MAXN = 8000000; // Trie의 최대 노드 수
int trie[MAXN][26];       // 알파벳 소문자에 대한 Trie
bool is_color_end[MAXN];  // 색상 이름의 종료 지점 표시
bool is_nick_end[MAXN];   // 닉네임의 종료 지점 표시
int node_count = 1;       // Trie의 노드 개수

// 색상 이름을 Trie에 삽입
void insert_color(const char* str) {
    int len = strlen(str);
    int node = 0;
    for (int i = 0; i < len; ++i) {
        int c = str[i] - 'a';
        if (!trie[node][c])
            trie[node][c] = node_count++;
        node = trie[node][c];
    }
    is_color_end[node] = true;
}

// 닉네임을 역순으로 Trie에 삽입
void insert_nick(const char* str) {
    int len = strlen(str);
    int node = 0;
    for (int i = len - 1; i >= 0; --i) {
        int c = str[i] - 'a';
        if (!trie[node][c])
            trie[node][c] = node_count++;
        node = trie[node][c];
    }
    is_nick_end[node] = true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int C, N;
    cin >> C >> N;

    char word[2001];
    // 색상 이름 입력 및 Trie 구성
    for (int i = 0; i < C; ++i) {
        cin >> word;
        insert_color(word);
    }

    // 닉네임 입력 및 Trie 구성
    for (int i = 0; i < N; ++i) {
        cin >> word;
        insert_nick(word);
    }

    int Q;
    cin >> Q;

    while (Q--) {
        cin >> word;
        int len = strlen(word);

        bitset<2000> color_match; // 색상 이름과 매칭되는 접두사의 위치 기록
        int node = 0;
        // 접두사 검사
        for (int i = 0; i < len; ++i) {
            int c = word[i] - 'a';
            if (!trie[node][c])
                break;
            node = trie[node][c];
            if (is_color_end[node])
                color_match.set(i);
        }

        bool found = false;
        node = 0;
        // 접미사 검사
        for (int i = len - 1; i >= 1; --i) {
            int c = word[i] - 'a';
            if (!trie[node][c])
                break;
            node = trie[node][c];
            if (is_nick_end[node] && color_match.test(i - 1)) {
                found = true;
                break;
            }
        }

        cout << (found ? "Yes\n" : "No\n");
    }

    return 0;
}
```

### 코드 설명

- **Trie 구현**: 이중 배열 `trie`를 사용하여 Trie를 구현한다. `trie[node][c]`는 현재 `node`에서 문자 `c`로 이동하는 간선을 나타낸다.
- **색상 이름 삽입**:
  - `insert_color` 함수에서 색상 이름을 Trie에 삽입한다.
  - 각 문자를 따라가며 노드를 생성하고, 끝나는 지점에 `is_color_end`를 `true`로 설정한다.
- **닉네임 삽입**:
  - `insert_nick` 함수에서 닉네임을 **역순**으로 Trie에 삽입한다.
  - 닉네임을 뒤에서부터 읽어들이며 Trie를 구성하고, 끝나는 지점에 `is_nick_end`를 `true`로 설정한다.
- **팀 이름 검사**:
  - 팀 이름의 접두사를 검사하여 색상 이름과 매칭되는 위치를 `bitset`에 기록한다.
  - 팀 이름의 끝에서부터 접미사를 검사하여 닉네임과 매칭되는지 확인한다.
  - 접두사와 접미사가 동시에 매칭되는 위치가 있으면 "Yes"를 출력한다.

## C++ without library 코드와 설명

```cpp
#include <stdio.h>
#include <string.h>

#define MAXN 8000000

int trie[MAXN][26];
char is_color_end[MAXN];
char is_nick_end[MAXN];
int node_count = 1;

void insert_color(char* str) {
    int len = strlen(str);
    int node = 0;
    for (int i = 0; i < len; ++i) {
        int c = str[i] - 'a';
        if (!trie[node][c])
            trie[node][c] = node_count++;
        node = trie[node][c];
    }
    is_color_end[node] = 1;
}

void insert_nick(char* str) {
    int len = strlen(str);
    int node = 0;
    for (int i = len - 1; i >= 0; --i) {
        int c = str[i] - 'a';
        if (!trie[node][c])
            trie[node][c] = node_count++;
        node = trie[node][c];
    }
    is_nick_end[node] = 1;
}

char word[2001];
char color_match[2000];

int main() {
    int C, N;
    scanf("%d %d", &C, &N);

    for (int i = 0; i < C; ++i) {
        scanf("%s", word);
        insert_color(word);
    }

    for (int i = 0; i < N; ++i) {
        scanf("%s", word);
        insert_nick(word);
    }

    int Q;
    scanf("%d", &Q);

    while (Q--) {
        scanf("%s", word);
        int len = strlen(word);
        memset(color_match, 0, len);

        int node = 0;
        // 접두사 검사
        for (int i = 0; i < len; ++i) {
            int c = word[i] - 'a';
            if (!trie[node][c])
                break;
            node = trie[node][c];
            if (is_color_end[node])
                color_match[i] = 1;
        }

        int found = 0;
        node = 0;
        // 접미사 검사
        for (int i = len - 1; i >= 1; --i) {
            int c = word[i] - 'a';
            if (!trie[node][c])
                break;
            node = trie[node][c];
            if (is_nick_end[node] && color_match[i - 1]) {
                found = 1;
                break;
            }
        }

        printf(found ? "Yes\n" : "No\n");
    }

    return 0;
}
```

### 코드 설명

- 표준 라이브러리만 사용하여 구현하였다.
- `char` 배열과 `int`를 사용하여 메모리를 절약하였다.
- `bitset` 대신 `char` 배열 `color_match`를 사용하여 접두사 매칭 결과를 저장한다.
- 나머지 로직은 앞서 설명한 코드와 동일하다.

## Python 코드와 설명

```python
import sys

def main():
    input_data = sys.stdin.read().split()
    index = 0
    C = int(input_data[index])
    index += 1
    N = int(input_data[index])
    index += 1

    color_trie = [{}]
    is_color_end = [False]

    nick_trie = [{}]
    is_nick_end = [False]

    def insert(trie, is_end, word, reverse=False):
        node = 0
        iterable = reversed(word) if reverse else word
        for c in iterable:
            if c not in trie[node]:
                trie.append({})
                is_end.append(False)
                trie[node][c] = len(trie) - 1
            node = trie[node][c]
        is_end[node] = True

    # 색상 이름 입력 및 Trie 구성
    for _ in range(C):
        word = input_data[index]
        index += 1
        insert(color_trie, is_color_end, word)

    # 닉네임 입력 및 Trie 구성
    for _ in range(N):
        word = input_data[index]
        index += 1
        insert(nick_trie, is_nick_end, word, reverse=True)

    Q = int(input_data[index])
    index += 1

    for _ in range(Q):
        word = input_data[index]
        index += 1
        len_word = len(word)
        color_match = [False] * len_word
        node = 0

        # 접두사 검사 (색상 이름)
        for i, c in enumerate(word):
            if c not in color_trie[node]:
                break
            node = color_trie[node][c]
            if is_color_end[node]:
                color_match[i] = True

        # 접미사 검사 (닉네임)
        found = False
        node = 0
        for i in range(len_word - 1, 0, -1):
            c = word[i]
            if c not in nick_trie[node]:
                break
            node = nick_trie[node][c]
            if is_nick_end[node] and color_match[i - 1]:
                found = True
                break

        print("Yes" if found else "No")

if __name__ == "__main__":
    main()
```

### 코드 설명

- **입력 처리 개선**:
  - `sys.stdin.read().split()`을 사용하여 모든 입력을 한 번에 읽어와서 처리한다. 이는 입력이 많은 경우에도 효율적으로 처리할 수 있다.
  - `index` 변수를 사용하여 입력 데이터를 순서대로 접근한다.

- **Trie 구현**:
  - 리스트와 딕셔너리를 사용하여 Trie를 구현한다.
  - 각 노드는 딕셔너리로, 문자를 키로 하여 다음 노드의 인덱스를 저장한다.

- **`insert` 함수**:
  - 단어를 Trie에 삽입하는 함수이다.
  - `reverse=True`인 경우 단어를 역순으로 삽입하여 접미사 검색에 활용한다.

- **팀 이름 검사 로직**:
  - **접두사 검사**:
    - 팀 이름의 앞부분부터 색상 이름 Trie를 탐색한다.
    - 각 위치에서 색상 이름이 종료되는 지점을 `color_match` 리스트에 기록한다.
  - **접미사 검사**:
    - 팀 이름의 뒷부분부터 닉네임 Trie를 탐색한다.
    - 닉네임이 종료되는 지점에서 앞서 기록한 `color_match`를 확인하여 색상 이름과 닉네임이 이어지는지 판단한다.

- **출력**:
  - 조건을 만족하면 "Yes"를, 그렇지 않으면 "No"를 출력한다.

### 추가 설명

- **Trie 자료 구조**:
  - 각 Trie는 리스트로 구현되며, 각 노드는 딕셔너리 형태로 자식 노드를 가진다.
  - 새로운 문자를 만나면 Trie에 노드를 추가하고, 해당 노드의 인덱스를 저장한다.

- **시간 및 메모리 효율성**:
  - 입력을 한 번에 읽어와 처리함으로써 입출력 시간을 단축하였다.
  - Trie를 효율적으로 사용하여 시간 복잡도를 줄였다.

## 결론

이 문제에서는 Trie 자료 구조를 활용하여 문자열 매칭 문제를 효율적으로 해결하였다. Trie를 두 개 사용하여 접두사와 접미사를 각각 검사함으로써 시간 복잡도를 효과적으로 줄일 수 있었다. 또한, 메모리 사용을 최적화하고 빠른 입출력을 위해 다양한 기법을 적용하였다.

이번 문제를 통해 문자열 처리와 Trie의 강력함을 다시 한 번 느낄 수 있었다. 실제 대회나 코딩 테스트에서 유용하게 활용될 수 있는 알고리즘이므로, 다양한 문제에 적용해보는 연습이 필요할 것이다.