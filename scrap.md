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
