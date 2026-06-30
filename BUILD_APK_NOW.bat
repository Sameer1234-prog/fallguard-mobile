@echo off
echo ========================================
echo Fall Guard APK Builder
echo ========================================
echo.
echo This will build the APK using WSL Ubuntu.
echo Build time: 25-35 minutes (first time)
echo.
pause

cd /d "%~dp0"

echo.
echo Starting WSL build...
echo.

wsl -- bash -c "cd /mnt/c/Users/Sameer/Downloads/50hz/50hz/mobile_app && chmod +x build_apk_wsl.sh && ./build_apk_wsl.sh"

echo.
echo ========================================
echo Build process finished!
echo ========================================
echo.
echo Check above for APK location.
echo If successful, APK is at: C:\Users\Sameer\Desktop\FallGuard_SMS.apk
echo.
pause
