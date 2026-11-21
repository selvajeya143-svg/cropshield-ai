# CropShield AI — ARM Edge Deployment Guide

This guide provides step-by-step instructions to run CropShield AI **100% offline** on ARM-based hardware targets:
1. **Target 1: Raspberry Pi 5 (4GB / 8GB RAM, Broadcom BCM2712 Quad-core Cortex-A76 @ 2.4GHz)**
2. **Target 2: Android Smartphone (ARM64-v8a / v9a with Snapdragon or MediaTek SoC)**

---

## Target 1: Raspberry Pi 5 Deployment (Debian Linux ARM64)

### 1.1 Prerequisites
- Raspberry Pi 5 with Raspberry Pi OS (64-bit, Debian Bookworm).
- Standard camera (Raspberry Pi Camera Module 3 or USB Webcam).
- Python 3.11+ and Node.js 18+.

### 1.2 System Dependencies Installation
```bash
sudo apt update && sudo apt install -y \
    python3-pip python3-venv git curl \
    libatlas-base-dev libopenblas-dev libjpeg-dev zlib1g-dev \
    v4l-utils

# Clone Repository
git clone https://github.com/your-username/cropshield-ai.git
cd cropshield-ai
```

### 1.3 Python Edge Environment Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt
```

### 1.4 Offline Llama 3.2 1B (LiteRT / llama.cpp / Ollama)
```bash
# Option A: Local Ollama (ARM64)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2:1b

# Option B: Standalone llama-cpp-python (Direct GGUF)
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
```

### 1.5 Run Edge Hardware Benchmark
```bash
python3 scripts/benchmark_arm_edge.py
```

### 1.6 Launch Full Offline System
```bash
# Terminal 1: Backend Server (FastAPI with Sequential Edge Engine)
source venv/bin/activate
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Terminal 2: Offline Web Frontend
node server.mjs
# Application is live at http://localhost:5173 or http://raspberrypi.local:5173
```

---

## Target 2: Android Smartphone Deployment (ARM64-v8a)

CropShield AI features a pre-configured **Capacitor Android wrapper** (`android/`) with offline Progressive Web App (PWA) service worker caching.

### 2.1 Build Android APK
```bash
# 1. Install Node dependencies and build production assets
npm install
npm run build

# 2. Sync web assets into native Android project
npx cap sync android

# 3. Open in Android Studio or build APK directly via Gradle
cd android
./gradlew assembleDebug
```
The compiled debug APK will be generated at:
`android/app/build/outputs/apk/debug/app-debug.apk`

### 2.2 Install on Device via ADB
```bash
adb install -r android/app/build/outputs/apk/debug/app-debug.apk
```

### 2.3 Instant PWA Offline Installation (No Android Studio Needed)
1. Serve the app over local WiFi or USB port forwarding:
   ```bash
   adb reverse tcp:5173 tcp:5173
   ```
2. Open Chrome on the Android phone to `http://localhost:5173`.
3. Tap **Install App** on the browser prompt or Chrome menu.
4. CropShield AI installs as a standalone home-screen app.
5. Turn on **Airplane Mode**. The service worker serves all UI assets and the offline botanical diagnostic model executes directly on device!

---

## Verification of 100% Offline Workflow

To verify that the application makes **zero cloud API calls**:
1. Connect device to your computer via USB.
2. In Android Chrome, open `chrome://inspect/#devices`.
3. Open the Network tab.
4. Capture a crop leaf and run diagnosis.
5. Confirm that:
   - All network requests resolve to `localhost` or cached service worker (`(ServiceWorker)`).
   - Zero outbound requests to external APIs (no Google, no OpenAI, no Groq, no AWS).
   - Inference latency matches ARM benchmark table (~42ms vision, ~1.4s Llama 3.2 1B).
