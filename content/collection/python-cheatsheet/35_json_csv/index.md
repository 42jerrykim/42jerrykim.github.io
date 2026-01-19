---
draft: true
image: "wordcloud.png"
title: "[Python Cheatsheet] 35. JSON & CSV - 읽기/쓰기/인코딩"
slug: "read-write-json-csv-file-serialization-encoding-guide"
description: "JSON/CSV를 빠르게 읽고 쓰기 위한 치트시트입니다. json.load/dump 옵션(ensure_ascii/indent), DictReader/DictWriter, newline/encoding 주의점, 흔한 데이터 타입 이슈를 실전 최소 예제로 정리합니다."
lastmod: 2026-01-17
collection_order: 35
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - json
  - csv
  - serialization
  - 직렬화
  - deserialization
  - 역직렬화
  - encoding
  - 인코딩
  - utf-8
  - newline
  - file-io
  - 파일입출력
  - io
  - open
  - with
  - context-manager
  - 표준라이브러리
  - standard-library
  - DictReader
  - DictWriter
  - reader
  - writer
  - ensure_ascii
  - indent
  - sort_keys
  - datetime
  - 날짜시간
  - types
  - 자료형
  - list
  - dict
  - performance
  - 성능
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
  - unicode
  - 유니코드
  - locale
  - security
  - 보안
  - validation
  - 검증
  - errors
  - exceptions
  - 예외처리
---
JSON과 CSV는 데이터 교환의 표준 포맷입니다. 이 치트시트는 json/csv 표준 라이브러리로 안전하게 읽고 쓰는 패턴과 encoding/newline 설정의 함정을 정리합니다.

## 언제 이 치트시트를 보나?

- API/설정 파일(JSON)이나 엑셀 내보내기(CSV)를 다룰 때
- “한글이 \\\\uXXXX로 보이네?” 같은 출력 문제를 해결할 때

## 핵심 패턴

- JSON: `json.load(f)` / `json.dump(obj, f, ensure_ascii=False, indent=2)`
- CSV(특히 Windows): `open(..., newline="", encoding="utf-8")` + `csv` 사용
- CSV는 **문자열** 중심이라 타입 변환(int/float/date)을 명시적으로

## 최소 예제

```python
import json

data = {"name": "김", "count": 3}
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

```python
import json

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
print(data["count"])
```

```python
import csv

rows = [{"name": "a", "n": 1}, {"name": "b", "n": 2}]
with open("out.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["name", "n"])
    w.writeheader()
    w.writerows(rows)
```

```python
import csv

with open("out.csv", "r", newline="", encoding="utf-8") as f:
    r = csv.DictReader(f)
    for row in r:
        n = int(row["n"])  # 타입 변환은 명시적으로
        print(row["name"], n)
```

## 자주 하는 실수/주의점

- JSON 출력에서 한글을 그대로 보이게 하려면 `ensure_ascii=False`
- CSV는 환경에 따라 줄바꿈이 깨질 수 있음 → `newline=""` 권장
- JSON은 `datetime` 같은 객체를 바로 dump 못 함 → 문자열(ISO)로 변환해서 저장

## 관련 링크(공식 문서)

- [json — JSON encoder and decoder](https://docs.python.org/3/library/json.html)
- [csv — CSV File Reading and Writing](https://docs.python.org/3/library/csv.html)

