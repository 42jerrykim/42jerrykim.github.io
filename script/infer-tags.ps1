<#
.SYNOPSIS
    Infers and adds tags to files with fewer than the minimum tag count.
.PARAMETER DryRun
    Show what would change without modifying files.
.PARAMETER MinTags
    Minimum number of tags a file should have. Default: 20.
#>
[CmdletBinding()]
param(
    [switch]$DryRun,
    [int]$MinTags = 20
)

$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$taxonomyPath = Join-Path $root 'data\tags.yaml'
$contentRoot  = Join-Path $root 'content'
$pathMapTsv   = Join-Path $PSScriptRoot 'path-tag-map.tsv'
$kwMapTsv     = Join-Path $PSScriptRoot 'keyword-tag-map.tsv'

$approvedTags = [System.Collections.Generic.HashSet[string]]::new(
    [System.StringComparer]::OrdinalIgnoreCase
)
foreach ($line in (Get-Content $taxonomyPath -Encoding UTF8)) {
    if ($line -match '^\s+-\s+(.+)$') {
        $null = $approvedTags.Add($Matches[1].Trim().Trim('"').Trim("'"))
    }
}
Write-Host "Loaded $($approvedTags.Count) approved tags" -ForegroundColor Cyan

# Load path-based tag map from TSV
$pathTagMap = [ordered]@{}
foreach ($line in (Get-Content $pathMapTsv -Encoding UTF8)) {
    $parts = $line -split "`t"
    if ($parts.Count -ge 2) {
        $pathTagMap[$parts[0]] = $parts[1..($parts.Count - 1)]
    }
}
Write-Host "Loaded $($pathTagMap.Count) path tag mappings" -ForegroundColor Cyan

# Load keyword-tag map from TSV
$keywordTagMap = [ordered]@{}
foreach ($line in (Get-Content $kwMapTsv -Encoding UTF8)) {
    $parts = $line -split "`t"
    if ($parts.Count -ge 2) {
        $keywordTagMap[$parts[0]] = $parts[1..($parts.Count - 1)]
    }
}
Write-Host "Loaded $($keywordTagMap.Count) keyword tag mappings" -ForegroundColor Cyan

$files = Get-ChildItem $contentRoot -Recurse -Filter 'index.md'
$filesAugmented = 0
$totalAdded = 0

foreach ($f in $files) {
    $raw = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
    if ($raw -notmatch '(?s)^---\s*\r?\n(.*?)\r?\n---') { continue }
    $fmBlock = $Matches[1]
    $fmLines = $fmBlock -split "`n"
    $rel = $f.FullName.Substring($root.Length + 1)

    if ($rel -match '^content\\page\\') { continue }
    if ($fmBlock -match 'draft\s*:\s*true') { continue }

    # parse existing tags
    $existingTags = [System.Collections.Generic.List[string]]::new()
    $inTags = $false
    $tagHeaderIdx = -1
    for ($i = 0; $i -lt $fmLines.Count; $i++) {
        $t = $fmLines[$i].Trim()
        if ($t -match '^tags\s*:' -and $t -notmatch '\[') {
            $inTags = $true; $tagHeaderIdx = $i; continue
        }
        if ($inTags) {
            if ($t -match '^-\s+(.+)$') { $existingTags.Add($Matches[1].Trim().Trim('"').Trim("'")) }
            elseif ($t -ne '' -and $t -notmatch '^-') { $inTags = $false }
        }
    }

    if ($existingTags.Count -ge $MinTags) { continue }

    $seen = [System.Collections.Generic.HashSet[string]]::new(
        [System.StringComparer]::OrdinalIgnoreCase
    )
    foreach ($et in $existingTags) { $null = $seen.Add($et) }
    $newTags = [System.Collections.Generic.List[string]]::new($existingTags)

    # extract title and categories for inference
    $title = ''
    $categories = @()
    $inCat = $false
    foreach ($ln in $fmLines) {
        $lt = $ln.Trim()
        if ($lt -match '^title\s*:\s*"?(.+?)"?\s*$') { $title = $Matches[1] }
        if ($lt -match '^categories\s*:') { $inCat = $true; continue }
        if ($inCat) {
            if ($lt -match '^-\s+(.+)$') { $categories += $Matches[1].Trim().Trim('"').Trim("'") }
            elseif ($lt -ne '' -and $lt -notmatch '^-') { $inCat = $false }
        }
    }

    # get body text (after frontmatter) for content-based inference
    $fmEndMarker = "---"
    $firstEnd = $raw.IndexOf($fmEndMarker)
    $secondEnd = $raw.IndexOf($fmEndMarker, $firstEnd + 3)
    $bodyText = ''
    if ($secondEnd -gt 0) {
        $bodyStart = $secondEnd + 3
        $bodyLen = [Math]::Min(3000, $raw.Length - $bodyStart)
        if ($bodyLen -gt 0) { $bodyText = $raw.Substring($bodyStart, $bodyLen) }
    }

    # Source 1: Directory path
    foreach ($pathKey in $pathTagMap.Keys) {
        if ($rel -match $pathKey) {
            foreach ($pt in $pathTagMap[$pathKey]) {
                if ($approvedTags.Contains($pt) -and $seen.Add($pt)) { $newTags.Add($pt) }
            }
            break
        }
    }

    # Source 2: Categories
    foreach ($cat in $categories) {
        if ($approvedTags.Contains($cat) -and $seen.Add($cat)) { $newTags.Add($cat) }
    }

    # Source 3: Title bracket prefix
    if ($title -match '^\[(\w+)\]') {
        $prefix = $Matches[1]
        if ($approvedTags.Contains($prefix) -and $seen.Add($prefix)) { $newTags.Add($prefix) }
    }

    # Source 4: Title + body keyword matching
    $searchText = "$title $bodyText"
    foreach ($kv in $keywordTagMap.GetEnumerator()) {
        if ($searchText -match $kv.Key) {
            foreach ($kt in $kv.Value) {
                if ($approvedTags.Contains($kt) -and $seen.Add($kt)) { $newTags.Add($kt) }
            }
        }
    }

    if ($newTags.Count -le $existingTags.Count) { continue }

    $addedCount = $newTags.Count - $existingTags.Count
    $filesAugmented++
    $totalAdded += $addedCount

    if ($DryRun) {
        Write-Host "  $rel : $($existingTags.Count) -> $($newTags.Count) (+$addedCount)" -ForegroundColor Yellow
        continue
    }

    # rewrite tags section preserving indentation
    if ($tagHeaderIdx -ge 0) {
        $newFmLines = [System.Collections.Generic.List[string]]::new()
        $skipTagItems = $false
        $tagLine = $fmLines[$tagHeaderIdx]
        $headerIndent = ''
        if ($tagLine -match '^(\s+)') { $headerIndent = $Matches[1] }
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
        [System.IO.File]::WriteAllText($f.FullName, $newContent, [System.Text.UTF8Encoding]::new($false))
    } else {
        # no tags: header - insert before end of frontmatter
        $headerIndent = ''
        $itemIndent = ''
        foreach ($ln in $fmLines) {
            if ($ln -match '^(\s+)\w+\s*:') { $headerIndent = $Matches[1]; $itemIndent = $Matches[1]; break }
        }

        $tagBlock = [System.Collections.Generic.List[string]]::new()
        $tagBlock.Add("${headerIndent}tags:")
        foreach ($nt in $newTags) {
            if ($nt -match '[\[\]{},:#>|&*!%@`]' -or $nt -match '^\s' -or $nt -match '\s$' -or $nt -match '^[''"]') {
                $tagBlock.Add("${itemIndent}- `"$nt`"")
            } else {
                $tagBlock.Add("${itemIndent}- $nt")
            }
        }

        $fmLinesList = [System.Collections.Generic.List[string]]::new($fmLines)
        $fmLinesList.InsertRange($fmLines.Count, $tagBlock)
        $newFm = $fmLinesList -join "`n"
        $newContent = $raw.Replace($fmBlock, $newFm)
        [System.IO.File]::WriteAllText($f.FullName, $newContent, [System.Text.UTF8Encoding]::new($false))
    }

    Write-Host "  $rel : $($existingTags.Count) -> $($newTags.Count) (+$addedCount)" -ForegroundColor Yellow
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  Tag Inference Report" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Files augmented: $filesAugmented"
Write-Host "  Total tags added: $totalAdded"
if ($DryRun) { Write-Host "`n[DRY RUN] No files modified." -ForegroundColor Magenta }
