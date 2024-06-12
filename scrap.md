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



Floyd-Steinberg 디더링 알고리즘은 이미지를 보다 적은 색상으로 변환하면서도 시각적으로 자연스럽게 보이도록 만들어주는 기법이다. 다음은 주어진 7가지 색상을 사용하여 Floyd-Steinberg 디더링을 적용하는 C++ 코드이다. 이 코드는 이미지를 7가지 색상 중 하나로 디더링하여 표현한다.

```cpp
#include <iostream>
#include <vector>
#include <cmath>

using namespace std;

struct Color {
    uint8_t r, g, b;
    uint8_t value;
};

vector<Color> palette = {
    {0, 0, 0, 0x0},        // black
    {255, 255, 255, 0x1},  // white
    {0, 255, 0, 0x2},      // green
    {0, 0, 255, 0x3},      // blue
    {255, 0, 0, 0x4},      // red
    {255, 255, 0, 0x5},    // yellow
    {255, 165, 0, 0x6}     // orange
};

// 유클리드 거리 계산 함수
double colorDistance(const Color &c1, const Color &c2) {
    return sqrt(pow(c1.r - c2.r, 2) + pow(c1.g - c2.g, 2) + pow(c1.b - c2.b, 2));
}

// 주어진 색상에 가장 가까운 팔레트 색상 찾기
Color findClosestColor(const Color &color) {
    Color closest = palette[0];
    double minDist = colorDistance(color, closest);

    for (const auto &p : palette) {
        double dist = colorDistance(color, p);
        if (dist < minDist) {
            closest = p;
            minDist = dist;
        }
    }

    return closest;
}

// Floyd-Steinberg 디더링 적용 함수
void floydSteinbergDithering(vector<vector<Color>> &image) {
    int height = image.size();
    int width = image[0].size();

    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            Color oldColor = image[y][x];
            Color newColor = findClosestColor(oldColor);
            image[y][x] = newColor;

            int errR = oldColor.r - newColor.r;
            int errG = oldColor.g - newColor.g;
            int errB = oldColor.b - newColor.b;

            if (x + 1 < width) {
                image[y][x + 1].r = clamp(image[y][x + 1].r + errR * 7 / 16);
                image[y][x + 1].g = clamp(image[y][x + 1].g + errG * 7 / 16);
                image[y][x + 1].b = clamp(image[y][x + 1].b + errB * 7 / 16);
            }
            if (x - 1 >= 0 && y + 1 < height) {
                image[y + 1][x - 1].r = clamp(image[y + 1][x - 1].r + errR * 3 / 16);
                image[y + 1][x - 1].g = clamp(image[y + 1][x - 1].g + errG * 3 / 16);
                image[y + 1][x - 1].b = clamp(image[y + 1][x - 1].b + errB * 3 / 16);
            }
            if (y + 1 < height) {
                image[y + 1][x].r = clamp(image[y + 1][x].r + errR * 5 / 16);
                image[y + 1][x].g = clamp(image[y + 1][x].g + errG * 5 / 16);
                image[y + 1][x].b = clamp(image[y + 1][x].b + errB * 5 / 16);
            }
            if (x + 1 < width && y + 1 < height) {
                image[y + 1][x + 1].r = clamp(image[y + 1][x + 1].r + errR * 1 / 16);
                image[y + 1][x + 1].g = clamp(image[y + 1][x + 1].g + errG * 1 / 16);
                image[y + 1][x + 1].b = clamp(image[y + 1][x + 1].b + errB * 1 / 16);
            }
        }
    }
}

// RGB 값 범위 제한 함수
uint8_t clamp(int value) {
    return value < 0 ? 0 : (value > 255 ? 255 : value);
}

int main() {
    // 예제 이미지 초기화 (3x3 크기의 이미지)
    vector<vector<Color>> image = {
        {{255, 0, 0}, {0, 255, 0}, {0, 0, 255}},
        {{255, 255, 0}, {255, 165, 0}, {0, 0, 0}},
        {{255, 255, 255}, {128, 128, 128}, {64, 64, 64}}
    };

    // 디더링 적용
    floydSteinbergDithering(image);

    // 결과 출력
    for (const auto &row : image) {
        for (const auto &color : row) {
            cout << "0x" << hex << (int)color.value << " ";
        }
        cout << endl;
    }

    return 0;
}
```

이 코드에서는 입력 이미지를 3x3 크기로 예시로 하여 `Color` 구조체를 사용해 각 픽셀의 RGB 값을 저장하고, Floyd-Steinberg 디더링을 적용하였다. `findClosestColor` 함수는 주어진 색상에 가장 가까운 팔레트 색상을 찾고, `floydSteinbergDithering` 함수는 디더링 알고리즘을 적용한다. 마지막으로 결과를 출력한다.

이 코드를 확장하여 더 큰 이미지 파일을 처리할 수도 있으며, 이미지 입출력 관련 라이브러리를 추가하여 실제 이미지 파일을 처리할 수 있다.




다음은 `struct PaletteColor`를 제거하고, 이미지 크기를 800x480으로 설정하여 Floyd-Steinberg 디더링을 적용하는 C++ 코드이다. 각 팔레트 색상은 개별 배열로 처리된다.

```cpp
#include <iostream>
#include <cmath>
#include <algorithm>

using namespace std;

// 팔레트 색상 정의
uint8_t palette[7][4] = {
    {0, 0, 0, 0x0},        // black
    {255, 255, 255, 0x1},  // white
    {0, 255, 0, 0x2},      // green
    {0, 0, 255, 0x3},      // blue
    {255, 0, 0, 0x4},      // red
    {255, 255, 0, 0x5},    // yellow
    {255, 165, 0, 0x6}     // orange
};

const int paletteSize = sizeof(palette) / sizeof(palette[0]);
const int width = 800;
const int height = 480;

// 유클리드 거리 계산 함수
double colorDistance(const uint8_t cell[3], const uint8_t color[3]) {
    return sqrt(pow(cell[0] - color[0], 2) + pow(cell[1] - color[1], 2) + pow(cell[2] - color[2], 2));
}

// 주어진 색상에 가장 가까운 팔레트 색상 찾기
int findClosestColor(const uint8_t cell[3]) {
    int closestIndex = 0;
    double minDist = colorDistance(cell, palette[0]);

    for (int i = 1; i < paletteSize; ++i) {
        double dist = colorDistance(cell, palette[i]);
        if (dist < minDist) {
            closestIndex = i;
            minDist = dist;
        }
    }

    return closestIndex;
}

// RGB 값 범위 제한 함수
uint8_t clamp(int value) {
    return value < 0 ? 0 : (value > 255 ? 255 : value);
}

// Floyd-Steinberg 디더링 적용 함수
void floydSteinbergDithering(uint8_t image[][3], int width, int height) {
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            uint8_t *oldColor = image[y * width + x];
            int closestColorIndex = findClosestColor(oldColor);
            uint8_t *newColor = palette[closestColorIndex];

            int errR = oldColor[0] - newColor[0];
            int errG = oldColor[1] - newColor[1];
            int errB = oldColor[2] - newColor[2];

            oldColor[0] = newColor[0];
            oldColor[1] = newColor[1];
            oldColor[2] = newColor[2];

            if (x + 1 < width) {
                image[y * width + (x + 1)][0] = clamp(image[y * width + (x + 1)][0] + errR * 7 / 16);
                image[y * width + (x + 1)][1] = clamp(image[y * width + (x + 1)][1] + errG * 7 / 16);
                image[y * width + (x + 1)][2] = clamp(image[y * width + (x + 1)][2] + errB * 7 / 16);
            }
            if (x - 1 >= 0 && y + 1 < height) {
                image[(y + 1) * width + (x - 1)][0] = clamp(image[(y + 1) * width + (x - 1)][0] + errR * 3 / 16);
                image[(y + 1) * width + (x - 1)][1] = clamp(image[(y + 1) * width + (x - 1)][1] + errG * 3 / 16);
                image[(y + 1) * width + (x - 1)][2] = clamp(image[(y + 1) * width + (x - 1)][2] + errB * 3 / 16);
            }
            if (y + 1 < height) {
                image[(y + 1) * width + x][0] = clamp(image[(y + 1) * width + x][0] + errR * 5 / 16);
                image[(y + 1) * width + x][1] = clamp(image[(y + 1) * width + x][1] + errG * 5 / 16);
                image[(y + 1) * width + x][2] = clamp(image[(y + 1) * width + x][2] + errB * 5 / 16);
            }
            if (x + 1 < width && y + 1 < height) {
                image[(y + 1) * width + (x + 1)][0] = clamp(image[(y + 1) * width + (x + 1)][0] + errR * 1 / 16);
                image[(y + 1) * width + (x + 1)][1] = clamp(image[(y + 1) * width + (x + 1)][1] + errG * 1 / 16);
                image[(y + 1) * width + (x + 1)][2] = clamp(image[(y + 1) * width + (x + 1)][2] + errB * 1 / 16);
            }
        }
    }
}

int main() {
    // 예제 이미지 초기화 (800x480 크기의 이미지)
    uint8_t image[width * height][3];

    // 임의의 이미지 데이터를 초기화 (단순히 그레이스케일 패턴으로 채운다)
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            image[y * width + x][0] = (x + y) % 256;
            image[y * width + x][1] = (x + y) % 256;
            image[y * width + x][2] = (x + y) % 256;
        }
    }

    // 디더링 적용
    floydSteinbergDithering(image, width, height);

    // 결과 출력 (간단히 첫 행만 출력)
    for (int x = 0; x < width; ++x) {
        int closestColorIndex = findClosestColor(image[x]);
        cout << "0x" << hex << (int)palette[closestColorIndex][3] << " ";
    }
    cout << endl;

    return 0;
}
```

이 코드는 `struct PaletteColor`를 제거하고, 팔레트 색상을 2차원 배열 `palette`로 정의하였다. 또한, 이미지 크기를 800x480으로 설정하고, Floyd-Steinberg 디더링 알고리즘을 적용하여 결과를 출력한다. 이미지 초기화 부분에서는 간단한 그레이스케일 패턴을 사용하여 초기값을 설정하였다.
