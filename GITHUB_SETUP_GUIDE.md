# GitHub Setup Guide - FallGuard Mobile App

This guide will help you push your FallGuard mobile app to GitHub and build the APK automatically using GitHub Actions.

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `fallguard-mobile` (or any name you prefer)
3. Description: `Fall detection mobile app with SMS alerts and Material Design UI`
4. Choose **Public** or **Private**
5. **DO NOT** initialize with README, .gitignore, or license (we already have them)
6. Click **Create repository**

## Step 2: Push Code to GitHub

Open WSL terminal and run these commands:

```bash
cd ~/mobile_app

# Configure git (if not done already)
git config user.email "your-email@example.com"
git config user.name "Your Name"

# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/fallguard-mobile.git

# Push code
git branch -M main
git push -u origin main
```

### Alternative: Push to existing repository

If you already have a repository:

```bash
cd ~/mobile_app
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main --force
```

## Step 3: GitHub Actions Will Build Automatically

Once you push, GitHub Actions will:
1. Automatically detect the `.github/workflows/build-apk.yml` file
2. Start building your APK (takes ~15-20 minutes)
3. Store the APK as an artifact

## Step 4: Download Your APK

### Method 1: From Actions Tab
1. Go to your repository on GitHub
2. Click the **Actions** tab
3. Click on the latest workflow run
4. Scroll down to **Artifacts** section
5. Download `fallguard-apk.zip`
6. Extract the ZIP to get your APK file

### Method 2: From Releases (if you create a tag)
```bash
cd ~/mobile_app
git tag v1.0.0
git push origin v1.0.0
```
The APK will be attached to the release at `https://github.com/YOUR_USERNAME/fallguard-mobile/releases`

## Step 5: Install APK on Android Device

1. Transfer the APK to your Android phone
2. Open the file manager and tap the APK
3. Allow "Install from unknown sources" if prompted
4. Install and test!

## Troubleshooting

### Build fails in GitHub Actions
- Check the Actions tab for error logs
- Most common issues:
  - Buildozer.spec configuration errors
  - Missing dependencies (already handled in workflow)
  - Python version conflicts (workflow uses Python 3.10)

### Git push fails with "remote: Permission denied"
```bash
# Use personal access token instead of password
# Generate token at: https://github.com/settings/tokens
# When prompted for password, paste your token
```

### "Repository not found" error
- Check the URL is correct
- Ensure you have access to the repository
- Try HTTPS instead of SSH

## File Structure in Repository

```
fallguard-mobile/
├── .github/
│   └── workflows/
│       └── build-apk.yml      # GitHub Actions workflow
├── assets/
│   └── fonts/                 # Material Design Icons + Inter fonts
├── main.py                    # Main app code with SMS + icons
├── buildozer.spec             # Build configuration
├── .gitignore                 # Ignore build files
├── README.md                  # Project documentation
└── GITHUB_SETUP_GUIDE.md      # This file
```

## What's Different in GitHub Build vs Local Build

**Advantages:**
- ✅ Clean environment (no cache conflicts)
- ✅ Reproducible builds
- ✅ No local setup required
- ✅ Build logs saved for debugging
- ✅ APK stored in artifacts/releases

**GitHub Actions Configuration:**
- Python 3.10
- Kivy 2.1.0
- Android API 31
- NDK r25b
- Java 17

## Updating Your App

To build a new version:

```bash
cd ~/mobile_app

# Make your changes to main.py or buildozer.spec

# Commit changes
git add .
git commit -m "Your change description"

# Push to trigger new build
git push
```

GitHub Actions will automatically build the new version.

## Questions?

- GitHub Actions logs: Check the Actions tab in your repository
- Build time: Typically 15-20 minutes
- Artifact retention: 30 days (configurable in workflow)
- Cost: Free for public repositories, limited minutes for private repos
