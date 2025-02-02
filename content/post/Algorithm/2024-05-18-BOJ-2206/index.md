---
image: "tmp_wordcloud.png"
categories: Algorithm
date: "2024-05-18T00:00:00Z"
header:
  teaser: /assets/images/2024/diagram_understanding_breaking_walls.png
tags:
- BFS
- Graph
title: '[Algorithm] C++ 백준 2206번 : 벽 부수고 이동하기'

---

"벽 부수고 이동하기" 문제는 N×M 크기의 2차원 배열로 주어진 맵에서 (1,1)에서 (N,M)까지 이동하는 최단 경로를 찾는 것이다. 이동은 상하좌우로 가능하며, 벽(1)을 최대 한 개까지 부술 수 있다. BFS를 활용하여 벽을 부순 상태와 부수지 않은 상태를 구분하여 최단 경로를 탐색하는 문제이다. 이동할 수 없는 경우 -1을 출력한다.

[원문 링크](https://www.acmicpc.net/problem/2206)

|![](/assets/images/2024/diagram_understanding_breaking_walls.png)|
|:---:|
|이미지로 형상화|

## 문제 이해
1. **맵의 크기**: NxM의 2차원 배열로 구성되며, 각 위치는 이동 가능(0) 또는 벽(1)으로 표시된다.
2. **목적지**: (1,1)에서 (N,M)까지의 최단 경로를 찾는 것.
3. **특징**: 벽을 최대 한 개까지 부술 수 있다.

## 접근 방법
1. **BFS (너비 우선 탐색)**를 이용하여 최단 경로를 탐색한다.
2. **방문 상태 관리**: 벽을 부순 상태와 부수지 않은 상태를 구분하여 3차원 배열로 방문 여부를 기록한다.

## 단계별 풀이
1. **입력 처리**: N, M과 맵 정보를 입력받는다.
2. **자료 구조 초기화**:
   - `visited` 배열: `visited[x][y][0]`은 벽을 부수지 않고 (x, y)에 도착한 상태를, `visited[x][y][1]`은 벽을 부수고 (x, y)에 도착한 상태를 기록한다.
   - `queue`: BFS 탐색을 위한 큐, 초기값은 시작점 (0, 0, 0) (벽을 부수지 않은 상태).
3. **BFS 탐색**:
   - 큐에서 현재 위치를 꺼내서 상하좌우로 이동할 수 있는 모든 경우를 확인한다.
   - 이동 가능한 경우를 확인하여 방문하지 않은 위치를 큐에 추가한다.
   - 벽을 부수는 경우, 아직 벽을 부수지 않았을 때만 벽을 부수고 이동할 수 있다.
4. **결과 반환**:
   - 목적지에 도달하면 해당 위치의 방문 횟수를 반환한다.
   - 모든 경로를 탐색해도 목적지에 도달하지 못하면 -1을 반환한다.

## 예제 코드
```python
from collections import deque

def bfs(N, M, graph):
    visited = [[[0] * 2 for _ in range(M)] for _ in range(N)]
    queue = deque([(0, 0, 0)])
    visited[0][0][0] = 1
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        x, y, wall_broken = queue.popleft()
        
        if x == N-1 and y == M-1:
            return visited[x][y][wall_broken]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < N and 0 <= ny < M:
                if graph[nx][ny] == 0 and visited[nx][ny][wall_broken] == 0:
                    visited[nx][ny][wall_broken] = visited[x][y][wall_broken] + 1
                    queue.append((nx, ny, wall_broken))
                
                if graph[nx][ny] == 1 and wall_broken == 0 and visited[nx][ny][1] == 0:
                    visited[nx][ny][1] = visited[x][y][wall_broken] + 1
                    queue.append((nx, ny, 1))
    
    return -1

# 입력 처리
N, M = map(int, input().split())
graph = [list(map(int, input().strip())) for _ in range(N)]

# BFS를 이용한 최단 경로 탐색
print(bfs(N, M, graph))
```

위의 코드와 같이 BFS 알고리즘을 활용하여 문제를 해결할 수 있다. 주요 포인트는 벽을 부순 상태와 그렇지 않은 상태를 명확하게 구분하여 각각의 상태를 관리하는 것이다. 이를 통해 최단 경로를 정확하게 찾아낼 수 있다.