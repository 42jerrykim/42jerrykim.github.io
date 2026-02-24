# Hugo 빌드 및 서버 실행 스크립트
# 이 스크립트는 다음 작업을 순차적으로 수행한다:
# 1. Hugo 빌드 실행
# 2. Pagefind 검색 인덱스 생성
# 3. Hugo 개발 서버 시작

Write-Host "Hugo 빌드를 시작합니다..." -ForegroundColor Yellow
hugo build --cleanDestinationDir --logLevel=info

if ($LASTEXITCODE -eq 0) {
    Write-Host "Hugo 빌드가 성공적으로 완료되었습니다." -ForegroundColor Green

    Write-Host "원본 PNG 파일 정리 중..." -ForegroundColor Yellow
    Get-ChildItem -Path "public\post" -Recurse -File -Filter "*.png" |
        Where-Object { $_.Name -notmatch '_hu_' } |
        Remove-Item -Force -ErrorAction SilentlyContinue
    Get-ChildItem -Path "public\tags" -Recurse -Directory -Filter "page" |
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    Get-ChildItem -Path "public\categories" -Recurse -Directory -Filter "page" |
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "정리 완료." -ForegroundColor Green

    Write-Host "Pagefind 검색 인덱스를 생성합니다..." -ForegroundColor Yellow
    python -m pagefind --site "public" --glob "post/**/*.html" --verbose
    # python -m pagefind --site "public" --glob "**/*.html" --glob "!tags/**/*.html" --glob "!categories/**/*.html"

    if ($LASTEXITCODE -eq 0) {
        Write-Host "Pagefind 검색 인덱스가 성공적으로 생성되었습니다." -ForegroundColor Green
        
        Write-Host "Hugo 개발 서버를 시작합니다..." -ForegroundColor Cyan
        
        hugo serve --port 12345 --templateMetrics --templateMetricsHints --logLevel=info
    } else {
        Write-Host "Pagefind 검색 인덱스 생성에 실패했습니다." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Hugo 빌드에 실패했습니다." -ForegroundColor Red
    exit 1
} 