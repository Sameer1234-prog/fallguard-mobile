@echo off
REM Fall Guard APK Build - Docker Method with SDK Installation
REM This will install Android SDK components then build the APK

echo ========================================
echo Fall Guard - Docker APK Build
echo Installing SDK Components First
echo ========================================
echo.
echo This will take 25-35 minutes...
echo Press Ctrl+C to cancel or wait 5 seconds to continue...
timeout /t 5
echo.

REM Step 1: Install Android SDK components
echo ========================================
echo STEP 1: Installing Android SDK Platform 33
echo ========================================
echo.

docker run --rm -v "%CD%:/home/user/hostcwd" --entrypoint="" kivy/buildozer bash -c "export BUILDOZER_WARN_ON_ROOT=0 && buildozer android update"

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo SDK installation had warnings, continuing with build...
    echo.
)

REM Step 2: Build APK
echo.
echo ========================================
echo STEP 2: Building APK
echo ========================================
echo.

docker run --rm -v "%CD%:/home/user/hostcwd" --entrypoint="" kivy/buildozer bash -c "cd /home/user/hostcwd && export BUILDOZER_WARN_ON_ROOT=0 && yes | buildozer android debug"

IF %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Build SUCCESS!
    echo ========================================
    echo.
    echo Copying APK to Desktop...
    copy bin\*.apk "%USERPROFILE%\Desktop\FallGuard_SMS.apk"
    echo.
    echo APK Location: %USERPROFILE%\Desktop\FallGuard_SMS.apk
    echo.
    echo Next Steps:
    echo 1. Copy APK to Android device
    echo 2. Install APK (allow Unknown sources)
    echo 3. Open app and configure in Settings:
    echo    - Emergency Contact: +923001234567
    echo    - Server URL: https://web-production-2755d.up.railway.app
    echo 4. Test SMS and Connection buttons
    echo.
) ELSE (
    echo.
    echo ========================================
    echo Build FAILED!
    echo ========================================
    echo.
    echo Check error messages above.
    echo.
)

pause
