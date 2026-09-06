---
draft: false
collection_order: 32
slug: git-blame-command-track-line-history
title: "[Git] 32. git blame — 변경 이력 추적"
date: 2026-09-04
lastmod: 2026-09-04
description: "git blame이 파일의 각 줄을 마지막으로 수정한 커밋·작성자·날짜로 연결하는 원리, 이름 변경을 넘어 추적하는 -C/-M 옵션, 대량 서식 변경 커밋을 건너뛰는 ignore-revs 파일 설정을 정리한 Git 챕터다."
categories:
- Git
tags:
- Git
- GitHub
- Version-Control(버전관리)
- Terminal
- Guide(가이드)
- Education(교육)
- Beginner
- Productivity(생산성)
- Documentation(문서화)
- Quick-Reference
- Best-Practices
- Comparison(비교)
- Reference(참고)
- How-To
- Tips
- Troubleshooting(트러블슈팅)
- Workflow(워크플로우)
- DevOps
- Collaboration(협업)
- Command-Line
- CLI
- Diagnostics(진단)
- Code-Review(코드리뷰)
- Open-Source(오픈소스)
- Career(커리어)
image: "wordcloud.png"
---

이해할 수 없는 코드 한 줄을 마주쳤을 때 "이 줄은 왜 이렇게 쓰여 있을까"라는 질문에 답하려면, 그 줄이 어느 커밋에서 왜 그렇게 바뀌었는지 알아야 한다. `git blame`은 파일의 모든 줄을 마지막으로 수정한 커밋에 연결해, 09장의 `git log`가 파일 단위로 하던 일을 줄 단위로 정밀하게 해준다.

## 개요

```bash
git blame src/app.js
```

```
a1b2c3d (Jerry Kim  2026-08-10 10:00:00 +0900  1) function calculateTotal(items) {
9f8e7d6 (Sora Lee   2026-08-15 14:20:00 +0900  2)   let total = 0;
a1b2c3d (Jerry Kim  2026-08-10 10:00:00 +0900  3)   for (const item of items) {
3f2a1c9 (Jerry Kim  2026-08-20 09:15:00 +0900  4)     total += item.price;
```

각 줄 앞에 붙은 짧은 해시, 작성자, 날짜는 그 줄을 <strong>마지막으로</strong> 변경한 커밋 정보다. 여러 줄이 같은 해시를 공유한다면(위 예시의 1번·3번 줄) 그 줄들이 같은 커밋에서 함께 작성됐다는 뜻이다.

## 기본 개념

`git blame`이 답하는 질문은 "이 줄을 누가 언제 마지막으로 건드렸는가"이지, "이 줄을 누가 원래 처음 작성했는가"가 아니다. 파일이 여러 번 리팩터링을 거쳤다면, 원래 작성자의 이름은 blame 결과에서 사라지고 가장 최근에 그 줄을 스쳐 지나간 사람만 남는다. 예를 들어 코드 포맷터를 전체 파일에 돌린 커밋이 있다면, 그 이후로는 실질적인 로직 작성자가 아니라 포맷터를 실행한 사람이 모든 줄의 blame 결과에 나타난다.

## 종류/세부

### 특정 커밋 이전 상태를 조회하기

`blame`은 기본적으로 현재 브랜치의 최신 상태를 기준으로 하지만, 특정 커밋 시점의 상태로 좁힐 수도 있다.

```bash
git blame a1b2c3d -- src/app.js    # a1b2c3d 시점까지의 blame(그 이후 변경은 반영 안 함)
```

### 이름 변경을 넘어 추적하기(`-C`, `-M`)

09장에서 `git log --follow`가 이름 변경된 파일의 이전 이력까지 추적한다고 설명했다. `blame`에도 유사한 옵션이 있다.

```bash
git blame -M src/app.js    # 파일 내에서 코드가 이동(move)된 경우도 추적
git blame -C src/app.js    # 다른 파일에서 복사(copy)된 코드까지 추적
```

`-M`은 같은 파일 안에서 함수 순서를 재배치했을 때 "새로 작성한 코드"로 잘못 표시되는 것을 막아준다. `-C`는 한 파일의 코드를 복사해 다른 파일을 새로 만들었을 때, 새 파일의 그 코드가 원래 어디서 왔는지까지 거슬러 올라간다.

### 특정 커밋을 건너뛰기(`--ignore-rev`)

대규모 서식 변경(들여쓰기 스타일 통일, 자동 포맷터 일괄 적용 등)을 한 커밋으로 실행하면, 그 이후 모든 blame 결과가 실제 로직 변경과 무관하게 그 서식 변경 커밋을 가리키게 된다. 이런 "노이즈성" 커밋을 blame 계산에서 제외할 수 있다.

```bash
git blame --ignore-rev <서식-변경-커밋-해시> src/app.js
```

매번 해시를 입력하는 대신, 저장소에 무시할 커밋 목록을 파일로 관리하고 설정에 등록해두는 방법도 있다.

```bash
echo "<서식-변경-커밋-해시>" >> .git-blame-ignore-revs
git config blame.ignoreRevsFile .git-blame-ignore-revs
```

이 파일을 저장소에 커밋해두면 팀 전체가 같은 설정을 공유할 수 있다.

## 주의사항·함정

**blame 결과만으로 "누구 책임인가"를 판단하는 것은 위험하다**: 위에서 설명했듯 blame은 마지막으로 그 줄을 건드린 사람을 보여줄 뿐, 코드 리뷰에서 함께 논의된 결정이었는지, 다른 사람의 요청으로 그렇게 수정했는지는 알려주지 않는다. 진짜 맥락이 필요하다면 blame이 가리키는 커밋의 메시지(08장에서 강조한 "왜" 설명)와 관련 Pull Request(21장)를 함께 확인해야 한다.

**한 줄이 여러 번 옮겨 다니면 추적이 끊길 수 있다**: `-M`, `-C` 옵션이 있어도 코드가 크게 재구성되거나 여러 파일에 걸쳐 흩어지면, Git의 휴리스틱이 원래 출처를 찾지 못하고 새로 작성된 것처럼 표시할 수 있다.

**대용량 파일이나 히스토리가 긴 저장소에서 blame이 느릴 수 있다**: blame은 해당 파일의 전체 히스토리를 순회하며 각 줄의 출처를 계산하므로, 오래되고 자주 수정된 파일일수록 계산 비용이 커진다. 필요한 줄 범위만 좁혀 조회하는 `-L <시작>,<끝>` 옵션으로 속도를 개선할 수 있다.

## Reference

- [git-blame Documentation](https://git-scm.com/docs/git-blame)
