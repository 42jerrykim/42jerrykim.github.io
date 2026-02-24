<#
.SYNOPSIS
    Cleans up tags across all Hugo content files based on an approved taxonomy.
.PARAMETER DryRun
    Show what would change without modifying files.
.PARAMETER ReportOnly
    Only output statistics, skip file modifications.
#>
[CmdletBinding()]
param(
    [switch]$DryRun,
    [switch]$ReportOnly
)

$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$taxonomyPath = Join-Path $root 'data\tags.yaml'
$contentRoot  = Join-Path $root 'content'
$mergeTsv     = Join-Path $PSScriptRoot 'tag-merge-map.tsv'
$mergeKoTsv   = Join-Path $PSScriptRoot 'tag-merge-map-ko.tsv'

# ---- 1. Load approved tags ----
$approvedTags = [System.Collections.Generic.HashSet[string]]::new(
    [System.StringComparer]::OrdinalIgnoreCase
)
foreach ($line in (Get-Content $taxonomyPath -Encoding UTF8)) {
    if ($line -match '^\s+-\s+(.+)$') {
        $null = $approvedTags.Add($Matches[1].Trim().Trim('"').Trim("'"))
    }
}
Write-Host "Loaded $($approvedTags.Count) approved tags" -ForegroundColor Cyan

# ---- 2. Load merge mappings ----
$mergeMap = @{}
foreach ($tsvPath in @($mergeTsv, $mergeKoTsv)) {
    if (Test-Path $tsvPath) {
        foreach ($line in (Get-Content $tsvPath -Encoding UTF8)) {
            $parts = $line -split "`t", 2
            if ($parts.Count -eq 2 -and $parts[0].Trim() -ne '') {
                $from = $parts[0].Trim()
                $to   = $parts[1].Trim()
                if (-not $mergeMap.ContainsKey($from)) {
                    $mergeMap[$from] = $to
                }
            }
        }
    }
}
Write-Host "Loaded $($mergeMap.Count) merge mappings" -ForegroundColor Cyan

# ---- 3. Category fallback ----
$categoryFallback = @{
    'Algorithm'        = @('Algorithm')
    'Movie'            = @('Movie')
    'English'          = @('Vocabulary', 'English')
    'Vocabulary'       = @('Vocabulary', 'English')
    'Science'          = @('Science')
    'History'          = @('History')
    'Culture'          = @('Culture')
    'Cycling'          = @('Cycling')
    'Gaming'           = @('Gaming')
    'ChatGPT'          = @('ChatGPT', 'AI')
    'Internet'         = @('Internet')
    'Brand'            = @('Brand')
    'EvolutionaryBiology' = @('Biology', 'Science')
    'Science Fiction'  = @('Sci-Fi')
    'Drama'            = @('Drama')
    'Comedy'           = @('Comedy')
    'Thriller'         = @('Thriller')
    'Horror'           = @('Horror')
    'Romance'          = @('Romance')
    'Animation'        = @('Animation')
    'Action'           = @('Action')
    'Fantasy'          = @('Fantasy')
    'Windows'          = @('Windows')
    'Linux'            = @('Linux')
    'PowerShell'       = @('PowerShell')
    'Hugo'             = @('Hugo', 'Blog')
    'Troubleshooting'  = @('Troubleshooting')
    'Python'           = @('Python')
    'CSharp'           = @('CSharp')
    'TV-Show'          = @('TV-Show')
}

# ---- 4. Process files ----
$files = Get-ChildItem $contentRoot -Recurse -Filter 'index.md'
$totalBefore = 0
$totalAfter  = 0
$filesModified = 0
$filesProcessed = 0
$tagsMerged = 0
$tagsRemoved = 0
$removedReport = @{}

foreach ($f in $files) {
    $raw = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
    if ($raw -notmatch '(?s)^---\s*\r?\n(.*?)\r?\n---') { continue }
    $filesProcessed++
    $fmBlock = $Matches[1]
    $fmLines = $fmBlock -split "`n"

    # extract categories
    $categories = @()
    $inCat = $false
    foreach ($ln in $fmLines) {
        $t = $ln.Trim()
        if ($t -match '^categories\s*:') { $inCat = $true; continue }
        if ($inCat) {
            if ($t -match '^-\s+(.+)$') { $categories += $Matches[1].Trim().Trim('"').Trim("'") }
            elseif ($t -ne '' -and $t -notmatch '^-') { $inCat = $false }
        }
    }

    # extract tags and their line range
    $originalTags = [System.Collections.Generic.List[string]]::new()
    $inTags = $false
    $tagHeaderIdx = -1

    for ($i = 0; $i -lt $fmLines.Count; $i++) {
        $t = $fmLines[$i].Trim()
        if ($t -match '^tags\s*:' -and $t -notmatch '\[') {
            $inTags = $true
            $tagHeaderIdx = $i
            continue
        }
        if ($inTags) {
            if ($t -match '^-\s+(.+)$') {
                $originalTags.Add($Matches[1].Trim().Trim('"').Trim("'"))
            } elseif ($t -ne '' -and $t -notmatch '^-') {
                $inTags = $false
            }
        }
    }

    if ($originalTags.Count -eq 0) { continue }
    $totalBefore += $originalTags.Count

    # resolve tags
    $newTags = [System.Collections.Generic.List[string]]::new()
    $seen = [System.Collections.Generic.HashSet[string]]::new(
        [System.StringComparer]::OrdinalIgnoreCase
    )

    foreach ($tag in $originalTags) {
        $resolved = $tag
        if ($mergeMap.ContainsKey($tag)) {
            $resolved = $mergeMap[$tag]
            if ($resolved -ne $tag) { $tagsMerged++ }
        }
        if ($approvedTags.Contains($resolved)) {
            if ($seen.Add($resolved)) { $newTags.Add($resolved) }
        } else {
            $tagsRemoved++
            if ($removedReport.ContainsKey($resolved)) { $removedReport[$resolved]++ }
            else { $removedReport[$resolved] = 1 }
        }
    }

    # fallback if too few tags: use categories
    if ($newTags.Count -lt 3) {
        foreach ($cat in $categories) {
            if ($categoryFallback.ContainsKey($cat)) {
                foreach ($fb in $categoryFallback[$cat]) {
                    if ($seen.Add($fb)) { $newTags.Add($fb) }
                }
            }
            if ($approvedTags.Contains($cat) -and $seen.Add($cat)) {
                $newTags.Add($cat)
            }
        }
    }

    # last resort: try to infer from title bracket prefix
    if ($newTags.Count -lt 1) {
        foreach ($ln in $fmLines) {
            if ($ln.Trim() -match '^title\s*:\s*"?\[(\w+)\]') {
                $prefix = $Matches[1]
                if ($approvedTags.Contains($prefix) -and $seen.Add($prefix)) {
                    $newTags.Add($prefix)
                }
                if ($categoryFallback.ContainsKey($prefix)) {
                    foreach ($fb in $categoryFallback[$prefix]) {
                        if ($seen.Add($fb)) { $newTags.Add($fb) }
                    }
                }
                break
            }
        }
    }

    # check if changed
    $changed = $false
    if ($newTags.Count -ne $originalTags.Count) { $changed = $true }
    else {
        for ($j = 0; $j -lt $newTags.Count; $j++) {
            if ($newTags[$j] -cne $originalTags[$j]) { $changed = $true; break }
        }
    }
    if (-not $changed) { $totalAfter += $originalTags.Count; continue }

    $totalAfter += $newTags.Count
    $filesModified++

    if ($ReportOnly) { continue }

    # rebuild frontmatter, preserving original indentation
    $newFmLines = [System.Collections.Generic.List[string]]::new()
    $skipTagItems = $false

    # detect indentation of the tags header line
    $tagLine = $fmLines[$tagHeaderIdx]
    $headerIndent = ''
    if ($tagLine -match '^(\s+)') { $headerIndent = $Matches[1] }

    # detect item indentation from original tag items
    $itemIndent = $headerIndent
    for ($k = $tagHeaderIdx + 1; $k -lt $fmLines.Count; $k++) {
        if ($fmLines[$k].Trim() -match '^-\s+') {
            if ($fmLines[$k] -match '^(\s*)- ') { $itemIndent = $Matches[1] }
            break
        }
    }

    for ($i = 0; $i -lt $fmLines.Count; $i++) {
        $t = $fmLines[$i].Trim()
        if ($i -eq $tagHeaderIdx) {
            $newFmLines.Add("${headerIndent}tags:")
            foreach ($nt in $newTags) {
                if ($nt -match '[\[\]{},:#>|&*!%@`]' -or $nt -match '^\s' -or $nt -match '\s$' -or $nt -match '^[''"]') {
                    $newFmLines.Add("${itemIndent}- `"$nt`"")
                } else {
                    $newFmLines.Add("${itemIndent}- $nt")
                }
            }
            $skipTagItems = $true
            continue
        }
        if ($skipTagItems) {
            if ($t -match '^-\s+' -or $t -eq '') { continue }
            else { $skipTagItems = $false }
        }
        $newFmLines.Add($fmLines[$i])
    }

    $newFm = $newFmLines -join "`n"
    $newContent = $raw.Replace($fmBlock, $newFm)

    if (-not $DryRun) {
        [System.IO.File]::WriteAllText($f.FullName, $newContent, [System.Text.UTF8Encoding]::new($false))
    }

    if ($DryRun -or $VerbosePreference -eq 'Continue') {
        $rel = $f.FullName.Substring($root.Length + 1)
        Write-Host "  $rel : $($originalTags.Count) -> $($newTags.Count)" -ForegroundColor Yellow
    }
}

# ---- 5. Report ----
Write-Host "`n========================================" -ForegroundColor Green
Write-Host "         Tag Cleanup Report" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "Files processed:  $filesProcessed"
Write-Host "Files modified:   $filesModified"
Write-Host "Total tags before: $totalBefore"
Write-Host "Tags merged:       $tagsMerged"
Write-Host "Tags removed:      $tagsRemoved"
Write-Host "Total tags after:  $totalAfter"
if ($DryRun) { Write-Host "`n[DRY RUN] No files modified." -ForegroundColor Magenta }

Write-Host "`nTop 50 removed tags:" -ForegroundColor Yellow
$removedReport.GetEnumerator() | Sort-Object Value -Descending |
    Select-Object -First 50 | ForEach-Object {
        Write-Host ("  {0,4}x  {1}" -f $_.Value, $_.Key)
    }

$rptPath = Join-Path $PSScriptRoot 'removed-tags-report.txt'
$removedReport.GetEnumerator() | Sort-Object Value -Descending |
    ForEach-Object { "{0}`t{1}" -f $_.Value, $_.Key } |
    Set-Content $rptPath -Encoding UTF8
Write-Host "`nFull report: $rptPath" -ForegroundColor Cyan
