@echo off
echo ============================================
echo Fall Guard APK - Docker Build (Fixed)
echo ============================================
echo.
echo This will build APK with proper settings
echo Build time: 30-40 minutes
echo.
echo IMPORTANT: Leave this window open!
echo.
pause

cd /d "%~dp0"

echo.
echo Starting Docker build...
echo.

docker run --rm -it -v "%cd%:/home/user/hostcwd" -e USE_SDK_WRAPPER=1 -e GRADLE_OPTS=-Dorg.gradle.jvmargs=-Xmx2048m kivy/buildozer bash -c "export BUILDOZER_WARN_ON_ROOT=0 && cd /home/user/hostcwd && buildozer android debug"

echo.
echo ============================================
echo Build Complete!
echo ============================================
echo.

if exist "bin\*.apk" (
    echo Copying APK to Desktop...
    copy "bin\*.apk" "%USERPROFILE%\Desktop\FallGuard_SMS.apk"
    echo.
    echo ✅ SUCCESS!
    echo APK location: %USERPROFILE%\Desktop\FallGuard_SMS.apk
    echo.
    echo File size:
    dir "%USERPROFILE%\Desktop\FallGuard_SMS.apk"
) else (
    echo ❌ ERROR: APK not found in bin folder!
    echo Check the output above for errors.
)

echo.
pause
