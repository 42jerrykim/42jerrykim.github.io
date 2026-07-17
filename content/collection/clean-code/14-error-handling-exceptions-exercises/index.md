---
draft: true
collection_order: 14
slug: error-handling-exceptions-exercises
title: "[Clean Code] 14장. 오류 처리 리팩토링 실습"
date: 2026-07-17
last_modified_at: 2026-07-17
description: "정수 오류 코드로 뒤덮인 파일 처리 코드를 의미 있는 예외 계층과 Optional로 재설계하는 실습을 통해 13장에서 배운 오류 처리 원칙을 직접 적용하고, 예외 계층을 얼마나 세분화해야 하는지 실무 판단 기준으로 함께 검증한다."
categories: Clean Code
tags:
- Clean-Code(클린코드)
- Error-Handling(에러처리)
- Refactoring(리팩토링)
- Code-Quality(코드품질)
- Best-Practices
- Readability
- Maintainability
- Java
- Debugging(디버깅)
- Type-Safety
- Implementation(구현)
- Pitfalls(함정)
- Testing(테스트)
- Edge-Cases(엣지케이스)
- Tutorial(튜토리얼)
- Guide(가이드)
- Education(교육)
- Career(커리어)
- Code-Review(코드리뷰)
- Interface(인터페이스)
- OOP(객체지향)
- Design-Pattern(디자인패턴)
- Modularity
- System-Design
- Readability
---

## 이 장을 읽기 전에

이 장은 [13장: 오류 코드 대신 예외를 써라](/post/clean-code/error-handling-exceptions-best-practices/)에서 다룬 원칙(예외 계층, 컨텍스트, null 회피)을 실제 코드에 적용하는 실습이다. 13장을 먼저 읽었다는 전제로 진행한다.

| 수준 | 읽을 부분 | 핵심 목표 |
|:--:|:--|:--|
| 입문자 | 실습 1 전체 | 오류 코드를 예외 계층으로 바꾸는 절차를 익힌다 |
| 실무자 | 실습 2, "판단 기준" | 예외 계층의 세분화 정도를 실제 호출자의 필요에 맞춰 설계한다 |

## 실습 1: 오류 코드를 예외 계층으로 변환

아래 파일 처리 코드는 정수 상수로 다섯 가지 오류 상황을 구분하고, 호출자가 반환값을 확인해 분기하도록 요구한다.

```java
// 실습 대상: 정수 오류 코드
public class FileProcessor {
    public static final int SUCCESS = 0;
    public static final int FILE_NOT_FOUND = 1;
    public static final int PERMISSION_DENIED = 2;
    public static final int INVALID_FORMAT = 3;

    public int processFile(String path) {
        if (!fileExists(path)) return FILE_NOT_FOUND;
        if (!hasReadPermission(path)) return PERMISSION_DENIED;
        if (!isValidFormat(path)) return INVALID_FORMAT;
        doProcess(path);
        return SUCCESS;
    }
}

// 호출부: 매번 정수 코드를 확인하고 분기해야 한다
int result = processor.processFile(path);
if (result == FileProcessor.FILE_NOT_FOUND) {
    System.out.println("파일을 찾을 수 없습니다: " + path);
} else if (result == FileProcessor.PERMISSION_DENIED) {
    System.out.println("읽기 권한이 없습니다: " + path);
} else if (result != FileProcessor.SUCCESS) {
    System.out.println("처리 실패: " + path);
}
```

13장에서 다룬 원칙에 따라, 먼저 각 실패 상황을 의미가 드러나는 예외 타입으로 분리한다. 이때 모든 예외를 하나의 최상위 타입으로 묶어두면, 호출자가 필요에 따라 구체적인 타입으로 잡거나 상위 타입으로 뭉뚱그려 잡을 수 있다.

```java
// 리팩토링 결과: 의미가 드러나는 예외 계층
public class FileProcessingException extends RuntimeException {
    public FileProcessingException(String message) { super(message); }
}

public class FileNotFoundException extends FileProcessingException {
    public FileNotFoundException(String path) {
        super("파일을 찾을 수 없습니다: " + path);
    }
}

public class InvalidFileFormatException extends FileProcessingException {
    public InvalidFileFormatException(String path, String expectedFormat) {
        super(String.format("파일 형식이 올바르지 않습니다: %s (기대 형식: %s)", path, expectedFormat));
    }
}

public class FileProcessor {
    public void processFile(String path) {
        if (!fileExists(path)) {
            throw new FileNotFoundException(path);
        }
        if (!isValidFormat(path)) {
            throw new InvalidFileFormatException(path, "CSV");
        }
        doProcess(path);
    }
}

// 호출부: 필요한 만큼만 구체적으로, 나머지는 상위 타입으로 처리
try {
    processor.processFile(path);
} catch (FileNotFoundException e) {
    System.out.println(e.getMessage());
} catch (FileProcessingException e) {
    logger.error("파일 처리 실패", e);
}
```

이제 각 예외 클래스 이름 자체가 실패 원인을 설명하므로, 오류 코드 상수표를 따로 찾아볼 필요가 없다. 또한 새로운 실패 유형이 추가되더라도, 그 실패를 세부적으로 처리하지 않는 호출자는 `FileProcessingException` 상위 타입 하나로 계속 처리할 수 있어 하위 호환성이 유지된다.

## 실습 2: null 대신 Optional로 검색 결과 표현하기

파일 메타데이터를 조회하는 아래 메서드는 결과가 없을 때 `null`을 반환한다.

```java
// 실습 대상: null 반환
public FileMetadata findMetadata(String path) {
    return metadataStore.get(path); // 없으면 null
}

// 호출부에서 null 확인을 빠뜨리면 NullPointerException이 발생한다
FileMetadata metadata = findMetadata(path);
System.out.println(metadata.getSize()); // path가 없으면 여기서 예외 발생
```

`Optional`로 바꾸면 컴파일러가 "값이 없을 수 있다"는 사실을 호출자에게 강제로 알린다.

```java
// 리팩토링 결과: Optional로 결과 없음을 타입으로 표현
public Optional<FileMetadata> findMetadata(String path) {
    return Optional.ofNullable(metadataStore.get(path));
}

// 호출부: 처리 경로를 명시적으로 선택해야 한다
long size = findMetadata(path)
    .map(FileMetadata::getSize)
    .orElseThrow(() -> new FileNotFoundException(path));
```

## 판단 기준: 예외 계층을 얼마나 세분화할 것인가

예외 클래스를 지나치게 세분화하면(파일별 실패 원인마다 별도 클래스) 오히려 호출부의 `catch` 블록이 늘어나 13장에서 지적한 화살촉 문제가 예외 버전으로 재현될 수 있다. 실무적인 기준은 "호출자가 이 실패 유형에 대해 서로 다른 대응을 해야 하는가"이다. `FileNotFoundException`은 "사용자에게 경로를 다시 물어본다"는 별도 대응이 필요하므로 구체적인 타입으로 분리할 가치가 있지만, "권한 없음"과 "형식 오류"를 호출자가 항상 동일하게(로그만 남기고 실패 처리) 다룬다면 굳이 별도 타입으로 나눌 필요가 없다.

## 다음 장에서는

[15장: 경계 — 외부 라이브러리 사용법](/post/clean-code/api-boundaries-third-party-integration/)에서는 우리가 직접 통제할 수 없는 외부 코드의 예외를 다루는 방법을 살펴본다.

## 평가 기준

- [ ] 정수 오류 코드를 의미가 드러나는 예외 계층으로 변환할 수 있다.
- [ ] null 반환을 Optional로 바꾸고 호출부에서 명시적으로 처리할 수 있다.
- [ ] 예외 계층의 세분화 정도를 "호출자의 대응 방식이 다른가"라는 기준으로 판단할 수 있다.

## 참고 및 출처

- Martin, R. C. (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall. 7장.
- [Oracle Java Tutorials — Exceptions](https://docs.oracle.com/javase/tutorial/essential/exceptions/index.html)
