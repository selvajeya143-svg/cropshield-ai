# CropShield AI — 1-Minute Demonstration Video Storyboard & Script

**Video Title:** CropShield AI: 100% Offline Edge Crop Diagnostics with Llama 3.2 1B on ARM  
**Target Duration:** 58 Seconds (< 1 Minute Limit)  
**Target Hardware:** Raspberry Pi 5 / Android Smartphone (ARM-based)  
**Submission Requirement:** Complete end-to-end workflow: crop image capture -> offline vision diagnosis -> offline Llama 3.2 1B advisory recommendations.

---

## Storyboard & Timing Breakdown

| Timecode | Visual Scene / Screen Action | On-Screen Text Overlay | Spoken Narration (English / Hindi) | Technical Demonstration Proof |
| :---: | :--- | :--- | :--- | :--- |
| **0:00 – 0:08** | **Device Setup & Network Isolation:** Close-up of Android phone / Raspberry Pi 5 running CropShield AI. The user swipes down the notification shade and turns on **Airplane Mode** (WiFi OFF, Mobile Data OFF). | `100% Offline ARM Edge Target` `Airplane Mode Active` `Zero Cloud APIs` | *"This is CropShield AI running entirely offline on an ARM-based target with zero internet connectivity."* | Shows active airplane mode icon; network status badge in app confirms `Offline Mode`. |
| **0:08 – 0:20** | **Crop Leaf Capture:** Farmer points smartphone camera (or Raspberry Pi camera) at a diseased rice leaf exhibiting Brown Spot lesions. Farmer taps the green **Scan Leaf** button. | `Image Capture` `Live Crop Foliage: Rice` | *"A farmer captures an image of a diseased crop leaf directly in the field."* | Live camera viewfinder captures high-resolution crop frame; autofocus locks on leaf blade. |
| **0:20 – 0:34** | **Stage 1 & 2: Quantized Vision Inference:** Screen displays on-device inference progress. The INT8 MobileNetV3-Small model detects disease in **42 milliseconds**, followed by the sequential IP102 pest classifier. | `MobileNetV3-Small (INT8 PTQ)` `Latency: 42.6 ms \| RAM: 84 MB` `Dataset: PlantVillage + PlantDoc` | *"In just 42 milliseconds, our quantized MobileNetV3 model detects Rice Brown Spot with 96.8% accuracy, followed by sequential insect pest screening."* | Latency counter shows `42.6ms`; diagnosis badge updates to `Rice Brown Spot (Bipolaris oryzae) - Moderate Severity`. |
| **0:34 – 0:50** | **Stage 3: Offline Llama 3.2 1B Advisory:** The structured diagnosis tuple is handed off to on-device **Llama 3.2 1B-Instruct (INT4)**. Recommendations stream smoothly on screen in local language (Marathi/Hindi/English). | `Llama 3.2 1B-Instruct (INT4 Q4_K_M)` `RAM Capped: 1,148 MB` `Structured Token-Efficient Handoff` | *"Next, the structured diagnosis passes to our offline Llama 3.2 1B assistant, delivering exact knapsack sprayer tank dosages and organic bio-controls in the farmer's native language."* | Text displays: `Mancozeb 75% WP @ 37.5g per 15L tank + Pseudomonas fluorescens bio-spray`; multilingual audio reads aloud. |
| **0:50 – 0:58** | **Summary & GitHub Repository Callout:** Split screen showing the full offline diagnostic card with exact spray tank dilution, power draw (4.8W), and GitHub repository URL. | `CropShield AI` `Ready for ARM Deployment` `GitHub: [Repo Link]` | *"CropShield AI: Empowering smallholder farmers with private, real-time edge intelligence. Available on GitHub."* | Clean closing card displaying GitHub repo URL, benchmarks summary, and submission form title. |

---

## Audio / Narration Transcript

> *"This is CropShield AI running entirely offline on an ARM-based target with zero internet connectivity. A farmer captures an image of a diseased crop leaf directly in the field. In just 42 milliseconds, our quantized MobileNetV3 model detects Rice Brown Spot with 96.8% accuracy, followed by sequential insect pest screening. Next, the structured diagnosis passes to our offline Llama 3.2 1B assistant, delivering exact knapsack sprayer tank dosages and organic bio-controls in the farmer's native language. CropShield AI: Empowering smallholder farmers with private, real-time edge intelligence. Available on GitHub."*

**Total Word Count:** 94 words (comfortably delivered in 54 seconds at natural speaking pace).

---

## Video Production Tips for User
1. **Screen Recording / Over-the-Shoulder Camera**: Use a second phone or desk tripod to record the ARM device screen to clearly prove Airplane Mode is enabled.
2. **Lighting**: Ensure daylight or clean LED lighting so the leaf specimen and on-screen text are crisp.
3. **Audio Quality**: Record the voiceover using a lavalier or headset mic for clear audio.
4. **Resolution**: Export at 1080p (1920x1080) at 30fps or 60fps, MP4 format under 50MB.
