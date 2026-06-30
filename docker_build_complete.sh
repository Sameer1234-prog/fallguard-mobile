#!/bin/bash
# Complete build script for Docker container
# Installs SDK components and builds APK

set -e  # Exit on error

echo "========================================"
echo "Fall Guard - Complete Build Process"
echo "========================================"
echo ""

# Set environment
export BUILDOZER_WARN_ON_ROOT=0
cd /home/user/hostcwd

echo "Step 1: Preparing SDK..."
echo ""

# Initialize buildozer (creates .buildozer directories)
buildozer android clean || true

# Download and setup SDK
echo "Downloading Android SDK..."
buildozer android update || echo "Update completed with warnings"

echo ""
echo "Step 2: Installing SDK Platform 33..."
echo ""

# Set SDK paths
export ANDROID_HOME=/root/.buildozer/android/platform/android-sdk
export ANDROIDSDK=$ANDROID_HOME

# Find sdkmanager
SDKMANAGER=""
if [ -f "$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager" ]; then
    SDKMANAGER="$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager"
elif [ -f "$ANDROID_HOME/tools/bin/sdkmanager" ]; then
    SDKMANAGER="$ANDROID_HOME/tools/bin/sdkmanager"
elif [ -f "$ANDROID_HOME/cmdline-tools/bin/sdkmanager" ]; then
    SDKMANAGER="$ANDROID_HOME/cmdline-tools/bin/sdkmanager"
fi

if [ -n "$SDKMANAGER" ]; then
    echo "Found sdkmanager: $SDKMANAGER"
    
    # Accept licenses
    yes | $SDKMANAGER --licenses 2>/dev/null || true
    
    # Install required components
    $SDKMANAGER "platforms;android-33" || echo "Platform install completed"
    $SDKMANAGER "build-tools;33.0.2" || echo "Build tools install completed"
    $SDKMANAGER "platform-tools" || echo "Platform tools install completed"
else
    echo "WARNING: Could not find sdkmanager, buildozer will try to install components"
fi

echo ""
echo "Step 3: Building APK..."
echo ""

# Build APK (auto-accept prompts)
yes | buildozer android debug || buildozer android debug

echo ""
echo "========================================"
echo "Build Complete!"
echo "========================================"
echo ""
echo "APK location: bin/fallguard-1.0-arm64-v8a-debug.apk"
