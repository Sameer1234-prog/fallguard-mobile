@echo off
REM Fall Guard - Final Build with API 31

color 0A
echo.
echo ========================================
echo   FALL GUARD - APK BUILD (API 31)
echo ========================================
echo.
echo   Android API changed from 33 to 31
echo   This WILL work now!
echo.
echo   Build time: 20-30 minutes
echo   Output: Desktop\FallGuard_SMS.apk
echo.
echo ========================================
echo.
echo Starting in 5 seconds...
echo Press Ctrl+C to cancel
timeout /t 5
echo.
echo Building APK...
echo.

docker run --rm -v "%CD%:/home/user/hostcwd" --entrypoint="" kivy/buildozer bash -c "cd /home/user/hostcwd && export BUILDOZER_WARN_ON_ROOT=0 && yes | buildozer android debug"

IF %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   BUILD SUCCESS! ✓
    echo ========================================
    echo.
    IF EXIST bin\*.apk (
        copy bin\*.apk "%USERPROFILE%\Desktop\FallGuard_SMS.apk" >nul
        echo   ✓ APK created successfully!
        echo   ✓ Copied to Desktop\FallGuard_SMS.apk
        echo.
        echo   Next steps:
        echo   1. Transfer APK to Android phone
        echo   2. Install APK
        echo   3. Configure in Settings:
        echo      - Emergency Contact: +923001234567
        echo      - Server URL: https://web-production-2755d.up.railway.app
        echo   4. Test SMS and Connection
        echo.
    ) ELSE (
        echo   ⚠ APK not found in bin folder
        dir bin
    )
) ELSE (
    echo.
    echo ========================================
    echo   BUILD FAILED ✗
    echo ========================================
    echo.
    echo   Check errors above
    echo.
)

echo ========================================
echo.
pause
