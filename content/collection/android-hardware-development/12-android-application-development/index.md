---
draft: false
collection_order: 120
slug: android-application-development
title: "[Android Hardware] 12. 안드로이드 애플리케이션 개발"
date: 2026-07-18
last_modified_at: 2026-07-18
description: "벤더 설정/진단 앱이 priv-app 권한 화이트리스트로 특권을 얻는 구조와 Jetpack/Compose 선언형 UI 아키텍처를 정리하고, 앱이 커스텀 시스템 서비스·HAL에 접근하는 세 가지 경로와 각각의 트레이드오프를 실전 코드로 비교한다."
categories: Android Hardware Development
tags:
- Android
- Embedded(임베디드)
- Hardware(하드웨어)
- Mobile(모바일)
- Security(보안)
- Kotlin
- Java
- System-Design
- Interface(인터페이스)
- Software-Architecture(소프트웨어아키텍처)
- Best-Practices
- Debugging(디버깅)
- Performance(성능)
- Advanced
- Samsung
- Authentication(인증)
- Case-Study
- Deep-Dive
- Configuration(설정)
- Troubleshooting(트러블슈팅)
- Jetpack
- Jetpack-Compose
- AIDL
- HAL
- SystemServer
- Priv-App
- Signature-Permission
- SELinux
- Binder
- ViewModel
- StateFlow
- Settings-App
- Diagnostic-App
- Android-bp
- Vendor-Partition
image: "wordcloud.png"
---

## 이 장을 읽기 전에

이 장은 시리즈 순서상 [11장: 인증 및 컴플라이언스](/post/android-hardware-development/certification-compliance/) 뒤에 오지만, 기술적으로는 [04장: 하드웨어 추상화 계층(HAL) 개발](/post/android-hardware-development/hal-development/)과 [05장: 시스템 서비스 개발](/post/android-hardware-development/system-services/)에서 다룬 AIDL·Binder·SystemServer 구조를 직접 이어받는다. 그 두 장이 "벤더가 HAL을 어떻게 노출하고, 시스템 서비스가 이를 어떻게 중개하는가"를 다뤘다면, 이 장은 그 파이프라인의 반대쪽 끝, 즉 "그렇게 노출된 API를 실제 애플리케이션 코드가 어떤 경로로 소비하는가"를 다룬다. 난이도는 중급–전문가 범위다. Kotlin과 기본 안드로이드 컴포넌트(Activity, Service, Manifest, Gradle 빌드)를 다뤄본 경험이 있다면 중급 구간을 따라갈 수 있고, priv-app 권한 화이트리스트를 구성하거나 프레임워크 패치 없이 시스템 서비스에 직접 접근하는 절은 벤더 이미지 빌드 경험을 전제로 한다.

이 장이 다루지 않는 것도 명확히 해 둔다. Jetpack/Compose 각 라이브러리의 API 레퍼런스 전체와 Activity/Fragment 생명주기 같은 일반 안드로이드 앱 개발 기초는 developer.android.com 공식 문서가 이미 충분히 다루므로 이 장에서 반복하지 않는다. C/C++ 라이브러리를 JNI로 앱에 연동하는 방법은 이 컬렉션의 네이티브 개발 챕터에서 별도로 다루고, 안드로이드 앱 빌드가 Soong/Make 빌드 그래프에 실제로 어떻게 편입되는지는 다음 장에서 이어진다. 이 장의 목표는 Jetpack 구성 요소를 나열하는 것이 아니라, "왜 벤더 설정/진단 앱은 플레이스토어 앱과 다른 권한·배포 규칙을 따르는가"와 "앱이 커스텀 HAL·시스템 서비스에 닿는 경로가 왜 하나가 아니라 여러 개이며 각각 무엇을 대가로 치르는가"를 이해하는 것이다.

| 수준 | 읽을 부분 | 핵심 목표 |
|:--:|:--|:--|
| 중급자(앱 개발 경험자) | 도입, 핵심 개념(시스템 앱의 특수성, Jetpack/Compose 개요) | 벤더 설정/진단 앱이 일반 서드파티 앱과 어떤 권한·배포 모델 차이를 갖는지, Compose가 기존 View 시스템과 무엇이 다른지 설명할 수 있다 |
| 실무자·전문가 | 비교/트레이드오프, 실전 적용, 흔한 오개념, 비판적 시각 | 커스텀 시스템 서비스에 접근하는 세 가지 경로를 구현하고, 각 경로의 서명·SELinux·hidden API 제약과 실패 지점을 판단할 수 있다 |

## 왜 "벤더 앱"은 플레이스토어 앱과 다른 규칙을 따르는가

일반 서드파티 앱 개발자는 `Context.getSystemService()`가 돌려주는 공개 SDK 매니저 뒤에 무엇이 있는지 몰라도 앱을 완성할 수 있다. 하지만 갤럭시급 제품을 만드는 조직에서 설정 앱이나 공장 진단 앱을 담당하는 팀은 사정이 다르다. 이런 앱은 발열 상태를 원시 값으로 조회하거나, 공장 출하 전 캘리브레이션 루틴을 실행하거나, 서드파티 앱에게는 절대 공개되지 않는 하드웨어 진단 API를 호출해야 한다. 이 요구를 만족시키려면 앱은 `/system/priv-app` 또는 `/vendor/priv-app`에 시스템 이미지의 일부로 설치되고, 플랫폼 서명 또는 벤더 서명을 받아 `signature|privileged` 등급의 권한을 부여받아야 한다. 이것이 이 장에서 "벤더 앱"이라 부르는 범주이며, 일반 안드로이드 앱 개발 튜토리얼이 거의 다루지 않는 영역이다.

이 장에서는 두 축을 함께 다룬다. 하나는 이런 벤더 앱이 왜, 어떻게 일반 앱과 다른 권한·배포 체계를 갖는가이고, 다른 하나는 그 앱의 UI 계층을 구성하는 현재의 표준 도구인 Jetpack/Compose가 어떤 아키텍처 원칙 위에 서 있는가이다. 이 두 축을 이해해야, 05장에서 등록한 커스텀 시스템 서비스를 실제 앱 코드가 안전하게 소비하는 마지막 구간을 완성할 수 있다.

## 핵심 개념

### priv-app: 설치 위치가 곧 권한 체계다

**특권 앱(Privileged App, priv-app)**은 시스템 이미지의 `priv-app` 디렉터리(`/system/priv-app`, `/vendor/priv-app`, `/product/priv-app` 등 파티션별로 존재)에 설치되는 시스템 앱을 가리킨다. 일반 시스템 앱이 `/system/app`에 놓여 `signature` 등급 권한까지만 받을 수 있는 것과 달리, priv-app은 `signature|privileged`로 선언된 권한, 즉 서명 조건과 별개로 "이 앱이 시스템의 특권 파티션에 속해 있다"는 사실 자체를 조건으로 삼는 권한까지 받을 수 있다. 이 구분이 중요한 이유는 명확하다 — 카메라 저수준 캘리브레이션이나 진단 목적의 원시 센서 접근 같은 권한은 서명만 검증해서는 안전하지 않다. 플레이스토어를 통해 배포되는 서명된 악성 앱이 우연히 같은 서명을 흉내 낼 위험까지 막으려면, "시스템 이미지 빌드 시점에 이미 그 자리에 있었는가"라는 물리적 조건을 추가로 요구해야 한다.

**진단 앱(Diagnostic App)**은 이 priv-app 범주 안에서도 한 걸음 더 나아간 특수성을 갖는다. 공장 출하 검사, A/S 센터 리페어 모드, 필드 엔지니어용 로그 수집 도구 등은 일반 사용자에게 노출되지 않는 진입점(예: 특정 다이얼 코드, `persist.sys.factory` 같은 시스템 프로퍼티, 리커버리 부트 모드)을 통해서만 실행되며, 공개 SDK에 없는 벤더 고유 AIDL 인터페이스를 직접 호출하는 경우가 흔하다. 이런 앱은 CTS/VTS를 통과해야 하는 최종 사용자용 기능과 달리 인증 범위 밖에 놓이는 경우가 많지만, 그렇다고 권한 검사나 SELinux 정책 검증까지 면제되는 것은 아니라는 점을 뒤에서 다시 짚는다.

### privapp-permissions 화이트리스트: priv-app이라고 자동으로 권한을 받지 않는다

Android 8(Oreo) 이후 플랫폼은 priv-app 디렉터리에 앱을 두는 것만으로 `signature|privileged` 권한을 자동 부여하지 않는다. 대신 각 파티션의 `/etc/permissions/privapp-permissions-<oem>.xml` 파일에 패키지명과 허용할 권한 목록을 명시적으로 선언해야 한다. `PackageManagerService`는 부팅 시 이 화이트리스트와 앱이 매니페스트에 선언한 권한을 대조하며, Android 9부터는 이 대조가 훨씬 엄격해져 화이트리스트에 명시되지 않은 권한 요청이 있으면 `enforce` 모드에서 아예 부팅이 진행되지 않는다(개발 단계에서는 `ro.control_privapp_permissions=log`로 완화해 위반 사항만 로그로 남길 수 있다).

```xml
<!-- vendor/etc/permissions/privapp-permissions-vendor.xml -->
<permissions>
    <privapp-permissions package="com.example.vendor.diagnostics">
        <permission name="com.android.server.devicemonitor.permission.MONITOR" />
    </privapp-permissions>
</permissions>
```

이 화이트리스트는 05장에서 정의한 `MONITOR` 권한처럼 벤더가 직접 만든 커스텀 권한에도 똑같이 적용된다. 즉 앱 쪽에서 매니페스트에 `<uses-permission>`을 선언하고, 프레임워크 쪽에서 그 권한을 `signature|privileged`로 선언하고, 마지막으로 이 화이트리스트 파일에 패키지명과 권한명을 함께 등록해야 비로소 세 조각이 맞물려 실제로 권한이 부여된다. 세 조각 중 하나라도 빠지면 컴파일과 설치는 성공하지만 런타임에 `SecurityException`이 발생하거나(개발 모드) 기기가 부팅되지 않는(강제 모드) 형태로 실패가 드러난다.

### Jetpack: 아키텍처 계층을 표준화하는 라이브러리 모음

**Jetpack**은 ViewModel, Room, WorkManager, Navigation, Lifecycle 같은 라이브러리 묶음으로, 안드로이드 앱이 반복적으로 겪는 구조적 문제(화면 회전 시 상태 손실, 백그라운드 작업 스케줄링, 생명주기와 비동기 작업의 경합)에 표준화된 해법을 제공한다. Jetpack이 권장하는 아키텍처는 UI 계층, 도메인 계층(선택적), 데이터 계층으로 나뉘며, 데이터는 항상 아래에서 위로(Repository → ViewModel → UI) 흐르고 이벤트는 위에서 아래로 흐르는 **단방향 데이터 흐름(Unidirectional Data Flow, UDF)**을 원칙으로 삼는다. `ViewModel`은 UI 상태를 화면 회전이나 프로세스 재생성과 무관하게 보존하는 홀더 역할을 하고, `StateFlow`/`LiveData`는 그 상태를 UI가 관찰 가능한 스트림으로 노출한다. 벤더 진단 앱에서 이 구조가 중요한 이유는, 05장에서 다룬 `IDeviceMonitorListener` 같은 Binder 콜백이 UI 스레드가 아닌 Binder 스레드 풀에서 도착하기 때문이다 — ViewModel과 StateFlow는 이 스레드 경계를 앱 코드가 직접 신경 쓰지 않아도 되게 흡수해 준다.

### Jetpack Compose: 선언형 UI와 리컴포지션

**Jetpack Compose**는 UI를 명령형 위젯 트리 조작이 아니라 상태의 함수로 선언하는 UI 툴킷이다. 기존 View 시스템에서는 개발자가 XML로 레이아웃을 정의하고 `findViewById()`로 위젯을 찾아 `setText()` 같은 메서드로 직접 상태를 반영해야 했다면, Compose에서는 `@Composable` 함수가 현재 상태를 입력받아 UI를 "그려야 할 모습"으로 기술하고, 관찰 중인 상태가 바뀌면 Compose 런타임이 영향받는 부분만 다시 실행하는 **리컴포지션(Recomposition)**을 수행한다. 이 모델의 핵심 원칙은 **상태 호이스팅(State Hoisting)**이다 — Composable 함수는 자기 자신의 상태를 직접 소유하지 않고 상위에서 전달받아, 같은 컴포저블을 다양한 상태 소스(ViewModel의 StateFlow, 단순 로컬 변수 등)와 재사용 가능하게 만든다. Compose는 기존 View 계층과 완전히 별개의 화면을 요구하지 않는다 — `ComposeView`로 기존 XML 레이아웃 안에 Compose 화면을 끼워 넣거나, `AndroidView`로 Compose 화면 안에 레거시 위젯을 끼워 넣는 상호운용이 표준으로 지원되므로, 부팅 초기 UI처럼 안정성이 최우선인 화면은 기존 View로 남겨두고 진단 앱의 나머지 화면부터 점진적으로 전환하는 전략이 실무에서 흔히 쓰인다.

### 앱이 커스텀 HAL·시스템 서비스에 접근하는 세 가지 경로

05장에서 커스텀 시스템 서비스를 `SystemServer`에 등록하고 `SystemServiceRegistry`에 노출하는 절차를 다뤘다면, 이 절은 그 반대쪽 — 앱 코드가 실제로 그 서비스에 닿는 경로를 정리한다. 경로는 크게 세 가지다. 첫째는 `Context.getSystemService()`를 통해 정식으로 노출된 공개 매니저를 쓰는 경로다. 둘째는 `SystemServiceRegistry`에 등록되지 않은(또는 등록할 수 없는) 서비스를 위해 `ServiceManager`에서 Binder 참조를 직접 조회해 AIDL 스텁을 감싸는 경로다. 셋째는 앱 프로세스 안에서 JNI를 거쳐 HAL을 hwbinder로 직접 여는 경로로, 이는 뒤에서 다룰 이유로 대부분의 상황에서 피해야 하는 안티패턴에 가깝다. 이 세 경로가 각각 어떤 대가를 치르는지는 다음 절의 비교 표에서 다룬다.

## 비교와 트레이드오프: 세 경로 중 무엇을 쓸 것인가

세 경로는 "얼마나 정식 절차를 거쳤는가"라는 하나의 축 위에 놓여 있다. 정식 절차를 거칠수록 프레임워크 패치와 SDK 문서화 비용이 늘어나지만 장기적인 호환성과 서드파티 공개 가능성을 얻고, 절차를 건너뛸수록 개발 속도는 빨라지지만 플랫폼 업그레이드에 취약해진다.

| 경로 | 구현 위치 | 필요 조건 | 프레임워크 패치 | 장점 | 단점 |
|---|---|---|---|---|---|
| A. 공개 매니저 (`getSystemService`) | 05장에서 다룬 `SystemServiceRegistry` 등록 서비스 | 해당 상수/래퍼 클래스에 대한 접근(공개 SDK 또는 벤더 제공 jar) | 필요 (`frameworks/base` 수정) | SDK 문서화 가능, 버전 호환성 관리 용이, 서드파티에도 공개 가능 | 프레임워크 소스 접근·빌드·재인증 비용 |
| B. 직접 Binder 조회 (`ServiceManager.getService`) | priv-app 프로세스 내부 | priv-app + SELinux `binder_call` 허용 + hidden API 정책 통과 | 불필요 | 프레임워크 소스를 건드리지 않고 빠르게 반복 가능 | non-SDK 인터페이스 정책 변경에 취약, 벤더 내부용으로만 안전 |
| C. HAL 직접 접근 (JNI + hwbinder) | 앱 프로세스 네이티브 레이어 | 커스텀 SELinux 도메인 + seapp_contexts 매핑 | 불필요(HAL 자체는 그대로) | 이론상 가장 낮은 지연 시간 | Treble 경계 우회로 VTS/CDD 위반 소지, 사실상 안티패턴 |

이 표가 가리키는 실무 판단은 단순하다. 서드파티 앱이나 다른 시스템 컴포넌트도 장기적으로 같은 기능을 쓸 가능성이 있다면 경로 A를 기본값으로 삼아야 한다 — 05장에서 다룬 등록 절차의 비용은 한 번만 치르면 되고, 그 이후로는 공개 SDK 앱과 동일한 안정성을 얻는다. 반대로 오직 자사 진단 앱 한 개만 이 서비스를 쓰고, 그 앱과 서비스를 같은 빌드에서 항상 함께 배포·업데이트한다면 경로 B로 개발 속도를 얻는 대신 non-SDK 인터페이스 정책 변경 위험을 스스로 감수하는 선택도 합리적일 수 있다. 경로 C는 원칙적으로 시스템 서비스나 네이티브 데몬만 열어야 하는 hwbinder 네임스페이스를 앱 프로세스가 직접 여는 것이므로, 정말로 시스템 서비스 계층조차 거칠 수 없는 극단적인 지연 시간 요구가 있지 않은 한 선택하지 않는 편이 안전하다.

## 실전 적용: Compose 기반 진단 앱에서 커스텀 시스템 서비스에 접근하기

05장에서 등록한 `DeviceMonitorService`의 발열 상태를 보여주는 벤더 진단 앱을 구성한다. 이 앱은 priv-app으로 배포되고, Compose로 화면을 그리며, 경로 A(공개 매니저)를 우선 사용하되 경로 B(직접 Binder 조회)를 대안으로 함께 구현해 두 경로의 코드 차이를 비교한다.

### Android.bp로 priv-app 선언하기

먼저 이 앱을 벤더 파티션의 특권 앱으로 빌드하도록 Android.bp 모듈을 정의한다. `privileged: true`는 이 앱이 priv-app 디렉터리에 설치되어야 함을, `certificate: "platform"`은 플랫폼 키로 서명됨을, `vendor: true`는 벤더 파티션에 설치됨을 각각 나타낸다. 정확한 필드 구성은 AOSP 버전에 따라 달라질 수 있으므로 실제 적용 시 해당 버전의 `build/soong` 문서를 함께 확인해야 한다.

```text
// vendor/example/apps/Diagnostics/Android.bp (개념 구조, 실제 필드는 AOSP 버전에 따라 다르다)
android_app {
    name: "VendorDiagnostics",
    srcs: ["src/**/*.kt"],
    manifest: "AndroidManifest.xml",
    privileged: true,
    certificate: "platform",
    vendor: true,
    static_libs: ["androidx.compose.material3_material3"],
}
```

매니페스트는 05장에서 정의한 `MONITOR` 권한을 선언한다. 이 선언만으로는 권한이 부여되지 않으며, 앞서 다룬 `privapp-permissions-vendor.xml`에 같은 패키지명·권한명 조합이 있어야 실제로 유효해진다.

```xml
<!-- vendor/example/apps/Diagnostics/AndroidManifest.xml -->
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.vendor.diagnostics">

    <uses-permission android:name="com.android.server.devicemonitor.permission.MONITOR" />

    <application
        android:label="Vendor Diagnostics"
        android:icon="@mipmap/ic_launcher">
        <activity
            android:name=".DiagnosticsActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
```

### 경로 A: 공개 매니저로 서비스 조회하기

05장에서 프레임워크에 `DeviceMonitorManager`를 등록해 두었다면, 앱은 그 클래스가 포함된 벤더 제공 jar를 컴파일 시점에 참조하는 것만으로 일반 SDK 앱과 동일한 방식으로 서비스를 쓸 수 있다. `Context.getSystemService(String)`은 공개 SDK 메서드이므로, 등록된 이름 문자열만 정확하다면 별도의 리플렉션이나 hidden API 우회 없이도 값을 돌려받는다.

```kotlin
// com/example/vendor/diagnostics/ThermalViewModel.kt
package com.example.vendor.diagnostics

import android.app.Application
import android.content.Context
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.android.server.devicemonitor.DeviceMonitorManager
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class ThermalViewModel(app: Application) : AndroidViewModel(app) {

    private val manager: DeviceMonitorManager? =
        getApplication<Application>().getSystemService("devicemonitor") as? DeviceMonitorManager

    private val _thermalStatus = MutableStateFlow(-1)
    val thermalStatus: StateFlow<Int> = _thermalStatus.asStateFlow()

    fun refresh() {
        viewModelScope.launch(Dispatchers.IO) {
            val status = manager?.getThermalStatus() ?: -1
            _thermalStatus.value = status
        }
    }
}
```

이 방식이 가능한 이유는 `getSystemService(String)`이 등록된 이름과 대조해 프레임워크가 만들어 둔 `DeviceMonitorManager` 인스턴스를 그대로 돌려주기 때문이다. 이 인스턴스는 non-SDK 인터페이스 정책이 감시하는 프레임워크 내부 클래스가 아니라, 벤더가 앱에 정식으로 배포한 공개 클래스이므로 hidden API 제약과 무관하게 안정적으로 동작한다.

### 경로 B: 프레임워크 패치 없이 직접 Binder 조회하기

만약 05장의 프레임워크 패치 절차를 아직 거치지 않았거나, 이 서비스가 오직 이 진단 앱 전용이라 공개 매니저를 만들 가치가 없다고 판단했다면, `ServiceManager`에서 Binder를 직접 조회해 AIDL 스텁으로 감싸는 방식으로도 같은 값을 얻을 수 있다. 다만 이 방식은 `android.os.ServiceManager.getService()`가 non-SDK 인터페이스이므로, 리플렉션으로 호출하더라도 기기의 hidden API 정책과 앱의 targetSdkVersion에 따라 차단될 수 있다는 점을 감안해야 한다.

```kotlin
// com/example/vendor/diagnostics/DirectBinderThermalSource.kt
package com.example.vendor.diagnostics

import android.os.IBinder
import com.android.server.devicemonitor.IDeviceMonitorService

class DirectBinderThermalSource {

    private val service: IDeviceMonitorService? by lazy {
        getServiceBinder("devicemonitor")?.let { IDeviceMonitorService.Stub.asInterface(it) }
    }

    private fun getServiceBinder(name: String): IBinder? = try {
        val serviceManagerClass = Class.forName("android.os.ServiceManager")
        val getService = serviceManagerClass.getMethod("getService", String::class.java)
        getService.invoke(null, name) as? IBinder
    } catch (e: ReflectiveOperationException) {
        // non-SDK 인터페이스 정책에 의해 차단되었거나 서비스가 아직 등록되지 않은 경우
        null
    }

    fun getThermalStatus(): Int = service?.getThermalStatus() ?: -1
}
```

이 코드에서 `ReflectiveOperationException`을 잡는 부분이 장식이 아니라는 점이 중요하다. non-SDK 인터페이스 정책이 이 메서드를 차단 목록에 올린 기기·버전 조합에서는 `getMethod()`나 `invoke()` 단계에서 예외가 발생하며, 이 실패는 컴파일 시점에는 전혀 드러나지 않고 특정 안드로이드 버전을 탑재한 기기에서만 런타임에 나타난다. 벤더가 이 경로를 선택한다면, 자사가 배포하는 정확한 안드로이드 버전 범위 안에서만 검증하고 그 범위를 벗어나면 재검증한다는 전제를 지켜야 한다.

### Compose로 화면 구성하기

두 소스 중 하나로부터 얻은 상태를 Compose 화면에 연결하는 부분은 어느 경로를 택했든 동일하다. `collectAsState()`가 `StateFlow`를 Compose가 관찰 가능한 State로 변환하고, 그 값이 바뀔 때마다 `Text`를 포함하는 영역만 리컴포지션된다.

```kotlin
// com/example/vendor/diagnostics/ThermalStatusScreen.kt
package com.example.vendor.diagnostics

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel

@Composable
fun ThermalStatusScreen(viewModel: ThermalViewModel = viewModel()) {
    val status by viewModel.thermalStatus.collectAsState()

    LaunchedEffect(Unit) {
        viewModel.refresh()
    }

    Column(modifier = Modifier.padding(24.dp)) {
        Text(
            text = "열 상태 코드: $status",
            style = MaterialTheme.typography.headlineSmall
        )
        Button(onClick = { viewModel.refresh() }) {
            Text("새로고침")
        }
    }
}
```

이 화면은 상태를 직접 소유하지 않고 `ThermalViewModel`이 노출한 `StateFlow`를 구독만 한다는 점에서 상태 호이스팅 원칙을 지킨다. 덕분에 같은 `ThermalStatusScreen` 컴포저블을 프리뷰 환경에서는 더미 `StateFlow`를 주입해 서비스 연결 없이도 렌더링을 확인할 수 있다.

## 흔한 오개념

**"priv-app 디렉터리에 넣기만 하면 `signature|privileged` 권한을 자동으로 받는다"**는 가장 흔한 오해다. 실제로는 privapp-permissions 화이트리스트에 패키지명과 권한명이 명시적으로 등록되어 있어야 하며, Android 9 이상의 `enforce` 모드에서는 이 등록이 빠지면 권한 거부에 그치지 않고 기기 부팅 자체가 막힌다. priv-app 배치와 권한 화이트리스트 등록은 서로 독립적인 두 단계이지 하나가 다른 하나를 포함하지 않는다.

**"Jetpack Compose를 도입하려면 기존 View 화면을 전부 다시 짜야 한다"**도 실무에서 자주 발목을 잡는 오해다. `ComposeView`와 `AndroidView`가 제공하는 상호운용 덕분에 기존 XML 레이아웃과 Compose 화면은 같은 액티비티 안에 공존할 수 있으며, 안정성이 검증된 레거시 화면은 그대로 두고 새로 추가하는 화면부터 Compose로 전환하는 점진적 마이그레이션이 표준적인 접근이다.

**"프레임워크를 패치해 `SystemServiceRegistry`에 등록하지 않으면 앱은 커스텀 시스템 서비스에 접근할 수 없다"**는 이 장에서 다룬 경로 B의 존재로 반박된다. 다만 이 경로는 non-SDK 인터페이스 정책의 적용을 받으므로 "가능하다"와 "안전하다"는 다른 이야기다. 실무에서는 이 경로를 자사 전용 진단 앱처럼 배포 범위와 안드로이드 버전을 스스로 통제할 수 있는 상황에 한정해서 쓴다.

## 비판적 시각

벤더 앱을 priv-app으로 배포하는 결정은 강력한 권한을 얻는 대신 배포 유연성을 희생하는 트레이드오프를 수반한다. 플레이스토어 앱은 사용자가 언제든 개별적으로 업데이트할 수 있지만, priv-app은 시스템 이미지의 일부이므로 그 앱의 버그 수정조차 OTA 업데이트를 기다려야 하는 경우가 많다. 이는 진단 앱처럼 자주 바뀌지 않는 도구에는 큰 문제가 아니지만, 사용자와 자주 상호작용하는 설정 앱이라면 이 배포 지연이 실질적인 비용이 된다. 이런 이유로 최근 플랫폼은 Project Mainline 같은 모듈화 메커니즘을 통해 일부 시스템 구성 요소를 APEX로 분리해 Play Store를 거쳐 갱신 가능하게 만드는 방향으로 움직이고 있으며, 새로운 벤더 앱을 설계할 때도 "정말 이 기능이 시스템 이미지에 고정되어야 하는가"를 먼저 따져보는 편이 안전하다.

경로 B(직접 Binder 조회)를 둘러싼 논쟁도 짚어둘 만하다. non-SDK 인터페이스 제한 정책은 구글이 프레임워크 내부 구현을 자유롭게 리팩터링할 수 있는 여지를 지키기 위한 것이지만, 벤더 입장에서는 프레임워크 소스를 건드리지 않고 빠르게 반복할 수 있는 유일한 실용적 수단을 제한하는 조치이기도 하다. 이 정책이 매 안드로이드 버전마다 차단 목록을 갱신하며 강화되어 온 것은 사실이지만, 그렇다고 경로 B가 항상 그른 선택은 아니다 — 배포 범위를 스스로 통제하는 자사 전용 도구에서는, 프레임워크 패치의 재인증 비용을 감수하기보다 이 위험을 감수하는 쪽이 합리적인 계산이 되는 경우도 실제로 존재한다.

## 다음 장에서는

[13장: AOSP 빌드 시스템 및 개발 도구](/post/android-hardware-development/aosp-build-system/)에서는 이 장에서 다룬 `Android.bp` 앱 모듈 정의가 실제로 Soong 빌드 그래프에 편입되어 시스템 이미지로 패키징되는 과정과, AOSP 개발에 필요한 빌드 도구 전반을 다룬다.

## 평가 기준

- [ ] priv-app과 일반 시스템 앱의 권한 모델 차이, privapp-permissions 화이트리스트가 강제되는 방식을 설명할 수 있다.
- [ ] Jetpack의 단방향 데이터 흐름 아키텍처와 Compose의 리컴포지션·상태 호이스팅 모델을 기존 View 시스템과 대비해 설명할 수 있다.
- [ ] 앱이 커스텀 시스템 서비스에 접근하는 세 경로(공개 매니저, 직접 Binder 조회, HAL 직접 접근)의 구현 방식과 트레이드오프를 비교할 수 있다.
- [ ] `Android.bp`에서 `privileged`/`certificate`/`vendor` 속성이 앱의 설치 위치·서명·권한 체계에 미치는 영향을 설명할 수 있다.
- [ ] 프레임워크 패치 없이 직접 Binder를 조회하는 방식이 non-SDK 인터페이스 정책 아래에서 어떤 위험을 동반하는지 판단할 수 있다.
- [ ] 벤더 진단 앱을 설계할 때 HAL 직접 접근 같은 안티패턴을 피해야 하는 이유를 인증·SELinux 관점에서 설명할 수 있다.

## 참고 및 출처

- Android Developers. "Jetpack Compose UI App Development Toolkit." *developer.android.com*, https://developer.android.com/jetpack/compose
- Android Developers. "Guide to app architecture." *developer.android.com*, https://developer.android.com/topic/libraries/architecture
- Android Developers. "Restrictions on non-SDK interfaces." *developer.android.com*, https://developer.android.com/guide/app-compatibility/restrictions-non-sdk-interfaces
- Android Open Source Project. "Privileged permission allowlisting." *source.android.com*, https://source.android.com/docs/core/permissions/perms-allowlist
