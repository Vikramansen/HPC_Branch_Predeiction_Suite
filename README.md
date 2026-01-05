# HPC_Branch_Predeiction_Analysis_Suite

## Overview

In the realm of High-Performance Computing (HPC), where every cycle counts, the Branch Predictor Analysis Suite emerges as a cutting-edge toolset, crucial for optimizing processor efficiency. This advanced project is ingeniously crafted to delve into the intricacies of branch prediction strategies, a cornerstone in modern CPU design. 

This robust system implements and compares various state-of-the-art branch prediction algorithms including:
- **Static Predictors**: Always Taken, Never Taken
- **Dynamic Predictors**: Bimodal, GShare, Perceptron
- **Advanced Predictors**: TAGE (Tagged Geometric History Length)

The suite provides comprehensive analysis capabilities for different application workloads (ML applications, I/O-heavy applications, and general applications), demonstrating domain-specific branch prediction optimization as described in the accompanying research paper.

## Features

- **Modular Architecture**: Clean separation of concerns with dedicated modules for predictors, data generation, and comparison
- **Multiple Predictor Implementations**: Six different branch prediction algorithms with configurable parameters
- **Domain-Specific Analysis**: Specialized datasets for ML, I/O-heavy, and general applications
- **Comprehensive Reporting**: Detailed accuracy metrics, execution time measurements, and domain-specific recommendations
- **Easy-to-Use Interface**: Command-line driver with flexible options
- **Research-Based**: Implementation based on published research in branch prediction optimization

## File Structure

```
HPC_Branch_Predeiction_Suite/
├── main.py                              # Main driver script
├── predictors.py                        # Branch predictor implementations
├── compare.py                           # Predictor comparison and analysis
├── datagen.py                          # Dataset generation for different workloads
├── config.py                           # Configuration and utility functions
├── prediction.py                       # Legacy prediction script (backward compatibility)
├── HPC_Branch_Prediction_Suite_Paper.pdf  # Research paper
├── README.md                           # This file
├── .gitignore                          # Git ignore rules
└── *.csv                               # Generated datasets
```

## Prerequisites

- Python 3.6 or higher
- No external dependencies required for basic functionality
- Optional: TensorFlow/PyTorch for neural network extensions (future work)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Vikramansen/HPC_Branch_Predeiction_Suite.git
cd HPC_Branch_Predeiction_Suite
```

2. No additional installation required - the suite uses only Python standard library!

## Usage

### Quick Start

Run the complete analysis pipeline:
```bash
python3 main.py
```

This will:
1. Generate synthetic branch prediction datasets
2. Run all predictors on all datasets
3. Display comprehensive comparison results
4. Provide domain-specific recommendations

### Individual Operations

Generate datasets only:
```bash
python3 main.py --generate
```

Run comparison (requires existing datasets):
```bash
python3 main.py --compare
```

Run legacy prediction script:
```bash
python3 main.py --legacy
```

### Direct Script Execution

You can also run individual scripts directly:

```bash
# Generate datasets
python3 datagen.py

# Run comparison
python3 compare.py

# Legacy mode
python3 prediction.py
```

## Branch Predictors

### 1. Always Taken
Static predictor that always predicts branches will be taken. Simple baseline with minimal latency.

### 2. Never Taken
Static predictor that always predicts branches will not be taken. Another baseline predictor.

### 3. Bimodal Predictor
Uses a table of 2-bit saturating counters indexed by branch address. Captures local branch behavior.

**Parameters:**
- `table_size`: Size of the prediction table (default: 1024)

### 4. GShare Predictor
Combines global branch history with branch address using XOR operation. Exploits correlation between branches.

**Parameters:**
- `history_bits`: Length of global history register (default: 10)
- `table_size`: Size of the pattern table (default: 1024)

### 5. Perceptron Predictor
Neural network-based predictor using perceptron learning algorithm. Adapts to complex branch patterns.

**Parameters:**
- `history_length`: Number of history bits (default: 8)
- `table_size`: Number of perceptrons (default: 256)
- `threshold`: Learning threshold (default: 1.5)

### 6. TAGE Predictor
Tagged Geometric History Length predictor - state-of-the-art predictor using multiple tables with different history lengths.

**Parameters:**
- `num_tables`: Number of tagged tables (default: 4)
- `base_table_size`: Size of base and tagged tables (default: 1024)

## Dataset Types

### ML Application Dataset
Simulates machine learning workload with:
- Repetitive training/inference patterns
- Regular loops with predictable behavior
- Occasional data-dependent branches

### I/O Heavy Application Dataset
Simulates I/O-intensive workload with:
- Wait patterns for I/O completion
- Error checking branches
- Resource availability checks

### General Application Dataset
Simulates typical application with:
- Mixed branch behavior
- Less predictable patterns
- Random decision points

## Understanding the Results

The comparison output includes:
- **Accuracy**: Percentage of correct predictions
- **Time**: Execution time in milliseconds (simulated overhead)
- **Misprediction Rate**: Percentage of incorrect predictions
- **Domain-Specific Recommendations**: Guidance based on research findings

### Example Output Interpretation

```
Predictor            Accuracy        Time (ms)       Mispredictions
--------------------------------------------------------------------------------
TAGE                  85.50%         12.05 ms       14.50%
Perceptron            82.30%          6.00 ms       17.70%
GShare                78.20%          2.20 ms       21.80%
Bimodal               72.15%          1.75 ms       27.85%
Always Taken          65.00%          0.28 ms       35.00%
Never Taken           35.00%          0.25 ms       65.00%
```

This shows TAGE has highest accuracy but higher latency, while simpler predictors offer lower latency but reduced accuracy.

## Research Background

This implementation is based on research in domain-specific branch prediction optimization. Key findings:

1. **Domain-Specific Optimization**: Different application types benefit from different prediction strategies
2. **Accuracy-Latency Tradeoff**: Advanced predictors offer higher accuracy but increased latency
3. **Workload Characteristics**: Branch behavior varies significantly across application domains

See `HPC_Branch_Prediction_Suite_Paper.pdf` for detailed research findings.

## Extending the Suite

### Adding New Predictors

1. Create a new class in `predictors.py` inheriting from `BranchPredictor`
2. Implement `predict()` and `update()` methods
3. Add to `get_all_predictors()` function

Example:
```python
class MyPredictor(BranchPredictor):
    def __init__(self):
        super().__init__("My Predictor")
        # Initialize state
    
    def predict(self, address, history=None):
        # Return 'taken' or 'not_taken'
        pass
    
    def update(self, address, actual_outcome, history=None):
        # Update predictor state
        pass
```

### Adding New Datasets

1. Add generation function to `datagen.py`
2. Update `DATASETS` in `config.py`
3. Update comparison loop in `compare.py`

## Performance Considerations

- Execution time measurements are simulated to reflect relative complexity
- For realistic performance analysis, integrate with architectural simulators (e.g., gem5)
- Actual hardware implementation would require RTL design and synthesis

## Future Work

- Integration with gem5 simulator for realistic performance evaluation
- SRNN (Sliced Recurrent Neural Network) predictor implementation
- SRNN+TAGE hybrid predictor
- Support for real branch trace files (from profiling tools)
- Visualization of predictor behavior over time
- Hardware cost analysis (area, power)

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is provided for educational and research purposes.

## References

See `HPC_Branch_Prediction_Suite_Paper.pdf` for complete list of academic references.

## Authors

Research and implementation by the HPC Branch Prediction research team.

## Acknowledgments

This work builds upon decades of branch prediction research. Special thanks to the authors of the foundational papers on TAGE, Perceptron, and neural network-based branch prediction.
