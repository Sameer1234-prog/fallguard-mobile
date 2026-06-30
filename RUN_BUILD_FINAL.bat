@echo off
echo ============================================
echo Fall Guard APK - Docker Build (FINAL)
echo ============================================
echo.
echo When asked "Are you sure you want to continue [y/n]?"
echo Just press: y
echo Then press: ENTER
echo.
pause

cd /d "%~dp0"

echo.
echo Starting Docker build...
echo.

docker run --rm -it -v "%cd%:/home/user/hostcwd" kivy/buildozer sh /home/user/hostcwd/build_in_docker.sh

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
)

echo.
pause
