# generate-improve-commands.ps1
# 비드래프트 경로 목록을 받아 agent -p --force "@경로" "프롬프트" 한 줄씩 출력합니다.
# 사용 (프로젝트 루트에서):
#   .\script\md-improve\generate-improve-commands.ps1 -PathListFile script\md-improve\non-draft-paths.txt -OutputFile script\md-improve\improve-commands.txt
#   .\script\md-improve\list-non-draft-md.ps1 | .\script\md-improve\generate-improve-commands.ps1 -OutputFile script\md-improve\improve-commands.txt
# -OutputFile 생략 시 터미널에 출력합니다.

param(
    [string]$PathListFile = "",
    [string]$OutputFile = ""
)

$improvePrompt = '이 포스트를 최신 규칙에 맞게 대폭 개선해줘. 살짝 고치는 수준이 아니라, 규칙을 완전히 반영해서 내용과 구조를 크게 보강해줘. 1) 규칙 확인: .cursor/rules의 rules-that-must-be-followed.mdc와 .cursor/skills/blog-post-writing/SKILL.md 및 reference.md(제목·날짜·내부 링크)를 반드시 읽고, 이 포스트가 속한 컬렉션에 해당하는 규칙 파일도 반드시 읽어줘. 특히 content/collection/Movies/ 아래 영화 리뷰인 경우 content/collection/Movies/.cursor/rules/movie-review-writing-rules.mdc를 반드시 읽고 전 항목을 준수해줘. 2) Front matter: tags 50개 이상(영어·한글, data/tags.yaml 참고), description 150자 분량, title 70자 이하, 제목 형식·날짜·lastmod 등 규칙에 맞게 전부 수정해줘. 3) Mermaid: 노드 ID(camelCase/PascalCase, 예약어 금지), 라벨에 특수문자·등호 등 있으면 반드시 큰따옴표로 감싸기, 줄바꿈은 </br> 사용 등 규칙대로 모두 수정해줘. 4) 본문: 컬렉션 규칙에서 요구하는 섹션 구조를 반드시 반영해줘. 영화 리뷰(Movies)인 경우 movie-review-writing-rules.mdc에 따라 개요(영화 정보·추천 대상), 구조 분석(Act 5 도식), 영화 전체 내용(Act 1~5, 장면 비트 [S01][S02]... 연속·미드포인트·클라이맥스 표시), 캐릭터 분석(3명 이상), 영상미와 음악, 종합 평가(장단점·한 줄 평·참고 문헌 3개 이상) 등이 빠지지 않도록 추가·보강하고, 작성 체크리스트를 모두 충족해줘. 문장만 다듬는 수준이 아니라 구조와 분량·품질을 규칙과 우수 포스트 수준까지 끌어올려줘.'

$paths = @()
if ($PathListFile -and (Test-Path $PathListFile)) {
    $paths = Get-Content -Path $PathListFile -Encoding utf8 | Where-Object { $_.Trim() -ne "" }
} else {
    # Read from pipeline (stdin)
    $paths = @($input | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" })
}

$lines = @()
foreach ($p in $paths) {
    $line = "agent -p --force `"@$p`" `"$improvePrompt`""
    $lines += $line
}

$result = $lines -join "`n"
if ($OutputFile) {
    $result | Out-File -FilePath $OutputFile -Encoding utf8
    Write-Host "Wrote $($lines.Count) commands to $OutputFile"
} else {
    $lines | ForEach-Object { Write-Output $_ }
}
