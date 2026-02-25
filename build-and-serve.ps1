# Hugo 빌드 및 서버 실행 스크립트
# 이 스크립트는 다음 작업을 순차적으로 수행한다:
# 1. Windows Defender 제외 상태 확인
# 2. 병렬 워커 수 증가 (HUGO_NUMWORKERMULTIPLIER)
# 3. (조건부) Hugo 빌드 + Pagefind 검색 인덱스 생성 → static/_pagefind/에 캐싱
# 4. Hugo 개발 서버 시작 (renderStaticToDisk로 pagefind 인덱스 서빙)
#
# pagefind 인덱스가 static/_pagefind/에 이미 존재하면 빌드+pagefind 단계를 건너뛰어
# hugo serve만 1회 빌드로 빠르게 시작한다.
#
# 사용법:
#   .\build-and-serve.ps1                    # 전체 빌드 (pagefind 캐시 있으면 빌드 생략)
#   .\build-and-serve.ps1 -Segment posts     # post 섹션만 빌드 (빠른 개발용)
#   .\build-and-serve.ps1 -Segment recent    # post + collection 빌드
#   .\build-and-serve.ps1 -Pagefind          # pagefind 인덱스 강제 재생성

param(
    [ValidateSet("", "posts", "recent")]
    [string]$Segment = "",
    [switch]$Pagefind
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

# --- WebP/리소스 캐시 활용 (CI와 동일 전략) ---
# HUGO_CACHEDIR을 워크스페이스 내 .hugo_cache로 두면, 빌드·서브 시 캐시가 유지되어
# 다음 실행에서 이미지(WebP) 변환·모듈 캐시를 재사용하고 빌드가 빨라진다. (deploy.yml 참고)
$env:HUGO_CACHEDIR = Join-Path (Get-Location) ".hugo_cache"

# --- Pagefind 인덱스 생성 (조건부) ---
$pagefindIndex = "static/_pagefind/pagefind.js"
$needPagefind = $Pagefind -or !(Test-Path $pagefindIndex)

if ($needPagefind) {
    if ($Pagefind) {
        Write-Host "Pagefind 인덱스를 강제 재생성합니다..." -ForegroundColor Yellow
    } else {
        Write-Host "Pagefind 인덱스가 없습니다. 빌드 후 생성합니다..." -ForegroundColor Yellow
    }

    # Hugo 빌드 (pagefind 인덱싱용). production 사용: development는 config에서 imageProcessing을 끄므로
    # WebP 변환이 생략되고, 캐시가 채워지지 않음. production으로 빌드해 WebP·캐시를 활용한다.
    $buildArgs = @("build", "--cleanDestinationDir", "--gc", "--environment", "--logLevel=info")

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

    if ($LASTEXITCODE -ne 0) {
        Write-Host "Hugo 빌드에 실패했습니다." -ForegroundColor Red
        exit 1
    }

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

    # Pagefind를 백그라운드 작업으로 실행 (serve와 병렬화)
    Write-Host "Pagefind 검색 인덱스를 백그라운드에서 생성합니다..." -ForegroundColor Yellow
    $pagefindJob = Start-Job -ScriptBlock {
        param($WorkDir)
        Set-Location $WorkDir
        python -m pagefind --site "public" --output-path "static/_pagefind" --glob "post/**/*.html" --verbose 2>&1
    } -ArgumentList (Get-Location).Path

} else {
    Write-Host "Pagefind 인덱스가 캐시되어 있습니다. 빌드를 건너뜁니다." -ForegroundColor Green
    Write-Host "  (인덱스 재생성이 필요하면 -Pagefind 플래그를 사용하세요)" -ForegroundColor DarkGray
}

# --- Hugo 개발 서버 시작 ---
Write-Host "Hugo 개발 서버를 시작합니다..." -ForegroundColor Cyan

$serveArgs = @("serve", "-D", "--port", "12345", "--renderStaticToDisk", "--templateMetrics", "--templateMetricsHints", "--logLevel=info")
if ($Segment) {
    $serveArgs += "--renderSegments"
    $serveArgs += $Segment
}

hugo @serveArgs

# --- 백그라운드 Pagefind 작업 정리 ---
if ($pagefindJob) {
    if ($pagefindJob.State -eq 'Running') {
        Stop-Job $pagefindJob -ErrorAction SilentlyContinue
    }
    $pagefindOutput = Receive-Job $pagefindJob -ErrorAction SilentlyContinue
    if ($pagefindOutput) {
        Write-Host "`nPagefind 작업 결과:" -ForegroundColor Yellow
        $pagefindOutput | Write-Host
    }
    Remove-Job $pagefindJob -ErrorAction SilentlyContinue
}

# --- templateMetrics 안내 ---
# hugo serve 종료 후 표시
Write-Host ""
Write-Host "[팁] 위 templateMetrics 출력에서 'cache potential: 100%'인 partial을 확인하세요." -ForegroundColor Cyan
Write-Host "  해당 partial은 'partial' 대신 'partialCached'로 변경하면 빌드가 더 빨라집니다." -ForegroundColor Cyan
