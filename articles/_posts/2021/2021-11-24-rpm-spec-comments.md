---
title: "RPM Spec 파일 내에서 주석과 매크로 사용시 주의 사항"
categories:
  - RPM
tags:
  - Spec
  - RPM
  - Comments
  - Macro
---

RPM을 빌드 할 때 사용하는 Spec 파일 내에서 주석과 매크로를 동시에 사용할 때 주의해야 한다.

# 예시

Spec 파일 내에서 아래의 코드처럼 작성하는 경우에는 주석을 무시하고 매크로가 동작한다.

## 샘플 코드

```bash
%define TEST disable
# %define TEST enable

echo %TEST
```

주석으로 표시된 ```# %define TEST enable```을 무시하고 ```disable```이 출력되는 것을 기대하는 예제이다.

## 결과

```rpm
enable
```

주석이 무시되고 ```enable```이 출력된 것을 확인 할 수 있다.

# 이유
Spec에서 주석은 ```#```을 맨 앞에 적어 주는 것이 맞다. 하지만 주석과 매크로를 동시에 사용하는 경우에는 매크로가 먼저 동작하기 때문에 주석을 무시하고 매크로가 동작하는 것이다. 매크로가 동작하지 않도록 ```%%```를 추가하면 주석이 의도한 대로 동작하는 것을 알 수 있다. [원문](https://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html/Packagers_Guide/chap-Packagers_Guide-Spec_File_Reference-Comments.html)에서 해당 내용을 확인 할 수 있다.