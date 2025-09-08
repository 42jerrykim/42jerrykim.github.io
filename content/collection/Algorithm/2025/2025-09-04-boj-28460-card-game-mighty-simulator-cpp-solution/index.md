---
title: "[Algorithm] cpp 백준 28460번: Card Game (Mighty) 시뮬레이션"
description: "54장 트럼프(조커 포함) 마이티 규칙을 완전 시뮬레이션하여 Deal Mistake/Rule Violation 우선, 선거·기루다/no-기루다, 프렌드, 조커 총, 1·10라운드 조커 무력화, 첫 라운드 제약, 승패·점수차 출력까지 정확 구현한 C++ 풀이."
date: 2025-09-04
lastmod: 2025-09-04
categories:
- "Algorithm"
- "Simulation"
tags:
- "Algorithm"
- "알고리즘"
- "BOJ"
- "백준"
- "Problem-28460"
- "cpp"
- "C++"
- "Simulation"
- "시뮬레이션"
- "Card Game"
- "마이티"
- "Mighty"
- "Trump"
- "기루다"
- "No-Giruda"
- "Friend"
- "프렌드"
- "Joker"
- "조커"
- "Joker Gun"
- "조커 총"
- "Ace"
- "에이스"
- "Rule Violation"
- "룰 위반"
- "Deal Mistake"
- "딜 미스"
- "Priority"
- "우선순위"
- "Game Simulation"
- "게임 시뮬레이션"
- "Parsing"
- "파싱"
- "Implementation"
- "구현"
- "Implementation Details"
- "구현 디테일"
- "Edge Cases"
- "코너 케이스"
- "Pitfalls"
- "실수 포인트"
- "Correctness"
- "정당성 증명"
- "Complexity"
- "복잡도"
- "Time Complexity"
- "시간복잡도"
- "Space Complexity"
- "공간복잡도"
- "Set"
- "집합"
- "Multiset"
- "멀티셋"
- "Data Structures"
- "자료구조"
- "Map"
- "해시"
- "Ordering"
- "정렬"
- "Tie-break"
- "동률 처리"
- "Game Rules"
- "게임 규칙"
- "Contest"
- "유틸컵"
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/28460
- 요약: 5인 마이티 카드 게임의 전 과정을 규칙대로 시뮬레이션하여 여당/야당 승패와 점수차(여당 점수−공약)를 출력한다. 덱 분배 위반, 딜 미스, 라운드 규칙 위반 등 모든 예외를 판정한다.
- 제한: 시간 1초, 메모리 256MB, 총 10라운드, 점수 카드 20장.

## 입력/출력
```
<입력>
5줄: 각 플레이어가 받은 10장(문양+숫자, 조커 JB/JC)
1줄: 5인의 공약(N 또는 S/D/H/C/X + 정수)
1줄: 대통령이 내려놓은 4장(점수는 여당 가산)
1줄: 프렌드 카드(그 소유자가 여당 합류, 대통령 자신이면 프렌드 없음)
10줄: 각 라운드 1~5번 플레이어가 낸 카드 5장(첫 카드가 조커면 JD/JH/JDH/JS/JC/JSC)

<출력>
Deal Mistake | Rule Violation | "<여당점수-공약> Government Party/ Opposition Party"
```

## 접근 개요
- 전체 파이프라인: 분배 검증 → 딜 미스 판정(우선 적용) → 선거/대통령/기루다(no-기루다) 결정 → 남은 4장 수거·버림(점수 가산) → 프렌드 설정 → 10라운드 진행 → 점수 합산/판정.
- 강함 순서(일반/노기루다)와 예외를 모두 반영: 마이티, 기루다/허용문양, 조커 색/무력화, 조커 총 강제, 1·10라운드 조커 무력화, 첫 라운드 대통령 기루다 리드 금지(전부 기루다 예외, 9기루다+마이티는 마이티 리드 강제).

## 알고리즘 설계
- 카드 파싱과 정규화, 전체 54장 덱 구성(중복/미존재 검증).
- 딜 미스 가중치: SA -1, 점수 카드 +1, 조커 -0.5. 초기 10장 합 ≤ 1 이면 Deal Mistake.
- 선거: no-기루다는 목표+1로 환산, 동률은 no-기루다 ≻ 문양 S>D>H>C ≻ 플레이어 번호.
- 조커 총: (기본 H3,C3) 단, 기루다 H면 H3→D3, 기루다 C면 C3→S3. 해당 색 조커 보유자 강제(단, 마이티 대체 허용). 강제된 그 조커만 무력화.
- 라운드: 허용문양 규칙, 마이티/조커 예외 허용, 조커 시작 시 허용문양 선택(J* 토큰). 1·10라운드 조커는 최약 클래스(낼 수는 있음).
- 판정 우선순위: (분배 위반이면 즉시) Rule Violation → (그 외) Deal Mistake → (그 외) 정상 결과 출력.

## 복잡도
- 라운드 수 고정(10). 각 라운드 5장 비교 및 자료구조 연산 상수에 가깝게 설계 → 전체 선형 수준.

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

enum Suit { SPADES=0, DIAMONDS=1, HEARTS=2, CLUBS=3, NOSUIT=4 };
enum Color { BLACK=0, RED=1 };

struct Card {
    bool isJoker = false;
    bool isBlackJoker = false; // true for JB, false for JC
    Suit suit = NOSUIT;
    int rank = 0;              // 2..10, 11=J, 12=Q, 13=K, 1=A
    string code;

    bool operator==(const Card& o) const {
        if (isJoker != o.isJoker) return false;
        if (isJoker) return isBlackJoker == o.isBlackJoker;
        return suit == o.suit && rank == o.rank;
    }
    bool operator<(const Card& o) const {
        if (isJoker != o.isJoker) return isJoker < o.isJoker;
        if (isJoker) return isBlackJoker < o.isBlackJoker;
        if (suit != o.suit) return suit < o.suit;
        return rank < o.rank;
    }
};

static inline Color suitColor(Suit s) {
    return (s == SPADES || s == CLUBS) ? BLACK : RED;
}
static inline string makeCode(Suit s, int r) {
    string res;
    res.push_back(s == SPADES ? 'S' : s == DIAMONDS ? 'D' : s == HEARTS ? 'H' : 'C');
    if (r == 1) res += "A";
    else if (r == 11) res += "J";
    else if (r == 12) res += "Q";
    else if (r == 13) res += "K";
    else res += to_string(r);
    return res;
}
static inline Card makeCard(Suit s, int r) {
    Card c; c.isJoker=false; c.suit=s; c.rank=r; c.code=makeCode(s,r); return c;
}
static inline Card blackJoker() { Card c; c.isJoker=true; c.isBlackJoker=true; c.code="JB"; return c; }
static inline Card colorJoker() { Card c; c.isJoker=true; c.isBlackJoker=false; c.code="JC"; return c; }

static inline bool isPointCard(const Card& c) {
    if (c.isJoker) return false;
    return (c.rank == 10 || c.rank == 11 || c.rank == 12 || c.rank == 13 || c.rank == 1);
}
static inline bool parseNormalCard(const string& t, Card& out) {
    out.code = t;
    if (t == "JB") { out.isJoker = true; out.isBlackJoker = true; return true; }
    if (t == "JC") { out.isJoker = true; out.isBlackJoker = false; return true; }
    if (t.size() < 2) return false;
    Suit suit = NOSUIT;
    if (t[0]=='S') suit=SPADES;
    else if (t[0]=='D') suit=DIAMONDS;
    else if (t[0]=='H') suit=HEARTS;
    else if (t[0]=='C') suit=CLUBS;
    else return false;
    string rstr = t.substr(1);
    int rank = 0;
    if (rstr == "A") rank = 1;
    else if (rstr == "J") rank = 11;
    else if (rstr == "Q") rank = 12;
    else if (rstr == "K") rank = 13;
    else {
        for (char c: rstr) if (!isdigit((unsigned char)c)) return false;
        rank = stoi(rstr);
        if (rank < 2 || rank > 10) return false;
    }
    out.isJoker=false; out.suit=suit; out.rank=rank;
    return true;
}

struct Bid {
    bool valid = false;
    bool noGiruda = false;
    Suit suit = NOSUIT;
    int target = 0;
};
static inline bool parseBid(const string& t, Bid& b) {
    if (t == "N") { b.valid=false; return true; }
    if (t.size() < 2) return false;
    if (t[0] == 'X') {
        string n = t.substr(1);
        for (char c: n) if (!isdigit((unsigned char)c)) return false;
        b.noGiruda = true; b.suit=NOSUIT; b.target=stoi(n); b.valid=true;
        if (b.target < 12 || b.target > 20) return false;
        return true;
    }
    Suit s = NOSUIT;
    if (t[0]=='S') s=SPADES;
    else if (t[0]=='D') s=DIAMONDS;
    else if (t[0]=='H') s=HEARTS;
    else if (t[0]=='C') s=CLUBS;
    else return false;
    string n = t.substr(1);
    for (char c: n) if (!isdigit((unsigned char)c)) return false;
    int tg = stoi(n);
    if (tg < 13 || tg > 20) return false;
    b.valid=true; b.noGiruda=false; b.suit=s; b.target=tg;
    return true;
}

static inline double dealMistakeWeight(const vector<Card>& hand10) {
    double w = 0.0;
    for (auto &c: hand10) {
        if (c.isJoker) w += -0.5;
        else if (c.suit == SPADES && c.rank == 1) w += -1.0;
        else if (isPointCard(c)) w += 1.0;
    }
    return w;
}

static inline bool isMighty(const Card& c, bool noGiruda, Suit giruda) {
    if (c.isJoker) return false;
    if (!noGiruda && giruda == SPADES) return (c.suit == DIAMONDS && c.rank == 1);
    return (c.suit == SPADES && c.rank == 1);
}
static inline bool isTrump(const Card& c, bool noGiruda, Suit giruda) {
    return (!noGiruda && !c.isJoker && c.suit == giruda);
}

static inline int suitStrengthOrder(Suit s) {
    if (s == SPADES) return 4;
    if (s == DIAMONDS) return 3;
    if (s == HEARTS) return 2;
    if (s == CLUBS) return 1;
    return 0;
}
static inline pair<int,int> intraRankKey(const Card& c) {
    int ro = (c.rank == 1 ? 14 : c.rank);
    return {ro, suitStrengthOrder(c.suit)};
}

struct StartInfo {
    bool isJokerStart = false;
    vector<Suit> allowed; // for Joker-start: 1 or 2 suits; for normal start: [suit]
    bool isBlack = false; // only for Joker-start
    bool invalid = false;
    Card firstCard;
};
static inline StartInfo parseStartToken(const string& token) {
    StartInfo si;
    if (token == "JD")  { si.isJokerStart=true; si.allowed={DIAMONDS}; si.isBlack=false; return si; }
    if (token == "JH")  { si.isJokerStart=true; si.allowed={HEARTS};   si.isBlack=false; return si; }
    if (token == "JDH") { si.isJokerStart=true; si.allowed={DIAMONDS,HEARTS}; si.isBlack=false; return si; }
    if (token == "JS")  { si.isJokerStart=true; si.allowed={SPADES};   si.isBlack=true;  return si; }
    if (token == "JC")  { si.isJokerStart=true; si.allowed={CLUBS};    si.isBlack=true;  return si; }
    if (token == "JSC") { si.isJokerStart=true; si.allowed={SPADES,CLUBS}; si.isBlack=true; return si; }
    Card c;
    if (!parseNormalCard(token, c)) { si.invalid=true; return si; }
    if (c.isJoker) { si.invalid=true; return si; }
    si.isJokerStart=false; si.firstCard=c; si.allowed={c.suit};
    return si;
}

struct RankContext {
    bool noGiruda = false;
    Suit giruda = NOSUIT;
    int roundIndex = 0;                // 0..9
    vector<Suit> allowed;              // 1 or 2 suits
    bool firstIsJoker = false;
    bool firstColorIsBlack = false;    // for no-giruda joker color comparison
    bool forcedJokerActive = false;    // Joker-gun active this round?
    bool forcedJokerIsBlack = false;   // which joker is forced if active
};
static inline int strengthClass(const Card& c, const RankContext& rc) {
    bool jokerPowerless = false;
    if (c.isJoker) {
        if (rc.roundIndex == 0 || rc.roundIndex == 9) jokerPowerless = true;
        if (rc.forcedJokerActive && (c.isBlackJoker == rc.forcedJokerIsBlack)) jokerPowerless = true;
    }
    if (isMighty(c, rc.noGiruda, rc.giruda)) return 0;

    if (!rc.noGiruda) {
        if (c.isJoker) {
            if (!jokerPowerless) {
                bool girudaBlack = (suitColor(rc.giruda) == BLACK);
                bool same = (c.isBlackJoker == girudaBlack);
                return same ? 1 : 3;
            } else {
                return 6; // powerless joker (weakest)
            }
        }
        if (isTrump(c, rc.noGiruda, rc.giruda)) return 2;
        bool isAllowed = false;
        for (auto s: rc.allowed) if (!c.isJoker && c.suit == s) { isAllowed = true; break; }
        if (isAllowed) return 4;
        return 5;
    } else {
        if (c.isJoker) {
            if (!jokerPowerless) {
                bool same = (c.isBlackJoker == rc.firstColorIsBlack);
                return same ? 1 : 3;
            } else {
                return 5; // powerless joker (weakest in no-giruda)
            }
        }
        bool isAllowed = false;
        for (auto s: rc.allowed) if (!c.isJoker && c.suit == s) { isAllowed = true; break; }
        if (isAllowed) return 2;
        return 4;
    }
}

static int decideWinner(const array<Card,5>& played,
                        const RankContext& baseRc) {
    int bestIdx = 0;
    int bestClass = INT_MAX;
    pair<int,int> bestIntra = {-1,-1};
    for (int i=0;i<5;i++) {
        int cls = strengthClass(played[i], baseRc);
        pair<int,int> intra = {-100,-100};
        if (cls == 0) intra = {200, 200}; // Mighty
        else if (!played[i].isJoker && (cls!=6)) intra = intraRankKey(played[i]);
        if (cls < bestClass || (cls == bestClass && intra > bestIntra)) {
            bestClass = cls; bestIntra = intra; bestIdx = i;
        }
    }
    return bestIdx;
}

struct JokerGunState {
    bool active = false;
    bool forceBlack = false; // true → JB forced; false → JC forced
    int shooterPlayer = -1;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<vector<string>> initialTokens(5, vector<string>(10));
    for (int i=0;i<5;i++) for (int j=0;j<10;j++) if (!(cin >> initialTokens[i][j])) return 0;
    vector<string> bidTok(5); for (int i=0;i<5;i++) cin >> bidTok[i];
    vector<string> discardTok(4); for (int i=0;i<4;i++) cin >> discardTok[i];
    string friendTok; cin >> friendTok;
    vector<array<string,5>> roundsTok(10);
    for (int r=0;r<10;r++) for (int i=0;i<5;i++) cin >> roundsTok[r][i];

    vector<Card> deck;
    for (int s=0;s<4;s++) {
        for (int r=2;r<=10;r++) deck.push_back(makeCard((Suit)s, r));
        deck.push_back(makeCard((Suit)s,11));
        deck.push_back(makeCard((Suit)s,12));
        deck.push_back(makeCard((Suit)s,13));
        deck.push_back(makeCard((Suit)s,1));
    }
    deck.push_back(blackJoker());
    deck.push_back(colorJoker());
    set<string> allDeckCodes; for (auto &c: deck) allDeckCodes.insert(c.code);

    auto parseCardVec = [&](const vector<string>& v) {
        vector<Card> res; res.reserve(v.size());
        for (auto &t: v) {
            Card c;
            if (!parseNormalCard(t, c)) { c.code = t + "#INVALID"; }
            res.push_back(c);
        }
        return res;
    };

    vector<vector<Card>> initHands(5);
    for (int i=0;i<5;i++) initHands[i] = parseCardVec(initialTokens[i]);

    bool distViolation = false;
    set<string> seen;
    for (int i=0;i<5;i++) for (auto &c: initHands[i]) {
        if (!allDeckCodes.count(c.code)) distViolation = true;
        if (!seen.insert(c.code).second) distViolation = true;
    }
    if (distViolation) { cout << "Rule Violation\n"; return 0; }

    bool hasDealMistake = false;
    for (int i=0;i<5;i++) if (dealMistakeWeight(initHands[i]) <= 1.0) hasDealMistake = true;
    if (hasDealMistake) { cout << "Deal Mistake\n"; return 0; }

    set<string> remaining = allDeckCodes;
    for (auto &s: seen) remaining.erase(s);
    if ((int)remaining.size() != 4) { cout << "Rule Violation\n"; return 0; }
    vector<Card> remain4; for (auto &c: deck) if (remaining.count(c.code)) remain4.push_back(c);

    vector<Bid> bids(5);
    for (int i=0;i<5;i++) if (!parseBid(bidTok[i], bids[i])) { cout << "Rule Violation\n"; return 0; }
    int pres = -1, bestEff = -1, tiePref = -1, bestRawTarget = -1; Suit bestSuit = NOSUIT;
    for (int i=0;i<5;i++) if (bids[i].valid) {
        int eff = bids[i].noGiruda ? (bids[i].target + 1) : bids[i].target;
        int pref = bids[i].noGiruda ? 2 : 1;
        if (eff > bestEff) { bestEff = eff; tiePref=pref; pres=i; bestSuit=bids[i].noGiruda?NOSUIT:bids[i].suit; bestRawTarget=bids[i].target; }
        else if (eff == bestEff) {
            if (pref > tiePref) { tiePref=pref; pres=i; bestSuit=bids[i].noGiruda?NOSUIT:bids[i].suit; bestRawTarget=bids[i].target; }
            else if (pref == tiePref) {
                if (!bids[i].noGiruda && bestSuit!=NOSUIT) {
                    int a = suitStrengthOrder(bids[i].suit), b = suitStrengthOrder(bestSuit);
                    if (a > b || (a==b && i<pres)) { pres=i; bestSuit=bids[i].suit; bestRawTarget=bids[i].target; }
                } else { if (i < pres) { pres=i; bestSuit=NOSUIT; bestRawTarget=bids[i].target; } }
            }
        }
    }
    if (pres == -1) { cout << "Rule Violation\n"; return 0; }

    bool noGiruda = bids[pres].noGiruda; Suit giruda = noGiruda ? NOSUIT : bids[pres].suit; int pledge = bids[pres].target;

    vector<multiset<string>> hands(5);
    for (int i=0;i<5;i++) for (auto &c: initHands[i]) hands[i].insert(c.code);
    for (auto &c: remain4) hands[pres].insert(c.code);

    vector<Card> discards = parseCardVec(discardTok);
    for (auto &c: discards) {
        if (!allDeckCodes.count(c.code) || !hands[pres].count(c.code)) { cout << "Rule Violation\n"; return 0; }
        hands[pres].erase(hands[pres].find(c.code));
    }

    Card friendCard; if (!parseNormalCard(friendTok, friendCard)) { cout << "Rule Violation\n"; return 0; }
    int friendPlayer = -1; for (int p=0;p<5;p++) if (hands[p].count(friendCard.code)) { friendPlayer=p; break; }
    bool friendInDiscards = false; for (auto &c: discards) if (c.code == friendCard.code) { friendInDiscards = true; break; }
    bool friendless = (friendPlayer == pres) || friendInDiscards;
    auto isGovernment = [&](int p){ return (p == pres) || (!friendless && p == friendPlayer); };

    int govScore = 0, oppScore = 0; for (auto &c: discards) if (isPointCard(c)) govScore++;

    auto jokerGunsForGiruda = [&](bool noG, Suit g)->vector<Card>{
        vector<Card> v;
        if (!noG && g == HEARTS) { v.push_back(makeCard(DIAMONDS,3)); v.push_back(makeCard(CLUBS,3)); }
        else if (!noG && g == CLUBS) { v.push_back(makeCard(HEARTS,3)); v.push_back(makeCard(SPADES,3)); }
        else { v.push_back(makeCard(HEARTS,3)); v.push_back(makeCard(CLUBS,3)); }
        return v;
    };
    vector<Card> guns = jokerGunsForGiruda(noGiruda, giruda);
    auto isJokerGunCard = [&](const Card& c){ for (auto &g: guns) if (c == g) return true; return false; };

    auto getCardFromToken = [&](const string& t, bool isStartToken, StartInfo &si)->Card {
        if (isStartToken) {
            si = parseStartToken(t);
            if (!si.isJokerStart && si.invalid) { Card x; x.code="#INVALID"; return x; }
            if (!si.isJokerStart) return si.firstCard;
            return si.isBlack ? blackJoker() : colorJoker();
        } else {
            StartInfo tmp; Card c; if (!parseNormalCard(t, c)) { c.code="#INVALID"; } return c;
        }
    };

    auto countTrumpInHand = [&](int p)->int{
        if (noGiruda) return 0;
        int cnt = 0;
        for (int r=1;r<=13;r++) {
            if (r==1 || (2<=r && r<=10) || r==11 || r==12 || r==13) {
                string cd = makeCode(giruda, r);
                cnt += (int)hands[p].count(cd);
            }
        }
        return cnt;
    };
    auto hasMightyInHand = [&](int p)->bool{
        Card m = (!noGiruda && giruda==SPADES) ? makeCard(DIAMONDS,1) : makeCard(SPADES,1);
        return hands[p].count(m.code) > 0;
    };

    int starter = pres; bool laterRuleViolation = false;

    for (int rnd=0; rnd<10; rnd++) {
        array<string,5> tokens = roundsTok[rnd];
        array<int,5> orderToPlayer{}; array<Card,5> played{}; array<StartInfo,5> startInfo{};
        for (int k=0;k<5;k++) {
            int p = (starter + k) % 5; orderToPlayer[k] = p; bool isStart = (k==0); StartInfo si; Card c = getCardFromToken(tokens[p], isStart, si);
            if (c.code == "#INVALID") { laterRuleViolation = true; }
            played[k] = c; startInfo[k] = si;
        }
        if (laterRuleViolation) break;

        vector<Suit> allowed; bool firstIsJokerStart = startInfo[0].isJokerStart; bool firstColorIsBlack = false;
        if (firstIsJokerStart) { allowed = startInfo[0].allowed; firstColorIsBlack = startInfo[0].isBlack; }
        else { if (played[0].isJoker) { laterRuleViolation = true; break; } allowed = { played[0].suit }; firstColorIsBlack = (suitColor(played[0].suit) == BLACK); }

        if (!noGiruda && rnd == 0 && starter == pres) {
            int trumpCnt = countTrumpInHand(pres); bool mightyIn = hasMightyInHand(pres);
            bool allTrump = (trumpCnt == 10); bool nineTrumpPlusMighty = (trumpCnt == 9 && mightyIn);
            Card led = played[0]; bool ledIsTrump = (!led.isJoker && led.suit == giruda); bool ledIsMighty = isMighty(led, noGiruda, giruda);
            if (nineTrumpPlusMighty && !ledIsMighty) { laterRuleViolation = true; break; }
            if (!allTrump && ledIsTrump) { laterRuleViolation = true; break; }
        }

        JokerGunState jg; if (!firstIsJokerStart && isJokerGunCard(played[0])) {
            jg.active = true; bool gunIsBlack = (suitColor(played[0].suit) == BLACK); jg.forceBlack = gunIsBlack; jg.shooterPlayer = orderToPlayer[0];
            Card forced = jg.forceBlack ? blackJoker() : colorJoker();
            if (hands[jg.shooterPlayer].count(forced.code)) { jg.active = false; }
            else { bool someoneHas=false; for (int p=0;p<5;p++) if (hands[p].count(forced.code)) { someoneHas=true; break; } if (!someoneHas) jg.active = false; }
        }

        auto mustFollowSuit = [&](int p)->bool{
            for (auto s: allowed) {
                for (int r=1;r<=13;r++) {
                    if (r==1 || (2<=r && r<=10) || r==11 || r==12 || r==13) {
                        string cc = makeCode(s, r);
                        if (hands[p].count(cc)) return true;
                    }
                }
            }
            return false;
        };

        Card forcedJoker = jg.active ? (jg.forceBlack ? blackJoker() : colorJoker()) : Card{};
        for (int k=0;k<5;k++) {
            int p = orderToPlayer[k]; Card c = played[k];
            if (!hands[p].count(c.code)) { laterRuleViolation = true; break; }
            if (jg.active && hands[p].count(forcedJoker.code)) {
                if (!(c.isJoker && c.isBlackJoker == forcedJoker.isBlackJoker)) {
                    if (!isMighty(c, noGiruda, giruda)) { laterRuleViolation = true; break; }
                }
            }
            if (mustFollowSuit(p)) {
                if (!c.isJoker && !isMighty(c, noGiruda, giruda)) {
                    bool ok=false; for (auto s: allowed) if (c.suit == s) { ok=true; break; }
                    if (!ok) { laterRuleViolation = true; break; }
                }
            }
            hands[p].erase(hands[p].find(c.code));
        }
        if (laterRuleViolation) break;

        RankContext rc; rc.noGiruda = noGiruda; rc.giruda = giruda; rc.roundIndex = rnd; rc.allowed = allowed; rc.firstIsJoker = firstIsJokerStart; rc.firstColorIsBlack = firstColorIsBlack; rc.forcedJokerActive = jg.active; rc.forcedJokerIsBlack = jg.forceBlack;
        int winnerIdx = decideWinner(played, rc); int winnerPlayer = orderToPlayer[winnerIdx];
        int pts = 0; for (int k=0;k<5;k++) if (isPointCard(played[k])) pts++;
        if (isGovernment(winnerPlayer)) govScore += pts; else oppScore += pts;
        starter = winnerPlayer;
    }

    if (laterRuleViolation) { cout << "Rule Violation\n"; return 0; }

    int diff = govScore - pledge; if (govScore >= pledge) cout << diff << " Government Party\n"; else cout << diff << " Opposition Party\n"; return 0;
}
```

## 코너 케이스 체크리스트
- 분배 위반(중복/범위 밖 카드), 딜 미스 우선 출력
- 첫 라운드 대통령의 기루다 리드 금지, 9기루다+마이티면 마이티 리드 강제
- 조커 총 강제: 보유자는 그 조커(또는 마이티) 의무, 해당 색 조커만 무력화
- 1·10라운드 조커는 낼 수 있으나 최약 클래스 처리(우위 없음)
- no-기루다: 조커 색 비교 기준, 허용문양/기타 순서 정확성

## 참고자료
- 문제: https://www.acmicpc.net/problem/28460
- 마이티 규칙 요약 및 변형 규칙 해설(문제 본문 및 힌트)


