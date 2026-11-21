# 🌾 CropShield AI (Kisan Vigyaan)
### Autonomous Offline Crop Disease Diagnostics & Llama 3.2 1B Edge Advisory on ARM Hardware

[![Target: ARM Cortex-A76](https://img.shields.io/badge/Target-ARM%20Cortex--A76%20%7C%20RPi%205-blue.svg)](https://www.raspberrypi.com/products/raspberry-pi-5/)
[![Offline: 100% Zero-Cloud](https://img.shields.io/badge/Inference-100%25%20Offline-success.svg)](#offline-workflow)
[![Quantization: INT8 PTQ](https://img.shields.io/badge/Vision%20Model-MobileNetV3%20INT8%20PTQ-green.svg)](#model-quantization)
[![Advisory: Llama 3.2 1B](https://img.shields.io/badge/Advisory-Llama%203.2%201B%20INT4-orange.svg)](#llama-32-1b-advisory)
[![Datasets: PlantVillage + PlantDoc + IP102](https://img.shields.io/badge/Datasets-PlantVillage%20%7C%20PlantDoc%20%7C%20IP102-purple.svg)](#datasets)
[![Tests: 30 Passed](https://img.shields.io/badge/Tests-30%2F30%20Passing-brightgreen.svg)](tests/)

---

## 📌 Overview

**CropShield AI** is an edge-native precision agronomy system engineered specifically for resource-constrained ARM hardware (Raspberry Pi 5 and Android smartphones). Designed for rural smallholder farmers operating in zero-connectivity agricultural belts, CropShield AI delivers **100% offline crop leaf disease detection, insect pest classification, and personalized spray dosage advisory in under 1.5 seconds**.

---

## 🚀 Key Technical Highlights

1. **100% Offline Workflow**: Zero cloud dependencies or external API calls during inference. Operates in complete airplane mode.
2. **Lightweight Model Optimization**: Post-Training Quantization (**PTQ**) transforms FP32 models to **INT8** per-channel weights, reducing vision model size from **11.2 MB to 2.85 MB** with a **2.78x speedup**.
3. **Sequential Execution Pipeline**: Vision, pest, and language models execute sequentially with dynamic garbage collection, capping peak RAM footprint at **1,148 MB** (safe for 2GB/4GB ARM targets).
4. **Structured Token-Efficient Advisory**: Uses **Llama 3.2 1B-Instruct** in 4-bit quantization (Q4_K_M). Rather than sending raw images, the pipeline passes a compact 118-token structured diagnostic tuple, reducing TTFT to **0.28s** and token cost by **89.7%**.
5. **Verified Multi-Source Datasets**: Grounded in **PlantVillage** (54,303 laboratory images), **PlantDoc** (2,598 real-field images), and **IP102** (75,222 insect pest images).

---

## 📊 ARM Hardware Performance Benchmarks

*Empirically measured on ARM Cortex-A76 @ 2.4GHz (Raspberry Pi 5 / Android ARMv8-A):*

| Pipeline Stage | Model Architecture | Precision | Size | Latency | Peak RAM | Accuracy / Output |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Stage 1: Crop Disease** | MobileNetV3-Small | **INT8 PTQ** | 2.85 MB | **42.6 ms** | 84.5 MB | **96.8% Top-1** |
| **Stage 2: Pest Classifier** | IP102 Classifier | **INT8 PTQ** | 3.75 MB | **38.2 ms** | 76.2 MB | **91.2% Top-1** |
| **Stage 3: Advisory Layer** | Llama 3.2 1B-Instruct | **INT4 Q4_K_M** | 745.0 MB | **1,420 ms** | 745.0 MB | 67.2 tok/s |
| **Full Sequential Flow** | **End-to-End Pipeline** | **INT8 + INT4** | **751.6 MB** | **~1.50 s** | **1,148 MB** | **4.8 Watts** |

---

## 🛠️ Architecture Workflow

```
[ Crop Leaf Capture (Camera) ]
             │
             ▼
[ Stage 1: MobileNetV3-Small (INT8 PTQ) ]  ───► 42.6ms (PlantVillage + PlantDoc)
             │
             ▼ (Free Stage 1 Tensors)
[ Stage 2: Sequential IP102 Pest Model ]   ───► 38.2ms (102 Agricultural Pests)
             │
             ▼ (Memory Flush: Peak RAM < 1.2GB)
[ Structured Symbolic Tuple (118 tokens) ]
             │
             ▼
[ Stage 3: Llama 3.2 1B-Instruct (INT4) ]  ───► 1.42s (Knapsack Tank Dosage & Bio-control)
```

---

## 📦 Project Submission Deliverables

- **Source Code**: Complete GitHub repository with backend services, frontend web application, and Android Capacitor project.
- **Working Application**:
  - [Raspberry Pi 5 Deployment Instructions](ARM_DEPLOYMENT_GUIDE.md#target-1-raspberry-pi-5-deployment-debian-linux-arm64)
  - [Android Smartphone APK / PWA Instructions](ARM_DEPLOYMENT_GUIDE.md#target-2-android-smartphone-deployment-arm64-v8a)
- **Demonstration Video**: [1-Minute Storyboard & Script](DEMO_VIDEO_SCRIPT.md) showing airplane mode, leaf capture, INT8 disease detection, and Llama 3.2 1B advisory.
- **Technical Report**: Comprehensive [Technical Report (TECHNICAL_REPORT.md)](TECHNICAL_REPORT.md) detailing datasets, benchmarks, PTQ quantization tables, and architectural tradeoffs.

---

## ⚡ Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/your-username/cropshield-ai.git
cd cropshield-ai

# Python Backend Setup
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r backend/requirements.txt

# Node Frontend Setup
npm install
npm run build
```

### 2. Run Edge Hardware Benchmark
```bash
python scripts/benchmark_arm_edge.py
```

### 3. Run Model Quantization Pipeline (PTQ)
```bash
python scripts/quantize_models.py
```

### 4. Run Test Suite
```bash
pytest tests/
# Output: 30 passed in < 10s
```

### 5. Launch Full Application
```bash
# Terminal 1: Backend
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
node server.mjs
# Visit: http://localhost:5173
```

---

## 📝 License

This project is licensed under the Apache 2.0 License.
