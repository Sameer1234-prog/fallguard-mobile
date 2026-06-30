@echo off
echo ============================================
echo Fall Guard APK - Docker Build
echo ============================================
echo.
echo Docker version detected:
docker --version
echo.
echo Starting build (40-50 minutes)...
echo.
echo Do NOT close this window!
echo.
pause

cd /d "%~dp0"

docker run --rm -v "%cd%:/home/user/hostcwd" kivy/buildozer bash -c "cd /home/user/hostcwd && buildozer android debug"

echo.
echo ============================================
echo Build Complete!
echo ============================================
echo.

if exist "bin\*.apk" (
    echo Copying APK to Desktop...
    copy "bin\*.apk" "%USERPROFILE%\Desktop\FallGuard_SMS.apk"
    echo.
    echo SUCCESS!
    echo APK: %USERPROFILE%\Desktop\FallGuard_SMS.apk
) else (
    echo ERROR: APK not found!
    echo Check output above for errors.
)

echo.
pause
