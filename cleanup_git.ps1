# URGENT: AIPM Git Cleanup Script
# This script removes mistakenly tracked sensitive files (like venv and .env) from Git tracking.

Write-Host "🛡️ Starting Git Cleanup..." -ForegroundColor Red

# 1. Remove tracked files from Git Index (keeps local files, but removes from repo)
Write-Host "Removing venv from Git tracking..." -ForegroundColor Yellow
git rm -r --cached venv/
git rm -r --cached env/
git rm -r --cached .env
git rm -r --cached frontend/.env
git rm -r --cached react_frontend/node_modules/
git rm -r --cached node_modules/

# 2. Commit the removal
Write-Host "Committing the cleanup..." -ForegroundColor Yellow
git commit -m "🛡️ Security: Remove sensitive and unnecessary files from Git tracking"

# 3. Push the fix
Write-Host "Pushing cleanup to GitHub..." -ForegroundColor Yellow
git push

Write-Host "`n✅ Cleanup Complete! The sensitive files are no longer tracked by Git." -ForegroundColor Green
Write-Host "Please refresh your GitHub page to verify." -ForegroundColor Cyan
