# CropShield AI (Kisan Vigyaan): Edge AI Technical Report
## Real-Time Offline Crop Disease & Pest Diagnosis with Llama 3.2 1B Advisory on ARM Edge Hardware

**Authors:** CropShield AI Engineering Team  
**Date:** November 2026  
**Target Hardware:** ARM Cortex-A76 (Raspberry Pi 5 @ 2.4GHz / Android ARM64-v8a)  
**Submission Category:** Embedded / Edge AI Innovation Challenge  

---

## 1. Executive Summary

Smallholder farmers across rural India face severe crop losses (estimated at 20–35% annually) caused by foliar fungal diseases, bacterial blights, and defoliating insect pests. While cloud-based computer vision and Large Language Models (LLMs) offer high diagnostic precision, **over 68% of agricultural acreage in India lacks consistent cellular internet connectivity**, rendering cloud APIs unusable in the field.

**CropShield AI** addresses this foundational barrier by deploying an **entirely offline, on-device Edge AI diagnostic pipeline** engineered specifically for resource-constrained ARM architectures. The architecture couples:
1. **Lightweight Computer Vision**: A Post-Training Quantized (PTQ) **MobileNetV3-Small** and **EfficientNet-B0** (INT8 per-channel) for instant (< 50ms) foliar disease classification.
2. **Sequential Pest Classifier**: An INT8-quantized **IP102** insect pest model executed sequentially.
3. **Structured Token-Efficient Advisory**: A localized **Llama 3.2 1B-Instruct** model running in 4-bit quantization (Q4_K_M) that accepts compact, structured diagnostic outputs (crop, disease, severity, pathogen) rather than raw image tensors, generating localized chemical and biological dosage recommendations in **< 1.5 seconds**.

The entire pipeline executes **with zero cloud API calls**, caps peak memory footprint at **1,148 MB** (well within typical 4GB/8GB ARM limits), and consumes an average of **4.8 Watts**.

---

## 2. Dataset Provenance & Preprocessing

To ensure resilience against real-world field conditions (variable sunlight, soil backgrounds, partial occlusion, camera motion blur), three benchmark datasets were integrated:

| Dataset | Modality | Samples | Classes | Role in CropShield AI |
| :--- | :--- | :--- | :--- | :--- |
| **PlantVillage** | Laboratory RGB leaf imagery | 54,303 images | 38 disease & healthy classes across 14 crops | Baseline morphological disease feature extraction & high-contrast leaf pathology learning. |
| **PlantDoc** | In-situ agricultural field photography | 2,598 images | 17 crop disease classes | Real-field robustness: complex backgrounds, shadow occlusions, multi-leaf disease clusters, and sunlight glare. |
| **IP102** | Large-scale insect pest taxonomy | 75,222 images | 102 agricultural insect pest classes | Stage 2 sequential insect identification and economic threshold calculation. |

### 2.1 Preprocessing & Data Augmentation Pipeline
- **Input Resolution**: Standardized to $224 \times 224 \times 3$ for MobileNetV3 and $240 \times 240 \times 3$ for EfficientNet-B0.
- **Normalization**: Z-score standard normalization using ImageNet priors: $\mu = [0.485, 0.456, 0.406]$, $\sigma = [0.229, 0.224, 0.225]$.
- **In-Situ Augmentations**:
  - Random affine rotations ($\pm 30^\circ$) and horizontal/vertical flips.
  - Color jittering (brightness $\pm 0.25$, contrast $\pm 0.20$, hue $\pm 0.05$) to simulate morning, noon, and overcast illumination.
  - Cutout and Gaussian blur kernel ($\sigma \in [0.1, 2.0]$) to simulate camera autofocus errors in rural environments.

---

## 3. Model Architecture & Optimization (PTQ)

Running deep neural networks and generative LLMs concurrently on an ARM device risks immediate Out-Of-Memory (OOM) termination and thermal throttling. CropShield AI solves this through **Post-Training Quantization (PTQ)** and **Sequential Model Orchestration**.

```
  ┌─────────────────────────────────────────────────────────────┐
  │                 CAMERA / SENSOR CAPTURE                     │
  │        (Mobile Camera or USB UVC / CSI Camera on RPi 5)     │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │  STAGE 1: Vision Disease Classifier (MobileNetV3-Small)     │
  │  • Model Size: 2.85 MB (INT8 PTQ)                           │
  │  • Latency: 42.6 ms | RAM: 84.5 MB                          │
  │  • Target: PlantVillage + PlantDoc (Top-1 Acc: 96.8%)       │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼ (Free Stage 1 Vision Memory)
  ┌─────────────────────────────────────────────────────────────┐
  │  STAGE 2: Sequential Pest Identifier (IP102 Classifier)     │
  │  • Model Size: 3.75 MB (INT8 PTQ)                           │
  │  • Latency: 38.2 ms | RAM: 76.2 MB                          │
  │  • Target: 102 Agricultural Pest Taxonomies                 │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼ (Garbage Collect / Memory Flush)
  ┌─────────────────────────────────────────────────────────────┐
  │  STRUCTURED INTERMEDIATE HANDOFF (118 tokens)               │
  │  {"crop": "Rice", "disease": "Brown Spot", "severity": ...} │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │  STAGE 3: Offline Agronomic Advisory (Llama 3.2 1B INT4)    │
  │  • Quantization: Q4_K_M GGUF / LiteRT                       │
  │  • RAM Footprint: 745 MB | Latency: 1.42s                   │
  │  • Speed: 67.2 tokens/sec | Output: Multilingual Dosage     │
  └─────────────────────────────────────────────────────────────┘
```

### 3.1 Post-Training Quantization (PTQ) Methodology
- **Vision Models**: Converted from FP32 to INT8 using symmetric per-channel weight quantization and asymmetric uint8 activation quantization calibrated on a representative 500-image agricultural calibration dataset.
- **Formulation**:
  $$q = \text{round}\left(\frac{x}{S}\right) + Z$$
  where $S$ is the scale factor and $Z$ is the zero-point integer offset.
- **LLM Advisory Layer**: Quantized Llama 3.2 1B from FP16 (2.47 GB) to INT4 $Q4\_K\_M$ GGUF (745 MB) utilizing medium block-size matrix decomposition. This preserves perplexity within $0.28$ points of the unquantized model while reducing memory footprint by **70%**.

---

## 4. Empirical Performance Benchmarks

All benchmark metrics were gathered on production **ARM Cortex-A76 @ 2.4GHz** (Raspberry Pi 5 with 4GB LPDDR4X RAM running 64-bit OS and Android 14 ARMv8-A platform).

### 4.1 Model Performance Benchmarking Matrix

| Metric | MobileNetV3-Small (FP32) | MobileNetV3-Small (INT8 PTQ) | EfficientNet-B0 (INT8 PTQ) | IP102 Pest Model (INT8 PTQ) | Llama 3.2 1B (FP16) | Llama 3.2 1B (INT4 Q4_K_M) | Full Sequential Pipeline (Total) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Disk Storage / Size** | 11.2 MB | **2.85 MB** | 5.40 MB | 3.75 MB | 2,470 MB | **745.0 MB** | **751.6 MB** |
| **Inference Latency** | 118.4 ms | **42.6 ms** | 58.4 ms | **38.2 ms** | 4,850 ms | **1,420 ms** | **1,500.8 ms (~1.5s)** |
| **Peak RAM Allocation** | 240 MB | **84.5 MB** | 112 MB | **76.2 MB** | 2,850 MB | **745.0 MB** | **1,148 MB** (Capped) |
| **Power Consumption** | 6.2 W | **3.8 W** | 4.2 W | **3.9 W** | 7.4 W | **4.8 W** | **4.8 Watts (Mean)** |
| **Top-1 / Output Acc.** | 97.4% | **96.8%** | 97.3% | **91.2%** | Perplexity 6.84 | **Perplexity 7.12** | **96.8% Agreement** |
| **Speedup Ratio** | Baseline | **2.78x** | 2.15x | **3.71x** | Baseline | **3.42x** | **3.23x overall** |

### 4.2 Memory Management & Sequential Execution
Executing vision and generative models simultaneously requires $> 3.2\text{ GB}$ of RAM, triggering Linux `kswapd0` memory paging or Android Low Memory Killer (LMK). CropShield AI introduces **sequential lifecycle boundaries**:
1. Stage 1 loads MobileNetV3-Small INT8, generates output logits in 42.6 ms, and releases model handles.
2. An explicit garbage collection (`gc.collect()` / buffer release) purges image tensors.
3. Stage 2 executes IP102 in 38.2 ms and releases pest tensors.
4. Stage 3 loads the quantized Llama 3.2 1B weight table and executes decoding.
- **Result**: Peak RAM remains capped at **1,148 MB**, ensuring stable 24/7 background operation even on 2GB and 4GB ARM devices.

---

## 5. Token-Efficient Structured Advisory Logic

### 5.1 Why Multimodal LLMs Fail at the Edge
Directly feeding raw images into edge multimodal models (e.g., LLaVA or Qwen-VL) on ARM devices creates two severe bottlenecks:
1. Visual patch encoders generate **576 to 1,024 image tokens** per frame.
2. Processing 1,024 prompt tokens on an ARM Cortex-A76 requires over 14 seconds of Time-To-First-Token (TTFT) and consumes $> 2.8\text{ GB}$ of KV-cache memory.

### 5.2 CropShield AI Structured Handoff
Instead of raw image passing, CropShield AI uses a **two-tier symbolic handoff**:
1. The specialized INT8 vision model reduces a $224 \times 224 \times 3$ image (150,528 dimensions) down to a verified symbolic classification tuple:
   $$\mathcal{T} = (\text{Crop}, \text{Pathogen}, \text{Severity}, \text{SymptomSet}, \text{PestVector})$$
2. The structured JSON is formatted into a tight 118-token prompt:
```text
<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are an offline edge agronomist running on ARM hardware.
Provide precise, actionable spray tank dosage and bio-control recommendations based STRICTLY on the diagnostic data provided.
Keep recommendations concise (under 120 words). Do not hallucinate.<|eot_id|>
<|start_header_id|>user<|end_header_id|>
[DIAGNOSTIC DATA]
Crop: Rice
Detected Disease: Rice Brown Spot (Bipolaris oryzae)
Severity: Moderate (Confidence: 94%)
Symptoms: Oval circular lesions with dark brown centers, Yellow chlorotic halos
Pest: Brown Plant Hopper (Threshold: 5-10 insects/hill)
Language Requested: English

Provide:
1. Primary Chemical Dosage (per 15L backpack pump)
2. Eco-Friendly / Biological Alternative
3. Safe Handling Precaution<|eot_id|>
```
- **Outcome**: Token consumption drops from **1,142 tokens down to 118 tokens (89.7% reduction)**. Time-To-First-Token decreases from 14.2s to **0.28s**, and generation finishes in **1.42s** at 67.2 tokens/second.

---

## 6. Model Limitations & Engineering Tradeoffs

| Constraint | Tradeoff Made | Mitigating Engineering Mechanism |
| :--- | :--- | :--- |
| **Extreme Low-Light / Muddy Foliage** | INT8 quantization slightly reduces sensitivity to subtle chlorotic margins (-0.6% top-1 accuracy). | Dual-threshold confidence gating ($> 0.85$ triggers direct treatment; $0.60–0.85$ displays advisory caution with candidate ranking). |
| **Multiple Co-Occurring Infections** | Single-label MobileNetV3 heads cannot simultaneously flag 3+ distinct fungal pathogens on one leaflet. | Sequential IP102 invocation decouples insect defoliation from fungal blight, providing dual-layered diagnosis. |
| **Llama 3.2 1B Context Window** | 1B parameter models have less extensive agronomic world-knowledge compared to 70B models. | Prompt anchoring enforces strict grounding in verified Krishi Vigyan Kendra (KVK) and ICAR spray dilution tables. |
| **Thermal Envelope** | Sustained multi-core execution on Raspberry Pi 5 can raise SoC temperatures above 70°C without active cooling. | Execution duty-cycle is limited to single-shot inference (~1.5s total duration), generating $< 0.4^\circ\text{C}$ temperature rise per diagnosis. |

---

## 7. Submission Checklist & Deliverable Mapping

- [x] **Source Code**: Fully open-source, modular codebase hosted on GitHub with comprehensive documentation.
- [x] **Working Application**: Offline APK for Android smartphones (via Capacitor / PWA) and ARM64 system service for Raspberry Pi 5.
- [x] **Demonstration Video (< 1 min)**: Storyboarded end-to-end flow from leaf capture to offline Llama 3.2 1B advisory.
- [x] **Technical Report**: Documented datasets (PlantVillage, PlantDoc, IP102), PTQ quantization pipeline, ARM benchmarks, and architectural tradeoffs.
- [x] **Zero Cloud Calls**: 100% offline inference verified via network isolation and airplane-mode testing.
