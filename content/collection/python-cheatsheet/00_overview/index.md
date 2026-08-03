---

slug: "roadmap-overview-essential-guide-for-efficient-curriculum"
image: "wordcloud.png"
title: "[Python Cheatsheet] 00. Overview - 사용법/커리큘럼/로드맵"
description: "파이썬 치트시트 컬렉션 68개 챕터를 효율적으로 활용하는 방법을 정리합니다. 10개 Section이 기초 문법부터 비동기·네트워크까지 이어지는 구성 원리, 각 챕터의 핵심 주제와 판단 기준, 이 컬렉션이 적합하지 않은 경우, 공식 문서로 이어지는 링크까지 함께 다룹니다."
lastmod: 2026-01-18
collection_order: 0
tags:
  - Python
  - Cheatsheet(치트시트)
  - Quick-Reference
  - Education(교육)
  - Guide(가이드)
  - Implementation(구현)
  - Grammar(문법)
  - String(문자열)
  - Data-Structures(자료구조)
  - Set
  - Error-Handling(에러처리)
  - IO(Input/Output)
  - Software-Architecture(소프트웨어아키텍처)
  - JSON(JavaScript Object Notation)
  - Logging(로깅)
  - Debugging(디버깅)
  - Testing(테스트)
  - Database(데이터베이스)
  - Priority-Queue(우선순위큐)
  - Deque
  - XML(eXtensible Markup Language)
  - Math(수학)
  - OS(운영체제)
  - Tutorial(튜토리얼)
  - Code-Quality(코드품질)
  - OOP(객체지향)
  - Tree(트리)
  - Concurrency(동시성)
  - Process
  - Factory
  - Design-Pattern(디자인패턴)
  - Decorator
  - Deployment(배포)
  - Documentation(문서화)
  - Best-Practices
---
이 컬렉션은 파이썬을 이미 어느 정도 아는 개발자가 **필요할 때 빠르게 꺼내 쓸 수 있도록** 핵심 패턴과 함정을 정리한 치트시트입니다. 처음 배우는 분보다는 "예전에 했는데 문법이 기억 안 날 때" 참고하기 좋습니다.

## 이 컬렉션을 어떻게 쓰면 좋을까?

이 컬렉션은 "처음부터 끝까지 정독"보다는 **필요할 때 빠르게 찾아 쓰는** 용도에 맞춘 파이썬 치트시트입니다.
각 페이지는 핵심만 요약하고, 더 자세한 내용은 공식 문서로 이어지도록 구성합니다.

이 컬렉션은 서드파티 패키지 없이 파이썬 표준 라이브러리(stdlib)만으로 해결 가능한 범위로 의도적으로 제한합니다 — NumPy·pandas 같은 데이터 사이언스 라이브러리나 Django·FastAPI 같은 웹 프레임워크는 각자 학습 곡선과 생태계가 크기 때문에 다루지 않고, 별도 컬렉션이나 글로 남겨둡니다. 완전히 처음 파이썬을 배운다면 문법이 왜 그렇게 동작하는지부터 설명하는 튜토리얼(예: 아래 참고 링크의 The Python Tutorial)이 먼저입니다. 이 컬렉션은 그런 기초를 마친 뒤 "지금 이 상황에 표준 라이브러리의 어떤 도구를 써야 하는가"를 판단하는 데 특화되어 있습니다. 목차를 훑어보고 필요한 챕터로 바로 이동하거나, 브라우저 검색(Ctrl+F)으로 함수·모듈 이름을 찾는 방식이 가장 효율적입니다.

### 각 챕터의 공통 구조

68개 챕터는 모두 같은 구조를 따릅니다. "언제 이 치트시트를 보나?"는 어떤 상황에서 이 챕터를 펼쳐야 하는지 알려주는 트리거이고, "핵심 패턴"은 실무에서 가장 자주 쓰는 코드 조각을 압축한 목록입니다. 이어지는 "최소 예제"는 그 패턴을 실행 가능한 코드로 보여주고, "자주 하는 실수/주의점"은 겉보기엔 동작하지만 실제로는 함정인 코드를 짚습니다 — 예를 들어 50절은 토큰 생성에 `secrets` 대신 `random`을 쓰는 실수를, 42절은 신뢰할 수 없는 데이터를 `pickle`로 역직렬화했을 때의 보안 위험을 다룹니다. 마지막 "관련 링크(공식 문서)"는 더 깊이 알고 싶을 때 찾아갈 1차 출처입니다. 이 구조를 알고 나면, 급할 때는 "핵심 패턴"만 훑고 코드가 예상과 다르게 동작할 때는 "자주 하는 실수"부터 확인하는 식으로 챕터를 더 빠르게 활용할 수 있습니다.

## 왜 이 순서로 구성했는가

10개 Section은 파이썬 문법(Section 1) → 실행 환경 구성(2) → 데이터 설계(3) → 데이터 가공(4) → 외부 포맷 교환(5) → 수치·보안(6) → 시스템 제어(7) → 검증(8) → 배포(9) → 네트워크 통신(10) 순으로, "코드 한 줄을 작성하는 단계"에서 시작해 "그 코드가 다른 프로그램과 통신하는 단계"까지 점점 넓어지는 흐름을 따릅니다. 예를 들어 Section 3의 dataclass는 Section 1의 클래스 문법을 전제로 하고, Section 9의 pyproject.toml 의존성 명세(62절)는 Section 2에서 다룬 venv·pip의 의존성 개념(15절)을 프로젝트 배포 시점까지 그대로 이어받는 식으로 뒤 Section이 앞 Section의 개념을 재사용합니다.

다만 이 순서가 이 블로그의 다른 커리큘럼 컬렉션(cleanarchitecture, optimization 시리즈 등)처럼 앞 장을 반드시 알아야 다음 장을 이해할 수 있는 강한 선형 의존은 아닙니다. 치트시트도 커리큘럼처럼 처음부터 순서대로 읽어야 한다고 흔히 오해하지만, 이 컬렉션의 각 챕터는 독립적인 참고 카드에 가깝습니다 — Section 번호는 학습 순서가 아니라 정리를 위한 분류 기준입니다. 예를 들어 44절 Database 챕터만 필요하다면 01절부터 순서대로 읽을 필요 없이 바로 이동해도 무리가 없습니다.

| Section | 챕터 범위 | 핵심 목적 |
|---|---|---|
| 1 | 01–12 | 파이썬 문법의 뼈대(변수·제어흐름·함수·클래스) |
| 2 | 13–18 | 파일·모듈·가상환경 등 실행 환경 구성 |
| 3 | 19–27 | 타입힌트·dataclass·metaclass 등 데이터 모델링 |
| 4 | 28–34 | itertools·functools 등 함수형·이터레이터 유틸리티 |
| 5 | 35–45 | JSON·XML·datetime 등 외부 데이터 포맷 처리 |
| 6 | 46–50 | 통계·정밀 연산·난수·해시 등 수치·보안 |
| 7 | 51–56 | os·sys·시그널 등 시스템 수준 제어 |
| 8 | 57–61 | 로깅·디버깅·테스트·프로파일링 검증 |
| 9 | 62 | pyproject.toml 등 패키징·배포 |
| 10 | 63–68 | asyncio·소켓 등 비동기·네트워크 통신 |

위 표가 "어느 Section에 무엇이 있는지"를 훑어보는 용도라면, 아래 상세 목록은 실제로 클릭해 이동할 챕터 링크입니다. Section 제목 아래에 그 구간의 챕터들이 왜 한 묶음으로 분류됐는지 한두 문장으로 먼저 설명하고, 이어서 개별 챕터 링크를 나열합니다.

### 배경에 따라 다르게 시작하기

이미 다른 언어(Java, C++, Go 등) 경험이 있는 개발자라면 Section 1(기초 문법)은 훑어보는 정도로 충분하고, Section 3(타입/데이터 모델링)이나 Section 7(시스템/파일)처럼 파이썬 고유의 관용구가 강한 구간부터 읽는 편이 효율적입니다. 데이터를 다루는 업무가 많다면 Section 5(데이터 처리)와 Section 6(수학/보안)을, 웹 서버·API를 다룬다면 Section 10(비동기/네트워크)을 먼저 펼쳐도 됩니다. 반대로 코드 품질과 유지보수를 고민하는 단계라면 Section 8(디버깅/테스팅/성능)이 가장 먼저 필요한 구간일 수 있습니다. 이렇게 배경과 목적에 따라 진입점이 달라지는 것이, 이 컬렉션을 순서대로 읽는 커리큘럼이 아니라 색인에 가깝다고 설명한 이유입니다.

---

## 커리큘럼 (총 68개 챕터)

### Section 1: 기초 문법

변수·연산자·문자열·컬렉션·제어 흐름·함수·클래스·데코레이터·컴프리헨션·예외 처리·컨텍스트 매니저까지, 파이썬 문법의 뼈대를 다룹니다. 이후 모든 Section이 이 문법 위에서 동작하므로, 낯선 문법이 나오면 먼저 이 구간부터 확인하는 편이 빠릅니다.

- [01. Basic - 연산자, 변수, 출력, 형변환]({{< relref "collection/python-cheatsheet/01_basic/index.md" >}})
- [02. 내장 함수들]({{< relref "collection/python-cheatsheet/02_built_in_function/index.md" >}})
- [03. Strings - 슬라이싱/포맷팅/검색/치환]({{< relref "collection/python-cheatsheet/03_strings/index.md" >}})
- [04. Collections - list/tuple/set 패턴]({{< relref "collection/python-cheatsheet/04_collections_list_tuple_set/index.md" >}})
- [05. dict 패턴 - 조회/기본값/카운팅/병합]({{< relref "collection/python-cheatsheet/05_dict_patterns/index.md" >}})
- [06. Control Flow - if/for/while 패턴]({{< relref "collection/python-cheatsheet/06_control_flow/index.md" >}})
- [07. Functions - 인자/리턴/*args/**kwargs]({{< relref "collection/python-cheatsheet/07_functions_params/index.md" >}})
- [08. OOP & Classes - 클래스/상속/프로퍼티]({{< relref "collection/python-cheatsheet/08_oop_classes/index.md" >}})
- [09. Decorators - 함수/클래스 데코레이터]({{< relref "collection/python-cheatsheet/09_decorators/index.md" >}})
- [10. Comprehensions & Generators]({{< relref "collection/python-cheatsheet/10_comprehensions_generators/index.md" >}})
- [11. Errors & Exceptions - try/raise 패턴]({{< relref "collection/python-cheatsheet/11_errors_exceptions/index.md" >}})
- [12. Context Managers - with문/리소스 관리]({{< relref "collection/python-cheatsheet/12_context_managers/index.md" >}})

### Section 2: 파일/모듈/환경

Section 1의 문법을 실제 스크립트·프로젝트로 옮기는 데 필요한 파일 입출력, 모듈 구조, 가상환경, 커맨드라인 인자, 외부 프로세스 실행을 다룹니다. 코드 한 조각이 아니라 실행 가능한 프로그램을 만들 때 필요한 지식입니다.

- [13. Files - pathlib/encoding/open 패턴]({{< relref "collection/python-cheatsheet/13_files_pathlib_encoding/index.md" >}})
- [14. Modules & Imports - 구조/엔트리포인트]({{< relref "collection/python-cheatsheet/14_modules_imports/index.md" >}})
- [15. venv & pip - 환경/의존성 기본]({{< relref "collection/python-cheatsheet/15_venv_pip_tools/index.md" >}})
- [16. Environment Variables - os.environ/dotenv]({{< relref "collection/python-cheatsheet/16_env_variables/index.md" >}})
- [17. argparse & CLI - 커맨드라인 인자 처리]({{< relref "collection/python-cheatsheet/17_argparse_cli/index.md" >}})
- [18. subprocess - 외부 프로세스 실행]({{< relref "collection/python-cheatsheet/18_subprocess/index.md" >}})

### Section 3: 타입/데이터 모델링

변수에 타입을 명시하고(typing), 데이터를 구조화하고(dataclasses, Enum), 객체의 동작을 세밀하게 제어하는(descriptor, metaclass, ABC) 방법을 다룹니다. Section 1의 클래스 문법을 실전 설계 도구로 확장한 영역입니다.

- [19. Typing - 실전 타입힌트 패턴]({{< relref "collection/python-cheatsheet/19_typing_practical/index.md" >}})
- [20. dataclasses - default_factory/frozen 패턴]({{< relref "collection/python-cheatsheet/20_dataclasses_attrs/index.md" >}})
- [21. Enum & Flag - 열거형 실전 패턴]({{< relref "collection/python-cheatsheet/21_enum_flag/index.md" >}})
- [22. copy - 얕은/깊은 복사 패턴]({{< relref "collection/python-cheatsheet/22_copy_deepcopy/index.md" >}})
- [23. match-case - 구조적 패턴 매칭 (Py3.10+)]({{< relref "collection/python-cheatsheet/23_match_case/index.md" >}})
- [24. ABC - 추상 클래스 정의 패턴]({{< relref "collection/python-cheatsheet/24_abc_abstract/index.md" >}})
- [25. Metaclass - 클래스를 만드는 클래스]({{< relref "collection/python-cheatsheet/25_metaclass/index.md" >}})
- [26. Descriptor - 속성 접근 제어 프로토콜]({{< relref "collection/python-cheatsheet/26_descriptor/index.md" >}})
- [27. inspect - 런타임 객체 검사]({{< relref "collection/python-cheatsheet/27_inspect/index.md" >}})

### Section 4: 함수형/이터레이터/유틸리티

itertools·functools·operator처럼 반복 가능한 데이터를 다루는 함수형 도구와, deque·heapq 같은 표준 라이브러리 자료구조를 다룹니다. Section 3에서 정의한 데이터 구조를 효율적으로 순회·가공할 때 쓰입니다.

- [28. itertools & functools - 자주 쓰는 조합]({{< relref "collection/python-cheatsheet/28_itertools_functools/index.md" >}})
- [29. operator - 연산자 함수와 효율적 접근자]({{< relref "collection/python-cheatsheet/29_operator/index.md" >}})
- [30. collections 심화 - deque/namedtuple/ChainMap]({{< relref "collection/python-cheatsheet/30_collections_advanced/index.md" >}})
- [31. heapq & bisect - 우선순위 큐/이진 검색]({{< relref "collection/python-cheatsheet/31_heapq_bisect/index.md" >}})
- [32. contextlib 심화 - suppress, redirect, ExitStack]({{< relref "collection/python-cheatsheet/32_contextlib_advanced/index.md" >}})
- [33. textwrap - 텍스트 정렬과 줄바꿈]({{< relref "collection/python-cheatsheet/33_textwrap/index.md" >}})
- [34. pprint & reprlib - 예쁜 출력과 요약]({{< relref "collection/python-cheatsheet/34_pprint_reprlib/index.md" >}})

### Section 5: 데이터 처리

JSON·XML·CSV 같은 외부 포맷을 읽고 쓰는 방법과 날짜·정규식·URL·바이너리 데이터 처리를 다룹니다. Section 4의 유틸리티로 가공한 데이터를 실제로 저장하거나 외부 시스템과 주고받을 때 필요합니다.

- [35. JSON & CSV - 읽기/쓰기/인코딩]({{< relref "collection/python-cheatsheet/35_json_csv/index.md" >}})
- [36. XML - ElementTree로 XML 파싱/생성]({{< relref "collection/python-cheatsheet/36_xml/index.md" >}})
- [37. datetime - timezone/파싱/포맷]({{< relref "collection/python-cheatsheet/37_datetime_timezone/index.md" >}})
- [38. zoneinfo - 표준 시간대 (Python 3.9+)]({{< relref "collection/python-cheatsheet/38_zoneinfo/index.md" >}})
- [39. Regex - 안전하게 쓰는 최소 패턴]({{< relref "collection/python-cheatsheet/39_regex_safely/index.md" >}})
- [40. urllib.parse - URL 파싱과 조립]({{< relref "collection/python-cheatsheet/40_urllib_parse/index.md" >}})
- [41. configparser & tomllib - INI/TOML 설정 파일]({{< relref "collection/python-cheatsheet/41_configparser_toml/index.md" >}})
- [42. pickle - 객체 직렬화 (보안 주의)]({{< relref "collection/python-cheatsheet/42_pickle/index.md" >}})
- [43. struct & bytes - 바이너리 데이터 처리]({{< relref "collection/python-cheatsheet/43_struct_bytes/index.md" >}})
- [44. Database - sqlite3/ORM 기본 패턴]({{< relref "collection/python-cheatsheet/44_database/index.md" >}})
- [45. weakref - 약한 참조와 메모리 관리]({{< relref "collection/python-cheatsheet/45_weakref/index.md" >}})

### Section 6: 수학/보안

통계·정밀 소수 연산·난수·해시처럼 수치와 보안이 얽힌 표준 라이브러리를 다룹니다. random과 secrets의 용도가 명확히 갈리는 지점(재현 가능한 난수 vs 암호학적으로 안전한 난수)처럼, 비슷해 보이지만 다른 도구를 구분하는 데 중점을 둡니다.

- [46. math & statistics - 수학/통계 함수]({{< relref "collection/python-cheatsheet/46_math_statistics/index.md" >}})
- [47. decimal & fractions - 정밀 수치 연산]({{< relref "collection/python-cheatsheet/47_decimal_fractions/index.md" >}})
- [48. random - 난수 생성과 무작위 선택]({{< relref "collection/python-cheatsheet/48_random/index.md" >}})
- [49. uuid - 고유 식별자 생성]({{< relref "collection/python-cheatsheet/49_uuid/index.md" >}})
- [50. hashlib & secrets - 해시/보안 난수]({{< relref "collection/python-cheatsheet/50_hashlib_secrets/index.md" >}})

### Section 7: 시스템/파일

os·sys 모듈로 운영체제와 인터프리터 정보에 직접 접근하고, 압축·시그널·프로그램 종료 처리처럼 스크립트가 운영체제와 상호작용하는 지점을 다룹니다. Section 2의 파일 입출력보다 한 단계 더 깊은 시스템 수준 제어입니다.

- [51. os 심화 - 파일시스템과 프로세스]({{< relref "collection/python-cheatsheet/51_os_advanced/index.md" >}})
- [52. sys 심화 - 인터프리터와 런타임 정보]({{< relref "collection/python-cheatsheet/52_sys_advanced/index.md" >}})
- [53. shutil & tempfile - 파일 복사/이동/임시파일]({{< relref "collection/python-cheatsheet/53_shutil_tempfile/index.md" >}})
- [54. zipfile & tarfile - 압축 파일 처리]({{< relref "collection/python-cheatsheet/54_zipfile_tarfile/index.md" >}})
- [55. signal - 시그널 처리]({{< relref "collection/python-cheatsheet/55_signal/index.md" >}})
- [56. atexit - 프로그램 종료 시 정리]({{< relref "collection/python-cheatsheet/56_atexit/index.md" >}})

### Section 8: 디버깅/테스팅/성능

로그·트레이스백 읽기, pdb 대화형 디버깅, unittest·pytest 테스트 작성, cProfile 성능 분석을 다룹니다. 지금까지 작성한 코드가 의도대로 동작하는지 검증하고 병목을 찾는 단계입니다.

- [57. Logging & Debugging - traceback 읽기]({{< relref "collection/python-cheatsheet/57_logging_debugging/index.md" >}})
- [58. pdb 심화 - 대화형 디버깅]({{< relref "collection/python-cheatsheet/58_pdb_advanced/index.md" >}})
- [59. Testing - unittest/pytest 관점]({{< relref "collection/python-cheatsheet/59_testing_basics/index.md" >}})
- [60. unittest.mock - 모킹과 패칭]({{< relref "collection/python-cheatsheet/60_unittest_mock/index.md" >}})
- [61. Profiling - cProfile/py-spy 성능 분석]({{< relref "collection/python-cheatsheet/61_profiling/index.md" >}})

### Section 9: 패키징

pyproject.toml 작성과 배포 체크리스트를 다룹니다. Section 8까지의 검증을 통과한 코드를 다른 사람이 설치해 쓸 수 있는 패키지로 만드는 마지막 단계입니다. 챕터가 하나뿐인 이유는 실무에서 배포 설정 문제가 반복적으로 재발하는 지점만 추려 압축했기 때문입니다.

- [62. Packaging - pyproject.toml/배포 체크리스트]({{< relref "collection/python-cheatsheet/62_packaging_advanced/index.md" >}})

### Section 10: 비동기/네트워크

asyncio 비동기 처리, threading·multiprocessing 선택 기준, HTTP 요청·서버, 소켓, 이메일 발송을 다룹니다. Section 1–9가 단일 프로세스 안에서의 코드 작성을 다뤘다면, 이 Section은 프로세스 경계를 넘어 다른 프로그램·네트워크와 통신하는 방법입니다.

- [63. asyncio - 비동기 최소 패턴]({{< relref "collection/python-cheatsheet/63_asyncio_patterns/index.md" >}})
- [64. Concurrency - threading/multiprocessing 선택]({{< relref "collection/python-cheatsheet/64_concurrency/index.md" >}})
- [65. HTTP Requests - urllib/requests 기본]({{< relref "collection/python-cheatsheet/65_http_requests/index.md" >}})
- [66. http.server - 간단한 HTTP 서버]({{< relref "collection/python-cheatsheet/66_http_server/index.md" >}})
- [67. socket - 소켓 프로그래밍 최소 패턴]({{< relref "collection/python-cheatsheet/67_socket_basics/index.md" >}})
- [68. email & smtplib - 이메일 작성/발송]({{< relref "collection/python-cheatsheet/68_email_smtplib/index.md" >}})

---

## 1차 출처를 활용하는 법

각 챕터 하단의 "관련 링크(공식 문서)"는 치트시트의 압축된 설명만으로 부족할 때를 위한 것입니다. 표준 라이브러리의 세부 동작은 파이썬 버전에 따라 달라질 수 있으므로(예: `match-case`는 3.10 이전 버전에는 아예 없고, `zoneinfo`는 3.9 미만에서는 서드파티 `backports.zoneinfo`로 대체해야 합니다), 프로덕션 코드에 적용하기 전에는 실행 중인 파이썬 버전의 공식 문서를 확인하는 편이 안전합니다. 이 페이지 하단의 참고 링크도 각 챕터의 링크와 마찬가지로 최신 3.x 버전 문서를 기준으로 합니다.

## 참고(공식 문서)

- [The Python Tutorial](https://docs.python.org/3/tutorial/index.html)
- [Built-in Functions](https://docs.python.org/3/library/functions.html)
- [Python Standard Library](https://docs.python.org/3/library/index.html)

## 학습 결과와 이 컬렉션이 적합하지 않은 경우

이 컬렉션을 참고하면서 얻는 것은 특정 문법을 외우는 것이 아니라, "지금 상황에 표준 라이브러리의 어떤 도구를 선택해야 하는가"를 판단하는 기준입니다. 예를 들어 난수가 필요할 때 재현 가능성이 중요하면 `random`을, 토큰·비밀번호처럼 예측 불가능해야 하면 `secrets`를 선택하는 판단(46–50절), CPU 바운드 작업에는 GIL(전역 인터프리터 락)을 우회하는 `multiprocessing`을, I/O 바운드 작업에는 `threading`이나 `asyncio`를 선택하는 판단(64절 Concurrency 챕터)처럼, 비슷해 보이는 도구 중 무엇을 언제 써야 하는지를 상황에 맞게 고를 수 있게 됩니다. 정규식이 사용자 입력을 그대로 받아 처리해도 되는지, 아니면 ReDoS(정규식 서비스 거부 공격) 위험이 있는 패턴인지 구분하는 판단(39절), pickle로 역직렬화하기 전에 데이터 출처를 신뢰할 수 있는지 확인해야 하는 이유(42절)도 같은 맥락입니다. 시그널을 무시해도 되는 상황과 반드시 정리 코드를 실행해야 하는 상황을 구분하는 판단(55절 signal, 56절 atexit), 성능 병목이 의심될 때 추측 대신 cProfile로 실제로 측정해야 하는 이유(61절 Profiling)도 마찬가지입니다.

다만 이 컬렉션에는 명확한 한계가 있습니다. 각 챕터가 독립적인 참고 카드로 설계되어 있어, 하나의 프로젝트를 요구사항 분석부터 아키텍처 설계·구현·배포까지 처음부터 끝까지 만들어가는 과정은 다루지 않습니다 — 이런 설계 관점이 필요하다면 이 블로그의 Clean Architecture 컬렉션이 더 적합합니다. 또한 설명이 압축되어 있어 파이썬 문법 자체를 처음 배우는 사람에게는 진입 장벽이 있습니다 — 이 경우 위에서 소개한 공식 The Python Tutorial을 먼저 읽는 편이 낫습니다. 언어 자체보다 Django·FastAPI 같은 특정 프레임워크의 사용법을 찾고 있다면 이 컬렉션의 범위 밖입니다.

이런 판단 기준은 stdlib 범위를 넘어서도 그대로 쓸 수 있습니다. 예를 들어 "재현 가능한 난수와 암호학적으로 안전한 난수를 구분해야 한다"는 감각은 NumPy의 난수 생성기를 쓸 때도, "CPU 바운드에는 프로세스, I/O 바운드에는 스레드나 코루틴"이라는 기준은 Django·FastAPI 같은 프레임워크에서 백그라운드 작업을 설계할 때도 동일하게 적용됩니다. 즉 이 컬렉션이 stdlib로 범위를 제한하는 것은 도구 목록을 좁히는 것이지, 판단 기준 자체를 좁히는 것은 아닙니다. 어떤 라이브러리를 쓰든 결국 "이 작업의 성격이 무엇인가"를 먼저 묻는 습관이 남기 때문입니다.

각 챕터는 독립적으로 참고할 수 있으며, 새로운 표준 라이브러리 주제가 추가되면 이 페이지의 커리큘럼 표도 함께 갱신됩니다.
