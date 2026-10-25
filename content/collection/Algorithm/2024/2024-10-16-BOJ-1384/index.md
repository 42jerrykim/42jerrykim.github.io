---
title: "[Algorithm] C++/Python 백준 1384번 : 메시지"
description: "백준 1384번 메시지는 원형으로 앉은 아이들이 종이를 돌려 쓴 N/P 기록에서 누가 누구에게 나쁜 말을 했는지 모듈러 인덱스 (i-j-1+n)%n으로 역산하는 구현 문제다. C++, C, Python 세 가지 풀이와 O(n²) 복잡도, 코너 케이스를 함께 정리한다."
categories: Algorithm
tags:
- Implementation(구현)
- Simulation(시뮬레이션)
- Brute-Force(완전탐색)
- Data-Structures(자료구조)
- Time-Complexity(시간복잡도)
- Algorithm(알고리즘)
- BOJ(백준)
- Competitive-Programming(경쟁프로그래밍)
- Problem-Solving(문제해결)
- C++
- Coding-Test(코딩테스트)
- Optimization(최적화)
- Code-Quality(코드품질)
- Python
- String(문자열)
- Space-Complexity(공간복잡도)
- Edge-Cases(엣지케이스)
- Testing(테스트)
- Complexity-Analysis(복잡도분석)
- Debugging(디버깅)
- Refactoring(리팩토링)
- Clean-Code(클린코드)
- Performance(성능)
- Pitfalls(함정)
- Error-Handling(에러처리)
- BOJ-1384
- Circular-Array(원형배열)
date: 2024-10-16
lastmod: 2024-10-16
image: "wordcloud.png"
---

알고리즘 문제를 풀다 보면 구현 능력이 중요한 경우가 많다. 이 글에서는 백준 온라인 저지의 1384번 문제인 "메시지"를 풀면서, 원형 구조를 모듈러 연산으로 다루는 방법과 "누가 썼는가"를 입력 순서에서 역산하는 사고방식을 정리한다.

문제 : [https://www.acmicpc.net/problem/1384](https://www.acmicpc.net/problem/1384)

## 문제 설명

여러 명의 아이들이 원형으로 앉아 각자 종이 한 장의 맨 위에 자기 이름을 적는다. 종이는 한 방향으로 한 칸씩 전달되고, 종이를 받은 아이는 그 종이 주인에 대한 메시지를 적은 뒤 맨 위를 접어 가린다. 이렇게 한 바퀴를 돌면 모든 종이에 주인을 향한 메시지가 쌓이고, 아이들은 자기 종이를 펼쳐 읽는다.

메시지 중에는 "넌 너무 말이 많아."처럼 기분 나쁜 말이 있을 수 있다. 입력은 그룹 단위로 주어진다. 각 그룹은 아이들의 수 n으로 시작하고, 이어지는 n줄에는 아이의 이름과 그 아이 종이에 적힌 메시지의 평가 기록이 순서대로 주어진다. 기록은 좋은 말이면 `P`, 나쁜 말이면 `N`이다. 목표는 `N`마다 "누가 누구에게 나쁜 말을 했는지"를 출력하는 것이다. n의 정확한 범위와 출력 형식(그룹 헤더, 빈 줄 규칙)은 위 문제 페이지의 제약을 따른다. 입력은 n이 0이면 끝난다.

## 접근 방식

핵심은 입력에 작성자가 직접 적혀 있지 않다는 점이다. 종이 주인 i가 정해지고 그 종이의 j번째(0부터 센다) 메시지가 `N`이라는 사실만 주어지므로, 작성자는 좌석 구조에서 역산해야 한다. 종이는 인덱스가 줄어드는 방향으로 한 칸씩 전달되므로 주인 i의 종이를 처음 받는 사람은 i-1번, 그다음은 i-2번이다. 따라서 j번째 메시지를 쓴 사람은 주인에서 j+1칸 떨어진 i-j-1번이고, 인덱스가 음수가 되면 n을 더해 한 바퀴 돌려 보정해야 하므로 `(i - j - 1 + n) % n`이 된다. 이 방향 서술과 식은 아래 세 코드가 모두 공유하는 규약이며, 입력 순서를 기준으로 한 해석이 바뀌면 식의 부호만 반대로 바뀐다.

이 규약을 n=4(A, B, C, D가 인덱스 0–3)로 추적하면 다음과 같다. 종이 주인 A(i=0)의 기록이 `P N P`라면 j=0,1,2의 작성자는 (0-0-1+4)%4=3(D), (0-1-1+4)%4=2(C), (0-2-1+4)%4=1(B)이다. 따라서 j=1의 `N`은 "C was nasty about A"가 된다.

| 종이 주인 i | j | 계산 | 작성자 | 기록 | 출력 |
|---|---|---|---|---|---|
| 0 (A) | 0 | (0-0-1+4)%4 = 3 | D | P | - |
| 0 (A) | 1 | (0-1-1+4)%4 = 2 | C | N | C was nasty about A |
| 0 (A) | 2 | (0-2-1+4)%4 = 1 | B | P | - |

모든 종이를 이렇게 훑으면서 `N`만 모으면 되므로, 알고리즘은 입력 파싱, 작성자 역산, 출력의 세 단계로 단순하다. 자료구조는 이름 배열과 종이별 기록 배열이면 충분하다.

## 복잡도 분석

한 그룹에서 모든 종이의 모든 기록을 한 번씩 보므로 총 기록 수에 비례한다. 종이 한 장에 쓰인 메시지는 한 바퀴를 넘지 않으므로 기록 수는 최대 n개이고, 전체는 n장이다.

| 구분 | 복잡도 | 근거 |
|---|---|---|
| 시간 | O(n²) | n장의 종이 × 종이당 최대 n개 기록, 각 기록의 작성자 계산은 O(1) |
| 공간 | O(n²) | 이름 n개와 기록 최대 n×n개, 결과 목록도 최대 n² 쌍 |

n이 작은 문제이므로 이 정도는 여유롭다. 개선할 여지는 시간이 아니라 입력을 줄 단위로 안전하게 읽는 쪽에 있다.

## C++ 코드와 설명

C++ 풀이는 `getline`으로 한 줄을 읽고 `stringstream`으로 이름과 `P`/`N` 문자를 분리한다. 그룹 시작의 n을 `cin >> n`으로 읽은 뒤 남은 개행을 `cin.ignore()`로 지워야 첫 `getline`이 빈 줄을 읽지 않는다. 작성자 계산은 접근 방식에서 유도한 식을 그대로 쓰며, `N`이 나오면 (작성자 이름, 주인 이름) 쌍을 모아 두었다가 그룹 끝에서 한꺼번에 출력한다. 모아 두는 이유는 나쁜 말이 하나도 없을 때 "Nobody was nasty"를 출력해야 하기 때문이다.

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

## C (표준 입출력) 코드와 설명

C 풀이는 `scanf`/`fgets`/`strtok`만 쓰는 같은 알고리즘이다. 배열 크기를 상수로 고정하고 `fgets`로 한 줄을 읽어 `strtok`으로 공백 단위 토큰을 분리한다. 첫 토큰이 이름이고 나머지 토큰의 첫 글자가 `P`/`N`이다. C++ 버전과 달리 결과를 모으지 않고 `nastyFound` 플래그 하나로 "아무도 없음" 출력을 판정하므로 메모리가 더 적게 든다. 다만 `fgets` 뒤의 개행 제거는 LF 문자 하나만 처리하므로, 입력 파일이 CR+LF 줄바꿈이면 이름 끝에 CR 문자가 남을 수 있다는 점은 유의해야 한다.

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

## Python 코드와 설명

Python 풀이는 `input().strip().split()`으로 줄을 분해해 첫 원소를 이름, 나머지를 기록으로 쓴다. 파이썬의 `%`는 피제수가 음수여도 결과가 0 이상이므로 `+ n` 보정이 필요 없다. 이 차이는 같은 식을 C/C++로 옮길 때 가장 흔한 실수 지점이다. 결과는 (작성자, 주인) 튜플 리스트에 모아 f-string으로 출력한다.

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

## 코너 케이스 및 실수 포인트

| 케이스 | 설명 | 처리 방법 |
|---|---|---|
| 나쁜 말이 없는 그룹 | 모든 기록이 `P` | "Nobody was nasty"를 출력한다 |
| 음수 인덱스 | i-j-1이 음수가 되는 경우 | C/C++는 `+ n` 후 `% n`, Python은 `% n`만으로 충분 |
| 개행 처리 | `cin >> n` 직후 `getline`이 빈 줄을 읽음 | `cin.ignore()` 또는 `getchar()`로 개행 제거 |
| 줄바꿈 형식 | CR+LF 입력에서 이름 끝에 CR 문자 잔존 | 토큰 분리 시 공백류로 함께 잘라내거나 CR을 제거 |
| 출력 형식 | 그룹 사이 빈 줄, 헤더 번호 | 문제 페이지의 출력 예제와 한 글자씩 대조 |

## 정리와 학습 목표

이 문제는 "정보가 입력에 없으면 구조에서 역산한다"는 패턴을 연습하는 구현 문제다. 원형 배열은 `(x + n) % n`으로 한 바퀴 돌려 보정하고, 방향(전달 방향)과 순서(몇 번째 메시지인지)를 먼저 한 문장으로 못 박은 뒤 식을 세우면 부호 실수가 줄어든다. 이 글을 읽고 나면 원형 좌석에서 j번째 전달자의 인덱스를 식으로 유도하고, 언어별 나머지 연산의 차이를 설명하며, 입력 개행 처리 때문에 생기는 오답을 점검할 수 있어야 한다.
