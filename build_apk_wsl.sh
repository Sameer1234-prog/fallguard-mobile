#!/bin/bash
set -e

echo "========================================="
echo "Fall Guard APK Builder - WSL"
echo "========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "main.py" ] || [ ! -f "buildozer.spec" ]; then
    echo "Error: main.py or buildozer.spec not found!"
    echo "Please run this script from the mobile_app directory"
    exit 1
fi

echo "Step 1: Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "Installing Python..."
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv
fi
python3 --version

echo ""
echo "Step 2: Installing system dependencies..."
sudo apt install -y git zip unzip openjdk-17-jdk \
    autoconf libtool pkg-config zlib1g-dev libncurses-dev \
    cmake libffi-dev libssl-dev

echo ""
echo "Step 3: Checking Buildozer installation..."
if ! command -v buildozer &> /dev/null; then
    echo "Installing Buildozer..."
    pip3 install --user buildozer==1.5.0 cython==0.29.36
    export PATH=$PATH:~/.local/bin
fi
buildozer version

echo ""
echo "Step 4: Cleaning old builds..."
rm -rf .buildozer/android/platform/build-arm64-v8a/build
rm -rf .buildozer/android/platform/build-arm64-v8a/dists
rm -f bin/*.apk

echo ""
echo "Step 5: Building APK (this will take 25-35 minutes)..."
echo "Building in debug mode..."
buildozer android debug

echo ""
echo "========================================="
echo "Build Complete!"
echo "========================================="
echo ""

# Find the APK
APK_FILE=$(find bin -name "*.apk" 2>/dev/null | head -n 1)

if [ -n "$APK_FILE" ]; then
    APK_SIZE=$(du -h "$APK_FILE" | cut -f1)
    echo "APK created: $APK_FILE"
    echo "Size: $APK_SIZE"
    echo ""
    echo "Copying to Desktop..."
    cp "$APK_FILE" "/mnt/c/Users/Sameer/Desktop/FallGuard_SMS.apk"
    echo "Copied to: C:\Users\Sameer\Desktop\FallGuard_SMS.apk"
else
    echo "Error: APK file not found!"
    echo "Check the build log above for errors."
    exit 1
fi

echo ""
echo "========================================="
echo "Next Steps:"
echo "========================================="
echo "1. Copy APK to your Android device"
echo "2. Install the APK"
echo "3. Grant SMS and Location permissions"
echo "4. Open app and go to Settings"
echo "5. Set emergency contact number"
echo "6. Set server URL (default is Railway)"
echo "7. Test SMS and connection"
echo "8. Ready to use!"
echo ""
