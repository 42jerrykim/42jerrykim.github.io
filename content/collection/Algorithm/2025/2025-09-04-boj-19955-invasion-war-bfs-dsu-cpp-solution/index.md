---
title: "[Algorithm] cpp 백준 19955번: 침략전쟁 - BFS·DSU 시뮬레이션"
description: "격자 기반 전쟁을 날짜별 페이즈(전략→전투→징집→확장)로 모델링하고, 다중 시작 BFS로 확장을 레이어 단위 1회만 처리하며, 전투는 DSU로 비수도 영토를 일괄 이관하고 징집은 날짜별 지연 갱신으로 정확히 반영하는 고효율 풀이입니다."
date: 2025-09-04
lastmod: 2025-09-04
categories:
- Algorithm
- Graph
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-19955
- cpp
- C++
- Simulation
- 시뮬레이션
- Graph
- 그래프
- Grid
- 격자
- BFS
- 다중시작BFS
- Multi-Source BFS
- Shortest Path
- 최단경로
- DSU
- Disjoint Set Union
- Union-Find
- 유니온파인드
- Lazy Update
- 지연갱신
- Event Processing
- 이벤트처리
- Layered Expansion
- 레이어확장
- Tie-breaking
- 타이브레이크
- Territory Expansion
- 영토확장
- Battle Simulation
- 전투시뮬레이션
- Recruitment
- 징집
- Time Management
- 시간관리
- Temporal Logic
- 시간논리
- State Machine
- 상태머신
- Offline Processing
- 오프라인처리
- O(N^2)
- 시간복잡도
- Space Complexity
- 공간복잡도
- Correctness Proof
- 정당성증명
- Edge Cases
- 코너케이스
- Pitfalls
- 실수포인트
- Optimization
- 최적화
- Competitive Programming
- 경쟁프로그래밍
- Implementation
- 구현
- Data Structures
- 자료구조
- Grid Graph
- 그래프탐색
- Invariant
- 불변식
- Large Input
- 대용량입력
- Fast IO
- 빠른입출력
- C++17
- Template
- 템플릿
image: "wordcloud.png"
---

## 문제 정보
- 링크: https://www.acmicpc.net/problem/19955
- 요약: N×N 격자에서 여러 국가가 날짜별로 전투·징집·확장 단계를 거칩니다. 실시간 쿼리로 (1) 전투 수행과 (2) 특정 국가 병력 조회를 처리합니다. 게임은 0일의 징집단계부터 시작합니다.
- 제한: N ≤ 2000, M ≤ min(N², 1,000,000), Q ≤ 1,000,000, t ≤ 1e9

## 입출력 형식/예제
- 입력: 초기 M개 국가의 수도 좌표와 병력, 이어서 Q개의 쿼리(전투/조회)
- 출력: 2번(조회) 쿼리마다 해당 국가의 병력을 한 줄에 출력

예제(문제 원문 참고):
```text
3 2 3
1 1 5
3 3 2
2 2 1
1 1 1 4
1 1 3 3
2 7 1 1
```

## 접근 개요
- 확장(자동전투): 수도들을 모두 시작점으로 하는 multi-source BFS로 각 칸의 최초 도달 거리 `dist`를 구하고, day = dist-1 레이어별로 단 한 번씩만 확장 처리합니다. 같은 날에 방금 점령된 칸은 후보로 사용하지 않습니다.
- 전투: t일 전투단계에서 두 국가의 병력(전날까지 반영)만 비교합니다. 승자는 병력 차만큼 남고, 패자는 0이 되며 비수도 영토 전체가 승자에게 귀속됩니다(수도는 유지). 비수도 영토의 대량 이관은 DSU 루트 소유자 갱신으로 O(α)에 처리합니다.
- 징집: 각 날 시작 시점의 영토 수만큼 병력이 증가합니다. 국가별 `lastUpdDay`로 병력을 지연 갱신하며, 오늘 징집 반영 여부에 따라 비교값을 정확히 계산합니다.
- 확장 동률 규칙: 오늘 징집 반영 후 병력이 큰 국가가 점령하며, 병력까지 같으면 국가 번호 A×N+B(수도 좌표 기준)가 작은 국가가 우선합니다.

## 알고리즘 설계
1) dist 계산: 수도들을 큐에 넣고 4방향 BFS. 각 칸의 dist는 해당 칸이 처음으로 접하는 거리.
2) 레이어 확장(day): day = dist-1인 칸들을 처리. 이웃 중 dist ≤ day인 칸들의 소유국만 후보로 삼아, "오늘 징집 후 병력"을 비교하여 승자를 결정. 승자에 한해 오늘 징집을 실제 1회 반영 후 칸 귀속. 새 영토는 다음 날부터 징집량에 반영.
3) 전투 처리(t): t-1일까지 병력을 당겨 비교 → 승패 결정 → DSU로 패자의 비수도 영토 일괄 이관 → 그날(t)의 징집을 (새 영토수 기준으로) 반영.
4) 지연 갱신: `ensureUpdateToEndOfDay(country, day)`로 전날 또는 오늘 시점까지 필요한 경우에만 누적 반영.

## 복잡도
- 시간: O(N²) = BFS + 각 칸 1회 확장 결정, 쿼리 당 O(α) 상수에 가까운 DSU 연산 포함
- 공간: O(N²) + O(M)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct DSU {
    vector<int> parent, sz, owner; // root -> current owning country id
    int new_label(int owner_country) {
        int id = (int)parent.size();
        parent.push_back(id);
        sz.push_back(0);
        owner.push_back(owner_country);
        return id;
    }
    int find(int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }
    void merge_to(int winner_root, int loser_root, int winner_country) {
        if (winner_root == loser_root) return;
        parent[loser_root] = winner_root;
        sz[winner_root] += sz[loser_root];
        owner[winner_root] = winner_country;
    }
};

static const int INF_INT = 0x3f3f3f3f;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, M, Qn;
    if (!(cin >> N >> M >> Qn)) return 0;

    const int total_cells = N * N;

    vector<int> capX(M), capY(M);
    vector<long long> soldiers(M, 0);
    vector<long long> territoryCount(M, 1); // includes capital
    vector<int> lastUpdDay(M, -1);          // last day applied to soldiers (end-of-day)
    vector<long long> tieKey(M);            // A*N + B (A=x, B=y), smaller wins on tie

    auto posId = [&](int x, int y) -> int { return (x - 1) * N + (y - 1); };

    for (int i = 0; i < M; ++i) {
        int x, y, k; cin >> x >> y >> k;
        capX[i] = x; capY[i] = y; soldiers[i] = k;
        tieKey[i] = 1LL * x * N + y;
    }

    struct Query {
        int type, t;
        int xa, ya, xb, yb; // type 1
        int xc, yc;         // type 2
    };
    vector<Query> queries(Qn);
    for (int i = 0; i < Qn; ++i) {
        int tp; cin >> tp;
        if (tp == 1) {
            int t, xa, ya, xb, yb; cin >> t >> xa >> ya >> xb >> yb;
            queries[i] = {1, t, xa, ya, xb, yb, 0, 0};
        } else {
            int t, xc, yc; cin >> t >> xc >> yc;
            queries[i] = {2, t, 0,0,0,0, xc, yc};
        }
    }

    // Multi-source BFS from capitals to get earliest reach day
    vector<int> dist(total_cells, INF_INT);
    deque<int> dq;
    for (int i = 0; i < M; ++i) {
        int pid = posId(capX[i], capY[i]);
        dist[pid] = 0;
        dq.push_back(pid);
    }
    const int dx[4] = {-1, 1, 0, 0};
    const int dy[4] = {0, 0, -1, 1};
    while (!dq.empty()) {
        int cur = dq.front(); dq.pop_front();
        int cx = cur / N, cy = cur % N;
        for (int d = 0; d < 4; ++d) {
            int nx = cx + dx[d], ny = cy + dy[d];
            if ((unsigned)nx >= (unsigned)N || (unsigned)ny >= (unsigned)N) continue;
            int nid = nx * N + ny;
            if (dist[nid] == INF_INT) {
                dist[nid] = dist[cur] + 1;
                dq.push_back(nid);
            }
        }
    }

    int maxDay = 0;
    for (int id = 0; id < total_cells; ++id) {
        if (dist[id] > 0 && dist[id] < INF_INT) {
            maxDay = max(maxDay, dist[id] - 1); // first claim day = dist-1
        }
    }
    vector<vector<int>> cellsByDay(maxDay + 1);
    for (int id = 0; id < total_cells; ++id) {
        if (dist[id] > 0 && dist[id] < INF_INT) {
            cellsByDay[dist[id] - 1].push_back(id);
        }
    }

    // Ownership grid: capitals are encoded as -1 - countryId; non-cap cells store DSU label id >= 0
    const int UNASSIGNED = INT_MIN;
    vector<int> ownerLabel(total_cells, UNASSIGNED);
    for (int i = 0; i < M; ++i) {
        ownerLabel[posId(capX[i], capY[i])] = -1 - i;
    }

    // DSU for non-capital territories; each country maintains a current label for all its non-cap cells
    DSU dsu;
    dsu.parent.reserve((size_t)M + 1024);
    dsu.sz.reserve((size_t)M + 1024);
    dsu.owner.reserve((size_t)M + 1024);

    vector<int> nonCapLabelId(M);
    for (int i = 0; i < M; ++i) nonCapLabelId[i] = dsu.new_label(i);

    auto getOwnerCountryAtPid = [&](int pid) -> int {
        int lbl = ownerLabel[pid];
        if (lbl == UNASSIGNED) return -1;
        if (lbl < 0) return -1 - lbl;        // capital
        int root = dsu.find(lbl);
        return dsu.owner[root];              // current owner country id
    };

    auto ensureUpdateToEndOfDay = [&](int country, int targetDay) {
        int &last = lastUpdDay[country];
        if (targetDay > last) {
            long long days = (long long)targetDay - (long long)last;
            soldiers[country] += territoryCount[country] * days;
            last = targetDay;
        }
    };

    auto strengthAfterRecruitOfDay = [&](int country, int day) -> long long {
        // Ensure up to previous day is applied
        ensureUpdateToEndOfDay(country, day - 1);
        // If today already applied, return current soldiers
        if (lastUpdDay[country] >= day) return soldiers[country];
        // Else, today after recruitment = prev soldiers + current territory count
        return soldiers[country] + territoryCount[country];
    };

    auto battle = [&](int t, int aIdx, int bIdx) {
        if (aIdx == bIdx) return;

        // Use end-of-day (t-1) soldiers for comparison
        ensureUpdateToEndOfDay(aIdx, t - 1);
        ensureUpdateToEndOfDay(bIdx, t - 1);

        if (soldiers[aIdx] == soldiers[bIdx]) return;

        int winner = (soldiers[aIdx] > soldiers[bIdx]) ? aIdx : bIdx;
        int loser  = (winner == aIdx ? bIdx : aIdx);

        long long newWinSold = soldiers[winner] - soldiers[loser];
        soldiers[winner] = newWinSold;
        soldiers[loser] = 0;

        // Transfer ALL non-cap territories of loser to winner
        int loserRoot = dsu.find(nonCapLabelId[loser]);
        int winnerRoot = dsu.find(nonCapLabelId[winner]);
        if (loserRoot != winnerRoot) {
            int transfer = dsu.sz[loserRoot];
            if (transfer > 0) {
                dsu.merge_to(winnerRoot, loserRoot, winner);
                territoryCount[winner] += transfer;
                territoryCount[loser]  -= transfer; // becomes 1 if all non-caps moved
            }
        }
        // Loser gets fresh empty label for future expansions
        nonCapLabelId[loser] = dsu.new_label(loser);

        // Apply day t recruitment immediately (post-battle territory counts)
        ensureUpdateToEndOfDay(winner, t);
        ensureUpdateToEndOfDay(loser, t);
    };

    auto processExpansionDay = [&](int day) {
        for (int cid : cellsByDay[day]) {
            int cx = cid / N, cy = cid % N;

            int cand[4], cnt = 0;
            for (int d = 0; d < 4; ++d) {
                int nx = cx + dx[d], ny = cy + dy[d];
                if ((unsigned)nx >= (unsigned)N || (unsigned)ny >= (unsigned)N) continue;
                int nid = nx * N + ny;

                // Only neighbors already owned by end of previous day (avoid same-day chaining)
                if (dist[nid] == INF_INT || dist[nid] > day) continue;

                int oc = getOwnerCountryAtPid(nid);
                bool seen = false;
                for (int i = 0; i < cnt; ++i) if (cand[i] == oc) { seen = true; break; }
                if (!seen) cand[cnt++] = oc;
            }

            if (cnt == 0) continue;

            int bestCountry = -1;
            long long bestVal = LLONG_MIN;
            for (int i = 0; i < cnt; ++i) {
                int c = cand[i];
                long long val = strengthAfterRecruitOfDay(c, day); // soldiers after today's recruitment
                if (bestCountry == -1 || val > bestVal ||
                    (val == bestVal && tieKey[c] < tieKey[bestCountry])) {
                    bestVal = val;
                    bestCountry = c;
                }
            }
            if (bestCountry < 0) continue;

            // Ensure winner has today's recruitment actually applied once
            ensureUpdateToEndOfDay(bestCountry, day);

            // Assign this cell to winner's current non-cap label
            ownerLabel[cid] = nonCapLabelId[bestCountry];
            int root = dsu.find(nonCapLabelId[bestCountry]);
            dsu.sz[root] += 1;

            // This new territory contributes starting from next day
            territoryCount[bestCountry] += 1;
        }
    };

    auto advanceToEndOfDay = [&](int &curDay, int targetDay) {
        for (int d = curDay + 1; d <= targetDay; ++d) {
            if (d >= 0 && d <= maxDay) processExpansionDay(d);
            curDay = d;
        }
    };

    int curDay = -1; // we maintain state as of end-of-day curDay
    ostringstream out;

    for (const auto &q : queries) {
        if (q.type == 2) {
            int t = q.t;
            if (curDay < t - 1) {
                int target = min(t - 1, maxDay);
                advanceToEndOfDay(curDay, target);
                if (curDay < t - 1) curDay = t - 1;
            }
            int country = getOwnerCountryAtPid(posId(q.xc, q.yc)); // guaranteed to exist
            ensureUpdateToEndOfDay(country, t - 1);
            out << soldiers[country] << '\n';
        } else {
            int t = q.t;
            if (curDay < t - 1) {
                int target = min(t - 1, maxDay);
                advanceToEndOfDay(curDay, target);
                if (curDay < t - 1) curDay = t - 1;
            }
            int a = getOwnerCountryAtPid(posId(q.xa, q.ya));
            int b = getOwnerCountryAtPid(posId(q.xb, q.yb));
            battle(t, a, b);

            if (curDay < t) {
                int target = min(t, maxDay);
                advanceToEndOfDay(curDay, target);
                if (curDay < t) curDay = t;
            }
        }
    }

    cout << out.str();
    return 0;
}
```

## 코너 케이스 체크리스트
- 같은 날 확장에서 "방금 점령된 칸"을 후보로 사용하지 않음(dist > day 제외)
- 전투 동률 무효, 승자 병력 = 승자−패자, 패자는 0
- 비수도 영토 전체 이관에서 수도는 유지, DSU 소유자만 갱신
- 전투(t) → 징집(t) → 확장(t) 순서 보장, 비교값은 "오늘 징집 후" 기준
- 매우 큰 t에서도 일일 시뮬 없이 레이어·이벤트 기반으로만 갱신

## 참고자료/유사문제
- 인하대학교 2020 IGRUS Newbie Programming Contest L

