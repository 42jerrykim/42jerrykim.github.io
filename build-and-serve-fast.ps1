Write-Host "Hugo 개발 서버를 시작합니다..." -ForegroundColor Cyan

# Hugo 개발 서버 시작 (live reload 활성화)
hugo serve -D -F --port 12345 --disableKinds term,home --openBrowser --logLevel=info --bind 0.0.0.0
#hugo serve -D -F --port 12345 --disableKinds section,term,home --openBrowser --logLevel=debug --bind 0.0.0.0
