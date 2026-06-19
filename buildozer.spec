[app]
title           = Fall Guard
package.name    = fallguard
package.domain  = org.fallguard
source.dir      = .
source.include_exts = py,png,jpg,kv,atlas,ttf,otf
source.include_patterns = assets/*,assets/fonts/*,assets/icons/*
version         = 1.0

# Dependencies
requirements    = python3,kivy==2.3.0,requests,plyer,urllib3,certifi,charset-normalizer,idna,pyjnius

# Orientation and display
orientation     = portrait
fullscreen       = 1
android.wakelock = False

# Screen density support
android.meta_data = android.max_aspect=2.1

# Android settings
android.permissions = INTERNET,VIBRATE,RECEIVE_BOOT_COMPLETED,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,SEND_SMS
android.api         = 33
android.accept_sdk_license = True
android.minapi      = 21
android.ndk         = 25b
android.ndk_api     = 21
android.archs       = arm64-v8a

# Build settings
android.allow_backup = True
android.release_artifact = apk
log_level = 2
warn_on_root = 1

[buildozer]
log_level = 2
