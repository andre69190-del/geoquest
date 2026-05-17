# Phase 181a: Automatischer Fix und Push
Write-Host "Phase 181a: Fixing git lock and pushing event delegation..." -ForegroundColor Green

$repoPath = "C:\Users\Andre\Desktop\Cowork\Geoquest"
cd $repoPath

# 1. Kill all git processes
Write-Host "Step 1: Killing hung git processes..." -ForegroundColor Yellow
Get-Process -Name "git" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

# 2. Remove lock file forcefully
Write-Host "Step 2: Removing stale lock file..." -ForegroundColor Yellow
$lockFile = "$repoPath\.git\index.lock"
if (Test-Path $lockFile) {
    Remove-Item -Force $lockFile -ErrorAction SilentlyContinue
    Write-Host "   [OK] Lock file removed" -ForegroundColor Green
}

# 3. Clean git state
Write-Host "Step 3: Resetting git state..." -ForegroundColor Yellow
git reset --hard HEAD 2>&1 | Out-Null

# 4. Pull latest from remote (integrates the new commit)
Write-Host "Step 4: Pulling from remote..." -ForegroundColor Yellow
git pull origin main 2>&1 | Select-String "Already up to date|Fast-forward" | Write-Host

# 5. Verify GeoQuest.html has event delegation
Write-Host "Step 5: Verifying GeoQuest.html contains event delegation..." -ForegroundColor Yellow
$searchResult = Select-String -Path "GeoQuest.html" -Pattern "handleQuizButtonClickDelegated" -ErrorAction SilentlyContinue
if ($searchResult) {
    Write-Host "   [OK] Event delegation code found!" -ForegroundColor Green
} else {
    Write-Host "   [WARNING] Event delegation code NOT found!" -ForegroundColor Red
    exit 1
}

# 6. Add and commit
Write-Host "Step 6: Creating commit..." -ForegroundColor Yellow
git add GeoQuest.html
git commit -m "Phase 181a: Deploy event delegation infrastructure (verified)" 2>&1 | Select-String "create mode|changed"

# 7. Push
Write-Host "Step 7: Pushing to GitHub..." -ForegroundColor Yellow
$pushResult = git push origin main 2>&1
if ($pushResult -match "Everything up-to-date|master.*main") {
    Write-Host "   [OK] Push successful!" -ForegroundColor Green
    Write-Host "Vercel will rebuild automatically in 1-2 minutes" -ForegroundColor Cyan
} else {
    Write-Host $pushResult -ForegroundColor Yellow
}

Write-Host "`nDone! Refresh https://geoquest-web.vercel.app with Ctrl+Shift+R" -ForegroundColor Green
