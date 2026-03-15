<#
.SYNOPSIS
    Improves a single blog post (md) file using Cursor Agent CLI and project rules.

.DESCRIPTION
    Accepts one md file path, validates it is under content/, detects collection
    from content/collection/<Name>/, builds a prompt that references global rules
    (.cursor/rules) and optional collection rules, then runs `agent -p "..."`.
    The agent edits the file in place. Use -DryRun to only print the prompt.
    Rules applied: global (.cursor/rules + hugo-content-bundle-naming); if path
    is under content/collection/<Name>/, that collection's .cursor/rules are also
    referenced in the prompt. Run from repo root; Cursor CLI must be installed.

.PARAMETER Path
    Path to the md file to improve (e.g. content/collection/cmd/xcopy/index.md).
    Can be relative to repo root or absolute.

.PARAMETER DryRun
    If set, do not invoke agent; only print the constructed prompt.

.PARAMETER Trust
    Pass --trust to agent for headless/script use (avoids approval prompts).

.EXAMPLE
    .\script\improve-md-with-agent.ps1 -Path "content/collection/cmd/xcopy/index.md" -Trust

.EXAMPLE
    .\script\improve-md-with-agent.ps1 -Path "content/collection/Algorithm/2024/2024-09-23-BOJ-2618/index.md" -DryRun
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Path,

    [switch]$DryRun,
    [switch]$Trust
)

$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$contentRoot = Join-Path $root 'content'

# Resolve to absolute path and ensure under content
$resolvedPath = $Path
if (-not [System.IO.Path]::IsPathRooted($Path)) {
    $resolvedPath = Join-Path $root $Path
}
$resolvedPath = [System.IO.Path]::GetFullPath($resolvedPath)
$contentRootFull = [System.IO.Path]::GetFullPath($contentRoot)

if (-not $resolvedPath.StartsWith($contentRootFull, [StringComparison]::OrdinalIgnoreCase)) {
    Write-Error "Path must be under content. Got: $Path"
}
if (-not (Test-Path -LiteralPath $resolvedPath -PathType Leaf)) {
    Write-Error "File not found: $resolvedPath"
}

# Path relative to repo root (forward slashes for prompt)
$relativePath = $resolvedPath.Substring($root.Length).TrimStart([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)
$relativePath = $relativePath -replace '\\', '/'

# Extract collection name: content/collection/<CollectionName>/...
$collectionName = $null
if ($relativePath -match '^content/collection/([^/]+)/') {
    $collectionName = $Matches[1]
}

# Build collection rules path for prompt (if any)
$collectionRulesHint = ''
if ($collectionName) {
    $rulesDir = Join-Path $root "content\collection\$collectionName\.cursor\rules"
    if (Test-Path $rulesDir) {
        $ruleFiles = Get-ChildItem -Path $rulesDir -Filter '*.mdc' -File -ErrorAction SilentlyContinue
        if ($ruleFiles) {
            $paths = $ruleFiles | ForEach-Object {
                $rel = $_.FullName.Substring($root.Length).TrimStart([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar) -replace '\\', '/'
                $rel
            }
            $collectionRulesHint = " This file is under content/collection/$collectionName/. Read and apply the rules in: " + ($paths -join ', ') + "."
        }
    }
}

# Build prompt
$prompt = @"
Improve the following blog post so it complies with this project's rules. Edit only this file in place.

**File to modify:** $relativePath

**Apply these rules:**
1. Global rules in .cursor/rules (already loaded by CLI):
   - Frontmatter: tags 50+ (use data/tags.yaml when possible), description ~150 chars, title ≤70 chars; new posts use draft: true.
   - Mermaid: node IDs without spaces (camelCase/PascalCase), no reserved words (end, subgraph, graph); labels with special characters (brackets, equals, operators) wrapped in double quotes; use </br> for line breaks, not \n.
2. hugo-content-bundle-naming: title format with category prefix (e.g. [CMD], [Algorithm]), lastmod updated when content is revised.
$(if ($collectionRulesHint) { "3.$collectionRulesHint" })
After editing, briefly list what you changed at the end of your response.
"@

if ($DryRun) {
    Write-Host "=== Dry run: prompt that would be sent to agent ===" -ForegroundColor Cyan
    Write-Host $prompt
    Write-Host "`n[DRY RUN] Agent was not invoked." -ForegroundColor Magenta
    exit 0
}

# Optional: check agent status
$agentOk = $false
try {
    $statusOut = & agent status 2>&1
    if ($LASTEXITCODE -eq 0) { $agentOk = $true }
} catch {
    # agent not in PATH or failed
}
if (-not $agentOk) {
    Write-Host "Warning: 'agent status' failed or agent not found. Ensure Cursor CLI is installed and logged in (agent login). Continuing anyway." -ForegroundColor Yellow
}

# Invoke agent
$agentArgs = @(
    '-p', $prompt,
    '--workspace', $root
)
if ($Trust) {
    $agentArgs += '--trust'
}
Write-Host "Invoking agent for: $relativePath" -ForegroundColor Cyan
& agent @agentArgs
exit $LASTEXITCODE
