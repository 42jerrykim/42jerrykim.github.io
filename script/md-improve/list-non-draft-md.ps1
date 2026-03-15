# list-non-draft-md.ps1
# content/ 아래 .md 파일 중 frontmatter에 draft: true 가 없는 파일의 상대 경로를 한 줄에 하나씩 출력합니다.
# 사용 (프로젝트 루트에서): .\script\md-improve\list-non-draft-md.ps1
# 저장: .\script\md-improve\list-non-draft-md.ps1 | Out-File -FilePath script\md-improve\non-draft-paths.txt -Encoding utf8

$contentDir = "content"
if (-not (Test-Path $contentDir)) {
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    $rootDir = Split-Path -Parent (Split-Path -Parent $scriptDir)
    Set-Location $rootDir
    if (-not (Test-Path $contentDir)) {
        Write-Error "content directory not found."
        exit 1
    }
}

$basePath = (Get-Location).Path
Get-ChildItem -Path $contentDir -Recurse -Filter "*.md" | ForEach-Object {
    $fullName = $_.FullName
    $raw = Get-Content -LiteralPath $fullName -Raw -ErrorAction SilentlyContinue
    if (-not $raw) { return }

    # Extract frontmatter: between first --- and second ---
    if ($raw -notmatch '(?s)^---\r?\n(.*?)\r?\n---') { return }
    $front = $Matches[1]

    # Treat as draft only if "draft:" exists and value is true (within frontmatter)
    if ($front -match '(?m)^draft:\s*true\s*$') { return }

    $rel = $fullName.Replace($basePath + [System.IO.Path]::DirectorySeparatorChar, "").Replace([System.IO.Path]::DirectorySeparatorChar, "/")
    $rel
}
