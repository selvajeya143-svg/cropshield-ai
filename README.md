# 🌾 CropShield AI (Kisan Vigyaan)
### Precision Agronomy System: Working Satellite & Cloud Hybrid Prototype with ARM Edge Hardware Roadmap

[![Submission: Bharat AI-SoC 2026](https://img.shields.io/badge/Challenge-Bharat%20AI--SoC%202026-orange.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Satellite: Copernicus Sentinel-2](https://img.shields.io/badge/Satellite-Copernicus%20Sentinel--2-blue.svg)](#multispectral-satellite-analysis)
[![Wiki: 176 Entries](https://img.shields.io/badge/Wiki-176%20Entries-green.svg)](wiki/agriculture)
[![Tests: 30 Passed](https://img.shields.io/badge/Tests-30%2F30%20Passing-brightgreen.svg)](tests/)

---

## 📌 Overview

**CropShield AI** is an intelligent agronomic diagnostic and farmland monitoring system built for Indian agriculture. It delivers an operational working prototype featuring real multispectral satellite farmland analytics, cloud-accelerated multimodal diagnosis, an extensive 176-entry agricultural knowledge base, and an offline rule-based fallback advisor, backed by a detailed ARM Edge Hardware deployment roadmap for low-power SoC integration.

---

## 🚀 System Architecture: Two-Tier Framework

### Tier 1: Operational Working Prototype (Live Today)

1. **Multispectral Satellite Farmland Analysis (Sentinel-2)**:
   - Authenticates to the **Copernicus Data Space Ecosystem (CDSE)**.
   - Fetches optical, red-edge, and SWIR spectral bands (`B02, B03, B04, B05, B06, B07, B08, B8A, B11, B12`).
   - Computes real vegetation indices: **NDVI** (Canopy Vigour), **NDMI** (Moisture Stress), **NDRE** (Chlorophyll Activity), and **EVI** (High-Biomass Dynamics).
   - Detects spatial crop stress hotspots with geo-referenced centroid coordinates and surface area bounds.

2. **Cloud-Accelerated Hybrid Diagnostic Engine**:
   - Uses Groq LPU acceleration (`qwen/qwen3.8-27b`) for deep multimodal leaf disease diagnosis and differential reasoning.
   - Computes botanical visual similarity and symptom alignment against reference pathologies.

3. **Multilingual Voice Assistant (Chota Kissan)**:
   - Voice interaction powered by cloud-based Whisper transcription and conversational Qwen reasoning.
   - Delivers localized spray recommendations and tank dosages in English, Hindi, and Marathi.

4. **Comprehensive Agriculture Wiki Knowledge Base**:
   - **176 Wiki entries** covering diseases, symptoms, pathogens, chemical spray dosages (per 15L backpack pump), and organic biocontrols across **27 major Indian crop categories**.

5. **Offline Rule-Based Agronomic Advisor**:
   - Zero-dependency local heuristic engine running directly on the edge client/backend.
   - Provides deterministic emergency agronomic guidance when internet connectivity is completely unavailable.

6. **Farmer Direct Marketplace Simulation**:
   - Interactive field workflow simulation with `localStorage` persistence for fair-trade produce listings, buyer inquiries, and transaction lifecycle tracking.

---

### Tier 2: Edge Hardware Porting Roadmap (Phase 2 Planning)

For deployment in zero-connectivity rural belts on standalone ARM hardware (such as Raspberry Pi 5 / Android ARMv8-A SoCs), CropShield AI establishes projected target resource budgets and architectural specifications:

| Projected Metric | Target Budget Envelope | Technical Strategy |
| :--- | :---: | :--- |
| **Peak RAM Budget** | **< 1,200 MB** | Sequential model execution with explicit memory flushing (`gc.collect()`). |
| **Power Consumption** | **< 5.0 Watts** | Passive cooling envelope suitable for solar/battery field deployment on ARM Cortex-A76. |
| **End-to-End Latency** | **< 1.5 seconds** | Post-Training Quantization (INT8 vision models + 4-bit quantized advisory model). |
| **Vision Model Target** | INT8 PTQ MobileNetV3-Small | Target export to LiteRT / ONNX Runtime Mobile for leaf classification. |
| **Advisory Model Target** | INT4 Llama 3.2 1B-Instruct | Target deployment via `llama.cpp` / LiteRT using structured token-efficient prompts. |

---

## ⚡ Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/selvajeya143-svg/cropshield-ai.git
cd cropshield-ai

# Python Backend Setup
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
# source venv/bin/activate
pip install -r backend/requirements.txt

# Node Frontend Setup
npm install
npm run build
```

### 2. Run Test Suite
```bash
python -m pytest tests/
# Output: 30 passed in ~12s
```

### 3. Run Offline Heuristic Advisor & Target Budget Profiler
```bash
python scripts/benchmark_arm_edge.py
```

### 4. Run Quantization Target Specification Generator
```bash
python scripts/quantize_models.py
```

### 5. Launch Full Application
```bash
# Terminal 1: Backend API (Port 8000)
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Terminal 2: Production Web Frontend (Port 5173)
node server.mjs
# Open browser at: http://localhost:5173
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
