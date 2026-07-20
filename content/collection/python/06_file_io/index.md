---
draft: false
image: "wordcloud.png"
title: "[Python Master] 06. 파일 입출력 - 경로/인코딩/JSON·CSV"
slug: "python-file-io-pathlib-json-csv-encoding-guide"
description: "파일 읽기/쓰기, 경로 처리, 인코딩, 다양한 포맷(JSON/CSV 등) 기본을 다룹니다. 예외 처리와 컨텍스트 매니저를 통해 안전하게 I/O를 처리하는 습관을 만듭니다."
tags:
  - Python
  - Implementation(구현)
  - Software-Architecture(소프트웨어아키텍처)
  - Algorithm(알고리즘)
  - Backend(백엔드)
  - Best-Practices
  - Clean-Code(클린코드)
  - Refactoring(리팩토링)
  - Testing(테스트)
  - Debugging(디버깅)
  - Logging(로깅)
  - Security(보안)
  - Performance(성능)
  - Concurrency(동시성)
  - Async(비동기)
  - OOP(객체지향)
  - Data-Structures(자료구조)
  - DevOps
  - Deployment(배포)
  - Design-Pattern(디자인패턴)
  - Web(웹)
  - Database(데이터베이스)
  - Networking(네트워킹)
  - CI-CD(Continuous Integration/Continuous Deployment)
  - Automation(자동화)
  - Documentation(문서화)
  - Git
  - Code-Quality(코드품질)
lastmod: 2026-01-17
collection_order: 6
---
# 챕터 6: 파일 입출력

> "데이터는 프로그램의 연료다" - 파일을 통해 데이터를 영구적으로 저장하고 불러오는 방법을 마스터해봅시다.

## 학습 목표
- 파일을 안전하게 열고 닫을 수 있다
- 다양한 모드로 파일을 읽고 쓸 수 있다
- 파일 경로와 디렉토리를 효과적으로 다룰 수 있다
- 다양한 파일 형식을 처리할 수 있다

## 핵심 개념(이론)

### 1) 파일 입출력의 역할과 경계
이 챕터의 핵심은 “무엇을 할 수 있나”가 아니라, **어떤 문제를 해결하고 어디까지 책임지는지**를 분명히 하는 것입니다.
경계가 흐리면 코드는 커질수록 결합이 늘어나고 수정 비용이 커집니다.

### 2) 왜 이 개념이 필요한가(실무 동기)
실무에서는 예외 상황, 성능, 협업, 테스트가 항상 문제를 만듭니다.
따라서 이 주제는 기능이 아니라 <strong>품질(신뢰성/유지보수성/보안)</strong>을 위한 기반으로 이해해야 합니다.

### 3) 트레이드오프: 간단함 vs 확장성
대부분의 선택은 “더 단순하게”와 “더 확장 가능하게” 사이에서 균형을 잡는 일입니다.
초기에는 단순함을, 장기 운영/팀 협업이 커질수록 확장성을 더 우선합니다.

### 4) 실패 모드(Failure Modes)를 먼저 생각하라
무엇이 실패하는지(입력, I/O, 동시성, 외부 시스템)를 먼저 떠올리면 설계가 안정적으로 변합니다.
이 챕터의 예제는 실패 모드를 축소해서 보여주므로, 실제 적용 시에는 더 많은 방어가 필요합니다.

### 5) 학습 포인트: 외우지 말고 “판단 기준”을 남겨라
핵심은 API를 외우는 것이 아니라, “언제 무엇을 선택할지” 판단 기준을 정리하는 것입니다.
이 기준이 쌓이면 새로운 라이브러리/도구가 나와도 빠르게 적응할 수 있습니다.

## 선택 기준(Decision Guide)
- 기본은 **가독성/명확성** 우선(최적화는 측정 이후).
- 외부 의존이 늘수록 **경계/추상화**와 **테스트**를 먼저 강화.
- 복잡도가 증가하면 “규칙을 코드로”가 아니라 “구조로” 담는 방향을 고려.

## 흔한 오해/주의점
- 도구/문법이 곧 실력이라는 오해가 있습니다. 실력은 문제를 단순화하고 구조화하는 능력입니다.
- 극단적 최적화/과설계는 학습과 유지보수를 방해할 수 있습니다.

## 요약
- 파일 입출력는 기능이 아니라 구조/품질을 위한 기반이다.
- 트레이드오프와 실패 모드를 먼저 생각하고, 판단 기준을 남기자.

## 기본 파일 연산

### 파일 열기와 닫기

**기본 파일 열기:**

```python
# 기본적인 파일 열기 (권장하지 않는 방법)
file = open('example.txt', 'r', encoding='utf-8')
content = file.read()
file.close()  # 반드시 닫아야 함!

print(content)
```

**문제점과 개선된 방법:**

```python
# 예외 발생 시에도 안전한 파일 처리
file = None
try:
    file = open('example.txt', 'r', encoding='utf-8')
    content = file.read()
    print(content)
except FileNotFoundError:
    print("파일을 찾을 수 없습니다.")
except IOError:
    print("파일을 읽는 중 오류가 발생했습니다.")
finally:
    if file:
        file.close()
```

### with 문을 사용한 안전한 파일 처리

```python
# with 문 (컨텍스트 매니저) - 권장 방법
with open('example.txt', 'r', encoding='utf-8') as file:
    content = file.read()
    print(content)
# 자동으로 파일이 닫힘

# 여러 파일 동시 처리
with open('input.txt', 'r', encoding='utf-8') as infile, \
     open('output.txt', 'w', encoding='utf-8') as outfile:
    data = infile.read()
    processed_data = data.upper()  # 대문자로 변환
    outfile.write(processed_data)
```

### 파일 모드

```python
# 텍스트 모드
# 'r' - 읽기 (기본값)
# 'w' - 쓰기 (파일 내용 덮어쓰기)
# 'a' - 추가 (파일 끝에 내용 추가)
# 'x' - 배타적 생성 (파일이 이미 존재하면 에러)

# 읽기 모드
with open('data.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# 쓰기 모드 (기존 내용 삭제)
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write("새로운 내용")

# 추가 모드 (기존 내용 유지)
with open('log.txt', 'a', encoding='utf-8') as f:
    f.write("로그 메시지\n")

# 바이너리 모드
# 'rb', 'wb', 'ab' - 바이너리 읽기/쓰기/추가

with open('image.jpg', 'rb') as f:
    binary_data = f.read()

with open('copy.jpg', 'wb') as f:
    f.write(binary_data)
```

## 경로 처리: pathlib

파이썬 3.4부터 표준 라이브러리에 포함된 `pathlib` 모듈은 파일 경로를 문자열이 아니라 객체로 다룬다. 문자열을 이어 붙이거나 `os.path.join`으로 경로를 조립하면 운영체제별 구분자 차이(윈도우 `\` vs 유닉스 `/`)를 신경 써야 하지만, `Path` 객체는 `/` 연산자를 오버로드해 현재 플랫폼에 맞는 경로를 자동으로 만들어 준다. 존재 여부 확인, 확장자 추출, 상위 디렉토리 접근처럼 예전에는 `os.path`와 `os` 모듈에 흩어져 있던 기능들이 모두 메서드로 통합되어 있어, 특별한 이유가 없다면 문자열 기반 경로 조작보다 `pathlib`를 우선 사용하는 것이 현재의 관례다.

```python
from pathlib import Path

# 현재 파일 기준 경로 생성
base_dir = Path(__file__).parent
data_file = base_dir / "data" / "input.txt"  # / 연산자로 경로 조합

print(data_file)
print(data_file.name)           # 파일명: input.txt
print(data_file.suffix)         # 확장자: .txt
print(data_file.stem)           # 확장자 제외 이름: input
print(data_file.parent)         # 상위 디렉토리
print(data_file.is_absolute())  # 절대 경로 여부
```

`Path` 객체는 경로 문자열을 만드는 데 그치지 않고 파일 시스템을 직접 조회하는 메서드도 제공한다. `exists()`로 존재 여부를, `is_file()`과 `is_dir()`로 종류를, `glob()`으로 패턴에 맞는 파일 목록을 얻을 수 있다. 이 메서드들은 내부적으로 `stat` 계열 시스템 콜을 호출하므로, 파일이 아주 많은 디렉토리에서 반복 호출하면 비용이 누적된다는 점은 기억해 둘 필요가 있다.

```python
from pathlib import Path

data_dir = Path("data")

if not data_dir.exists():
    data_dir.mkdir(parents=True, exist_ok=True)  # 중간 디렉토리까지 한 번에 생성

# 확장자로 파일 검색 (바로 아래 단계만)
for csv_file in data_dir.glob("*.csv"):
    print(f"발견: {csv_file}")

# 하위 디렉토리까지 재귀적으로 탐색
for py_file in data_dir.rglob("*.py"):
    print(f"발견(재귀): {py_file}")

# 짧은 파일은 open() 없이 바로 읽고 쓸 수 있다
readme = data_dir / "readme.txt"
readme.write_text("설명 문서", encoding="utf-8")
print(readme.read_text(encoding="utf-8"))
```

`glob()`은 지정한 디렉토리 바로 아래만 검색하고 `rglob()`은 하위 디렉토리까지 재귀적으로 내려간다는 차이가 있다. `write_text`/`read_text`와 `write_bytes`/`read_bytes`는 `open()`과 `with` 문 없이 짧은 파일을 다룰 때 편리하지만, 대용량 파일이나 스트리밍 처리가 필요할 때는 다음 절에서 다루는 `open()` 기반 패턴을 사용해야 한다.

## 텍스트 파일을 줄 단위로 읽기

파일 전체를 `read()`로 한 번에 메모리에 올리는 방식은 작은 설정 파일에는 문제없지만, 크기를 예측할 수 없는 로그 파일 같은 데이터에는 위험하다. 파이썬의 파일 객체는 반복자(iterator) 프로토콜을 구현하고 있어서 `for line in f:` 형태로 순회하면 한 번에 한 줄씩만 메모리에 올리며 처리할 수 있다. 이 관용구는 파이썬에서 텍스트 파일을 읽는 가장 표준적인 방법이며, 내부적으로 버퍼링된 I/O를 사용하므로 한 줄씩 시스템 콜을 하는 것보다 훨씬 효율적으로 동작한다.

```python
# 권장: 한 줄씩 스트리밍하며 처리 (메모리 효율적)
with open("access.log", "r", encoding="utf-8") as f:
    for line_number, line in enumerate(f, start=1):
        line = line.rstrip("\n")  # 줄 끝 개행 문자 제거
        if "ERROR" in line:
            print(f"{line_number}: {line}")

# readlines()는 모든 줄을 리스트로 반환 (파일 전체가 메모리에 올라감)
with open("small_config.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    print(f"총 {len(lines)}줄")
```

`readlines()`는 전체 줄을 리스트로 반환하므로 인덱싱이나 슬라이싱이 필요한 짧은 파일에는 편리하지만, 파일이 크면 `for line in f:`보다 메모리를 훨씬 많이 사용한다는 차이가 있다. 줄 끝의 개행 문자(`\n`)는 자동으로 제거되지 않으므로 `rstrip("\n")`이나 `strip()`으로 정리하는 습관을 들이는 것이 좋다.

## 구조화된 데이터 포맷 다루기

텍스트 파일을 한 줄씩 읽는 것만으로는 설정값이나 표 형태 데이터를 다루기 번거롭다. 파이썬 표준 라이브러리는 JSON과 CSV라는 두 가지 널리 쓰이는 포맷을 위한 전용 모듈을 제공하며, 직접 문자열을 파싱하는 대신 이 모듈들을 사용하는 것이 오류를 줄이는 정석이다.

### JSON 읽기와 쓰기

JSON(JavaScript Object Notation)은 설정 파일, API 응답, 애플리케이션 간 데이터 교환에 널리 쓰이는 텍스트 기반 포맷이다. `json` 모듈은 파이썬 객체와 JSON 텍스트를 상호 변환하는 `load`/`dump`(파일 객체 대상)와 `loads`/`dumps`(문자열 대상) 네 가지 함수를 제공한다. 파이썬의 `dict`, `list`, `str`, `int`, `float`, `bool`, `None`은 각각 JSON의 object, array, string, number, boolean, null에 대응하므로 별도의 변환 로직 없이 바로 직렬화·역직렬화할 수 있다.

```python
import json

config = {
    "app_name": "MyApp",
    "version": "1.2.0",
    "debug": False,
    "max_connections": 100,
    "allowed_hosts": ["localhost", "127.0.0.1"],
}

# JSON 파일로 쓰기 (들여쓰기와 한글 유지 옵션)
with open("config.json", "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

# JSON 파일 읽기
with open("config.json", "r", encoding="utf-8") as f:
    loaded_config = json.load(f)

print(loaded_config["app_name"])
print(loaded_config["allowed_hosts"])
```

`indent` 옵션은 사람이 읽기 쉬운 형태로 출력하며, 지정하지 않으면 공백 없이 압축된 한 줄로 저장되어 파일 용량은 줄지만 가독성은 떨어진다. `ensure_ascii=False`를 지정하지 않으면 한글 등 비ASCII 문자가 `\uXXXX` 형태의 이스케이프 시퀀스로 저장되므로, 사람이 직접 열어볼 설정 파일이라면 반드시 함께 지정해야 한다. 존재하지 않는 키에 접근하거나 파일이 손상된 JSON을 담고 있으면 각각 `KeyError`와 `json.JSONDecodeError`가 발생하므로, 신뢰할 수 없는 입력을 다룰 때는 이를 함께 처리해야 한다.

### CSV 읽기와 쓰기

CSV(Comma-Separated Values)는 스프레드시트나 데이터베이스 내보내기에서 흔히 만나는 표 형태 텍스트 포맷이다. 콤마로 필드를 구분하는 형식 자체는 단순해 보이지만, 필드 안에 콤마나 줄바꿈이 포함된 경우를 처리하려면 따옴표 이스케이프 규칙이 필요하다. 이 규칙을 문자열 `split(",")`로 직접 구현하면 이런 경계 사례에서 쉽게 깨지므로, 표준 라이브러리 `csv` 모듈을 사용하는 것이 정석이다.

```python
import csv

rows = [
    ["이름", "국어", "영어", "수학"],
    ["김철수", "90", "85", "95"],
    ["이영희", "88", "92", "79"],
]

# CSV 쓰기 (newline="" 지정이 중요: 빈 줄 삽입 방지)
with open("scores.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

# CSV 읽기: 각 행이 리스트로 반환됨
with open("scores.csv", "r", encoding="utf-8", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)  # 첫 줄은 헤더로 소비
    for row in reader:
        print(dict(zip(header, row)))
```

`open()`에 `newline=""`을 지정하지 않으면 윈도우 환경에서 줄마다 빈 줄이 하나씩 추가로 삽입될 수 있다. 텍스트 모드의 자동 개행 변환과 CSV 모듈 자체의 개행 처리가 중복되기 때문이며, 공식 문서에서도 CSV 파일을 다룰 때는 항상 `newline=""`을 명시하도록 권장한다.

행을 리스트가 아니라 딕셔너리로 다루고 싶다면 `DictReader`와 `DictWriter`를 사용한다. 헤더 행을 자동으로 키로 사용하므로 열 순서에 의존하지 않고 열 이름으로 값에 접근할 수 있어, 열 순서가 바뀌거나 일부 열이 누락될 수 있는 실무 데이터에 더 안전하다.

```python
import csv

# DictWriter: 딕셔너리 리스트를 CSV로 저장
students = [
    {"name": "김철수", "korean": 90, "english": 85, "math": 95},
    {"name": "이영희", "korean": 88, "english": 92, "math": 79},
]

fieldnames = ["name", "korean", "english", "math"]
with open("students.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(students)

# DictReader: 각 행이 딕셔너리로 반환됨
with open("students.csv", "r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        avg = (int(row["korean"]) + int(row["english"]) + int(row["math"])) / 3
        print(f"{row['name']}: 평균 {avg:.1f}")
```

`DictReader`가 반환하는 값은 모두 문자열이므로, 숫자 연산이 필요하면 `int()`나 `float()`로 명시적으로 변환해야 한다는 점을 잊지 않아야 한다.

## 대용량 파일과 인코딩 오류 처리

파일 크기가 사용 가능한 메모리보다 클 수 있는 상황과, 파일의 실제 인코딩이 예상과 다른 상황은 파일 입출력에서 가장 흔하게 마주치는 두 가지 문제다. 아래에서는 각각을 다루는 표준적인 방법을 살펴본다.

### 스트리밍 읽기 패턴

로그 파일이나 대용량 데이터셋처럼 크기를 예측할 수 없는 파일은 `read()`나 `readlines()`로 전체를 한 번에 불러오면 안 된다. 앞서 본 `for line in f:` 패턴이 바로 이런 상황을 위한 것으로, 파일 객체가 내부 버퍼만 유지한 채 요청할 때마다 다음 줄을 반환하므로 파일 크기와 무관하게 메모리 사용량이 일정하게 유지된다. 집계나 필터링처럼 전체 데이터를 동시에 들고 있을 필요가 없는 작업이라면 이 스트리밍 패턴을 항상 먼저 고려해야 한다.

```python
def count_error_lines(filepath):
    """대용량 로그 파일에서 ERROR 줄만 세기 (메모리에 전체를 올리지 않음)"""
    error_count = 0
    total_count = 0

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:  # 한 줄씩만 메모리에 존재
            total_count += 1
            if "ERROR" in line:
                error_count += 1

    return error_count, total_count

errors, total = count_error_lines("huge_access.log")
print(f"{total}줄 중 {errors}줄이 에러")
```

### 인코딩 오류 처리

파일을 열 때 지정한 인코딩이 실제 파일의 바이트 인코딩과 다르면 `UnicodeDecodeError`가 발생한다. 예를 들어 EUC-KR로 저장된 한글 파일을 `encoding="utf-8"`로 열면 특정 바이트 시퀀스가 유효한 UTF-8 문자로 해석되지 않아 예외가 발생한다. `open()`의 `errors` 매개변수로 이런 상황에서의 동작을 지정할 수 있는데, 기본값 `"strict"`는 예외를 발생시키고 `"replace"`는 깨진 문자를 대체 문자(U+FFFD)로 바꾸며 `"ignore"`는 해당 바이트를 조용히 건너뛴다.

```python
# 인코딩이 맞지 않으면 예외 발생
try:
    with open("legacy_data.txt", "r", encoding="utf-8") as f:
        content = f.read()
except UnicodeDecodeError as e:
    print(f"인코딩 오류: {e}")
    # 실제 인코딩을 모른다면 errors 옵션으로 완화하거나
    # chardet 같은 서드파티 라이브러리로 인코딩을 추정한다

# 깨진 문자를 대체 문자로 바꾸며 읽기 (데이터 손실 감수)
with open("legacy_data.txt", "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

# 깨진 바이트를 건너뛰며 읽기
with open("legacy_data.txt", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()
```

`errors="replace"`나 `"ignore"`는 예외를 피할 수 있지만 원본 데이터의 일부가 손실되거나 왜곡된다는 대가를 치르므로 임시방편에 가깝다. 운영 환경에서는 파일의 실제 인코딩을 정확히 파악해 올바른 `encoding` 값을 지정하는 것이 근본적인 해결책이며, 인코딩을 알 수 없는 레거시 파일을 다뤄야 한다면 `chardet` 같은 서드파티 라이브러리로 인코딩을 추정하는 방법도 있다.

## 실습 프로젝트

### 프로젝트 1: CSV 성적 처리기

학생들의 성적이 담긴 CSV 파일을 읽어 과목별 평균과 학생별 총점 등수를 계산하고, 결과를 새로운 CSV 파일로 저장하는 프로그램이다. `csv.DictReader`로 입력을 읽고 `csv.DictWriter`로 출력을 쓰는, 앞에서 다룬 CSV 처리 방법을 그대로 활용한다.

```python
import csv
from pathlib import Path


def load_scores(filepath):
    """CSV 파일에서 학생 성적을 읽어 딕셔너리 리스트로 반환"""
    with open(filepath, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def calculate_subject_averages(students, subjects):
    """과목별 평균 점수 계산"""
    averages = {}
    for subject in subjects:
        scores = [int(s[subject]) for s in students]
        averages[subject] = sum(scores) / len(scores)
    return averages


def rank_students(students, subjects):
    """학생별 총점 기준 등수 매기기"""
    for student in students:
        student["총점"] = sum(int(student[subject]) for subject in subjects)

    ranked = sorted(students, key=lambda s: s["총점"], reverse=True)
    for rank, student in enumerate(ranked, start=1):
        student["등수"] = rank
    return ranked


def save_report(students, subjects, output_path):
    """등수가 매겨진 결과를 CSV로 저장"""
    fieldnames = ["name"] + subjects + ["총점", "등수"]
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for student in students:
            writer.writerow({key: student[key] for key in fieldnames})


def main():
    input_path = Path("scores.csv")
    output_path = Path("report.csv")
    subjects = ["korean", "english", "math"]

    # 입력 파일이 없으면 예제 데이터를 생성
    if not input_path.exists():
        sample = [
            {"name": "김철수", "korean": "90", "english": "85", "math": "95"},
            {"name": "이영희", "korean": "88", "english": "92", "math": "79"},
            {"name": "박민수", "korean": "76", "english": "80", "math": "88"},
        ]
        with open(input_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["name"] + subjects)
            writer.writeheader()
            writer.writerows(sample)

    students = load_scores(input_path)
    averages = calculate_subject_averages(students, subjects)
    for subject, avg in averages.items():
        print(f"{subject} 평균: {avg:.1f}")

    ranked = rank_students(students, subjects)
    save_report(ranked, subjects, output_path)
    print(f"결과 저장: {output_path}")


if __name__ == "__main__":
    main()
```

이 프로그램의 함수들은 각각 읽기, 계산, 정렬, 쓰기라는 단일 책임만 맡도록 나뉘어 있다. `load_scores`가 파일 형식을 몰라도 되도록 `main`이 조립을 담당하는 구조는, 이후 입력 소스를 CSV에서 JSON이나 데이터베이스로 바꿔야 할 때 `load_scores` 함수 하나만 교체하면 되게 해 준다.

### 프로젝트 2: JSON 설정 파일 관리자

애플리케이션 설정을 JSON 파일로 관리하면서, 파일이 없으면 기본값으로 생성하고 값을 변경하면 즉시 저장하는 간단한 설정 관리자다. 실무에서 반복되는 "설정 로드 → 기본값 병합 → 변경 시 저장" 패턴을 하나의 클래스로 캡슐화한다.

```python
import json
from pathlib import Path


class ConfigManager:
    """JSON 파일 기반 설정 관리자"""

    DEFAULTS = {
        "app_name": "MyApp",
        "debug": False,
        "max_connections": 100,
        "log_level": "INFO",
    }

    def __init__(self, config_path):
        self.config_path = Path(config_path)
        self.data = self._load()

    def _load(self):
        """설정 파일을 읽되, 없으면 기본값으로 새로 생성"""
        if not self.config_path.exists():
            self._save(self.DEFAULTS.copy())
            return self.DEFAULTS.copy()

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print("설정 파일이 손상되어 기본값으로 복구합니다.")
            data = self.DEFAULTS.copy()
            self._save(data)

        # 기본값에는 있지만 파일에는 없는 키를 보완 (버전 업그레이드 대응)
        merged = {**self.DEFAULTS, **data}
        return merged

    def _save(self, data=None):
        data = data if data is not None else self.data
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self._save()


def main():
    config = ConfigManager("app_config.json")

    print(f"현재 앱 이름: {config.get('app_name')}")
    print(f"디버그 모드: {config.get('debug')}")

    config.set("debug", True)
    config.set("max_connections", 200)
    print("설정 변경 완료:")
    print(f"디버그 모드: {config.get('debug')}")
    print(f"최대 연결 수: {config.get('max_connections')}")


if __name__ == "__main__":
    main()
```

`_load` 메서드에서 `{**self.DEFAULTS, **data}`로 딕셔너리를 병합하는 부분이 핵심이다. 프로그램 버전이 올라가며 새로운 설정 키가 추가되어도, 사용자가 예전 버전에서 저장한 설정 파일에는 그 키가 없을 수 있다. 기본값을 먼저 펼치고 저장된 값으로 덮어쓰는 순서로 병합하면 새 키는 기본값을 갖고 기존 키는 사용자 설정을 유지하는 하위 호환 동작을 자연스럽게 얻는다.

## 체크리스트

### 기본 파일 연산
- [ ] with 문으로 파일을 열고 자동으로 닫을 수 있다
- [ ] 텍스트/바이너리, 읽기/쓰기/추가 모드의 차이를 설명할 수 있다
- [ ] 예외가 발생해도 파일이 안전하게 닫히는 이유를 설명할 수 있다

### 경로와 텍스트 처리
- [ ] pathlib의 Path 객체로 경로를 조합하고 탐색할 수 있다
- [ ] glob()과 rglob()의 차이를 설명할 수 있다
- [ ] for line in f: 와 readlines()의 메모리 사용 차이를 설명할 수 있다

### 데이터 포맷
- [ ] json.load/dump로 설정 파일을 읽고 쓸 수 있다
- [ ] csv.DictReader/DictWriter로 표 형태 데이터를 다룰 수 있다
- [ ] CSV 파일을 열 때 newline=""이 필요한 이유를 설명할 수 있다

### 대용량 파일과 인코딩
- [ ] 대용량 파일을 스트리밍으로 처리하는 패턴을 구현할 수 있다
- [ ] UnicodeDecodeError가 발생하는 원인과 errors 옵션의 차이를 설명할 수 있다

## 다음 단계

파일 입출력의 기본기를 다졌습니다. 이제 [07. 예외 처리](/post/python/python-exception-handling-try-except-finally-custom-errors-guide/)로 넘어가서 파일이 없거나 손상된 경우처럼 예측 가능한 실패를 안전하게 다루는 방법을 학습해봅시다.

---

**팁:**
- CSV/JSON처럼 구조화된 포맷은 문자열을 직접 파싱하지 말고 표준 라이브러리를 우선 사용하세요
- 대용량 파일은 항상 전체를 메모리에 올리기 전에 스트리밍 처리가 가능한지 먼저 검토하세요
- 파일 경로 조작은 os.path보다 pathlib을 우선 사용하는 것이 최신 관례입니다

