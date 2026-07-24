---
name: vocabulary-post-writing
description: >-
  Vocabulary 컬렉션 영단어 글 작성 가이드. 제목/메타데이터 규칙(70자 이하 title, 150자 내외 description,
  25개 이상 tags), 폴더명·날짜·워드클라우드 이미지 규칙, EN/KR 예문 구조, 콜로케이션·유의어·문법 포인트·한눈에
  정리 섹션 템플릿과 작성 체크리스트를 포함한다. content/collection/Vocabulary/ 하위 포스트 작성·보강
  시 사용한다.
---

# Vocabulary 글 작성 가이드

`content/collection/Vocabulary/`에 영단어 학습 포스트를 작성할 때 따르는 제목·메타데이터·폴더명·본문 구조·체크리스트다. 2025년 이후 작성된 글들(`bulk`, `rowdy`, `recurrent`, `inn`, `thatched`, `scramble`, `acquaint`, `indestructible`, `screen`, `instigate`)의 패턴을 표준화한 것이다. [`blog-post-writing`](../blog-post-writing/SKILL.md)과 함께 적용한다.

---

## 제목/메타 규칙 (필수)

- **카테고리 접두어**: `[Vocabulary]` 사용
- **메인 제목 템플릿**: `[Vocabulary] {단어} 뜻과 의미 - {품사} 핵심 정리`
  - 예: `[Vocabulary] bulk 뜻과 의미 - 동사 핵심 정리`
  - 예: `[Vocabulary] rowdy 뜻과 의미 - 형용사 핵심 정리`
- **"뜻" 문자열 필수 포함**: 검색 콘솔 데이터 확인 결과, 이 컬렉션 유입은 대부분 `"{단어} 뜻"` 형태 쿼리다. 제목에 "의미"만 쓰고 "뜻"을 빼면 검색어와 SERP 타이틀의 문자열이 일치하지 않아(구글이 검색어 일치 부분을 굵게 강조하는 로직) 노출 대비 클릭률이 크게 떨어진다(예: 실측 사례 다수가 노출 10~90회에 클릭 0). 제목에 반드시 "뜻"을 넣는다.
- **품사 표기**: 한국어 품사명(명사/동사/형용사/부사 등)을 사용
- **총 길이**: 70자 이내 유지

### description 규칙 (필수)

- **언어**: 한국어, **길이**: 150자 내외 (2~3문장)
- **필수 요소**: 단어/품사/핵심 의미 요약, 주요 사용 맥락(도메인: 헬스, 비즈니스, 사회, 의학, 건축 등), 콜로케이션과 EN/KR 예문 50개로 학습한다는 정보
- **템플릿 예시**: `"영어 {품사} '{word}'의 핵심 뜻(의미1, 의미2, 의미3)을 정리한다. {분야/맥락}에서 자주 쓰이는 정확한 용법을 콜로케이션과 EN/KR 예문 50개로 익힌다. {도메인/상황}에서 반복 등장하는 중요한 {품사}."`
- **실제 예** (`bulk` 글 패턴): `"영어 동사 'bulk'의 핵심 뜻(늘리다, 부풀리다, 튀어나오다)을 정리한다. 근육량 증가, 크기 확장, 거부 등 다양한 용법을 자주 쓰는 콜로케이션과 50개 예문으로 익힌다. 헬스, 건설, 비즈니스 분야에서 자주 등장하는 중요한 동사."`

### tags 규칙 (필수)

- **개수**: 최소 25개 이상 (`data/tags.yaml` 승인 태그, 병용 개념은 Tag(태그) 형식)
- **구성 패턴**:
  - 기본 메타: `Vocabulary`, `English`, `English Words`, `영단어`
  - 단어 직접 관련: `{Word}`, `{word} meaning`, `{word} usage`, `{word} examples`, `{word} {part-of-speech}` (예: `bulk`, `bulk meaning`, `bulk usage`, `bulk examples`, `bulk verb`)
  - 의미/뉘앙스(영/한 병기): 의미군별 동의어(영어: `increase`, `enlarge`, `expand`, `noisy`, `unruly`, `recurrent`, `chronic` 등) + 한국어(`늘리다`, `부풀리다`, `소란한`, `거친`, `반복되는`, `재발하는` 등)
  - 품사/문법: `영어동사`, `영어명사`, `영어형용사`, `{word} 의미`, `{word} 용법`, `{word} 예문`, `collocation`, `콜로케이션`, `nuance`, `뉘앙스`, `context`, `맥락`
  - 도메인/상황: 헬스/운동/건설/비즈니스/사회/의학/건축/교육/법률/심리 등 (`fitness`, `bodybuilding`, `medical`, `business`, `architecture` 등)
  - 빈도/패턴/추상 개념: `pattern`, `frequency`, `cycle`, `repetition`, `behavior`, `phenomenon`, `situation`
  - 메타 태그: `etymology`, `origin`, `usage notes`, `grammar`, `pronunciation`, `examples`, `EN/KR`, `study English`, `vocabulary building`
- **실행 규칙**: 재사용 가능한 공통 태그 + 단어/품사/도메인 특화 태그를 조합해 25개 이상을 채운다. 영/한 병용 개념은 `data/tags.yaml`의 Tag(태그) 형식 승인 태그로 검색 노출과 학습 검색성을 동시에 확보한다.

## 날짜/버전 관리 (필수)

- `date`, `lastmod`는 작성/수정 당일(로컬 타임존) 날짜 사용
- 폴더명 날짜와 Front Matter `date`는 반드시 동일
- 의미 있는 내용 수정(예문 대량 추가, 설명 구조 변경 등) 시 `lastmod` 갱신

## 폴더명 규칙 (필수)

```text
YYYY-MM-DD-단어-품사-meaning-usage-examples
```

**예시**:
- `2025-12-08-bulk-verb-meaning-usage-examples`
- `2025-12-08-rowdy-adjective-meaning-usage-examples`
- `2025-11-25-recurrent-adjective-meaning-usage-examples`
- `2025-10-28-inn-noun-meaning-usage-examples`

**구성 요소**:
- **날짜**: `YYYY-MM-DD` (작성일, `date`/`lastmod`와 동일)
- **단어**: 소문자 영어 단어 (예: `bulk`, `rowdy`, `recurrent`)
- **품사**: `noun`, `verb`, `adjective`, `adverb` 등 소문자 품사 슬러그
- **슬러그**: `meaning-usage-examples` 고정 (의미/용법/예문 구조를 나타냄)

**규칙**: 모든 영문은 소문자 + 하이픈(`-`) 사용, 공백/특수문자 사용 금지.

## 이미지 규칙 (워드클라우드)

- 워드클라우드 생성기는 각 글의 `index.md` 내용을 읽어 `wordcloud.png` 이미지를 생성한다.
- Front Matter에는 `image: "wordcloud.png"`로 고정 사용한다.
- 실제 경로 예: `content/collection/Vocabulary/2025/2025-12-08-bulk-verb-meaning-usage-examples/wordcloud.png`

## Front Matter 템플릿

```yaml
---
title: "[Vocabulary] bulk 뜻과 의미 - 동사 핵심 정리"
description: "영어 동사 'bulk'의 핵심 뜻(늘리다, 부풀리다, 튀어나오다)을 정리한다. {주요 맥락/도메인 요약}. {콜로케이션/예문/학습 포인트 요약}. EN/KR 예문 50개로 실제 사용을 익힌다."
date: {{ .Date }}
lastmod: {{ .Date }}
categories:
  - English
  - Vocabulary
tags: # 최소 25개 이상 (data/tags.yaml 승인 태그)
  - Vocabulary
  - English
  - English Words
  - bulk
  - bulk meaning
  - bulk usage
  - bulk examples
  - bulk verb
  - 영단어
  - 영어동사
  - bulk 의미
  - bulk 용법
  - bulk 예문
  - collocation
  - 콜로케이션
  - nuance
  - 뉘앙스
  - context
  - 맥락
  - increase
  - enlarge
  - expand
  - swell
  - grow
  - amplify
  - magnify
  - fitness
  - bodybuilding
  - construction
  - business
  - volume
  - size
  - 근육 늘리다
  - 벌크업
  - 부피
  - 덩치
  - 체격
  - 거절하다
  - 꺼리다
  - 헬스 용어
  - 스포츠 용어
  - 건설 용어
  - 비즈니스 용어
  - 일상 표현
  - usage notes
  - grammar
  - pronunciation
  - EN/KR examples
image: "wordcloud.png"
---
```

> 실제 작성 시 `title`, `description`, `tags`는 단어/품사/의미/도메인에 맞게 수정하되, **길이 규칙(70자 이하 title, 150자 내외 description, 25개 이상 tags)**은 반드시 지킨다.

## 본문 구조 가이드

### 1. 도입부

```markdown
오늘은 {품사} '{word}'의 정확한 의미와 실제 쓰임을 정리한다.
이 단어는 {핵심 의미 요약: 예) 반복되는 현상/재발하는 질병/소란한 군중/전통 숙박 시설 등}을 표현할 때 자주 쓰이며,
{대표 맥락: 예) 의학, 일상 대화, 뉴스, 학술 글 등}에서 반복 등장하는 중요한 {품사}다.
단순 사전 정의를 넘어서, 콜로케이션과 EN/KR 예문을 통해 자연스러운 사용을 익힌다.
```

### 2. 핵심 의미 섹션

```markdown
## {word}의 핵심 의미 ({품사})

### 의미1 한글 요약 (예: 반복되는, 재발하는)
   - {Word} means {영어 정의 한 문장}.
     ({Word}는 {간결한 한국어 정의}를 의미한다.)
   - 예문 1 EN
     (예문 1 KR)
   - 예문 2 EN
     (예문 2 KR)

### 의미2 한글 요약 (예: 소란한, 거친)
   - ...

### 의미3 한글 요약 (필요 시)
   - ...
```

**형식 규칙**: 각 의미 블록은 영어 정의 1문장 + 한국어 해석 1문장, EN/KR 예문 2~4개(최소 2개)로 구성한다. EN/KR 예문은 영어 문장 끝에 두 칸 공백 + 줄바꿈 후 괄호 속 한국어 문장으로 작성한다:

```markdown
The athlete bulks up during the off-season to build strength.  
(그 선수는 비시즌 동안 근력을 키우기 위해 근육을 늘린다.)
```

### 3. 어원 섹션

```markdown
## 어원

"{word}"는 {언어/어근 정보}에서 유래했다.
{어근 의미, 구성 요소(`re-`, `in-`, `de-` 등), 원래 의미}를 설명하고,
어떻게 현대적 의미(의학/심리/일상/기술 등)로 확장되었는지 서술한다.
필요하면 관련 파생어(`-tion`, `-able`, `-ment` 등)와 역사적 사용 예도 간단히 덧붙인다.
```

### 4. 자주 쓰는 패턴과 콜로케이션

```markdown
## 자주 쓰는 패턴과 콜로케이션

### 사람/대상 관련
- **패턴1**: 굵게 영어 패턴
  - 예: rowdy crowd, rowdy behavior, rowdy teenagers
- **패턴2**: ...

### 도메인/상황별
- **의학/건강**: recurrent infection, recurrent symptom, recurrent episode
- **비즈니스/경제**: bulk inventory, bulk production, recurrent issue
- **사회/문화**: rowdy youth, instigate protests, social unrest
```

각 하위 섹션에서 **영어 패턴(굵게) + 짧은 한국어 설명**을 bullet 형식으로 정리한다.

### 5. 비슷한 말과 차이

```markdown
## 비슷한 말과 차이

### 유사 표현
- **동의어1**: 간단 정의 + 차이
- **동의어2**: ...

### 구별 포인트
- **{word} vs. 동의어1**:
  {word}는 ~에 초점을 두고, 동의어1은 ~을 강조한다.
- **{word} vs. 동의어2**: ...
```

표 또는 bullet로 나열하되, "시험/실제 사용에서 헷갈리는 포인트"를 중심으로 비교한다.

### 6. 문법/표기 포인트

```markdown
## 문법/표기 포인트

- 품사: {noun/verb/adjective/adverb 등}
- 발음: /IPA/ (영국식/미국식 필요 시 구분)
- 파생어: 명사/형용사/부사/동사 등 파생형
- 전형적 전치사/패턴: {acquaint with, bulk up, bulk at, screen for, screen out, instigate violence 등}
- 격식도: 비공식/중립/격식/학술 등
- 뉘앙스: 긍정/부정/중립, 강도, 감정 톤 등
- 문화적 연상/사용 맥락: 뉴스/학술/일상/소셜미디어/전문 분야 등
```

### 7. 주요 표현과 숙어

```markdown
## 주요 표현과 숙어

### 도메인1 (예: 헬스/피트니스, 의학, 비즈니스 등)
- **표현1**: 간단 설명 + EN/KR 예문 1개
- **표현2**: ...

### 도메인2
- ...
```

### 8. 예문 모음 (EN/KR)

```markdown
## 예문 모음 (EN/KR)

### 소제목1 (예: 정의/일반, 헬스, 비즈니스 등)
1. 예문 EN
   (예문 KR)
2. 예문 EN
   (예문 KR)
```

총 **50문장 이상** EN/KR 예문을 제공한다(번호 매기기 권장). 의미별/도메인별로 5문장 단위로 묶어서 섹션화한다.

### 9. 한눈에 정리

```markdown
## 한눈에 정리

- '{word}' ({품사}) = {핵심 의미 요약}
- 핵심 패턴: {주요 콜로케이션 나열}
- 발음: /IPA/
- 어원: {한 줄 요약}
- 맥락: {주요 도메인}
- 관련어: {주요 동의어/반의어}
- 특징: {뉘앙스/강도/사용 시 주의점}
- 대상: {사람/행동/상황/현상 등}
```

## 작성 워크플로우 (필수)

Vocabulary 영단어 글 작성 시에는 다음 순서를 항상 동일하게 따른다.

1. **디렉토리 생성**

```powershell
New-Item -ItemType Directory -Force -Path "content/collection/Vocabulary/2025/YYYY-MM-DD-단어-품사-meaning-usage-examples"
```

2. **`index.md`에 글 전체 작성**
   - Front Matter: `title`(`[Vocabulary] ...` 70자 이하), `description`(한국어 150자 내외), `tags`(`data/tags.yaml` 승인 태그 25개 이상), `date`/`lastmod`(폴더명 날짜와 동일), `categories`(`English`, `Vocabulary`), `image`(`"wordcloud.png"`)
   - 본문: 도입부 → `{word}의 핵심 의미 ({품사})` → 어원 → 자주 쓰는 패턴과 콜로케이션 → 비슷한 말과 차이 → 문법/표기 포인트 → 주요 표현과 숙어 → 예문 모음 (EN/KR, 50문장 이상) → 한눈에 정리

3. **워드클라우드 생성** — **반드시 글(Front Matter + 본문)을 먼저 완전히 작성한 뒤** 실행한다.

```bash
python script/wordcloud_generator.py "content/collection/Vocabulary/2025/YYYY-MM-DD-단어-품사-meaning-usage-examples"
```

## 작성 체크리스트

- [ ] 폴더명이 `YYYY-MM-DD-단어-품사-meaning-usage-examples` 형식인가?
- [ ] Front Matter의 `title`이 `[Vocabulary] {단어} 뜻과 의미 - {품사} 핵심 정리` 패턴("뜻" 포함, 70자 이하)인가?
- [ ] `description`이 한국어로 150자 내외이며, 핵심 의미·용법·예문 구조를 잘 요약했는가?
- [ ] `tags`가 `data/tags.yaml` 승인 태그 25개 이상인가? (단어/품사/도메인/메타 태그 조합)
- [ ] `categories`가 `English`, `Vocabulary`로 설정되었는가?
- [ ] `image: "wordcloud.png"`가 설정되어 있고, 실제로 워드클라우드가 생성되었는가?
- [ ] 본문에 핵심 의미/어원/콜로케이션/유의어 비교/문법 포인트/주요 표현/예문 50개 이상/한눈에 정리가 모두 포함되어 있는가?
- [ ] EN/KR 예문 형식(영어 문장 + 두 칸 공백 + 괄호 속 한국어 번역)이 일관되게 적용되었는가?
- [ ] `date`와 `lastmod`가 폴더 날짜와 정확히 일치하는가?
- [ ] 기존 Vocabulary 글들과 전체 톤/구조/난이도가 일관되는가?
