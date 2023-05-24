* http://egloos.zum.com/sweeper/v/3149089
* https://betterprogramming.pub/are-early-returns-any-good-eed4b4d03866
* http://stiner01.blogspot.com/2012/07/cs0051.html
* https://stackoverflow.com/questions/1088290/define-statements-within-a-namespace
* https://gunnarpeipman.com/cost-of-exceptions/?utm_source=csharpdigest&utm_medium=email&utm_campaign=370
* https://refactoring.guru/design-patterns/strategy/cpp/example
* https://modoocode.com/
* https://docs.microsoft.com/ko-kr/dotnet/standard/design-guidelines/choosing-between-class-and-struct
# 파일에서 문자열 검색
grep -r 검색할_문자열 파일이름

* https://m.blog.naver.com/njuhb/220983631282
* https://daringfireball.net/projects/markdown/
* https://stackoverflow.com/questions/7322503/pinvoke-how-to-free-a-mallocd-string
* https://github.com/bgk0018/refactoring-cheat-sheet
* https://www.planetgeek.ch/wp-content/uploads/2013/06/Clean-Code-V2.pdf
* http://www.cheat-sheets.org/


자건거 도색 : http://miamikustom.com/product/detail.html?product_no=21&cate_no=61&display_group=1

class Character {
public:
	void PrintItems() {
		for each (int item in _items) {
			std::cout << "item : " << item << std::endl;
		}
	}

	void PushItem(int item) {
		_items.push_back(item);
	}

private:
	std::vector<int> _items;

};

void LoadingThread(std::function<void()> callback) {
	Sleep(1000);
	callback();
}

void main() {
	Character* pChar = new Character();
	std::thread* loading;

	pChar->PushItem(1);
	pChar->PushItem(5);
	pChar->PushItem(10);

	auto callback = std::bind(&Character::PrintItems, pChar);

	callback();

	loading = new std::thread(LoadingThread, printItems);

	delete pChar;
	std::cout << "deleted pChar" << std::endl;

	loading->join();
	if (loading) delete loading;

}

출처: https://eastroot1590.tistory.com/entry/c11-stdsharedptr로-thread-safe-callback-구현하기 [글그리 블로그]


void SafePrint(std::weak_ptr<Character> w) {
	auto pChar = w.lock();
	if (pChar) {
		pChar->PrintItems();
	}
}

void main() {
	auto pChar = std::make_shared<Character>();
	std::thread* loading;

	pChar->PushItem(1);
	pChar->PushItem(5);
	pChar->PushItem(10);

	auto callback = std::bind(&SafePrint, std::weak_ptr<Character>(pChar));

	loading = new std::thread(LoadingThread, callback);

	pChar.reset();	// delete pChar

	std::cout << "deleted pChar" << std::endl;

	loading->join();
	if (loading) delete loading;

}
/home/abuild/rpmbuild/BUILD/dotnet-launcher-tv-plugin-4.0.81/plugin/src/dotnet-launcher-tv-plugin.cpp
출처: https://eastroot1590.tistory.com/entry/c11-stdsharedptr로-thread-safe-callback-구현하기 [글그리 블로그]
