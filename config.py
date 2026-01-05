"""
Configuration and utility functions for the HPC Branch Prediction Suite
"""

import csv
import sys

# Dataset configurations
DATASETS = {
    'ml_app': {
        'name': 'ML App',
        'filename': 'ml_app_branch_dataset.csv',
        'description': 'Machine Learning application with repetitive training/inference patterns',
        'size': 2000
    },
    'io_app': {
        'name': 'I/O Heavy App',
        'filename': 'io_app_branch_dataset.csv',
        'description': 'I/O-heavy application with wait patterns and data availability checks',
        'size': 2000
    },
    'general_app': {
        'name': 'General App',
        'filename': 'general_app_branch_dataset.csv',
        'description': 'General application with unpredictable branch behavior',
        'size': 2000
    }
}

# Predictor configurations
PREDICTOR_CONFIGS = {
    'bimodal': {
        'table_size': 1024,
        'description': '2-bit saturating counter predictor'
    },
    'gshare': {
        'history_bits': 10,
        'table_size': 1024,
        'description': 'GShare predictor with global history XOR'
    },
    'perceptron': {
        'history_length': 8,
        'table_size': 256,
        'threshold': 1.5,
        'description': 'Neural network-based perceptron predictor'
    },
    'tage': {
        'num_tables': 4,
        'base_table_size': 1024,
        'description': 'Tagged Geometric history length predictor'
    }
}

# Color codes for terminal output (optional)
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def format_percentage(value, decimals=2):
    """Format a value as a percentage"""
    return f"{value * 100:.{decimals}f}%"


def format_time_ms(seconds, decimals=2):
    """Format seconds as milliseconds"""
    return f"{seconds * 1000:.{decimals}f} ms"


def format_number(value, decimals=2):
    """Format a number with specified decimals"""
    return f"{value:.{decimals}f}"


def validate_dataset_format(dataset):
    """
    Validate that a dataset has the correct format
    Returns: (is_valid, error_message)
    """
    if not isinstance(dataset, list):
        return False, "Dataset must be a list"
    
    if len(dataset) == 0:
        return False, "Dataset is empty"
    
    for i, entry in enumerate(dataset):
        if not isinstance(entry, tuple) or len(entry) != 2:
            return False, f"Entry {i} is not a (address, outcome) tuple"
        
        address, outcome = entry
        if outcome not in ['taken', 'not_taken']:
            return False, f"Entry {i} has invalid outcome: {outcome}"
    
    return True, None


def get_predictor_description(predictor_name):
    """Get a human-readable description of a predictor"""
    descriptions = {
        'Always Taken': 'Static predictor that always predicts branches as taken',
        'Never Taken': 'Static predictor that always predicts branches as not taken',
        'Bimodal': 'Dynamic predictor using 2-bit saturating counters indexed by branch address',
        'GShare': 'Dynamic predictor combining global history with branch address using XOR',
        'Perceptron': 'Machine learning-based predictor using perceptron neural network',
        'TAGE': 'Advanced predictor using multiple tagged tables with geometric history lengths'
    }
    return descriptions.get(predictor_name, 'Unknown predictor')


def print_info(message, prefix="INFO"):
    """Print an informational message"""
    print(f"[{prefix}] {message}")


def print_error(message):
    """Print an error message"""
    print(f"[ERROR] {message}")


def print_success(message):
    """Print a success message"""
    print(f"[SUCCESS] {message}")


def print_warning(message):
    """Print a warning message"""
    print(f"[WARNING] {message}")


def load_dataset_from_file(filename):
    """
    Load branch trace dataset from CSV file
    Returns: list of (address, outcome) tuples, or None on error
    """
    dataset = []
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    address, outcome = row[0], row[1]
                    dataset.append((address, outcome))
                else:
                    print_warning(f"Skipping malformed row in {filename}")
        return dataset
    except FileNotFoundError:
        print_error(f"Dataset file '{filename}' not found.")
        print("Please run 'python3 datagen.py' first to generate datasets.")
        return None
    except Exception as e:
        print_error(f"Error loading dataset: {e}")
        return None
