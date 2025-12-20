---
title: "[Algorithm] C++/Python 백준 13907번 : 세금"
description: "백준 13907번 '세금' 문제는 세금 인상 전후 최소 통행료를 각 경로 길이별로 동적 계획법과 반복적 그래프 완화(Bellman-Ford) 기법을 활용해 계산한다. 본문에서는 효율적인 구현 전략과 알고리즘 최적화 방안, 경로별 누적 세금 처리를 상세히 다룬다."
categories: 
- Algorithm
- Platinum IV
- Dynamic Programming
- Graph Theory
tags:
- DP
- Graph Theory
- Iterative Relaxation
- Memoization
- O(N*M)
- Array
- Bellman-Ford
- Dynamic Programming
image: "index.png"
date: 2025-02-07
---

본 포스트에서는 백준 문제 13907번 “세금”을 다루고 있으며, 해당 문제를 해결하기 위한 다양한 알고리즘 아이디어와 최적화 기법을 소개하고자 한다. 문제의 핵심은 모든 도로의 통행료에 동일하게 누적되는 세금 인상에 따른 경로 비용 변화를 효율적으로 계산하는 것이다. C++와 Python 두 가지 언어로 구현한 코드를 통해 문제 해결 과정을 상세히 설명할 것이며, 문제의 접근 방식과 코드의 각 부분에 대해 한 줄 한 줄 주석과 함께 분석할 것이다.

문제 : [https://www.acmicpc.net/problem/13907](https://www.acmicpc.net/problem/13907)

## 문제 설명

이 문제는 N개의 도시와 M개의 양방향 도로로 구성된 그래프에서, 출발 도시 S에서 도착 도시 D까지 이동하는 과정에서 발생하는 통행료 문제를 다룬다. 각 도로에는 기본 통행료가 존재하며, 정부는 한 번에 올리지 않고 여러 단계에 걸쳐 세금을 인상한다. 세금이 p만큼 인상되면 모든 도로의 통행료에 p가 추가되며, 이 세금은 누적된다. 즉, 경로상에 l개의 도로를 거치면 최종 통행료는 (기본 통행료의 합) + l × (누적 세금)이 된다. 문제의 요구사항은 최초 세금 인상 전과 K번의 세금 인상 이후에 대해 S에서 D로 이동하는 최소 통행료를 각각 계산하는 것이다. 단순히 다익스트라 알고리즘을 적용하기에는 세금 인상이라는 추가 요소 때문에 경로의 길이에 따른 가중치 변화가 발생하므로, 경로에 포함된 도로의 개수 l에 따른 기본 통행료의 최소값을 미리 구해놓고 누적 세금을 반영하여 최종 비용을 계산해야 한다. 이 문제는 동적 계획법(Dynamic Programming)과 그래프 이론(Graph Theory)의 기법을 적절히 혼용하여 해결할 수 있으며, 반복적 완화(iterative relaxation) 기법을 통해 각 경로 길이별 최소 기본 통행료를 구하는 전략을 사용한다. 문제의 제한 조건이 상당히 크므로(N 최대 1,000, M 최대 30,000, K 최대 30,000) 효율적인 구현이 필수적이다.

## 접근 방식

본 문제는 도로마다 동일하게 누적되는 세금 인상 구조를 고려할 때, S에서 D까지 l개의 도로를 사용한 경우의 기본 통행료를 미리 계산해놓고, 각 세금 인상 단계마다 “최종 비용 = 기본 통행료 + l × (누적 세금)”의 형태로 최소값을 구하는 방식으로 접근한다. 구체적으로는, l = 1부터 최대 N-1까지 각 경로 길이에 대해 동적 계획법(DP)을 이용하여 S에서 D까지 도달하는 최소 기본 통행료 best[l]를 계산한다. 이후, 초기에는 세금이 없으므로 best[l] 중 최솟값이 답이 되며, 세금이 인상될 때마다 누적 세금을 갱신하고, 각 l에 대해 best[l] + l × (누적 세금) 값의 최솟값을 출력하는 방식이다. 이 과정은 Bellman–Ford 알고리즘의 반복적 완화(iterative relaxation) 기법과 유사하게 진행되며, 각 단계마다 모든 도로에 대해 relax 연산을 수행하여 dp 배열을 갱신하는 방식으로 구현된다.

## C++ 코드와 설명

다음은 본 문제를 해결하기 위한 최적화된 C++ 코드이다.

```cpp
#include <iostream>            // 입출력을 위한 헤더이다.
#include <vector>              // vector 컨테이너를 사용하기 위한 헤더이다.
#include <algorithm>           // min 함수를 사용하기 위한 헤더이다.
#include <limits>              // 무한대 상수를 정의하기 위한 헤더이다.
using namespace std;

const long long INF = 1e18;      // 매우 큰 값을 INF로 정의한 것이다.

int main(){
    ios::sync_with_stdio(false);   // 빠른 입출력을 위해 sync를 해제한 것이다.
    cin.tie(nullptr);              // cin과 cout의 tie를 해제한 것이다.
    
    int N, M, K;
    cin >> N >> M >> K;            // 도시의 수, 도로의 수, 세금 인상 횟수를 입력받은 것이다.
    int S, D;
    cin >> S >> D;                 // 출발 도시와 도착 도시 번호를 입력받은 것이다.
    
    // 1부터 N까지의 도시를 노드로 하여, 양방향 도로 정보를 저장한 것이다.
    vector<vector<pair<int,int>>> graph(N+1);
    for (int i = 0; i < M; i++){
        int a, b, w;
        cin >> a >> b >> w;       // 각 도로의 양 끝 도시와 기본 통행료를 입력받은 것이다.
        graph[a].push_back({b, w}); // 도시 a에서 b로의 도로 정보를 저장한 것이다.
        graph[b].push_back({a, w}); // 도시 b에서 a로의 도로 정보도 저장한 것이다.
    }
    
    int maxL = N - 1;              // 최대로 사용할 수 있는 도로의 개수이다.
    vector<long long> dp(N+1, INF), next_dp(N+1, INF);
    dp[S] = 0;                   // 시작 도시 S의 비용은 0으로 초기화한 것이다.
    // best[l]는 l개의 도로를 사용하여 D에 도달하는 최소 기본 통행료이다.
    vector<long long> best(maxL+1, INF);
    
    // l = 1부터 maxL까지 경로 길이에 따른 최소 비용을 계산한 것이다.
    for (int l = 1; l <= maxL; l++){
        fill(next_dp.begin(), next_dp.end(), INF);  // 다음 단계 dp 배열을 INF로 초기화한 것이다.
        for (int u = 1; u <= N; u++){
            if(dp[u] == INF) continue;                // u에 도달할 수 없는 경우를 건너뛴 것이다.
            // u에서 인접한 모든 정점을 확인하여 relax 연산을 수행한 것이다.
            for(auto &edge : graph[u]){
                int v = edge.first;
                int w = edge.second;
                next_dp[v] = min(next_dp[v], dp[u] + w); // v까지 l개의 도로로 이동하는 최소 비용을 갱신한 것이다.
            }
        }
        dp = next_dp;              // dp 배열을 한 단계 진행한 결과로 갱신한 것이다.
        best[l] = dp[D];           // D에 도달하는 l개의 도로를 사용한 최소 비용을 저장한 것이다.
    }
    
    // 초기 세금(0)일 때의 최소 통행료를 계산한 것이다.
    long long initAns = INF;
    for (int l = 1; l <= maxL; l++){
        if(best[l] < initAns)
            initAns = best[l];
    }
    cout << initAns << "\n";
    
    long long cumTax = 0;         // 누적 세금을 저장할 변수이다.
    // K번의 세금 인상에 대해 최소 통행료를 계산한 것이다.
    for (int i = 0; i < K; i++){
        int p;
        cin >> p;               // 현재 단계에서 인상되는 세금을 입력받은 것이다.
        cumTax += p;            // 누적 세금을 갱신한 것이다.
        long long ans = INF;
        // 모든 가능한 경로 길이에 대해 최종 비용 (기본 통행료 + l × 누적 세금)을 계산하여 최소값을 찾은 것이다.
        for (int l = 1; l <= maxL; l++){
            if(best[l] < INF){
                ans = min(ans, best[l] + (long long)l * cumTax);
            }
        }
        cout << ans << "\n";    // 현재 세금 인상 단계에서의 최소 통행료를 출력한 것이다.
    }
    
    return 0;                  // 프로그램을 정상 종료한 것이다.
}
```

위 코드는 먼저 S에서 시작하여 l개의 도로를 사용해 도달 가능한 모든 도시의 최소 기본 통행료를 동적 계획법 방식으로 계산한 것이다. 이후 누적 세금이 적용될 때마다 각 경로 길이별로 (기본 통행료 + l × 누적 세금)을 계산하여 그 중 최솟값을 답으로 출력하는 구조이다.

## Python 코드와 설명

다음은 동일한 알고리즘을 Python으로 구현한 코드이다.

```python
import sys
input = sys.stdin.readline         # 빠른 입출력을 위한 input 함수이다.
INF = 10**18                         # 매우 큰 값을 INF로 정의한 것이다.

def main():
    N, M, K = map(int, input().split())  # 도시의 수, 도로의 수, 세금 인상 횟수를 입력받은 것이다.
    S, D = map(int, input().split())       # 시작 도시와 도착 도시 번호를 입력받은 것이다.
    
    # 각 도시별 인접 리스트를 생성한 것이다.
    graph = [[] for _ in range(N+1)]
    for _ in range(M):
        a, b, w = map(int, input().split())  # 도로의 양 끝 도시와 기본 통행료를 입력받은 것이다.
        graph[a].append((b, w))              # 도시 a에서 b로 가는 도로 정보를 추가한 것이다.
        graph[b].append((a, w))              # 도시 b에서 a로 가는 도로 정보도 추가한 것이다.
    
    maxL = N - 1                           # 최대 도로 사용 개수이다.
    dp = [INF] * (N+1)                     # 현재 단계의 최소 비용 배열을 초기화한 것이다.
    dp[S] = 0                              # 시작 도시 S의 비용은 0으로 설정한 것이다.
    best = [INF] * (maxL+1)                # l개의 도로를 사용한 D 도착 비용을 저장할 배열이다.
    
    # l = 1부터 maxL까지 각 경로 길이에 따른 최소 비용을 계산한 것이다.
    for l in range(1, maxL+1):
        next_dp = [INF] * (N+1)            # 다음 단계의 dp 배열을 INF로 초기화한 것이다.
        for u in range(1, N+1):
            if dp[u] == INF:
                continue                   # u에 도달할 수 없는 경우는 건너뛴 것이다.
            # u에서 갈 수 있는 모든 인접 도시 v에 대해 relax 연산을 수행한 것이다.
            for v, w in graph[u]:
                if dp[u] + w < next_dp[v]:
                    next_dp[v] = dp[u] + w
        dp = next_dp                       # dp 배열을 한 단계 진행한 결과로 갱신한 것이다.
        best[l] = dp[D]                    # l개의 도로를 사용하여 D에 도달하는 최소 비용을 저장한 것이다.
    
    # 초기 세금(0)일 때의 최소 통행료를 계산한 것이다.
    initAns = min(best[1:])                # 1개 이상의 도로를 이용한 최소 비용 중 최솟값을 찾은 것이다.
    sys.stdout.write(str(initAns) + "\n")
    
    cumTax = 0                           # 누적 세금을 저장하는 변수이다.
    # 각 세금 인상 단계마다 최종 최소 통행료를 계산한 것이다.
    for _ in range(K):
        p = int(input())                 # 현재 단계에서 인상되는 세금을 입력받은 것이다.
        cumTax += p                      # 누적 세금을 갱신한 것이다.
        ans = INF
        # 모든 가능한 경로 길이에 대해 (기본 통행료 + l × 누적 세금)을 계산하여 최솟값을 찾은 것이다.
        for l in range(1, maxL+1):
            if best[l] < INF:
                ans = min(ans, best[l] + l * cumTax)
        sys.stdout.write(str(ans) + "\n")  # 현재 세금 인상 단계의 최소 통행료를 출력한 것이다.
    
if __name__ == '__main__':
    main()                               # main 함수를 호출하여 프로그램을 시작한 것이다.
```

이 Python 코드는 C++ 코드와 동일한 알고리즘을 사용하여 각 단계별로 dp 배열을 갱신한 후, 누적 세금을 반영하여 최종 비용을 계산하는 방식이다. 다만, Python의 경우 반복문의 최적화가 덜 되어 있어 제한 조건이 매우 큰 경우에는 속도 개선을 위한 추가적인 기법이 필요할 수 있다.

## 결론

본 문제는 도로마다 동일하게 누적되는 세금 인상이라는 특수 조건 하에서 S에서 D까지 이동하는 최소 통행료를 계산하는 문제이다. 각 경로 길이별로 기본 통행료의 최소값을 미리 구해두고, 누적 세금을 반영하여 최종 비용을 산출하는 방식은 동적 계획법과 반복적 완화를 통해 효율적으로 구현할 수 있었다. C++에서는 빠른 입출력과 반복문의 최적화 덕분에 문제를 원활하게 해결할 수 있었으며, Python의 경우 코드의 가독성을 유지하면서도 동일한 알고리즘 아이디어를 적용하였으나, 매우 큰 입력에 대해서는 추가적인 최적화가 필요할 수 있음을 느낀 문제이다. 이와 같이 문제를 접근하고 해결하는 과정은 그래프 이론과 동적 계획법의 융합 아이디어를 이해하는 데 많은 도움이 된다고 생각된다.