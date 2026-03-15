<#
.SYNOPSIS
    Improves a single blog post under content/post using Cursor Agent CLI and project rules.

.DESCRIPTION
    Wrapper for improve-md-with-agent.ps1 that restricts the target to content/post.
    Accepts a path to an md file under content/post (full path or relative to repo root),
    or a path relative to content/post (e.g. 2024/2024-10-16-two-pointers/index.md).
    Validates the file is under content/post, then invokes the main improvement script.
    Rules applied: global .cursor/rules and hugo-content-bundle-naming (no collection-specific rules).

.PARAMETER Path
    Path to the md file to improve. Can be:
    - Full or relative path under content/post (e.g. content/post/2024/2024-10-16-two-pointers/index.md)
    - Path relative to content/post (e.g. 2024/2024-10-16-two-pointers/index.md)

.PARAMETER DryRun
    If set, do not invoke agent; only print the constructed prompt (passed through to improve-md-with-agent.ps1).

.PARAMETER Trust
    Pass --trust to agent for headless/script use (passed through to improve-md-with-agent.ps1).

.EXAMPLE
    .\script\improve-post-with-agent.ps1 -Path "content/post/2024/2024-10-16-two-pointers/index.md" -Trust

.EXAMPLE
    .\script\improve-post-with-agent.ps1 -Path "2024/2024-10-16-two-pointers/index.md" -DryRun
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Path,

    [switch]$DryRun,
    [switch]$Trust
)

$ErrorActionPreference = 'Stop'
$Path = ($Path -replace '\r\n?|\n', '').Trim()
$root = (Split-Path $PSScriptRoot -Parent).TrimEnd()
$postRoot = Join-Path $root 'content\post'

# Resolve path: if it already contains content/post, use as-is relative to root; else treat as relative to content/post
$pathNorm = $Path -replace '/', [IO.Path]::DirectorySeparatorChar
$resolvedPath = $null

if ($pathNorm.StartsWith('content' + [IO.Path]::DirectorySeparatorChar + 'post', [StringComparison]::OrdinalIgnoreCase) -or
    $pathNorm.StartsWith('content/post', [StringComparison]::OrdinalIgnoreCase)) {
    $resolvedPath = Join-Path $root $pathNorm
} elseif ($pathNorm.StartsWith('content' + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase) -or
          $pathNorm.StartsWith('content/', [StringComparison]::OrdinalIgnoreCase)) {
    Write-Error "Path must be under content/post. Use improve-md-with-agent.ps1 for other content. Got: $Path"
} else {
    # Relative to content/post
    $resolvedPath = Join-Path $postRoot $pathNorm
}

$resolvedPath = [System.IO.Path]::GetFullPath($resolvedPath)
$postRootFull = [System.IO.Path]::GetFullPath($postRoot)

if (-not $resolvedPath.StartsWith($postRootFull, [StringComparison]::OrdinalIgnoreCase)) {
    Write-Error "Path must be under content/post. Got: $Path (resolved: $resolvedPath)"
}
if (-not (Test-Path -LiteralPath $resolvedPath -PathType Leaf)) {
    Write-Error "File not found: $resolvedPath"
}

# Path relative to repo root for the main script (no newlines for safe parameter passing)
$relativeToRoot = $resolvedPath.Substring($root.Length).TrimStart([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar) -replace '\\', '/' -replace '\r\n?|\n', ''

$mainScript = Join-Path $PSScriptRoot 'improve-md-with-agent.ps1'
$params = @{ Path = $relativeToRoot }
if ($DryRun) { $params['DryRun'] = $true }
if ($Trust)  { $params['Trust']  = $true }
& $mainScript @params
exit $LASTEXITCODE
