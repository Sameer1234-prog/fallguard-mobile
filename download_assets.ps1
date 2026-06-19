# Fall Guard - Asset Download Script (Windows PowerShell)
# Downloads required fonts for UI redesign

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Fall Guard - Asset Download Script" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Create directories
Write-Host "📁 Creating asset directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "assets\fonts" | Out-Null
Set-Location "assets\fonts"

# Download Inter font
Write-Host ""
Write-Host "📥 Downloading Inter font..." -ForegroundColor Yellow
Invoke-WebRequest -Uri "https://github.com/rsms/inter/releases/download/v3.19/Inter-3.19.zip" -OutFile "Inter-3.19.zip"

Write-Host "📦 Extracting Inter font..." -ForegroundColor Yellow
Expand-Archive -Path "Inter-3.19.zip" -DestinationPath "." -Force
Copy-Item "Inter Desktop\Inter-Regular.ttf" -Destination "."
Copy-Item "Inter Desktop\Inter-Bold.ttf" -Destination "."
Remove-Item "Inter-3.19.zip"
Remove-Item -Recurse -Force "Inter Desktop", "Inter Hinted", "Inter Variable" -ErrorAction SilentlyContinue
Write-Host "✅ Inter font installed" -ForegroundColor Green

# Download Material Design Icons
Write-Host ""
Write-Host "📥 Downloading Material Design Icons font..." -ForegroundColor Yellow
Invoke-WebRequest -Uri "https://github.com/Templarian/MaterialDesign-Webfont/raw/master/fonts/materialdesignicons-webfont.ttf" -OutFile "materialdesignicons-webfont.ttf"
Write-Host "✅ Material Design Icons installed" -ForegroundColor Green

# Verify installation
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "📋 Installation Summary" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Get-ChildItem -Name
Write-Host ""

# Check file sizes
$interRegular = (Get-Item "Inter-Regular.ttf").Length
$interBold = (Get-Item "Inter-Bold.ttf").Length
$mdiFont = (Get-Item "materialdesignicons-webfont.ttf").Length

if ($interRegular -gt 200000 -and $interBold -gt 200000 -and $mdiFont -gt 500000) {
    Write-Host "✅ All fonts downloaded successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 Font sizes:" -ForegroundColor Yellow
    Write-Host "   Inter-Regular.ttf: $([math]::Round($interRegular/1024)) KB"
    Write-Host "   Inter-Bold.ttf: $([math]::Round($interBold/1024)) KB"
    Write-Host "   materialdesignicons-webfont.ttf: $([math]::Round($mdiFont/1024)) KB"
    Write-Host ""
    Write-Host "=========================================" -ForegroundColor Cyan
    Write-Host "🎉 Setup Complete!" -ForegroundColor Green
    Write-Host "=========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Apply changes from QUICK_CHANGES_GUIDE.md"
    Write-Host "2. Update buildozer.spec"
    Write-Host "3. Build: buildozer android debug"
    Write-Host ""
} else {
    Write-Host "❌ Error: Some fonts may not have downloaded correctly" -ForegroundColor Red
    Write-Host "Please check file sizes and try again"
    exit 1
}
