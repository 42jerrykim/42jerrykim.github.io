---
collection_order: 8
date: 2026-07-14
lastmod: 2026-07-14
draft: false
image: wordcloud.png
title: "[IO 09] Direct I/O"
slug: direct-io-o-direct-page-cache-bypass
description: "O_DIRECT로 페이지 캐시를 우회하는 원리, 버퍼·오프셋·길이 정렬 요구사항과 EINVAL 실패 모드, statx STATX_DIOALIGN으로 정렬 정보를 조회하는 방법, Windows FILE_FLAG_NO_BUFFERING과의 대응 관계, 캐시 우회가 유리한 워크로드 판단 기준을 다룹니다."
tags:
  - Performance(성능)
  - Optimization(최적화)
  - IO(Input/Output)
  - File-System
  - OS(운영체제)
  - Linux(리눅스)
  - Windows(윈도우)
  - Kernel
  - C
  - Memory(메모리)
  - Cache
  - Database(데이터베이스)
  - Benchmark
  - Latency
  - Throughput
  - Implementation(구현)
  - Best-Practices
  - System-Design
  - Advanced
  - Deep-Dive
  - Pitfalls(함정)
  - Edge-Cases(엣지케이스)
  - Reference(참고)
  - Guide(가이드)
  - Comparison(비교)
  - O_DIRECT
  - Page-Cache
  - Buffered-IO
  - Sector-Alignment
  - statx
  - posix_memalign
  - DMA
  - FILE_FLAG_NO_BUFFERING
  - NVMe
---

**Direct I/O**란 `O_DIRECT` 플래그로 페이지 캐시(page cache)를 우회해 애플리케이션 버퍼와 스토리지 디바이스 사이에서 데이터를 직접 주고받는 I/O 방식을 말합니다. 데이터베이스나 캐시 서버처럼 자체적으로 버퍼 관리 로직을 갖춘 애플리케이션은 커널의 페이지 캐시가 오히려 이중 캐싱(double caching)과 예측 불가능한 메모리 압박을 만드는 원인이 되는데, 이 장에서는 O_DIRECT가 페이지 캐시를 우회하는 원리와 그 대가로 떠안는 정렬 요구사항, 그리고 어떤 워크로드에서 이 트레이드오프가 실제로 이득인지를 다룹니다.

## 이 장을 읽기 전에

**전제 지식**: [Memory-mapped I/O](/post/io-optimization/memory-mapped-io-mmap-usage-pitfalls/)에서 다룬 "페이지 캐시가 파일 데이터를 메모리에 올려 두는 계층"이라는 개념과, [I/O 비용 직관](/post/io-optimization/io-cost-intuition-sync-async-copy-fundamentals/)에서 다룬 "시스템콜과 복사 횟수가 지연에 미치는 영향"을 전제로 합니다. `read()`/`write()`가 커널 버퍼를 거쳐 사용자 버퍼로 복사된다는 사실만 알면 충분합니다.

**이 장의 깊이**: 이 장은 **심화** 난이도로, O_DIRECT의 동작 원리·정렬 규칙·실패 모드를 실제 코드로 다룹니다. **다루지 않는 것**: `sendfile`/`splice`/`copy_file_range` 같은 zero-copy 기법은 [Zero-copy 기법](/post/io-optimization/zero-copy-sendfile-splice-copy-file-range/)에서, ext4/XFS/ZFS의 세부 성능 특성은 다음 장인 [파일시스템 성능 특성](/post/io-optimization/filesystem-performance-characteristics-ext4-xfs-zfs/)에서, NVMe·I/O 스케줄러 튜닝은 [블록 디바이스 최적화](/post/io-optimization/block-device-nvme-ssd-io-scheduler-optimization/)에서, WAL·fsync·저널링 전략은 [Database I/O 패턴](/post/io-optimization/database-io-wal-fsync-journaling-strategy/)에서, Windows의 비동기 완료 모델은 [IOCP와 Windows I/O](/post/io-optimization/windows-iocp-io-model-optimization/)에서 각각 다룹니다. 이 장은 그 앞단에 있는 "왜, 언제 캐시를 우회하는가"에 집중합니다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **중급자(진입)** | "O_DIRECT의 역사와 설계 배경" ~ "페이지 캐시를 우회하는 메커니즘" | O_DIRECT가 왜 만들어졌고 무엇을 우회하는지 이해 |
| **심화 실무자** | "정렬 요구사항과 실패 모드" ~ "정렬 정보를 동적으로 조회하기" | 정렬 규칙을 코드로 다루고 EINVAL을 진단·해결 |
| **전문가** | "판단 기준" ~ "비판적 시각" | 워크로드별 채택 여부를 판단하고 인터페이스의 한계를 인지 |

---

## O_DIRECT의 역사와 설계 배경

O_DIRECT는 리눅스가 발명한 개념이 아닙니다. SGI IRIX에서 먼저 도입되었고, 리눅스에는 2.4.10(2001년)에 추가되었습니다. 도입 배경은 명확히 데이터베이스 벤더, 특히 Oracle의 요구였습니다. Oracle 같은 RDBMS는 이미 자체 버퍼 캐시(SGA)로 페이지를 관리하고 있었기 때문에, 커널 페이지 캐시가 같은 데이터를 한 번 더 들고 있는 것은 메모리 낭비이자 예측하기 어려운 스와핑·회수(reclaim) 압박의 원인이었습니다. 커널 입장에서는 파일마다 "이 파일은 캐시하지 마라"는 요청을 들어주는 플래그 하나를 추가하는 것이 가장 손쉬운 해법이었습니다.

이 설계 방식은 커널 커뮤니티 내부에서도 논쟁거리였습니다. Linus Torvalds는 2002년 커널 개발자 Gerrit Huizenga에게 보낸 메일에서 O_DIRECT의 인터페이스 설계 방식 자체를 두고 "the whole interface is just stupid"([Torvalds, 2002, lkml 메일](https://static.lwn.net/2002/0516/a/lt-deranged-monkey.php3))라고 직설적으로 비판하며, `MAP_UNCACHED` 플래그를 쓴 `mmap` 기반 읽기와 `mmwrite()` 류의 쓰기 API가 더 깔끔한 대안이 될 수 있었다고 주장했습니다. 이 논쟁은 결론이 나지 않은 채로 O_DIRECT가 그대로 표준적인 인터페이스로 굳어졌고, 그 결과 지금도 파일시스템·디바이스·커널 버전에 따라 동작이 미묘하게 갈리는 인터페이스로 남아 있습니다.

## 페이지 캐시를 우회하는 메커니즘

일반적인 **Buffered I/O**에서 `read()`/`write()`는 사용자 버퍼와 디바이스 사이에 커널 페이지 캐시를 끼워 넣습니다. 읽기는 페이지 캐시에 데이터가 있으면(cache hit) 디바이스 접근 없이 캐시에서 사용자 버퍼로 복사만 하고, 없으면(cache miss) 디바이스에서 페이지 캐시로 읽어온 뒤 다시 사용자 버퍼로 복사합니다. 쓰기는 사용자 버퍼의 내용을 페이지 캐시에 반영(dirty 표시)한 뒤 즉시 반환하고, 실제 디바이스 반영은 writeback 데몬이 나중에 비동기로 처리합니다. 이 구조 덕분에 반복 접근하는 데이터는 디바이스 왕복 없이 메모리 속도로 처리되고, 순차 읽기는 readahead로 미리 채워질 수 있습니다.

`O_DIRECT`를 지정하면 이 경로에서 페이지 캐시 단계가 통째로 빠집니다([man7.org, open(2)](https://man7.org/linux/man-pages/man2/open.2.html)에 O_DIRECT의 정렬 제약과 파일시스템별 차이가 정리되어 있습니다). 커널은 사용자 버퍼를 블록 계층(block layer)에 직접 연결해 DMA로 디바이스와 주고받으며, 캐시 적중이라는 개념 자체가 사라집니다. 읽기는 매번 디바이스까지 왕복하고, 쓰기는 `write()`가 반환하는 시점에 (동기 O_DIRECT 구현이라면) 디바이스 계층까지 요청이 전달된 상태입니다. 그 결과 애플리케이션은 캐시 적중률·회수 정책·readahead 휴리스틱 같은 커널의 판단에 좌우되지 않고 자신의 접근 패턴을 그대로 디바이스에 반영할 수 있지만, 그 대신 캐시가 주던 이득(반복 읽기 가속, 쓰기 합치기)도 함께 잃습니다.

```mermaid
flowchart TB
  subgraph bufferedPath ["Buffered I/O 경로"]
    appBuf["애플리케이션 버퍼"] --> vfsBuf["VFS read()/write()"]
    vfsBuf --> pageCache["Page Cache"]
    pageCache -->|"cache miss/writeback만"| blockBuf["Block I/O 계층"]
    blockBuf --> deviceBuf["스토리지 디바이스"]
  end
  subgraph directPath ["O_DIRECT 경로"]
    appDio["정렬된 애플리케이션 버퍼"] --> vfsDio["VFS read()/write(O_DIRECT)"]
    vfsDio --> blockDio["Block I/O 계층"]
    blockDio --> deviceDio["스토리지 디바이스"]
  end
```

두 경로의 차이는 결국 "누가 캐싱을 책임지는가"의 문제입니다. Buffered I/O는 커널이 범용 정책으로 책임지고, O_DIRECT는 그 책임을 애플리케이션에 넘깁니다. 자체 버퍼 캐시가 없는 애플리케이션이 O_DIRECT만 켠다면 캐싱 자체가 사라지는 것이므로, O_DIRECT 도입은 항상 "우리 애플리케이션이 커널보다 더 잘 캐싱할 수 있는가"라는 질문과 함께 다뤄야 합니다.

## 정렬 요구사항과 실패 모드

O_DIRECT는 DMA로 사용자 버퍼와 디바이스를 직접 연결하기 때문에, 버퍼 주소·전송 길이·파일 오프셋이 특정 배수로 정렬되어 있어야 합니다. 전통적으로 리눅스는 이 정렬 단위를 파일시스템의 논리 블록 크기(흔히 512바이트 또는 4096바이트)로 요구해 왔고, 이를 무시하면 `read()`/`write()`가 `EINVAL`로 실패합니다. 아래는 흔히 저지르는 실수인, `malloc`으로 받은 버퍼를 그대로 O_DIRECT 쓰기에 넘기는 코드입니다.

```c
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>

int main(void) {
  int fd = open("/tmp/dio_test.bin", O_RDWR | O_CREAT | O_DIRECT, 0644);
  if (fd < 0) { perror("open"); return 1; }

  size_t len = 4096;
  char *buf = malloc(len);           // alignof(max_align_t) 정도만 보장 (보통 16바이트)
  memset(buf, 'A', len);

  ssize_t n = write(fd, buf, len);   // 길이·오프셋은 4096 배수처럼 보이지만 버퍼 주소가 문제
  if (n < 0) fprintf(stderr, "write 실패: %s\n", strerror(errno));

  free(buf);
  close(fd);
  return 0;
}
```

`malloc`은 반환 포인터가 `alignof(max_align_t)`(보통 16바이트) 배수임만 보장하며, 512바이트나 4096바이트 섹터 정렬은 보장하지 않습니다. 그래서 길이와 오프셋을 정확히 맞춰도 버퍼 주소 하나 때문에 `write()`가 `EINVAL`로 실패하는 경우가 흔합니다. 올바른 구현은 `posix_memalign`(또는 `aligned_alloc`)으로 정렬된 버퍼를 할당하고, 오프셋·길이도 같은 정렬 단위의 배수로 맞추는 것입니다.

```c
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>

#define DIO_ALIGN 4096   // 대상 파일시스템/디바이스의 정렬 단위. 하드코딩 대신 statx로 조회 권장

int main(void) {
  int fd = open("/tmp/dio_test.bin", O_RDWR | O_CREAT | O_DIRECT, 0644);
  if (fd < 0) { perror("open"); return 1; }

  void *buf;
  size_t len = 4096;                      // 길이도 DIO_ALIGN의 배수
  if (posix_memalign(&buf, DIO_ALIGN, len) != 0) { perror("posix_memalign"); return 1; }
  memset(buf, 'A', len);

  off_t offset = 0;                       // 오프셋도 DIO_ALIGN의 배수
  ssize_t n = pwrite(fd, buf, len, offset);
  if (n < 0) fprintf(stderr, "write 실패: %s\n", strerror(errno));
  else printf("write 성공: %zd바이트\n", n);

  free(buf);
  close(fd);
  return 0;
}
```

수정된 코드가 실제로 O_DIRECT 경로를 타는지는 `strace`로 확인할 수 있습니다. `openat`에 `O_DIRECT` 플래그가 그대로 보이고 `pwrite64`가 오류 없이 요청한 바이트 수를 반환하면 정렬 조건을 만족한 것입니다.

```text
$ strace -e trace=openat,pwrite64 ./dio_fixed
openat(AT_FDCWD, "/tmp/dio_test.bin", O_RDWR|O_CREAT|O_DIRECT, 0644) = 3
pwrite64(3, "AAAAAAAAAAAAAAAA"..., 4096, 0) = 4096
```

주의할 점은 "정렬 단위가 항상 512바이트"라는 가정이 더 이상 안전하지 않다는 것입니다. Advanced Format(4Kn) 디바이스, 일부 압축·암호화·저널링 기능이 켜진 파일시스템, NFS처럼 O_DIRECT 지원 자체가 제한적인 원격 파일시스템에서는 정렬 단위가 다르거나 O_DIRECT 자체가 무시되거나 `EINVAL`로 거부될 수 있습니다. 커널 6.0부터는 일부 경로에서 사용자 버퍼 정렬 요구가 논리 블록 크기 대신 더 완화된 DMA 정렬로도 충분해졌지만, 이는 파일시스템·커널 버전에 따른 구현 정의 동작이므로 하드코딩된 상수에 의존하지 말고 실행 시점에 조회하는 편이 안전합니다.

## 정렬 정보를 동적으로 조회하기

Linux 6.1부터는 `statx()`에 `STATX_DIOALIGN` 마스크를 넘기면 파일이 O_DIRECT를 지원하는지, 지원한다면 어떤 정렬 단위가 필요한지를 커널에 직접 물어볼 수 있습니다. 이 기능은 블록 디바이스에서는 6.1부터, ext4·f2fs·XFS 같은 일반 파일시스템의 파일에서도 6.1부터 지원됩니다([Phoronix, "Linux 6.1 Adding Support To statx() For Reporting Direct I/O Alignment Details"](https://www.phoronix.com/news/Linux-6.1-statx-DIO-Alignment)). 정렬 단위를 코드에 상수로 박아 두는 대신 이 API로 조회하면, 파일시스템·디바이스가 바뀌어도 코드를 고치지 않아도 됩니다.

```c
#include <sys/stat.h>
#include <linux/stat.h>   // struct statx, STATX_DIOALIGN (커널 헤더 6.1+ 필요)
#include <fcntl.h>
#include <stdio.h>

int main(void) {
  struct statx stx;
  if (statx(AT_FDCWD, "/tmp/dio_test.bin", 0, STATX_DIOALIGN, &stx) != 0) {
    perror("statx");
    return 1;
  }
  if (stx.stx_dio_mem_align == 0) {
    printf("이 파일에는 O_DIRECT가 지원되지 않습니다\n");
  } else {
    printf("버퍼 정렬 단위=%u바이트, 오프셋/길이 정렬 단위=%u바이트\n",
           stx.stx_dio_mem_align, stx.stx_dio_offset_align);
  }
  return 0;
}
```

`stx_dio_mem_align`이 0이면 해당 파일(또는 파일시스템)이 O_DIRECT를 지원하지 않는다는 뜻이므로, 이 값을 확인해 Buffered I/O로 폴백하는 경로를 마련해 두는 것이 이식성 있는 설계입니다. 오래된 커널을 함께 지원해야 한다면 `STATX_DIOALIGN`이 없는 환경을 대비해 컴파일 타임에 기능 존재 여부를 확인하는 코드도 함께 두어야 합니다.

## Windows의 대응 개념: FILE_FLAG_NO_BUFFERING

Windows에서 O_DIRECT에 대응하는 것은 `CreateFile`의 `FILE_FLAG_NO_BUFFERING` 플래그입니다. 접근 방식은 다르지만 요구사항의 본질은 같습니다. 파일 접근 크기(오프셋 포함)는 볼륨 섹터 크기의 배수여야 하고, 버퍼 주소는 섹터 정렬이어야 합니다. Advanced Format 디바이스는 논리 섹터(512바이트, 호환성용 에뮬레이션)와 물리 섹터(보통 4096바이트, 실제 원자적 쓰기 단위)가 다를 수 있어, `IOCTL_STORAGE_QUERY_PROPERTY`로 물리 섹터 크기를 조회해 그 값에 맞추는 것이 안전합니다([Microsoft Learn, "File Buffering"](https://learn.microsoft.com/en-us/windows/win32/fileio/file-buffering)). `VirtualAlloc`으로 할당한 메모리는 페이지 크기(x86/x64에서 4096바이트) 배수로 정렬되므로 대부분의 경우 섹터 정렬도 함께 만족합니다. Windows에서 이 플래그를 비동기 I/O·IOCP와 결합하는 구체적인 방법은 [IOCP와 Windows I/O](/post/io-optimization/windows-iocp-io-model-optimization/)에서 다룹니다.

## 벤치마크로 확인하기

O_DIRECT와 Buffered I/O의 성능 차이는 워크로드의 접근 패턴(순차/랜덤, 반복 재읽기 여부, 큐 깊이)에 따라 부호까지 뒤바뀔 수 있어 일반화된 배율을 제시하기보다 직접 측정하는 것이 안전합니다. `fio`는 `direct` 파라미터 하나로 같은 접근 패턴을 Buffered/O_DIRECT 양쪽으로 재현할 수 있어 이 비교에 적합한 도구입니다.

```ini
; fio 실행: fio dio_vs_buffered.fio (Linux 5.x/6.x, ext4 또는 XFS, NVMe SSD 기준)
; direct=0으로 바꿔 같은 조건에서 Buffered I/O와 비교
[global]
ioengine=libaio
direct=1
bs=4k
rw=randread
size=1G
runtime=30
time_based=1
filename=/data/dio_bench.img

[direct-vs-buffered]
numjobs=1
iodepth=32
```

캐시에 이미 올라와 있는 데이터를 반복 재읽기하는 워크로드(`rw=randread`를 같은 파일에 여러 번 반복)라면 Buffered I/O가 페이지 캐시 적중으로 디바이스 접근 자체를 건너뛰는 반면 O_DIRECT는 매번 디바이스까지 왕복하므로, 이런 워크로드에서는 O_DIRECT가 상당히 불리하게 나올 수 있습니다. 반대로 데이터셋이 메모리보다 훨씬 크고 매 요청이 사실상 캐시 미스인 워크로드(대용량 순차 스캔, 콜드 랜덤 읽기)라면 두 경로의 실제 디바이스 접근 횟수가 비슷해지고, O_DIRECT는 캐시 적재·회수에 드는 CPU·메모리 오버헤드를 아낄 수 있습니다. 정확한 배율은 디바이스 종류(NVMe vs SATA SSD vs HDD)와 큐 깊이, 커널 버전에 따라 크게 달라지므로 위 스켈레톤을 대상 환경에서 직접 돌려 확인하는 것을 권장합니다.

## 흔한 오개념

<strong>"O_DIRECT는 항상 더 빠르다"</strong>는 가장 널리 퍼진 오해입니다. O_DIRECT는 캐시를 "우회"할 뿐 데이터 접근을 빠르게 만드는 마법이 아니며, readahead와 캐시 재사용이라는 두 가지 강력한 가속 수단을 함께 포기합니다. 자체 캐시가 없는 애플리케이션이 반복 접근이 많은 워크로드에 O_DIRECT를 켜면 오히려 느려지는 경우가 흔합니다.

<strong>"O_DIRECT만 켜면 내구성(durability)이 보장된다"</strong>도 흔한 착각입니다. O_DIRECT는 페이지 캐시를 우회할 뿐이며, 디바이스 컨트롤러의 휘발성 쓰기 캐시까지 우회한다는 보장은 없습니다. `write()`가 반환됐다고 해서 데이터가 물리 매체에 안전하게 기록됐다는 뜻은 아니므로, 내구성이 필요하면 `O_DSYNC`나 명시적 `fsync`/`fdatasync`, 혹은 FUA(Force Unit Access) 계열의 메커니즘을 함께 써야 합니다. 이 조합은 트랜잭션 로그의 fsync 전략을 다루는 [Database I/O 패턴](/post/io-optimization/database-io-wal-fsync-journaling-strategy/)에서 더 깊이 다룹니다.

<strong>"정렬 단위는 512바이트로 고정"</strong>이라는 가정도 위험합니다. Advanced Format 4Kn 디바이스, 저널링·압축·암호화가 켜진 파일시스템, 커널 버전(6.0 전후의 완화)에 따라 요구되는 정렬 단위가 달라집니다. 상수를 하드코딩하지 말고 `STATX_DIOALIGN`(Linux) 또는 `IOCTL_STORAGE_QUERY_PROPERTY`(Windows)로 실행 시점에 조회하는 편이 안전합니다.

## 판단 기준

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 자체 버퍼 캐시를 가진 DB·스토리지 엔진 | O_DIRECT + 애플리케이션 레벨 캐시 | 커널 캐시와 애플리케이션 캐시의 이중 보관 방치 |
| 1회성 대용량 순차 스트리밍(백업, ETL, 벌크 로드) | O_DIRECT로 다른 프로세스의 캐시 오염 방지 | 매번 페이지 캐시 전체를 밀어내도록 방치 |
| 소규모 랜덤 I/O·재사용 많은 워크로드 | Buffered I/O + readahead에 의존 | O_DIRECT로 캐시 적중 이득을 스스로 포기 |
| 강한 내구성 보장 필요 | O_DIRECT + O_DSYNC/fsync/FUA 조합 | O_DIRECT만으로 내구성이 보장된다고 가정 |
| NFS·다양한 파일시스템 이식성 필요 | statx/에러 코드로 지원 여부 확인 후 폴백 | 정렬 단위·지원 여부를 하드코딩 |

## 비판적 시각: 한계와 트레이드오프

O_DIRECT는 20여 년 전 특정 벤더의 요구에서 출발한 인터페이스이고, 커널 메인테이너 스스로가 그 설계를 앞서 인용한 것처럼 강하게 비판했을 만큼 처음부터 우아함보다 실용성을 택한 기능입니다. 그 결과 파일시스템·디바이스·커널 버전마다 정렬 요구사항과 실패 모드가 미묘하게 다르고, 어떤 파일시스템은 아예 O_DIRECT를 무시하거나 `EINVAL`로 거부합니다. 이식성이 중요한 코드라면 O_DIRECT를 "있으면 쓰고 없으면 폴백"하는 경로로 설계해야지, 항상 성공한다고 가정해서는 안 됩니다.

또한 O_DIRECT를 도입한다고 캐싱 문제가 사라지는 것이 아니라, 캐싱의 책임이 커널에서 애플리케이션으로 옮겨질 뿐이라는 점도 냉정하게 봐야 합니다. 애플리케이션이 readahead·회수 정책·쓰기 합치기를 커널만큼(혹은 더 잘) 구현하지 못한다면 O_DIRECT 도입은 순손실입니다. 실제로 PostgreSQL은 오랫동안 O_DIRECT 전면 도입을 미뤄 왔고, 현재도 프로덕션 권장 기능이 아닌 디버그 전용 옵션(`debug_io_direct`)으로만 노출되어 있습니다. 성숙한 데이터베이스 엔진조차 O_DIRECT를 프로덕션 기본값으로 전환하는 데 신중을 기한다는 사실은, 이 기능이 "캐시를 끄는 스위치" 이상의 설계·검증 부담을 요구한다는 것을 보여줍니다. io_uring·POSIX AIO 같은 비동기 인터페이스와 O_DIRECT를 함께 쓸 때의 상호작용은 [io_uring 심화](/post/io-optimization/io-uring-advanced-deep-dive/)와 [POSIX AIO vs io_uring](/post/io-optimization/posix-aio-vs-io-uring-performance-comparison/)에서 별도로 다룹니다.

## 마무리

- [ ] O_DIRECT가 페이지 캐시 단계를 건너뛰고 사용자 버퍼를 블록 계층에 직접 연결하는 원리를 설명할 수 있다.
- [ ] 버퍼 주소·오프셋·길이 정렬 요구사항을 이해하고, `posix_memalign`으로 정렬된 버퍼를 할당하는 코드를 작성할 수 있다.
- [ ] `EINVAL` 실패의 원인을 진단하고 `strace`로 검증할 수 있다.
- [ ] `STATX_DIOALIGN`으로 정렬 단위를 하드코딩 없이 조회하는 방법을 안다.
- [ ] O_DIRECT가 항상 빠르지 않으며 내구성을 자동으로 보장하지 않는다는 것을 설명할 수 있다.
- [ ] 자체 버퍼 캐시 유무·접근 패턴을 기준으로 O_DIRECT 채택 여부를 판단할 수 있다.

**이전 장**: [Memory-mapped I/O](/post/io-optimization/memory-mapped-io-mmap-usage-pitfalls/)

**다음 장**에서는 O_DIRECT를 실제로 올려놓는 바닥인 파일시스템 자체의 성능 특성을 다룹니다. ext4, XFS, ZFS가 저널링·할당·정렬을 다루는 방식이 다르면 같은 O_DIRECT 코드도 파일시스템에 따라 다르게 동작할 수 있습니다.

→ [파일시스템 성능 특성](/post/io-optimization/filesystem-performance-characteristics-ext4-xfs-zfs/)
