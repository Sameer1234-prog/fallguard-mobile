@echo off
REM Fall Guard APK Build - Docker Method
REM This will build the APK using Docker (no WSL needed)

echo ========================================
echo Fall Guard - Docker APK Build
echo ========================================
echo.
echo This will take 20-30 minutes...
echo Press Ctrl+C to cancel or wait 5 seconds to continue...
timeout /t 5
echo.
echo Starting build...
echo.

docker run --rm -v "%CD%:/home/user/hostcwd" --entrypoint="" kivy/buildozer bash -c "cd /home/user/hostcwd && export BUILDOZER_WARN_ON_ROOT=0 && yes | buildozer android debug 2>&1 | tee build.log"

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
