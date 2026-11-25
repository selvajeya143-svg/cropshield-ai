# Bharat AI-SoC Student Challenge 2026: Final Project Technical Report
## CropShield AI (Kisan Vigyaan): Precision Agronomy System with Sentinel-2 Earth Observation, Cloud-Edge Multimodal Diagnostics & ARM SoC Deployment Roadmap

**Challenge:** Bharat AI-SoC Student Challenge 2026  
**Project Title:** CropShield AI (Kisan Vigyaan)  
**Target Hardware Architecture:** ARM Cortex-A76 @ 2.4GHz (Raspberry Pi 5 / Android ARM64-v8a SoC)  
**Submission Category:** Edge AI & Embedded Systems  
**Report Date:** 25 November 2026  
**Repository:** [https://github.com/selvajeya143-svg/cropshield-ai](https://github.com/selvajeya143-svg/cropshield-ai)  

---

## 1. Executive Summary

Smallholder farmers across rural India face severe annual crop yield losses caused by foliar fungal diseases, bacterial blights, and defoliating insect pests. While advanced deep learning models and large language models (LLMs) offer strong diagnostic capabilities, over 68% of agricultural acreage in India experiences intermittent or absent cellular internet connectivity. 

To address this challenge effectively, **CropShield AI** is architected as an end-to-end precision agronomy platform organized into a **Two-Tier System Framework**:

1. **Tier 1 — Operational Working Prototype (Live Implementation)**:
   - **Earth Observation & Satellite Remote Sensing**: Direct integration with the European Space Agency's **Copernicus Data Space Ecosystem (CDSE)** to ingest real Sentinel-2 Level-2A multispectral imagery, calculating calibrated vegetation indices (**NDVI**, **NDMI**, **NDRE**, **EVI**) and delineating geo-referenced crop stress anomalies.
   - **Cloud-Accelerated Multimodal Diagnosis**: A high-throughput diagnostic engine powered by Groq LPU acceleration (`qwen/qwen3.8-27b` Vision) performing botanical phenotype extraction and iterative disease comparison.
   - **Multilingual Voice Assistant (Chota Kissan)**: Audio transcription via Groq Whisper and conversational agronomic reasoning in regional languages (English, Hindi, Marathi).
   - **Comprehensive Agricultural Knowledge Base**: **176 Wiki entries** covering symptoms, biological vectors, chemical dosages (calibrated per 15L knapsack spray tank), and organic alternatives across **27 major Indian crop categories**.
   - **Deterministic Offline Fallback Advisor**: A zero-dependency local rule-based heuristic engine delivering instantaneous agronomic guidance when internet connectivity is completely lost.
   - **Farmer Direct Marketplace Simulation**: An interactive workflow prototype with `localStorage` persistence and transaction lifecycle management.

2. **Tier 2 — ARM Edge Hardware Porting Roadmap (Phase 2 Planning)**:
   - A rigorous hardware resource budgeting specification designed for standalone low-power deployment on **ARM Cortex-A76** (e.g., Raspberry Pi 5 / Android ARMv8-A SoCs).
   - Establishes concrete hardware budget ceilings: **Peak RAM < 1,200 MB**, **Power Draw < 5.0 Watts**, and **End-to-End Latency < 1.5 seconds**.
   - Outlines the model porting strategy utilizing Post-Training Quantization (INT8 PTQ for vision backbones and 4-bit INT4 quantization for local language models via `llama.cpp` / LiteRT).

---

## 2. Tier 1: Operational Working Prototype

### 2.1 Multispectral Farmland Analysis (Copernicus Sentinel-2)
CropShield AI implements an automated satellite processing pipeline in `backend/services/sentinel_service.py` that connects directly to the Copernicus Data Space Ecosystem:
- **Authentication**: Obtains OAuth2 Bearer tokens from the Copernicus CDSE identity provider.
- **Spectral Band Acquisition**: Requests 11 calibrated Level-2A surface reflectance bands:
  - Optical bands: Blue ($B02$), Green ($B03$), Red ($B04$)
  - Vegetation Red Edge bands: $B05, B06, B07, B8A$
  - Near-Infrared (NIR): $B08$
  - Short-Wave Infrared (SWIR): $B11, B12$
  - Scene Classification Layer ($SCL$)
- **Vegetation Index Computation**:
  - **NDVI (Normalized Difference Vegetation Index)**: Measures overall photosynthetic canopy vigour:
    $$\text{NDVI} = \frac{B08 - B04}{B08 + B04}$$
  - **NDMI (Normalized Difference Moisture Index)**: Gauges crop canopy moisture stress:
    $$\text{NDMI} = \frac{B08 - B11}{B08 + B11}$$
  - **NDRE (Normalized Difference Red Edge)**: Evaluates early-stage nitrogen and chlorophyll dynamics:
    $$\text{NDRE} = \frac{B08 - B05}{B08 + B05}$$
  - **EVI (Enhanced Vegetation Index)**: Mitigates atmospheric and soil background interference:
    $$\text{EVI} = 2.5 \times \frac{B08 - B04}{B08 + 6 \times B04 - 7.5 \times B02 + 1}$$
- **Spatial Stress Clustering**: Applies morphological connected-component labeling on the resulting index rasters to isolate contiguous unhealthy farm parcels, calculating centroid coordinates (latitude/longitude), bounding polygons, and estimated affected acreage.

### 2.2 Cloud-Accelerated Multimodal Diagnosis (Groq LPU)
For scenarios where rural field workers or extension officers have network access, CropShield AI leverages Groq LPU inference for low-latency multimodal reasoning:
- **Vision Pipeline (`qwen/qwen3.8-27b`)**: Analyzes high-resolution leaf photography to extract botanical phenotypes, lesion morphology (chlorotic rings, necrotic borders, water-soaked margins), and visual coloration profiles.
- **Differential Pathology Comparison**: Ranks candidate diseases identified in the local knowledge base against observed symptoms, generating multi-candidate differential diagnoses with clear biological justification.
- **Voice Interaction (`Chota Kissan`)**: Integrates cloud-based Groq Whisper for spoken audio transcription, converting regional voice queries into structured agronomic prompts and streaming actionable chemical and biological guidance.

### 2.3 Comprehensive Agriculture Wiki (176 Wiki Entries)
CropShield AI incorporates an extensive, offline-readable markdown knowledge base structured in `wiki/agriculture/`:
- **176 standalone Wiki entries** spanning 27 crop categories (Rice, Cotton, Tomato, Wheat, Sugarcane, Sorghum, Pearl Millet, Soybean, Groundnut, Vegetables, etc.).
- Each entry documents:
  - Pathogen taxonomy (fungal, bacterial, viral, or deficiency).
  - Characteristic visual symptoms at vegetative, flowering, and maturity stages.
  - Recommended chemical fungicides/insecticides with exact dosages per standard **15-liter knapsack backpack pump**.
  - Eco-friendly biological alternatives (e.g., *Trichoderma viride*, *Pseudomonas fluorescens*, Neem Seed Kernel Extract).
  - Safe application intervals and pre-harvest wait times.

### 2.4 Offline Rule-Based Agronomic Advisor (Local Heuristic Engine)
To maintain operational capability when internet connectivity drops entirely:
- The system includes a zero-dependency Python rule engine (`backend/services/offline_edge_engine.py`) and a client-side JavaScript evaluator (`src/services/visionService.js`).
- Given a selected crop and environmental inputs, the engine performs deterministic taxonomy traversal to identify primary endemic crop diseases and correlated insect pests (e.g., Whitefly vectors for Cotton Leaf Curl; Plant Hoppers for Rice Blast).
- Generates structured spray schedules and tank dosage advisories in under **40 milliseconds** on standard CPU hardware with zero cloud calls.

### 2.5 Interactive Marketplace & Automated Test Verification
- **Farmer Direct Marketplace Simulation**: Built with client-side state persistence (`localStorage`), enabling simulated listings, fair-trade pricing benchmarks, buyer order requests, and transaction lifecycle tracking.
- **Automated Test Suite**: Tested using pytest (`tests/`), with **30 passing unit tests** validating API route integrity, diagnostic schemas, iterative comparison algorithms, and markdown parser correctness.

---

## 3. Tier 2: ARM Edge Hardware Porting Roadmap (Phase 2 Planning)

While the operational prototype demonstrates full-stack software and cloud-hybrid execution, the next phase of the project focuses on porting deep learning inference directly onto dedicated ARM-based System-on-Chip (SoC) hardware.

### 3.1 Hardware Budget Specifications for ARM Cortex-A76
For standalone deployment on an embedded board (e.g., Raspberry Pi 5) or low-cost Android ARMv8-A smartphone without cloud connectivity, CropShield AI defines the following **Projected Target Budget Specifications**:

| Hardware Metric | Projected Budget Ceiling | Rationale & Constraints |
| :--- | :---: | :--- |
| **Peak Pipeline RAM** | **< 1,200 MB** | Ensures reliable operation on devices with 2GB–4GB total system memory without triggering OS Out-Of-Memory (OOM) killers or disk swapping. |
| **Power Consumption** | **< 5.0 Watts** | Enables prolonged battery or solar-panel operation in off-grid field setups without requiring active cooling fans. |
| **Total Pipeline Latency** | **< 1.5 seconds** | Maintains interactive responsiveness for farmers capturing leaf images in the field. |
| **Target Architecture** | **ARM Cortex-A76 @ 2.4 GHz** | Quad-core 64-bit ARMv8.2-A with 128-bit NEON SIMD vector extensions. |

### 3.2 Planned Multi-Stage Sequential Pipeline Architecture
To respect the < 1,200 MB memory ceiling, models cannot run concurrently. The proposed edge architecture uses a sequential execution lifecycle:

```
  ┌─────────────────────────────────────────────────────────────┐
  │                 CAMERA SENSOR CAPTURE                       │
  │            (Mobile Camera or USB/CSI on RPi 5)              │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │  STAGE 1: Vision Disease Classifier (Target: MobileNetV3)   │
  │  • Precision Target: INT8 PTQ (Per-Channel)                 │
  │  • Target Size: ~2.85 MB | Target Latency: < 50 ms          │
  │  • Memory Target: < 100 MB RAM                              │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼ (Free Stage 1 Vision Tensors)
  ┌─────────────────────────────────────────────────────────────┐
  │  STAGE 2: Sequential Pest Classifier (Target: IP102 Model)  │
  │  • Precision Target: INT8 PTQ                               │
  │  • Target Size: ~3.75 MB | Target Latency: < 45 ms          │
  │  • Memory Target: < 80 MB RAM                               │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼ (Explicit Garbage Collection: gc.collect())
  ┌─────────────────────────────────────────────────────────────┐
  │  STRUCTURED SYMBOLIC HANDOFF (~118 Tokens)                  │
  │  {"crop": "Rice", "disease": "Brown Spot", "pest": ...}     │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │  STAGE 3: Structured Advisory LLM (Target: Llama 3.2 1B)    │
  │  • Precision Target: INT4 (Q4_K_M GGUF via llama.cpp)       │
  │  • Target Size: ~745 MB | Target Memory: < 800 MB RAM       │
  │  • Target Output: Concise Tank Dosages (< 1.5s generation)  │
  └─────────────────────────────────────────────────────────────┘
```

### 3.3 Planned Optimization Techniques

#### 1. Token-Efficient Symbolic Handoff Strategy
Directly executing edge multimodal vision-language models (e.g., LLaVA or Qwen-VL) on embedded ARM CPUs introduces severe bottlenecks: visual patch encoders generate 576 to 1,024 image tokens per capture, resulting in multi-second prompt evaluation times and large KV-cache allocations.

Instead, the planned architecture uses a **symbolic handoff**:
1. The lightweight INT8 vision model reduces a $224 \times 224 \times 3$ image into a discrete classification tuple:
   $$\mathcal{T} = (\text{Crop}, \text{Detected Disease}, \text{Severity}, \text{Observed Symptoms}, \text{Pest Vector})$$
2. The classification tuple is injected into a compact, pre-structured 118-token prompt:
```text
<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are an offline edge agronomist running on ARM hardware.
Provide precise, actionable spray tank dosage and bio-control recommendations based STRICTLY on the diagnostic data provided.
Keep recommendations concise (under 120 words). Do not hallucinate.<|eot_id|>
<|start_header_id|>user<|end_header_id|>
[DIAGNOSTIC DATA]
Crop: Rice
Detected Disease: Rice Brown Spot (Bipolaris oryzae)
Severity: Moderate
Symptoms: Oval circular lesions with dark brown centers, Yellow chlorotic halos
Pest: Brown Plant Hopper (Threshold: 5-10 insects/hill)
Language Requested: English

Provide:
1. Primary Chemical Dosage (per 15L backpack pump)
2. Eco-Friendly / Biological Alternative
3. Safe Handling Precaution<|eot_id|>
```
This strategy reduces token consumption from over 1,000 multimodal tokens to approximately 118 text tokens, drastically reducing Time-To-First-Token and memory allocation.

#### 2. Post-Training Quantization (PTQ) Schema
- **Vision Models (MobileNetV3-Small / EfficientNet-B0)**: Target conversion to INT8 per-channel weights and uint8 activations using standard symmetric quantization:
  $$q = \text{round}\left(\frac{x}{S}\right) + Z$$
- **Language Advisory Model (Llama 3.2 1B-Instruct)**: Target quantization using 4-bit medium block-size matrix decomposition ($Q4\_K\_M$) to compress the weight table from ~2.47 GB down to approximately 745 MB, allowing it to fit comfortably within the projected 1,200 MB RAM budget.

---

## 4. Hardware Utilization & Porting Specifications

The hardware deployment plan targets 64-bit ARM architectures prevalent in modern single-board computers and mobile chipsets:

| Hardware Parameter | Raspberry Pi 5 Deployment Target | Android Mobile SoC Target |
| :--- | :--- | :--- |
| **System-on-Chip (SoC)** | Broadcom BCM2712 (16nm FinFET) | Qualcomm Snapdragon / MediaTek Dimensity |
| **CPU Configuration** | Quad-core ARM Cortex-A76 @ 2.4 GHz | Octa-core ARMv8.2-A / ARMv9 (Cortex-A78/A55) |
| **SIMD Extensions** | ARM NEON 128-bit SIMD | ARM NEON + DotProd (8-bit matrix dot product) |
| **Operating System** | Raspberry Pi OS 64-bit (Debian Bookworm) | Android 14 (Linux Kernel 5.15+ / 6.1+) |
| **Target Runtime Engines** | `llama.cpp` (C++) / ONNX Runtime Mobile | LiteRT (TFLite) / ExecuTorch |
| **Projected Peak RAM Budget** | **< 1,200 MB** (Well within 4GB capacity) | **< 1,200 MB** (Well within 6GB–8GB capacity) |
| **Projected Power Envelope** | **< 5.0 Watts** (Passive heat spreader) | **< 4.0 Watts** (Battery operation) |

---

## 5. Software Architecture & Verification Summary

### 5.1 Repository Structure
```
cropshield-ai/
├── backend/
│   ├── main.py                  # FastAPI server with 21 REST endpoints
│   ├── config.py                # Environment and model configurations
│   ├── schemas.py               # Pydantic data validation schemas
│   └── services/
│       ├── sentinel_service.py  # Copernicus Sentinel-2 multispectral pipeline
│       ├── diagnostic_service.py# Multimodal diagnostic and comparison engine
│       ├── offline_edge_engine.py# Deterministic offline rule-based advisor
│       └── wiki_service.py      # Markdown agronomic knowledge parser
├── scripts/
│   ├── benchmark_arm_edge.py    # Local heuristic benchmark and budget profiler
│   ├── quantize_models.py       # PTQ target specification generator
│   ├── generate_pdf_report.py   # Automated PDF report generator
│   └── generate_docx_report.py  # Automated Word document report generator
├── src/                         # React + Vite full-stack frontend application
├── wiki/agriculture/            # 176 agronomic markdown knowledge profiles
├── sentinel2_analysis/          # Sample Sentinel-2 GeoTIFF, NPZ, and analysis maps
└── tests/                       # 30 automated unit tests (all passing)
```

### 5.2 Automated Test Coverage
The automated test suite verifies core backend functionality across 30 unit tests:
- `tests/test_api.py`: Validates health checks, endpoint responses, and request schema compliance.
- `tests/test_diagnostic_service.py`: Validates phenotype extraction, optical fallback logic, and confidence scoring.
- `tests/test_iterative_comparison.py`: Verifies candidate ranking algorithms and differential symptom matching.
- `tests/test_wiki_parser.py` & `tests/test_wiki_service.py`: Verifies markdown extraction, taxonomy resolution, and spray tank dosage parsing across all 176 Wiki entries.

---

## 6. Engineering Tradeoffs & Planned Milestones

| Engineering Area | Current Prototype State | Planned Edge Milestone (Phase 2) |
| :--- | :--- | :--- |
| **Satellite Analysis** | Operational with live Copernicus CDSE API authentication and synthetic spectral fallback. | Integration of temporal NDVI differencing to track multi-week recovery trends post-treatment. |
| **Diagnostic Reasoning** | Operational via cloud Groq LPU (`qwen/qwen3.8-27b`) for high-precision differential diagnosis. | Export of fine-tuned MobileNetV3 to ONNX/LiteRT INT8 for on-device visual disease classification. |
| **Voice Assistant** | Operational via Groq Whisper and cloud Qwen conversational reasoning. | Migration to on-device Whisper.cpp (tiny/base model) for fully offline voice transcription. |
| **Offline Advisory** | Operational zero-dependency rule-based agronomic heuristic engine. | Deployment of quantized Llama 3.2 1B INT4 GGUF via `llama.cpp` using token-efficient structured prompts. |
| **Marketplace** | Functional interactive field simulation with `localStorage` persistence. | Integration with Open Network for Digital Commerce (ONDC) agricultural protocols. |

---

## 7. Submission Checklist & Verification

- [x] **Public Code Repository**: Hosted on GitHub at [https://github.com/selvajeya143-svg/cropshield-ai](https://github.com/selvajeya143-svg/cropshield-ai) under the MIT License.
- [x] **Working Prototype Application**: Production web application (`http://localhost:5173`) and FastAPI backend (`http://localhost:8000`) supporting Copernicus satellite analytics, Groq multimodal reasoning, 176 Wiki entries, and offline rule-based fallback.
- [x] **Demo Video (2 Minutes)**: 1080p 16:9 MP4 presentation demonstrating real Sentinel-2 satellite analysis, Chota Kissan voice assistant, specimen diagnosis, and the offline agronomic advisor.
- [x] **Final Technical Report**: Available in `.pdf` and `.docx` formats, covering methodology, working prototype implementation, hardware target budgeting, and the Phase 2 ARM SoC roadmap.
- [x] **Official Submission Form Link**: [https://forms.gle/3KyscquPFG8rS9ASA](https://forms.gle/3KyscquPFG8rS9ASA) (Deadline: 25 November 2026, 11:59 PM IST).
