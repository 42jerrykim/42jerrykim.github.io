// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다
#include <bits/stdc++.h>
using namespace std;

const long long INF = 1e18;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    // dp[last0][last1] = min total difficulty
    // last0 = last index person 0 sang (-1 if none)
    // last1 = last index person 1 sang (-1 if none)
    const int NONE = -1;
    map<pair<int, int>, long long> dp;
    dp[{NONE, NONE}] = 0;

    for (int k = 0; k < n; k++) {
        map<pair<int, int>, long long> ndp;
        for (auto& [key, cost] : dp) {
            int last0 = key.first, last1 = key.second;
            if (k > 0 && last0 != k - 1 && last1 != k - 1) continue;

            // Person 0 sings note k
            long long c0 = cost;
            if (last0 != NONE) c0 += abs(a[k] - a[last0]);
            {
                auto p = make_pair(k, last1);
                if (!ndp.count(p) || ndp[p] > c0) ndp[p] = c0;
            }

            // Person 1 sings note k
            long long c1 = cost;
            if (last1 != NONE) c1 += abs(a[k] - a[last1]);
            {
                auto p = make_pair(last0, k);
                if (!ndp.count(p) || ndp[p] > c1) ndp[p] = c1;
            }
        }
        dp = move(ndp);
    }

    long long ans = INF;
    for (auto& [key, cost] : dp) {
        ans = min(ans, cost);
    }
    cout << ans << "\n";
    return 0;
}
