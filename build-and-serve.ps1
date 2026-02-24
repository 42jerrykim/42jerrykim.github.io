# Hugo 빌드 및 서버 실행 스크립트
# 이 스크립트는 다음 작업을 순차적으로 수행한다:
# 1. Windows Defender 제외 상태 확인
# 2. 병렬 워커 수 증가 (HUGO_NUMWORKERMULTIPLIER)
# 3. Hugo 빌드 실행 (pagefind 인덱싱용, development 환경으로 이미지 처리 생략)
# 4. Pagefind 검색 인덱스 생성
# 5. Hugo 개발 서버 시작 (renderToDisk로 pagefind 인덱스 재사용)
#
# 사용법:
#   .\build-and-serve.ps1                  # 전체 빌드
#   .\build-and-serve.ps1 -Segment posts   # post 섹션만 빌드 (빠른 개발용)
#   .\build-and-serve.ps1 -Segment recent  # post + collection 빌드

param(
    [ValidateSet("", "posts", "recent")]
    [string]$Segment = ""
)

# --- Windows Defender 제외 확인 ---
# Hugo 공식 문서: Defender가 빌드 시간을 400% 이상 증가시킬 수 있음
$hugoCmd = Get-Command hugo -ErrorAction SilentlyContinue
if ($hugoCmd) {
    $hugoPath = $hugoCmd.Source
    try { 
        $defenderExclusions = @((Get-MpPreference).ExclusionProcess)
        if ("hugo.exe" -notin $defenderExclusions -and $hugoPath -notin $defenderExclusions) {
            Write-Host "[성능 경고] hugo.exe가 Windows Defender 제외 목록에 없습니다." -ForegroundColor Red
            Write-Host "  Hugo 공식 문서에 따르면 Defender가 빌드 시간을 400%+ 증가시킬 수 있습니다." -ForegroundColor Red
            Write-Host "  제외 설정: Settings > Windows Security > Virus & threat protection" -ForegroundColor Yellow
            Write-Host "    > Manage settings > Exclusions > Add Process > hugo.exe" -ForegroundColor Yellow
            Write-Host "  또는 관리자 PowerShell에서:" -ForegroundColor Yellow
            Write-Host "    Add-MpPreference -ExclusionProcess 'hugo.exe'" -ForegroundColor Cyan
            Write-Host ""
        }
    } catch {
        # Get-MpPreference 실행 불가 시(권한 부족 등) 경고 생략
    }
}

# --- 병렬 워커 수 증가 ---
# Go 루틴은 경량이므로 CPU 코어 수보다 높게 설정해도 안전하며, I/O 대기 시 throughput 개선
$env:HUGO_NUMWORKERMULTIPLIER = 4

# --- Hugo 빌드 ---
$buildArgs = @("build", "--cleanDestinationDir", "--gc", "--environment", "development", "--logLevel=info")

if ($Segment) {
    $buildArgs += "--renderSegments"
    $buildArgs += $Segment
    Write-Host "Hugo 빌드를 시작합니다 (segment: $Segment)..." -ForegroundColor Yellow
} else {
    Write-Host "Hugo 빌드를 시작합니다..." -ForegroundColor Yellow
}

$buildTimer = [System.Diagnostics.Stopwatch]::StartNew()

hugo @buildArgs

$buildTimer.Stop()

if ($LASTEXITCODE -eq 0) {
    Write-Host ("Hugo 빌드 완료 ({0:N1}초)" -f $buildTimer.Elapsed.TotalSeconds) -ForegroundColor Green

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

    if ($LASTEXITCODE -eq 0) {
        Write-Host "Pagefind 검색 인덱스가 성공적으로 생성되었습니다." -ForegroundColor Green
        
        Write-Host "Hugo 개발 서버를 시작합니다..." -ForegroundColor Cyan

        $serveArgs = @("serve", "--port", "12345", "--renderStaticToDisk", "--templateMetrics", "--templateMetricsHints", "--logLevel=info")
        if ($Segment) {
            $serveArgs += "--renderSegments"
            $serveArgs += $Segment
        }
        
        hugo @serveArgs
    } else {
        Write-Host "Pagefind 검색 인덱스 생성에 실패했습니다." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Hugo 빌드에 실패했습니다." -ForegroundColor Red
    exit 1
}

# --- templateMetrics 안내 ---
# hugo serve 종료 후 표시
Write-Host ""
Write-Host "[팁] 위 templateMetrics 출력에서 'cache potential: 100%'인 partial을 확인하세요." -ForegroundColor Cyan
Write-Host "  해당 partial은 'partial' 대신 'partialCached'로 변경하면 빌드가 더 빨라집니다." -ForegroundColor Cyan 