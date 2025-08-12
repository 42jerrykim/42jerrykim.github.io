---
title: "[Algorithm] BOJ 17442 - 삼분 그래프 - 듀얼 그래프+2D 질의 C++"
description: "평면 그래프에 두 수직선 x=A, x=B를 그어 그래프를 삼분할할 때 조각 수를 구한다. 오일러 공식 ΔC=ΔV−ΔE+ΔF와 듀얼 그래프로 각 면의 x-범위를 구해 2D 질의로 ΔF(잘리는 면 수)를 세고, ΔE는 간선 교차수 누적으로 계산한다. 외부 면을 제외해 정확히 세며, 전체는 O((N+M)logN + Qlog^2N)로 처리하는 C++ 풀이."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "Algorithm"
- "BOJ"
tags:
- "BOJ"
- "Baekjoon"
- "백준"
- "17442"
- "삼분 그래프"
- "Three Minute Graph"
- "Planar Graph"
- "평면 그래프"
- "Dual Graph"
- "듀얼 그래프"
- "Euler Formula"
- "오일러 공식"
- "Connected Components"
- "연결 성분"
- "Faces"
- "면"
- "Edge Split"
- "간선 분할"
- "Vertical Line Cuts"
- "수직선 절단"
- "Inclusion-Exclusion"
- "포함 배제"
- "Merge Sort Tree"
- "머지 소트 트리"
- "Segment Tree"
- "세그먼트 트리"
- "2D Range Query"
- "2D 질의"
- "Range Counting"
- "범위 카운팅"
- "Coordinate Compression"
- "좌표 압축"
- "Angle Sort"
- "각 정렬"
- "CCW"
- "외적"
- "Union-Find"
- "DSU"
- "Disjoint Set Union"
- "자료구조"
- "Data Structure"
- "Graph Algorithms"
- "그래프 알고리즘"
- "Geometry"
- "기하"
- "Offline Query"
- "오프라인 질의"
- "Complexity"
- "시간복잡도"
- "Space Complexity"
- "공간복잡도"
- "C++"
- "CPP"
- "GNU++17"
- "Fast IO"
- "빠른 입출력"
- "Implementation"
- "구현"
- "Debugging"
- "디버깅"
- "Competitive Programming"
- "CP"
- "ICPC"
- "SNUPC"
- "SNU"
- "서울대학교"
image: "featured-image.jpg"
draft: true
---

백준 문제 [삼분 그래프 (17442)](https://www.acmicpc.net/problem/17442)의 C++ 풀이를 정리합니다. 평면 그래프에 수직선 `x=A`, `x=B`로 절단을 가하면, 정의에 따라 교점에서 간선을 둘로 나누고 각 끝에 새 정점을 추가합니다. 목표는 잘린 뒤 연결 성분(조각) 수를 구하는 것입니다.

### 핵심 아이디어
- 평면 그래프에서는 오일러 공식이 성립: \(V - E + F = C + 1\). 변화량으로 보면 \(\Delta C = \Delta V - \Delta E + \Delta F\).
- 한 수직선이 간선을 한 번 지날 때마다 간선은 1개 증가, 정점은 2개 증가하므로, 두 직선을 함께 보면 \(\Delta V = 2\Delta E\)가 되어 \(\Delta C = \Delta E + \Delta F\).
- 여기서 \(\Delta F\)는 "잘리는 면의 수"에 대해 음수이므로 최종 성분 수는 `1 + ΔE − (잘리는 면 수)`.
- `ΔE` 계산: 모든 간선의 `x` 구간 `[min(x_u,x_v), max(x_u,x_v))`에 대해 차분 배열을 두고, `A`, `B`에서 누적값을 더한다.
- `ΔF` 계산: 듀얼 그래프 관점에서 각 면의 `x`-범위를 `[L, R]`로 구한 뒤, 2D 자료구조(머지 소트 트리)로
  - `A`를 포함하는 면: `L ≤ A ≤ R` → 점 `(L,R)` 중 `L ∈ [1..A]` and `R ∈ [A..∞]`
  - `B`를 포함하는 면: `L ≤ B ≤ R`
  - 두 선 모두 포함: `L ≤ A` and `R ≥ B`
  를 세어 포함배제로 `faces(A ∪ B) = faces(A) + faces(B) − faces(A ∩ B)`를 얻는다. 외부 면은 제외한다.

### 구현 메모
- 각 꼭짓점 기준으로 인접 간선을 각도 정렬하고, 반엣지(half-edge)를 이어 DSU로 면을 결합해 `[L,R]` 범위를 합친다.
- 외부 면은 가장 왼쪽-아래 정점에서 시작한 특정 반엣지로 판별한다(정렬된 첫 이웃의 반엣지의 오른쪽 면).
- 좌표 압축은 `x-1, x, x+1`를 함께 넣어 "엄밀한 [L,R) 처리"와 수직선 인덱싱을 안전하게 한다.

### C++ 정답 코드

```cpp
// 더 많은 정보는 42jerrykim.github.io에서 확인하세요.
// For more information, visit https://42jerrykim.github.io

#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct Point { ll x, y; };

struct DSU {
  vector<int> p; vector<ll> minX, maxX;
  DSU(int n): p(n), minX(n, (ll)4e18), maxX(n, -(ll)4e18) { iota(p.begin(), p.end(), 0); }
  int find(int v){ return p[v]==v? v : p[v]=find(p[v]); }
  void set_init(int i, ll L, ll R){ minX[i]=min(minX[i],L); maxX[i]=max(maxX[i],R); }
  void unite(int a, int b){ a=find(a); b=find(b); if(a==b) return; p[a]=b; minX[b]=min(minX[b],minX[a]); maxX[b]=max(maxX[b],maxX[a]); }
};

struct MergeSortTree2D {
  int base; vector<vector<int>> t;
  explicit MergeSortTree2D(int n=0){ init(n); }
  void init(int n){ base=1; while(base<n+2) base<<=1; t.assign(base<<1,{}); }
  void add_point(int Lidx,int Ridx){ t[Lidx+base].push_back(Ridx); }
  void build(){
    for(int i=base;i<base*2;i++) if(t[i].size()>1) sort(t[i].begin(),t[i].end());
    for(int i=base-1;i>=1;i--){
      auto &L=t[i<<1], &R=t[i<<1|1], &T=t[i];
      T.resize(L.size()+R.size());
      merge(L.begin(),L.end(),R.begin(),R.end(),T.begin());
    }
  }
  int query(int l,int r,int Lq,int Rq)const{
    if(l>r||Lq>Rq) return 0; l+=base-1; r+=base-1; int ans=0;
    while(l<=r){
      if(l&1){ const auto &v=t[l]; ans+=int(upper_bound(v.begin(),v.end(),Rq)-lower_bound(v.begin(),v.end(),Lq)); l++; }
      if(!(r&1)){ const auto &v=t[r]; ans+=int(upper_bound(v.begin(),v.end(),Rq)-lower_bound(v.begin(),v.end(),Lq)); r--; }
      l>>=1; r>>=1;
    }
    return ans;
  }
};

int n,m,q;
vector<Point> pt;
vector<vector<pair<int,int>>> adj; // (neighbor, edgeId)

int ccw(const Point&a,const Point&b,const Point&c){
  long long dx1=b.x-a.x, dy1=b.y-a.y; long long dx2=c.x-b.x, dy2=c.y-b.y; long long v=dx1*dy2-dx2*dy1;
  return v>0?1:(v<0?-1:0);
}
inline bool rightHalf(const Point&p,const Point&base){ if(p.x!=base.x) return p.x>base.x; return p.y>base.y; }
Point BASE;
bool cmp_angle(const pair<int,int>&A,const pair<int,int>&B){
  const Point &a=pt[A.first], &b=pt[B.first]; bool ha=rightHalf(a,BASE), hb=rightHalf(b,BASE);
  if(ha!=hb){ if(a.x!=b.x) return a.x>b.x; return a.y>b.y; }
  return ccw(a,BASE,b)>0;
}

int main(){
  ios::sync_with_stdio(false); cin.tie(nullptr);

  cin>>n>>m>>q; pt.assign(n+1,{});
  for(int i=1;i<=n;i++) cin>>pt[i].x>>pt[i].y;

  adj.assign(n+1,{}); vector<pair<int,int>> edges(m+1);
  for(int i=1;i<=m;i++){ int u,v; cin>>u>>v; edges[i]={u,v}; adj[u].push_back({v,i}); adj[v].push_back({u,i}); }

  // x compression (include x-1, x, x+1)
  vector<ll> comp; comp.reserve(3*n+10);
  for(int i=1;i<=n;i++){ comp.push_back(pt[i].x-1); comp.push_back(pt[i].x); comp.push_back(pt[i].x+1); }
  sort(comp.begin(),comp.end()); comp.erase(unique(comp.begin(),comp.end()),comp.end());
  auto idxOf=[&](ll x){ return int(lower_bound(comp.begin(),comp.end(),x)-comp.begin())+1; };
  int C=(int)comp.size();

  // ΔE: range add on [L, R)
  vector<int> pref(C+5,0);
  for(int i=1;i<=m;i++){
    auto [u,v]=edges[i]; ll L=min(pt[u].x,pt[v].x), R=max(pt[u].x,pt[v].x);
    int a=idxOf(L), b=idxOf(R); if(a<b){ pref[a]++; pref[b]--; }
  }
  for(size_t i=1;i<pref.size();i++) pref[i]+=pref[i-1];

  // Dual faces via DSU on half-edges
  DSU dsu(2*m+5);
  for(int i=1;i<=m;i++){
    auto [u,v]=edges[i]; ll L=min(pt[u].x,pt[v].x), R=max(pt[u].x,pt[v].x);
    dsu.set_init(i<<1,L,R); dsu.set_init(i<<1|1,L,R);
  }

  for(int i=1;i<=n;i++){
    BASE=pt[i]; auto &g=adj[i]; sort(g.begin(),g.end(),[&](const auto& A,const auto& B){ return cmp_angle(A,B); });
    int sz=(int)g.size();
    for(int j=0;j<sz;j++){
      int k=(j? j-1 : sz-1); int he_u=(g[k].second<<1)|1; int he_v=(g[j].second<<1);
      const Point &p1=pt[g[k].first], &p2=pt[g[j].first]; if(rightHalf(p1,BASE)) he_u^=1; if(rightHalf(p2,BASE)) he_v^=1; dsu.unite(he_u,he_v);
    }
  }

  // outer face
  int mn=1; for(int i=2;i<=n;i++) if(pt[i].x<pt[mn].x || (pt[i].x==pt[mn].x && pt[i].y<pt[mn].y)) mn=i;
  int outer = dsu.find((adj[mn][0].second<<1)|1);

  // collect inner faces [L,R]
  vector<pair<ll,ll>> faces; faces.reserve(2*m); unordered_set<int> seen; seen.reserve(2*m+7);
  for(int he=0; he<=(m<<1|1); he++){ int r=dsu.find(he); if(r==outer) continue; if(seen.insert(r).second) faces.push_back({dsu.minX[r], dsu.maxX[r]}); }

  // build 2D structure
  MergeSortTree2D mst(C+3);
  for(auto [Lval,Rval]:faces){ int Lidx=idxOf(Lval), Ridx=idxOf(Rval); mst.add_point(Lidx,Ridx); }
  mst.build();

  // answer queries: 1 + ΔE − ΔF, where ΔF = #(faces hit by A or B) over inner faces
  const int INF_R = C+2;
  while(q--){
    ll A,B; cin>>A>>B; int a=idxOf(A), b=idxOf(B);
    int dE = pref[a] + pref[b];
    int fA = mst.query(1,a, a,INF_R);
    int fB = mst.query(1,b, b,INF_R);
    int fAB= mst.query(1,a, b,INF_R);
    int dF = fA + fB - fAB; // faces hit by A or B (outer excluded)
    cout << (1 + dE - dF) << '\n';
  }
  return 0;
}
```

### 복잡도
- 빌드(듀얼·정렬·압축): `O((N+M) log N)`
- 질의: 각 `O(log^2 N)` → 전체 `O(Q log^2 N)`

### 참고
- 아이디어 정리: [JusticeHui 블로그 - BOJ17442](https://justicehui.github.io/ps/2020/08/09/BOJ17442/)


