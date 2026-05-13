# Multimodal BCI: Real-Time Motor Imagery Decoding with EEG & Blink Analysis (Python)

This project implements a **real-time Brain-Computer Interface (BCI) pipeline** using EEG data to classify motor imagery EEG signals (kinesthetic motor imagery by imagining grasping with either their left or right hand, involving all fingers), integrating:
- Motor Imagery (MI) decoding
- Eye-blink (EOG) artefact analysis
- CSP-based feature extraction
- Sliding-window real-time simulation

## Dataset Background

This work is based on the following dataset:

[Guttmann-Flury, E., Sheng, X. & Zhu, X. Dataset combining EEG, eye-tracking, and high-speed video for ocular activity analysis across BCI paradigms. Sci Data 12, 587 (2025).](https://arxiv.org/pdf/2506.07488)

The dataset is available online [here](https://www.synapse.org/Synapse:syn64005218/wiki/630018)

According to the above pape, the dataset used in this project was originally designed to study the physiology of eye blinks and their effect on EEG signals. 

During data acquisition, multiple modalities were recorded simultaneously, including:
- EEG (brain activity)
- Eye movements (EOG)
- Eyelid motion (EMG-based blink signals)

This multimodal setup enables analysis of how blink-related artefacts influence EEG recordings.

## How This Project Uses the Dataset?

While the original study focuses on modelling blink physiology, this project takes a different perspective; It investigates how blink artefacts affect **motor imagery (MI) classification in BCI systems**

Key questions explored:
- How much do blinks degrade classification accuracy?
- Can removing blink-contaminated epochs improve performance?
- How does this impact real-time decoding?
---

## Key Features

- EEG + EOG multimodal processing
- Motor imagery classification (Left vs Right)
- Real-time sliding window decoding
- Common Spatial Pattern (CSP) feature extraction
- Latency benchmarking
- Blink artefact impact analysis
  
---
## Design Choices

- **Decoded Channels**: Based on the original paper, the following electrodes are excluded from analysis, as they were identified as either malfunctioning or exhibiting bridging effects: PO3, F1, POZ, OZ, F3, O2, P8, PO7, FC3, P7, and P4
- In the real-time stage, a sliding window with a window size of 1.0 s and a step size of 0.25 s is chosen  

---

## Load EEG motor imagery data

- Download the dataset from [here](https://www.synapse.org/Synapse:syn64005218/wiki/630018)

- Start by loading motor imagery-based EEG recording of one of the subjects. `S01/Sess01/Neuroscan/MI011.csv ` is chosen here.

## Offline Pipeline Overview
In this stage, trial-level offline evaluation is performed. One feature vector is extracted per MI trial.

Run: ` run_offline_pipeline.py `

### Feature Extraction
- Common Spatial Pattern (CSP)

### Classification
- Binary (Left vs Right motor imagery)

### Artefact Impact

| Dataset        | Accuracy |
|---------------|--------|
| All epochs    | 83.3% |
| Clean epochs  | 87.5% |

### EEG + HEO + Blink Timeline
- Dual-axis plot showing:
  - EEG (C3)
  - Eye movement (HEO)
  - Blink markers
  - Motor imagery cues
 ![Dual-axis plot](results/eeg_heo_blink_cue_timeline_dual_axis.png)


## Real-Time Pipeline Overview

In this stage, window-level real-time simulation is performed. Each trial is divided into overlapping 1-second windows.

Run: ` run_realtime_simulation.py `

### Real-Time Simulation



### Offline Performance
- CSP Accuracy: **73.7%**
- Balanced precision/recall across classes

---

### Real-Time Simulation

### Real-Time Predictions
- Sliding-window predictions vs ground truth
 ![realtime_predictions](results/realtime_predictions.png)

### Latency Analysis
- Processing time per window (sub-millisecond performance)
 ![latency_over_time](results/latency_over_time.png)

- Accuracy: **75.4%**
- Mean latency: **0.33 ms**
- Max latency: **2.34 ms**

This demonstrates real-time feasibility
