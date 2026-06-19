# FallGuard Mobile App

Fall detection mobile application using accelerometer data and machine learning.

## Features

- Real-time fall detection using device accelerometer
- GPS location tracking
- Automatic SMS alerts to emergency contacts
- Material Design Icons UI
- 2.5-second sliding window analysis
- Cloud-based ML model inference

## Building the APK

### Local Build (Ubuntu/WSL)

```bash
# Install dependencies
sudo apt-get update
sudo apt-get install -y build-essential git zip unzip openjdk-17-jdk

# Create virtual environment
python3 -m venv buildozer-env
source buildozer-env/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install --upgrade cython==0.29.36
pip install --upgrade buildozer

# Build APK
buildozer android debug
```

The APK will be generated in `bin/fallguard-1.0-arm64-v8a-debug.apk`

### GitHub Actions Build

1. Push code to GitHub repository
2. GitHub Actions will automatically build the APK
3. Download the APK from the Actions artifacts
4. Or create a release tag to publish the APK

## Requirements

- Python 3.10
- Kivy 2.1.0
- Plyer (for GPS and SMS)
- Requests (for API calls)

## Configuration

Edit `buildozer.spec` to customize:
- App name and version
- Package name
- Permissions
- Python/Kivy versions
- Android API levels

## Emergency Contacts

Configure emergency contacts in the app settings. When a fall is detected:
1. GPS location is captured
2. SMS is sent automatically to configured contacts
3. Message includes: "Fall detected! Location: [GPS coordinates] [Google Maps link]"

## Permissions Required

- ACCESS_FINE_LOCATION (GPS)
- ACCESS_COARSE_LOCATION (GPS)
- SEND_SMS (Emergency alerts)
- INTERNET (API calls)
- VIBRATE (Feedback)
- WAKE_LOCK (Keep screen on during monitoring)

## License

MIT License
