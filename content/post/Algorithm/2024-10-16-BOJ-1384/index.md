---
title: "[Algorithm] C++/Python 백준 1384번 : 메시지"
categories: Algorithm
tags:
- Implementation
- Simulation
- String Manipulation
- Brute Force
- Data Structures
- O(N^2)
date: 2024-10-16
image: "tmp_wordcloud.png"
---

알고리즘 문제를 풀다 보면 구현 능력이 중요한 경우가 많다. 오늘은 백준 온라인 저지의 1384번 문제인 "메시지"를 풀어보면서 구현력과 시뮬레이션 능력을 향상시켜보자.

문제 : [https://www.acmicpc.net/problem/1384](https://www.acmicpc.net/problem/1384)

## 문제 설명

여러 명의 아이들이 원형으로 앉아 종이 위에 자신의 이름을 적는 활동을 하고 있다. 이들은 종이를 왼쪽으로 전달하며, 종이를 받으면 맨 위에 적힌 이름의 아이에게 메시지를 적는다. 메시지는 좋은 말일 수도 있고 나쁜 말일 수도 있다. 각 메시지를 적은 후에는 종이를 접어 이전에 적힌 내용을 가린다. 이렇게 종이를 전달하다가 자신의 이름이 적힌 종이를 받으면 활동이 종료되고, 종이에 적힌 메시지들을 읽어본다.

하지만 가끔 아이들 중 일부는 "넌 너무 말이 많아.", "니 옷이 별로야."와 같은 나쁜 메시지를 남기기도 한다. 이런 경우 해당 메시지를 읽은 아이는 기분이 나빠질 수 있다. 우리의 목표는 누가 누구에게 나쁜 말을 했는지 알아내는 것이다.

입력은 여러 그룹의 데이터로 이루어져 있다. 각 그룹은 참여한 아이들의 수 \( n \) (5 ≤ \( n \) ≤ 20)로 시작하며, 다음 \( n \) 줄에는 각 아이의 이름과 그 아이가 받은 종이에 적힌 메시지들이 순서대로 주어진다. 메시지는 'P'로 표시된 좋은 말과 'N'으로 표시된 나쁜 말로 구성된다. 각 그룹의 데이터를 처리하여 나쁜 말을 한 아이와 그 대상이 된 아이를 찾아내야 한다.

## 접근 방식

이 문제는 시뮬레이션과 구현 능력이 요구된다. 아이들이 원형으로 앉아 있고, 종이를 왼쪽으로 전달하며 메시지를 적는 과정을 그대로 구현해야 한다.

1. **데이터 구조화**: 아이들의 이름과 메시지를 저장할 적절한 데이터 구조를 설계한다.
2. **원형 구조 구현**: 원형으로 앉은 아이들의 좌석 배치를 고려하여 인덱스를 처리한다. 좌석 번호는 리스트의 인덱스로 표현할 수 있다.
3. **메시지 작성자 추적**: 각 메시지가 누구에 의해 작성되었는지 추적해야 한다. 메시지는 종이를 받은 아이의 오른쪽에 앉은 아이가 작성한다.
4. **나쁜 메시지 식별**: 메시지 목록에서 'N'을 찾아 해당 메시지를 작성한 아이와 받은 아이를 기록한다.
5. **출력 형식 맞추기**: 요구된 출력 형식에 맞게 결과를 출력한다.

## C++ 코드와 설명

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <sstream>

using namespace std;

int main() {
    int groupNumber = 1; // 그룹 번호 초기화

    while (true) {
        int n;
        cin >> n; // 아이들의 수 입력
        if (n == 0) break; // 입력이 0이면 종료
        cin.ignore(); // 남은 개행 문자 제거

        vector<string> names(n); // 아이들의 이름 저장
        vector<vector<char>> messages(n); // 각 아이가 받은 메시지 저장

        // 아이들의 이름과 메시지 입력 받기
        for (int i = 0; i < n; ++i) {
            string line;
            getline(cin, line); // 한 줄 입력
            stringstream ss(line);
            ss >> names[i]; // 이름 추출

            char msg;
            while (ss >> msg) {
                messages[i].push_back(msg); // 메시지 저장
            }
        }

        vector<pair<string, string>> nastyMessages; // 나쁜 메시지를 저장할 벡터

        // 메시지 분석
        for (int i = 0; i < n; ++i) {
            int owner = i; // 종이의 주인
            int messageCount = messages[i].size();

            for (int j = 0; j < messageCount; ++j) {
                // 메시지를 작성한 아이의 인덱스 계산
                int writer = (owner - j - 1 + n) % n;
                if (messages[i][j] == 'N') {
                    // 나쁜 메시지라면 저장
                    nastyMessages.push_back({names[writer], names[owner]});
                }
            }
        }

        // 출력
        cout << "Group " << groupNumber << endl;
        if (nastyMessages.empty()) {
            cout << "Nobody was nasty" << endl;
        } else {
            for (auto &p : nastyMessages) {
                cout << p.first << " was nasty about " << p.second << endl;
            }
        }
        cout << endl; // 그룹 간 공백
        groupNumber++; // 그룹 번호 증가
    }

    return 0;
}
```

### 코드 설명

- **입력 처리**:
  - 각 그룹별로 아이들의 수 \( n \)을 입력받는다.
  - 아이들의 이름과 메시지를 저장하기 위해 `names`와 `messages` 벡터를 사용한다.
  - 한 줄씩 입력받아 이름과 메시지를 분리하여 저장한다.
  
- **메시지 분석**:
  - 각 종이에 적힌 메시지를 순회하면서 누가 메시지를 작성했는지 계산한다.
  - 메시지를 작성한 아이의 인덱스는 `(owner - j - 1 + n) % n`으로 계산한다.
  - 메시지가 'N'이라면 `nastyMessages` 벡터에 작성자와 대상자를 저장한다.
  
- **출력**:
  - 그룹 번호와 함께 나쁜 말을 한 아이와 대상자를 출력한다.
  - 나쁜 메시지가 없다면 "Nobody was nasty"를 출력한다.

## C++ without library 코드와 설명

```cpp
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_N 20
#define MAX_NAME_LEN 61
#define MAX_MSG_LEN 25

int main() {
    int groupNumber = 1;
    while (1) {
        int n;
        scanf("%d", &n);
        if (n == 0) break;
        getchar(); // 개행 문자 제거

        char names[MAX_N][MAX_NAME_LEN];
        char messages[MAX_N][MAX_MSG_LEN];
        int msgLengths[MAX_N];

        for (int i = 0; i < n; ++i) {
            char line[256];
            fgets(line, sizeof(line), stdin);
            int len = strlen(line);
            if (line[len - 1] == '\n') line[len - 1] = '\0'; // 개행 문자 제거

            char *token = strtok(line, " ");
            strcpy(names[i], token);

            int idx = 0;
            while ((token = strtok(NULL, " ")) != NULL) {
                messages[i][idx++] = token[0];
            }
            msgLengths[i] = idx;
        }

        printf("Group %d\n", groupNumber);
        int nastyFound = 0;

        for (int i = 0; i < n; ++i) {
            int owner = i;
            for (int j = 0; j < msgLengths[i]; ++j) {
                int writer = (owner - j - 1 + n) % n;
                if (messages[i][j] == 'N') {
                    printf("%s was nasty about %s\n", names[writer], names[owner]);
                    nastyFound = 1;
                }
            }
        }

        if (!nastyFound) {
            printf("Nobody was nasty\n");
        }
        printf("\n");
        groupNumber++;
    }
    return 0;
}
```

### 코드 설명

- **입력 처리**:
  - `fgets`와 `strtok`를 이용하여 입력을 처리한다.
  - 이름과 메시지를 분리하여 배열에 저장한다.

- **메시지 분석**:
  - C언어 스타일로 배열과 인덱스를 사용하여 메시지를 분석한다.
  - 메시지 작성자의 인덱스를 계산하여 나쁜 메시지를 찾는다.

- **출력**:
  - 표준 출력으로 결과를 출력한다.
  - 나쁜 메시지가 없을 경우 해당 메시지를 출력한다.

## Python 코드와 설명

```python
group_number = 1

while True:
    n = int(input())
    if n == 0:
        break

    names = []
    messages = []

    for _ in range(n):
        line = input().strip().split()
        names.append(line[0])
        messages.append(line[1:])

    nasty_messages = []

    for i in range(n):
        owner = i
        message_count = len(messages[i])
        for j in range(message_count):
            writer = (owner - j - 1) % n
            if messages[i][j] == 'N':
                nasty_messages.append((names[writer], names[owner]))

    print(f"Group {group_number}")
    if not nasty_messages:
        print("Nobody was nasty")
    else:
        for writer, owner in nasty_messages:
            print(f"{writer} was nasty about {owner}")
    print()

    group_number += 1
```

### 코드 설명

- **입력 처리**:
  - 반복문을 통해 그룹별로 데이터를 입력받는다.
  - 이름과 메시지를 리스트에 저장한다.

- **메시지 분석**:
  - 각 메시지를 확인하면서 작성자를 계산한다.
  - 나쁜 메시지('N')인 경우 결과 리스트에 추가한다.

- **출력**:
  - 요구된 형식에 맞게 결과를 출력한다.
  - 나쁜 메시지가 없으면 "Nobody was nasty"를 출력한다.

## 결론

이 문제는 구현과 시뮬레이션 능력을 요구하는 좋은 연습 문제였다. 원형으로 앉은 아이들의 메시지 전달 과정을 정확히 구현하는 것이 핵심이었다. 특히 인덱스 계산에서 모듈러 연산을 활용하여 원형 구조를 표현하는 방법을 익힐 수 있었다.

추가적으로, 코드의 효율성을 높이기 위해 불필요한 연산을 줄이고 자료 구조를 효율적으로 사용하는 방법을 고민해볼 수 있었다. 이러한 구현 문제를 많이 풀어보면서 꼼꼼한 코딩과 디버깅 능력을 향상시킬 수 있을 것이다.