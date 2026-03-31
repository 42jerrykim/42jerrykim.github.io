# 영화 리뷰 작성 레퍼런스

SKILL.md에서 참조하는 검색 쿼리 상세 예시, 분석 관점 가이드, 장르별 분석 포인트를 포함한다.

---

## 검색 쿼리 상세 예시

### 영어 검색 (WebSearch)

| 목적 | 쿼리 템플릿 | 예시 (Interstellar) |
|------|-----------|-------------------|
| 줄거리 | `"{title}" {year} full plot summary spoilers` | `"Interstellar" 2014 full plot summary spoilers` |
| 분석 | `"{title}" {year} film analysis themes symbolism` | `"Interstellar" 2014 film analysis themes symbolism` |
| 제작 비화 | `"{title}" {year} behind the scenes making of` | `"Interstellar" 2014 behind the scenes making of` |
| 영상 | `"{title}" {year} cinematography visual style Hoyte van Hoytema` | `"Interstellar" 2014 cinematography visual style Hoyte van Hoytema` |
| 음악 | `"{title}" {year} Hans Zimmer soundtrack score analysis` | `"Interstellar" 2014 Hans Zimmer soundtrack score analysis` |
| 캐스트 | `"{title}" {year} cast performance review` | `"Interstellar" 2014 cast performance review` |
| 평점 | `"{title}" {year} rotten tomatoes metacritic imdb` | `"Interstellar" 2014 rotten tomatoes metacritic imdb` |
| 감독론 | `"{director}" filmography directing style auteur` | `Christopher Nolan filmography directing style auteur` |

### 한국어 검색 (WebSearch)

| 목적 | 쿼리 템플릿 |
|------|-----------|
| 줄거리 | `"{한국 제목}" 줄거리 전체 스포일러 결말` |
| 평가 | `"{한국 제목}" 리뷰 평가 분석` |
| 평점 | `"{한국 제목}" 네이버 평점 CGV` |
| 비화 | `"{한국 제목}" 제작 비화 촬영 뒷이야기` |

### Browser MCP 탐색 우선순위 URL

```
Wikipedia:     https://en.wikipedia.org/wiki/{Title}_(film)
               https://en.wikipedia.org/wiki/{Title}_({year}_film)
IMDb:          https://www.imdb.com/title/tt{id}/
Rotten Tomatoes: https://www.rottentomatoes.com/m/{slug}
나무위키:       https://namu.wiki/w/{제목}
네이버 영화:    WebSearch로 "네이버 영화 {제목}" 검색 후 URL 확보
```

---

## 분석 관점 가이드

### 캐릭터 심층 분석 체크리스트

각 주요 캐릭터(최소 3명)에 대해:

- [ ] **원형(Archetype)**: 영웅, 멘토, 그림자, 변신자, 문지기 등 서사 원형
- [ ] **성장 곡선**: Act별 캐릭터 상태 변화 추적
- [ ] **동기-장애물-변화**: Want(원하는 것) vs Need(필요한 것) 구분
- [ ] **관계 역학**: 다른 캐릭터와의 관계가 어떻게 플롯을 추동하는가
- [ ] **배우 연기**: 특기할 만한 연기 장면, 연기 스타일의 적합성

### 영상미 분석 체크리스트

- [ ] **색감/색채 팔레트**: 전체 톤, 장면별 색감 변화와 의미
- [ ] **구도/프레이밍**: 대칭, 규칙 of Thirds, 깊이감, 인물 배치
- [ ] **카메라 워크**: 롱테이크, 핸드헬드, 스테디캠, 드론, 특수 장비
- [ ] **조명**: 자연광 vs 인공광, 하이키/로우키, 빛의 방향과 의미
- [ ] **편집 리듬**: 컷 빈도, 전환 기법, 몽타주 사용
- [ ] **VFX/CGI**: 실사 대비, 미니어처, 프랙티컬 이펙트 병용 여부
- [ ] **미장센**: 세트 디자인, 소품, 의상, 메이크업의 서사적 기능

### 음악/사운드 분석 체크리스트

- [ ] **메인 테마**: 멜로디 특징, 악기 편성, 감정 효과
- [ ] **라이트모티프**: 캐릭터/상황별 반복 모티프
- [ ] **다이제틱/논다이제틱**: 화면 내 음원 vs 배경음악 활용
- [ ] **침묵의 활용**: 음악이 멈추는 순간의 효과
- [ ] **사운드 디자인**: 환경음, 효과음의 심리적 효과
- [ ] **기존 곡 사용**: 삽입곡 선택의 의미와 가사 연관성

### 상징/메타포 분석 관점

| 분석 레이어 | 질문 |
|------------|------|
| 시각 상징 | 반복되는 이미지/색상/사물이 무엇을 상징하는가? |
| 공간 상징 | 장소/환경이 캐릭터의 심리 상태를 반영하는가? |
| 이름/숫자 | 캐릭터 이름, 반복되는 숫자에 의도가 있는가? |
| 구조 메타포 | 서사 구조 자체가 주제를 반영하는가? (예: 시간 루프 = 반복되는 실수) |
| 장르 전복 | 장르 관습을 따르거나 뒤집어 전달하는 메시지가 있는가? |
| 인터텍스트 | 다른 작품/신화/역사에 대한 오마주나 인용이 있는가? |
| 사회적 맥락 | 개봉 당시 사회 이슈와 어떤 관련이 있는가? |

---

## 장르별 추가 분석 포인트

### SF / 판타지
- 세계관 설정의 내적 일관성
- 과학적 근거 또는 의도적 비과학의 서사적 기능
- 기술/마법 시스템의 규칙과 제약

### 액션 / 스릴러
- 액션 시퀀스 안무와 물리적 설득력
- 긴장감 조성 기법 (정보 비대칭, 시간 제한, 공간 제약)
- 폭력 묘사의 톤과 의도

### 드라마 / 로맨스
- 감정 곡선의 자연스러움
- 대사의 서브텍스트 (말하지 않는 것이 전달하는 의미)
- 관계 역학의 구체성

### 애니메이션
- 캐릭터 디자인과 감정 표현 기법
- 배경 미술의 세계관 구현
- 물리 법칙 해석 (과장/생략/변형의 의도)

### 호러
- 공포 유발 기법 (점프스케어 vs 서스펜스 vs 불안)
- 괴물/위협의 상징적 의미
- 서바이벌 논리의 설득력

---

## 종합 평가 기준

최종 평점(5.0 만점)을 매길 때 참고하는 가중치:

| 항목 | 비중 | 평가 기준 |
|------|------|----------|
| 서사/각본 | 30% | 구조적 완성도, 주제 전달력, 대사 품질 |
| 연출 | 20% | 장면 연출, 톤 일관성, 페이스 조절 |
| 연기 | 15% | 캐릭터 설득력, 앙상블 조화 |
| 영상미 | 15% | 촬영, 미장센, VFX, 색감 |
| 음악/사운드 | 10% | 감정 증폭, 독자성, 서사 기여 |
| 독창성 | 10% | 장르 내 차별성, 새로운 시도 |

---

## 출처 표기 형식

```markdown
## 참고 문헌 및 출처

- [Article Title — Site Name](https://verified-url.com)
- [Review Title — Reviewer Name, Publication](https://verified-url.com)
- [Wikipedia: Film Title](https://en.wikipedia.org/wiki/Film_Title)
```

모든 URL은 본문에 포함하기 전 `WebFetch` 또는 `browser_navigate`로 접근 가능 여부를 확인한다. 404/5xx 응답이면 제거하거나 대체 URL을 찾는다.
