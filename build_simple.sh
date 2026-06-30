#!/bin/bash
set -e

echo "========================================="
echo "Fall Guard APK Builder - Simple Version"
echo "========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "main.py" ] || [ ! -f "buildozer.spec" ]; then
    echo "Error: main.py or buildozer.spec not found!"
    exit 1
fi

echo "Installing Buildozer with --break-system-packages..."
pip3 install --user buildozer==1.5.0 cython==0.29.36 --break-system-packages
export PATH=$PATH:~/.local/bin

echo ""
echo "========================================="
echo "Starting APK Build"
echo "========================================="
echo "This will take 25-35 minutes on first build..."
echo ""

# Build APK
buildozer android debug 2>&1 | tee build.log

echo ""
echo "========================================="
echo "Build Complete!"
echo "========================================="

# Find and copy APK
APK_FILE=$(find bin -name "*.apk" 2>/dev/null | head -n 1)

if [ -n "$APK_FILE" ]; then
    echo "APK: $APK_FILE"
    echo "Copying to Desktop..."
    cp "$APK_FILE" "/mnt/c/Users/Sameer/Desktop/FallGuard_SMS.apk"
    echo ""
    echo "✅ Success!"
    echo "APK location: C:\Users\Sameer\Desktop\FallGuard_SMS.apk"
    echo ""
else
    echo "❌ APK not found. Check build.log for errors."
fi
