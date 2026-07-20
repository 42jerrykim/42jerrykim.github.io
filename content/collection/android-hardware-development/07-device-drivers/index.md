---
draft: false
collection_order: 70
slug: device-drivers
title: "[Android Hardware] 07. 디바이스 드라이버 개발"
date: 2026-07-18
last_modified_at: 2026-07-18
description: "커널 모듈과 캐릭터·플랫폼 드라이버 구조, sysfs·ioctl 두 제어 경로의 트레이드오프를 이론적으로 정리하고, IMU 센서 드라이버를 실제로 작성해 AIDL 센서 HAL과 연결하는 과정과 V4L2 카메라 드라이버가 카메라 HAL로 이어지는 방식을 실전 예제로 설명한다."
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
- System-Design
- Interface(인터페이스)
- IO(Input/Output)
- Concurrency(동시성)
- Debugging(디버깅)
- Advanced
- Deep-Dive
- Kernel-Module
- Character-Driver
- Platform-Driver
- sysfs
- ioctl
- IIO
- I2C
- SPI
- GPIO
- Device-Tree
- Sensor-HAL
- Camera-HAL
- V4L2
- Media-Controller
- cdev
image: "wordcloud.png"
---

## 이 장을 읽기 전에

이 장은 시리즈 순서상 [06장: 프레임워크 커스터마이징](/post/android-hardware-development/framework-customization/) 뒤에 오지만, 내용상으로는 그보다 앞선 두 장과 더 밀접하게 연결된다. [03장: 커널 개발](/post/android-hardware-development/kernel-development/)에서 캐릭터·플랫폼 드라이버의 기초 개념을 다뤘다면, 이 장은 그 개념을 실제로 컴파일 가능한 코드 수준까지 심화하고, 드라이버가 노출한 제어 인터페이스가 [04장: 하드웨어 추상화 계층(HAL) 개발](/post/android-hardware-development/hal-development/)에서 정의한 AIDL HAL 서비스와 정확히 어떻게 맞물리는지를 끝까지 추적한다. 난이도는 중급–전문가 범위이며, 리눅스 커널 빌드 시스템 자체(Kbuild, Kconfig 구성)나 인터럽트 하위 처리(threaded IRQ, tasklet, workqueue의 세부 스케줄링 차이) 같은 커널 내부 메커니즘은 다루지 않는다. 이런 내용은 커널 서브시스템 자체를 주제로 삼는 별도 자료나 커널 문서를 참고하는 편이 낫다. 이 장의 목표는 드라이버 API를 통째로 암기하는 것이 아니라, "왜 어떤 데이터는 sysfs로 노출하고 어떤 데이터는 ioctl로 내보내는가"라는 설계 판단과 "커널 드라이버가 만든 노드를 HAL이 어떻게 소비 계약으로 굳히는가"를 이해하는 것이다.

| 수준 | 읽을 부분 | 핵심 목표 |
|:--:|:--|:--|
| 중급자 | 핵심 개념, 비교/트레이드오프, 실전 적용의 앞부분(커널 모듈~sysfs 속성 정의) | 커널 모듈이 로드되는 방식, 캐릭터 드라이버와 플랫폼 드라이버가 각각 어떤 문제를 푸는지, sysfs 속성을 어떻게 선언하는지 익힌다 |
| 실무자·전문가 | 실전 적용의 뒷부분(ioctl 데이터 평면–카메라 HAL 연결), 흔한 오개념, 비판적 시각 | 센서 HAL이 커널 노드를 여는 시점부터 실제 샘플이 Binder를 거쳐 프레임워크에 도달하기까지 전체 경로를 추적하고, GKI/KMI 체제가 벤더 드라이버 개발 관행에 어떤 제약을 거는지 판단한다 |

## 왜 드라이버 계층이 여전히 실무의 병목인가

HAL과 VINTF가 시스템/벤더 파티션을 깔끔하게 분리해 준다 해도, 그 경계선의 가장 아래쪽 끝에는 결국 실제 레지스터를 읽고 쓰는 커널 코드가 있어야 한다. 새로운 칩셋으로 제품을 개발하는 조직이 실제로 가장 많은 시간을 쓰는 지점은 화려한 AIDL 인터페이스 설계가 아니라, 이 커널 드라이버가 하드웨어의 기벽(errata)과 타이밍 제약을 견디면서도 그 위의 HAL 계층이 기대하는 계약을 정확히 지키게 만드는 작업이다. 드라이버 하나가 노출하는 인터페이스 설계가 잘못되면, 그 위에 아무리 잘 설계된 AIDL HAL을 올려도 결국 폴링 지연, 배터리 소모, 혹은 커널 패닉으로 이어진다.

이 장에서는 두 축을 동시에 다룬다. 하나는 커널 안에서 드라이버가 어떻게 구조화되는가(모듈, 캐릭터 디바이스, 플랫폼 디바이스)이고, 다른 하나는 그 드라이버가 사용자 공간과 대화하는 통로(sysfs, ioctl)를 어떻게 선택하는가이다. 이 두 축을 정확히 이해하고 있어야, 04장에서 다룬 HAL 구현체가 "왜 이 경로로 이 데이터를 가져오는지"를 코드만 보고도 설명할 수 있게 된다.

## 핵심 개념

### 커널 모듈: 빌드타임이 아니라 런타임에 커널을 확장하기

<strong>커널 모듈(Kernel Module)</strong>은 커널 이미지 전체를 재빌드하지 않고도 `insmod`/`modprobe`로 동적으로 적재하거나 `rmmod`로 제거할 수 있는 오브젝트 파일이다. 모듈은 `module_init()`으로 등록한 초기화 함수가 적재 시점에 한 번 호출되고, `module_exit()`으로 등록한 함수가 언로드 시점에 호출되는 생명주기를 갖는다. 안드로이드 기기에서 모듈 방식이 특히 중요한 이유는 **GKI(Generic Kernel Image, 범용 커널 이미지)** 정책 때문이다. 구글은 안드로이드 커널을 하드웨어에 독립적인 코어 커널과, 벤더가 별도로 빌드해 배포하는 벤더 모듈로 나누고, 이 둘 사이의 안정된 심볼 계약을 <strong>KMI(Kernel Module Interface)</strong>라는 이름으로 관리한다. 즉 칩셋 벤더가 작성하는 드라이버 상당수는 GKI 커널 본체에 정적으로 링크되는 코드가 아니라, GKI가 노출하는 KMI 심볼만 사용해 별도로 빌드되는 `.ko` 모듈이어야 한다.

다음은 최소한의 모듈 골격이다. 실제 드라이버는 이 골격 안에 캐릭터 디바이스나 플랫폼 드라이버 등록 코드를 추가하는 방식으로 확장된다.

```c
// drivers/misc/example_mod.c
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>

static int __init example_mod_init(void)
{
    pr_info("example_mod: 모듈 로드 완료\n");
    return 0;
}

static void __exit example_mod_exit(void)
{
    pr_info("example_mod: 모듈 언로드\n");
}

module_init(example_mod_init);
module_exit(example_mod_exit);

MODULE_LICENSE("GPL v2");
MODULE_DESCRIPTION("Example kernel module skeleton");
MODULE_AUTHOR("Example Vendor");
```

`MODULE_LICENSE`는 단순한 메타데이터가 아니라 컴파일 시점의 실질적 제약이다. `"GPL v2"`가 아닌 라이선스를 선언한 모듈은 `EXPORT_SYMBOL_GPL`로 노출된 커널 심볼을 링크할 수 없으며, 이는 커널 코드베이스가 라이선스 경계를 코드 수준에서 강제하는 방식이다.

### 캐릭터 드라이버: file_operations로 세우는 사용자-커널 경계

<strong>캐릭터 드라이버(Character Driver)</strong>는 바이트 스트림 형태로 데이터를 주고받는 장치를 `/dev` 아래의 노드로 노출하는 드라이버 유형이다. 커널은 이 노드에 대한 `open`, `read`, `write`, `ioctl`, `poll` 같은 시스템 호출을 `struct file_operations`에 등록된 함수 포인터로 위임하며, 사용자 공간 프로세스가 표준 POSIX 파일 API로 하드웨어와 대화할 수 있게 해준다. 드라이버는 부팅 시 `alloc_chrdev_region()`으로 메이저/마이너 번호를 할당받고, `cdev_init()`으로 `file_operations`를 캐릭터 디바이스 구조체에 묶은 뒤 `cdev_add()`로 커널에 등록한다.

```c
// drivers/iio/accel/example_accel_ioctl.h
#pragma once
#include <linux/ioctl.h>

#define EXAMPLE_ACCEL_MAGIC 'A'
#define EXAMPLE_ACCEL_IOCTL_GET_RANGE   _IOR(EXAMPLE_ACCEL_MAGIC, 1, int)
#define EXAMPLE_ACCEL_IOCTL_SET_RANGE   _IOW(EXAMPLE_ACCEL_MAGIC, 2, int)
#define EXAMPLE_ACCEL_IOCTL_FLUSH_FIFO  _IO(EXAMPLE_ACCEL_MAGIC, 3)
```

`_IOR`, `_IOW`, `_IO` 매크로는 방향(읽기/쓰기/없음)과 매직 번호, 명령 번호, 데이터 타입 크기를 하나의 32비트 값으로 인코딩한다. 매직 문자를 드라이버마다 다르게 고르는 관례는 서로 다른 드라이버의 ioctl 명령이 우연히 같은 값으로 충돌하는 사고를 줄이기 위한 것으로, 커널 문서는 이미 사용 중인 매직 문자 목록을 관리해 이 충돌을 예방한다.

### 플랫폼 드라이버: 버스 없는 SoC 내장 장치를 매칭하는 방법

PCI나 USB 장치는 버스 자체가 장치를 자동으로 열거(enumerate)해 주지만, SoC에 직접 매핑된 레지스터 블록(내장 센서 컨트롤러, 클록 컨트롤러, 전용 하드웨어 가속기 등)은 그런 자동 열거 메커니즘이 없다. <strong>플랫폼 드라이버(Platform Driver)</strong>는 이런 "버스 없는" 장치를 다루기 위한 리눅스 드라이버 모델의 하위 계층이다. 장치는 <strong>디바이스 트리(Device Tree)</strong>에 `compatible` 문자열과 메모리 주소 범위, 인터럽트 번호로 선언되고, 드라이버는 `of_device_id` 배열의 `compatible` 문자열과 커널이 일치시켜 준 뒤 `probe()` 콜백을 호출받는다. 이 매칭은 드라이버가 직접 하드웨어를 뒤지지 않고, 커널의 드라이버 코어가 디바이스 트리 파싱 결과와 등록된 드라이버 목록을 대조해 이루어진다.

I2C나 SPI 버스에 매달린 센서 IC는 이와는 다른 하위 모델을 쓴다는 점을 구분해야 한다. 그런 장치는 `platform_driver`가 아니라 `i2c_driver`/`spi_driver` 구조체로 등록되며, 매칭도 I2C/SPI 버스 고유의 `of_device_id` 또는 `i2c_device_id` 테이블을 통해 이루어진다. `probe`/`remove` 콜백 계약 자체는 플랫폼 드라이버와 거의 같은 형태를 따르지만, 버스 계층이 다르므로 두 모델을 뒤섞어 등록하면 매칭이 아예 이루어지지 않는다. 이 장의 실전 예제는 SoC에 직접 매핑된 센서 컨트롤러를 가정해 `platform_driver`로 구성하지만, 실제 IMU가 I2C 버스에 있다면 등록 부분만 `i2c_driver`로 바뀌고 `probe` 내부의 캐릭터 디바이스·sysfs 등록 로직은 그대로 재사용할 수 있다.

### sysfs와 ioctl: 제어 평면과 데이터 평면의 분리

**sysfs**는 커널 객체(`kobject`)의 속성을 `/sys` 아래의 일반 파일로 노출하는 RAM 기반 가상 파일시스템이다. 드라이버는 `show`/`store` 콜백 한 쌍을 `DEVICE_ATTR` 계열 매크로로 등록해 하나의 속성 파일을 만든다. sysfs의 설계 원칙은 "파일 하나에 값 하나"다. 여러 값을 한 줄에 섞어 넣거나 파일 하나에 서로 다른 의미의 데이터를 담는 것은 sysfs 관례에 어긋나며, 이 제약 때문에 sysfs는 저빈도 설정값(활성화 여부, 샘플링 주파수, 측정 범위)을 노출하는 데는 적합하지만, 초당 수백–수천 개씩 쏟아지는 연속 샘플 스트림을 실어 나르기에는 구조적으로 맞지 않는다.

**ioctl**은 `file_operations.unlocked_ioctl`로 등록하는 범용 제어 채널로, 임의의 구조체를 커널과 사용자 공간 사이에 주고받을 수 있다. sysfs가 "파일 하나=값 하나"라는 제약을 갖는 반면, ioctl은 명령 번호와 페이로드 구조체를 자유롭게 설계할 수 있어 배치 모드 설정이나 복잡한 캘리브레이션 파라미터처럼 여러 필드가 얽힌 데이터를 한 번의 호출로 주고받기에 유리하다. 다만 이 자유로움은 대가를 동반한다. ioctl 명령과 구조체 레이아웃은 sysfs처럼 표준화된 파일 하나짜리 관례가 없으므로, 드라이버 작성자가 명령 번호 충돌, 32비트/64비트 구조체 정렬 차이, 하위 호환성까지 스스로 책임져야 한다.

## 언제 sysfs를, 언제 ioctl을 쓸 것인가

두 인터페이스는 경쟁 관계가 아니라 상호 보완 관계로 쓰이는 경우가 훨씬 많다. 아래 표는 실무에서 이 둘을 나누는 기준이 되는 축을 정리한 것이다.

| 항목 | sysfs | ioctl (+ read/poll) |
|---|---|---|
| 적합한 데이터 성격 | 저빈도 설정값 (enable, 샘플링 주파수, 임계값) | 연속 데이터 스트림, 복잡한 구조체 페이로드 |
| 파일당 데이터 형태 | 단일 값 또는 동일 타입 배열 1개로 제한 | 임의의 구조체, 명령 번호로 다중 연산 표현 가능 |
| 사용자 도구 친화성 | `cat`/`echo`로 셸에서 직접 조작 가능 | 전용 클라이언트 코드(구조체 정의 공유) 필요 |
| 버전 관리 관례 | 커널 전역 sysfs ABI 문서화 관례가 있음 | 드라이버별 매직 번호로 관리, 표준 강제력이 약함 |
| 실시간성 | 폴링 기반, 이벤트 지연 시간이 상대적으로 큼 | `poll()`/`read()` 조합으로 블로킹 대기 가능, 지연 시간 최소화에 유리 |

이 표에서 실무적으로 가장 중요한 판단은 "설정은 sysfs로, 스트리밍 데이터는 캐릭터 디바이스의 ioctl+read로"라는 역할 분담이다. 뒤에서 다룰 IMU 예제가 정확히 이 패턴을 따른다. 측정 범위나 활성화 여부처럼 사람이 셸에서 즉시 확인하고 바꿀 만한 값은 sysfs 속성으로 노출하고, 초당 수백 회씩 발생하는 가속도 샘플은 캐릭터 디바이스의 `read()`와 `poll()`로 흘려보낸다. 이 역할 분담을 어기고 고빈도 데이터를 sysfs로 폴링하게 만들면, 사용자 공간이 매 샘플마다 파일을 열고 파싱하는 오버헤드를 감수해야 하고, 결과적으로 배터리 소모와 지연 시간 모두 악화된다.

## 실전 적용: IMU 센서 드라이버를 작성해 AIDL 센서 HAL과 연결하기

이제 SoC에 직접 매핑된 가상의 가속도계 컨트롤러를 위한 드라이버를 처음부터 구성하고, 이 드라이버가 노출한 인터페이스를 04장에서 다룬 패턴의 AIDL 센서 HAL이 어떻게 소비하는지 끝까지 추적한다. 하드웨어는 MMIO 레지스터로 접근하며, 인터럽트로 새 샘플이 준비되었음을 알린다고 가정한다.

### 디바이스 트리와 플랫폼 드라이버 등록

먼저 부트로더가 커널에 넘기는 디바이스 트리에 이 컨트롤러의 존재를 선언한다. `reg`는 레지스터 블록의 물리 주소와 크기를, `interrupts`는 GIC(Generic Interrupt Controller)에 연결된 인터럽트 라인을 나타낸다.

```text
// arch/arm64/boot/dts/example/example-board.dtsi (개념 구조, 실제 필드는 SoC 벤더에 따라 다르다)
accel_ctrl: accel-controller@1a300000 {
    compatible = "example,accel-imu";
    reg = <0x1a300000 0x1000>;
    interrupts = <GIC_SPI 118 IRQ_TYPE_LEVEL_HIGH>;
};
```

드라이버는 이 `compatible` 문자열을 `of_device_id` 테이블에 등록해 매칭시키고, `probe()`에서 캐릭터 디바이스와 sysfs 속성을 함께 준비한다.

```c
// drivers/iio/accel/example_accel.c (구조 축약)
#include <linux/module.h>
#include <linux/platform_device.h>
#include <linux/of.h>
#include <linux/cdev.h>
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/poll.h>
#include <linux/wait.h>
#include "example_accel_ioctl.h"

struct example_accel_dev {
    struct platform_device *pdev;
    struct cdev cdev;
    dev_t devt;
    int range_g;
    bool enabled;
    wait_queue_head_t read_wq;
};

static const struct of_device_id example_accel_of_match[] = {
    { .compatible = "example,accel-imu" },
    {}
};
MODULE_DEVICE_TABLE(of, example_accel_of_match);
```

`MODULE_DEVICE_TABLE`은 이 모듈이 어떤 `compatible` 문자열을 지원하는지를 모듈 메타데이터에 새겨, `modprobe`가 필요한 시점에 모듈을 자동으로 찾아 적재할 수 있게 해주는 매크로다.

### sysfs로 제어 평면 노출

측정 범위와 활성화 여부는 사람이 셸에서 즉시 조작하고 확인할 수 있어야 하는 값이므로 sysfs 속성으로 노출한다. `DEVICE_ATTR_RW`는 `show`/`store` 함수 쌍으로부터 읽기/쓰기가 모두 가능한 속성 파일을 만들어 준다.

```c
static ssize_t enable_show(struct device *dev, struct device_attribute *attr, char *buf)
{
    struct example_accel_dev *adev = dev_get_drvdata(dev);

    return sysfs_emit(buf, "%d\n", adev->enabled ? 1 : 0);
}

static ssize_t enable_store(struct device *dev, struct device_attribute *attr,
                             const char *buf, size_t count)
{
    struct example_accel_dev *adev = dev_get_drvdata(dev);
    bool val;
    int ret = kstrtobool(buf, &val);

    if (ret)
        return ret;

    adev->enabled = val;
    /* 실제 구현에서는 여기서 전원/스트리밍 관련 레지스터를 쓴다 */
    return count;
}
static DEVICE_ATTR_RW(enable);

static struct attribute *example_accel_attrs[] = {
    &dev_attr_enable.attr,
    NULL,
};
ATTRIBUTE_GROUPS(example_accel);
```

이렇게 등록한 속성은 `/sys/devices/.../accel_ctrl/enable` 경로에 나타나며, `echo 1 > enable`처럼 셸에서 직접 조작할 수 있다. 이는 디버깅 단계에서 HAL 코드를 거치지 않고 하드웨어 동작을 즉시 검증할 수 있게 해주는 실질적인 이점이다.

### ioctl과 poll로 데이터 평면 구성

연속 샘플 스트림은 sysfs가 아니라 캐릭터 디바이스의 `read()`/`poll()`로 흘려보낸다. `unlocked_ioctl`은 측정 범위 변경처럼 드물게 일어나지만 구조화된 파라미터가 필요한 제어에 쓰인다.

```c
static long example_accel_ioctl(struct file *filp, unsigned int cmd, unsigned long arg)
{
    struct example_accel_dev *dev = filp->private_data;
    int range;

    switch (cmd) {
    case EXAMPLE_ACCEL_IOCTL_GET_RANGE:
        if (copy_to_user((int __user *)arg, &dev->range_g, sizeof(int)))
            return -EFAULT;
        return 0;
    case EXAMPLE_ACCEL_IOCTL_SET_RANGE:
        if (copy_from_user(&range, (int __user *)arg, sizeof(int)))
            return -EFAULT;
        if (range != 2 && range != 4 && range != 8)
            return -EINVAL;
        dev->range_g = range;
        return 0;
    case EXAMPLE_ACCEL_IOCTL_FLUSH_FIFO:
        /* 하드웨어 FIFO 초기화 레지스터 접근은 생략 */
        return 0;
    default:
        return -ENOTTY;
    }
}

static ssize_t example_accel_read(struct file *filp, char __user *buf, size_t count, loff_t *ppos)
{
    struct example_accel_dev *dev = filp->private_data;
    int16_t sample[3];

    if (count < sizeof(sample))
        return -EINVAL;

    /* 실제 구현에서는 하드웨어 FIFO 레지스터에서 최신 샘플을 읽어온다 */
    if (copy_to_user(buf, sample, sizeof(sample)))
        return -EFAULT;

    return sizeof(sample);
}

static __poll_t example_accel_poll(struct file *filp, poll_table *wait)
{
    struct example_accel_dev *dev = filp->private_data;

    poll_wait(filp, &dev->read_wq, wait);
    /* 인터럽트 핸들러가 wake_up_interruptible(&dev->read_wq)을 호출하면
     * 여기서 EPOLLIN을 반환하도록 새 샘플 유무 플래그를 확인한다 */
    return 0;
}

static int example_accel_open(struct inode *inode, struct file *filp)
{
    filp->private_data = container_of(inode->i_cdev, struct example_accel_dev, cdev);
    return 0;
}

static const struct file_operations example_accel_fops = {
    .owner          = THIS_MODULE,
    .open           = example_accel_open,
    .read           = example_accel_read,
    .poll           = example_accel_poll,
    .unlocked_ioctl = example_accel_ioctl,
};

static int example_accel_probe(struct platform_device *pdev)
{
    struct example_accel_dev *adev;
    int ret;

    adev = devm_kzalloc(&pdev->dev, sizeof(*adev), GFP_KERNEL);
    if (!adev)
        return -ENOMEM;

    adev->pdev = pdev;
    adev->range_g = 2;
    init_waitqueue_head(&adev->read_wq);
    platform_set_drvdata(pdev, adev);

    ret = alloc_chrdev_region(&adev->devt, 0, 1, "example_accel");
    if (ret)
        return ret;

    cdev_init(&adev->cdev, &example_accel_fops);
    ret = cdev_add(&adev->cdev, adev->devt, 1);
    if (ret) {
        unregister_chrdev_region(adev->devt, 1);
        return ret;
    }

    return 0;
}

static void example_accel_remove(struct platform_device *pdev)
{
    struct example_accel_dev *adev = platform_get_drvdata(pdev);

    cdev_del(&adev->cdev);
    unregister_chrdev_region(adev->devt, 1);
}

static struct platform_driver example_accel_driver = {
    .driver = {
        .name = "example_accel",
        .of_match_table = example_accel_of_match,
        .dev_groups = example_accel_groups,
    },
    .probe  = example_accel_probe,
    .remove = example_accel_remove,
};
module_platform_driver(example_accel_driver);

MODULE_LICENSE("GPL v2");
MODULE_DESCRIPTION("Example IMU accelerometer platform driver");
```

`poll()` 구현에서 눈여겨봐야 할 부분은 `poll_wait()`가 즉시 블로킹하지 않고 대기 큐에 현재 프로세스를 등록만 한다는 점이다. 실제로 사용자 공간을 깨우는 것은 인터럽트 핸들러(이 예제에서는 생략)가 새 샘플이 준비되었을 때 `wake_up_interruptible()`을 호출하는 시점이며, 이 구조 덕분에 사용자 공간 스레드는 새 데이터가 없는 동안 CPU를 점유하지 않고 잠들어 있을 수 있다.

### 센서 HAL이 이 인터페이스를 소비하는 방법

커널 드라이버가 `/dev/example_accel` 노드와 그 아래 sysfs 속성을 만들었다고 해서 프레임워크가 이 데이터를 자동으로 받는 것은 아니다. 04장에서 다룬 것과 같은 패턴으로, 벤더 파티션의 센서 HAL 구현체가 이 노드를 명시적으로 열고, 정해진 ioctl 번호와 `read()` 페이로드 레이아웃을 알고 있어야 한다. 아래는 그 소비자 쪽 코드를 단순화한 예시다. 실제 `android.hardware.sensors` AIDL 인터페이스는 이벤트 큐잉·배치 모드·다중 센서 멀티플렉싱까지 포함해 훨씬 복잡하므로, 여기서는 커널 노드를 읽어오는 하위 계층만 보여준다.

```cpp
// vendor/example/sensors/AccelSensorReader.h (구조 예시, 실제 ISensors 구현의 하위 계층만 축약)
#pragma once

#include <fcntl.h>
#include <poll.h>
#include <unistd.h>
#include <cstdint>
#include <functional>

#include "example_accel_ioctl.h"

class AccelSensorReader {
  public:
    bool Open() {
        fd_ = open("/dev/example_accel", O_RDONLY);
        return fd_ >= 0;
    }

    bool SetRange(int rangeG) {
        return ioctl(fd_, EXAMPLE_ACCEL_IOCTL_SET_RANGE, &rangeG) == 0;
    }

    // onSample은 x, y, z 세 축 샘플을 받아 AIDL Event로 변환해 콜백에 전달하는 역할을 한다.
    void RunLoop(std::function<void(int16_t, int16_t, int16_t)> onSample) {
        struct pollfd pfd { .fd = fd_, .events = POLLIN };

        while (running_) {
            int ret = poll(&pfd, 1, /*timeout_ms=*/1000);
            if (ret > 0 && (pfd.revents & POLLIN)) {
                int16_t sample[3];
                if (read(fd_, sample, sizeof(sample)) == sizeof(sample)) {
                    onSample(sample[0], sample[1], sample[2]);
                }
            }
        }
    }

    void Stop() { running_ = false; }

  private:
    int fd_ = -1;
    bool running_ = true;
};
```

이 리더 클래스는 실제 서비스 프로세스 안에서 별도 스레드로 `RunLoop()`을 돌리며, 새 샘플이 들어올 때마다 이를 AIDL `ISensors` 구현체가 정의한 이벤트 콜백으로 전달한다. 이 콜백은 프레임워크가 `registerDirectChannel` 또는 폴링 방식으로 등록해 둔 소비자에게 Binder를 거쳐 전달되며, 결국 애플리케이션이 `SensorManager`로 받는 값의 최초 출처가 바로 이 `read()` 호출 한 줄이다. 즉 커널 드라이버의 `example_accel_read()`부터 앱의 `onSensorChanged()` 콜백까지는 캐릭터 디바이스 read, HAL의 폴링 스레드, Binder IPC, 프레임워크의 멀티플렉싱이라는 네 개의 계층을 순서대로 거치는 하나의 연속된 경로다.

### 카메라 드라이버가 V4L2로 카메라 HAL과 연결되는 방식

카메라는 센서보다 훨씬 복잡한 파이프라인(이미지 센서, ISP, 여러 개의 서브 블록)을 다루기 때문에, 리눅스 커널은 개별 벤더가 임의의 캐릭터 디바이스를 새로 설계하는 대신 <strong>V4L2(Video4Linux2)</strong>라는 표준화된 서브시스템과 **미디어 컨트롤러(Media Controller)** 프레임워크를 제공한다. ISP나 이미지 센서 각각은 `v4l2_subdev`로 등록되고, 이 서브디바이스들은 미디어 컨트롤러 그래프로 연결되어 데이터가 센서에서 ISP를 거쳐 최종 출력 노드까지 흐르는 경로를 명시적으로 표현한다.

```c
// drivers/media/platform/example/example_isp.c (구조 축약)
#include <media/v4l2-subdev.h>
#include <media/v4l2-device.h>

static int example_isp_s_stream(struct v4l2_subdev *sd, int enable)
{
    struct example_isp *isp = container_of(sd, struct example_isp, subdev);

    return enable ? example_isp_stream_on(isp) : example_isp_stream_off(isp);
}

static const struct v4l2_subdev_video_ops example_isp_video_ops = {
    .s_stream = example_isp_s_stream,
};

static const struct v4l2_subdev_ops example_isp_subdev_ops = {
    .video = &example_isp_video_ops,
};
```

사용자 공간에서 이 서브디바이스 그래프를 구동하는 쪽은 표준 V4L2 uAPI를 통해 통신한다. 카메라 HAL(대개 Camera Provider AIDL/HIDL 인터페이스를 구현하는 벤더 프로세스)이 실제로 프레임을 받아오기까지 발행하는 ioctl 호출 순서는 다음과 같다. 실제 벤더 카메라 스택은 대부분 비공개 소스이므로, 여기서는 커널 uAPI로 공개된 V4L2 계약만을 기준으로 순서를 보여준다.

```text
open("/dev/video0")
  -> VIDIOC_QUERYCAP        // 장치 기능(캡처/스트리밍 지원 여부) 조회
  -> VIDIOC_S_FMT           // 해상도·픽셀 포맷 설정
  -> VIDIOC_REQBUFS         // 커널이 관리할 버퍼 개수 요청 (videobuf2 큐 생성)
  -> VIDIOC_STREAMON        // 스트리밍 시작
  -> loop {
       VIDIOC_QBUF          // 빈 버퍼를 커널 큐에 반납
       VIDIOC_DQBUF         // 채워진 버퍼를 큐에서 꺼내 프레임 획득
     }
  -> VIDIOC_STREAMOFF       // 스트리밍 종료
```

이 순서에서 `VIDIOC_QBUF`/`VIDIOC_DQBUF` 쌍이 반복되는 루프는 커널과 사용자 공간이 버퍼 소유권을 명시적으로 주고받는 구조라는 점이 중요하다. 사용자 공간이 버퍼를 소유한 동안 커널은 그 메모리에 다음 프레임을 쓰지 않으며, 이 소유권 이양 규칙 덕분에 별도의 메모리 복사 없이 DMA로 채워진 버퍼를 그대로 다음 처리 단계(예: 카메라 HAL이 하는 후처리, 혹은 코덱으로의 전달)로 넘길 수 있다. 센서 HAL이 캐릭터 디바이스의 `read()`로 값을 "당겨오는" 모델이었다면, 카메라 HAL은 이렇게 버퍼 큐 소유권을 주고받는 훨씬 무거운 모델을 쓴다는 차이를 이해해 두면, 왜 카메라 스택이 센서 스택보다 구조적으로 복잡한지 납득할 수 있다.

## 흔한 오개념

<strong>"ioctl은 낡은 기법이니 가능하면 전부 sysfs로 대체해야 한다"</strong>는 절반만 맞는 생각이다. sysfs는 "파일 하나에 값 하나"라는 설계 원칙 자체가 고빈도 스트리밍 데이터를 표현하기에 구조적으로 맞지 않는다. 표준화된 IIO 서브시스템조차 저빈도 설정값은 sysfs로, 고빈도 원시 샘플은 별도의 문자 디바이스나 버퍼 큐로 분리해서 다룬다. 두 인터페이스는 대체재가 아니라 각자 다른 데이터 성격에 맞춘 상호 보완재로 보는 것이 정확하다.

<strong>"디바이스 트리에 노드를 선언하면 아무 드라이버 모델로나 등록할 수 있다"</strong>도 흔한 착각이다. I2C 버스의 자식 노드로 선언된 장치는 `i2c_driver`로, SPI 버스의 자식 노드는 `spi_driver`로 등록해야 커널의 버스 매칭 로직이 실제로 `probe()`를 호출해 준다. `platform_driver`의 `of_match_table`은 최상위 플랫폼 버스에 붙은 노드에만 적용되며, 버스 계층을 무시하고 아무 드라이버 모델에나 같은 `compatible` 문자열을 걸어두면 커널은 조용히 매칭을 실패시킬 뿐 별도의 오류를 크게 알리지 않는다.

<strong>"커널이 sysfs 노드나 ioctl 인터페이스를 노출하면 HAL이 이를 자동으로 인식한다"</strong>는 기대도 실제 동작과 다르다. HAL 구현체는 노드 경로, ioctl 매직 번호, 구조체 레이아웃을 소스 코드에 명시적으로 하드코딩하거나 설정 파일로 매핑해 두어야 한다. 커널 드라이버 쪽에서 경로나 ioctl 번호를 바꾸면, 그 변경을 인지하지 못한 HAL은 컴파일 오류 없이 `open()`이나 `ioctl()`이 조용히 실패하는 형태로 문제를 드러낸다. 이 계약은 코드로 강제되지 않으므로, 드라이버와 HAL을 같은 저장소에서 함께 리뷰하는 절차가 실무적으로 중요하다.

## 비판적 시각

커널 모듈과 캐릭터/플랫폼 드라이버, sysfs/ioctl이라는 조합은 유연하지만, 그 유연함이 곧 표준화의 부재를 뜻하기도 한다. IIO 서브시스템처럼 센서 드라이버를 위한 공용 sysfs ABI가 커널 상류(upstream)에 존재함에도 불구하고, 다수의 벤더는 배치 모드나 저전력 센서 허브 연동 같은 자사 고유 기능을 위해 표준 IIO 인터페이스를 그대로 쓰지 않고 이 장에서 다룬 것과 유사한 커스텀 ioctl 채널을 별도로 만든다. 이는 이식성을 낮추지만, 표준 인터페이스가 아직 지원하지 않는 하드웨어 기능을 빠르게 노출해야 하는 실무 압력 아래에서는 합리적인 선택이 되는 경우도 많다. "표준을 따라야 한다"는 원칙과 "출시 일정 안에 하드웨어 고유 기능을 노출해야 한다"는 압력은 실제 드라이버 설계 회의에서 자주 충돌하는 두 힘이며, 어느 한쪽이 항상 옳다고 말하기는 어렵다.

GKI와 KMI 체제도 마찬가지로 트레이드오프를 동반한다. 커널 코어와 벤더 모듈 사이의 심볼 계약을 안정화한 덕분에 보안 패치가 담긴 GKI 이미지를 벤더 모듈 재빌드 없이 배포할 수 있는 이점이 생겼지만, 이는 동시에 벤더 드라이버가 GKI가 공식적으로 노출하지 않는 내부 커널 심볼에 의존할 수 없다는 뜻이기도 하다. 과거에는 벤더가 원하는 커널 내부 함수를 자유롭게 호출해 최적화를 넣을 수 있었던 관행이, KMI 안정성 요구 아래에서는 점점 더 제약된다. 이 제약은 커널 유지보수성과 보안 패치 배포 속도라는 생태계 전체의 이익을 위한 것이지만, 개별 벤더 입장에서는 과거 대비 드라이버 설계의 자유도가 줄어드는 비용으로 체감된다.

## 다음 장에서는

[08장: 부트로더 개발](/post/android-hardware-development/bootloader-development/)에서는 이 장에서 다룬 커널과 드라이버가 메모리에 올라오기 이전 단계, 즉 부트로더가 하드웨어를 초기화하고 커널 이미지의 무결성을 검증해 제어권을 넘기는 과정을 다룬다.

## 평가 기준

- [ ] 커널 모듈의 적재·언로드 생명주기와 GKI/KMI가 벤더 모듈 빌드 방식에 어떤 제약을 거는지 설명할 수 있다.
- [ ] 캐릭터 드라이버가 `file_operations`로 사용자-커널 경계를 세우는 방식과, `alloc_chrdev_region`부터 `cdev_add`까지의 등록 절차를 설명할 수 있다.
- [ ] 플랫폼 드라이버가 디바이스 트리의 `compatible` 문자열로 매칭되는 원리와, I2C/SPI 장치가 왜 다른 드라이버 모델을 써야 하는지 구분할 수 있다.
- [ ] sysfs와 ioctl 각각이 어떤 데이터 성격(저빈도 설정 vs 고빈도 스트림)에 적합한지, 그 판단 기준을 표를 보지 않고 설명할 수 있다.
- [ ] IMU 센서 드라이버가 노출한 sysfs/ioctl/read 인터페이스를 AIDL 센서 HAL이 어떻게 열고 소비하는지, 커널부터 앱 콜백까지 전체 경로를 나열할 수 있다.
- [ ] V4L2 서브디바이스와 미디어 컨트롤러가 카메라 파이프라인을 표현하는 방식과, `VIDIOC_QBUF`/`VIDIOC_DQBUF`가 구현하는 버퍼 소유권 이양 모델을 설명할 수 있다.

## 참고 및 출처

- Android Open Source Project. "Android kernel overview." *source.android.com*, https://source.android.com/docs/core/architecture/kernel
- The Linux Kernel documentation. "Platform Devices and Drivers." *docs.kernel.org*, https://docs.kernel.org/driver-api/driver-model/platform.html
- The Linux Kernel documentation. "sysfs - _The_ filesystem for exporting kernel objects." *docs.kernel.org*, https://docs.kernel.org/filesystems/sysfs.html
- Android Open Source Project. "Sensors overview." *source.android.com*, https://source.android.com/docs/core/interaction/sensors/sensor-stack
