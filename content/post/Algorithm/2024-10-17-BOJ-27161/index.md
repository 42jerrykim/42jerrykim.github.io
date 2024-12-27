---
title: "[Algorithm] C++/Python 백준 27161번 : 크레이지 타임"
categories: 
- Algorithm
- Implementation
- Simulation
tags:
- Implementation
- Simulation
- BruteForce
- O(N)
- Implementation Strategy: Simulation
image: "tmp_wordcloud.png"
date: 2024-01-01
---

우주 어딘가에는 시간을 셈으로써 시간이 흐르도록 만들어 주는 존재들이 있습니다. 영겁의 시간을 살아온 그들은 더 재미있게 시간을 세기 위해 시간을 세는 게임을 만들어 냈답니다. 그게 바로 《크레이지 타임》이죠! 이 게임에서는 플레이어들이 시간 카드를 이용해 시각을 외치며 다양한 법칙을 따르면서 진행됩니다. 이번 포스팅에서는 이 《크레이지 타임》 게임의 문제를 해결하는 방법에 대해 알아보겠습니다.

문제 : [https://www.acmicpc.net/problem/27161](https://www.acmicpc.net/problem/27161)

## 문제 설명

《크레이지 타임》 게임은 시간 카드를 사용하여 시각을 외치는 게임입니다. 게임을 시작하기 전에 시간 카드를 잘 섞은 후 플레이어들에게 최대한 비슷한 수량의 카드를 나눠줍니다. 각 시간 카드는 앞면과 뒷면이 있으며, 앞면에는 시계 그림과 시각이 적혀 있습니다. 시계의 종류는 벽시계(CLOCK), 손목시계(WATCH), 모래시계(HOURGLASS)로 총 세 가지가 있습니다. 플레이어들은 자신의 카드 더미를 뒷면이 보이도록 쌓아둡니다.

게임은 다음과 같은 규칙으로 진행됩니다:

1. 플레이어는 자신의 차례가 되면 개인 더미의 가장 윗장 카드를 펼치며 이번 순서의 시각을 외칩니다. 첫 번째 플레이어는 "1시"로 시작합니다.
2. 시계 방향으로 차례가 돌아가며, 특별한 방해 요소가 없다면 이전에 외친 시각에 1시간을 더해 다음 시각을 외칩니다. 예를 들어, 이전에 "12시"를 외쳤다면 다음 플레이어는 "1시"를 외칩니다.
3. 펼쳐진 카드에 따라 특별한 규칙이 적용될 수 있습니다:
    - **시간 역행의 법칙**: 모래시계 카드를 펼치면 시간이 거꾸로 흐르기 시작합니다. "2시", "1시", "12시" 순으로 외쳐야 합니다. 모래시계 카드를 펼칠 때마다 시간의 흐름이 반전됩니다.
    - **동기화의 법칙**: 플레이어가 외친 시각과 카드에 적힌 시각이 일치하면 모든 플레이어는 게임판 중앙을 손바닥으로 내리쳐야 합니다.
4. **과부하의 원칙**: 한 카드가 동시에 두 개 이상의 법칙을 발동시키면, 어떤 법칙도 적용되지 않습니다.

게임 중 잘못된 시각을 외치거나 손바닥을 가장 늦게 내리친 플레이어는 벌점 토큰을 받습니다. 벌점 토큰을 받은 후 게임은 초기화되며, 벌점을 받은 플레이어가 "1시"를 외치며 게임을 재개합니다. 

이번 문제에서는 카드들이 주어질 때, 각 차례의 플레이어가 외쳐야 하는 시각과 해야 하는 행동을 출력하는 프로그램을 작성해야 합니다. 

## 접근 방식

이 문제는 시뮬레이션 문제로, 게임의 규칙을 그대로 코드로 구현하는 방식으로 접근할 수 있습니다. 다음과 같은 단계로 문제를 해결할 수 있습니다:

1. **입력 처리**: 펼쳐질 카드의 개수 N과 각 카드의 정보를 입력받습니다.
2. **초기 설정**: 현재 시각을 1시로 설정하고, 시간의 흐름 방향을 앞으로 설정합니다.
3. **카드 순회**: 각 카드에 대해 다음을 수행합니다:
    - 카드를 펼치고, 시각과 카드에 적힌 시각을 비교합니다.
    - 동시에 여러 법칙이 발동되는지 확인합니다 (과부하의 원칙).
    - 법칙에 따라 시각을 외치고, 필요한 경우 행동을 결정합니다.
    - 시간의 흐름을 업데이트합니다 (방향에 따라 시각을 증가 또는 감소).
4. **출력**: 각 차례마다 외친 시각과 행동을 출력합니다.

특히, 시간의 흐름 방향이 바뀔 때와 시각이 12시를 넘어갈 때를 주의 깊게 처리해야 합니다. 또한, 과부하의 원칙을 적용하여 여러 법칙이 동시에 발동될 경우 법칙을 무시해야 합니다.

## C++ 코드와 설명

```cpp
#include <bits/stdc++.h>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);
    
    int N;
    cin >> N;
    
    // 초기 시각과 방향 설정
    int current_time = 1;
    int direction = 1; // 1: 앞으로, -1: 뒤로
    
    for(int i=0;i<N;i++){
        string S;
        int X;
        cin >> S >> X;
        
        bool isHOURGLASS = (S == "HOURGLASS");
        bool isSYNC = (X == current_time);
        
        // 과부하 체크: 두 개 이상의 법칙이 발동하면 아무 것도 하지 않음
        if(isHOURGLASS && isSYNC){
            // 아무 것도 하지 않음
            cout << current_time << " NO\n";
        }
        else{
            // 동기화의 법칙 적용 여부 확인
            if(isSYNC){
                cout << current_time << " YES\n";
            }
            else{
                cout << current_time << " NO\n";
            }
            
            // 시간 역행의 법칙 적용
            if(isHOURGLASS){
                direction *= -1;
            }
        }
        
        // 시각 업데이트
        current_time += direction;
        if(current_time > 12){
            current_time = 1;
        }
        if(current_time < 1){
            current_time = 12;
        }
    }
}
```

### 코드의 동작을 단계별로 상세하게 설명

1. **입력 처리**:
    - `N`을 입력받아 카드의 개수를 결정합니다.
    - 각 카드에 대해 시계의 종류 `S`와 시각 `X`를 입력받습니다.

2. **초기 설정**:
    - `current_time`을 1시로 설정합니다.
    - `direction`을 1로 설정하여 시간이 앞으로 흐르도록 합니다.

3. **카드 순회**:
    - 각 카드에 대해:
        - `isHOURGLASS`를 통해 현재 카드가 모래시계인지 확인합니다.
        - `isSYNC`를 통해 현재 시각과 카드에 적힌 시각이 일치하는지 확인합니다.
        - **과부하의 원칙**: 만약 `isHOURGLASS`와 `isSYNC`가 모두 참이면, 아무 행동도 하지 않고 "NO"를 출력합니다.
        - 그렇지 않으면:
            - `isSYNC`가 참일 경우 "YES"를 출력합니다.
            - `isSYNC`가 거짓일 경우 "NO"를 출력합니다.
            - `isHOURGLASS`가 참일 경우, 시간의 흐름 방향을 반전시킵니다.
        - 시각을 `direction`에 따라 업데이트합니다. 12시를 넘어가면 1시로, 1시보다 작아지면 12시로 설정합니다.

4. **출력**:
    - 각 차례마다 외친 시각과 행동("YES" 또는 "NO")을 출력합니다.

## Python 코드와 설명

```python
def main():
    import sys
    input = sys.stdin.readline
    
    N = int(input())
    current_time = 1
    direction = 1  # 1: forward, -1: backward
    
    for _ in range(N):
        S, X = input().split()
        X = int(X)
        
        isHOURGLASS = (S == "HOURGLASS")
        isSYNC = (X == current_time)
        
        if isHOURGLASS and isSYNC:
            # Overload: No action
            print(f"{current_time} NO")
        else:
            if isSYNC:
                print(f"{current_time} YES")
            else:
                print(f"{current_time} NO")
            
            if isHOURGLASS:
                direction *= -1
        
        # Update current_time
        current_time += direction
        if current_time > 12:
            current_time = 1
        elif current_time < 1:
            current_time = 12

if __name__ == "__main__":
    main()
```

### 코드의 동작을 단계별로 상세하게 설명

1. **입력 처리**:
    - `N`을 입력받아 카드의 개수를 결정합니다.
    - 각 카드에 대해 시계의 종류 `S`와 시각 `X`를 입력받습니다.

2. **초기 설정**:
    - `current_time`을 1시로 설정합니다.
    - `direction`을 1로 설정하여 시간이 앞으로 흐르도록 합니다.

3. **카드 순회**:
    - 각 카드에 대해:
        - `isHOURGLASS`를 통해 현재 카드가 모래시계인지 확인합니다.
        - `isSYNC`를 통해 현재 시각과 카드에 적힌 시각이 일치하는지 확인합니다.
        - **과부하의 원칙**: 만약 `isHOURGLASS`와 `isSYNC`가 모두 참이면, 아무 행동도 하지 않고 "NO"를 출력합니다.
        - 그렇지 않으면:
            - `isSYNC`가 참일 경우 "YES"를 출력합니다.
            - `isSYNC`가 거짓일 경우 "NO"를 출력합니다.
            - `isHOURGLASS`가 참일 경우, 시간의 흐름 방향을 반전시킵니다.
        - 시각을 `direction`에 따라 업데이트합니다. 12시를 넘어가면 1시로, 1시보다 작아지면 12시로 설정합니다.

4. **출력**:
    - 각 차례마다 외친 시각과 행동("YES" 또는 "NO")을 출력합니다.

## 결론

이번 《크레이지 타임》 문제는 게임의 규칙을 충실히 코드로 구현하는 시뮬레이션 문제였다. 시간의 흐름 방향을 적절히 관리하고, 과부하의 원칙을 정확히 적용하는 것이 핵심이었다. 문제의 규칙을 잘 이해하고, 시각을 업데이트하는 과정에서 모듈러 연산을 활용하여 시각이 1시에서 12시 사이를 유지하도록 처리하였다. 

추가적인 최적화 방안으로는, 입력을 빠르게 처리하기 위해 C++에서는 `ios::sync_with_stdio(false)`와 `cin.tie(0)`을 사용하였으며, Python에서는 `sys.stdin.readline`을 활용하여 입력 속도를 개선하였다. 이 문제는 구현의 정확성이 중요한 문제였으며, 다양한 조건을 꼼꼼히 체크하는 것이 중요했다.

앞으로 유사한 시뮬레이션 문제를 풀 때에는 문제의 규칙을 잘 분석하고, 각 조건을 코드로 옮기는 연습을 통해 구현력을 더욱 향상시킬 수 있을 것이다.