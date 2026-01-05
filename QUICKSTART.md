# Quick Start Guide

## HPC Branch Prediction Analysis Suite

### Installation
```bash
git clone https://github.com/Vikramansen/HPC_Branch_Predeiction_Suite.git
cd HPC_Branch_Predeiction_Suite
```

No dependencies required - uses only Python 3 standard library!

### Quick Usage

#### 1. Run Everything (Recommended for first time)
```bash
python3 main.py
```
This will:
- Generate datasets
- Run all predictors
- Display results

#### 2. Individual Commands

**Generate Datasets:**
```bash
python3 main.py --generate
```

**Compare Predictors:**
```bash
python3 main.py --compare
```

**Run Tests:**
```bash
python3 main.py --test
```

**Visualize Results:**
```bash
python3 main.py --visualize
```

**Export to CSV:**
```bash
python3 main.py --export
```

#### 3. Direct Script Execution

```bash
# Generate datasets
python3 datagen.py

# Run comparison
python3 compare.py

# Run tests
python3 test_predictors.py

# Generate visualizations
python3 visualize.py

# Export results
python3 export_results.py
```

### Understanding the Output

**Accuracy**: Percentage of correct predictions (higher is better)
**Time**: Simulated execution time (lower is better)
**Misprediction Rate**: Percentage of incorrect predictions (lower is better)

### Predictor Overview

1. **Always Taken / Never Taken**: Simple baselines
2. **Bimodal**: 2-bit saturating counter predictor
3. **GShare**: Global history XOR with address
4. **Perceptron**: Neural network-based learning
5. **TAGE**: State-of-the-art with geometric history lengths

### Dataset Types

1. **ML App**: Machine learning workload (repetitive patterns)
2. **I/O Heavy App**: I/O operations (wait patterns)
3. **General App**: Mixed behavior (unpredictable)

### Extending the Suite

#### Add a New Predictor

Edit `predictors.py`:
```python
class MyPredictor(BranchPredictor):
    def __init__(self):
        super().__init__("My Predictor")
        # Initialize state
    
    def predict(self, address, history=None):
        # Return 'taken' or 'not_taken'
        return 'taken'
    
    def update(self, address, actual_outcome, history=None):
        # Update based on actual outcome
        self.total_predictions += 1
        if actual_outcome == 'taken':
            self.correct_predictions += 1
```

Then add to `get_all_predictors()`:
```python
def get_all_predictors():
    return {
        # ... existing predictors ...
        'My Predictor': MyPredictor()
    }
```

### Tips

- Always run `--test` after making changes to predictors
- Use `--export` to analyze results in spreadsheet software
- Check the research paper (HPC_Branch_Prediction_Suite_Paper.pdf) for background

### Common Issues

**Q: Datasets not found?**
A: Run `python3 main.py --generate` first

**Q: How to get graphical charts?**
A: Use `--export` and open CSV files in Excel/LibreOffice, or use matplotlib

**Q: What Python version?**
A: Python 3.6 or higher required

### File Structure

```
HPC_Branch_Predeiction_Suite/
├── main.py                 # Main driver
├── predictors.py          # Predictor implementations
├── compare.py             # Comparison engine
├── datagen.py            # Dataset generator
├── test_predictors.py    # Test suite
├── visualize.py          # Visualization
├── export_results.py     # CSV export
├── config.py            # Configuration
├── README.md            # Full documentation
└── QUICKSTART.md        # This file
```

### Performance Expectations

On a typical modern CPU:
- Dataset generation: < 1 second
- Comparison (all predictors, all datasets): 1-2 seconds
- Tests: < 1 second
- Visualization: 1-2 seconds
- Export: < 1 second

### Support

For detailed information, see:
- `README.md` - Comprehensive documentation
- `HPC_Branch_Prediction_Suite_Paper.pdf` - Research background
- Code comments in each module

### License

Educational and research use.
