#!/bin/bash
# Fall Guard - Asset Download Script
# Downloads required fonts for UI redesign

set -e

echo "========================================="
echo "Fall Guard - Asset Download Script"
echo "========================================="
echo ""

# Create directories
echo "📁 Creating asset directories..."
mkdir -p assets/fonts
cd assets/fonts

# Download Inter font
echo ""
echo "📥 Downloading Inter font..."
wget -q --show-progress https://github.com/rsms/inter/releases/download/v3.19/Inter-3.19.zip
echo "📦 Extracting Inter font..."
unzip -q Inter-3.19.zip
cp "Inter Desktop/Inter-Regular.ttf" ./
cp "Inter Desktop/Inter-Bold.ttf" ./
rm -rf Inter-3.19.zip "Inter Desktop" "Inter Hinted" "Inter Variable"
echo "✅ Inter font installed"

# Download Material Design Icons
echo ""
echo "📥 Downloading Material Design Icons font..."
wget -q --show-progress https://github.com/Templarian/MaterialDesign-Webfont/raw/master/fonts/materialdesignicons-webfont.ttf
echo "✅ Material Design Icons installed"

# Verify installation
echo ""
echo "========================================="
echo "📋 Installation Summary"
echo "========================================="
ls -lh
echo ""

# Check file sizes
inter_regular=$(stat -f%z Inter-Regular.ttf 2>/dev/null || stat -c%s Inter-Regular.ttf 2>/dev/null)
inter_bold=$(stat -f%z Inter-Bold.ttf 2>/dev/null || stat -c%s Inter-Bold.ttf 2>/dev/null)
mdi_font=$(stat -f%z materialdesignicons-webfont.ttf 2>/dev/null || stat -c%s materialdesignicons-webfont.ttf 2>/dev/null)

if [ "$inter_regular" -gt 200000 ] && [ "$inter_bold" -gt 200000 ] && [ "$mdi_font" -gt 500000 ]; then
    echo "✅ All fonts downloaded successfully!"
    echo ""
    echo "📊 Font sizes:"
    echo "   Inter-Regular.ttf: $(($inter_regular / 1024)) KB"
    echo "   Inter-Bold.ttf: $(($inter_bold / 1024)) KB"
    echo "   materialdesignicons-webfont.ttf: $(($mdi_font / 1024)) KB"
    echo ""
    echo "========================================="
    echo "🎉 Setup Complete!"
    echo "========================================="
    echo ""
    echo "Next steps:"
    echo "1. Apply changes from QUICK_CHANGES_GUIDE.md"
    echo "2. Update buildozer.spec"
    echo "3. Build: buildozer android debug"
    echo ""
else
    echo "❌ Error: Some fonts may not have downloaded correctly"
    echo "Please check file sizes and try again"
    exit 1
fi
