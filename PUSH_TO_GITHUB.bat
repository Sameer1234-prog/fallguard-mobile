@echo off
REM Push Fall Guard app to GitHub for cloud build

color 0B
cls
echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║        PUSH TO GITHUB - BUILD IN CLOUD                   ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo This will push your code to GitHub where it will build
echo automatically in the cloud - no local space needed!
echo.
echo ═══════════════════════════════════════════════════════════
echo.

REM Check if git is installed
where git >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Git is not installed!
    echo.
    echo Please install Git from: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo [INFO] Git is installed ✓
echo.

REM Get GitHub repository URL from user
set /p REPO_URL="Enter your GitHub repository URL (e.g., https://github.com/username/fallguard-app.git): "

IF "%REPO_URL%"=="" (
    echo.
    echo [ERROR] No repository URL provided!
    echo.
    echo Steps to create a repository:
    echo 1. Go to https://github.com/new
    echo 2. Create a new repository (e.g., "fallguard-app")
    echo 3. Copy the repository URL
    echo 4. Run this script again
    echo.
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════════════════
echo  PUSHING CODE TO GITHUB
echo ═══════════════════════════════════════════════════════════
echo.

REM Initialize git if needed
IF NOT EXIST .git (
    echo [INFO] Initializing git repository...
    git init
    echo.
)

REM Add all files
echo [INFO] Adding files...
git add .
echo.

REM Commit
echo [INFO] Creating commit...
git commit -m "Fall Guard app - SMS + GPS + Editable URL"
echo.

REM Add remote if needed
git remote remove origin 2>nul
echo [INFO] Adding remote repository...
git remote add origin %REPO_URL%
echo.

REM Push to GitHub
echo [INFO] Pushing to GitHub...
echo.
git branch -M main
git push -u origin main

IF %ERRORLEVEL% EQU 0 (
    color 0A
    echo.
    echo ═══════════════════════════════════════════════════════════
    echo  ✓ SUCCESS! CODE PUSHED TO GITHUB
    echo ═══════════════════════════════════════════════════════════
    echo.
    echo Next steps:
    echo.
    echo 1. Go to your repository: %REPO_URL%
    echo 2. Click "Actions" tab
    echo 3. Watch the build progress (30-40 minutes)
    echo 4. When complete, download APK from "Artifacts"
    echo.
    echo The build will start automatically!
    echo.
) ELSE (
    color 0C
    echo.
    echo ═══════════════════════════════════════════════════════════
    echo  ✗ PUSH FAILED
    echo ═══════════════════════════════════════════════════════════
    echo.
    echo Possible issues:
    echo • Authentication required - run: gh auth login
    echo • Repository doesn't exist - create it first
    echo • Wrong URL - check the repository URL
    echo.
    echo For authentication, install GitHub CLI:
    echo https://cli.github.com/
    echo.
    echo Then run: gh auth login
    echo.
)

pause
