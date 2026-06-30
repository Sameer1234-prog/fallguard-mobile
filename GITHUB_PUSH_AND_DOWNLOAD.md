# GitHub Push & APK Download Guide

## 🔐 Step 1: Fix GitHub Login

You need to authenticate with the **Sameer1234-prog** account:

### Option A: Use GitHub Desktop (Easiest)
1. Download GitHub Desktop: https://desktop.github.com
2. Install and login with **Sameer1234-prog** account
3. File → Add Local Repository
4. Select: `C:\Users\Sameer\Downloads\50hz\50hz\mobile_app`
5. Click "Push origin" button
6. Done! ✅

### Option B: Use Git Credential Manager
1. Open PowerShell in this folder
2. Clear old credentials:
   ```powershell
   git credential-manager delete https://github.com
   ```
3. Try push again - will prompt for login:
   ```powershell
   git push origin main
   ```
4. Login with **Sameer1234-prog** in browser
5. Done! ✅

### Option C: Use Personal Access Token
1. Go to: https://github.com/settings/tokens
2. Generate new token (classic)
3. Select scope: **repo** (full control)
4. Copy the token
5. Push with token:
   ```powershell
   git push https://YOUR_TOKEN@github.com/Sameer1234-prog/fallguard-mobile.git main
   ```

---

## 📤 Step 2: What Happens After Push

Once you successfully push to GitHub:

### Automatic Build Starts:
1. **GitHub Actions** detects new code
2. **Build runner** starts (Ubuntu VM)
3. **Downloads** Android SDK, NDK, dependencies
4. **Compiles** app with Buildozer
5. **Creates** APK file
6. **Uploads** APK as artifact

**Build Time:** ~30-40 minutes (sometimes faster with cache)

---

## 📥 Step 3: Download APK from GitHub

### Watch the Build:
1. Go to: **https://github.com/Sameer1234-prog/fallguard-mobile/actions**
2. You'll see "Build Android APK" workflow running
3. Status shows:
   - 🟡 Yellow/Orange = Building (in progress)
   - ✅ Green = Success (completed)
   - ❌ Red = Failed (error)

### When Build is Green (Success):

1. **Click** on the completed workflow run
   - Shows green checkmark ✅
   - Has timestamp when it completed

2. **Scroll down** to "Artifacts" section
   - Located at bottom of the page
   - Shows "fallguard-apk" with file size

3. **Click "fallguard-apk"** to download
   - Downloads as ZIP file
   - Name: `fallguard-apk.zip`

4. **Extract ZIP file**
   - Right-click → Extract All
   - Inside you'll find: `fallguard-1.0-arm64-v8a-debug.apk`

5. **Done!** Copy APK to your Android device

---

## 📱 Step 4: Install APK on Android

### Transfer to Phone:
- **USB Cable:** Copy to phone storage
- **Cloud:** Upload to Drive/Dropbox, download on phone
- **Email:** Send to yourself, download on phone
- **WhatsApp:** Send to yourself, download

### Install:
1. Open APK file on phone
2. Allow "Install from Unknown Sources" if prompted
3. Click "Install"
4. Wait for installation
5. Open app

### First Launch - Grant Permissions:
- ✅ **SEND_SMS** - For emergency alerts
- ✅ **ACCESS_FINE_LOCATION** - For GPS in SMS
- ✅ **INTERNET** - To connect to Railway

---

## ⚙️ Step 5: Configure App

### Open App → Settings:

1. **Emergency Contact:**
   - Enter: `+923001234567`
   - Format must include `+` and country code

2. **Server URL:**
   - Default: `https://web-production-2755d.up.railway.app`
   - You can edit if you have different URL

3. **Click "Save Settings"**

4. **Test Connection:**
   - Click "Test Connection" button
   - Should show: "Connected! Model: Gradient Boosting (95%)"

5. **Test SMS:**
   - Click "Test SMS" button
   - Should receive test message on emergency contact

6. **Return to Home:**
   - Should show "Live" status (green)
   - Ready to detect falls!

---

## 📊 How GitHub Actions Works

### Workflow File:
Location: `.github/workflows/android-build.yml`

### What it does:
```yaml
1. Checkout code from GitHub
2. Setup Python 3.10
3. Cache buildozer files (faster rebuilds)
4. Install system dependencies
5. Install buildozer and cython
6. Accept Android SDK licenses
7. Build APK with buildozer
8. Upload APK as artifact
```

### Build Logs:
You can view detailed logs:
1. Go to Actions page
2. Click on running/completed workflow
3. Click "build" job
4. Expand each step to see output

---

## 📦 APK Details

### What You'll Get:

**File Name:** `fallguard-1.0-arm64-v8a-debug.apk`

**Size:** ~20-30 MB

**Architecture:** ARM64-v8a (works on most modern Android phones)

**Android Version:** Requires Android 5.0+ (API 21+)

**Features:**
- ✅ SMS via SIM (not WhatsApp)
- ✅ GPS location in messages
- ✅ Editable Railway URL
- ✅ Live fall detection
- ✅ Fall history
- ✅ Test buttons

---

## 🔍 Troubleshooting

### Push Failed - Permission Denied:
```
Error: Permission denied to Sameer1234-prog/fallguard-mobile.git
```
**Solution:** Use GitHub Desktop or regenerate credentials (see Step 1)

### Build Failed on GitHub:
1. Check the workflow logs
2. Look for red ❌ error messages
3. Common issues:
   - Python version mismatch
   - Missing dependencies
   - Buildozer configuration error

### Can't Find Artifacts:
- Artifacts only appear AFTER build succeeds ✅
- Check workflow is green/completed
- Scroll to bottom of workflow run page

### APK Won't Install:
- Enable "Unknown sources" in Android settings
- Check you downloaded .apk not .zip
- Try different installation method

### App Crashes on Open:
- Check all permissions granted
- Check Android version (need 5.0+)
- Check phone architecture (need ARM64)

---

## ✅ Quick Checklist

Before pushing to GitHub:
- [ ] Code updated with SMS functionality
- [ ] Railway URL configured
- [ ] buildozer.spec has correct settings
- [ ] .github/workflows/android-build.yml exists

After pushing:
- [ ] Go to GitHub Actions page
- [ ] Watch build progress (30-40 min)
- [ ] Build completes successfully ✅
- [ ] Download APK from Artifacts
- [ ] Extract ZIP file
- [ ] Copy APK to phone

After installing:
- [ ] Grant all permissions
- [ ] Set emergency contact in Settings
- [ ] Set/verify server URL in Settings
- [ ] Test connection (should be green)
- [ ] Test SMS (should receive message)
- [ ] Return home (should show "Live")
- [ ] Ready to use!

---

## 🚀 Current Files Ready to Push:

✅ `main.py` - SMS + Editable URL + Visual feedback  
✅ `buildozer.spec` - Python 3.10, Kivy 2.3.0, API 33  
✅ `.github/workflows/android-build.yml` - Auto-build config with cache  

**Everything is ready!** Just push to GitHub and wait for build.

---

## 📞 Need Help?

**GitHub Actions URL:**
https://github.com/Sameer1234-prog/fallguard-mobile/actions

**Repository URL:**
https://github.com/Sameer1234-prog/fallguard-mobile

**Railway URL:**
https://web-production-2755d.up.railway.app

---

## Summary - 3 Steps:

1. **Push to GitHub** (use GitHub Desktop or fix credentials)
2. **Wait 30-40 minutes** for automatic build
3. **Download APK** from Artifacts section

That's it! The app will build automatically in the cloud. 🎉
