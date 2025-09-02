---
title: "[Algorithm] Big O 표기법 쉽게 이해하기 - Sam Rose 소개"
description: "Sam Rose의 'Big O' 글을 바탕으로 O(1), O(log n), O(n), O(n^2)을 시각적으로 이해합니다. 반복 합 공식, 버블 정렬, 이진 탐색, Set/Map, 캐싱 등 실무 팁을 한눈에 정리했습니다."
date: "2025-09-01"
lastmod: "2025-09-01"
categories:
- Algorithm
- Computer Science
tags:
- BigO
- TimeComplexity
- O(1)
- O(log n)
- O(n)
- O(n^2)
- Algorithm
- DataStructures
- BinarySearch
- BubbleSort
- Performance
- Optimization
- C++
- Set
- Map
- Caching
- Education
- Visualization
image: image01.png
---

알고리즘 성능을 “빠르다/느리다”로만 말하긴 어렵습니다. 입력 크기에 따라 시간이 어떻게 늘어나는지를 설명하는 도구가 바로 Big O 표기법입니다. Sam Rose의 ‘Big O’는 상호작용 예제와 직관적인 시각화로 `O(1)`·`O(log n)`·`O(n)`·`O(n^2)`의 차이를 체감하게 해 주는 훌륭한 안내서입니다. 이 글에서는 해당 글의 핵심 개념과, 내 코드에 바로 적용할 수 있는 실무 팁을 간결하게 정리했습니다. 복잡도를 “암기”하기보다, 병목을 “식별하고 바꾸는” 감각을 얻어가세요.

## 요약

- **핵심**: Big O는 입력 크기에 따른 실행 시간 증가율(성장 차수)을 표현합니다. 벽시계 시간 자체보다 **입력과 시간의 관계**를 작게 기술하는 표기법입니다.
- **4가지 대표 복잡도**: `O(1)`(상수), `O(log n)`(로그), `O(n)`(선형), `O(n^2)`(제곱). 최악 기준으로 설명하는 것이 일반적입니다.
- **사례**: 반복 합 `sum(1..n)`은 루프 구현 시 `O(n)`, 수학 공식 `(n*(n+1))/2` 사용 시 `O(1)`. 버블 정렬은 최악 `O(n^2)`, 이진 탐색은 `O(log n)`.
- **실무 팁**: `Set/Map` 조회는 `O(1)`이지만, 컬렉션을 새로 만드는 비용은 `O(n)`. 루프 안에서 `.indexOf` 같은 `O(n)` 호출을 피하고, 캐시로 중복 계산을 줄이세요.

## 글 소개

Sam Rose가 쓴 "Big O"는 빅오 표기법을 가장 직관적으로 설명하는 훌륭한 입문 글입니다. 단순한 이론 나열을 넘어, **상호작용 예제**와 **시각화**로 `O(1)`·`O(log n)`·`O(n)`·`O(n^2)`의 차이를 체감하게 해 줍니다. 개발자라면 반드시 한 번 읽어볼 만한 글로, 면접 대비와 실무 성능 점검 모두에 유용합니다.

## 핵심 개념 정리

- **Big O의 목적**: 절대 시간이 아니라, 입력이 커질수록 시간이 어떻게 늘어나는지(성장률)를 표현합니다. 같은 작업이라도 구현 방식에 따라 성장 차수가 달라질 수 있습니다.
- **최악 기준(Worst-case default)**: 별도 언급이 없다면 최악 경우 복잡도로 기록합니다. (예: 버블 정렬은 역순 입력에서 `O(n^2)`)
- **상수항·계수 무시**: `O(2n)`이나 `O(n+1)`도 결국 `O(n)`으로 표기합니다. 성장 차수만 남기는 게 관례입니다.

## 사례로 이해하는 Big O

1) **반복 합 vs 수학 공식**  
루프로 1부터 n까지 더하면 반복 횟수가 n번이므로 `O(n)`. 반면 `(n*(n+1))/2` 공식을 쓰면 입력 크기와 무관하게 연산 횟수가 일정해 `O(1)`입니다.

2) **버블 정렬(Bubble Sort)**  
인접 원소를 교환하며 정렬합니다. 이미 정렬되어 있으면 한 번 훑고 끝나 `O(n)`도 가능하지만, 일반적으로(특히 역순) `O(n^2)`입니다.

3) **이진 탐색(Binary Search)**  
정렬된 배열에서 절반씩 범위를 줄이며 찾습니다. 후보가 절반씩 사라지므로 `O(log n)`. 10억 원소도 31회 내외의 비교로 찾을 수 있습니다.

## 샘플 코드

### O(n) vs O(1): 1부터 n까지 합

```cpp
// O(n): 루프
long long sumLoop(long long n) {
  long long total = 0;
  for (long long i = 1; i <= n; ++i) {
    total += i;
  }
  return total;
}

// O(1): 공식
long long sumFormula(long long n) {
  return n * (n + 1) / 2;
}
```

### O(log n): 이진 탐색

```cpp
// 정렬된 벡터에서 target의 인덱스를 반환, 없으면 -1
int binarySearch(const std::vector<int>& a, int target) {
  int left = 0, right = static_cast<int>(a.size()) - 1;
  while (left <= right) {
    int mid = left + (right - left) / 2;
    if (a[mid] == target) return mid;
    if (a[mid] < target) left = mid + 1;
    else right = mid - 1;
  }
  return -1;
}
```

### O(n^2): 버블 정렬(교육용)

```cpp
std::vector<int> bubbleSort(std::vector<int> a) {
  bool swapped;
  do {
    swapped = false;
    for (size_t i = 0; i + 1 < a.size(); ++i) {
      if (a[i] > a[i + 1]) {
        std::swap(a[i], a[i + 1]);
        swapped = true;
      }
    }
  } while (swapped);
  return a;
}
```

### 안티패턴: 루프 안의 indexOf vs 인덱스 루프

```cpp
// O(n^2): 루프 안에서 std::find 사용
std::string buildListBad(const std::vector<std::string>& items) {
  std::ostringstream out;
  for (const auto& item : items) {
    auto it = std::find(items.begin(), items.end(), item); // O(n)
    int index = static_cast<int>(std::distance(items.begin(), it));
    out << "Item " << (index + 1) << ": " << item << '\n';
  }
  return out.str();
}

// O(n): 인덱스 루프
std::string buildListGood(const std::vector<std::string>& items) {
  std::ostringstream out;
  for (size_t i = 0; i < items.size(); ++i) {
    out << "Item " << (i + 1) << ": " << items[i] << '\n';
  }
  return out.str();
}
```

### Set/Map: 조회는 O(1), 빌드는 O(n)

```cpp
// 빈번 조회 시에만 unordered_set을 재사용하세요
std::vector<std::string> items = {"apple", "banana", "cherry"};
std::unordered_set<std::string> itemSet(items.begin(), items.end()); // 평균 O(n)
bool hasBanana = itemSet.count("banana") > 0;                        // 평균 O(1)
```

### 캐싱으로 중복 계산 줄이기(팩토리얼)

```cpp
std::unordered_map<int, long long> memo{{0, 1}, {1, 1}};
long long factorial(int n) {
  auto it = memo.find(n);
  if (it != memo.end()) return it->second;
  long long result = static_cast<long long>(n) * factorial(n - 1);
  memo[n] = result;
  return result;
}
```

## 실무에서 자주 보는 실수와 개선 패턴

- **루프 내부의 선형 탐색 호출**: 예를 들어 `std::find`를 루프 안에서 호출하면 전체가 `O(n^2)`가 됩니다. 인덱스 기반 for 루프로 개선하세요.
- **즉석 Set/Map 빌드**: 조회는 평균 `O(1)`이지만 `std::unordered_set` 생성은 `O(n)`입니다. 빈번 조회가 아니라면 오히려 느려질 수 있습니다. 재사용 가능한 곳에서 한 번만 빌드하세요.
- **중복 계산**: 팩토리얼처럼 부분 문제가 반복되는 경우 **메모이제이션(캐시)**으로 평균 성능을 크게 개선할 수 있습니다.
- **항상 측정**: 온라인 글의 수치를 맹신하지 말고, 변경 전후를 **같은 환경에서 측정**해 실제 개선을 확인해야 합니다.

## 이렇게 읽으면 좋아요

- 처음엔 각 복잡도의 시각화를 통해 “성장률의 감각”을 익히고, 이어서 정렬/탐색 같은 친숙한 문제에 적용해 보세요. 마지막으로 자신의 코드에서 **루프 안의 비싼 호출**, **불필요한 자료구조 빌드**, **중복 계산**을 찾고 치환하면 즉각적인 체감 이득을 얻을 수 있습니다.

## 참고 링크

- [Sam Rose — Big O](https://samwho.dev/big-o/)
- [해다(HADA) 토픽 소개](https://news.hada.io/topic?id=22736)