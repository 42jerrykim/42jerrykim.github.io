/**
 * 검색 페이지 JavaScript 모듈
 * 모듈화된 구조로 코드를 정리하고 성능을 최적화
 */

// ========================================
// 유틸리티 클래스
// ========================================

class Utils {
    /**
     * Debounce 함수 - 연속적인 호출을 방지
     */
    static debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    /**
     * 다크모드 감지
     */
    static isDarkMode() {
        return document.documentElement.getAttribute('data-scheme') === 'dark' || 
               document.documentElement.classList.contains('dark') || 
               document.body.classList.contains('dark') ||
               window.matchMedia('(prefers-color-scheme: dark)').matches;
    }

    /**
     * 이미지 URL 생성
     */
    // static generateImageCandidates(pageUrl) {
    //     const url = new URL(pageUrl, window.location.origin);
    //     const basePath = url.pathname.endsWith('/') ? url.pathname.slice(0, -1) : url.pathname;
        
    //     return [
    //         `${basePath}/poster.webp`,
    //         `${basePath}/poster.jpg`,
    //         `${basePath}/poster.png`,
    //         `${basePath}/image.webp`,
    //         `${basePath}/image.jpg`,
    //         `${basePath}/image.png`
    //     ];
    // }
}

// ========================================
// 이미지 처리 클래스
// ========================================

class ImageProcessor {
    constructor() {
        this.imageCache = new Map();
    }

    /**
     * Pagefind 메타데이터에서 이미지 URL 추출
     */
    extractImageFromPagefindMeta(result) {
        console.log('🔍 extractImageFromPagefindMeta 호출됨:', result);
        
        if (result.meta && result.meta.image) {
            let imageUrl = result.meta.image.trim();
            console.log('📸 원본 이미지 URL:', imageUrl);
            
            if (!imageUrl) {
                console.log('❌ 빈 이미지 URL');
                return null;
            }
            
            // 상대 경로인 경우 절대 경로로 변환
            if (imageUrl.startsWith('/')) {
                imageUrl = window.location.origin + imageUrl;
                console.log('🔄 상대 경로를 절대 경로로 변환:', imageUrl);
            } else if (!imageUrl.startsWith('http')) {
                imageUrl = window.location.origin + '/' + imageUrl.replace(/^\/+/, '');
                console.log('🔄 프로토콜 없는 경로를 절대 경로로 변환:', imageUrl);
            }
            
            console.log('✅ 최종 이미지 URL:', imageUrl);
            return imageUrl;
        }
        
        console.log('❌ 이미지 메타데이터 없음');
        return null;
    }

    /**
     * 이미지 존재 확인
     */
    async checkImageExists(imageUrl) {
        console.log('🔍 checkImageExists 호출됨:', imageUrl);
        try {
            const response = await fetch(imageUrl, { method: 'HEAD' });
            const exists = response.ok;
            console.log('🔍 이미지 존재 확인 결과:', exists, '상태 코드:', response.status);
            return exists;
        } catch (error) {
            console.log('❌ 이미지 존재 확인 실패:', error);
            return false;
        }
    }

    /**
     * 페이지에서 이미지 찾기
     */
    async findImageInPage(pageUrl) {
        if (this.imageCache.has(pageUrl)) {
            return this.imageCache.get(pageUrl);
        }
        
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 3000);
            
            const response = await fetch(pageUrl, { 
                signal: controller.signal,
                cache: 'force-cache'
            });
            clearTimeout(timeoutId);
            
            if (response.ok) {
                const html = await response.text();
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                
                const articleImg = doc.querySelector('article img, .article-content img, .content img, main img');
                if (articleImg) {
                    let src = articleImg.src || articleImg.getAttribute('src') || articleImg.getAttribute('data-src');
                    if (src && !src.includes('avatar') && !src.includes('favicon')) {
                        if (src.startsWith('/')) {
                            src = window.location.origin + src;
                        }
                        this.imageCache.set(pageUrl, src);
                        return src;
                    }
                }
            }
            
            this.imageCache.set(pageUrl, null);
            return null;
        } catch (error) {
            console.warn('이미지 검색 실패:', pageUrl, error.message);
            this.imageCache.set(pageUrl, null);
            return null;
        }
    }

    /**
     * 결과에 이미지 로딩
     */
    async loadImageForResult(imageDiv, pageUrl, metaImage) {
        console.log('🖼️ loadImageForResult 호출됨:', { pageUrl, metaImage });
        
        try {
            let imageUrl = null;
            
            // 1. Pagefind 메타데이터 이미지 우선 확인
            if (metaImage) {
                console.log('📸 메타데이터 이미지 사용:', metaImage);
                imageUrl = metaImage.startsWith('http') ? metaImage : 
                          metaImage.startsWith('/') ? window.location.origin + metaImage : metaImage;
                
                console.log('🔗 변환된 이미지 URL:', imageUrl);
                
                if (await this.checkImageExists(imageUrl)) {
                    console.log('✅ 메타데이터 이미지 존재 확인됨');
                    this.loadImageSuccess(imageDiv, imageUrl);
                    return;
                } else {
                    console.log('❌ 메타데이터 이미지 존재하지 않음');
                }
            } else {
                console.log('❌ 메타데이터 이미지 없음');
            }
            
            if (imageUrl) {
                this.loadImageSuccess(imageDiv, imageUrl);
            } else {
                console.log('❌ 이미지 URL 없음, 실패 처리');
                this.loadImageFailed(imageDiv);
            }
        } catch (error) {
            console.warn('이미지 로딩 실패:', pageUrl, error);
            this.loadImageFailed(imageDiv);
        }
    }

    /**
     * 이미지 로딩 성공
     */
    loadImageSuccess(imageDiv, imageUrl) {
        console.log('✅ loadImageSuccess 호출됨:', imageUrl);
        console.log('🖼️ imageDiv 요소:', imageDiv);
        console.log('🖼️ imageDiv 현재 클래스:', imageDiv.className);
        console.log('🖼️ imageDiv 현재 HTML:', imageDiv.innerHTML);
        
        imageDiv.className = 'search-result-image';
        
        const img = document.createElement('img');
        img.alt = '검색 결과 이미지';
        
        console.log('🖼️ 생성된 img 요소:', img);
        
        // 이미지 로딩 타임아웃 설정 (10초)
        const timeoutId = setTimeout(() => {
            console.log('⏰ 이미지 로딩 타임아웃:', imageUrl);
            this.loadImageFailed(imageDiv);
        }, 10000);
        
        // onload/onerror 이벤트 먼저 설정
        img.onload = () => {
            console.log('🖼️ 이미지 로드 성공:', imageUrl);
            console.log('🖼️ DOM 업데이트 시작');
            clearTimeout(timeoutId);
            imageDiv.innerHTML = '';
            imageDiv.appendChild(img);
            console.log('🖼️ 이미지 요소가 DOM에 추가됨');
            console.log('🖼️ imageDiv 최종 HTML:', imageDiv.innerHTML);
        };
        
        img.onerror = () => {
            console.log('❌ 이미지 로드 실패:', imageUrl);
            clearTimeout(timeoutId);
            this.loadImageFailed(imageDiv);
        };
        
        // 마지막에 src 설정 (이벤트 설정 후)
        console.log('🖼️ img.src 설정 시작:', imageUrl);
        img.src = imageUrl;
        console.log('🖼️ img.src 설정 완료:', img.src);
        
        // src 설정 후 즉시 캐시된 이미지인지 확인
        setTimeout(() => {
            if (img.complete) {
                console.log('🖼️ 이미지가 즉시 로딩됨 (캐시됨), 처리 중');
                clearTimeout(timeoutId);
                if (img.naturalWidth > 0 && img.naturalHeight > 0) {
                    console.log('🖼️ 캐시된 이미지 로드 성공:', img.naturalWidth, 'x', img.naturalHeight);
                    imageDiv.innerHTML = '';
                    imageDiv.appendChild(img);
                    console.log('🖼️ 캐시된 이미지 DOM에 추가 완료');
                } else {
                    console.log('❌ 캐시된 이미지 크기 정보 없음, 일반 로딩 계속');
                    const newSrc = img.src + '?t=' + Date.now();
                    console.log('🔄 이미지 강제 재로딩 시도:', newSrc);
                    img.src = newSrc;
                }
            } else {
                console.log('🖼️ 이미지 로딩 중, 이벤트 대기');
            }
        }, 10);
    }

    /**
     * 이미지 로딩 실패
     */
    loadImageFailed(imageDiv) {
        console.log('❌ loadImageFailed 호출됨');
        console.log('🖼️ imageDiv 요소:', imageDiv);
        console.log('🖼️ imageDiv 변경 전 클래스:', imageDiv.className);
        console.log('🖼️ imageDiv 변경 전 HTML:', imageDiv.innerHTML);
        
        imageDiv.className = 'search-result-image no-image';
        imageDiv.innerHTML = '<div>이미지 없음</div>';
        
        console.log('🖼️ imageDiv 최종 클래스:', imageDiv.className);
        console.log('🖼️ imageDiv 최종 HTML:', imageDiv.innerHTML);
    }
}

// ========================================
// 검색 결과 렌더링 클래스
// ========================================

class SearchResultRenderer {
    constructor(imageProcessor) {
        this.imageProcessor = imageProcessor;
    }

    /**
     * 커스텀 검색 결과 생성
     */
    createCustomSearchResult(result) {
        const resultElement = document.createElement('div');
        resultElement.className = 'search-result-item';
        
        // 이미지 영역 (고정 크기)
        const imageDiv = document.createElement('div');
        imageDiv.className = 'search-result-image loading';
        imageDiv.href = result.url;
        imageDiv.innerHTML = '<div>이미지 로딩 중...</div>';
        
        // 컨텐츠 영역
        const contentDiv = document.createElement('div');
        contentDiv.className = 'search-result-content';
        
        // 제목
        const titleLink = document.createElement('a');
        titleLink.className = 'search-result-title';
        titleLink.href = result.url;
        titleLink.textContent = result.meta?.title || '제목 없음';
        
        // 요약
        const excerptDiv = document.createElement('div');
        excerptDiv.className = 'search-result-excerpt';
        excerptDiv.innerHTML = result.excerpt || '';
        
        // 메타 정보
        const metaDiv = document.createElement('div');
        metaDiv.className = 'search-result-meta';
        metaDiv.textContent = new URL(result.url).pathname;
        
        // DOM 요소들을 올바른 순서로 추가
        contentDiv.appendChild(titleLink);
        contentDiv.appendChild(excerptDiv);
        
        // 소제목들 (sub-results) 처리
        if (result.sub_results && result.sub_results.length > 0) {
            result.sub_results.forEach(subResult => {
                const subDiv = document.createElement('div');
                subDiv.className = 'search-result-sub';
                
                const subTitleLink = document.createElement('a');
                subTitleLink.className = 'search-result-sub-title';
                subTitleLink.href = subResult.url;
                subTitleLink.textContent = subResult.title || '소제목';
                
                const subExcerptDiv = document.createElement('div');
                subExcerptDiv.className = 'search-result-sub-excerpt';
                subExcerptDiv.innerHTML = subResult.excerpt || '';
                
                subDiv.appendChild(subTitleLink);
                if (subResult.excerpt) {
                    subDiv.appendChild(subExcerptDiv);
                }
                
                contentDiv.appendChild(subDiv);
            });
        }
        
        // 태그들 처리
        if (result.meta?.tags && result.meta.tags.length > 0) {
            const tagsDiv = document.createElement('div');
            tagsDiv.className = 'search-result-tags';
            
            result.meta.tags.forEach(tag => {
                const tagSpan = document.createElement('span');
                tagSpan.className = 'search-result-tag';
                tagSpan.textContent = tag;
                tagsDiv.appendChild(tagSpan);
            });
            
            contentDiv.appendChild(tagsDiv);
        }
        
        contentDiv.appendChild(metaDiv);
        
        resultElement.appendChild(imageDiv);
        resultElement.appendChild(contentDiv);
        
        // 이미지 로딩 시작
        console.log('🖼️ loadImageForResult 호출 준비:', {
            resultUrl: result.url,
            metaImage: result.meta?.image,
            imageDiv: !!imageDiv
        });
        this.imageProcessor.loadImageForResult(imageDiv, result.url, result.meta?.image);
        
        return resultElement;
    }
}

// ========================================
// 검색 관리 클래스
// ========================================

class SearchManager {
    constructor() {
        this.pagefindInstance = null;
        this.imageProcessor = new ImageProcessor();
        this.resultRenderer = new SearchResultRenderer(this.imageProcessor);
        
        // 성능 최적화용 변수들
        this.convertPagefindResultsTimeout = null;
        this.lastProcessedResultsCount = 0;
        this.isConverting = false;
        this.processedUrls = new Set();
        
        // 중복 검색 방지를 위한 변수
        this.currentSearchTerm = '';
        this.isSearching = false;
        
        // debounced 버전의 convertPagefindResults 생성
        this.debouncedConvertResults = Utils.debounce(this.convertPagefindResults.bind(this), 300);
        
        this.init();
    }

    /**
     * 초기화
     */
    init() {
        this.initPagefindUI();
        this.initEventListeners();
        this.initURLParams();
    }

    /**
     * PagefindUI 초기화
     */
    initPagefindUI() {
        this.pagefindInstance = new PagefindUI({ 
            element: "#pagefind-search",
            showSubResults: true,
            showEmptyFilters: true,
            resetStyles: false,
            autofocus: false,
            processResult: (result) => {
                // 작성자 정보 정리
                if (result.meta?.author === "42jerrykim") {
                    delete result.meta.author;
                }
                
                // 제목 정리
                if (result.meta?.title) {
                    result.meta.title = result.meta.title.trim();
                }
                
                // 이미지 메타데이터 처리
                if (result.meta?.image) {
                    if (result.meta.image.startsWith('/')) {
                        result.meta.image = window.location.origin + result.meta.image;
                    }
                }
                
                return result;
            },
            translations: {
                placeholder: "검색어를 입력하세요...",
                clear_search: "검색 지우기",
                load_more: "더 보기",
                search_label: "사이트 검색",
                filters_label: "필터",
                zero_results: "검색 결과가 없습니다: [SEARCH_TERM]",
                many_results: "[COUNT]개의 결과가 있습니다: [SEARCH_TERM]",
                one_result: "1개의 결과가 있습니다: [SEARCH_TERM]",
                alt_search: "검색: [SEARCH_TERM]",
                search_suggestion: "검색어를 입력하세요",
                searching: "검색 중..."
            }
        });
    }

    /**
     * 이벤트 리스너 초기화
     */
    initEventListeners() {
        // Pagefind 결과 감지 및 커스텀 결과로 변환
        const observer = new MutationObserver((mutations) => {
            let shouldUpdate = false;
            
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList') {
                    const addedNodes = Array.from(mutation.addedNodes);
                    const hasRelevantChanges = addedNodes.some(node => {
                        if (node.nodeType === Node.ELEMENT_NODE) {
                            return node.classList.contains('pagefind-ui__result') ||
                                   node.classList.contains('pagefind-ui__message') ||
                                   node.classList.contains('pagefind-ui__button') ||
                                   node.querySelector('.pagefind-ui__result') ||
                                   node.querySelector('.pagefind-ui__message') ||
                                   node.querySelector('.pagefind-ui__button');
                        }
                        return false;
                    });
                    
                    if (hasRelevantChanges) {
                        shouldUpdate = true;
                    }
                }
            });
            
            if (shouldUpdate) {
                console.log("관련 변경사항 감지 - Pagefind 결과 업데이트");
                this.debouncedConvertResults();
            }
        });
        
        // Pagefind 컨테이너 관찰
        const pagefindContainer = document.getElementById('pagefind-search');
        if (pagefindContainer) {
            observer.observe(pagefindContainer, { childList: true, subtree: true });
        }
        
        // 커스텀 검색 입력과 PagefindUI 연결
        const customInput = document.getElementById('pagefind-search-input');
        customInput.addEventListener('input', () => this.performSearch());
        customInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.performSearch();
            }
        });
    }

    /**
     * URL 파라미터 초기화
     */
    initURLParams() {
        const urlParams = new URLSearchParams(window.location.search);
        const searchQuery = urlParams.get('keyword') || urlParams.get('q') || urlParams.get('search');
        
        if (searchQuery) {
            const customInput = document.getElementById('pagefind-search-input');
            customInput.value = searchQuery;
            setTimeout(() => this.performSearch(), 500);
        }
    }

    /**
     * 검색 실행
     */
    performSearch() {
        const searchTerm = document.getElementById('pagefind-search-input').value.trim();
        
        if (!searchTerm) {
            this.hideSearchResults();
            return;
        }
        
        // 동일한 검색어로 이미 검색 중인 경우 중복 실행 방지
        if (this.isSearching && this.currentSearchTerm === searchTerm) {
            console.log('동일한 검색어로 이미 검색 중, 건너뜀:', searchTerm);
            return;
        }
        
        // 동일한 검색어인데 이미 결과가 있는 경우 스킵
        const customResultsContainer = document.getElementById('custom-search-results');
        if (this.currentSearchTerm === searchTerm && customResultsContainer.children.length > 0) {
            console.log('동일한 검색어의 결과가 이미 표시됨, 건너뜀:', searchTerm);
            return;
        }
        
        // 검색 시작
        this.isSearching = true;
        
        // 새로운 검색어인 경우에만 상태 초기화
        if (this.currentSearchTerm !== searchTerm) {
            console.log('새로운 검색어 감지, 상태 초기화:', this.currentSearchTerm, '->', searchTerm);
            this.currentSearchTerm = searchTerm;
            this.processedUrls.clear();
            this.lastProcessedResultsCount = 0;
            this.isConverting = false;
            
            // 기존 결과 컨테이너 초기화 (새로운 검색어인 경우에만)
            customResultsContainer.innerHTML = '';
        } else {
            console.log('동일한 검색어 재실행, 초기화 생략:', searchTerm);
        }
        
        console.log(`새 검색 시작: "${searchTerm}"`);
            
        // 검색 결과 제목 업데이트
        this.updateSearchResultTitle(searchTerm);
        
        // Pagefind 검색 실행
        const pagefindInput = document.querySelector('.pagefind-ui__search-input');
        if (pagefindInput) {
            pagefindInput.value = searchTerm;
            pagefindInput.dispatchEvent(new Event('input'));
        }
        
        // 검색 완료 표시 (약간의 지연 후)
        // setTimeout(() => {
            this.isSearching = false;
        // }, 1000);
    }

    /**
     * 검색 결과 제목 업데이트
     */
    updateSearchResultTitle(searchTerm) {
        const resultTitle = document.querySelector('.search-result--title');
        if (searchTerm) {
            resultTitle.textContent = `"${searchTerm}"에 대한 검색 결과`;
            resultTitle.classList.add('show');
        } else {
            resultTitle.classList.remove('show');
        }
    }

    /**
     * 검색 결과 숨기기
     */
    hideSearchResults() {
        const resultTitle = document.querySelector('.search-result--title');
        resultTitle.classList.remove('show');
        const customResultsContainer = document.getElementById('custom-search-results');
        customResultsContainer.innerHTML = '';
        
        // 상태 초기화
        this.processedUrls.clear();
        this.lastProcessedResultsCount = 0;
        this.isConverting = false;
    }

    /**
     * Pagefind 결과를 커스텀 결과로 변환 (최적화된 버전)
     */
    async convertPagefindResults() {
        // 중복 실행 방지
        if (this.isConverting) {
            console.log('convertPagefindResults 이미 실행 중, 건너뜀');
            return;
        }
        
        this.isConverting = true;
        
        try {
            const customResultsContainer = document.getElementById('custom-search-results');
            console.log('convertPagefindResults 실행 시작');
            
            // Pagefind 결과 가져오기
            const pagefindResults = document.querySelectorAll('#pagefind-search .pagefind-ui__result');
            
            // 결과 개수가 이전과 같으면 스킵 (추가 최적화)
            if (pagefindResults.length === this.lastProcessedResultsCount && pagefindResults.length > 0) {
                console.log('결과 개수 동일, 변환 건너뜀');
                this.isConverting = false;
                return;
            }
            
            if (pagefindResults.length === 0) {
                // 메시지 처리 (검색 결과 없음 등)
                const message = document.querySelector('#pagefind-search .pagefind-ui__message');
                if (message) {
                    customResultsContainer.innerHTML = '';
                    const customMessage = message.cloneNode(true);
                    customResultsContainer.appendChild(customMessage);
                }
                this.lastProcessedResultsCount = 0;
                this.processedUrls.clear();
                this.isConverting = false;
                return;
            }
            
            console.log(`Pagefind 결과 ${pagefindResults.length}개 처리 시작`);
            
            // 새로운 검색인 경우 컨테이너 초기화
            if (pagefindResults.length > 0 && customResultsContainer.children.length === 0) {
                customResultsContainer.innerHTML = '';
            }
            
            // 새로운 결과만 추가하는 방식으로 최적화
            let addedCount = 0;
            
            // 각 결과를 커스텀 형식으로 변환
            for (const pagefindResult of pagefindResults) {
                try {
                    // Pagefind 결과에서 데이터 추출
                    const titleElement = pagefindResult.querySelector('.pagefind-ui__result-link');
                    const excerptElement = pagefindResult.querySelector('.pagefind-ui__result-excerpt');
                    const subResultElements = pagefindResult.querySelectorAll('.pagefind-ui__result-nested');
                    const tagElements = pagefindResult.querySelectorAll('.pagefind-ui__result-tag');
                    
                    if (!titleElement) continue;
                    
                    const resultUrl = titleElement.href;
                    
                    // 이미 처리된 URL인지 확인 (중복 방지)
                    if (this.processedUrls.has(resultUrl)) {
                        console.log('중복 URL 스킵:', resultUrl);
                        continue;
                    }
                    
                    console.log('새 결과 처리:', resultUrl);
                    
                    // 소제목들 추출
                    const subResults = [];
                    subResultElements.forEach(subElement => {
                        const subTitleEl = subElement.querySelector('.pagefind-ui__result-link');
                        const subExcerptEl = subElement.querySelector('.pagefind-ui__result-excerpt');
                        
                        if (subTitleEl) {
                            subResults.push({
                                title: subTitleEl.textContent.trim(),
                                url: subTitleEl.href,
                                excerpt: subExcerptEl ? subExcerptEl.innerHTML : ''
                            });
                        }
                    });
                    
                    // 태그들 추출
                    const tags = [];
                    tagElements.forEach(tagEl => {
                        const tagText = tagEl.textContent.trim();
                        if (tagText) {
                            tags.push(tagText);
                        }
                    });
                    
                    // Pagefind 결과에서 이미지 정보 추출 (여러 방법 시도)
                    let pagefindImage = null;
                    
                    // 방법 1: Pagefind가 렌더링한 <img> 태그에서 직접 추출
                    const pagefindImgElement = pagefindResult.querySelector('img.pagefind-ui__result-image');
                    if (pagefindImgElement && pagefindImgElement.src) {
                        pagefindImage = pagefindImgElement.src;
                        console.log('📸 방법 1 - <img> 태그에서 추출된 이미지 URL:', pagefindImage);
                    }
                    
                    // 방법 2: data-pagefind-meta="image" 요소에서 추출 (fallback)
                    if (!pagefindImage) {
                        const imageMetaElement = pagefindResult.querySelector('[data-pagefind-meta="image"]');
                        if (imageMetaElement) {
                            const imageText = imageMetaElement.textContent.trim();
                            if (imageText) {
                                pagefindImage = this.imageProcessor.extractImageFromPagefindMeta({
                                    meta: { image: imageText }
                                });
                                console.log('📸 방법 2 - data-pagefind-meta에서 추출된 이미지 URL:', pagefindImage);
                            }
                        }
                    }
                    
                    // 방법 3: pagefind-image-hidden 클래스에서 추출 (fallback)
                    if (!pagefindImage) {
                        const hiddenImageElement = pagefindResult.querySelector('.pagefind-image-hidden');
                        if (hiddenImageElement) {
                            const imageText = hiddenImageElement.textContent.trim();
                            if (imageText) {
                                pagefindImage = this.imageProcessor.extractImageFromPagefindMeta({
                                    meta: { image: imageText }
                                });
                                console.log('📸 방법 3 - pagefind-image-hidden에서 추출된 이미지 URL:', pagefindImage);
                            }
                        }
                    }
                    
                    // 방법 4: 모든 data-pagefind-meta 속성을 가진 요소 확인 (fallback)
                    if (!pagefindImage) {
                        const allMetaElements = pagefindResult.querySelectorAll('[data-pagefind-meta]');
                        allMetaElements.forEach(el => {
                            const key = el.getAttribute('data-pagefind-meta');
                            if (key === 'image' && !pagefindImage) {
                                const imageText = el.textContent.trim();
                                if (imageText) {
                                    pagefindImage = this.imageProcessor.extractImageFromPagefindMeta({
                                        meta: { image: imageText }
                                    });
                                    console.log('📸 방법 4 - 메타데이터에서 추출된 이미지 URL:', pagefindImage);
                                }
                            }
                        });
                    }
                    
                    const result = {
                        url: resultUrl,
                        meta: {
                            title: titleElement.textContent.trim(),
                            tags: tags.length > 0 ? tags : undefined,
                            image: pagefindImage
                        },
                        excerpt: excerptElement ? excerptElement.innerHTML : '',
                        sub_results: subResults.length > 0 ? subResults : undefined
                    };
                    
                    // 커스텀 결과 생성 및 추가
                    console.log('createCustomSearchResult 호출 시작:', resultUrl);
                    const customResult = this.resultRenderer.createCustomSearchResult(result);
                    console.log('createCustomSearchResult 완료:', !!customResult, customResult ? customResult.className : 'no element');
                    
                    if (customResult) {
                        console.log('DOM에 추가 시작');
                        customResultsContainer.appendChild(customResult);
                        console.log('DOM에 추가 완료, 현재 children count:', customResultsContainer.children.length);
                    } else {
                        console.error('createCustomSearchResult가 null 반환');
                    }
                    
                    // 처리된 URL 기록
                    this.processedUrls.add(resultUrl);
                    addedCount++;
                    
                } catch (error) {
                    console.warn('결과 변환 실패:', error);
                }
            }
            
            console.log(`새로운 결과 ${addedCount}개 추가됨`);
            
            // "더 보기" 버튼 처리
            const existingLoadMoreButton = customResultsContainer.querySelector('.pagefind-ui__button');
            if (existingLoadMoreButton) {
                existingLoadMoreButton.remove();
            }
            
            const loadMoreButton = document.querySelector('#pagefind-search .pagefind-ui__button');
            if (loadMoreButton) {
                const customLoadMoreButton = loadMoreButton.cloneNode(true);
                customLoadMoreButton.onclick = () => {
                    loadMoreButton.click();
                    console.log("더 보기 버튼 클릭");
                    this.debouncedConvertResults();
                };
                customResultsContainer.appendChild(customLoadMoreButton);
            }
            
            this.lastProcessedResultsCount = pagefindResults.length;
            
        } catch (error) {
            console.error('convertPagefindResults 실행 실패:', error);
        } finally {
            this.isConverting = false;
        }
    }
}

// ========================================
// 전역 인스턴스 생성
// ========================================

// DOM이 로드된 후 SearchManager 인스턴스 생성
document.addEventListener('DOMContentLoaded', function() {
    window.SearchManager = new SearchManager();
});
