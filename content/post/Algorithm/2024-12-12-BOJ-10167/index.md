---
title: "[Algorithm] C++ 백준 10167번 : 금광"
categories: 
- Algorithm
- Sweeping
- Segment-Tree
tags:
- SegmentTree
- CoordinateCompression
- MaximumSubarray
- Sweeping
- O(N² log N)
- DataStructure
- Geometry
- Optimization
image: "tmp_wordcloud.png"
date: 2024-12-12
---

금광 개발 문제를 다루는 백준 10167번 문제이다. 이 문제는 평면상에 주어진 금광들을 특정 직사각형 영역 안에 모두 포함시켰을 때의 이익(또는 손해)을 합산하고, 이 합이 최대가 되는 직사각형 영역을 찾는 문제이다. 직사각형의 변은 x축 또는 y축에 평행하도록 조건이 주어지고, 금광점 각각의 이익/손해 값이 주어진다. 이 문제는 모든 점을 포함할 수 있는 직사각형 중 최대 개발 이익을 내는 영역을 찾아야 하므로, 단순한 완전 탐색으로는 처리하기 어렵다. 본 글에서는 이 문제를 Segment Tree, 좌표 압축, 그리고 최대 부분합(Maximum Subarray) 알고리즘 등을 활용하여 효율적으로 해결하는 방법을 살펴본다.

문제 : [https://www.acmicpc.net/problem/10167](https://www.acmicpc.net/problem/10167)

## 문제 설명

이 문제는 "금광"에 관한 이야기이다. 황금의 땅으로 불리는 어떤 나라가 있고, 이 나라의 평면 상에는 아직 개발되지 않은 수많은 금광들이 점으로 존재한다고 한다. 각 금광은 (x, y) 좌표를 가지며, 해당 금광을 개발했을 때 얻는 이익 또는 손해값 w를 가지고 있다. w가 양수라면 그만큼 이익을, 음수라면 그만큼 손해를 뜻한다.

개발업자는 직사각형 모양의 땅 R을 사서 그 안에 포함된 모든 금광을 개발하고 싶어 한다. 직사각형 R의 변은 x, y축에 평행해야 하며, 그 안에 포함된 모든 금광들의 이익/손해 값을 합산한 것이 "개발 이익"이 된다. 개발업자의 목표는 개발 이익이 최대가 되는 직사각형 R을 찾는 것이다.

이 문제에서 주어진 입력은 다음과 같다.

- 금광의 개수 N (1 ≤ N ≤ 3,000)
- 각 금광의 좌표 (x, y), 그리고 이익 또는 손해 w (-10^9 ≤ w ≤ 10^9)
- 좌표 x, y는 0 ≤ x, y ≤ 10^9 범위를 가지며, w > 0인 금광이 최소 한 개 이상 존재한다.

출력은 최대 개발 이익을 나타내는 하나의 정수이다.

이 문제는 단순히 모든 사각형을 탐색하는 방식으로는 해결하기 어렵다. x좌표와 y좌표에 대한 범위가 매우 크고, 금광의 개수도 최대 3,000개이므로, 모든 가능한 사각형을 직접 그려보는 것은 비효율적이다. 따라서 이 문제의 핵심 포인트는 다음과 같다.

1. **좌표 압축(Coordinate Compression)**: x, y 좌표 범위가 최대 10^9이지만, 실제 금광의 개수는 3,000개이므로 실제 사용할 유효 좌표만 압축하면 된다.
2. **스위핑(Sweeping)**: x좌표를 기준으로 left 경계를 하나씩 이동시키면서, 이에 대해 right 경계를 움직여 [left, right] 구간에 해당하는 열(column)들을 고려한다.
3. **세그먼트 트리(Segment Tree)** 또는 **카데인(Kadane's) 알고리즘**: [left, right] 범위 내에서 y축에 대해 최대 부분합을 효율적으로 구하는 데이터 구조와 알고리즘을 사용한다.

개발 이익의 최대값을 찾기 위해서는:
- x좌표를 압축하고, x = left 부터 시작하여,
- right를 left 이상으로 증가시키며, 해당 [left, right] 범위에 있는 점들만을 고려한다.
- 이때, y축 방향으로 점들의 w값을 더한 뒤, 최대 부분합을 구한다.
- 이를 모든 (left, right) 쌍에 대해 반복하면, 그 중 최대값이 곧 문제의 답이 된다.

좌표 압축과 Segment Tree를 활용하면 O(N² log N) 정도로 해결할 수 있으며, 이는 N = 3,000 정도면 충분히 가능한 시간 내에 계산 가능한 수준이다.

## 접근 방식

1. **좌표 압축**: 점들의 x좌표와 y좌표를 각각 압축한다. 이렇게 하면 최대 3,000 정도의 유효좌표로 관리할 수 있다.
   
2. **열별로 점 정리**: 압축된 x좌표를 기준으로, 각 x열에 해당하는 점들을 묶어둔다. 각 점은 y좌표 인덱스와 w값을 갖는다.
   
3. **두 겹의 루프 (x 스위핑)**: 
   - 첫 번째 루프에서 left를 0부터 X-1까지 순회한다.
   - 두 번째 루프에서 right를 left부터 X-1까지 확장한다.
   
   각 단계에서 [left, right] 구간에 속한 모든 점들의 w값을 y좌표별로 합산한 뒤, 이 1차원 배열에 대해 최대 부분합을 구한다. 이는 세그먼트 트리를 이용하거나, 단순 Kadane 알고리즘으로도 가능하다. 다만 N이 3,000이므로 단순 Kadane를 사용하면 O(N³)가 되어 비효율적일 수 있으므로 세그먼트 트리와 같은 자료구조를 사용해 O(N² log N)으로 줄일 수 있다.
   
4. **세그먼트 트리를 이용한 최대 부분합 계산**:
   - 세그먼트 트리는 O(log N)에 구간 최대 부분합 갱신 및 질의를 수행할 수 있다.
   - 각 [left, right] 구간에 대해 y축 방향으로 sumArray를 업데이트하고, 세그먼트 트리에 반영해 최대 부분합을 구한다.

이러한 접근 방식으로 문제를 효율적으로 해결할 수 있다.

## C++ 코드와 설명

아래 코드는 C++로 구현한 예시이다. 좌표 압축 후, 세그먼트 트리를 사용하여 O(N² log N)에 문제를 해결하는 전략을 보여준다.

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Point {
    long long x, y, w;
};

struct Node {
    long long sum;
    long long prefix;
    long long suffix;
    long long maxSub;
};

static Node mergeNode(const Node &l, const Node &r) {
    Node ret;
    ret.sum = l.sum + r.sum;
    ret.prefix = max(l.prefix, l.sum + r.prefix);
    ret.suffix = max(r.suffix, r.sum + l.suffix);
    ret.maxSub = max({l.maxSub, r.maxSub, l.suffix + r.prefix});
    return ret;
}

static Node makeNode(long long val) {
    Node ret;
    ret.sum = val;
    ret.prefix = val;
    ret.suffix = val;
    ret.maxSub = val;
    return ret;
}

struct SegmentTree {
    int size;
    vector<Node> tree;

    SegmentTree(int n) {
        size = 1;
        while (size < n) size <<= 1;
        tree.assign(size*2, {0,-1000000000000000000LL,-1000000000000000000LL,-1000000000000000000LL});
        for (int i = size; i < size*2; i++) {
            tree[i] = makeNode(0);
        }
        for (int i = size-1; i >= 1; i--) {
            tree[i] = mergeNode(tree[i*2], tree[i*2+1]);
        }
    }

    void update(int pos, long long val) {
        pos += size;
        tree[pos] = makeNode(val);
        for (pos /= 2; pos > 0; pos /= 2) {
            tree[pos] = mergeNode(tree[pos*2], tree[pos*2+1]);
        }
    }

    Node query() {
        return tree[1];
    }

    void init_zero() {
        // 모든 노드를 0으로 초기화
        for (int i = 0; i < 2*size; i++) {
            tree[i].sum = 0;
            tree[i].prefix = -1000000000000000000LL;
            tree[i].suffix = -1000000000000000000LL;
            tree[i].maxSub = -1000000000000000000LL;
        }
        for (int i = size; i < size*2; i++) {
            tree[i] = makeNode(0);
        }
        for (int i = size-1; i >= 1; i--) {
            tree[i] = mergeNode(tree[i*2], tree[i*2+1]);
        }
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(NULL);

    int N; cin >> N;
    vector<Point> points(N);
    vector<long long> xs, ys;

    for (int i = 0; i < N; i++) {
        cin >> points[i].x >> points[i].y >> points[i].w;
        xs.push_back(points[i].x);
        ys.push_back(points[i].y);
    }

    // 좌표 압축
    sort(xs.begin(), xs.end());
    xs.erase(unique(xs.begin(), xs.end()), xs.end());
    sort(ys.begin(), ys.end());
    ys.erase(unique(ys.begin(), ys.end()), ys.end());

    for (auto &p : points) {
        p.x = (int)(lower_bound(xs.begin(), xs.end(), p.x) - xs.begin());
        p.y = (int)(lower_bound(ys.begin(), ys.end(), p.y) - ys.begin());
    }

    int X = (int)xs.size();
    int Y = (int)ys.size();

    // 각 x좌표별로 점 모으기
    vector<vector<pair<int,long long>>> cols(X);
    for (auto &p : points) {
        cols[p.x].push_back({p.y, p.w});
    }

    vector<long long> sumArray(Y, 0);
    SegmentTree seg(Y);
    long long ans = -1000000000000000000LL;

    // left를 고정하고 right를 확장하며 최대 부분합 탐색
    for (int left = 0; left < X; left++) {
        for (int i = 0; i < Y; i++) sumArray[i] = 0;
        seg.init_zero();

        for (int right = left; right < X; right++) {
            for (auto &pr : cols[right]) {
                int yidx = pr.first;
                sumArray[yidx] += pr.second;
                seg.update(yidx, sumArray[yidx]);
            }

            Node res = seg.query();
            ans = max(ans, res.maxSub);
        }
    }

    cout << ans << "\n";
    return 0;
}
```

### 코드 설명 (C++):

- **좌표 압축**: xs, ys 벡터를 정렬 후 중복 제거하여 각각 x, y 좌표를 압축한다.
- **cols 벡터 구성**: 각 압축된 x좌표에 해당하는 점들의 (y, w) 쌍을 cols[x]에 저장한다.
- **두 겹의 for문**: left, right 인덱스(압축한 x좌표 인덱스)를 활용해 [left, right] 범위의 열을 순회한다.
- **sumArray와 Segment Tree**: y축 방향으로 각 점의 w를 sumArray에 더하고, 그 값을 세그먼트 트리로 관리하여 최대 부분합을 구한다.
- 최종적으로 ans에는 최대 개발 이익값이 저장된다.

## C++ without library 코드와 설명

아래 코드는 stdio.h와 malloc.h만 사용 가능한 환경(예: BOJ 정규판)에서 동작하도록, 최소한의 STL 의존성을 없앤 버전의 예시이다. 동적 메모리 할당과 기본 C 표준 입출력을 사용한다. (실제 환경에서는 BOJ에서 C++14까지 stdio.h, iostream 모두 사용 가능하지만, 여기서는 의도대로 stdio.h, malloc.h만 사용한다고 가정한다.)

```cpp
#include <stdio.h>
#include <stdlib.h>

// 간단한 compare 함수
int cmp_ll(const void *a, const void *b) {
    long long A = *(long long*)a;
    long long B = *(long long*)b;
    if (A < B) return -1;
    else if (A > B) return 1;
    return 0;
}

typedef struct {
    long long x, y, w;
} Point;

typedef struct {
    long long sum, prefix, suffix, maxSub;
} Node;

#define INF (-1000000000000000000LL)

static Node mergeNode(Node l, Node r) {
    Node ret;
    ret.sum = l.sum + r.sum;
    ret.prefix = (l.prefix > l.sum + r.prefix) ? l.prefix : (l.sum + r.prefix);
    ret.suffix = (r.suffix > r.sum + l.suffix) ? r.suffix : (r.sum + l.suffix);
    // maxSub = max(l.maxSub, r.maxSub, l.suffix + r.prefix)
    long long temp_max = l.maxSub;
    if (r.maxSub > temp_max) temp_max = r.maxSub;
    long long cross = l.suffix + r.prefix;
    if (cross > temp_max) temp_max = cross;
    ret.maxSub = temp_max;
    return ret;
}

static Node makeNode(long long val) {
    Node ret;
    ret.sum = val;
    ret.prefix = val;
    ret.suffix = val;
    ret.maxSub = val;
    return ret;
}

typedef struct {
    int size;
    Node* tree;
} SegmentTree;

static void seg_init(SegmentTree* seg, int n) {
    seg->size = 1;
    while (seg->size < n) seg->size <<= 1;
    seg->tree = (Node*)malloc(sizeof(Node)*seg->size*2);
    for (int i = 0; i < seg->size*2; i++) {
        seg->tree[i].sum = 0;
        seg->tree[i].prefix = INF;
        seg->tree[i].suffix = INF;
        seg->tree[i].maxSub = INF;
    }
    for (int i = seg->size; i < seg->size*2; i++) {
        seg->tree[i] = makeNode(0);
    }
    for (int i = seg->size-1; i >= 1; i--) {
        seg->tree[i] = mergeNode(seg->tree[i*2], seg->tree[i*2+1]);
    }
}

static void seg_update(SegmentTree* seg, int pos, long long val) {
    pos += seg->size;
    seg->tree[pos] = makeNode(val);
    for (pos /= 2; pos > 0; pos /= 2) {
        seg->tree[pos] = mergeNode(seg->tree[pos*2], seg->tree[pos*2+1]);
    }
}

static void seg_init_zero(SegmentTree* seg) {
    for (int i = 0; i < seg->size*2; i++) {
        seg->tree[i].sum = 0;
        seg->tree[i].prefix = INF;
        seg->tree[i].suffix = INF;
        seg->tree[i].maxSub = INF;
    }
    for (int i = seg->size; i < seg->size*2; i++) {
        seg->tree[i] = makeNode(0);
    }
    for (int i = seg->size-1; i >= 1; i--) {
        seg->tree[i] = mergeNode(seg->tree[i*2], seg->tree[i*2+1]);
    }
}

int main() {
    int N; 
    scanf("%d", &N);
    Point* points = (Point*)malloc(sizeof(Point)*N);
    long long* xs = (long long*)malloc(sizeof(long long)*N);
    long long* ys = (long long*)malloc(sizeof(long long)*N);

    for (int i = 0; i < N; i++) {
        scanf("%lld %lld %lld", &points[i].x, &points[i].y, &points[i].w);
        xs[i] = points[i].x;
        ys[i] = points[i].y;
    }

    // 좌표 압축
    qsort(xs, N, sizeof(long long), cmp_ll);
    int xlen = 0;
    for (int i = 0; i < N; i++) {
        if (i == 0 || xs[i] != xs[i-1]) {
            xs[xlen++] = xs[i];
        }
    }

    qsort(ys, N, sizeof(long long), cmp_ll);
    int ylen = 0;
    for (int i = 0; i < N; i++) {
        if (i == 0 || ys[i] != ys[i-1]) {
            ys[ylen++] = ys[i];
        }
    }

    for (int i = 0; i < N; i++) {
        long long *px = (long long*)bsearch(&points[i].x, xs, xlen, sizeof(long long), cmp_ll);
        long long *py = (long long*)bsearch(&points[i].y, ys, ylen, sizeof(long long), cmp_ll);
        int xi = (int)(px - xs);
        int yi = (int)(py - ys);
        points[i].x = xi;
        points[i].y = yi;
    }

    // cols 만들기
    // cols를 동적 할당: 최대 xlen개, 각에 대해 N개 점 가능
    // 인덱스와 개수를 관리해줘야 함
    int* colCount = (int*)calloc(xlen, sizeof(int));
    for (int i = 0; i < N; i++) colCount[points[i].x]++;
    int** colY = (int**)malloc(sizeof(int*)*xlen);
    long long** colW = (long long**)malloc(sizeof(long long*)*xlen);
    for (int i = 0; i < xlen; i++) {
        colY[i] = (int*)malloc(sizeof(int)*colCount[i]);
        colW[i] = (long long*)malloc(sizeof(long long)*colCount[i]);
    }
    for (int i = 0; i < xlen; i++) colCount[i] = 0;
    for (int i = 0; i < N; i++) {
        int cx = (int)points[i].x;
        int idx = colCount[cx]++;
        colY[cx][idx] = (int)points[i].y;
        colW[cx][idx] = points[i].w;
    }

    // sumArray
    long long* sumArray = (long long*)malloc(sizeof(long long)*ylen);
    for (int i = 0; i < ylen; i++) sumArray[i] = 0;

    SegmentTree seg;
    seg_init(&seg, ylen);
    long long ans = INF;

    for (int left = 0; left < xlen; left++) {
        for (int i = 0; i < ylen; i++) sumArray[i] = 0;
        seg_init_zero(&seg);

        for (int right = left; right < xlen; right++) {
            // cols[right] 반영
            for (int idx = 0; idx < colCount[right]; idx++) {
                int yidx = colY[right][idx];
                sumArray[yidx] += colW[right][idx];
                seg_update(&seg, yidx, sumArray[yidx]);
            }

            Node res = seg.tree[1];
            if (res.maxSub > ans) ans = res.maxSub;
        }
    }

    printf("%lld\n", ans);

    // 메모리 해제
    for (int i = 0; i < xlen; i++) {
        free(colY[i]);
        free(colW[i]);
    }
    free(colY);
    free(colW);
    free(colCount);
    free(points);
    free(xs);
    free(ys);
    free(sumArray);
    free(seg.tree);

    return 0;
}
```

### 코드 설명 (C++ without library):

- 표준 라이브러리를 최소화하고, bsearch, qsort 등을 사용하여 좌표 압축을 수행한다.
- Segment Tree 또한 직접 구현하여 최대 부분합을 관리한다.
- sumArray를 업데이트하고 seg_update를 호출하며, [left, right] 구간에 대한 최대 부분합을 지속적으로 추적한다.

## 결론

백준 10167번 "금광" 문제는 평면상 점들을 대상으로 하는 최대 부분합 문제의 변형으로, 좌표 압축, 스위핑, 세그먼트 트리(또는 고급 자료구조) 등을 종합적으로 활용해야 하는 문제이다. 단순한 완전탐색으로 접근하기는 어렵고, O(N² log N) 정도의 알고리즘을 구현해야 시간 내에 해결 가능하다.

본 글에서는 C++, 그리고 라이브러리 최소화를 가정한 C++ 코드 예시까지 제시하였다. 최적화 기법으로는 세그먼트 트리를 통한 최대 부분합 계산과 좌표 압축을 활용하였으며, 이를 통해 문제를 효율적으로 해결하였다. 이 문제를 통해, 고난도의 2차원 최대 부분합 문제를 푸는 방법에 대한 경험과, 세그먼트 트리를 최대 부분합 계산용으로 확장하는 방법, 그리고 좌표 압축과 스위핑 기법을 실전 문제에 적용하는 방법을 익힐 수 있다.  
```
