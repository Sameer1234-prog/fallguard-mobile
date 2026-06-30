FROM kivy/buildozer:latest

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app/

# Build APK
RUN buildozer android debug

# The APK will be in /app/bin/
