#!/bin/bash
# Install Android SDK Platform 33 and Build Tools

echo "Installing Android SDK components..."

# Set environment variables
export ANDROID_HOME=/root/.buildozer/android/platform/android-sdk
export ANDROIDSDK=$ANDROID_HOME
export PATH=$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$PATH

# Create cmdline-tools directory structure
mkdir -p $ANDROID_HOME/cmdline-tools/latest
cd $ANDROID_HOME/cmdline-tools

# Move tools to correct location if needed
if [ -d "tools" ]; then
    mv tools/* latest/ 2>/dev/null || true
fi

# Accept licenses
yes | $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --licenses 2>/dev/null || true

# Install required SDK components
echo "Installing platform-tools..."
$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager "platform-tools"

echo "Installing platforms;android-33..."
$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager "platforms;android-33"

echo "Installing build-tools;33.0.2..."
$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager "build-tools;33.0.2"

echo "SDK installation complete!"
