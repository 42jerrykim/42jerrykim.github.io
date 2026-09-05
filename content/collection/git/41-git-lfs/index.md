---
draft: false
collection_order: 41
slug: git-lfs-large-file-storage
title: "[Git] 41. Git LFS(Large File Storage)"
date: 2026-09-04
lastmod: 2026-09-04
description: "Git LFS가 대용량 바이너리 파일을 저장소 히스토리 대신 포인터 파일로 대체해 저장하는 원리, 34장의 blob 방식이 대용량 파일마다 전체 clone 크기를 부풀리는 근본 문제, .gitattributes와 연동해 특정 확장자를 자동으로 LFS 대상으로 지정하는 법을 정리한 Git 8부 마무리 챕터다."
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
- File-System(파일시스템)
- Advanced
- Open-Source(오픈소스)
- Career(커리어)
- Configuration(설정)
- Command-Line
- CLI
image: "wordcloud.png"
---

34장에서 배운 대로 Git은 파일 내용을 blob으로 저장하고, 바뀌지 않은 파일은 이전 스냅샷을 재사용해 공간을 아낀다. 하지만 이 최적화는 텍스트 위주 소스 코드에서 잘 작동할 뿐, 매번 조금씩 통째로 바뀌는 대용량 바이너리 파일(디자인 파일, 동영상, 대형 데이터셋)에는 거의 효과가 없다. Git LFS는 8부 마지막 챕터로서 이 근본적인 한계에 대한 해법을 제공한다.

## 개요

Git LFS(Large File Storage)는 Git 자체의 기능이 아니라, Git과 함께 동작하는 별도의 확장 프로그램이다. 설치 후 특정 파일 패턴을 LFS 추적 대상으로 등록하면, 그 파일들은 저장소 히스토리에 실제 내용 대신 <strong>포인터 파일</strong>로 저장된다.

```bash
git lfs install                     # 최초 1회, 이 컴퓨터에 LFS 훅(39장) 설정
git lfs track "*.psd"                # .psd 파일을 LFS 대상으로 등록
git add .gitattributes .psd 파일들
git commit -m "디자인 파일에 LFS 적용"
```

`git lfs track`으로 등록한 내용은 실제로 40장에서 다룬 `.gitattributes`에 기록된다.

```gitattributes
*.psd filter=lfs diff=lfs merge=lfs -text
```

## 기본 개념

일반 Git 저장소에서 대용량 바이너리 파일을 그대로 커밋하면, 34장에서 설명한 대로 그 파일의 <strong>모든 버전</strong>이 blob으로 영구히 저장소에 쌓인다. 100MB짜리 동영상 파일을 열 번 수정해 커밋했다면, 저장소는 (재사용되지 않는 한) 최대 1GB에 가까운 크기로 불어날 수 있다. `git clone`(18장)은 이 히스토리 전체를 받아와야 하므로, 대용량 바이너리가 쌓인 저장소는 clone 자체가 매우 느려진다.

Git LFS는 이 문제를 <strong>간접 참조</strong>로 해결한다. 저장소의 Git 히스토리에는 실제 파일 내용이 아니라, 그 내용을 가리키는 작은 텍스트 포인터만 저장된다.

```
version https://git-lfs.github.com/spec/v1
oid sha256:4d7a214614ab2935c943f9e0ff69d22eadbb8f32b1b78469eec9c8fdf189261
size 12345
```

실제 파일 내용은 Git 저장소가 아니라 별도의 LFS 서버(GitHub·GitLab이 자체 LFS 스토리지를 제공)에 저장되며, `git checkout`(12장)이나 `git clone` 시 이 포인터를 보고 실제 내용을 그 서버에서 내려받는다.

```mermaid
flowchart LR
    gitHistory["Git 히스토리</br>(포인터 파일만 저장)"] -.->|"checkout 시 조회"| lfsServer["LFS 서버</br>(실제 바이너리 내용)"]
```

## 종류/세부

### 어떤 파일에 LFS를 적용해야 하는가

| 파일 유형 | LFS 적용 권장 여부 |
|---|---|
| 소스 코드, 설정 텍스트 | 불필요 — Git의 기본 blob 재사용이 이미 효율적 |
| 디자인 파일(.psd, .sketch), 동영상, 대형 오디오 | 권장 — 크기가 크고 자주 통째로 바뀜 |
| 컴파일된 바이너리, 빌드 산출물 | 대개 `.gitignore`(10장)로 아예 추적 제외가 더 나음(LFS보다 우선 검토) |
| 대형 데이터셋(ML 모델 가중치 등) | 권장 — 다만 전용 데이터 버전 관리 도구(DVC 등)도 비교 검토할 만함 |

### 이미 커밋된 파일을 뒤늦게 LFS로 옮기기

프로젝트 초기에 LFS 없이 대용량 파일을 커밋해버렸다면, 이미 히스토리에 쌓인 내용까지 정리하려면 히스토리 재작성이 필요하다. 이는 42장에서 다루는 대용량 저장소 관리와 이어지는 주제로, `git lfs migrate` 명령이 이 과정을 돕는다.

```bash
git lfs migrate import --include="*.psd"    # 히스토리 전체에서 .psd 파일을 LFS 포인터로 교체
```

이 명령은 커밋 해시를 재작성하므로, 15장·20장에서 다룬 것과 동일한 주의(공유된 히스토리에는 위험)가 그대로 적용된다.

### 대역폭·스토리지 비용

GitHub 등 대부분의 LFS 호스팅은 무료 계정에 일정량의 스토리지·대역폭 한도를 두고, 초과하면 추가 요금이 발생한다. 대용량 파일을 자주 다루는 프로젝트라면 이 한도를 미리 확인하는 편이 예상 밖의 비용을 피하는 데 도움이 된다.

## 주의사항·함정

**LFS가 설치되지 않은 환경에서 clone하면 포인터 파일만 받게 된다**: `git lfs install`을 실행하지 않은 컴퓨터에서 LFS 저장소를 clone하면, 실제 이미지·동영상 대신 앞서 본 텍스트 포인터 파일이 그대로 보인다. CI 환경 등에서 이 문제가 생긴다면 해당 환경에 Git LFS 클라이언트가 설치·초기화되어 있는지 확인해야 한다.

**`.gitattributes`에 LFS 규칙을 등록하기 전에 커밋된 파일은 소급 적용되지 않는다**: 40장에서 다룬 것과 같은 원리다. `git lfs track`을 실행한 이후의 새 커밋부터 적용되며, 과거 커밋을 정리하려면 위에서 언급한 `git lfs migrate`가 필요하다.

**모든 저장소 호스팅 서비스가 LFS를 기본 지원하지는 않는다**: 사내에 직접 구축한 Git 서버나 일부 저비용 호스팅은 LFS 서버 기능을 별도로 구축해야 할 수 있다. 프로젝트에서 LFS 도입을 검토하기 전에 실제로 사용할 호스팅 환경이 LFS를 지원하는지 먼저 확인한다.

## Reference

- [Git Large File Storage](https://git-lfs.com/)
