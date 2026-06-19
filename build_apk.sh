#!/bin/bash
# Run this inside WSL: bash build_apk.sh

echo "=========================================="
echo "  Fall Guard APK Builder"
echo "=========================================="

# Install system deps
echo "Installing system dependencies..."
sudo apt update -qq
sudo apt install -y python3-pip git zip unzip openjdk-17-jdk \
    autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
    libffi-dev libssl-dev cmake 2>/dev/null

# Install buildozer
echo "Installing buildozer..."
pip3 install --user --quiet --break-system-packages buildozer cython==0.29.33

# Copy files
echo "Copying app files..."
mkdir -p ~/fallguard
cp /mnt/c/Users/Sameer/Downloads/50hz/50hz/mobile_app/main.py ~/fallguard/
cp /mnt/c/Users/Sameer/Downloads/50hz/50hz/mobile_app/buildozer.spec ~/fallguard/

# Build
echo "Building APK (this takes 30-60 min first time)..."
cd ~/fallguard
~/.local/bin/buildozer android debug 2>&1 | tee build.log

# Copy result
if [ -f bin/fallguard-1.0-debug.apk ]; then
    cp bin/fallguard-1.0-debug.apk /mnt/c/Users/Sameer/Downloads/FallGuard.apk
    echo ""
    echo "=========================================="
    echo "  SUCCESS! APK saved to:"
    echo "  C:\\Users\\Sameer\\Downloads\\FallGuard.apk"
    echo "=========================================="
else
    echo "Build failed. Check build.log for errors."
fi
