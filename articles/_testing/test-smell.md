---
title : "Software Unit Test Smells"
date: 2022-03-18
---

일반적인 소스 코드와 마찬가지로 단위 테스트 코드는 안티 패턴, 결함 및 냄새라고도 하는 잘못된 프로그래밍 관행의 영향을 받는다.

이러한 관행들은 테스트 코드를 이해하기 어렵고 유지 관리를 어렵게 만들며 소프트웨어 시스템의 품질을 저하시키는 원인이 된다.

아래의 예시들은 통해 Test Smell에 대해서 살펴 본다.

# Assertion Roulette

테스트 함수가 설명이 없는 Assertion을 여러개 가지고 있을때 발생한다. Readability, Understandability, Maintainability을 고려하지 않는 Assertion 구문은 테스트가 실패 했을때 원인을 파악하기 힘들게 만든다.

검출 : 테스트 함수 안에 설명이 없는 Assertion 구문이 있는지 확인한다.

```java
@MediumTest
public void testCloneNonBareRepoFromLocalTestServer() throws Exception {
    Clone cloneOp = new Clone(false, integrationGitServerURIFor("small-repo.early.git"), helper().newFolder());

    Repository repo = executeAndWaitFor(cloneOp);

    assertThat(repo, hasGitObject("ba1f63e4430bff267d112b1e8afc1d6294db0ccc"));

    File readmeFile = new File(repo.getWorkTree(), "README");
    assertThat(readmeFile, exists());
    assertThat(readmeFile, ofLength(12));
}
```

Original File : [GitAsyncTaskTest.java](https://github.com/rtyley/agit/blob/fc99d8eaa42940198589b032a2b9ba74d9ce3094/agit-integration-tests/src/main/java/com/madgag/agit/GitAsyncTaskTest.java#L107)

테스트 코드 안에서 `assertThat()`가 3번이나 불리고 있다. 각 구문은 다른 조건을 확인 하고 있다. 그러나 개발자는 각 구문에 대해서 부가적인 설명을 하고 있지 않기 때문에 테스트가 실패 했을때 어떤 문제가 발생한건지 파악하기 어렵다.

# Conditional Test Logic

테스트 코드는 간결하게 실행되어야 한다. 테스트 함수 안에 조건문이 있으면 테스트의 결과를 바꿀수 있다. 또한 조건문이 False로 통과하는 경우에는 문제점을 파악할 수 없는 테스트 코드가 될 수 있다. 더욱이 테스트 코드 안에 조건문은 다른 개발자 들을 이해시키는데 방해가 된다.

검출 : 테스트 코드 안에 if, switch, for, foreach, while이 포함되어 있는지 확인한다.

```java
@Test
public void testSpinner() {
    for (Map.Entry entry : sourcesMap.entrySet()) {

        String id = entry.getKey();
        Object resultObject = resultsMap.get(id);
        if (resultObject instanceof EventsModel) {
            EventsModel result = (EventsModel) resultObject;
            if (result.testSpinner.runTest) {
                System.out.println("Testing " + id + " (testSpinner)");
                //System.out.println(result);
                AnswerObject answer = new AnswerObject(entry.getValue(), "", new CookieManager(), "");
                EventsScraper scraper = new EventsScraper(RuntimeEnvironment.application, answer);
                SpinnerAdapter spinnerAdapter = scraper.spinnerAdapter();
                assertEquals(spinnerAdapter.getCount(), result.testSpinner.data.size());
                for (int i = 0; i < spinnerAdapter.getCount(); i++) {
                    assertEquals(spinnerAdapter.getItem(i), result.testSpinner.data.get(i));
                }
            }
         }
    }
}
```

Original File : [EventsScraperTest.java](https://github.com/Tyde/TuCanMobile/blob/dbee8a0a738400427bb94e5bc38a9970687ac147/app/src/test/java/com/dalthed/tucan/EventsScraperTest.java#L30)

`testSpinner()`는 여러 제어문을 포함하고 있다. 예상할 수 없는 제어문의 결과에 따라서 테스트의 성공 실패가 나뉜다. 이는 테스트 코드의 복잡하게 만들며 유지 보수를 힘들게 만든다.

# Constructor Initialization

테스트 코드 내에는 생성자가 없는것이 이상적이다. **초기화 작업은 `setUp()`에서 해야 한다.

검출 : 테스트 코드에 클래스 생성자가 있는지 확인한다.

```java
public class TagEncodingTest extends BrambleTestCase {
	private final CryptoComponent crypto;
	private final SecretKey tagKey;
	private final long streamNumber = 1234567890;

	public TagEncodingTest() {
		crypto = new CryptoComponentImpl(new TestSecureRandomProvider());
		tagKey = TestUtils.getSecretKey();
	}

	@Test
	public void testKeyAffectsTag() throws Exception {
		Set set = new HashSet<>();
		for (int i = 0; i < 100; i++) {
			byte[] tag = new byte[TAG_LENGTH];
			SecretKey tagKey = TestUtils.getSecretKey();
			crypto.encodeTag(tag, tagKey, PROTOCOL_VERSION, streamNumber);
			assertTrue(set.add(new Bytes(tag)));
		}
	}
 ...
}
```

Original File : [TagEncodingTest.java](https://code.briarproject.org/briar/briar/-/blob/0327d4f38a16b09be7cb2578d7c6f694093e65df/bramble-core/src/test/java/org/briarproject/bramble/crypto/TagEncodingTest.java#L24)

`setUp()`이 아닌 테스트 코드 내에서 클래스를 생성하고 있다.

# Default Test

By default Android Studio creates default test classes when a project is created. These classes are meant to serve as an example for developers when wring unit tests and should either be removed or renamed. Having such files in the project will cause developers to start adding test methods into these files, making the default test class a container of all test cases. This also would possibly cause problems when the classes need to be renamed in the future.

Detection: A test class is named either `ExampleUnitTest` or `ExampleInstrumentedTest`.

# Duplicate Assert

This smell occurs when a test method tests for the same condition multiple times within the same test method. If the test method needs to test the same condition using different values, a new test method should be utilized; the name of the test method should be an indication of the test being performed. Possible situations that would give rise to this smell include: (1) developers grouping multiple conditions to test a single method; (2) developers performing debugging activities; and (3) an accidental copy-paste of code.

Detection: A test method that contains more than one assertion statement with the same parameters.

# Eager Test

Occurs when a test method invokes several methods of the production object. This smell results in difficulties in test comprehension and maintenance.

Detection: A test method contains multiple calls to multiple production methods.

# Empty Test

Occurs when a test method does not contain executable statements. Such methods are possibly created for debugging purposes and then forgotten about or contains commented out code. An empty test can be considered problematic and more dangerous than not having a test case at all since JUnit will indicate that the test passes even if there are no executable statements present in the method body. As such, developers introducing behavior-breaking changes into production class, will not be notified of the alternated outcomes as JUnit will report the test as passing.

Detection: A test method that does not contain a single executable statement.

# Exception Handling

This smell occurs when a test method explicitly a passing or failing of a test method is dependent on the production method throwing an exception. Developers should utilize JUnit's exception handling to automatically pass/fail the test instead of writing custom exception handling code or throwing an exception.

Detection: A test method that contains either a throw statement or a catch clause.

# General Fixture

Occurs when a test case fixture is too general and the test methods only access part of it. A test setup/fixture method that initializes fields that are not accessed by test methods indicates that the fixture is too generalized. A drawback of it being too general is that unnecessary work is being done when a test method is run.

Detection: Not all fields instantiated within the setUp method of a test class are utilized by all test methods in the same test class.

# Ignored Test

JUnit 4 provides developers with the ability to suppress test methods from running. However, these ignored test methods result in overhead since they add unnecessary overhead with regards to compilation time, and increases code complexity and comprehension.

Detection: A test method or class that contains the @Ignore annotation.

# Lazy Test

Occurs when multiple test methods invoke the same method of the production object.

Detection: Multiple test methods calling the same production method.

# Magic Number Test

Occurs when assert statements in a test method contain numeric literals (i.e., magic numbers) as parameters. Magic numbers do not indicate the meaning/purpose of the number. Hence, they should be replaced with constants or variables, thereby providing a descriptive name for the input.

Detection: An assertion method that contains a numeric literal as an argument.

# Mystery Guest

Occurs when a test method utilizes external resources (e.g. files, database, etc.). Use of external resources in test methods will result in stability and performance issues. Developers should use mock objects in place of external resources.

Detection: A test method containing object instances of files and databases classes.

# Redundant Print

Print statements in unit tests are redundant as unit tests are executed as part of an automated process with little to no human intervention. Print statements are possibly used by developers for traceability and debugging purposes and then forgotten.

Detection: A test method that invokes either the print or println or printf or write method of the System class.

# Redundant Assertion

This smell occurs when test methods contain assertion statements that are either always true or always false. This smell is introduced by developers for debugging purposes and then forgotten.

Detection: A test method that contains an assertion statement in which the expected and actual parameters are the same.

# Resource Optimism

This smell occurs when a test method makes an optimistic assumption that the external resource (e.g., File), utilized by the test method, exists.

Detection: A test method utilizes an instance of a File class without calling the exists(), isFile() or notExists() methods of the object.

# Sensitive Equality

Occurs when the toString method is used within a test method. Test methods verify objects by invoking the default toString() method of the object and comparing the output against an specific string. Changes to the implementation of toString() might result in failure. The correct approach is to implement a custom method within the object to perform this comparison.

Detection: A test method invokes the toString() method of an object.

# Sleepy Test

Explicitly causing a thread to sleep can lead to unexpected results as the processing time for a task can differ on different devices. Developers introduce this smell when they need to pause execution of statements in a test method for a certain duration (i.e. simulate an external event) and then continuing with execution.

Detection: A test method that invokes the Thread.sleep() method.

# Unknown Test

An assertion statement is used to declare an expected boolean condition for a test method. By examining the assertion statement it is possible to understand the purpose of the test method. However, It is possible for a test method to written sans an assertion statement, in such an instance JUnit will show the test method as passing if the statements within the test method did not result in an exception, when executed. New developers to the project will find it difficult in understanding the purpose of such test methods (more so if the name of the test method is not descriptive enough). 

Detection: A test method that does not contain a single assertion statement and @Test(expected) annotation parameter.

# 참고

* [Software Unit Test Smells](https://testsmells.org/#)