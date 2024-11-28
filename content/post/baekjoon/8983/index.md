---
image: "tmp_wordcloud.png"
title : "[C/C++] 8983번: 사냥꾼 - 백준"
date: 2022-07-07T00:00:00Z
categories: Algorithm
aliases: ["/collections/baekjoon/8983/"]
---

[8983번: 사냥꾼](https://www.acmicpc.net/problem/8983) 문제는 2차원 평면의 공간에 N마리의 동물이 자리잡고 있고, X축에 M개의 사대(총을 쏘는 장소)가 있다. 사정거리 L이 주어질때 잡을 수 있는 동물의 수를 출력하는 문제이다.

|![](https://upload.acmicpc.net/80de7dba-b822-4f30-b833-de3071af385b/-/preview/)|
|:---:|
|사대는 작은 사각형으로, 동물의 위치는 작은 원으로 표시되어 있다. 사정거리 L이 4라고 하면, 점선으로 표시된 영역은 왼쪽에서 세 번째 사대에서 사냥이 가능한 영역이다.|

## 문제 분석

2차원 평면의 공간에 N마리의 동물이 자리잡고 있고, X축에 M개의 사대(총을 쏘는 장소)가 있다. 사정거리 L이 주어질때 잡을 수 있는 동물의 수를 출력하는 문제이다.

사대의 수 M (1 ≤ M ≤ 100,000), 동물의 수 N (1 ≤ N ≤ 100,000), 사정거리 L (1 ≤ L ≤ 1,000,000,000)으로 입력이 주어지는데 단순히 사냥꾼을 기준으로 잡을 수 있는 동물을 순회하는것은 $$ O(M \times N) $$ 의 복잡도를 가진다.

어떤 사냥꾼이 잡을수 있는지는 중요하지 않다. 역으로 생각해서 동물을 잡을 수 있는 사냥꾼이 있는지 판단하는 식으로 코드를 작성한다.

## 풀이

1. 먼저 lower_bound(이분탐색) 함수를 사용하기위해서, 입력받은 발사대를 오름차순 정렬을 해준다.
2. 동물을 입력받음과 동시에, 동물의 x좌표와 가까운 발사대를 lower_bound를 통해 찾는다.
3. 해당 발사대와의 거리가 L 이하라면, answer++를 해준다.
4. 해당 발사대와 거리가 멀다면 , 해당 발사대의 이전 발사대를 조사해 L 이하라면 answer++를 해준다.

> 주의 : Lower_bound 함수는 해당 배열 혹은 벡터에서 key값과 같은 값을 찾고, 만약 없다면 key값보다 큰 가장 작은 정수를 찾아준다. 따라서 해당 key값이 배열 혹은 벡터의 마지막원소 (제일 큰 원소) 보다 크다면, 배열/벡터의 사이즈+1 을 리턴해주기 때문에, out of index 처리를 잘 해주어야 한다.

```cpp
#include<iostream>	
#include<algorithm>	
#include<vector>	
#include<cmath>	
using namespace std;
	
vector<long long> M;
	
int main() {
	ios_base::sync_with_stdio(0);	
	cin.tie(0);	
	long long n, m, l, cnt = 0;
	
	cin >> m >> n >> l;
	
	for (long long i = 0; i < m; i++) {	
		long long data;	
		cin >> data;	
		M.push_back(data);	
	}
	
	sort(M.begin(), M.end());
	
	for (long long i = 0; i < n; i++) {	
		long long x, y;	
		cin >> x >> y;
	
		long long ind = lower_bound(M.begin(), M.end(), x) - M.begin();	
		if (ind!=m&&abs(M[ind] - x) + y <= l) cnt++;	
		else if (ind - 1 >= 0 && abs(M[ind - 1] - x) + y <= l) cnt++;	
	}
	
	cout << cnt;	
}
```
## 시간 복잡도

발사대를 정렬하는데 $$ O(MlogM) $$ 이 된다. 각 동물의 좌표마다 이분탐색을 하므로, $$ O(NlogN) $$ 이 된다.

따라서 총 $$ O(NlogN) \qquad \small\text{M의범위 == N의 범위} $$이 된다. 