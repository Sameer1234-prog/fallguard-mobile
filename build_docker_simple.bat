@echo off
echo ============================================
echo Fall Guard APK - Docker Build (Simple)
echo ============================================
echo.
echo This uses official Kivy Docker image
echo Build time: 30-40 minutes first time
echo.
echo Requirements:
echo - Docker Desktop installed and running
echo - Internet connection
echo.
pause

cd /d "%~dp0"

echo.
echo Checking Docker...
docker --version
if errorlevel 1 (
    echo.
    echo ERROR: Docker not found!
    echo Please install Docker Desktop from:
    echo https://www.docker.com/products/docker-desktop
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================
echo Building APK with Docker...
echo ============================================
echo.
echo This will:
echo 1. Pull Kivy buildozer Docker image
echo 2. Build APK inside container
echo 3. Copy APK to Desktop
echo.

docker run --rm -v "%cd%:/home/user/hostcwd" kivy/buildozer bash -c "cd /home/user/hostcwd && buildozer android debug && cp bin/*.apk /home/user/hostcwd/"

echo.
echo ============================================
echo Copying to Desktop...
echo ============================================

if exist "bin\*.apk" (
    copy "bin\*.apk" "%USERPROFILE%\Desktop\FallGuard_SMS.apk"
    echo.
    echo ✅ SUCCESS!
    echo APK location: %USERPROFILE%\Desktop\FallGuard_SMS.apk
) else (
    echo.
    echo ❌ ERROR: APK not found!
    echo Check the output above for errors.
)

echo.
pause
