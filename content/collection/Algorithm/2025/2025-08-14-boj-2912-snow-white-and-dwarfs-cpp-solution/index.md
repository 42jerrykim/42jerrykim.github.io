---
title: "[Algorithm] cpp 백준 2912번: 백설공주와 난쟁이 - 세그트리+후보검증"
description: "세그먼트 트리로 Boyer–Moore 다수결(majority) 후보를 구간 병합으로 구하고, 색상별 위치 배열에 대한 이분탐색으로 실제 빈도를 검증합니다. 전처리 O(N), 질의 O(log N)로 제한을 만족합니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- "Algorithm"
- "Data Structures"
tags:
- "Algorithm"
- "알고리즘"
- "BOJ"
- "백준"
- "Problem-2912"
- "cpp"
- "C++"
- "Python"
- "Data Structures"
- "자료구조"
- "Implementation"
- "구현"
- "Time Complexity"
- "시간복잡도"
- "Space Complexity"
- "공간복잡도"
- "Proof of Correctness"
- "정당성 증명"
- "Edge Cases"
- "코너 케이스"
- "Pitfalls"
- "실수 포인트"
- "Optimization"
- "최적화"
- "Competitive Programming"
- "경쟁프로그래밍"
- "Editorial"
- "에디토리얼"
- "Code Review"
- "코드리뷰"
- "Template"
- "템플릿"
- "Testing"
- "테스트"
- "Complexity Analysis"
- "복잡도 분석"
- "Invariant"
- "불변식"
- "Greedy"
- "그리디"
- "Dynamic Programming"
- "동적계획법"
- "Graph"
- "그래프"
- "Tree"
- "트리"
- "BFS"
- "DFS"
- "Shortest Path"
- "최단경로"
- "Dijkstra"
- "다익스트라"
- "Bellman-Ford"
- "벨만포드"
- "Floyd-Warshall"
- "플로이드워셜"
- "Topological Sort"
- "위상정렬"
- "Segment Tree"
- "세그먼트 트리"
- "Fenwick Tree"
- "펜윅트리"
- "Disjoint Set Union"
- "유니온파인드"
- "Binary Search"
- "이분탐색"
- "Two Pointers"
- "투포인터"
- "Sliding Window"
- "슬라이딩윈도우"
- "Hashing"
- "해싱"
- "String"
- "문자열"
- "Geometry"
- "기하"
- "Math"
- "수학"
- "Modulo"
- "모듈러"
- "Implementation Details"
- "구현 디테일"
- "Debugging"
- "디버깅"
- "Majority Element"
- "Boyer-Moore"
- "Range Majority Query"
- "Range Query"
- "Occurrence Counting"
- "Index Map"
- "COCI"
- "백설공주와난쟁이"
- "Snow White"
- "난쟁이"
- "2912"
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/2912
- 요약: 길이 \(N\)의 모자 색 배열에서 구간 \([A,B]\)에 절반을 초과해 등장하는 색이 있는지, 있다면 그 색을 \(M\)개의 질의에 대해 판단합니다.
- 제한: \(N \le 3\times10^5\), \(C \le 10^4\), \(M \le 10^4\), 시간 1초

## 입력/출력
```
입력
N C
colors[1..N]
M
A B (M줄)

출력
각 질의에 대해, 다수색이 없으면 "no",
있으면 "yes X" (X는 다수색 번호)
```

## 접근 개요
- **핵심 아이디어**: 구간의 다수 원소(majority)는 Boyer–Moore 다수결의 법칙처럼, 후보와 카운트를 병합해도 후보가 유지됩니다. 이를 세그먼트 트리로 일반화하면, 구간 병합으로 후보를 빠르게 구할 수 있습니다.
- **검증 단계**: 후보가 실제로 절반을 초과하는지 확인하려면 색상별로 등장 위치를 저장해 두고, \([A,B]\)에서의 빈도를 이분탐색(lower/upper_bound)으로 계산합니다.
- **복잡도**: 빌드 \(O(N)\), 질의당 후보 추출 \(O(\log N)\) + 검증 \(O(\log N)\) → 전체 \(O((N+M)\log N)\).

## Mermaid로 보는 흐름
```mermaid
flowchart TD
    Q[Query [A,B]] --> ST[Segment Tree Query]
    ST --> Cand[Candidate (color,count)]
    Cand --> Verify[positions[color]로 빈도 이분탐색]
    Verify --> Decision{cnt > len/2?}
    Decision -- Yes --> YesOut["yes color"]
    Decision -- No --> NoOut["no"]
```

## 알고리즘 설계
- 세그먼트 트리 노드: `(color, count)`
  - 두 노드 병합:
    - 같으면 `(color, countL+countR)`
    - 다르면 더 큰 쪽 카운트에서 작은 쪽을 상쇄하여 후보 유지
    - 공집합 대용 `color=-1`
- 색상별 등장 위치 벡터 `positions[color]`에 인덱스들을 정렬 저장
- 질의 처리:
  1) 세그트리에서 후보색 `cand.color` 구하기
  2) `positions[cand.color]`에서 \([A,B]\) 빈도를 `upper_bound - lower_bound`로 계산
  3) `cnt > (B-A+1)/2`면 다수색

### 정당성 근거
- Boyer–Moore의 상쇄 법칙: 서로 다른 원소를 짝지어 제거해도 다수 원소(절반 초과)는 남습니다. 세그먼트 트리 병합은 이 상쇄를 구간 단위로 일반화하여 후보를 보존합니다.
- 후보의 실제 다수 여부는 위치 배열을 통한 정확한 빈도 계산으로 최종 검증됩니다.

## 복잡도
- 시간: 빌드 \(O(N)\), 질의당 \(O(\log N)\)
- 공간: 세그먼트 트리 \(O(N)\) + 위치 벡터 총합 \(O(N)\)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Node { int color; int count; };

Node mergeNode(const Node &L, const Node &R) {
    if (L.color == -1) return R;
    if (R.color == -1) return L;
    if (L.color == R.color) return {L.color, L.count + R.count};
    if (L.count > R.count) return {L.color, L.count - R.count};
    return {R.color, R.count - L.count};
}

int main(){ios::sync_with_stdio(false);cin.tie(nullptr);
    int N,C; if(!(cin>>N>>C)) return 0;
    vector<int> a(N+1);
    vector<vector<int>> pos(C+1);
    for(int i=1;i<=N;++i){cin>>a[i]; if(1<=a[i] && a[i]<=C) pos[a[i]].push_back(i);}    

    vector<Node> seg(4*N+4, {-1,0});
    function<void(int,int,int)> build = [&](int idx,int l,int r){
        if(l==r){ seg[idx]={a[l],1}; return; }
        int m=(l+r)>>1; build(idx<<1,l,m); build(idx<<1|1,m+1,r);
        seg[idx]=mergeNode(seg[idx<<1],seg[idx<<1|1]);
    };
    function<Node(int,int,int,int,int)> query = [&](int idx,int l,int r,int ql,int qr)->Node{
        if(qr<l||r<ql) return Node{-1,0};
        if(ql<=l && r<=qr) return seg[idx];
        int m=(l+r)>>1; Node L=query(idx<<1,l,m,ql,qr), R=query(idx<<1|1,m+1,r,ql,qr);
        return mergeNode(L,R);
    };
    auto countInRange = [&](const vector<int>& v, int L, int R){
        auto itL=lower_bound(v.begin(),v.end(),L);
        auto itR=upper_bound(v.begin(),v.end(),R);
        return (int)(itR-itL);
    };

    build(1,1,N);
    int M; cin>>M;
    while(M--){
        int A,B; cin>>A>>B; if(A>B) swap(A,B);
        Node cand=query(1,1,N,A,B);
        int color=cand.color; int len=B-A+1; int cnt=0;
        if(color!=-1 && 1<=color && color<=C) cnt=countInRange(pos[color],A,B);
        if(cnt>len/2) cout<<"yes "<<color<<'\n'; else cout<<"no\n";
    }
    return 0; }
```

## 코너 케이스 체크리스트
- 구간 길이 1인 경우
- 후보색이 `-1`로 반환되는 공집합 병합 경로
- 색상 범위를 벗어난 입력값 보호(검증 단계에서 범위 체크)
- 동일 구간 반복 질의, 전 구간 \([1,N]\) 질의

## 제출 전 점검
- 출력 형식과 개행 확인, `A>B` 입력 시 스왑 처리 여부
- 64-bit 오버플로 없음(인덱스/카운트는 `int`로 충분)
- 세그먼트 트리 인덱스, 경계, 병합 로직 재검토
- 위치 벡터에서 `lower_bound/upper_bound` 사용 범위 확인

## 참고자료
- Boyer–Moore Majority Vote: https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_majority_vote_algorithm
---

