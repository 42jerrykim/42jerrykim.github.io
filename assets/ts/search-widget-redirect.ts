// Search widget redirect to pagefind search page
document.addEventListener('DOMContentLoaded', function() {
    // Search widget form을 찾아서 pagefind 검색 페이지로 리디렉션
    const searchForms = document.querySelectorAll('.search-form');
    const searchWidgets = document.querySelectorAll('.widget.search');
    
    // Search form 처리
    searchForms.forEach(form => {
        // 만약 이미 pagefind 검색 페이지라면 건너뛰기
        if (document.body.classList.contains('template-search')) {
            return;
        }
        
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const input = form.querySelector('input[name="keyword"]') as HTMLInputElement;
            const searchTerm = input?.value.trim();
            
            if (searchTerm) {
                window.location.href = `/search/?keyword=${encodeURIComponent(searchTerm)}`;
            }
        });
    });
    
    // Widget 내의 검색 입력 필드 처리
    searchWidgets.forEach(widget => {
        const input = widget.querySelector('input') as HTMLInputElement;
        const button = widget.querySelector('button') as HTMLButtonElement;
        
        if (input) {
            // 엔터 키 처리
            input.addEventListener('keypress', function(e: KeyboardEvent) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    const searchTerm = input.value.trim();
                    if (searchTerm) {
                        window.location.href = `/search/?keyword=${encodeURIComponent(searchTerm)}`;
                    }
                }
            });
        }
        
        if (button) {
            // 검색 버튼 클릭 처리
            button.addEventListener('click', function(e) {
                e.preventDefault();
                const searchTerm = input?.value.trim();
                if (searchTerm) {
                    window.location.href = `/search/?keyword=${encodeURIComponent(searchTerm)}`;
                }
            });
        }
    });
    
    // 일반적인 검색 입력 필드 처리 (Hugo Stack 테마 특정)
    const searchInputs = document.querySelectorAll('input[placeholder*="검색"], input[placeholder*="Search"], input[name="keyword"]');
    
    searchInputs.forEach(input => {
        // 이미 pagefind 검색 페이지라면 건너뛰기
        if (document.body.classList.contains('template-search')) {
            return;
        }
        
        input.addEventListener('keypress', function(e: KeyboardEvent) {
            if (e.key === 'Enter') {
                e.preventDefault();
                const searchTerm = (input as HTMLInputElement).value.trim();
                if (searchTerm) {
                    window.location.href = `/search/?keyword=${encodeURIComponent(searchTerm)}`;
                }
            }
        });
    });
}); 