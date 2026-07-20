---
draft: false
image: "wordcloud.png"
title: "[Python Master] 26. 디자인 패턴 - GoF 패턴의 파이썬다운 구현"
slug: "python-design-patterns-gof-singleton-factory-observer-guide"
description: "GoF 디자인 패턴을 파이썬 맥락에서 해석하고, 언제 패턴이 유용하고 과한지 판단 기준을 제공합니다. 결합도/확장성/가독성을 균형 있게 다루는 설계 감각을 키웁니다."
tags:
  - Python
  - Implementation(구현)
  - Software-Architecture(소프트웨어아키텍처)
  - Algorithm(알고리즘)
  - Backend(백엔드)
  - Best-Practices
  - Clean-Code(클린코드)
  - Refactoring(리팩토링)
  - Testing(테스트)
  - Debugging(디버깅)
  - Logging(로깅)
  - Security(보안)
  - Performance(성능)
  - Concurrency(동시성)
  - Async(비동기)
  - OOP(객체지향)
  - Data-Structures(자료구조)
  - DevOps
  - Deployment(배포)
  - Design-Pattern(디자인패턴)
  - Web(웹)
  - Database(데이터베이스)
  - Networking(네트워킹)
  - CI-CD(Continuous Integration/Continuous Deployment)
  - Automation(자동화)
  - Documentation(문서화)
  - Git
  - Code-Quality(코드품질)
lastmod: 2026-01-17
collection_order: 26
---
# 챕터 26: 디자인 패턴 전략

## 학습 목표
- 디자인 패턴의 개념과 필요성을 이해할 수 있다
- 주요 GoF 패턴을 파이썬으로 구현할 수 있다
- 상황에 맞는 적절한 패턴을 선택할 수 있다
- 파이썬다운 패턴 구현을 할 수 있다

## 핵심 개념(이론)

### 1) 디자인 패턴의 역할과 경계
이 챕터의 핵심은 “무엇을 할 수 있나”가 아니라, **어떤 문제를 해결하고 어디까지 책임지는지**를 분명히 하는 것입니다.
경계가 흐리면 코드는 커질수록 결합이 늘어나고 수정 비용이 커집니다.

### 2) 왜 이 개념이 필요한가(실무 동기)
실무에서는 예외 상황, 성능, 협업, 테스트가 항상 문제를 만듭니다.
따라서 이 주제는 기능이 아니라 <strong>품질(신뢰성/유지보수성/보안)</strong>을 위한 기반으로 이해해야 합니다.

### 3) 트레이드오프: 간단함 vs 확장성
대부분의 선택은 “더 단순하게”와 “더 확장 가능하게” 사이에서 균형을 잡는 일입니다.
초기에는 단순함을, 장기 운영/팀 협업이 커질수록 확장성을 더 우선합니다.

### 4) 실패 모드(Failure Modes)를 먼저 생각하라
무엇이 실패하는지(입력, I/O, 동시성, 외부 시스템)를 먼저 떠올리면 설계가 안정적으로 변합니다.
이 챕터의 예제는 실패 모드를 축소해서 보여주므로, 실제 적용 시에는 더 많은 방어가 필요합니다.

### 5) 학습 포인트: 외우지 말고 “판단 기준”을 남겨라
핵심은 API를 외우는 것이 아니라, “언제 무엇을 선택할지” 판단 기준을 정리하는 것입니다.
이 기준이 쌓이면 새로운 라이브러리/도구가 나와도 빠르게 적응할 수 있습니다.

## 선택 기준(Decision Guide)
- 기본은 **가독성/명확성** 우선(최적화는 측정 이후).
- 외부 의존이 늘수록 **경계/추상화**와 **테스트**를 먼저 강화.
- 복잡도가 증가하면 “규칙을 코드로”가 아니라 “구조로” 담는 방향을 고려.

## 흔한 오해/주의점
- 도구/문법이 곧 실력이라는 오해가 있습니다. 실력은 문제를 단순화하고 구조화하는 능력입니다.
- 극단적 최적화/과설계는 학습과 유지보수를 방해할 수 있습니다.

## 요약
- 디자인 패턴는 기능이 아니라 구조/품질을 위한 기반이다.
- 트레이드오프와 실패 모드를 먼저 생각하고, 판단 기준을 남기자.

## 핵심 내용

### 패턴이 해결하는 문제와 이 장의 범위

디자인 패턴이라는 용어는 Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides가 1994년에 출간한 『Design Patterns: Elements of Reusable Object-Oriented Software』(통칭 GoF, Gang of Four)에서 체계화되었다. 이들은 자신들이 반복적으로 마주친 객체지향 설계 문제 23가지를 정리하고, 각 문제에 이름을 붙여 팀 사이의 **공통 어휘**로 만들었다. "여기에 옵저버를 쓰자"라는 한마디가 구조 전체를 설명하는 문서를 대신할 수 있다는 것이 패턴의 실질적 가치다. 원서는 C++과 Smalltalk을 배경으로 쓰였고, 그 언어들에는 1급 함수·덕 타이핑·모듈 시스템이 없었다는 점이 중요하다. 파이썬은 함수를 값으로 다루고, 클래스를 만들지 않고도 인터페이스를 만족시킬 수 있으며, 모듈 자체가 이미 싱글톤이다. 그 결과 GoF 패턴 중 상당수는 파이썬에서 원래 형태 그대로 구현할 필요가 없고, 언어 기능으로 대체되거나 훨씬 짧아진다. 이 장에서는 23개 패턴을 모두 나열하지 않고, 실무에서 자주 등장하는 6가지(싱글톤, 팩토리 메서드, 옵저버, 전략, 구조적 데코레이터, 컨텍스트 매니저 기반 패턴)를 골라 "어떤 문제를 해결하는가"와 "파이썬다운 대안이 있는가"를 함께 다룬다. 나머지 GoF 패턴의 요약과 분류는 [Refactoring.Guru의 디자인 패턴 카탈로그](https://refactoring.guru/design-patterns)에서 확인할 수 있다.

### 생성 패턴: 싱글톤과 파이썬다운 대안

<strong>싱글톤(Singleton)</strong>은 클래스의 인스턴스가 프로그램 전체에서 하나만 존재하도록 강제하는 패턴이다. 설정 객체, 커넥션 풀, 로거처럼 "여러 개 만들면 오히려 버그가 되는" 자원에 쓴다. 문제는 전통적인 구현이 `__new__`를 오버라이드해 전역 가변 상태를 클래스 뒤에 숨긴다는 점이다. 이 상태는 테스트 간에 공유되어 격리를 깨뜨리고, 멀티스레드 환경에서는 `__new__` 호출 시점에 경쟁 조건이 생길 수 있다.

```python
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, value=None):
        # __init__은 __new__와 달리 호출할 때마다 실행되므로
        # 이미 초기화된 인스턴스를 다시 덮어쓰지 않도록 방어한다.
        if not hasattr(self, "_initialized"):
            self.value = value
            self._initialized = True


a = Singleton("first")
b = Singleton("second")
print(a is b, a.value)  # True first
```

파이썬에서는 이 구조가 거의 항상 불필요하다. **모듈은 최초 import 시 한 번만 실행되고 `sys.modules`에 캐시되므로, 이미 언어 차원에서 싱글톤이다.** 클래스와 `__new__` 트릭 대신 모듈 레벨에 인스턴스를 하나 만들어 두고 그 모듈을 import해서 쓰면 같은 효과를 훨씬 적은 코드로, 그리고 테스트에서 모킹하기 쉬운 형태로 얻는다.

```python
# app_config.py라는 별도 모듈에 작성한다고 가정한다.
_settings: dict = {}


def get_setting(key, default=None):
    return _settings.get(key, default)


def set_setting(key, value):
    _settings[key] = value


# 사용하는 쪽에서는 다음처럼 import하기만 하면 된다.
# from app_config import get_setting, set_setting
# set_setting("debug", True)
```

싱글톤 클래스가 여전히 정당화되는 경우는 (1) 여러 서브클래스가 있고 다형성이 필요할 때, (2) 인스턴스 생성 시점을 지연시켜야 할 때 정도다. 단순히 "전역에서 하나만 쓰고 싶다"는 요구라면 모듈 레벨 인스턴스나 의존성 주입(생성자에 객체를 넘기는 방식)이 테스트하기 더 쉽다 — 싱글톤은 숨겨진 전역 상태이기 때문에 단위 테스트에서 상태를 초기화하기 번거롭다는 점이 실무에서 반복적으로 지적되는 단점이다.

### 팩토리 메서드: 생성 로직의 위임

<strong>팩토리 메서드(Factory Method)</strong>는 "어떤 클래스의 인스턴스를 만들지"를 호출하는 쪽 코드에서 분리해, 조건 분기가 생성 로직 안에만 모이게 하는 패턴이다. 알림 채널, 파서, 드라이버처럼 같은 인터페이스를 구현하는 구현체가 여러 개이고 런타임에 어떤 것을 쓸지 결정해야 할 때 유용하다. 이 패턴이 없으면 `if channel == "email": ... elif channel == "slack": ...` 같은 분기가 호출부마다 중복된다.

```python
from abc import ABC, abstractmethod


class Notifier(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        ...


class EmailNotifier(Notifier):
    def send(self, message: str) -> None:
        print(f"[Email] {message}")


class SlackNotifier(Notifier):
    def send(self, message: str) -> None:
        print(f"[Slack] {message}")


def create_notifier(channel: str) -> Notifier:
    """채널 이름에 따라 알맞은 Notifier를 생성하는 팩토리 함수."""
    notifiers = {"email": EmailNotifier, "slack": SlackNotifier}
    try:
        return notifiers[channel]()
    except KeyError:
        raise ValueError(f"지원하지 않는 채널: {channel}")


notifier = create_notifier("slack")
notifier.send("배포가 완료되었습니다")
```

파이썬에서 이 패턴은 클래스로 감쌀 필요 없이 함수 하나와 딕셔너리로 충분히 구현된다는 점이 원서의 예제와 다르다. `abstractmethod`로 인터페이스를 강제한 것도 필수는 아니다 — 덕 타이핑 덕분에 `send(message)`를 구현하는 어떤 객체든 통과하며, `ABC`는 "이 인터페이스를 구현하지 않으면 인스턴스화 시점에 바로 실패하게" 만드는 안전장치로만 쓰인다.

### 옵저버 패턴: 상태 변화를 구독자에게 전파

<strong>옵저버(Observer)</strong>는 하나의 객체(주체, Subject) 상태가 바뀔 때 등록된 여러 관찰자(Observer)에게 자동으로 알리는 패턴이다. GUI 이벤트, 주가 변동 알림, 발행-구독 시스템이 전형적인 예다. 핵심 가치는 주체가 관찰자의 구체 타입을 몰라도 된다는 결합도 감소에 있다.

```python
from typing import Callable, List


class StockTicker:
    """관찰 대상(Subject): 가격이 바뀌면 등록된 관찰자에게 알린다."""

    def __init__(self) -> None:
        self._observers: List[Callable[[str, float], None]] = []

    def subscribe(self, observer: Callable[[str, float], None]) -> None:
        self._observers.append(observer)

    def unsubscribe(self, observer: Callable[[str, float], None]) -> None:
        self._observers.remove(observer)

    def set_price(self, symbol: str, price: float) -> None:
        for observer in self._observers:
            observer(symbol, price)


def log_price_change(symbol: str, price: float) -> None:
    print(f"[로그] {symbol} = {price}")


def alert_if_high(symbol: str, price: float) -> None:
    if price > 100:
        print(f"[경고] {symbol} 가격 급등: {price}")


ticker = StockTicker()
ticker.subscribe(log_price_change)
ticker.subscribe(alert_if_high)
ticker.set_price("AAPL", 150.0)
```

GoF 원형은 관찰자마다 `update()` 메서드를 가진 클래스를 요구하지만, 파이썬에서는 함수가 1급 객체이므로 관찰자를 그냥 콜러블 목록으로 다뤄도 충분하다. 이 코드에는 별도의 `Observer` 추상 클래스가 없다 — `subscribe`에 넘기는 대상이 함수든, `__call__`을 구현한 객체든 상관없다. 구독자 수가 많고 스레드 간 통지가 필요하다면 표준 라이브러리보다 `blinker` 같은 신호(signal) 라이브러리를 검토할 가치가 있지만, 대부분의 실무 코드에서는 위 예제 수준의 콜백 리스트로 충분하다.

### 전략 패턴: 알고리즘을 값으로 교체하기

<strong>전략(Strategy)</strong>은 서로 바꿔 끼울 수 있는 알고리즘 계열을 캡슐화해, 호출하는 코드를 수정하지 않고도 알고리즘을 교체할 수 있게 하는 패턴이다. 정렬 기준, 가격 계산 방식, 압축 알고리즘처럼 "같은 일을 하는 여러 방법 중 하나를 골라 끼운다"는 상황에 쓴다.

```python
from typing import Callable, Iterable


def by_price(item: dict) -> float:
    return item["price"]


def by_name(item: dict) -> str:
    return item["name"]


def sort_items(items: Iterable[dict], key: Callable[[dict], object]) -> list:
    """정렬 기준(전략)을 함수로 주입받는다."""
    return sorted(items, key=key)


products = [
    {"name": "keyboard", "price": 50},
    {"name": "monitor", "price": 300},
    {"name": "mouse", "price": 20},
]

print(sort_items(products, key=by_price))
print(sort_items(products, key=by_name))
```

이 예제가 사실 보여주는 것은 파이썬 내장 `sorted(key=...)` 자체가 이미 전략 패턴을 구현하고 있다는 점이다. GoF 원형처럼 `Strategy` 추상 클래스와 `ConcreteStrategyA/B` 서브클래스를 만드는 대신, 함수를 값으로 넘기는 것만으로 같은 유연성을 얻는다. 전략이 내부 상태(예: 누적 통계, 캐시)를 가져야 한다면 함수 대신 `__call__`을 구현한 클래스나 클로저를 쓰는 편이 자연스럽다.

### 구조적 데코레이터 패턴: `@decorator` 문법과는 다른 것

**구조적 데코레이터(Decorator) 패턴**은 [13장](/post/python/python-decorators-closures-caching-logging-pattern-guide/)에서 다룬 함수 데코레이터(`@my_decorator` 문법)와 이름은 같지만 의도가 다르다. 13장의 데코레이터는 함수를 다른 함수로 감싸는 파이썬 문법 설탕이고, 여기서 말하는 구조적 데코레이터는 **객체를 같은 인터페이스를 유지한 채로 감싸서 런타임에 행동을 덧붙이는 GoF 패턴**이다. 상속으로 기능을 조합하면 조합 수만큼 서브클래스가 폭발하지만("우유 추가", "샷 추가", "우유+샷 추가" 각각을 서브클래스로 만드는 상황), 데코레이터 패턴은 감싸는 순서를 조합해 같은 효과를 낸다.

```python
from abc import ABC, abstractmethod


class Beverage(ABC):
    @abstractmethod
    def cost(self) -> float:
        ...

    @abstractmethod
    def description(self) -> str:
        ...


class Espresso(Beverage):
    def cost(self) -> float:
        return 2.0

    def description(self) -> str:
        return "에스프레소"


class BeverageDecorator(Beverage):
    """Beverage를 감싸서 같은 인터페이스를 유지하며 기능을 덧붙인다."""

    def __init__(self, beverage: Beverage) -> None:
        self._beverage = beverage

    def cost(self) -> float:
        return self._beverage.cost()

    def description(self) -> str:
        return self._beverage.description()


class WithMilk(BeverageDecorator):
    def cost(self) -> float:
        return super().cost() + 0.5

    def description(self) -> str:
        return super().description() + " + 우유"


class WithShot(BeverageDecorator):
    def cost(self) -> float:
        return super().cost() + 0.8

    def description(self) -> str:
        return super().description() + " + 샷 추가"


drink = WithShot(WithMilk(Espresso()))
print(drink.description(), drink.cost())  # 에스프레소 + 우유 + 샷 추가 3.3
```

`WithShot(WithMilk(Espresso()))`처럼 감싸는 순서를 바꾸면 조합이 늘어나며, 상속 계층을 미리 설계할 필요가 없다. 이 패턴의 본질은 "상속 대신 합성(composition)"이며, 같은 원칙이 이후 코드 품질을 다루는 장에서도 반복해 등장한다.

### 컨텍스트 매니저 기반 패턴: 파이썬이 흡수한 GoF 패턴

[15장](/post/python/python-context-managers-with-statement-resource-cleanup-guide/)에서 다룬 `with`문과 `__enter__`/`__exit__` 프로토콜은 그 자체로 파이썬이 언어 차원에서 흡수한 디자인 패턴이다. GoF의 여러 패턴(특히 트랜잭션 경계를 다루는 Command나 자원 획득·해제를 다루는 관용구)이 다른 언어에서는 `try/finally` 보일러플레이트와 클래스 계층으로 구현되지만, 파이썬은 이를 `with`문 하나로 문법화했다. 아래는 트랜잭션 커밋/롤백 경계를 컨텍스트 매니저로 표현한 예로, 성공하면 커밋하고 예외가 발생하면 자동으로 폐기한다.

```python
from contextlib import contextmanager


class InMemoryLedger:
    """트랜잭션 경계를 컨텍스트 매니저로 표현하는 간단한 원장(ledger)."""

    def __init__(self) -> None:
        self._committed: list[tuple[str, float]] = []
        self._pending: list[tuple[str, float]] = []

    def record(self, account: str, amount: float) -> None:
        self._pending.append((account, amount))

    @contextmanager
    def transaction(self):
        self._pending = []
        try:
            yield self
            self._committed.extend(self._pending)
        finally:
            self._pending = []

    @property
    def balance(self) -> float:
        return sum(amount for _, amount in self._committed)


ledger = InMemoryLedger()

with ledger.transaction() as tx:
    tx.record("checking", -100.0)
    tx.record("savings", 100.0)

print(ledger.balance)  # 0.0: 두 기록 모두 커밋됨

try:
    with ledger.transaction() as tx:
        tx.record("checking", -50.0)
        raise RuntimeError("외부 결제 실패")
except RuntimeError:
    pass

print(ledger.balance)  # 여전히 0.0: 실패한 트랜잭션은 커밋되지 않음
```

`transaction()`이 예외를 삼키지 않고 `finally`에서만 정리하기 때문에, 예외는 호출부까지 그대로 전파되면서도 `_pending`이 `_committed`에 반영되지 않는다. `contextlib.contextmanager`의 동작(제너레이터의 `yield` 이전이 `__enter__`, 이후가 `__exit__`에 대응한다)은 [Python 공식 문서](https://docs.python.org/3/library/contextlib.html)에 정의되어 있다.

### 과설계 경계: YAGNI와 패턴을 위한 패턴

패턴을 배우고 나면 모든 문제에 패턴을 적용하고 싶어지는 함정에 빠지기 쉽다. 그러나 패턴은 "반복되는 문제"에 대한 해법이지, 코드를 있어 보이게 만드는 장식이 아니다. 서브클래스가 하나뿐인 추상 팩토리, 관찰자가 하나뿐인 옵저버, 전략이 하나뿐인 전략 패턴은 대부분 불필요한 간접 계층이며 YAGNI(You Aren't Gonna Need It) 원칙 위반이다. 파이썬 커뮤니티에서 "패턴을 위한 패턴"을 경계하라는 조언이 반복되는 이유는, 정적 타입 언어에서 다형성을 얻기 위해 필요했던 클래스 계층이 파이썬에서는 함수·딕셔너리·덕 타이핑으로 훨씬 짧게 표현되기 때문이다. 클래스 3개짜리 구조를 도입하기 전에 "이걸 함수 하나와 `if`문으로 대체하면 정말 안 되는가"를 먼저 물어보는 습관이, 패턴 이름을 아는 것보다 실무에서 더 자주 쓰인다.

## 실습 프로젝트

### 프로젝트 1: 로깅 시스템 (모듈 레벨 싱글톤 + 팩토리)

여러 모듈에서 같은 로거를 공유하되, 핸들러(콘솔/파일) 생성 로직은 팩토리 함수로 분리한 예제다.

```python
import logging
from typing import Dict


def create_handler(handler_type: str) -> logging.Handler:
    """핸들러 생성을 담당하는 팩토리 함수."""
    formatter = logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s")

    if handler_type == "console":
        handler: logging.Handler = logging.StreamHandler()
    elif handler_type == "file":
        handler = logging.FileHandler("app.log", encoding="utf-8")
    else:
        raise ValueError(f"지원하지 않는 핸들러 유형: {handler_type}")

    handler.setFormatter(formatter)
    return handler


class LoggerRegistry:
    """애플리케이션 전체에서 공유하는 로거 저장소."""

    def __init__(self) -> None:
        self._loggers: Dict[str, logging.Logger] = {}

    def get_logger(self, name: str, handler_type: str = "console") -> logging.Logger:
        if name in self._loggers:
            return self._loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        logger.addHandler(create_handler(handler_type))
        self._loggers[name] = logger
        return logger


# 모듈 레벨 인스턴스: 이 모듈을 import하는 모든 코드가 같은 registry를 공유한다.
# 클래스 기반 싱글톤(__new__ 오버라이드) 없이도 단일 인스턴스가 보장된다.
registry = LoggerRegistry()


def main() -> None:
    app_logger = registry.get_logger("app")
    db_logger = registry.get_logger("db")

    app_logger.info("애플리케이션 시작")
    db_logger.info("DB 연결 완료")

    # 같은 이름으로 다시 요청하면 동일한 로거 인스턴스를 반환한다.
    assert registry.get_logger("app") is app_logger


if __name__ == "__main__":
    main()
```

### 프로젝트 2: 플러그인 아키텍처 (옵저버 + 전략)

이벤트가 발생하면(옵저버) 데이터 형식에 맞는 처리 함수를 고르는(전략) 간단한 플러그인 관리자다.

```python
from typing import Callable, Dict, List


class PluginManager:
    """옵저버 패턴으로 이벤트를 구독자에게 전달하는 플러그인 관리자."""

    def __init__(self) -> None:
        self._listeners: Dict[str, List[Callable[[dict], None]]] = {}

    def on(self, event: str, callback: Callable[[dict], None]) -> None:
        self._listeners.setdefault(event, []).append(callback)

    def emit(self, event: str, payload: dict) -> None:
        for callback in self._listeners.get(event, []):
            callback(payload)


# 전략 패턴: 데이터 형식별 처리 로직을 함수로 분리한다.
def process_as_json(payload: dict) -> None:
    print(f"[JSON 처리] {payload}")


def process_as_csv(payload: dict) -> None:
    row = ",".join(str(v) for v in payload.values())
    print(f"[CSV 처리] {row}")


STRATEGIES: Dict[str, Callable[[dict], None]] = {
    "json": process_as_json,
    "csv": process_as_csv,
}


def dispatch_by_format(payload: dict) -> None:
    """payload의 'format' 키를 보고 알맞은 전략 함수를 선택해 실행한다."""
    strategy = STRATEGIES.get(payload.get("format", "json"), process_as_json)
    strategy(payload)


def audit_log(payload: dict) -> None:
    print(f"[감사 로그] 데이터 수신: {list(payload.keys())}")


def main() -> None:
    manager = PluginManager()
    manager.on("data_received", audit_log)
    manager.on("data_received", dispatch_by_format)

    manager.emit("data_received", {"format": "csv", "name": "kim", "age": 30})
    manager.emit("data_received", {"format": "json", "name": "lee", "age": 25})


if __name__ == "__main__":
    main()
```

## 체크리스트
- [ ] 싱글톤이 해결하는 문제와, 모듈 레벨 인스턴스가 더 적합한 이유를 설명할 수 있다
- [ ] 팩토리 메서드로 객체 생성 분기를 호출부에서 분리할 수 있다
- [ ] 옵저버 패턴을 클래스 계층 없이 콜러블 목록으로 구현할 수 있다
- [ ] 전략 패턴이 `sorted(key=...)`처럼 파이썬 표준 API에 이미 녹아 있음을 안다
- [ ] 구조적 데코레이터 패턴과 13장의 함수 데코레이터 문법을 구분할 수 있다
- [ ] 컨텍스트 매니저로 트랜잭션 경계 같은 GoF 패턴을 대체할 수 있다
- [ ] 서브클래스·구현체가 하나뿐인 상황에서 패턴 도입을 보류할 수 있다(YAGNI)

## 다음 단계
디자인 패턴을 마스터했다면, [27장. 알고리즘과 자료구조](/post/python/python-advanced-algorithms-data-structures-big-o-guide/)로 넘어가 효율적인 알고리즘과 고급 자료구조를 학습합니다.
