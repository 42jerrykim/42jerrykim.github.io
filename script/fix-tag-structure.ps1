<#
.SYNOPSIS
    Fixes structural tag issues: 'tag:' typo -> 'tags:', inline arrays -> YAML lists.
.PARAMETER DryRun
    Show what would change without modifying files.
#>
[CmdletBinding()]
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$contentRoot = Join-Path $root 'content'

$files = Get-ChildItem $contentRoot -Recurse -Filter 'index.md'
$fixedTagTypo = 0
$fixedInlineArray = 0

foreach ($f in $files) {
    $raw = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
    if ($raw -notmatch '(?s)^---\s*\r?\n(.*?)\r?\n---') { continue }
    $fmBlock = $Matches[1]
    $fmLines = $fmBlock -split "`n"
    $modified = $false
    $newFmLines = [System.Collections.Generic.List[string]]::new()

    for ($i = 0; $i -lt $fmLines.Count; $i++) {
        $line = $fmLines[$i]
        $trimmed = $line.Trim()

        # Fix 1: 'tag:' -> 'tags:' (singular to plural)
        if ($trimmed -match '^tag\s*:' -and $trimmed -notmatch '^tags\s*:') {
            $indent = ''
            if ($line -match '^(\s+)') { $indent = $Matches[1] }

            if ($trimmed -match '^tag\s*:\s*\[(.+)\]$') {
                # inline array: tag: [a, b, c]
                $items = $Matches[1] -split ',' | ForEach-Object { $_.Trim().Trim('"').Trim("'").Trim() } | Where-Object { $_ -ne '' }
                $newFmLines.Add("${indent}tags:")
                foreach ($item in $items) {
                    if ($item -match '[\[\]{},:#>|&*!%@`]') {
                        $newFmLines.Add("${indent}- `"$item`"")
                    } else {
                        $newFmLines.Add("${indent}- $item")
                    }
                }
                $modified = $true
                $fixedTagTypo++
                $fixedInlineArray++
            } elseif ($trimmed -match '^tag\s*:\s*$') {
                # tag: with items on next lines
                $newFmLines.Add(($line -replace '(?<=^(\s*))tag(\s*:)', 'tags$2'))
                $modified = $true
                $fixedTagTypo++
            } else {
                # tag: with YAML list items below
                $newFmLines.Add(($line -replace '(?<=^(\s*))tag(\s*:)', 'tags$2'))
                $modified = $true
                $fixedTagTypo++
            }
            continue
        }

        # Fix 2: inline tags: [a, b, c] -> YAML list
        if ($trimmed -match '^tags\s*:\s*\[(.+)\]$') {
            $indent = ''
            if ($line -match '^(\s+)') { $indent = $Matches[1] }
            $items = $Matches[1] -split ',' | ForEach-Object { $_.Trim().Trim('"').Trim("'").Trim() } | Where-Object { $_ -ne '' }
            $newFmLines.Add("${indent}tags:")
            foreach ($item in $items) {
                if ($item -match '[\[\]{},:#>|&*!%@`]') {
                    $newFmLines.Add("${indent}- `"$item`"")
                } else {
                    $newFmLines.Add("${indent}- $item")
                }
            }
            $modified = $true
            $fixedInlineArray++
            continue
        }

        # Fix 3: inline categories: [a, b, c] -> YAML list (for consistency)
        if ($trimmed -match '^categories\s*:\s*\[(.+)\]$') {
            $indent = ''
            if ($line -match '^(\s+)') { $indent = $Matches[1] }
            $items = $Matches[1] -split ',' | ForEach-Object { $_.Trim().Trim('"').Trim("'").Trim() } | Where-Object { $_ -ne '' }
            $newFmLines.Add("${indent}categories:")
            foreach ($item in $items) {
                if ($item -match '[\[\]{},:#>|&*!%@`]') {
                    $newFmLines.Add("${indent}- `"$item`"")
                } else {
                    $newFmLines.Add("${indent}- $item")
                }
            }
            $modified = $true
            continue
        }

        $newFmLines.Add($line)
    }

    if (-not $modified) { continue }

    $newFm = $newFmLines -join "`n"
    $newContent = $raw.Replace($fmBlock, $newFm)

    if (-not $DryRun) {
        [System.IO.File]::WriteAllText($f.FullName, $newContent, [System.Text.UTF8Encoding]::new($false))
    }

    $rel = $f.FullName.Substring($root.Length + 1)
    Write-Host "  Fixed: $rel" -ForegroundColor Yellow
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  Structure Fix Report" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "  tag: -> tags: fixes:      $fixedTagTypo"
Write-Host "  Inline array conversions: $fixedInlineArray"
if ($DryRun) { Write-Host "`n[DRY RUN] No files modified." -ForegroundColor Magenta }
