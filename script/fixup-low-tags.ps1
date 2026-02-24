<#
.SYNOPSIS
    Final pass: aggressively infers tags for files still below MinTags.
    Uses broader heuristics: path segments, title words, generic topic tags.
#>
[CmdletBinding()]
param([int]$MinTags = 6)

$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$taxonomyPath = Join-Path $root 'data\tags.yaml'
$contentRoot  = Join-Path $root 'content'

$approvedTags = [System.Collections.Generic.HashSet[string]]::new(
    [System.StringComparer]::OrdinalIgnoreCase
)
foreach ($line in (Get-Content $taxonomyPath -Encoding UTF8)) {
    if ($line -match '^\s+-\s+(.+)$') {
        $null = $approvedTags.Add($Matches[1].Trim().Trim('"').Trim("'"))
    }
}

$files = Get-ChildItem $contentRoot -Recurse -Filter 'index.md'
$fixedCount = 0

foreach ($f in $files) {
    $raw = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
    if ($raw -notmatch '(?s)^---\s*\r?\n(.*?)\r?\n---') { continue }
    $fmBlock = $Matches[1]
    $fmLines = $fmBlock -split "`n"
    $rel = $f.FullName.Substring($root.Length + 1)

    if ($rel -match '^content\\page\\') { continue }
    if ($fmBlock -match 'draft\s*:\s*true') { continue }

    $existingTags = [System.Collections.Generic.List[string]]::new()
    $inTags = $false; $tagHeaderIdx = -1
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

    $seen = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
    foreach ($et in $existingTags) { $null = $seen.Add($et) }
    $newTags = [System.Collections.Generic.List[string]]::new($existingTags)

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

    $fmEndMarker = "---"
    $firstEnd = $raw.IndexOf($fmEndMarker)
    $secondEnd = $raw.IndexOf($fmEndMarker, $firstEnd + 3)
    $bodyText = ''
    if ($secondEnd -gt 0) {
        $bodyStart = $secondEnd + 3
        $bodyLen = [Math]::Min(5000, $raw.Length - $bodyStart)
        if ($bodyLen -gt 0) { $bodyText = $raw.Substring($bodyStart, $bodyLen) }
    }

    $allText = "$title $bodyText $rel"

    # Aggressive per-word scan: check each word against approved tags
    $words = $allText -replace '[^a-zA-Z0-9\-\.\+\#]', ' ' -split '\s+' | Where-Object { $_.Length -ge 2 }
    foreach ($w in $words) {
        if ($newTags.Count -ge $MinTags) { break }
        if ($approvedTags.Contains($w) -and $seen.Add($w)) { $newTags.Add($w) }
    }

    # Add categories as tags
    foreach ($cat in $categories) {
        if ($newTags.Count -ge $MinTags) { break }
        if ($approvedTags.Contains($cat) -and $seen.Add($cat)) { $newTags.Add($cat) }
    }

    # Broad topic inference from path/title
    $broadMatches = @()
    if ($allText -match 'cpp|c\+\+|cout|cin|include') { $broadMatches += @('C++', 'Implementation') }
    if ($allText -match 'csharp|c#|\.net|dotnet') { $broadMatches += @('CSharp', '.NET') }
    if ($allText -match 'python|pip|pypi') { $broadMatches += @('Python') }
    if ($allText -match 'java(?!script)') { $broadMatches += @('Java') }
    if ($allText -match 'javascript|js(?:\s|$)|node') { $broadMatches += @('JavaScript') }
    if ($allText -match 'typescript|ts(?:\s|$)') { $broadMatches += @('TypeScript') }
    if ($allText -match 'rust') { $broadMatches += @('Rust') }
    if ($allText -match 'go(?:lang)') { $broadMatches += @('Go') }
    if ($allText -match 'shell|bash|sh(?:\s|$)|zsh|terminal') { $broadMatches += @('Shell', 'Bash', 'Linux', 'Terminal') }
    if ($allText -match 'linux|ubuntu|debian|centos|rpm') { $broadMatches += @('Linux') }
    if ($allText -match 'windows|win10|win11|hyper-?v|rdp') { $broadMatches += @('Windows') }
    if ($allText -match 'git(?:\s|$|hub)|commit|branch|merge') { $broadMatches += @('Git') }
    if ($allText -match 'docker|container') { $broadMatches += @('Docker') }
    if ($allText -match 'css|html|web|blog|seo') { $broadMatches += @('Web', 'CSS', 'HTML') }
    if ($allText -match 'keyboard') { $broadMatches += @('Keyboard', 'Hardware') }
    if ($allText -match 'test|tdd') { $broadMatches += @('Testing') }
    if ($allText -match 'security|encrypt|ssl|tls|virus|defend|antivirus') { $broadMatches += @('Security') }
    if ($allText -match 'ai|machine.learn|deep.learn|llm|gpt|chatgpt|prompt') { $broadMatches += @('AI') }
    if ($allText -match 'algorithm|sort|search|graph|tree|dp|greedy') { $broadMatches += @('Algorithm') }
    if ($allText -match 'vocab|english|word') { $broadMatches += @('Vocabulary', 'English') }
    if ($allText -match 'movie|film|cinema') { $broadMatches += @('Movie') }
    if ($allText -match 'tv.show|series|season|episode|netflix') { $broadMatches += @('TV-Show') }
    if ($allText -match 'regex|regular.express') { $broadMatches += @('String', 'Implementation') }
    if ($allText -match 'cycling|bike|bicycle') { $broadMatches += @('Cycling') }
    if ($allText -match 'game|gaming|sim.rac') { $broadMatches += @('Gaming') }
    if ($allText -match 'photo|image|camera') { $broadMatches += @('Photography') }
    if ($allText -match 'network|tcp|ip|dns|http') { $broadMatches += @('Networking') }
    if ($allText -match 'deploy|ci.cd|devops') { $broadMatches += @('Deployment', 'DevOps') }
    if ($allText -match 'config|setup|install') { $broadMatches += @('Configuration') }
    if ($allText -match 'review') { $broadMatches += @('Review') }
    if ($allText -match 'tutorial|how.to|guide') { $broadMatches += @('Tutorial', 'Guide') }
    if ($allText -match 'trouble|fix|error|issue|bug|solve|resolv') { $broadMatches += @('Troubleshooting') }
    if ($allText -match 'history|calendar|ancient') { $broadMatches += @('History') }
    if ($allText -match 'science|biology|physics|chemistry|evolution') { $broadMatches += @('Science') }
    if ($allText -match 'career|soft.skill|team|leadership') { $broadMatches += @('Career') }
    if ($allText -match 'productiv|workflow|automat') { $broadMatches += @('Productivity') }
    if ($allText -match 'mobile|android|ios|samsung|galaxy|phone') { $broadMatches += @('Mobile') }
    if ($allText -match 'self.hosted|nas|synology|plex') { $broadMatches += @('Self-Hosted') }
    if ($allText -match 'open.source') { $broadMatches += @('Open-Source') }
    if ($allText -match 'hardware|gadget|device') { $broadMatches += @('Hardware', 'Gadget') }
    if ($allText -match 'speaker|audio|sound') { $broadMatches += @('Speaker') }
    if ($allText -match 'watch|timepiece') { $broadMatches += @('Watch', 'Brand') }
    if ($allText -match 'markdown|kramdown') { $broadMatches += @('Markdown') }
    if ($allText -match 'jekyll') { $broadMatches += @('Jekyll', 'Blog') }
    if ($allText -match 'hugo') { $broadMatches += @('Hugo', 'Blog') }
    if ($allText -match 'memory|allocat') { $broadMatches += @('Memory') }
    if ($allText -match 'file.?system|directory|folder|path|mount') { $broadMatches += @('File-System') }
    if ($allText -match 'process|thread|concurren') { $broadMatches += @('Process', 'Concurrency') }
    if ($allText -match 'api|rest|grpc|endpoint') { $broadMatches += @('API') }
    if ($allText -match 'database|sql|query') { $broadMatches += @('Database', 'SQL') }
    if ($allText -match 'ocr') { $broadMatches += @('AI', 'Technology') }

    foreach ($bt in $broadMatches) {
        if ($newTags.Count -ge $MinTags) { break }
        if ($approvedTags.Contains($bt) -and $seen.Add($bt)) { $newTags.Add($bt) }
    }

    # Final fallback: add generic tags based on content type
    $fallbackTags = @('Technology', 'Tutorial', 'Guide', 'Implementation', 'Quick-Reference', 'Review', 'Troubleshooting', 'Education', 'Productivity')
    foreach ($fb in $fallbackTags) {
        if ($newTags.Count -ge $MinTags) { break }
        if ($approvedTags.Contains($fb) -and $seen.Add($fb)) { $newTags.Add($fb) }
    }

    if ($newTags.Count -le $existingTags.Count) { continue }

    $addedCount = $newTags.Count - $existingTags.Count
    $fixedCount++

    # rewrite frontmatter
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
        $headerIndent = ''; $itemIndent = ''
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
Write-Host "  Final Fixup Report" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Files fixed: $fixedCount"
