---

image: "wordcloud.png"
title: "[Python Cheatsheet] 61. Profiling - cProfile/py-spy 성능 분석"
slug: "profiling-cprofile-pyspy-performance-analysis-guide"
description: "파이썬 성능 분석을 빠르게 시작하기 위한 치트시트입니다. timeit 마이크로벤치마크, cProfile/pstats 함수별 분석, py-spy 샘플링 프로파일러, 병목 식별 접근법을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 61
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - profiling
  - 프로파일링
  - performance
  - 성능
  - optimization
  - 최적화
  - benchmark
  - 벤치마크
  - timeit
  - cProfile
  - profile
  - pstats
  - py-spy
  - line_profiler
  - memory_profiler
  - bottleneck
  - 병목
  - cpu
  - time
  - 시간
  - function-call
  - 함수호출
  - hotspot
  - 핫스팟
  - flame-graph
  - 플레임그래프
  - sampling
  - 샘플링
  - deterministic
  - overhead
  - 오버헤드
  - debugging
  - 디버깅
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
  - standard-library
  - 표준라이브러리
  - tools
  - 도구
  - cli
  - visualization
  - 시각화
---
성능 최적화는 "측정 먼저, 최적화 나중"이 원칙입니다. 이 치트시트는 timeit으로 마이크로벤치마크, cProfile로 함수별 분석, py-spy로 운영 환경 샘플링하는 방법을 정리합니다.

## 언제 이 치트시트를 보나?

- "왜 느리지?" 하고 병목 지점을 찾고 싶을 때
- 코드 변경 전후 성능을 **수치로** 비교하고 싶을 때

## 핵심 패턴

- 마이크로벤치마크: `timeit` (작은 코드 조각)
- 전체 프로파일링: `cProfile` + `pstats` (함수별 호출 횟수/시간)
- 운영 환경 샘플링: `py-spy` (프로세스 attach, 오버헤드 낮음)
- 라인별 분석: `line_profiler` (설치 필요)

## timeit - 마이크로벤치마크

```python
import timeit

# 문자열로 코드 전달
t = timeit.timeit('"-".join(str(i) for i in range(100))', number=10000)
print(f"{t:.4f}s")

# 함수로 전달
def test_func():
    return sum(range(1000))

t = timeit.timeit(test_func, number=10000)
print(f"{t:.4f}s")
```

```bash
# CLI에서 실행
python -m timeit '"-".join(str(i) for i in range(100))'
```

## cProfile - 함수별 프로파일링

```python
import cProfile
import pstats

def slow_function():
    total = 0
    for i in range(10000):
        total += sum(range(100))
    return total

# 프로파일 실행
profiler = cProfile.Profile()
profiler.enable()
slow_function()
profiler.disable()

# 결과 출력 (cumulative time 기준 상위 10개)
stats = pstats.Stats(profiler)
stats.sort_stats("cumulative")
stats.print_stats(10)
```

```bash
# CLI에서 실행
python -m cProfile -s cumulative my_script.py

# 파일로 저장 후 분석
python -m cProfile -o output.prof my_script.py
python -c "import pstats; p = pstats.Stats('output.prof'); p.sort_stats('cumulative').print_stats(20)"
```

## py-spy - 샘플링 프로파일러

```bash
# 설치
pip install py-spy

# 실행 중인 프로세스에 attach (PID)
py-spy top --pid 12345

# 스크립트 실행하면서 프로파일링
py-spy record -o profile.svg -- python my_script.py

# 플레임 그래프 생성
py-spy record --format speedscope -o profile.json -- python my_script.py
```

## 병목 식별 접근법

1. **전체 실행 시간** 확인 → `time python script.py`
2. **cProfile**로 가장 오래 걸리는 함수 찾기
3. 해당 함수 내부를 `line_profiler`로 라인별 분석 (필요 시)
4. 알고리즘/자료구조 개선 → 다시 측정
5. **측정 없이 최적화하지 말기**

## 자주 하는 실수/주의점

- **cProfile**은 오버헤드가 있음 → 상대적 비교는 괜찮지만 절대 시간은 실제보다 느림
- `timeit`은 **작은 코드 조각**에 적합 → 전체 프로그램 분석에는 cProfile
- 최적화 전에 **반드시 테스트 작성** → 최적화 후 동작이 바뀌면 안 됨
- I/O 대기 시간은 CPU 프로파일러로 잘 안 보임 → 필요 시 별도 분석

## pstats 주요 정렬 키

| 키 | 설명 |
|----|------|
| `cumulative` | 누적 시간 (하위 함수 호출 포함) |
| `tottime` | 해당 함수 자체 시간 (하위 호출 제외) |
| `calls` | 호출 횟수 |
| `filename` | 파일명 순 |

## 관련 링크(공식 문서)

- [timeit](https://docs.python.org/3/library/timeit.html)
- [cProfile and profile](https://docs.python.org/3/library/profile.html)
- [py-spy (GitHub)](https://github.com/benfred/py-spy)
