@echo off
REM Fall Guard - FINAL Build (All Issues Fixed)

color 0A
cls
echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║         FALL GUARD - FINAL BUILD (ALL FIXED!)            ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo  Fixed Issues:
echo  ✓ Root warning error
echo  ✓ API 33 unavailable (changed to API 31)
echo  ✓ Python version mismatch (removed version pin)
echo  ✓ Docker entrypoint
echo  ✓ Auto-accept prompts
echo.
echo  Build Time: 20-30 minutes
echo  Output: Desktop\FallGuard_SMS.apk
echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo Starting in 5 seconds... (Press Ctrl+C to cancel)
timeout /t 5 >nul
echo.
echo [INFO] Starting Docker build...
echo [INFO] This may take 20-30 minutes...
echo.

docker run --rm -v "%CD%:/home/user/hostcwd" --entrypoint="" kivy/buildozer bash -c "cd /home/user/hostcwd && export BUILDOZER_WARN_ON_ROOT=0 && yes | buildozer android debug"

echo.
IF %ERRORLEVEL% EQU 0 (
    color 0A
    echo ═══════════════════════════════════════════════════════════
    echo.
    echo   ✓✓✓ BUILD SUCCESS! ✓✓✓
    echo.
    echo ═══════════════════════════════════════════════════════════
    echo.
    IF EXIST bin\*.apk (
        echo [INFO] Copying APK to Desktop...
        copy bin\*.apk "%USERPROFILE%\Desktop\FallGuard_SMS.apk" >nul 2>&1
        echo.
        echo ✓ APK Location: %USERPROFILE%\Desktop\FallGuard_SMS.apk
        echo.
        echo ═══════════════════════════════════════════════════════════
        echo  NEXT STEPS:
        echo ═══════════════════════════════════════════════════════════
        echo.
        echo  1. Transfer FallGuard_SMS.apk to Android phone
        echo  2. Install APK (enable Unknown sources)
        echo  3. Open app ^> Settings tab
        echo  4. Configure:
        echo     • Emergency Contact: +923001234567
        echo     • Server URL: https://web-production-2755d.up.railway.app
        echo  5. Click "Save Settings"
        echo  6. Click "Test SMS" (should receive test message)
        echo  7. Click "Test Connection" (should show Connected!)
        echo  8. Go to Home tab - ready to detect falls!
        echo.
        echo ═══════════════════════════════════════════════════════════
        echo  APP FEATURES:
        echo ═══════════════════════════════════════════════════════════
        echo.
        echo  ✓ SMS via SIM card (not WhatsApp)
        echo  ✓ GPS location with Google Maps link
        echo  ✓ Editable Railway server URL
        echo  ✓ Test SMS and Connection buttons
        echo  ✓ Live fall detection
        echo  ✓ Fall history screen
        echo.
        echo ═══════════════════════════════════════════════════════════
        echo.
    ) ELSE (
        color 0C
        echo ⚠ WARNING: APK file not found in bin folder
        echo.
        echo Check if there were any build errors above.
        echo.
    )
) ELSE (
    color 0C
    echo ═══════════════════════════════════════════════════════════
    echo.
    echo   ✗✗✗ BUILD FAILED ✗✗✗
    echo.
    echo ═══════════════════════════════════════════════════════════
    echo.
    echo [ERROR] Build failed with error code: %ERRORLEVEL%
    echo.
    echo Please check the error messages above.
    echo.
    echo Common issues:
    echo  • Docker not running - Open Docker Desktop
    echo  • Insufficient disk space - Need 8GB free
    echo  • Network issues - Check internet connection
    echo.
)

echo.
pause
