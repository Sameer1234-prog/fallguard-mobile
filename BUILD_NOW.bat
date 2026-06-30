@echo off
echo ============================================
echo Fall Guard APK - Local Build with WSL
echo ============================================
echo.
echo This will build APK locally (faster than GitHub queue!)
echo Build time: 30-40 minutes
echo.
echo Requirements:
echo - WSL Ubuntu installed
echo - 8GB free space
echo - Internet connection
echo.
pause

wsl -- bash -c "cd /mnt/c/Users/Sameer/Downloads/50hz/50hz/mobile_app && bash -c 'pip3 install --user buildozer==1.5.0 cython==0.29.36 && export PATH=\$HOME/.local/bin:\$PATH && buildozer android debug && cp bin/*.apk /mnt/c/Users/Sameer/Desktop/FallGuard_SMS.apk && echo && echo APK ready at: C:\Users\Sameer\Desktop\FallGuard_SMS.apk'"

echo.
echo ============================================
echo Build complete!
echo ============================================
echo.
echo APK location: C:\Users\Sameer\Desktop\FallGuard_SMS.apk
echo.
pause
