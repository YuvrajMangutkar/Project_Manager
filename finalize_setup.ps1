# AIPM Frontend Finalization Script
# This script builds the React UI and pushes everything to GitHub for Render deployment.

Write-Host "Starting AIPM UI Finalization..." -ForegroundColor Cyan

# 1. Install React Dependencies
Write-Host "Installing React dependencies..." -ForegroundColor Yellow
cd react_frontend
npm install
if ($LASTEXITCODE -ne 0) { Write-Error "Failed to install npm packages."; exit }

# 2. Build the React Bundle
Write-Host "Building React production bundle..." -ForegroundColor Yellow
npm run build
if ($LASTEXITCODE -ne 0) { Write-Error "Vite build failed."; exit }
cd ..

# 3. Preparation for Git
Write-Host "Committing changes to Git..." -ForegroundColor Yellow
git add .
git commit -m "Upgrade UI to React + Tailwind CSS with Premium Glassmorphism"

# 4. Push to GitHub
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
git push
if ($LASTEXITCODE -ne 0) { 
    Write-Host "Automatic push failed. Please push manually using 'git push'." -ForegroundColor Red
} else {
    Write-Host "Successfully pushed! Render will now start the deployment." -ForegroundColor Green
}

Write-Host ""
Write-Host "UI Upgrade Complete! Visit your site once Render finishes building." -ForegroundColor Cyan
