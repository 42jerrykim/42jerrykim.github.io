---
draft: false
collection_order: 130
slug: aosp-build-system
title: "[안드로이드 하드웨어 개발] 13장. AOSP 빌드 시스템 및 개발 도구"
date: 2026-07-18
last_modified_at: 2026-07-18
description: "repo로 수백 개 AOSP 저장소를 관리하는 법부터 Soong/Kati가 Android.bp를 ninja 빌드 그래프로 변환하는 과정, lunch 타겟 선택 기준, ccache로 반복 빌드 시간을 단축하는 실전 방법까지 다룬다."
categories: Android Hardware Development
tags:
- Android
- Embedded(임베디드)
- Hardware(하드웨어)
- Linux(리눅스)
- Kernel
- C
- C++
- Mobile(모바일)
- Performance(성능)
- CPU(Central Processing Unit)
- OS(운영체제)
- Compiler(컴파일러)
- Debugging(디버깅)
- Profiling(프로파일링)
- Optimization(최적화)
- System-Design
- Documentation(문서화)
- Best-Practices
- Troubleshooting(트러블슈팅)
- Configuration(설정)
- CI-CD(Continuous Integration/Continuous Deployment)
- Git
- Automation(자동화)
- Tutorial(튜토리얼)
- Guide(가이드)
- Advanced
- Deep-Dive
- Soong
- Kati
- Blueprint
- Ninja
- ccache
- AOSP
- ELF(Executable and Linkable Format)
- File-System
- IO(Input/Output)
---

## 이 장을 읽기 전에

이 장은 [12장: 안드로이드 애플리케이션 개발](/post/android-hardware-development/android-application-development/)에서 다룬 시스템 앱·NDK 연동을 전제로 하지 않는다. 다만 지금까지의 챕터에서 다뤄 온 커널 모듈(3장), HAL(4장), 부트로더(8장) 같은 결과물이 실제로는 하나의 빌드 파이프라인에서 나온다는 점을 이해하려면, 리눅스 커맨드라인과 Git에 익숙하고 `Makefile`을 한 번쯤 열어본 경험이 있는 편이 좋다. 이 장의 난이도는 초급(개념·명령어 사용)에서 전문가(빌드 그래프 디버깅, 캐시 튜닝)까지 걸쳐 있다.

이 장이 다루지 않는 것도 명확히 해둔다. NDK/JNI로 네이티브 라이브러리를 작성하고 Java/Kotlin과 연동하는 방법은 [14장: 네이티브 개발(NDK/JNI)](/post/android-hardware-development/native-development/)에서, 커널 소스 자체의 구조와 모듈 작성은 3장에서, HAL 인터페이스 설계는 4장에서 다룬다. 이 장은 그 모든 산출물을 실제로 "어떻게 컴파일하고 링크해서 이미지로 만드는가"라는 빌드 시스템 자체에 집중한다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|----------|----------|
| 초급 | 도입, 핵심 개념(repo, lunch), 실전 적용의 1~2단계 | `repo sync`로 소스를 받고 `lunch`로 타겟을 골라 `m`으로 빌드를 실행할 수 있다 |
| 중급 | 핵심 개념 전체, 비교/트레이드오프, 실전 적용 전체 | Soong/Kati가 왜 공존하는지, `Android.bp`를 어떻게 작성하는지, 증분 빌드가 느려지는 이유를 진단할 수 있다 |
| 전문가 | 흔한 오개념, 비판적 시각, ninja 그래프 분석, ccache 튜닝 | ninja 빌드 그래프를 직접 열어 병목을 찾고, ccache 캐시 미스 원인을 추적하며 CI 빌드 시간을 정량적으로 개선할 수 있다 |

## 도입

AOSP(Android Open Source Project)는 수백 개의 Git 저장소, 수만 개의 빌드 모듈, 그리고 커널·HAL·프레임워크·앱이 뒤섞인 초대형 소프트웨어 스택이다. 삼성이나 퀄컴 같은 SoC(System on Chip) 벤더가 새 칩셋용 안드로이드 이미지를 이식하거나, 개인 개발자가 커스텀 롬을 빌드하거나, 사내 CI 파이프라인이 매일 밤 전체 이미지를 검증할 때 공통으로 마주치는 첫 관문이 바로 이 빌드 시스템이다. 일반적인 애플리케이션 개발자는 IDE가 빌드를 알아서 처리해 주므로 빌드 시스템의 내부를 몰라도 크게 문제되지 않지만, 하드웨어 개발자는 사정이 다르다. 새 드라이버 모듈 하나를 추가하려면 `Android.bp`에 의존성을 선언해야 하고, 빌드가 예상보다 오래 걸리면 그 원인이 소스 코드 자체인지 빌드 그래프의 설계 문제인지 구분해야 하며, CI 서버에서 반복 빌드 시간을 줄이려면 캐시 계층을 이해해야 한다.

이 장에서는 소스를 내려받는 `repo` 도구, 실제 빌드 규칙을 처리하는 Soong/Kati 이중 시스템, 빌드 대상을 고르는 `lunch`, 그 결과 만들어지는 ninja 빌드 그래프, 그리고 반복 빌드를 단축하는 ccache를 순서대로 다룬다. 이 다섯 가지는 서로 독립된 도구가 아니라 하나의 파이프라인을 이루는 단계이므로, 개별 명령어 암기보다 각 단계가 "무엇을 입력받아 무엇을 출력하는가"라는 데이터 흐름으로 이해하는 편이 훨씬 오래간다.

## 핵심 개념

### repo: 다중 저장소를 하나의 트리로 묶는 도구

**repo(레포)**는 구글이 만든 Git 저장소 오케스트레이션 도구로, `.git` 저장소 하나가 아니라 수백 개의 Git 저장소를 하나의 논리적 소스 트리로 묶어 관리한다. AOSP는 프레임워크, 커널, 각종 라이브러리, 벤더 코드가 모두 별도 Git 저장소로 나뉘어 있는데, 이를 개별적으로 `git clone`하면 버전 조합을 맞추는 일 자체가 악몽이 된다. repo는 **manifest(매니페스트)**라는 XML 파일에 "어떤 저장소를, 어떤 브랜치·리비전으로, 어느 경로에 배치할지"를 선언해 두고, 이 매니페스트 하나를 기준으로 전체 트리의 일관된 스냅샷을 만든다.

repo의 동작 원리를 이해하는 핵심은 두 명령어의 역할 분리에 있다. `repo init`은 매니페스트 저장소 자체를 `.repo/` 디렉터리에 내려받아 "무엇을 받을지"의 설계도를 준비하는 단계이고, `repo sync`는 그 설계도에 나열된 모든 저장소를 실제로 내려받거나 갱신하는 단계다. source.android.com의 Repo 명령어 레퍼런스는 `repo sync`의 동작을 "최초 동기화는 `git clone`과 동등하고, 이후 동기화는 `git fetch`와 rebase를 실행한다"고 설명한다. 즉 두 번째 이후의 `repo sync`는 매번 전체를 새로 받는 것이 아니라 각 저장소에서 변경분만 가져와 로컬 브랜치 위에 재정렬하는 증분 작업이다.

```bash
# 매니페스트 저장소를 초기화한다 (최초 1회, 브랜치는 실제 존재하는 브랜치명으로 지정)
repo init -u https://android.googlesource.com/platform/manifest -b android-14.0.0_r1

# 매니페스트에 정의된 모든 하위 저장소를 병렬로 동기화한다
repo sync -c -j8

# 특정 하위 프로젝트에서 로컬 수정을 시작하려면 repo start로 토픽 브랜치를 만든다
repo start my-feature-branch --all
```

`-j8`은 8개 작업을 병렬로 실행해 동기화 시간을 단축하는 옵션이며, 실제 병렬도는 네트워크 대역폭과 로컬 I/O 성능에 따라 조정해야 한다. `-c` 옵션은 매니페스트에 지정된 리비전에 대해 현재 브랜치의 히스토리만 가져오는 얕은 동기화를 지시해 다운로드량을 줄인다. 이 단계에서 받은 소스 트리가 바로 다음 단계인 Soong/Kati의 입력이 된다.

### Soong과 Kati: 두 세대 빌드 시스템의 공존

안드로이드 빌드 시스템은 오랫동안 GNU Make 기반의 `Android.mk` 파일로 모듈을 정의했다. 이 방식은 저장소 규모가 커질수록 두 가지 한계에 부딪혔다. Make의 텍스트 기반 매크로 언어는 대규모 빌드 로직을 표현할수록 가독성이 떨어졌고, Make 자체가 의존성 그래프를 전역적으로 재평가하는 방식이라 증분 빌드 성능이 저하됐다. 이를 해결하기 위해 구글은 **Soong(소옹)**이라는 새 빌드 시스템을 도입했다. Soong은 Go 언어로 작성된 빌드 로직 생성기로, `Android.mk` 대신 **Blueprint(블루프린트)** 문법의 `Android.bp` 파일을 입력으로 받는다. `Android.bp`는 Make의 절차적 매크로 대신 선언적 JSON 유사 문법으로 모듈을 기술하므로, 파일을 읽는 것만으로 "이 모듈이 무엇을 빌드하고 무엇에 의존하는지"가 명확히 드러난다.

여기서 흔히 오해하는 지점이 있는데, Soong은 컴파일러가 직접 소스를 컴파일하는 도구가 아니라 **빌드 그래프를 생성하는 도구**라는 점이다. Soong과 그 전신인 **Kati(카티)**는 최종적으로 ninja 빌드 파일을 만들어내는 역할을 한다. Kati는 여전히 남아 있는 `Android.mk` 기반 모듈들을 파싱해 Make 문법을 ninja 규칙으로 변환하는 역할을 맡고, Soong은 `Android.bp` 기반 모듈을 직접 ninja 규칙으로 컴파일한다. 두 시스템의 출력은 최종적으로 `combined.ninja`라는 단일 빌드 그래프로 합쳐진다. source.android.com의 빌드 개요 문서는 "Make to Soong 변환" 가이드를 별도로 제공할 만큼, AOSP 자체가 아직 이 이행기에 있다는 점을 보여준다 — 즉 최신 AOSP 트리에서도 `Android.mk`와 `Android.bp`가 한동안 함께 존재하는 것이 정상이며, 이는 설계 결함이 아니라 대규모 마이그레이션의 과도기적 상태다.

다음 표는 두 빌드 정의 파일이 같은 정적 라이브러리 모듈을 어떻게 기술하는지 비교한다. 문법 차이보다 중요한 것은 Blueprint가 의존성과 속성을 구조화된 필드로 강제한다는 점이다 — Make의 변수 할당은 오타나 순서 실수를 컴파일 시점까지 숨길 수 있지만, Blueprint의 JSON 유사 구조는 파서가 필드명을 검증한다.

```makefile
# Android.mk (레거시 Make 방식)
LOCAL_PATH := $(call my-dir)
include $(CLEAR_VARS)
LOCAL_MODULE := libsensorhub
LOCAL_SRC_FILES := sensor_hub.cpp sensor_calibration.cpp
LOCAL_SHARED_LIBRARIES := liblog libcutils
LOCAL_CFLAGS := -Wall -Werror
include $(BUILD_SHARED_LIBRARY)
```

```json
// Android.bp (Soong/Blueprint 방식)
cc_library_shared {
    name: "libsensorhub",
    srcs: [
        "sensor_hub.cpp",
        "sensor_calibration.cpp",
    ],
    shared_libs: [
        "liblog",
        "libcutils",
    ],
    cflags: [
        "-Wall",
        "-Werror",
    ],
}
```

### lunch: 빌드 타겟과 환경 변수를 선택하는 진입점

**lunch(런치)**는 빌드를 시작하기 전에 "어떤 제품을, 어떤 릴리스 구성으로, 어떤 빌드 변형으로 만들 것인가"를 선택하는 명령어다. source.android.com의 빌드 문서는 `lunch` 명령을 사용하려면 셸마다 한 번 `source build/envsetup.sh`를 실행해야 하며, `lunch` 인자의 형식이 `product_name-release_config-build_variant`라고 명시한다. 예를 들어 `aosp_arm64-trunk_staging-userdebug`라는 타겟명은 ARM64 아키텍처용 표준 AOSP 제품 구성을, trunk_staging 릴리스 채널로, 디버그 권한이 살아있는 userdebug 변형으로 빌드하겠다는 뜻이다.

세 요소는 각기 다른 축을 담당한다. 제품명(product)은 어떤 하드웨어/제품 구성을 타겟하는지를 정의하며, 실제 디바이스를 이식할 때는 벤더가 자체 제품 정의(`device/<vendor>/<board>/`)를 트리에 추가한다. 빌드 변형(variant)은 `eng`(개발자 편의 기능과 디버깅 도구 포함, 최적화 최소), `userdebug`(운영 빌드에 가깝지만 root 접근과 디버깅 훅 유지), `user`(출하용, 최적화 최대, 디버깅 인터페이스 최소화)의 세 단계로 나뉘며 이 선택은 이후 살펴볼 컴파일 최적화 수준과 SELinux 정책 강도에 직접 영향을 준다. `lunch`가 완료되면 이후의 `m`, `mm`, `mmm` 명령이 모두 이 선택된 타겟을 기준으로 동작하므로, 잘못된 타겟으로 빌드를 시작하면 전체 빌드를 다시 해야 하는 경우가 많다 — 특히 아키텍처가 바뀌면 툴체인 자체가 달라지기 때문이다.

### ninja: Soong/Kati가 만든 명세를 실행하는 빌드 그래프 엔진

**ninja(닌자)**는 사람이 직접 작성하는 빌드 시스템이 아니라, 다른 빌드 시스템(여기서는 Soong/Kati)이 생성한 저수준 빌드 명세를 매우 빠르게 실행하기 위해 설계된 실행 엔진이다. ninja 공식 매뉴얼은 스스로를 이렇게 설명한다.

> "Ninja is yet another build system. It takes as input the interdependencies of files (typically source code and output executables) and orchestrates building them, quickly." — Ninja 공식 매뉴얼(ninja-build.org)

이 인용에서 핵심은 "quickly"다. Make는 빌드를 실행할 때마다 Makefile의 매크로와 규칙을 다시 파싱하고 재귀적으로 평가하는데, 이 과정 자체가 대규모 빌드에서는 무시할 수 없는 오버헤드가 된다. ninja는 반대로 사람이 직접 편집하지 않는 저수준의 `.ninja` 파일을 입력받아, 파일 간 의존 관계를 **방향성 비순환 그래프(DAG, Directed Acyclic Graph)**로 미리 구성해 두고, 그래프 순회와 타임스탬프 비교만으로 무엇을 다시 빌드해야 하는지 빠르게 판단한다. 공식 매뉴얼의 표현을 빌리면 "Ninja evaluates a graph of dependencies between files, and runs whichever commands are necessary to make your build target up to date" — 즉 그래프 평가와 명령 실행이라는 두 단계만 남기고 나머지 복잡도(모듈 정의, 조건부 로직, 의존성 해석)는 모두 Soong/Kati가 그래프 생성 시점에 미리 처리해 버리는 구조다.

이 이중 구조는 "느린 그래프 생성 + 빠른 그래프 실행"으로 요약할 수 있다. `m` 명령을 처음 실행하면 Soong이 모든 `Android.bp`/`Android.mk`를 스캔해 `combined.ninja`를 생성하는 단계(흔히 "Soong 분석" 또는 "kati 단계"로 불린다)를 거치고, 그 다음에야 ninja가 실제 컴파일 명령을 실행한다. 소스 코드 몇 줄만 바꾼 증분 빌드에서 이 그래프 생성 단계가 매번 반복되면 실제 컴파일보다 그래프 재평가에 더 많은 시간이 걸릴 수 있는데, 이것이 바로 뒤에서 다룰 "흔한 오개념"의 소재가 된다.

## 비교/트레이드오프: 빌드 도구별 선택 기준

세 가지 선택 지점 — Make 기반 정의를 유지할지 Blueprint로 이전할지, 어떤 lunch 변형을 쓸지, 로컬 캐시를 어떻게 구성할지 — 은 각각 다른 판단 기준을 요구한다. 아래 표는 이 장에서 다룬 구성 요소들을 실무 판단 기준과 함께 정리한 것이다.

| 구성 요소 | 선택지 | 언제 선택하는가 |
|-----------|--------|----------------|
| 모듈 정의 문법 | `Android.mk` (Make) | 레거시 모듈을 유지 보수만 할 때. 신규 작성은 지양한다 |
| 모듈 정의 문법 | `Android.bp` (Blueprint/Soong) | 신규 모듈 전부. 정적 검증과 IDE 지원이 필요할 때 |
| lunch variant | `eng` | 로컬 개발, 빠른 반복, 디버깅 도구가 필요할 때 |
| lunch variant | `userdebug` | 디바이스 통합 테스트, root 권한이 필요한 디버깅 |
| lunch variant | `user` | 출하 이미지 검증, 성능/보안 최종 확인 |
| 빌드 범위 명령 | `m` | 전체 이미지 또는 여러 모듈에 걸친 변경 |
| 빌드 범위 명령 | `mm` / `mmm` | 현재(또는 지정) 디렉터리 모듈만 빠르게 재빌드할 때 |

`mm`은 현재 작업 디렉터리의 모듈만, `mmm`은 지정한 경로들의 모듈만 빌드하도록 범위를 좁히는 명령으로, 드라이버나 HAL 모듈 하나를 반복 수정하는 국면에서는 매번 `m`으로 전체 그래프를 재평가하는 것보다 훨씬 짧은 반복 주기를 만든다. 다만 `mm`/`mmm`은 의존하는 다른 모듈이 이미 최신 상태라는 전제하에 동작하므로, 여러 모듈에 걸친 헤더 변경처럼 파급 범위가 넓은 수정 후에는 결국 `m`으로 전체 일관성을 확인해야 한다. 판단 기준은 단순하다 — 수정 범위가 좁고 반복 횟수가 많으면 `mm`/`mmm`, 수정이 여러 모듈에 걸치거나 최종 검증이 필요하면 `m`이다.

## 실전 적용: 신규 HAL 모듈을 빌드 트리에 통합하고 반복 빌드를 단축하기

가상의 시나리오를 설정해 본다. 4장에서 설계한 센서 HAL 구현체를 새 정적 라이브러리 모듈로 AOSP 트리에 추가하고, 이 모듈을 반복 수정하면서 빠르게 재빌드하는 개발 루프를 구성한다고 하자. 이 과정은 (1) 소스 동기화, (2) Blueprint 모듈 정의 작성, (3) 타겟 선택과 부분 빌드, (4) ccache로 반복 빌드 단축의 네 단계로 이뤄진다.

첫 단계는 이미 앞서 다룬 `repo sync`로 최신 소스 트리를 확보하는 것이므로 반복하지 않는다. 두 번째 단계로 `hardware/vendor/sensorhub/` 같은 벤더 디렉터리에 `Android.bp`를 작성한다. 아래 예시는 정적 라이브러리 하나와 이를 사용하는 공유 라이브러리 하나로 모듈을 구성한 것으로, `static_libs`와 `shared_libs`의 차이를 보여준다. 정적 라이브러리는 링크 시점에 결과물 안으로 코드가 복사되어 별도 배포 파일이 남지 않는 반면, 공유 라이브러리는 런타임에 별도의 `.so` 파일로 로드된다 — 여러 프로세스가 같은 HAL 구현을 공유해야 한다면 공유 라이브러리 쪽이 메모리 사용량과 업데이트 배포 측면에서 유리하다.

```json
// hardware/vendor/sensorhub/Android.bp
cc_library_static {
    name: "libsensorhub_calibration",
    srcs: ["sensor_calibration.cpp"],
    cflags: [
        "-Wall",
        "-Werror",
        "-O2",
    ],
    export_include_dirs: ["include"],
}

cc_library_shared {
    name: "libsensorhub_hal",
    srcs: ["sensor_hub_hal.cpp"],
    static_libs: ["libsensorhub_calibration"],
    shared_libs: [
        "liblog",
        "libcutils",
        "libhardware",
    ],
    relative_install_path: "hw",
    vendor: true,
}
```

`vendor: true` 속성은 이 모듈이 시스템 파티션이 아니라 벤더 파티션에 설치되어야 함을 Soong에 알린다. 안드로이드의 Treble 아키텍처는 시스템 이미지와 벤더 이미지를 분리해 독립적으로 업데이트할 수 있게 하는데, HAL처럼 하드웨어에 직접 결합된 모듈은 벤더 파티션에 두는 것이 원칙이다. 이 속성을 빠뜨리면 모듈이 시스템 파티션에 설치되어 벤더 인터페이스 안정성 검증(VTS)에서 위반으로 잡힐 수 있다.

세 번째 단계로 타겟을 선택하고 이 모듈만 빠르게 빌드한다.

```bash
source build/envsetup.sh
lunch aosp_arm64-trunk_staging-userdebug

# 이 디렉터리의 모듈만 빌드 (전체 그래프 재평가 없이 해당 서브트리만 처리)
mmm hardware/vendor/sensorhub

# 특정 모듈만 이름으로 지정해 빌드하려면
m libsensorhub_hal
```

네 번째 단계는 반복 수정 주기를 단축하는 캐시 설정이다. **ccache(씨캐시)**는 컴파일러 호출을 가로채 소스 파일과 컴파일 플래그의 해시를 계산하고, 동일한 해시로 이미 컴파일된 결과가 캐시에 있으면 실제 컴파일을 건너뛰고 캐시된 오브젝트 파일을 재사용하는 컴파일러 캐시 도구다. ccache 공식 사이트는 이를 "이전 컴파일을 캐싱하고 동일한 컴파일을 감지하여 재컴파일 속도를 높인다"고 설명한다. AOSP 빌드에서 ccache가 특히 효과적인 이유는, 브랜치를 전환하거나 `repo sync`로 다른 리비전으로 옮겨갔다가 원래 코드로 돌아오는 일이 잦은데 이런 상황에서는 소스 내용이 과거와 동일한 오브젝트를 다시 만들어내는 경우가 많기 때문이다.

```bash
# ccache 사용을 활성화하고 캐시 디렉터리·최대 크기를 지정한다
export USE_CCACHE=1
export CCACHE_EXEC=/usr/bin/ccache
export CCACHE_DIR=/mnt/build-cache/.ccache
ccache -M 100G   # 캐시 최대 크기를 100GB로 설정

# 캐시 적중률을 확인해 실제로 캐시가 동작하고 있는지 검증한다
ccache -s
```

`ccache -s`로 출력되는 캐시 적중률(hit rate)은 빌드 구성이 실제로 캐시 친화적인지 판단하는 근거가 된다. 적중률이 낮다면 컴파일 플래그가 빌드마다 미묘하게 달라지고 있거나(타임스탬프를 플래그에 섞어 넣는 경우 등), 캐시 크기가 작업 세트보다 작아 오래된 항목이 밀려나고 있을 가능성을 의심해야 한다 — 단순히 "ccache를 켰으니 빨라졌겠지"라고 가정하지 말고 수치로 확인하는 습관이 중요하다.

## 흔한 오개념

가장 먼저 바로잡아야 할 오해는 "Soong이 컴파일을 수행한다"는 생각이다. 앞서 핵심 개념에서 다뤘듯 Soong과 Kati는 `Android.bp`/`Android.mk`를 해석해 ninja 빌드 그래프를 생성하는 역할만 하며, 실제 컴파일러(Clang/LLVM 등) 호출과 링크는 ninja가 그 그래프를 따라 실행한다. 이 구분을 모르면 컴파일 에러와 빌드 그래프 생성 실패(예: `Android.bp` 문법 오류)를 같은 종류의 문제로 착각해 잘못된 곳에서 원인을 찾게 된다.

두 번째 오개념은 "증분 빌드가 느린 것은 항상 컴파일 자체가 느려서"라는 가정이다. 앞서 설명했듯 `m` 실행 시마다 Soong이 빌드 그래프를 재생성하는 단계(흔히 "kati 단계"라 불리는 이 과정)가 선행되는데, 파일 몇 개만 바뀌었어도 이 단계는 트리 전체를 다시 스캔할 수 있다. 실제로 컴파일 시간이 아니라 그래프 재생성 시간이 병목인 경우가 드물지 않으므로, 빌드가 느리다고 느껴질 때는 `m` 출력에서 "kati" 또는 "Analyzing"으로 표시되는 구간과 실제 `ninja` 실행 구간을 구분해서 봐야 한다. 이 구분 없이 무작정 병렬 작업 수(`-jN`)만 늘리면 그래프 생성 단계에는 거의 도움이 되지 않는다.

세 번째는 "ccache를 켜기만 하면 항상 빨라진다"는 가정이다. ccache는 컴파일러 호출 자체를 가로채는 방식이므로 캐시 조회와 해시 계산에도 I/O·CPU 비용이 든다. 캐시 적중률이 낮은 환경(예: 매 빌드마다 소스가 실질적으로 달라지는 CI, 혹은 캐시 디렉터리가 네트워크 스토리지 위에 있어 조회 자체가 느린 경우)에서는 ccache가 오히려 순수 빌드보다 느려질 수 있다. 캐시를 도입했다면 반드시 `ccache -s`로 적중률을 확인해 실제 이득을 검증해야 한다.

## 비판적 시각

Soong/Kati 이중 구조는 실용적 타협의 산물이지 이상적인 설계는 아니다. 수만 개 모듈을 하루아침에 마이그레이션할 수 없었기 때문에 두 시스템이 공존하는 것이며, 이 과도기가 길어질수록 빌드 그래프 생성 로직도 두 갈래로 유지보수해야 하는 복잡성을 안게 된다. `Android.mk`로 작성된 레거시 모듈을 계속 붙잡고 있는 벤더 코드가 많을수록, Soong이 제공하는 정적 검증과 더 빠른 그래프 생성의 이점을 온전히 누리지 못한다. 신규 개발자 입장에서는 "왜 어떤 모듈은 `.mk`이고 어떤 모듈은 `.bp`인가"라는 질문 자체가 학습 부담으로 작용한다.

ccache 역시 만능 해법은 아니다. 캐시 디렉터리가 커질수록 디스크 사용량이 늘고, 다수의 CI 에이전트가 같은 캐시를 공유하는 구조에서는 캐시 무효화 정책과 동시 쓰기 충돌을 별도로 설계해야 한다. 또한 컴파일러 버전이나 플래그가 미세하게 바뀌는 순간 캐시 전체가 무효화될 수 있어, "캐시가 있으니 빌드 환경을 재현 가능하게 관리할 필요가 없다"는 식의 안일한 태도로 이어지면 오히려 빌드 재현성 문제를 감추는 부작용이 있다. 빌드 속도 최적화는 특정 도구를 켜는 문제가 아니라, 그래프 생성 비용·컴파일 비용·I/O 비용 중 실제 병목이 어디인지를 프로파일링해서 판단해야 하는 문제이며, 이 장에서 다룬 도구들은 그 판단을 위한 수단이지 자동으로 문제를 없애주는 마법이 아니다.

## 다음 장에서는

[14장: 네이티브 개발(NDK/JNI)](/post/android-hardware-development/native-development/)에서는 이 장에서 구성한 빌드 파이프라인 위에서 실제로 C/C++ 네이티브 라이브러리를 작성하고 JNI를 통해 Java/Kotlin 코드와 연동하는 방법을 다룬다.

## 평가 기준

이 장을 읽은 후 다음을 할 수 있어야 한다.

- `repo init`과 `repo sync`의 역할 차이를 설명하고, 매니페스트가 무엇을 정의하는지 말할 수 있다.
- Soong/Kati가 컴파일러가 아니라 ninja 빌드 그래프 생성기라는 점을 설명할 수 있다.
- `Android.mk`와 `Android.bp` 중 신규 모듈에 어느 것을 써야 하는지, 그리고 두 방식이 왜 공존하는지 설명할 수 있다.
- `lunch` 타겟명의 세 구성 요소(제품, 릴리스 구성, 빌드 변형)를 해석하고 상황에 맞는 variant를 선택할 수 있다.
- `m`, `mm`, `mmm`의 빌드 범위 차이를 이해하고 반복 개발 상황에 맞게 선택할 수 있다.
- ccache 캐시 적중률을 확인하는 방법을 알고, 적중률이 낮을 때 의심해야 할 원인을 나열할 수 있다.

## 참고 및 출처

- [Android Open Source Project — Build Android](https://source.android.com/docs/setup/build/building) (source.android.com)
- [Android Open Source Project — Build overview](https://source.android.com/docs/setup/build) (source.android.com)
- [Android Open Source Project — Repo Command Reference](https://source.android.com/docs/setup/reference/repo) (source.android.com)
- [Ninja Build System — Manual](https://ninja-build.org/manual.html) (ninja-build.org)
- [ccache — a fast C/C++ compiler cache](https://ccache.dev/) (ccache.dev)
