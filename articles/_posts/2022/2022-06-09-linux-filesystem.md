---
title: "[Linux] File System 종류- DebugFS, SecurityFS, PipeFS, SockFS"
category: Linux
tags:
- Linux
- FileSystem
- DebugFS
- SecurityFS
- PipeFS
- SockFS
- Thread
- Sock
- Pipe
- Fork
- Mediator
- Compatibility
- Port
- VFS
- Virtual Filesystem Switch
- Virtual Filesystem

header:
  teaser: /assets/images/undefined/securityfs.png
---

리눅스에는 다양한 목적을 가지고 있는 가상 파일 시스템을 가지고 있다. 파일 시스템을 사용하든 간에 관계없이 프로그램을 작성할 땐 open, read, write, close와 같은 시스템 호출을 사용해서 이 모든 걸 처리할 수 있다. 지금은 이게 모두 당연하지만, 예전에는 그렇지 않았다. 실제 파일 시스템이 무엇이냐에 관계없이 공통된 인터페이스(open/read/write/close 등)로 접근하는 것은 매우 어려운 일이었다. 이렇듯 리눅스에서, 실제 파일시스템과 관계없이 공통된 인터페이스로 파일시스템에 접근하도록 하는 계층을 가상 파일시스템(Virtual Filesystem Switch, VFS)이라고 한다.

> 아래의 내용은 [PipeFS, SockFS, DebugFS, and SecurityFS](https://www.linux.org/threads/pipefs-sockfs-debugfs-and-securityfs.9638/)을 보고 작성한 글이다.
 
리눅스에는 다양한 목적을 가지고 있는 가상 파일 시스템을 가지고 있다. 다른 것들도 언급하겠지만 DebugFS, SecurityFS, PipeFS, SockFS는 중요한 파일 시스템이다.
 
# DebugFS

DebugFS는 디버깅을 위해서 사용되며 램 기반에 파일 시스템이다. DebugFS는 ProcFS, SysFS와 비슷한 점이 많다. 그러나 디버그 정보를 표시한다는 것이 다르다. 다른 램 기반(RAM-based)의 파일시스템처럼 DebugFS는 커널과 유저 영역 사이를 연결하는 인터페이스(kernel-user interface) 역활을 한다. DebugFS는 터미널에 `mount -t debugfs none /sys/kernel/debug`명령어를 통해서 마운트 할 수 있다.

만약에 시스템이 부팅될 때 DebugFS가 마운트하려면 `/etc/fstab`에 `debugfs /sys/kernel/debug debugfs defaults 0 0`을 추가 한다.

리눅스 커널을 수정하는 중이라면 DebugFS는 `CONFIG_DEBUG_FS`이라는 이름으로 불린다. `CONFIG_DEBUG_FS`을 활성화하면 DebugFS를 활성화할 수 있다.

DebugFS는 아래와 같은 다양한 시스템콜(system-calls)을 가지고 있다.

* debugfs_create_atomic_t() creates a debugfs file for reading/writing an atomic_t value
* debugfs_create_blob() creates a debugfs file for reading a binary-blob
* debugfs_create_bool() creates a debugfs file for reading/writing a boolean value
* debugfs_create_dir() creates a directory
* debugfs_create_file() writes a file on the filesystem
* debugfs_create_regset32() creates a debugfs file that returns register values
* debugfs_create_size_t() creates a debugfs file for reading/writing a size_t value
* debugfs_create_symlink() creates a symbolic link
* debugfs_create_u{8,16,32,64}() creates a debugfs file for reading/writing an unsigned *-bit value
* debugfs_create_u32_array() creates a debugfs file to read an unsigned 32-bit array
* debugfs_create_x{8,16,32,64}() creates a debugfs file for reading/writing an unsigned *-bit value
* debugfs_initialized() determines if debugfs is or is not registered
* debugfs_print_regs32() use seq_print to describe a set of registers
* debugfs_remove deletes() a file or directory from DebugFS
* debugfs_remove_recursive() recursively removes a directory
* debugfs_rename() renames a debugfs directory or file

# SecurityFS

SecurityFS은 커널 보안 모듈을 위한 메모리 안에 있는 가상 파일 시스템이다. 커널 보안 모듈은 보안 정책과 데이터를 가지고 있다. 유저 영역에서 SecurityFS를 바라보념 SysFS의 일부로 보인다. SecurityFS은 `/sys/kernel/security/`으로 마운트 된다. 몇몇 보안 모듈은 보안 모듈을 설정하기 위해서 `/sys/kernel/security/`에 파일을 읽고 쓴다. 리눅스 보안 모듈([LSM](https://www.kernel.org/doc/html/v4.14/admin-guide/LSM/index.html))은 가상 파일 시스템(pseudo-filesystem)에 데이터를 쓰고 읽어야 하기 때문에 SecurityFS가 이미 마운트 된 경우가 아니라면 수동으로 마운트한다.

LSM은 SecurityFS의 루트 폴더에 특정 이름으로 폴더를 만든다. 예를 들어 AppArmor는 `apparmor`란 이름으로 `/sys/kernel/security/`에 폴더를 만든다.

|![링크](/assets/images/undefined/securityfs.png)|
|:---:|
| `/sys/kernel/security/`에 생성되어 있는 `apparmor`폴더|

# PipeFS

PipeFS는 독특한 가상 파일 시스템이다. PipeFS는 유저영역 대신에 커널영역 안에 마운트 된다. 대부분의 파일시스템은 `/`아래에 생성되는데 말이다. PipeFS는 자신만의 루트를 만들면서 `pipe`에 마운트 된다. PipeFS는 하나의 슈퍼블록(superblock)을 가진다. 그리고 시스템에서 정의하는 총량을 넘어서 생성할 수 없다. `pipe()` 시스템콜을 사용하여 `filesystem/second-root`에 접근 할 수 있다. 다른 가상 파일 시스템(Virtual/Pseudo Filesystems)과는 다르게 PipeFS는 보여지지 않는다.

PipeFS의 목적에 대해서 많은 의문을 가질수 있다. 유닉스의 파이프는 PipeFS를 사용한다. `like this - ls | less`처럼 파이프가 사용될때, `pipe()`는 PipeFS에 새로운 파이프 객체를 생성한다. PipeFS가 없다면 파이프를 생성할수 없으며, 또한 스레드(Thread)나 포크(Fork)가 파이프를 이용한 통신도 불가능하다. PipeFS가 없다면 프로세스는 포크(Fork) 할 수 없고, 스레드(Thread)는 서로 통신할 수 없다. 네트워크 파이프 또한 PipeFS에 의존하여 동작한다.

# SockFS

SockFS는 소켓/포트(Socket/Port) 및 호환성 레이어(Compatibility Layer)에 대한 정보를 저장하기 위한 RAM에 위치한 가상 파일 시스템이다. SockFS는 소켓 파일 시스템(Socket FileSystem)이라고 불리기도 한다. 현재, SockFS는 호환성 계층의 역활을 하기 때문에 `write()` 시스템콜은 데이터를 소켓/포트(FTP가 21번 포트를 사용하는것처럼)에 쓴다. 여기서 중요한것은 이러한 소켓들은 TCP나 UDP 통신에 사용되며 `write()` 명령어는 하드 디스크같은 파일 시스템에서 사용하는 명령어랑 같다는 것이다. SockFS는 `write()` 시스템콜을 통해서 데이터를 쓸때 소켓과 호환할 수 있도록 변환해주기 때문에 중요하다. 따라서 `write()`는 소켓과 직접 상호작용하지 않지만 SockFS가 중재자(Mediator)역활을 하기 때문에 상호작용 할 수 있다.

> TIP : 시스템에 마운트된 모든 파일 시스템(real and virtual)을 보고 싶다면 `cat /proc/filesystems`을 사용한다.

유닉스나 리눅스는 파일 디스크립터(file descriptor)나 프로세스(process)로 모든것을 표현한다. 이제는 네트워크나 파이프가 파일 시스템을 필요로 한다는것에 대애서 깊은 생각을 할 수 있을것이다.

# 추가로 고민할 내용

Virtual Filesystem과 Pseudo Filesystem은 다른것인가?

# 참고

* [리눅스 보안 모듈 - ko.wikipedia.org](https://ko.wikipedia.org/wiki/%EB%A6%AC%EB%88%85%EC%8A%A4_%EB%B3%B4%EC%95%88_%EB%AA%A8%EB%93%88)
* [Linux Security Module Usage - www.kernel.org](https://www.kernel.org/doc/html/v4.14/admin-guide/LSM/index.html)
* [[Linux Kernel] 가상 파일시스템이란 (VFS, Virtual Filesystem Switch) - hyeyoo.com](https://hyeyoo.com/84)
* [How pipes work in Linux - unix.stackexchange.com](https://unix.stackexchange.com/questions/148401/how-pipes-work-in-linux)
* [[LinuxKernel]파일시스템, 가상 파일시스템, 슈퍼블록, 아이노드, 덴트리, 파일(FileSystem, VFS, SuperBlock, Inode, Dentry, File) - hyoje420.tistory.com](https://hyoje420.tistory.com/53)
