# MicroArch Branch Predictor

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

> A professional-grade microarchitecture simulation toolkit for analyzing branch prediction logic (GShare, Perceptron).

## Overview

In the domain of Computer Architecture and High-Performance Computing (HPC), cycle-accurate behavior and pipeline efficiency are paramount. This suite implements low-level branch prediction logic found in modern processor pipelines. It allows for rigorous sensitivity analysis of predictor accuracy against varying workload phases (Training, Inference, I/O).

Key features:
-   **Advanced Predictors**: Implementations of GShare, Perceptron, Bimodal, and static predictors.
-   **Domain-Specific Analysis**: specialized datasets for differing workload characteristics.
-   **Extensible Architecture**: Modular design allows easy addition of new predictors (e.g., TAGE, SRNN).

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/Vikramansen/HPC_Branch_Predeiction_Suite.git
cd HPC_Branch_Predeiction_Suite
```

### Usage

The simulator uses a unified CLI `micro_sim.py`.

**1. Generate Instruction Traces**
Create synthetic branch signal traces:
```bash
python micro_sim.py generate --output-dir data
```

**2. Run Micro-Architecture Simulation**
Evaluate branch predictor logic:
```bash
python micro_sim.py compare
```

**Options**:
-   `--history-bits N`: Set history length for GShare/Perceptron (default: 8).
-   `--datasets [FILE...]`: Compare on custom CSV files.

## 📊 Supported Predictors

| Predictor | Type | Description |
|-----------|------|-------------|
| **Always Taken** | Static | Simple baseline predicting all branches taken. |
| **Never Taken** | Static | Simple baseline predicting all branches not taken. |
| **Bimodal** | Dynamic | Uses 2-bit saturating counters per address. |
| **GShare** | Dynamic | Uses global history XORed with address. |
| **Perceptron** | Neural | Single-layer neural network for linearly separable paths. |

## 📚 Research & Citation

This project accompanies the research on **"Branch Prediction with Neural Networks"**.
If you use this suite in your research, please cite

A copy of the paper is available in [docs/HPC_Branch_Prediction_Suite_Paper.pdf](docs/HPC_Branch_Prediction_Suite_Paper.pdf).

## 🔮 Future Roadmap

-   **TAGE Predictor**: Implementation of the Tagged Geometric History Length predictor.
-   **SRNN Integration**: Integrating Sliced Recurrent Neural Networks for handling non-linear histories.
-   **Gem5 Simulation**: Porting logic to the Gem5 architectural simulator.

## 🤝 Contributing

Contributions are welcome!

## 📄 License

This project is licensed under the MIT License

## Authors

-   **Vikraman Senthil Kumar** 
-   **Madhumitha Santhanakrishnan**
