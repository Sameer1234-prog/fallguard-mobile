#!/bin/bash
# Build script to run inside Docker container
cd /home/user/hostcwd
export BUILDOZER_WARN_ON_ROOT=0
buildozer android debug
