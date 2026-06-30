[app]

# (str) Title of your application
title = Fall Guard

# (str) Package name
package.name = fallguard

# (str) Package domain
package.domain = org.fallguard

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,otf,json

# Include assets
source.include_patterns = assets/*,assets/fonts/*,assets/icons/*

# (str) Application version
version = 1.0

# Application requirements
requirements = python3,kivy==2.3.0,requests,plyer,urllib3,certifi,charset-normalizer,idna

# Orientation
orientation = portrait

fullscreen = 1

# Android permissions
android.permissions = INTERNET,VIBRATE,RECEIVE_BOOT_COMPLETED,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,SEND_SMS

# Android SDK versions
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.accept_sdk_license = True

# Build architecture
android.archs = arm64-v8a

# APK instead of AAB
android.release_artifact = apk

# Misc
android.allow_backup = True
android.wakelock = False

# Logging
log_level = 2

warn_on_root = 0


[buildozer]

log_level = 2