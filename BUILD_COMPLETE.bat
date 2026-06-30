@echo off
REM Fall Guard - Complete Docker Build with SDK Installation

echo ========================================
echo Fall Guard - Complete APK Build
echo ========================================
echo.
echo This will:
echo  1. Install Android SDK Platform 33
echo  2. Build the APK
echo.
echo Total time: 25-35 minutes
echo.
echo Press Ctrl+C to cancel or wait 5 seconds...
timeout /t 5
echo.
echo Starting build...
echo.

docker run --rm -v "%CD%:/home/user/hostcwd" --entrypoint="" kivy/buildozer bash /home/user/hostcwd/docker_build_complete.sh

IF %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Build SUCCESS!
    echo ========================================
    echo.
    echo Copying APK to Desktop...
    IF EXIST bin\*.apk (
        copy bin\*.apk "%USERPROFILE%\Desktop\FallGuard_SMS.apk"
        echo.
        echo ✓ APK copied to: %USERPROFILE%\Desktop\FallGuard_SMS.apk
    ) ELSE (
        echo.
        echo WARNING: APK file not found in bin folder
        echo Check build output above for errors
    )
    echo.
    echo Next Steps:
    echo  1. Copy FallGuard_SMS.apk to Android device
    echo  2. Install APK (enable Unknown sources)
    echo  3. Open app ^> Go to Settings
    echo  4. Set Emergency Contact: +923001234567
    echo  5. Verify Server URL: https://web-production-2755d.up.railway.app
    echo  6. Click Save Settings
    echo  7. Test SMS and Connection
    echo.
) ELSE (
    echo.
    echo ========================================
    echo Build FAILED
    echo ========================================
    echo.
    echo Check error messages above
    echo.
)

pause
