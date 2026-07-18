---
draft: false
collection_order: 30
slug: kernel-development
title: "[Android Hardware] 03. 커널 개발"
date: 2026-07-18
last_modified_at: 2026-07-18
description: "Android Common Kernel과 GKI 구조, ashmem·Binder·Wakelock·Low Memory Killer 같은 안드로이드 전용 커널 서브시스템, Device Tree 기반 하드웨어 기술, 커스텀 커널 빌드·플래시 절차를 이론과 실전 코드로 정리한다."
categories: Android Hardware Development
tags:
- Android
- Embedded(임베디드)
- Hardware(하드웨어)
- Kernel
- Linux(리눅스)
- C
- Mobile(모바일)
- Security(보안)
- Memory(메모리)
- Process
- Thread
- Debugging(디버깅)
- Performance(성능)
- Concurrency(동시성)
- Synchronization
- IO(Input/Output)
- Configuration(설정)
- Troubleshooting(트러블슈팅)
- Advanced
- System-Design
- SoC
- Device-Tree
- Binder-IPC
- Wakelock
- Low-Memory-Killer
- ashmem
- Android-Common-Kernel
- GKI
- Kbuild
- Bootloader
- Fastboot
- defconfig
- KMI
image: "wordcloud.png"
---

## 이 장을 읽기 전에

이 장은 [02장: 안드로이드 아키텍처](/post/android-hardware-development/android-architecture/)에서 다룬 소프트웨어 스택 전체 구조 중 가장 아래층, 즉 리눅스 커널 레이어를 파고든다. 02장에서 부트로더-커널-init-Zygote로 이어지는 부팅 흐름과 HAL·프레임워크 레이어의 위치를 이미 이해했다는 전제로 진행하므로, 커널 공간과 유저 공간의 구분, 시스템 호출이 무엇인지 정도는 알고 있다고 가정한다. 난이도 범위는 중급에서 전문가까지다 — "핵심 개념"과 "비교/트레이드오프"는 리눅스 커널을 처음 다뤄보는 안드로이드 개발자도 따라올 수 있게 썼고, "실전 적용"과 "비판적 시각"은 실제로 벤더 BSP(Board Support Package)를 다뤄본 사람에게 의미가 큰 수준으로 썼다. 이 장은 캐릭터/블록 디바이스 드라이버 작성법 전반이나 인터럽트·DMA 프로그래밍의 세부 API, 부트로더 자체의 구조는 다루지 않는다. 이런 주제는 이 시리즈의 이후 장인 디바이스 드라이버 개발 장과 부트로더 개발 장에서 별도로 다룬다. 또한 HAL 계층의 AIDL/HIDL 인터페이스 설계는 [04장: 하드웨어 추상화 계층(HAL) 개발](/post/android-hardware-development/hal-development/)의 영역이므로 이 장에서는 커널이 HAL에 무엇을 제공하는지까지만 언급한다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| 초급 (커널을 처음 접하는 안드로이드 개발자) | 도입, 핵심 개념 | ACK/GKI 구조와 ashmem·Binder·Wakelock·LMK 같은 안드로이드 전용 서브시스템이 왜 필요한지 설명할 수 있다 |
| 중급 (시스템 프로그래밍·드라이버 경험자) | 핵심 개념, 비교/트레이드오프, 실전 적용 | Device Tree 기반 드라이버 매칭 원리를 이해하고 GKI 빌드·플래시 파이프라인을 직접 구성할 수 있다 |
| 전문가 (커널 포팅·벤더 BSP 담당) | 비교/트레이드오프, 실전 적용, 비판적 시각 | KMI 안정성 제약 아래에서 벤더 모듈을 설계하고 보안·호환성 트레이드오프를 판단할 수 있다 |

## 도입

안드로이드 기기 개발에서 커널은 애플리케이션 개발자에게는 거의 보이지 않지만, 실제로는 배터리 수명·터치 반응성·메모리 회수 정책·프로세스 간 통신 성능을 좌우하는 계층이다. 스마트폰 제조사가 신제품마다 새 SoC(System on Chip)를 채택할 때, 프레임워크 코드는 거의 그대로 두면서도 커널만은 새 하드웨어에 맞춰 다시 빌드해야 한다. 이 작업이 왜 "리눅스 커널을 빌드하는 일"이 아니라 "안드로이드 커널을 빌드하는 일"로 따로 불리는지, 그리고 왜 구글이 최근 몇 년간 이 절차를 GKI(Generic Kernel Image)라는 이름으로 표준화했는지를 이해하는 것이 이 장의 목표다. 안드로이드는 표준 리눅스 커널만으로는 해결되지 않는 두 가지 문제, 즉 짧은 지연 시간이 요구되는 프로세스 간 통신(Binder)과 배터리에 민감한 절전 제어(Wakelock, LMK)를 커널 레벨에서 풀어야 했고, 이 과정에서 채택한 설계와 그것이 리눅스 메인라인과 충돌하거나 합쳐진 역사를 알면 지금의 GKI/Treble 구조가 왜 이런 모습인지가 자연스럽게 이해된다.

## 핵심 개념

### Android Common Kernel과 mainline Linux

**Android Common Kernel(안드로이드 공용 커널, ACK)**은 kernel.org에서 배포하는 LTS(Long Term Support) 커널의 다운스트림 프로젝트로, 안드로이드 생태계에 필요하지만 아직 리눅스 메인라인에 병합되지 않은 패치를 포함한 커널을 가리킨다. ACK는 `android-mainline`이라는 개발 브랜치를 주축으로 하며, 새 LTS 버전이 선언될 때마다 여기서 릴리스 브랜치가 갈라져 나온다. 브랜치 이름은 `ANDROID_RELEASE-KERNEL_VERSION` 형식(예: `android14-6.1`)을 따르고, 각 릴리스는 개발-안정화-KMI(Kernel Module Interface, 커널 모듈 인터페이스) 동결의 세 단계를 거친다. 즉 ACK와 mainline Linux의 관계는 "완전히 다른 커널"이 아니라 "메인라인에 아직 없는 안드로이드 특화 패치를 얹은 LTS 커널"에 가깝다. 실제로 Binder 드라이버는 오랫동안 안드로이드만의 아웃오브트리(out-of-tree) 패치였다가 스테이징 트리를 거쳐 정식 드라이버 트리인 `drivers/android/`로 승격되었고, 지금도 리눅스 커널 소스 안에 `binder.c`로 존재한다(정확히 어느 버전에서 승격되었는지는 배포판 문서마다 표기가 갈릴 수 있어 여기서는 특정 버전 번호를 단정하지 않는다). 커널 6.6부터는 ACK가 4년의 지원 수명을 제공하도록 정책이 정리되었고, GKI 커널이라는 표현은 커널 5.10 이상의 ACK를 가리키는 데 쓰인다.

**GKI(Generic Kernel Image, 범용 커널 이미지)**는 벤더가 SoC·보드별 코드를 커널 소스 자체에 패치해 넣던 관행을 끊기 위한 구조다. 핵심 아이디어는 커널 이미지를 두 부분으로 나누는 것이다. 하나는 구글이 배포하는 공용 코어 커널 이미지(`boot.img`)이고, 다른 하나는 SoC·보드 제조사가 커널 모듈(`.ko`) 형태로 제공하는 벤더 코드(`vendor_boot.img`, `vendor_dlkm.img`)다. 두 부분은 KMI라는 안정된 심볼 목록으로 연결되며, KMI가 동결된 이후에는 코어 커널을 업데이트해도 벤더 모듈을 다시 빌드하지 않아도 동작해야 한다는 것이 GKI의 계약이다. 이 구조 덕분에 구글은 보안 패치를 벤더 커널 소스를 일일이 건드리지 않고도 Play 시스템 업데이트 형태로 배포할 수 있게 되었다. 다만 이 계약은 "벤더가 커널을 전혀 건드릴 수 없다"는 뜻이 아니라 "코어 커널 소스는 건드리지 않고, 모듈이라는 안정된 경계를 통해서만 확장한다"는 뜻이라는 점이 중요하다.

### Binder 드라이버

**Binder(바인더) 드라이버**는 안드로이드의 프로세스 간 통신(IPC)을 커널 레벨에서 지원하는 캐릭터 디바이스 드라이버다. 전통적인 리눅스 IPC 수단인 소켓·파이프·System V IPC는 프로세스 경계를 넘을 때마다 데이터를 커널 버퍼로 복사하고 다시 사용자 버퍼로 복사하는 이중 복사가 필요하지만, Binder는 송신 프로세스의 데이터를 수신 프로세스의 주소 공간에 매핑된 커널 버퍼로 한 번만 복사한다. 각 프로세스는 `/dev/binder`를 `mmap`으로 매핑해 이 공유 버퍼를 확보하고, `ioctl(BINDER_WRITE_READ)`를 통해 트랜잭션을 주고받는다. Binder는 단순한 메시지 전달 이상의 역할을 하는데, 원격 객체에 대한 참조 카운팅, 프로세스가 죽었을 때 상대방에게 알려주는 death notification, 그리고 호출자의 UID/PID를 커널이 보증해 주는 신원 확인까지 담당한다. 이 신원 확인 기능이 있기 때문에 SELinux와 결합한 권한 검사, 시스템 서비스 간 인증이 애플리케이션 코드의 자체 검증 없이도 성립한다.

### ashmem과 wakelock

**ashmem(Anonymous Shared Memory, 익명 공유 메모리)**은 이름 없는(anonymous) 메모리 영역을 여러 프로세스가 파일 디스크립터를 통해 공유하도록 해 주는 메커니즘이다. 일반적인 `mmap(MAP_ANONYMOUS)`와 다른 점은, ashmem 영역에 이름과 크기를 부여하고 `ASHMEM_UNPIN`으로 "지금 당장은 안 쓰지만 필요하면 다시 채울 수 있는" 영역으로 표시할 수 있다는 것이다. 커널은 메모리 압박 상황에서 unpin된 영역을 회수하고, 다음에 그 영역을 pin하려는 프로세스에게 "회수되었으니 다시 채우라"고 알려준다. 이는 캐시성 데이터(비트맵 등)를 위한 자원 관리에 유용했다. 다만 최근 안드로이드 버전에서는 커널 드라이버 형태의 `/dev/ashmem` 대신, `memfd_create` 기반의 유저스페이스 에뮬레이션으로 같은 API를 흉내 내는 방식이 점점 널리 쓰이고 있다(정확한 전환 시점과 적용 범위는 기기와 커널 버전에 따라 다르다). GKI 커널에는 ashmem 드라이버가 포함되지 않는 경우가 흔해서, 이 유저스페이스 에뮬레이션이 사실상 기본 경로가 되어 가고 있다.

**wakelock(웨이크락)**은 시스템이 절전 상태(suspend)로 들어가지 못하게 막는 커널 자원이다. 초기 안드로이드는 `wake_lock()`/`wake_unlock()`이라는 아웃오브트리 API를 직접 만들어 썼는데, 이는 리눅스 메인라인 개발자들과 상당한 논쟁을 낳았다. 임베디드 진영은 "앱이 명시적으로 깨어 있음을 선언해야 배터리를 아낄 수 있다"고 주장했고, 메인라인 진영은 "그런 정책은 커널이 아니라 유저스페이스가 판단해야 한다"고 맞섰다. 이 논쟁은 결국 리눅스 메인라인이 **wakeup source(웨이크업 소스)**라는 좀 더 일반화된 개념을 받아들이는 것으로 정리되었고(2012년경 커널 3.5 전후로 병합된 것으로 알려져 있다), 드라이버는 `device_init_wakeup()`으로 디바이스를 깨어남의 원천으로 등록하고 `pm_wakeup_event()`로 절전 진입을 잠시 지연시키는 식으로 절전을 제어한다. 레거시 `/sys/power/wake_lock` 인터페이스는 호환을 위해 일부 커널에 남아 있지만, 새 드라이버를 작성할 때는 표준 wakeup source API를 쓰는 것이 정석이다.

### Low Memory Killer

**low memory killer(LMK, 메모리 부족 킬러)**는 리눅스 커널의 OOM(Out Of Memory) killer가 개입하기 전에 선제적으로 우선순위가 낮은 프로세스를 종료해 메모리를 확보하는 안드로이드의 메커니즘이다. 리눅스의 OOM killer는 메모리 할당이 정말로 실패하는 마지막 순간에야 개입하는 최후의 보루인 반면, 모바일 기기는 그 지경에 이르기 전에 백그라운드 앱을 미리 정리해야 사용자가 스와핑이나 프리징을 체감하지 않는다. 초기 구현은 `drivers/staging/android/lowmemorykiller.c`라는 커널 드라이버였고, 각 프로세스의 `oom_score_adj` 값과 여유 메모리 페이지 수를 비교해 종료 대상을 골랐다. 이 커널 내장 드라이버는 리눅스 4.12 이후 커널 소스에서 제거되었고, 이후 역할은 유저스페이스 데몬인 lmkd가 이어받았다. Android 10부터는 lmkd가 PSI(Pressure Stall Information)라는 커널 지표를 활용해 기존 `vmpressure` 신호가 갖고 있던 거짓 양성(false positive) 문제를 줄이고 더 정확한 메모리 압박 감지를 하도록 개선되었으며, `ro.lmk.use_psi`, `ro.lmk.psi_partial_stall_ms` 같은 속성으로 기기별 튜닝이 가능하다. 즉 "안드로이드에는 LMK가 있다"는 문장은 이제 커널 드라이버가 아니라 유저스페이스 데몬을 가리킨다는 점이 최근 몇 년 사이 가장 크게 바뀐 부분이다.

### Device Tree

**Device Tree(디바이스 트리)**는 커널 이미지를 재컴파일하지 않고도 보드에 어떤 하드웨어가 어떤 주소·인터럽트 번호로 연결되어 있는지를 기술하는 데이터 구조다. 개발자는 `.dts`(Device Tree Source) 파일에 노드와 속성을 텍스트로 작성하고, `dtc`(Device Tree Compiler)로 이를 `.dtb`(Device Tree Blob) 바이너리로 컴파일한다. 커널은 부팅 시 이 바이너리를 읽어 각 노드의 `compatible` 속성과 드라이버의 `of_match_table`을 대조해 어떤 드라이버가 어떤 하드웨어를 담당할지 자동으로 매칭한다. 안드로이드는 여기에 **DTO(Device Tree Overlay, 디바이스 트리 오버레이)**라는 확장을 더해, 부트로더가 SoC 공통의 기본 DTB 위에 기기별 DTBO(overlay용 DTB)를 겹쳐 적용할 수 있게 했다. 이렇게 하면 같은 SoC를 쓰는 여러 기기가 공통 커널 이미지 하나를 공유하면서도, 기기마다 다른 센서·디스플레이 구성을 오버레이만으로 표현할 수 있다. Android 9부터는 부트로더가 오버레이 속성을 임의로 수정하지 않고 병합된 통합 DTB를 그대로 커널에 전달해야 한다는 요구사항이 추가되어, 오버레이 적용 결과의 일관성이 강화되었다.

## 비교/트레이드오프

과거의 벤더 포크 방식과 현재의 GKI 방식, 그리고 각 서브시스템의 레거시 구현과 현대적 구현은 저마다 다른 트레이드오프를 갖는다. 아래 표는 이 장에서 다룬 서브시스템별로 "예전에 흔히 쓰던 방식"과 "지금 권장되는 방식"을 대비한 것이다.

| 구분 | 과거 방식 | 현재 권장 방식 | 선택 기준 |
|---|---|---|---|
| 공유 메모리 | `/dev/ashmem` 커널 드라이버 | `memfd_create` 기반 유저스페이스 ashmem 에뮬레이션, 대용량 그래픽 버퍼는 ION/DMA-BUF heap | 신규 드라이버·HAL 코드는 dma-buf heap을 우선 검토하고, 기존 ashmem API 호출부는 그대로 두어도 무방하다 |
| 메모리 회수 | 커널 내장 lowmemorykiller 드라이버(~리눅스 4.12) | 유저스페이스 lmkd + PSI 기반 압박 감지 | GKI 커널에는 인커널 LMK가 없으므로 lmkd 설정(oom_score_adj, PSI 임계값) 튜닝이 필수다 |
| 절전 제어 | 아웃오브트리 `wake_lock()`/`wake_unlock()` | 표준 wakeup source API(`device_init_wakeup`, `pm_wakeup_event`) | 새 플랫폼 드라이버는 wakeup source API로 작성하고, 레거시 sysfs 인터페이스는 호환 목적에만 의존한다 |
| 벤더 코드 위치 | 벤더가 커널 소스 전체를 포크해 직접 패치 | GKI 코어 이미지 + 안정된 KMI로 연결된 벤더 모듈(.ko) | Treble을 준수해야 하는 신규 기기는 GKI가 사실상 필수이며, 레거시 기기·특수 목적 커스텀 롬만 완전 포크 방식을 고려한다 |

이 표에서 "과거 방식"이 곧바로 틀렸다는 뜻은 아니다. 완전히 통제된 단일 기기(예: 상용화하지 않는 사내 레퍼런스 보드)를 다룬다면 커널을 통째로 포크해 자유롭게 패치하는 쪽이 오히려 개발 속도가 빠를 수 있다. 반대로 여러 SoC 파트너와 협업해야 하는 양산 제품이라면 GKI의 KMI 계약을 지키는 편이 보안 패치 배포 속도와 장기 유지보수 비용 면에서 유리하다. 즉 선택 기준은 "옳고 그름"이 아니라 "이 기기가 몇 개의 커널 업데이트를 몇 년 동안 받아야 하는가"라는 질문에 달려 있다.

## 실전 적용

GKI를 지원하는 레퍼런스 기기에 새로운 센서 인터럽트를 wakeup source로 등록하는 플랫폼 드라이버를 추가하고, 이를 Device Tree에 기술한 뒤 커널을 빌드해 기기에 플래시하는 흐름을 예로 든다. 먼저 하드웨어가 어떤 핀에 연결되어 있는지를 Device Tree 노드로 선언한다. 아래 예제는 I2C 버스 3번에 연결된 센서가 GPIO 21번을 인터럽트 겸 wakeup 신호로 사용한다고 가정한 것이다.

```dts
&i2c3 {
    sensor_wake_irq: sensor-wake@44 {
        compatible = "example,sensor-wake-irq";
        reg = <0x44>;
        wake-gpios = <&tlmm 21 GPIO_ACTIVE_HIGH>;
        interrupt-parent = <&tlmm>;
        interrupts = <21 IRQ_TYPE_EDGE_RISING>;
        wakeup-source;
    };
};
```

`compatible = "example,sensor-wake-irq"` 문자열은 드라이버 쪽의 `of_match_table`과 정확히 일치해야 커널이 이 노드를 해당 드라이버에 매칭한다. `wakeup-source` 속성은 이 노드가 시스템을 깨울 수 있는 장치임을 커널의 전력 관리 서브시스템에 미리 알려주는 역할을 한다. 이 선언을 받는 플랫폼 드라이버는 인터럽트를 등록하고, 인터럽트가 발생하면 레거시 wakelock 대신 표준 wakeup source API로 절전 진입을 지연시킨다.

```c
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/platform_device.h>
#include <linux/of.h>
#include <linux/of_device.h>
#include <linux/interrupt.h>
#include <linux/pm_wakeup.h>
#include <linux/gpio/consumer.h>
#include <linux/slab.h>

struct sensor_wake_data {
    struct device *dev;
    struct gpio_desc *irq_gpio;
    int irq;
};

static irqreturn_t sensor_wake_irq_handler(int irq, void *data)
{
    struct sensor_wake_data *wake_data = data;

    /* 300ms 동안 절전 진입을 지연시켜 유저스페이스가 이벤트를 처리할 시간을 확보한다 */
    pm_wakeup_event(wake_data->dev, 300);

    return IRQ_HANDLED;
}

static int sensor_wake_probe(struct platform_device *pdev)
{
    struct sensor_wake_data *wake_data;
    int ret;

    wake_data = devm_kzalloc(&pdev->dev, sizeof(*wake_data), GFP_KERNEL);
    if (!wake_data)
        return -ENOMEM;

    wake_data->dev = &pdev->dev;
    wake_data->irq_gpio = devm_gpiod_get(&pdev->dev, "wake", GPIOD_IN);
    if (IS_ERR(wake_data->irq_gpio))
        return PTR_ERR(wake_data->irq_gpio);

    wake_data->irq = gpiod_to_irq(wake_data->irq_gpio);
    if (wake_data->irq < 0)
        return wake_data->irq;

    ret = devm_request_threaded_irq(&pdev->dev, wake_data->irq, NULL,
                                     sensor_wake_irq_handler,
                                     IRQF_TRIGGER_RISING | IRQF_ONESHOT,
                                     "sensor-wake", wake_data);
    if (ret)
        return ret;

    /* 레거시 wake_lock() 대신 표준 wakeup source를 디바이스에 등록한다 */
    device_init_wakeup(&pdev->dev, true);
    platform_set_drvdata(pdev, wake_data);

    return 0;
}

static int sensor_wake_remove(struct platform_device *pdev)
{
    device_init_wakeup(&pdev->dev, false);
    return 0;
}

static const struct of_device_id sensor_wake_of_match[] = {
    { .compatible = "example,sensor-wake-irq" },
    { }
};
MODULE_DEVICE_TABLE(of, sensor_wake_of_match);

static struct platform_driver sensor_wake_driver = {
    .probe = sensor_wake_probe,
    .remove = sensor_wake_remove,
    .driver = {
        .name = "sensor-wake-irq",
        .of_match_table = sensor_wake_of_match,
    },
};
module_platform_driver(sensor_wake_driver);

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Example wakeup-source platform driver for Android GKI");
```

이 드라이버를 빌드에 포함시키려면 `drivers/misc/`(또는 벤더 모듈 트리) 아래에 Kconfig 항목과 Makefile 규칙을 추가해야 한다. GKI 체계에서는 이 모듈이 코어 커널이 아니라 벤더 모듈로 빌드되어 `vendor_dlkm.img`에 담기는 것이 일반적이다.

```text
# drivers/misc/Kconfig
config SENSOR_WAKE_IRQ
    tristate "Example sensor wakeup-source driver"
    depends on OF && GPIOLIB
    help
      GKI 벤더 모듈로 빌드되는 예제 wakeup-source 플랫폼 드라이버다.

# drivers/misc/Makefile
obj-$(CONFIG_SENSOR_WAKE_IRQ) += sensor_wake_irq.o
```

전체 흐름은 소스 동기화, Kleaf(Bazel) 빌드, 이미지 플래시의 세 단계로 요약된다.

```mermaid
flowchart LR
    kernelSrc["Android Common Kernel</br>(android-mainline / android14-6.1)"] --> vendorFork["벤더 BSP</br>(defconfig + 모듈 소스)"]
    vendorFork --> kleafBuild["Kleaf/Bazel 빌드</br>(bazel run //common:kernel_aarch64_dist)"]
    kleafBuild --> images["boot.img / vendor_boot.img</br>/ dtbo.img / *.ko"]
    images --> fastbootFlash["fastboot flash"]
    fastbootFlash --> device["대상 기기</br>(부트로더 언락 필요)"]
```

Android 13 이상의 ACK는 Kleaf라는 Bazel 기반 빌드 시스템을 표준으로 채택했다. 이는 환경 변수에 의존하던 레거시 `build.sh` 방식보다 재현성이 높고, `defconfig` 프래그먼트로 커널 설정을 조합하기 쉽다는 장점이 있다. 실제 빌드와 플래시는 아래와 같은 명령으로 진행한다.

```bash
# GKI 커널 소스 동기화 (android14-6.1 예시)
repo init -u https://android.googlesource.com/kernel/manifest -b android14-6.1
repo sync -c -j"$(nproc)"

# Kleaf(Bazel) 기반 빌드 - Android 13 이상 권장 방식
tools/bazel run //common:kernel_aarch64_dist -- --dist_dir=out/dist

# 빌드 산출물을 기기에 플래시한다 (부트로더 언락 상태여야 한다)
fastboot flash boot out/dist/boot.img
fastboot flash dtbo out/dist/dtbo.img
fastboot flash vendor_dlkm out/dist/vendor_dlkm.img
fastboot reboot
```

플래시 전에는 반드시 대상 파티션(boot, dtbo, vendor_dlkm 등)이 기기의 파티션 레이아웃과 일치하는지 확인해야 한다. GKI 코어 이미지만 새로 빌드했다면 `boot.img`만 교체하면 되지만, 새 드라이버 모듈을 추가했다면 그 모듈이 담긴 `vendor_dlkm.img`도 함께 갱신해야 부팅 시 모듈이 로드된다. 또한 부트로더 언락은 기기의 Verified Boot 체인을 깨뜨리므로, 실기기에서 이 절차를 실행하기 전에는 데이터 초기화와 보증·무결성 검증 실패 가능성을 감수해야 한다.

## 흔한 오개념

**"Wakelock은 최신 안드로이드에서 완전히 사라졌다"**는 정확하지 않다. 사라진 것은 구글이 리눅스 메인라인과 오래 대립했던 아웃오브트리 구현 방식이지, "절전 진입을 지연시킨다"는 개념 자체가 아니다. 그 개념은 wakeup source API라는 표준화된 형태로 메인라인에 흡수되었고, 유저스페이스에서는 `PowerManager.WakeLock` API가 지금도 정상적으로 동작한다. "wakelock이 사라졌다"보다는 "wakelock을 구현하는 커널 인터페이스가 표준화되었다"가 더 정확한 서술이다.

**"GKI를 쓰면 벤더는 커널을 전혀 커스터마이징할 수 없다"**도 흔한 오해다. GKI가 금지하는 것은 코어 커널 소스 자체를 벤더가 임의로 패치하는 관행이지, 벤더의 하드웨어 지원 코드 자체가 아니다. 벤더는 여전히 자신의 SoC·주변장치를 위한 드라이버를 커널 모듈로 작성해 `vendor_dlkm` 파티션에 담을 수 있다. 다만 그 모듈이 코어 커널의 심볼에 의존한다면, 그 심볼이 KMI로 안정성이 보장된 것인지 확인해야 한다는 제약이 새로 생겼을 뿐이다.

**"Low Memory Killer와 OOM killer는 같은 것이다"**도 자주 나오는 혼동이다. 두 메커니즘은 목적과 개입 시점이 다르다. 리눅스 커널의 OOM killer는 메모리 할당이 정말로 실패하기 직전에 개입하는 최후 수단이며, 어떤 프로세스를 죽여야 시스템 전체가 회복되는지를 기준으로 판단한다. 반면 lmkd(과거의 커널 내장 LMK)는 그 지경에 이르기 훨씬 전에, 사용자 체감 성능을 지키기 위해 우선순위가 낮은 백그라운드 앱을 선제적으로 종료한다. 실무에서 앱이 예상치 못하게 종료되는 문제를 조사할 때 이 둘을 구분하지 못하면 로그에서 엉뚱한 곳을 찾게 된다.

## 비판적 시각

GKI와 KMI 동결은 보안 패치 배포 속도를 크게 개선했지만 공짜로 얻은 이득은 아니다. KMI가 한번 동결되면 코어 커널의 심볼 시그니처를 함부로 바꿀 수 없으므로, 심각한 설계 결함이 뒤늦게 발견되더라도 다음 LTS 사이클까지 구조적으로 고치기 어려운 경우가 생긴다. 구글은 이를 완화하기 위해 ABI 모니터링 도구로 심볼 변경을 추적하지만, 이는 "완전한 자유"와 "완전한 안정성" 사이의 트레이드오프를 도구로 관리하는 것이지 트레이드오프 자체를 없애는 것은 아니다. Binder 역시 설계 이후 스캐터-게이터 최적화, 프로세스 프리즈 알림, oneway 트랜잭션 큐잉 한계 대응 등 여러 차례 개선을 거쳤을 만큼, 원설계가 오늘날의 대규모 시스템 서비스 통신량을 처음부터 완벽히 예견했다고 보기는 어렵다. lmkd의 PSI 기반 접근도 `vmpressure`보다 개선된 것은 분명하지만 여전히 휴리스틱이며, 제조사마다 임계값 튜닝이 달라 같은 안드로이드 버전에서도 기기별로 백그라운드 앱이 종료되는 시점이 크게 달라지는 현상은 앱 개발자에게 실질적인 골칫거리로 남아 있다. 마지막으로, 커스텀 커널을 빌드해 플래시하는 능력은 연구·개발에는 강력한 도구지만, 부트로더 언락이 Verified Boot 체인과 기기 무결성 증명(예: Play Integrity 계열 검사)에 미치는 영향을 정확히 이해하지 못한 채 진행하면 실제 서비스 배포 환경과는 다른 조건에서 테스트하게 되는 함정에 빠지기 쉽다.

## 다음 장에서는

[04장: 하드웨어 추상화 계층(HAL) 개발](/post/android-hardware-development/hal-development/)에서는 이 장에서 다룬 커널 드라이버가 상위 프레임워크와 어떻게 연결되는지, 즉 커널 인터페이스를 감싸는 HAL 계층의 구조와 AIDL 기반 구현 방법을 다룬다.

## 평가 기준

이 장을 읽은 후에는 다음을 할 수 있어야 한다. Android Common Kernel이 mainline Linux와 어떤 관계인지, GKI와 KMI가 이 관계를 어떻게 구조화하는지 설명할 수 있다. Binder 드라이버가 소켓·파이프 같은 전통적 IPC와 비교해 어떤 지점에서 데이터 복사를 줄이는지 설명할 수 있다. ashmem·wakelock·LMK가 각각 어떤 문제를 풀기 위해 등장했고, 그중 어떤 부분이 최근 유저스페이스 구현으로 옮겨갔는지 구분할 수 있다. Device Tree 노드의 `compatible` 속성이 드라이버 매칭에서 어떤 역할을 하는지 설명할 수 있다. Kleaf 기반 빌드로 커널 이미지를 만들고 `fastboot`로 기기에 플래시하는 절차를 순서대로 수행할 수 있다. GKI가 벤더의 자유도를 제한하는 지점과, 그 제한이 KMI 안정성이라는 대가로 얻는 이득이 무엇인지 판단 기준을 가지고 설명할 수 있다.

## 참고 및 출처

- Android Open Source Project, "Kernel overview," [source.android.com/docs/core/architecture/kernel](https://source.android.com/docs/core/architecture/kernel)
- Android Open Source Project, "Android common kernels," [source.android.com/docs/core/architecture/kernel/android-common](https://source.android.com/docs/core/architecture/kernel/android-common)
- Android Open Source Project, "Generic Kernel Image (GKI) release builds," [source.android.com/docs/core/architecture/kernel/gki-release-builds](https://source.android.com/docs/core/architecture/kernel/gki-release-builds)
- Android Open Source Project, "Build kernels," [source.android.com/docs/setup/build/building-kernels](https://source.android.com/docs/setup/build/building-kernels)
- Android Open Source Project, "Low memory killer daemon," [source.android.com/docs/core/perf/lmkd](https://source.android.com/docs/core/perf/lmkd)
- Android Open Source Project, "Device tree overlays," [source.android.com/docs/core/architecture/dto](https://source.android.com/docs/core/architecture/dto)
- Linux kernel source tree, `drivers/android/binder.c`, Bootlin Elixir Cross Referencer, [elixir.bootlin.com/linux/latest/source/drivers/android/binder.c](https://elixir.bootlin.com/linux/latest/source/drivers/android/binder.c)
