# HPC Branch Prediction Analysis Suite

## Overview

In the realm of High-Performance Computing (HPC), where every cycle counts, the Branch Predictor Analysis Suite emerges as a cutting-edge toolset, crucial for optimizing processor efficiency. This advanced project is ingeniously crafted to delve into the intricacies of branch prediction strategies, a cornerstone in modern CPU design. It encompasses a suite of sophisticated scripts, meticulously designed for generating comprehensive branch prediction datasets and for conducting an in-depth comparative analysis of various state-of-the-art predictors. This includes, but is not limited to, Always Taken, Never Taken, Bimodal, GShare, and Perceptron predictors. The suite stands as an invaluable asset for HPC enthusiasts, researchers, and professionals, offering insights that drive the next generation of processor performance enhancements.

## Features

- **Robust Error Handling**: Comprehensive error checking and validation
- **Flexible Configuration**: Command-line arguments for all parameters
- **Multiple Dataset Types**: ML-based, I/O-heavy, and general application datasets
- **Advanced Predictors**: Implementation of 5 different prediction algorithms
- **Configurable Parameters**: Adjustable history bits and predictor settings
- **Professional Output**: Formatted tables and clear status messages
- **Type-Safe**: Python type hints for better code quality

## Prerequisites

- Python 3.6 or higher
- No external dependencies required (uses only Python standard library)

## Installation

```bash
git clone https://github.com/Vikramansen/HPC_Branch_Predeiction_Suite.git
cd HPC_Branch_Predeiction_Suite
```

## Quick Start

1. **Generate datasets**:
```bash
python3 datagen.py
```

2. **Run comparison**:
```bash
python3 compare.py
```

Or use the direct prediction script:
```bash
python3 prediction.py
```

## File Descriptions

- **datagen.py**: Generates synthetic datasets representing branch prediction scenarios for different application types
- **prediction.py**: Main comparison tool with advanced features and error handling
- **compare.py**: Wrapper script for backward compatibility (calls prediction.py)
- **requirements.txt**: Python dependencies (currently none required)
- **HPC_Branch_Prediction_Suite_Paper.pdf**: Research paper detailing the methodology
- **\*_branch_dataset.csv**: Generated dataset files for different application types

## Usage

### Generating Datasets

Generate datasets with default settings (2000 samples each):
```bash
python3 datagen.py
```

Generate datasets with custom size:
```bash
python3 datagen.py --size 5000
```

Generate datasets to a specific directory:
```bash
python3 datagen.py --size 3000 --output-dir ./datasets
```

**Options**:
- `--size SIZE`: Number of samples per dataset (default: 2000)
- `--output-dir DIR`: Output directory for datasets (default: current directory)

### Running Comparisons

Run comparison with default datasets:
```bash
python3 compare.py
```

Run with custom history bits:
```bash
python3 compare.py --history-bits 10
```

Run with custom dataset files:
```bash
python3 compare.py --datasets my_dataset1.csv my_dataset2.csv
```

Specify individual dataset paths:
```bash
python3 compare.py --ml-dataset path/to/ml.csv --io-dataset path/to/io.csv
```

**Options**:
- `--datasets FILE [FILE ...]`: Paths to custom dataset CSV files
- `--ml-dataset FILE`: Path to ML app dataset (default: ml_app_branch_dataset.csv)
- `--io-dataset FILE`: Path to I/O app dataset (default: io_app_branch_dataset.csv)
- `--general-dataset FILE`: Path to general app dataset (default: general_app_branch_dataset.csv)
- `--history-bits N`: History bits for GShare and Perceptron (default: 8)

## Branch Predictors

The suite implements the following prediction algorithms:

1. **Always Taken**: Predicts that every branch will be taken
2. **Never Taken**: Predicts that no branch will be taken
3. **Bimodal**: Simple predictor that maintains a single prediction state
4. **GShare**: Advanced predictor using global history register and pattern table
5. **Perceptron**: Machine learning-based predictor using perceptron weights

## Dataset Types

The suite generates three types of datasets:

1. **ML Application Dataset**: Simulates patterns from machine learning workloads with training/inference cycles
2. **I/O Heavy Application Dataset**: Simulates patterns from I/O-intensive applications with error checking
3. **General Application Dataset**: Simulates general-purpose application patterns with mixed behavior

## Customization

### Adding New Predictors

Edit `prediction.py` and add your predictor function:

```python
def my_custom_predictor(dataset):
    # Your implementation
    correct_predictions = 0
    for address, outcome in dataset:
        # Make prediction
        prediction = 'taken'  # or 'not_taken'
        correct_predictions += (prediction == outcome)
    return correct_predictions / len(dataset)

# Add to predictors dictionary
predictors["My Custom"] = my_custom_predictor
```

### Modifying Dataset Generation

Edit `datagen.py` to change branch prediction patterns:

```python
def generate_ml_app_dataset(size=1000):
    dataset = []
    for i in range(size):
        # Modify the logic here
        outcome = 'taken' if condition else 'not_taken'
        dataset.append((address, outcome))
    return dataset
```

## Example Output

```
============================================================
Branch Predictor Comparison Tool
============================================================

============================================================
Accuracies for ML App Dataset:
============================================================
  Always Taken        :  74.35%
  Never Taken         :  25.65%
  Bimodal             :  74.35%
  Gshare              :  88.20%
  Perceptron          :  82.60%
============================================================

✓ Successfully processed 3 dataset(s)
```

## Error Handling

The suite includes comprehensive error handling:

- File not found errors with helpful messages
- Invalid CSV format detection
- Data validation for branch outcomes
- Graceful degradation with warnings
- Proper exit codes for automation

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is part of HPC research and educational purposes.

## Citation

If you use this suite in your research, please cite the accompanying paper:
- HPC_Branch_Prediction_Suite_Paper.pdf

## Authors

- Vikram Ansen

## Acknowledgments

This project implements branch prediction algorithms based on established computer architecture research and is designed for educational and research purposes in the field of High-Performance Computing.

