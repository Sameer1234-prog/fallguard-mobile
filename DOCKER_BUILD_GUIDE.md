# Docker Build Guide - Build APK in Container

## 🐳 Why Docker?

✅ **No Python issues** - Pre-configured environment  
✅ **Clean build** - Isolated from your system  
✅ **Faster than GitHub queue** - Builds immediately  
✅ **Repeatable** - Same result every time  

---

## 📋 Prerequisites

### Step 1: Install Docker Desktop

1. **Download:** https://www.docker.com/products/docker-desktop
2. **Install** Docker Desktop for Windows
3. **Start** Docker Desktop
4. **Wait** for Docker to fully start (whale icon in system tray)

### Step 2: Verify Docker Works

Open PowerShell and run:
```powershell
docker --version
```

Should show: `Docker version 24.x.x` or similar

---

## 🚀 Build APK with Docker

### Method 1: Double-Click (Easiest)

Just double-click:
```
build_docker_simple.bat
```

That's it! The script will:
1. Pull Kivy buildozer Docker image (~2GB)
2. Build APK inside container
3. Copy APK to Desktop

**Time:**
- First time: ~40-50 minutes (downloads image + builds)
- Next times: ~30 minutes (uses cached image)

---

### Method 2: PowerShell Commands

Open PowerShell in the `mobile_app` folder:

```powershell
# Build APK with Docker
docker run --rm -v "${PWD}:/home/user/hostcwd" kivy/buildozer bash -c "cd /home/user/hostcwd && buildozer android debug"

# Copy APK to Desktop
copy bin\*.apk $env:USERPROFILE\Desktop\FallGuard_SMS.apk
```

---

## 📊 What Happens During Build

```
1. Docker pulls kivy/buildozer image (first time only)
   → ~2GB download
   
2. Container starts with your code mounted
   → Your mobile_app folder is accessible inside

3. Buildozer builds APK
   → Downloads Android SDK
   → Downloads Android NDK
   → Compiles Python for Android
   → Compiles Kivy
   → Builds your app
   → Creates APK

4. APK is saved to bin/ folder
   → Accessible from Windows

5. Script copies APK to Desktop
   → Ready to install!
```

---

## 🎯 Advantages Over Other Methods

| Method | Queue Time | Build Time | Issues |
|--------|-----------|------------|--------|
| **Docker** | 0 min ✅ | 30-40 min | None! |
| GitHub Actions | 15-60 min ❌ | 30-40 min | Long queue |
| WSL | 0 min ✅ | 30-40 min | Python 3.12 errors |

**Docker = Best Choice!** ⭐

---

## 📁 Files Created

After successful build:

```
mobile_app/
├── bin/
│   └── fallguard-1.0-arm64-v8a-debug.apk  ← Your APK!
├── .buildozer/  ← Build cache (reused next time)
└── build.log  ← Build output
```

**Desktop:**
```
C:\Users\Sameer\Desktop\FallGuard_SMS.apk  ← Ready to install!
```

---

## 🔄 Rebuild After Changes

If you change code and want to rebuild:

```powershell
# Just run the command again!
docker run --rm -v "${PWD}:/home/user/hostcwd" kivy/buildozer bash -c "cd /home/user/hostcwd && buildozer android debug"
```

It will be **faster** (5-10 minutes) because:
- Docker image already downloaded
- Android SDK/NDK cached
- Only recompiles changed code

---

## 🆘 Troubleshooting

### Docker not installed:
```
'docker' is not recognized as internal or external command
```
**Solution:** Install Docker Desktop from https://www.docker.com/products/docker-desktop

### Docker not running:
```
error during connect: This error may indicate that the docker daemon is not running
```
**Solution:** Start Docker Desktop application

### Out of disk space:
```
no space left on device
```
**Solution:** Free up at least 10GB disk space

### Port already in use:
This shouldn't happen with buildozer, but if you see port errors, restart Docker Desktop.

### Build fails - check logs:
```powershell
# View detailed build log
type build.log
```

---

## 💡 Tips

### Speed Up Builds:
1. **Keep .buildozer folder** - Contains cached SDK/NDK
2. **Don't delete Docker images** - Reused for next build
3. **Use SSD** - Faster than HDD
4. **Close other apps** - Free up RAM

### Clean Build (if issues):
```powershell
# Remove build cache
Remove-Item -Recurse -Force .buildozer

# Remove Docker cache
docker system prune -a

# Build again
docker run --rm -v "${PWD}:/home/user/hostcwd" kivy/buildozer bash -c "cd /home/user/hostcwd && buildozer android debug"
```

---

## 📱 After Building

### 1. Install APK:
- Copy `FallGuard_SMS.apk` to phone
- Open APK file
- Allow "Unknown sources"
- Install

### 2. Configure App:
- Open app
- Grant permissions (SMS, Location, Internet)
- Go to Settings
- Set emergency contact: `+923001234567`
- Set server URL: `https://web-production-2755d.up.railway.app`
- Save settings

### 3. Test:
- Click "Test Connection" → Should show "Connected!"
- Click "Test SMS" → Should receive test message
- Return to Home → Should show "Live" status

---

## ✅ Complete Docker Build Commands

### Quick Build:
```powershell
docker run --rm -v "${PWD}:/home/user/hostcwd" kivy/buildozer bash -c "cd /home/user/hostcwd && buildozer android debug && cp bin/*.apk /home/user/hostcwd/"
```

### With Progress Output:
```powershell
docker run --rm -it -v "${PWD}:/home/user/hostcwd" kivy/buildozer bash -c "cd /home/user/hostcwd && buildozer -v android debug"
```

### Save Build Log:
```powershell
docker run --rm -v "${PWD}:/home/user/hostcwd" kivy/buildozer bash -c "cd /home/user/hostcwd && buildozer android debug 2>&1 | tee build.log"
```

---

## 🎯 Summary

**Simplest way to build APK:**

1. **Install Docker Desktop**
2. **Double-click:** `build_docker_simple.bat`
3. **Wait 40 minutes**
4. **Get APK** on Desktop
5. **Done!** ✅

No Python issues, no environment problems, just works! 🐳

---

## 📞 App Features (In This Build)

✅ SMS via SIM (not WhatsApp)  
✅ Editable Railway URL in Settings  
✅ GPS location in messages  
✅ Test Connection button  
✅ Test SMS button  
✅ Live fall detection  
✅ Fall history  
✅ Visual feedback  

**Default URL:** `https://web-production-2755d.up.railway.app`

---

**Ready to build?** Just run: `build_docker_simple.bat` 🚀
