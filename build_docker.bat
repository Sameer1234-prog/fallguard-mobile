@echo off
echo ============================================
echo Fall Guard APK - Docker Build
echo ============================================
echo.
echo This uses Docker to build APK (no Python issues!)
echo Build time: 30-40 minutes
echo.
echo Requirements:
echo - Docker Desktop installed and running
echo - 10GB free space
echo.
pause

cd /d "%~dp0"

echo.
echo Step 1: Building Docker image...
docker build -t fallguard-builder .

echo.
echo Step 2: Building APK inside Docker...
docker run --rm -v "%cd%:/home/user/hostapp" fallguard-builder bash -c "cp -r /app/. /home/user/hostapp/ && cd /home/user/hostapp && buildozer android debug"

echo.
echo Step 3: Copying APK to Desktop...
copy bin\*.apk "%USERPROFILE%\Desktop\FallGuard_SMS.apk"

echo.
echo ============================================
echo Build Complete!
echo ============================================
echo.
echo APK location: %USERPROFILE%\Desktop\FallGuard_SMS.apk
echo.
pause
