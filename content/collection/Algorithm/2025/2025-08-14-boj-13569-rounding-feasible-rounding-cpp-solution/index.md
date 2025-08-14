---
title: "[Algorithm] cpp 백준 13569번: Rounding - 표 합계 보존 반올림"
description: "소수 첫째 자리로 기록된 표의 각 원소·행합·열합을 정수로 내림/올림하되, 행과 열의 합이 동시에 보존되도록 결정하는 문제입니다. 하한·상한 제약을 갖는 순환 유량으로 모델링해 정수 해를 보장하고, Dinic으로 구현합니다. 엣지 케이스, 정당성, 복잡도, 구현 포인트까지 간결히 정리했습니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- "Algorithm"
- "Graph"
tags:
- "Algorithm"
- "알고리즘"
- "BOJ"
- "백준"
- "Problem-13569"
- "cpp"
- "C++"
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
- "Graph"
- "그래프"
- "Network Flow"
- "네트워크 플로우"
- "Max Flow"
- "최대 유량"
- "Circulation"
- "순환 유량"
- "Lower Bound"
- "하한"
- "Upper Bound"
- "상한"
- "Lower-Upper Bounded Flow"
- "하한상한 유량"
- "Dinic"
- "디닉"
- "Bipartite"
- "이분 그래프"
- "Integer Rounding"
- "정수 반올림"
- "Feasible Rounding"
- "가능 반올림"
- "Rounding"
- "반올림"
- "Floor"
- "내림"
- "Ceil"
- "올림"
- "Row Sum"
- "행 합"
- "Column Sum"
- "열 합"
- "Fractional Part"
- "소수부"
- "Matrix"
- "행렬"
- "Table Rounding"
- "표 반올림"
- "Parsing"
- "문자열 파싱"
- "ICPC"
- "Regional"
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/13569
- 요약: 소수 첫째 자리까지 주어진 M×N 표의 실수 원소와 행/열 합을 모두 정수로 내림 또는 올림하되, 각 행의 정수 합이 주어진 행 합의 정수 반올림치와 일치하고, 각 열의 정수 합도 주어진 열 합의 정수 반올림치와 동시에 일치하도록 만드는 문제. 항상 가능한 해가 존재함이 보장됩니다.
- 제한/스펙: M,N ≤ 200, 원소 범위 0.0~1000.0, 입력은 소수 첫째 자리까지. 시간 1초, 메모리 512MB.

## 입력/출력
```
예제 입력 1
3 3
4.3 6.7 7.1 18.1
9.2 3.0 0.2 12.4
4.0 7.7 1.3 13.0
17.5 17.4 8.6

예제 출력 1
4 7 7 18
9 3 0 12
4 7 2 13
17 17 9
```

## 접근 개요
- 핵심 아이디어: 각 실수 x에 대해 floor(x) 또는 ceil(x)만 허용됩니다. 모든 원소를 일단 내림한 뒤, 소수부가 있는 칸들 중 일부를 올림으로 바꾸면 행/열 합의 남는 몫(필요 올림 개수)을 맞출 수 있습니다.
- 모델링: 하한·상한 제약이 있는 순환 유량으로 구성합니다. 행 노드에 “해당 행에서 올려야 할 개수의 범위”, 열 노드에 “해당 열에서 받아야 할 개수의 범위”를 두고, 소수부가 있는 칸마다 행→열 용량 1의 간선을 둡니다.
- 효과: 정수 유량 해가 곧 올림 선택(0/1)의 집합이 되며, 동시에 모든 행/열의 정수 합 제약을 만족합니다.

## 알고리즘 설계
1) 정수 스케일링: 모든 값에 10을 곱해 문자열로 안전 파싱 후, `floor = v/10`, `hasFrac = (v%10 != 0)`로 처리합니다.
2) 바닥 합 계산: 모든 칸을 내림했을 때 각 행/열의 기본 합을 구합니다.
3) 행/열의 허용 올림 개수 범위 계산:
   - 어떤 합 S(실수)에 대해 `floor(S)`는 올림 0개 사용, 소수부가 있다면 `ceil(S)=floor(S)+1`로 “올림 1개 추가”가 됩니다.
   - 행 i의 필요 올림 개수 d_i = `floor(rowSum_i) - sum_j floor(a_ij)`. 소수부가 있으면 d_i 또는 d_i+1이 허용(0~해당 행의 소수부 개수 범위에 한함).
   - 열도 동일하게 d_j^col 범위를 계산합니다.
4) 유량 그래프 구성(순환 유량 + 하한 변환):
   - S→행_i 간선 [rowLow_i, rowUp_i]
   - 행_i→열_j 간선 [0,1] (소수부가 있는 칸만)
   - 열_j→T 간선 [colLow_j, colUp_j]
   - T→S 간선 [0,∞)를 추가해 순환 허용
   - 모든 간선의 하한을 수요(demand)로 옮기고, 초원천 SS/초싱크 TT를 둔 뒤 SS→(수요>0), (수요<0)→TT 간선을 추가, SS→TT 최대유량이 전체 수요 합이면 해가 존재
5) 복원: 행→열 간선의 흐름(0/1)이 곧 해당 칸의 올림 여부. 바닥값에 더해 최종 정수 표를 얻고 행/열 합을 출력합니다.

## 정당성 근거
- 지역적 선택(개별 칸의 올림/내림)이 전역 제약(모든 행/열 합)과 충돌하지 않도록, “필요 올림 개수의 보존”을 흐름 보존 법칙으로 강제합니다.
- 각 간선 용량과 하한이 정수이므로, 네트워크 최대 유량 해는 정수 해가 되며 곧 올림 선택의 이진 해를 제공합니다.
- 문제에서 항상 가능해를 보장하므로, 수요 충족 가능한 순환이 존재합니다.

## 복잡도
- 시간: Dinic 기준 최악 O(E V^2). 여기서 V ≤ M+N+상수(≈ 500), E ≤ (소수부 칸 수) + M + N + 상수(≤ 4×10^4)로 1초 내 충분.
- 공간: O(V + E).

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Dinic {
	struct Edge {
		int to;
		int rev;
		int cap;
	};
	int n;
	vector<vector<Edge>> g;
	vector<int> level, it;
	Dinic(int n_) : n(n_), g(n_), level(n_), it(n_) {}
	int add_edge_ret(int u, int v, int cap) {
		Edge a{v, (int)g[v].size(), cap};
		Edge b{u, (int)g[u].size(), 0};
		g[u].push_back(a);
		g[v].push_back(b);
		return (int)g[u].size() - 1;
	}
	void add_edge(int u, int v, int cap) { add_edge_ret(u, v, cap); }
	bool bfs(int s, int t) {
		fill(level.begin(), level.end(), -1);
		queue<int> q;
		level[s] = 0;
		q.push(s);
		while (!q.empty()) {
			int v = q.front(); q.pop();
			for (auto &e : g[v]) if (e.cap > 0 && level[e.to] < 0) {
				level[e.to] = level[v] + 1;
				q.push(e.to);
			}
		}
		return level[t] >= 0;
	}
	int dfs(int v, int t, int f) {
		if (v == t) return f;
		for (int &i = it[v]; i < (int)g[v].size(); i++) {
			Edge &e = g[v][i];
			if (e.cap <= 0 || level[e.to] != level[v] + 1) continue;
			int pushed = dfs(e.to, t, min(f, e.cap));
			if (pushed > 0) {
				e.cap -= pushed;
				g[e.to][e.rev].cap += pushed;
				return pushed;
			}
		}
		return 0;
	}
	int maxflow(int s, int t) {
		int flow = 0, INF = 1e9;
		while (bfs(s, t)) {
			fill(it.begin(), it.end(), 0);
			int f;
			while ((f = dfs(s, t, INF)) > 0) flow += f;
		}
		return flow;
	}
};

static int parseScaled(const string &s) {
	int i = 0, sign = 1;
	if (i < (int)s.size() && (s[i] == '+' || s[i] == '-')) { sign = (s[i] == '-') ? -1 : 1; i++; }
	long long integerPart = 0;
	while (i < (int)s.size() && isdigit((unsigned char)s[i])) { integerPart = integerPart * 10 + (s[i] - '0'); i++; }
	int frac = 0;
	if (i < (int)s.size() && s[i] == '.') {
		i++;
		if (i < (int)s.size() && isdigit((unsigned char)s[i])) { frac = s[i] - '0'; i++; }
	}
	return sign * (int)(integerPart * 10 + frac);
}

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	int M, N;
	if (!(cin >> M >> N)) return 0;

	vector<vector<int>> a10(M, vector<int>(N));
	vector<vector<int>> floorCell(M, vector<int>(N));
	vector<vector<int>> fracCell(M, vector<int>(N));
	vector<int> rowSum10(M), colSum10(N);
	vector<int> rowFloor(M), colFloor(N);
	vector<int> rowFrac(M), colFrac(N);

	for (int i = 0; i < M; i++) {
		for (int j = 0; j < N; j++) {
			string s; cin >> s;
			a10[i][j] = parseScaled(s);
			floorCell[i][j] = a10[i][j] / 10;
			fracCell[i][j] = (a10[i][j] % 10 != 0);
		}
		string rs; cin >> rs;
		rowSum10[i] = parseScaled(rs);
		rowFloor[i] = rowSum10[i] / 10;
		rowFrac[i] = (rowSum10[i] % 10 != 0);
	}
	for (int j = 0; j < N; j++) {
		string cs; cin >> cs;
		colSum10[j] = parseScaled(cs);
		colFloor[j] = colSum10[j] / 10;
		colFrac[j] = (colSum10[j] % 10 != 0);
	}

	vector<int> baseRow(M, 0), baseCol(N, 0), rowFracCnt(M, 0), colFracCnt(N, 0);
	for (int i = 0; i < M; i++) {
		for (int j = 0; j < N; j++) {
			baseRow[i] += floorCell[i][j];
			baseCol[j] += floorCell[i][j];
			if (fracCell[i][j]) {
				rowFracCnt[i] += 1;
				colFracCnt[j] += 1;
			}
		}
	}

	vector<int> rowLow(M), rowUp(M), colLow(N), colUp(N);
	for (int i = 0; i < M; i++) {
		int d = rowFloor[i] - baseRow[i];
		vector<int> candidates;
		if (0 <= d && d <= rowFracCnt[i]) candidates.push_back(d);
		if (rowFrac[i]) {
			int d2 = d + 1;
			if (0 <= d2 && d2 <= rowFracCnt[i]) candidates.push_back(d2);
		}
		if (candidates.empty()) {
			int d0 = max(0, min(rowFracCnt[i], d));
			rowLow[i] = rowUp[i] = d0;
		} else {
			int mn = *min_element(candidates.begin(), candidates.end());
			int mx = *max_element(candidates.begin(), candidates.end());
			rowLow[i] = mn; rowUp[i] = mx;
		}
	}
	for (int j = 0; j < N; j++) {
		int d = colFloor[j] - baseCol[j];
		vector<int> candidates;
		if (0 <= d && d <= colFracCnt[j]) candidates.push_back(d);
		if (colFrac[j]) {
			int d2 = d + 1;
			if (0 <= d2 && d2 <= colFracCnt[j]) candidates.push_back(d2);
		}
		if (candidates.empty()) {
			int d0 = max(0, min(colFracCnt[j], d));
			colLow[j] = colUp[j] = d0;
		} else {
			int mn = *min_element(candidates.begin(), candidates.end());
			int mx = *max_element(candidates.begin(), candidates.end());
			colLow[j] = mn; colUp[j] = mx;
		}
	}

	int S = 0, T = 1;
	int rowBaseIdx = 2;
	int colBaseIdx = rowBaseIdx + M;
	int SS = colBaseIdx + N;
	int TT = SS + 1;
	int totalNodes = TT + 1;
	Dinic dinic(totalNodes);
	vector<int> demand(totalNodes, 0);

	auto addLowerEdge = [&](int u, int v, int low, int up, bool returnIndex = false) -> int {
		if (low < 0 || up < low) { /* feasibility guaranteed */ }
		demand[u] -= low;
		demand[v] += low;
		int cap = up - low;
		if (cap > 0) {
			int idx = dinic.add_edge_ret(u, v, cap);
			if (returnIndex) return idx;
		}
		return -1;
	};

	for (int i = 0; i < M; i++) {
		addLowerEdge(S, rowBaseIdx + i, rowLow[i], rowUp[i], false);
	}

	vector<vector<int>> edgeIdx(M, vector<int>(N, -1));
	for (int i = 0; i < M; i++) {
		for (int j = 0; j < N; j++) {
			if (fracCell[i][j]) {
				int idx = addLowerEdge(rowBaseIdx + i, colBaseIdx + j, 0, 1, true);
				edgeIdx[i][j] = idx;
			}
		}
	}

	for (int j = 0; j < N; j++) {
		addLowerEdge(colBaseIdx + j, T, colLow[j], colUp[j], false);
	}

	const int INF = 1e9;
	addLowerEdge(T, S, 0, INF, false);

	long long sumPos = 0;
	for (int v = 0; v < totalNodes; v++) {
		if (demand[v] > 0) {
			dinic.add_edge(SS, v, demand[v]);
			sumPos += demand[v];
		} else if (demand[v] < 0) {
			dinic.add_edge(v, TT, -demand[v]);
		}
	}

	(void)sumPos;
	int flowed = dinic.maxflow(SS, TT);
	(void)flowed; // feasibility is guaranteed

	vector<vector<int>> ans(M, vector<int>(N));
	for (int i = 0; i < M; i++) {
		for (int j = 0; j < N; j++) {
			int val = floorCell[i][j];
			if (edgeIdx[i][j] != -1) {
				auto &e = dinic.g[rowBaseIdx + i][edgeIdx[i][j]];
				int used = dinic.g[e.to][e.rev].cap > 0 ? 1 : 0;
				val += used;
			}
			ans[i][j] = val;
		}
	}

	for (int i = 0; i < M; i++) {
		long long sumRow = 0;
		for (int j = 0; j < N; j++) sumRow += ans[i][j];
		for (int j = 0; j < N; j++) {
			if (j) cout << ' ';
			cout << ans[i][j];
		}
		cout << ' ' << sumRow << '\n';
	}
	for (int j = 0; j < N; j++) {
		long long sumCol = 0;
		for (int i = 0; i < M; i++) sumCol += ans[i][j];
		if (j) cout << ' ';
		cout << sumCol;
	}
	cout << '\n';
	return 0;
}
```

## 코너 케이스 체크리스트
- 소수부가 전혀 없는 행/열(올림 범위가 [0,0])
- 한 행(열)에 소수부 칸이 매우 적어 올림 가능 개수가 제한되는 경우
- 행/열 합의 소수부 존재 여부에 따른 d 또는 d+1 선택 분기
- 최대 입력(M=N=200), 모든 칸 소수부 보유
- 0.0, 1000.0 같은 경계 값

## 제출 전 점검
- 입출력 형식과 개행을 예제와 동일하게 출력했는지
- 하한 변환 시 수요(demand) 부호 처리 오류 없는지
- 정수 스케일 파싱(문자열)로 부동소수 오차를 회피했는지

## 참고자료
- 하한·상한이 있는 유량의 순환(circulation with lower/upper bounds) 표준 기법
- 문제: https://www.acmicpc.net/problem/13569


