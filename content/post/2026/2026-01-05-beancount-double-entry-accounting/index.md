---
title: "[Finance] Beancount - 텍스트 파일 기반 복식 부기 시스템"
categories:
- Accounting
- Finance
- OpenSource
- Python
tags:
- Beancount
- accounting
- double_entry_bookkeeping
- finance
- personal_finance
- financial_management
- open_source
- Python
- text_based
- command_line
- CLI
- accounting_software
- bookkeeping
- ledger
- plain_text
- financial_records
- transaction_tracking
- budget
- expense_tracking
- income_tracking
- financial_reports
- balance_sheet
- income_statement
- tax_reporting
- investment_tracking
- portfolio_management
- asset_management
- liability_management
- equity_tracking
- journal_entries
- chart_of_accounts
- financial_analysis
- GPL_license
- Martin_Blais
- Github
- documentation
- web_interface
- data_visualization
- financial_planning
- 회계
- 복식부기
- 재무관리
- 개인재무
- 예산관리
- 지출추적
- 수입추적
- 자산관리
- 투자관리
- 포트폴리오
- 재무보고
- 세금신고
- 장부관리
- 재무분석
- 오픈소스
- 파이썬
- 텍스트파일
- 명령줄도구
- 재무데이터
- 거래기록
- 회계시스템
- 재무소프트웨어
image: "wordcloud.png"
description: "Beancount는 텍스트 파일로 재무 거래를 기록하는 오픈소스 복식 부기 시스템입니다. Python으로 개발되었으며 명령줄 환경에서 강력한 회계 기능을 제공하고 다양한 보고서를 생성할 수 있습니다."
date: 2026-01-05
lastmod: 2026-01-05
---

[Beancount](https://github.com/beancount/beancount)는 텍스트 파일을 사용하여 재무 거래를 기록하고 관리하는 복식 부기(Double-Entry Bookkeeping) 시스템입니다. Martin Blais가 개발한 이 오픈소스 프로젝트는 2007년부터 시작되어 현재까지 지속적으로 발전해왔으며, GitHub에서 5,000개 이상의 스타를 받은 인기 있는 회계 솔루션입니다.

전통적인 회계 소프트웨어들이 그래픽 사용자 인터페이스(GUI)와 데이터베이스를 사용하는 것과 달리, Beancount는 "코드로서의 회계(Accounting as Code)" 철학을 따릅니다. 이는 소프트웨어 개발자들이 코드를 관리하듯이 재무 데이터를 관리할 수 있게 해주며, Git과 같은 버전 관리 시스템, 텍스트 편집기, 명령줄 도구 등 개발자에게 익숙한 도구들을 그대로 활용할 수 있습니다.

Python으로 작성된 Beancount는 단순히 장부를 기록하는 것을 넘어, 강력한 보고 기능, 데이터 검증, 자동화된 거래 입력, 그리고 확장 가능한 플러그인 시스템을 제공합니다. 이러한 특징들 덕분에 개인 재무 관리부터 소규모 비즈니스 회계, 복잡한 투자 포트폴리오 추적까지 다양한 용도로 활용되고 있습니다.

## Beancount란 무엇인가?

Beancount는 금융 거래 기록을 텍스트 파일로 정의할 수 있는 컴퓨터 언어입니다. 이를 메모리에 읽어들여 다양한 보고서를 생성하고, 웹 인터페이스를 통해 시각적으로 확인할 수 있습니다. 전문적인 회계 지식이 없어도 개인 재무를 체계적으로 관리할 수 있는 강력한 도구입니다.

## 회계의 기본 개념: 단식 부기 vs 복식 부기

Beancount를 이해하기 위해서는 먼저 회계의 기본 개념인 단식 부기와 복식 부기의 차이를 알아야 합니다.

### 단식 부기(Single-Entry Bookkeeping)

단식 부기는 가장 간단한 형태의 장부 기록 방법으로, 많은 사람들이 일상적으로 사용하는 방식입니다.

**특징:**
- 각 거래를 한 번만 기록 (수입 또는 지출)
- 현금의 입출만 추적
- 가계부나 간단한 현금 출납부가 대표적인 예

**예시:**

```
날짜        내역             금액
2026-01-10  급여 입금       +3,000,000원
2026-01-15  식료품 구매      -150,000원
2026-01-20  월세 지불       -1,200,000원
잔액: 1,650,000원
```

**장점:**
- 간단하고 이해하기 쉬움
- 소규모 개인 재무 관리에 적합
- 빠르게 기록 가능

**단점:**
- 전체 재무 상태를 파악하기 어려움
- 자산, 부채, 자본의 관계를 추적할 수 없음
- 오류 검증이 어려움
- 복잡한 거래 처리 불가능

### 복식 부기(Double-Entry Bookkeeping)

복식 부기는 15세기 이탈리아에서 시작된 회계 방법으로, 현대 회계의 기본 원칙입니다. Beancount는 이 복식 부기 원칙을 따릅니다.

**핵심 원칙:**
- 모든 거래는 최소 두 개의 계정에 영향을 미침
- 차변(Debit)과 대변(Credit)의 합은 항상 0 (균형을 이룸)
- "돈이 어디서 왔고, 어디로 갔는지"를 정확히 추적

**예시 (같은 거래를 복식 부기로):**

```
# 급여 입금: 은행 계좌 증가, 급여 수입 발생
2026-01-10 급여
  Assets:Bank:Checking    +3,000,000원  (차변: 자산 증가)
  Income:Salary           -3,000,000원  (대변: 수입 발생)
  합계: 0원 (균형)

# 식료품 구매: 은행 계좌 감소, 식료품 비용 발생
2026-01-15 식료품
  Expenses:Groceries      +150,000원   (차변: 비용 발생)
  Assets:Bank:Checking    -150,000원   (대변: 자산 감소)
  합계: 0원 (균형)
```

**장점:**
- 완전한 재무 상태 파악 가능 (자산, 부채, 자본, 수익, 비용)
- 자동으로 오류 검증 (균형이 맞지 않으면 오류)
- 재무제표 자동 생성 가능
- 복잡한 거래도 정확히 추적
- 세금 신고 및 감사에 적합

**단점:**
- 학습 곡선이 있음
- 단식 부기보다 기록이 복잡함
- 초기 설정에 시간 필요

### 5가지 기본 계정 유형

복식 부기에서는 모든 계정을 5가지 유형으로 분류합니다:

1. **자산(Assets)**: 소유하고 있는 것
   - 현금, 은행 예금, 주식, 부동산, 자동차 등
   - 예: `Assets:Bank:Checking`, `Assets:Investments:Stocks`

2. **부채(Liabilities)**: 갚아야 하는 것
   - 대출, 신용카드 빚, 미지급금 등
   - 예: `Liabilities:CreditCard`, `Liabilities:Mortgage`

3. **자본(Equity)**: 순자산 (자산 - 부채)
   - 초기 자본, 이익잉여금 등
   - 예: `Equity:OpeningBalances`

4. **수익(Income)**: 들어오는 돈
   - 급여, 이자, 배당금, 사업 수입 등
   - 예: `Income:Salary`, `Income:Dividends`

5. **비용(Expenses)**: 나가는 돈
   - 식료품, 월세, 교통비, 세금 등
   - 예: `Expenses:Rent`, `Expenses:Groceries`

### 회계 등식

복식 부기의 핵심은 다음 등식이 항상 성립한다는 것입니다:

```
자산(Assets) = 부채(Liabilities) + 자본(Equity)
```

또는:

```
자산 = 부채 + 자본 + (수익 - 비용)
```

Beancount는 이 등식이 항상 성립하도록 자동으로 검증하며, 균형이 맞지 않으면 오류를 표시합니다.

### 왜 Beancount는 복식 부기를 사용하는가?

1. **정확성**: 자동 균형 검증으로 입력 오류를 즉시 발견
2. **완전성**: 재무 상태의 전체 그림 파악 가능
3. **전문성**: 실제 기업 회계 방식과 동일한 원칙 사용
4. **확장성**: 단순한 가계부부터 복잡한 투자 포트폴리오까지 처리 가능
5. **보고서**: 대차대조표, 손익계산서 등 전문적인 재무제표 자동 생성

단식 부기에 익숙한 사람들에게는 처음에 복잡해 보일 수 있지만, 복식 부기의 원칙을 이해하고 나면 훨씬 더 정확하고 체계적인 재무 관리가 가능해집니다. Beancount는 이러한 복식 부기의 장점을 텍스트 파일과 프로그래밍 방식으로 활용할 수 있게 해줍니다.

## 주요 특징

### 1. 텍스트 기반 데이터 관리

모든 재무 데이터를 평문(plain text) 파일로 저장합니다. 이는 다음과 같은 장점을 제공합니다:

- **버전 관리**: Git 등의 버전 관리 시스템으로 변경 이력 추적 가능
- **영구 보존**: 특정 소프트웨어에 종속되지 않아 데이터 손실 위험 최소화
- **편집 자유도**: 원하는 텍스트 에디터로 자유롭게 편집 가능
- **검색 및 자동화**: grep, sed 등 표준 유닉스 도구로 데이터 처리 가능

### 2. 자동 균형 검증 및 오류 감지

Beancount는 복식 부기 원칙을 엄격하게 적용하여 데이터의 정확성을 보장합니다:

- **자동 균형 체크**: 모든 거래의 차변과 대변 합계가 0인지 자동 검증
- **계정 유형 검증**: 잘못된 계정 유형 사용 시 오류 메시지 표시
- **날짜 순서 검증**: 거래가 논리적인 시간 순서로 기록되었는지 확인
- **계정 개설 검증**: 사용 전에 계정이 올바르게 개설되었는지 확인
- **통화 일관성**: 같은 거래 내에서 통화 단위가 일치하는지 검증
- **상세한 오류 메시지**: 문제 발생 시 정확한 위치와 원인을 알려줌

### 3. 강력한 보고 기능

다양한 형태의 재무 보고서를 생성할 수 있습니다:

- 잔액 조회(Balance Sheet)
- 손익 계산(Income Statement)
- 현금 흐름표(Cash Flow Statement)
- 계정별 거래 내역(Journal)
- 순자산 변화 추이
- 투자 포트폴리오 현황

### 4. 웹 인터페이스

내장된 웹 서버를 통해 브라우저에서 데이터를 시각적으로 확인할 수 있습니다:

- 대시보드 뷰
- 차트 및 그래프
- 계정별 상세 내역
- 문서 첨부 기능

## 왜 텍스트 기반 회계인가?

### 데이터 소유권과 통제

Excel이나 상용 회계 소프트웨어와 달리, Beancount는 사용자가 완전한 데이터 소유권과 통제권을 갖습니다. 데이터는 읽을 수 있는 평문 형태로 저장되며, 특정 소프트웨어나 서비스에 종속되지 않습니다.

### 프로그래머 친화적

코드를 다루듯이 재무 데이터를 다룰 수 있습니다:

- 스크립트를 작성하여 반복 거래 자동화
- 은행 명세서를 파싱하여 자동 입력
- Python API를 활용한 커스텀 분석 도구 개발
- 테스트 주도 회계 가능

### 투명성과 감사 가능성

모든 거래가 명시적으로 기록되며, 변경 사항은 버전 관리 시스템을 통해 추적됩니다. 이는 감사나 세금 신고 시 유용한 증거 자료가 됩니다.

## 버전 정보

Beancount는 세 가지 주요 버전이 있습니다:

### Version 3 (현재 안정 버전)

2024년 6월부터 공식 안정 버전으로 출시되었습니다. 이 버전은 v2에서 핵심 기능만 남기고 많은 도구들을 독립 프로젝트로 분리했습니다. 새로운 사용자는 이 버전을 사용해야 합니다.

### Version 2 (유지보수 모드)

2020년부터 2024년까지 유지보수 모드로 운영되었으며, 현재는 더 이상 업데이트되지 않습니다. 초기 버전의 완전한 재작성으로 새로운 문법과 제약사항을 도입했습니다.

### Version 1 (구버전)

2013년 개발이 중단된 최초 버전입니다. Ledger와 부분적으로 호환되도록 설계되었으나, 현재는 사용하지 않습니다.

## Beancount 파일 예제

다음은 간단한 Beancount 파일의 예시입니다:

```beancount
; 계정 정의
2026-01-01 open Assets:Checking:MyBank
2026-01-01 open Income:Salary
2026-01-01 open Expenses:Groceries
2026-01-01 open Expenses:Rent

; 초기 잔액
2026-01-01 * "Initial balance"
  Assets:Checking:MyBank    1000.00 USD

; 급여 입금
2026-01-15 * "January salary"
  Assets:Checking:MyBank    3000.00 USD
  Income:Salary            -3000.00 USD

; 식료품 구매
2026-01-20 * "Grocery shopping" "SuperMart"
  Expenses:Groceries         150.00 USD
  Assets:Checking:MyBank    -150.00 USD

; 월세 지불
2026-01-25 * "Monthly rent"
  Expenses:Rent             1200.00 USD
  Assets:Checking:MyBank   -1200.00 USD
```

이 예제는 다음을 보여줍니다:

- **계정 개설**: `open` 명령으로 계정 생성
- **거래 기록**: 날짜, 상태(\*), 설명, 계정별 금액
- **복식 부기**: 각 거래의 차변과 대변 합계는 0

## 설치 방법

### Python pip를 통한 설치

```bash
pip install beancount
```

### 소스에서 빌드

```bash
git clone https://github.com/beancount/beancount.git
cd beancount
pip install .
```

### 기본 사용법

```bash
# 파일 검증
bean-check myfinances.beancount

# 잔액 조회
bean-report myfinances.beancount balances

# 웹 인터페이스 실행
bean-web myfinances.beancount
```

## 생태계와 확장 도구

Beancount는 활발한 커뮤니티와 다양한 확장 도구를 보유하고 있습니다:

### 가져오기 도구

- **beancount-import**: 은행 명세서, 신용카드 내역 자동 가져오기
- **smart_importer**: 머신러닝을 활용한 거래 분류 자동화
- **plaid2beancount**: Plaid API를 통한 자동 데이터 동기화

### 시각화 도구

- **fava**: 현대적인 웹 인터페이스 (가장 인기 있는 확장)
- **beancount-web**: 공식 웹 인터페이스
- **beancount-mobile**: 모바일 앱

### 분석 도구

- **beancount-reds-importers**: 다양한 금융 기관 지원
- **beancount-interpolate**: 정기 거래 자동 생성
- **beancount-portfolio**: 투자 포트폴리오 분석

## 사용 사례

### 개인 재무 관리

- 일상적인 수입과 지출 추적
- 예산 관리 및 지출 분석
- 세금 신고 자료 준비
- 재무 목표 설정 및 추적

### 투자 관리

- 주식, 채권, 펀드 등 다양한 자산 추적
- 포트폴리오 성과 분석
- 배당금 및 이자 수익 기록
- 자본 이득 세금 계산

### 소규모 비즈니스

- 사업 수입 및 지출 관리
- 청구서 추적
- 부가가치세 계산
- 재무제표 생성

## 학습 리소스

### 공식 문서

- [Beancount 공식 문서](https://beancount.github.io/docs/)
- [Google Docs의 원본 문서](http://furius.ca/beancount/doc/index)

### 커뮤니티

- [Beancount 메일링 리스트](https://groups.google.com/forum/#!forum/beancount)
- [Ledger 메일링 리스트](https://groups.google.com/forum/#!forum/ledger-cli)
- GitHub Issues 및 Discussions

### 튜토리얼

공식 문서에는 초보자를 위한 단계별 가이드가 포함되어 있으며, 실제 사용 사례와 베스트 프랙티스를 다룹니다.

## 다른 도구와의 비교

### Ledger

Ledger는 Beancount의 영감이 된 오래된 프로젝트입니다. Beancount는 더 엄격한 문법과 명확한 오류 메시지를 제공하며, Python 생태계의 이점을 활용합니다.

### hledger

Haskell로 작성된 Ledger의 재구현입니다. Beancount와 유사한 목표를 가지고 있으나, 각자 다른 문법과 철학을 따릅니다.

### GnuCash, Quicken

전통적인 GUI 회계 소프트웨어와 달리, Beancount는 텍스트 기반이며 프로그래머 친화적입니다. 자동화와 커스터마이징이 훨씬 용이합니다.

## 라이선스 및 기여

Beancount는 GNU GPLv2 라이선스로 배포되는 완전한 오픈소스 프로젝트입니다. GitHub에서 버그 리포트, 기능 제안, 풀 리퀘스트를 통해 프로젝트에 기여할 수 있습니다.

개발자 Martin Blais는 프로젝트에 대한 기부를 받고 있으며, Wise나 PayPal을 통해 후원할 수 있습니다. 프로젝트는 2007년부터 시작되어 18년 넘게 개발자의 헌신적인 노력으로 유지되고 있습니다.

## 시작하기

Beancount를 시작하는 가장 좋은 방법은:

1. **공식 문서 읽기**: 기본 개념과 문법 학습
2. **예제 파일 실행**: examples 디렉토리의 샘플 파일로 실습
3. **자신의 파일 작성**: 간단한 거래부터 시작
4. **fava 설치**: 시각적 인터페이스로 데이터 확인
5. **자동화 구축**: 반복 작업을 스크립트로 자동화

## 결론

Beancount는 개인 재무 관리를 프로그래밍 방식으로 접근하고자 하는 사람들에게 이상적인 도구입니다. 텍스트 파일 기반의 접근 방식은 처음에는 생소할 수 있지만, 익숙해지면 다른 어떤 도구보다 강력하고 유연한 재무 관리 시스템을 구축할 수 있습니다.

데이터의 완전한 소유권, 버전 관리 가능성, 무한한 확장성은 장기적인 재무 데이터 관리에 있어 Beancount를 탁월한 선택으로 만듭니다. 프로그래머라면 한 번쯤 시도해볼 만한 가치가 있는 프로젝트입니다.

더 자세한 정보는 [Beancount GitHub 저장소](https://github.com/beancount/beancount)와 [공식 문서](https://beancount.github.io/docs/)에서 확인할 수 있습니다.
