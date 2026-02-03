---
title: "[Software] Immich로 구현하는 (EXIF 중심) 사진 관리 시스템 소개"
description: "Jaisen Mathai의 Immich 기반 사진 관리 워크플로를 정리합니다. Immich 편집을 EXIF에 저장해 DB 의존을 줄이고, External Libraries·Synology NAS·Dropbox 백업과 3-2-1 전략으로 장기 보존을 설계합니다."
date: 2026-02-03
lastmod: 2026-02-03
categories:
  - Software
  - Self-Hosted
  - Photography
  - Backup
tags:
  - Immich
  - Immich Edition
  - photo management
  - 사진 관리
  - 영상 관리
  - self-hosted
  - 셀프호스팅
  - personal cloud
  - 개인 클라우드
  - digital archiving
  - 디지털 아카이빙
  - Preserve
  - Unify
  - Experience
  - 메타데이터
  - metadata
  - EXIF
  - XMP
  - sidecar
  - XMP sidecar
  - 앨범
  - albums
  - 설명
  - description
  - 즐겨찾기
  - favorites
  - 위치 정보
  - location
  - date time
  - 타임라인
  - timeline
  - external libraries
  - External Libraries
  - read-only mount
  - ro mount
  - Synology
  - Synology NAS
  - NAS
  - Dropbox
  - backup
  - 백업
  - 3-2-1 backup
  - 데이터 주권
  - data ownership
  - database
  - Postgres
  - PostgreSQL
  - docker
  - docker compose
  - file-based library
  - filesystem-first
  - Elodie
  - immich-exif
  - Google Photos
  - google-photos alternative
  - eventual consistency
  - 자동화
  - 워크플로
  - workflow
  - 장기 보존
  - long-term preservation
image: "wordcloud.png"
---

Immich를 써 보신 분들이라면 “구글 포토 같은 **발견(추억/검색)** 경험을, 내 서버에서 다시 얻고 싶다”는 욕심이 생깁니다. 그런데 진짜 어려운 문제는 뷰어가 아니라 **장기 보존**입니다. 앱이 바뀌고, DB 스키마가 바뀌고, 서비스가 사라져도 내 사진 라이브러리가 *수십 년 뒤에도* 그대로 살아있게 하려면 무엇을 기준(원천)으로 삼을지부터 결정해야 하죠.

Jaisen Mathai의 글 **[My Ridiculously Robust Photo Management System (Immich Edition)](https://jaisenmathai.com/articles/my-ridiculously-robust-photo-management-system-immich-edition/)** 은 이 고민을 아주 공격적으로 해결한 사례입니다. 핵심은 한 줄로 요약됩니다.

- Immich에서 만든 변경(앨범/설명/위치/시간/즐겨찾기)을 **사진 파일의 EXIF에 저장**하고
- 그 결과물을 **Synology NAS + Dropbox**로 자동 백업해
- “앱/DB가 바뀌어도 살아남는 라이브러리”를 만들었다

아래에서는 이 글의 아이디어를 소개하고, Immich 공식 문서의 제약(특히 External Libraries의 메타데이터 보존)과 백업 포인트까지 함께 정리합니다.

## 이 워크플로의 목표: Experience / Unify / Preserve

Jaisen은 자신의 사진 관리 철학을 다음 3가지로 정리합니다(중요도 순):

- **Experience**: 사진과 비디오가 “다시 그 순간을 살게” 만드는 발견 경험이 있어야 한다
- **Unify**: 부부(여러 기기)의 사진이 단일 라이브러리로 합쳐져야 한다
- **Preserve**: 수십 년 단위로 미래에도 유지되는 구조여야 한다

여기서 “Preserve”를 진짜로 밀어붙이면, 자연스럽게 **메타데이터를 어디에 저장할 것인가?** 로 귀결됩니다.

## ‘DB 없이도’ 살아남는 메타데이터: EXIF를 원천으로 삼기

이 글의 가장 강한 주장(그리고 가장 논쟁적인 선택)은 이겁니다.

- 앨범/설명/즐겨찾기 같은 정리 정보까지 포함해, 사진과 비디오의 메타데이터를 **외부 DB가 아니라 EXIF에만 의존**해야 오래 간다

Jaisen은 자신이 10년 넘게 운영해 온 CLI 도구 **Elodie**를 “캐노니컬 오거나이저(canonical organizer)”로 두고, EXIF 기반으로 파일 시스템에 라이브러리를 ‘구체화(materialize)’하는 방식을 유지해 왔습니다.

## Immich를 선택한 결정적 이유: External Libraries

Jaisen이 2025년 말 Immich를 본격 검토하게 된 계기는 **External Libraries**였습니다.

- 기존 폴더(예: NAS의 사진 폴더)를 Immich에 “외부 라이브러리”로 연결하면, Immich가 스캔해서 타임라인에 자산을 올립니다.
- 그리고 중요하게도, 해당 경로를 **read-only(:ro)로 마운트**할 수 있습니다. (즉, “내 원본은 건드리지 마”가 가능)

Immich 공식 문서(External Libraries)도 같은 맥락을 설명합니다. 스캔을 통해 디스크의 파일을 자산으로 등록하고, 지도 보기/앨범 추가 등 일반 자산처럼 동작합니다.

- 참고: [Immich 문서 - External Libraries](https://docs.immich.app/features/libraries/)

## 하지만… External Libraries의 “치명적인” 한계

여기서 중요한 함정이 하나 있습니다. Immich 문서가 명확하게 경고하듯이:

- External Libraries의 자산에 대해 Immich에서 앨범 추가/설명 수정 등 메타데이터를 바꾸면,
  - 그 메타데이터는 **Immich 내부에만 저장**되고
  - **원본 파일(외부 자산 파일)에 영속 저장되지 않습니다**
  - 게다가 파일을 외부에서 이동시키면(경로가 바뀌면) Immich는 새 자산으로 간주해, 기존 메타데이터가 리스캔 시점에 유실될 수 있습니다

즉, “파일이 진짜 원천(source of truth)이고, Immich는 뷰어/경험 계층”이라는 철학을 유지하려면, **Immich에서 한 편집을 다시 파일 쪽(EXIF)으로 되돌려야** 합니다.

## Jaisen의 해법: immich-exif 플러그인(편집을 EXIF로 되돌리기)

Jaisen은 바로 이 지점을 해결하기 위해 Immich 편집 내용을 EXIF에 저장하는 방향으로 시스템을 확장합니다.

- Immich는 기본적으로 변경을 Postgres DB에 저장합니다(그리고 필요 시 XMP sidecar를 다룰 수 있음)
- 하지만 Jaisen은 sidecar가 “너무 번거롭다”는 이유로, **메타데이터를 사진 파일에 임베드(embedded)** 하는 방식을 원했습니다
- 그래서 자신이 쓰는 플러그인을 정리해 **`immich-exif`** 라는 더 단순한 버전을 공개했습니다

- 참고: [jmathai/immich-exif](https://github.com/jmathai/immich-exif)

## 운영에서 부딪히는 현실: “파일 이동 = 삭제 + 새로 생성” 문제

Elodie가 EXIF를 업데이트하면서 파일을 앨범 폴더로 이동시키는 방식은, Immich 입장에서는 보통 이렇게 보입니다.

- 원래 있던 경로의 파일이 사라짐(삭제로 인식)
- 새 경로에 새로운 파일이 생김(새 자산으로 인식)

이 문제는 External Libraries를 쓰는 많은 워크플로에서 반복해서 등장하는데, Jaisen은 이를 **eventual consistency(최종적 일관성)** 접근으로 풀었다고 설명합니다. 즉, “변경은 저장해두고, 시간이 지나면 결국 원하는 상태로 수렴하게 한다”는 방식입니다.

기술적 상세는 글 범위를 벗어난다고 했지만, 진행 상황과 코드는 Elodie 이슈에서 추적할 수 있게 링크를 남겨두었습니다.

- 참고: [Elodie issue #496](https://github.com/jmathai/elodie/issues/496)

## 백업 관점에서 이 글이 더 유용한 이유

이 워크플로가 “robust”한 이유는 편집/정리뿐 아니라, 백업 전략이 같이 붙기 때문입니다.

Immich 공식 문서는 백업을 다음처럼 정리합니다.

- **3-2-1 백업**을 권장
- Immich의 자동 DB 덤프는 `UPLOAD_LOCATION/backups`에 생기지만,
  - **사진/영상 파일은 포함하지 않고 메타데이터만** 담는다
- 종합 백업을 위해서는 **DB + 업로드/라이브러리 파일(UPLOAD_LOCATION)** 둘 다를 백업해야 한다

- 참고: [Immich 문서 - Backup and Restore](https://docs.immich.app/administration/backup-and-restore/)

Jaisen의 TL;DR 역시 “Immich를 통해 바꾼 내용이 EXIF에 들어가고, Synology NAS와 Dropbox로 자동 백업된다”는 점을 강조합니다. 즉, 앱 레벨의 편집 경험을 누리면서도 “파일이 살아남는” 방향으로 백업을 맞춘 셈입니다.

## 내가 이 아이디어를 도입한다면: 체크리스트

이 글을 읽고 바로 따라 하고 싶다면, 아래 질문에 답해보는 게 좋습니다.

- **원천(source of truth)**: “DB가 원천”인가, “파일(EXIF)이 원천”인가?
- **External Libraries 전략**: 원본을 `:ro`로 마운트해서 Immich가 절대 수정/삭제하지 못하게 할 건가?
- **메타데이터 보존**: Immich 내부에만 저장되는 메타데이터(앨범/설명)가 리스캔/이동에 의해 날아가도 괜찮은가?
  - 괜찮지 않다면: EXIF 임베드 또는 XMP sidecar 중 어떤 방식으로 영속화할 것인가?
- **백업**: Immich DB + `UPLOAD_LOCATION`(자산/생성물) + 외부 라이브러리 원본 폴더까지 포함해 3-2-1로 가져갈 것인가?

## 참고 링크

- 원문: [My Ridiculously Robust Photo Management System (Immich Edition)](https://jaisenmathai.com/articles/my-ridiculously-robust-photo-management-system-immich-edition/)
- Immich 문서: [External Libraries](https://docs.immich.app/features/libraries/)
- Immich 문서: [Backup and Restore](https://docs.immich.app/administration/backup-and-restore/)
- GitHub: [jmathai/immich-exif](https://github.com/jmathai/immich-exif)
- GitHub: [jmathai/elodie](https://github.com/jmathai/elodie)

