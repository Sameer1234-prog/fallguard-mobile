# Build APK with SMS Functionality

## ✅ App Features Updated:

1. **Editable Server URL** - Change Railway URL from Settings
2. **SMS via SIM** - Direct SMS through Android SmsManager (not WhatsApp)
3. **GPS Location** - Includes Google Maps link in SMS
4. **Test Buttons** - Test SMS and server connection separately
5. **Visual Feedback** - Status messages for all actions

---

## 🚀 Build Methods:

### Method 1: WSL Build (Recommended - Local)

**Requirements:**
- WSL Ubuntu installed on Windows
- Internet connection
- 8GB free disk space
- 30-40 minutes time

**Steps:**
1. Open PowerShell or CMD in this folder
2. Run: `BUILD_APK_NOW.bat`
3. Wait 25-35 minutes for build
4. APK will be copied to: `C:\Users\Sameer\Desktop\FallGuard_SMS.apk`

**OR manually run in WSL:**
```bash
wsl
cd /mnt/c/Users/Sameer/Downloads/50hz/50hz/mobile_app
chmod +x build_apk_wsl.sh
./build_apk_wsl.sh
```

---

### Method 2: GitHub Actions (Online)

**Requirements:**
- GitHub account access
- Internet connection
- 30-40 minutes time

**Steps:**
1. Push code to GitHub (if not already)
2. Go to: https://github.com/Sameer1234-prog/fallguard-mobile/actions
3. Wait for build to complete
4. Download APK from Artifacts section

---

## 📱 App Configuration:

### Default Settings:
```python
base_url = 'https://web-production-2755d.up.railway.app'
emergency_contact = ''  # Set in app Settings
```

### After Installing APK:

1. **First Launch:**
   - App will request permissions
   - Allow: SEND_SMS, LOCATION, INTERNET

2. **Go to Settings:**
   - Set Emergency Contact: `+923001234567`
   - Server URL (editable): `https://web-production-2755d.up.railway.app`
   - Click "Save Settings"

3. **Test Everything:**
   - Click "Test Connection" - Should show "Connected! Model: ..."
   - Click "Test SMS" - Should send test SMS to emergency contact

4. **Return to Home:**
   - Should show "Live" status (green)
   - Monitor real-time fall detection

---

## 📨 SMS Format:

When fall is detected, SMS sent:
```
FALL DETECTED!
Time: 2026-06-19 15:30:45
Prob: 85%
Location: https://maps.google.com/?q=31.5204,74.3587
```

---

## 🔧 App Screens:

### Home Screen:
- Connection status (Live/Offline)
- Fall status (NO FALL / FALL DETECTED)
- Probability percentage
- Confidence level
- Stats: Samples, Falls, Last Update
- Probability bar (visual)
- Recent events log
- Buttons: Settings, Reset, History

### Settings Screen:
- Emergency contact input
- Server URL input (editable!)
- Save Settings button
- Test Connection button
- Test SMS button
- Back button

### History Screen:
- List of all detected falls
- Time and probability for each
- Refresh button
- Back button

---

## 🎯 Testing Checklist:

After installing APK:

- [ ] App opens successfully
- [ ] Permissions granted (SMS, Location, Internet)
- [ ] Set emergency contact in Settings
- [ ] Set/verify server URL in Settings
- [ ] Test SMS button sends SMS
- [ ] Test Connection shows "Connected"
- [ ] Home screen shows "Live" status
- [ ] Trigger fall detection (ESP32 or manually)
- [ ] SMS sent automatically on fall
- [ ] SMS includes GPS coordinates
- [ ] Fall appears in History

---

## 📂 Files:

- `main.py` - App with SMS, editable URL ✅
- `buildozer.spec` - Build configuration ✅
- `build_apk_wsl.sh` - WSL build script ✅
- `BUILD_APK_NOW.bat` - Windows launcher ✅

---

## ⏱️ Build Time Estimate:

**First Build:** 30-40 minutes
- Downloads Android SDK (~500MB)
- Downloads Android NDK (~1GB)
- Compiles Python for Android
- Compiles Kivy and dependencies
- Builds APK

**Subsequent Builds:** 5-10 minutes
- Uses cached SDK/NDK
- Only recompiles changed code

---

## 🆘 Troubleshooting:

**Build fails in WSL:**
- Ensure WSL Ubuntu is installed: `wsl --install`
- Update WSL: `wsl --update`
- Check disk space: `df -h`

**SMS not sending:**
- Check phone number format: `+92xxxxxxxxxx`
- Verify SMS permission granted
- Test with "Test SMS" button first

**Can't connect to server:**
- Verify Railway URL in Settings
- Check internet connection
- Test with "Test Connection" button

**GPS not working:**
- Enable Location services on device
- Grant Location permission to app
- Wait 30 seconds for GPS fix

---

## 🚀 Ready to Build!

Just double-click: **BUILD_APK_NOW.bat**

Or run manually in WSL terminal.

APK will be at: `C:\Users\Sameer\Desktop\FallGuard_SMS.apk`
