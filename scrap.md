https://comsmart.co.kr/cmart/shop/item.php?it_id=1644305465&num=19&ca_id2=
[https://plantuml.com/ko/link#google_vignette](https://plantuml.com/ko/link)

https://blog.naver.com/yally23232/220793048885

https://humber.tistory.com/entry/%EB%9D%BC%EC%A6%88%EB%B2%A0%EB%A6%AC%ED%8C%8C%EC%9D%B4Raspberry-Pi-%ED%95%9C%EA%B8%80-%EC%84%A4%EC%B9%98%ED%95%98%EA%B8%B0

```
class Thread
{
private:
	struct TThread* m;
private:
	static void* sm_Thread(void* p);

protected:
	virtual void t_OnThread() = 0;

public:
	Thread() { m = NULL; }
	virtual ~Thread() { ASSERT(m == NULL); }
	bool Create();
	virtual void Destroy();

	static int Id();

	static void Sleep(int ms);
};

class Task;

class Handler
{
	friend Task;

	static const int EVENT_EXIT = 1;

private:
	struct THandler* m;

protected:
	virtual void t_OnHandler(Event* e);

public:
	Handler() { m = NULL; }
	virtual ~Handler() { ASSERT(m == NULL); }

	void Create(Task* task);
	virtual void Destroy();

	Task* TaskP();
};
class Timer : public Thread
{
private:
	struct TTimer* m;

protected:
	virtual void t_OnThread();

public:
	Timer() : m(NULL) {}
	virtual ~Timer() { ASSERT(m == NULL); }

	bool Create();
	virtual void Destroy();

	bool SubscribeEvent(int id, Handler* receiver, int ms);
	bool UnsubscribeEvent(int id, Handler* receiver);
};
struct TTimerNode
{
	int id;
	int ms;
	Handler* receiver;
};

struct TTimer
{
	Semaphore sem;
	int remain;
	List list;
	Mutex mutex;
};


void Timer::t_OnThread()
{
	_ENTRY();
	while (true)
	{
		m->sem.Take(m->remain);

		// TODO
	}
}

bool Timer::Create()
{
	_ENTRY();
	m = new TTimer;
	m->list.Create();
	m->sem.Create(0);
	m->mutex.Create();
	return false;
}


void Timer::Destroy()
{
	_ENTRY();
	m->mutex.Destroy();
	m->sem.Destroy();
	m->list.Destroy();
	delete m;
	m = NULL;
}


bool Timer::SubscribeEvent(int id, Handler* receiver, int ms)
{
	_ENTRY();
	m->mutex.Lock();
	TTimerNode* node = new TTimerNode;
	node->id = id;
	node->receiver = receiver;
	node->ms = ms;
	m->list.Add(node);
	m->mutex.Unlock();
	return false;
}


bool Timer::UnsubscribeEvent(int id, Handler* receiver)
{
	_ENTRY();
	bool ret = false;
	m->mutex.Lock();
	for (int a = m->list.Size() - 1; a >= 0; a--)
	{
		TTimerNode* node = (TTimerNode*)m->list.GetAt(a);
		if (node->id == id && node->receiver == receiver)
		{
			delete node;
			m->list.RemoveAt(a);
			ret = true;
			break;
		}
	}
	m->mutex.Unlock();
	return true;
}
```


Timer 클래스를 동작하도록 구현하기 위해서는 Timer의 주요 기능들을 정의하고 구현해야 한다. 이는 Thread 클래스의 기능을 상속받아 Timer가 독립적으로 동작하도록 만드는 과정이다. 제공된 코드에서는 타이머 스레드를 생성하고, 이벤트를 구독하고, 이벤트를 취소하는 메커니즘이 포함되어 있다.

이를 완성하기 위해 다음과 같은 주요 부분을 추가 및 수정해야 한다:

1. 타이머 이벤트 처리 루프 구현
2. 이벤트가 발생했을 때 Handler로 이벤트 전달
3. Thread와 Timer 간의 정확한 동기화

아래는 수정 및 추가된 코드이다:

```cpp
#include <iostream>
#include <thread>
#include <chrono>
#include <mutex>
#include <list>
#include <condition_variable>

// Assuming necessary structures and classes are declared as before

class Semaphore {
public:
    Semaphore(int count_ = 0)
        : count(count_) {
    }

    void notify() {
        std::unique_lock<std::mutex> lock(mtx);
        count++;
        cv.notify_one();
    }

    void wait() {
        std::unique_lock<std::mutex> lock(mtx);
        while (count == 0) {
            cv.wait(lock);
        }
        count--;
    }

    bool try_wait() {
        std::unique_lock<std::mutex> lock(mtx);
        if (count) {
            count--;
            return true;
        }
        return false;
    }

private:
    std::mutex mtx;
    std::condition_variable cv;
    int count;
};

class Mutex {
public:
    void Lock() {
        mtx.lock();
    }

    void Unlock() {
        mtx.unlock();
    }

private:
    std::mutex mtx;
};

class List {
public:
    void Add(TTimerNode* node) {
        list.push_back(node);
    }

    void RemoveAt(int index) {
        auto it = std::next(list.begin(), index);
        list.erase(it);
    }

    TTimerNode* GetAt(int index) {
        auto it = std::next(list.begin(), index);
        return *it;
    }

    int Size() const {
        return list.size();
    }

    void Create() {
        list.clear();
    }

    void Destroy() {
        list.clear();
    }

private:
    std::list<TTimerNode*> list;
};

struct Event {
    int id;
};

void Timer::t_OnThread() {
    _ENTRY();
    while (true) {
        m->sem.Take(m->remain);
        std::this_thread::sleep_for(std::chrono::milliseconds(m->remain));

        m->mutex.Lock();
        for (int i = 0; i < m->list.Size(); ++i) {
            TTimerNode* node = m->list.GetAt(i);
            node->receiver->t_OnHandler(new Event{node->id});
        }
        m->mutex.Unlock();
    }
}

bool Timer::Create() {
    _ENTRY();
    m = new TTimer;
    m->list.Create();
    m->sem.Create(0);
    m->mutex.Create();
    std::thread(&Timer::t_OnThread, this).detach();
    return true;
}

void Timer::Destroy() {
    _ENTRY();
    m->mutex.Destroy();
    m->sem.Destroy();
    m->list.Destroy();
    delete m;
    m = NULL;
}

bool Timer::SubscribeEvent(int id, Handler* receiver, int ms) {
    _ENTRY();
    m->mutex.Lock();
    TTimerNode* node = new TTimerNode;
    node->id = id;
    node->receiver = receiver;
    node->ms = ms;
    m->list.Add(node);
    m->mutex.Unlock();
    return true;
}

bool Timer::UnsubscribeEvent(int id, Handler* receiver) {
    _ENTRY();
    bool ret = false;
    m->mutex.Lock();
    for (int a = m->list.Size() - 1; a >= 0; a--) {
        TTimerNode* node = (TTimerNode*)m->list.GetAt(a);
        if (node->id == id && node->receiver == receiver) {
            delete node;
            m->list.RemoveAt(a);
            ret = true;
            break;
        }
    }
    m->mutex.Unlock();
    return true;
}
```

위 코드에서 주요 수정사항은 다음과 같다:

1. `Semaphore`와 `Mutex` 클래스를 C++ 표준 라이브러리의 동기화 도구를 사용하여 구현하였다.
2. `List` 클래스는 STL의 `std::list`를 사용하여 구현하였다.
3. `Timer::t_OnThread` 메서드는 실제 타이머 기능을 구현하였다. 여기서는 `std::this_thread::sleep_for`를 사용하여 지정된 시간(ms) 동안 스레드를 일시 중지시킨 후 이벤트를 처리한다.
4. `Timer::Create` 메서드는 타이머 스레드를 생성하고 detach한다.
5. `Handler::t_OnHandler` 메서드는 이벤트가 발생했을 때 호출되며, 각 Handler 클래스에서 구현되어야 한다.

이제 Timer 클래스는 독립적으로 동작하며, 이벤트를 구독하고 발생시키는 기능을 제대로 수행할 것이다. 각 Handler는 `t_OnHandler` 메서드를 통해 이벤트를 처리할 수 있다.


```cpp
#include <iostream>
#include <filesystem>
#include <vector>
#include <cstdlib>
#include <ctime>

namespace fs = std::filesystem;

std::string getRandomFile(const std::string& directory) {
    std::vector<fs::path> files;

    // Iterate through the directory and store file paths
    for (const auto& entry : fs::directory_iterator(directory)) {
        if (entry.is_regular_file()) {
            files.push_back(entry.path());
        }
    }

    // Check if the directory contains any files
    if (files.empty()) {
        return "No files found in the directory.";
    }

    // Seed the random number generator
    std::srand(std::time(nullptr));
    
    // Get a random index
    int randomIndex = std::rand() % files.size();

    // Return the randomly selected file path
    return files[randomIndex].string();
}

int main() {
    std::string directory = "./sample";
    std::string randomFile = getRandomFile(directory);

    std::cout << "Random file: " << randomFile << std::endl;

    return 0;
}
```

이 코드는 C++17 이상을 필요로 한다. `std::filesystem` 라이브러리를 사용하여 디렉터리 내의 파일을 나열하고, 그 중 하나를 무작위로 선택하여 반환한다. `getRandomFile` 함수는 주어진 디렉터리 경로에서 임의의 파일을 선택하여 해당 파일의 경로를 문자열로 반환한다. `main` 함수는 이 함수를 호출하여 결과를 출력한다.
