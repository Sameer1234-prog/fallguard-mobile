@echo off
REM Clean up disk space for Android build

color 0E
cls
echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║          DISK SPACE CLEANUP - FREE UP 8-10 GB            ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo ERROR: No space left on device
echo.
echo Docker needs 8-10GB free space to build the APK.
echo This script will clean up Docker caches and old data.
echo.
echo ═══════════════════════════════════════════════════════════
echo.
pause

echo.
echo [1/5] Checking current disk space...
echo.
wmic logicaldisk get caption,freespace,size

echo.
echo [2/5] Stopping Docker containers...
docker stop $(docker ps -aq) 2>nul

echo.
echo [3/5] Removing old Docker containers...
docker container prune -f

echo.
echo [4/5] Removing unused Docker images...
docker image prune -a -f

echo.
echo [5/5] Cleaning Docker system (caches, volumes)...
docker system prune -a --volumes -f

echo.
echo ═══════════════════════════════════════════════════════════
echo  CLEANUP COMPLETE!
echo ═══════════════════════════════════════════════════════════
echo.
echo [INFO] Checking disk space after cleanup...
echo.
wmic logicaldisk get caption,freespace,size

echo.
echo ═══════════════════════════════════════════════════════════
echo  ADDITIONAL CLEANUP OPTIONS:
echo ═══════════════════════════════════════════════════════════
echo.
echo If you still need more space:
echo.
echo 1. Delete Windows Temp files:
echo    - Open: C:\Windows\Temp
echo    - Delete all files
echo.
echo 2. Empty Recycle Bin
echo.
echo 3. Run Disk Cleanup:
echo    - Search "Disk Cleanup" in Start menu
echo    - Clean System files
echo.
echo 4. Delete old downloads:
echo    - Check Downloads folder
echo    - Delete large files you don't need
echo.
echo 5. Uninstall unused programs:
echo    - Settings ^> Apps ^> Installed apps
echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo After freeing space, run: BUILD_WITH_SDK_SETUP.bat
echo.
pause
