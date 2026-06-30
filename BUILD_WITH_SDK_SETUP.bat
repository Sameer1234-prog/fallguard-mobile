@echo off
REM Fall Guard - Build with proper SDK installation

color 0A
cls
echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║        FALL GUARD - BUILD WITH SDK AUTO-INSTALL          ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo  Changes:
echo  • API 31 → API 27 (Android 8.1, more compatible)
echo  • Auto-accept SDK licenses
echo  • Buildozer will auto-install platform-27
echo.
echo  Build Time: 25-35 minutes
echo  Output: Desktop\FallGuard_SMS.apk
echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo Starting in 5 seconds... (Press Ctrl+C to cancel)
timeout /t 5 >nul
echo.
echo [INFO] Starting Docker build...
echo [INFO] Buildozer will auto-install Android Platform 27...
echo [INFO] This may take 25-35 minutes...
echo.

docker run --rm -v "%CD%:/home/user/hostcwd" --entrypoint="" kivy/buildozer bash -c "cd /home/user/hostcwd && export BUILDOZER_WARN_ON_ROOT=0 && export ANDROID_SDK_LICENSE_ACCEPTED=yes && yes | buildozer -v android debug"

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
        echo ✓ APK: %USERPROFILE%\Desktop\FallGuard_SMS.apk
        echo.
        echo ═══════════════════════════════════════════════════════════
        echo  INSTALL ^& CONFIGURE:
        echo ═══════════════════════════════════════════════════════════
        echo.
        echo  1. Transfer APK to Android phone
        echo  2. Install (enable Unknown sources)
        echo  3. Open app ^> Settings
        echo  4. Emergency Contact: +923001234567
        echo  5. Server URL: https://web-production-2755d.up.railway.app
        echo  6. Save ^> Test SMS ^> Test Connection
        echo.
    ) ELSE (
        echo ⚠ APK not found in bin folder
    )
) ELSE (
    color 0C
    echo ═══════════════════════════════════════════════════════════
    echo.
    echo   ✗✗✗ BUILD FAILED ✗✗✗
    echo.
    echo ═══════════════════════════════════════════════════════════
    echo.
    echo [ERROR] Build failed. Check errors above.
    echo.
)

echo.
pause
