#!/usr/bin/env python3
"""
Branch Predictor Comparison Tool

This module implements and compares various branch prediction algorithms
including Always Taken, Never Taken, Bimodal, GShare, and Perceptron predictors.
"""

import csv
import argparse
import sys
import os
from typing import List, Tuple, Dict, Callable


def load_dataset_from_file(filename: str) -> List[Tuple[str, str]]:
    """
    Load branch prediction dataset from a CSV file.
    
    Args:
        filename: Path to the CSV file
        
    Returns:
        List of tuples (address, outcome)
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the file format is invalid
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Dataset file not found: {filename}")
    
    dataset = []
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            # Skip header if present
            first_row = next(reader, None)
            if first_row and first_row[0].lower() != 'address':
                # First row is data, not header
                if len(first_row) >= 2:
                    dataset.append((first_row[0], first_row[1]))
            
            for row in reader:
                if len(row) < 2:
                    continue  # Skip malformed rows
                address, outcome = row[0], row[1]
                if outcome not in ['taken', 'not_taken']:
                    print(f"Warning: Invalid outcome '{outcome}' in {filename}, skipping row", 
                          file=sys.stderr)
                    continue
                dataset.append((address, outcome))
                
        if not dataset:
            raise ValueError(f"No valid data found in {filename}")
            
        return dataset
    except csv.Error as e:
        raise ValueError(f"Error parsing CSV file {filename}: {e}")


# Redefining the predictor functions
# Always Taken Predictor
def always_taken_predictor(dataset):
    """
    Always predicts 'taken' for every branch.
    
    Args:
        dataset: List of tuples (address, outcome)
        
    Returns:
        Accuracy as a float between 0 and 1
    """
    return sum(outcome == 'taken' for _, outcome in dataset) / len(dataset)


def never_taken_predictor(dataset):
    """
    Always predicts 'not_taken' for every branch.
    
    Args:
        dataset: List of tuples (address, outcome)
        
    Returns:
        Accuracy as a float between 0 and 1
    """
    return sum(outcome == 'not_taken' for _, outcome in dataset) / len(dataset)


def bimodal_predictor(dataset, initial_prediction='taken'):
    """
    Bimodal predictor that maintains a state machine per branch address.
    
    Args:
        dataset: List of tuples (address, outcome)
        initial_prediction: Initial prediction ('taken' or 'not_taken')
        
    Returns:
        Accuracy as a float between 0 and 1
    """
    # Use a 2-bit saturating counter per address
    prediction_table = {}
    correct_predictions = 0
    
    for address, outcome in dataset:
        # Initialize counter for new addresses (0=strong not_taken, 3=strong taken)
        if address not in prediction_table:
            prediction_table[address] = 2 if initial_prediction == 'taken' else 1
        
        # Make prediction based on counter (>=2 means predict taken)
        prediction = 'taken' if prediction_table[address] >= 2 else 'not_taken'
        correct_predictions += (prediction == outcome)
        
        # Update counter (saturating at 0 and 3)
        if outcome == 'taken':
            prediction_table[address] = min(3, prediction_table[address] + 1)
        else:
            prediction_table[address] = max(0, prediction_table[address] - 1)
    
    return correct_predictions / len(dataset)


def gshare_predictor(dataset, history_bits=1):
    """
    GShare predictor using global history register and pattern table.
    
    Args:
        dataset: List of tuples (address, outcome)
        history_bits: Number of bits in the history register
        
    Returns:
        Accuracy as a float between 0 and 1
    """
    history = 0
    pattern_table = [0] * (2 ** history_bits)
    correct_predictions = 0

    for _, outcome in dataset:
        index = history
        prediction = 'taken' if pattern_table[index] > 0 else 'not_taken'
        correct_predictions += prediction == outcome
        
        # Update history and pattern table
        history = ((history << 1) & (2 ** history_bits - 1)) | (1 if outcome == 'taken' else 0)
        pattern_table[index] += 1 if outcome == 'taken' else -1

    return correct_predictions / len(dataset)


def perceptron_predictor(dataset, history_bits=8, threshold=1.5):
    """
    Perceptron-based branch predictor using machine learning.
    
    Args:
        dataset: List of tuples (address, outcome)
        history_bits: Number of history bits to track
        threshold: Training threshold for weight updates
        
    Returns:
        Accuracy as a float between 0 and 1
    """
    history = 0
    num_perceptrons = 2 ** history_bits
    weights = [[0] * (history_bits + 1) for _ in range(num_perceptrons)]
    correct_predictions = 0

    for _, outcome in dataset:
        index = history
        x = [1] + [1 if bit == '1' else -1 for bit in bin(history)[2:].zfill(history_bits)]
        y = 1 if outcome == 'taken' else -1
        dot_product = sum(w * x_i for w, x_i in zip(weights[index], x))
        prediction = 'taken' if dot_product > 0 else 'not_taken'
        correct_predictions += (prediction == outcome)
        
        # Update weights and history
        if y * dot_product <= threshold:
            weights[index] = [w + y * x_i for w, x_i in zip(weights[index], x)]
        history = ((history << 1) & (num_perceptrons - 1)) | (1 if outcome == 'taken' else 0)

    return correct_predictions / len(dataset)


def calculate_accuracies(dataset: List[Tuple[str, str]], 
                        predictors: Dict[str, Callable]) -> Dict[str, float]:
    """
    Calculate accuracy for all predictors on a given dataset.
    
    Args:
        dataset: List of tuples (address, outcome)
        predictors: Dictionary of predictor name -> predictor function
        
    Returns:
        Dictionary of predictor name -> accuracy
    """
    accuracies = {}
    for name, predictor in predictors.items():
        try:
            accuracies[name] = predictor(dataset)
        except Exception as e:
            print(f"Warning: Error running {name} predictor: {e}", file=sys.stderr)
            accuracies[name] = 0.0
    return accuracies


def print_accuracies(dataset_name: str, accuracies: Dict[str, float]):
    """
    Print accuracy results in a formatted table.
    
    Args:
        dataset_name: Name of the dataset
        accuracies: Dictionary of predictor name -> accuracy
    """
    print(f"\n{'='*60}")
    print(f"Accuracies for {dataset_name} Dataset:")
    print(f"{'='*60}")
    for predictor_name, accuracy in accuracies.items():
        print(f"  {predictor_name:20s}: {accuracy * 100:6.2f}%")
    print(f"{'='*60}")


def main():
    """Main function to run branch predictor comparison."""
    parser = argparse.ArgumentParser(
        description='Compare branch prediction algorithms on datasets'
    )
    parser.add_argument(
        '--datasets',
        nargs='+',
        help='Paths to dataset CSV files'
    )
    parser.add_argument(
        '--ml-dataset',
        default='ml_app_branch_dataset.csv',
        help='Path to ML app dataset (default: ml_app_branch_dataset.csv)'
    )
    parser.add_argument(
        '--io-dataset',
        default='io_app_branch_dataset.csv',
        help='Path to I/O app dataset (default: io_app_branch_dataset.csv)'
    )
    parser.add_argument(
        '--general-dataset',
        default='general_app_branch_dataset.csv',
        help='Path to general app dataset (default: general_app_branch_dataset.csv)'
    )
    parser.add_argument(
        '--history-bits',
        type=int,
        default=8,
        help='History bits for GShare and Perceptron (default: 8)'
    )
    
    args = parser.parse_args()
    
    # Predictor functions dictionary
    predictors = {
        "Always Taken": always_taken_predictor,
        "Never Taken": never_taken_predictor,
        "Bimodal": bimodal_predictor,
        "Gshare": lambda d: gshare_predictor(d, history_bits=args.history_bits),
        "Perceptron": lambda d: perceptron_predictor(d, history_bits=args.history_bits)
    }
    
    print("\n" + "="*60)
    print("Branch Predictor Comparison Tool")
    print("="*60)
    
    # Determine which datasets to process
    if args.datasets:
        # Use custom datasets
        for dataset_path in args.datasets:
            try:
                dataset = load_dataset_from_file(dataset_path)
                dataset_name = os.path.basename(dataset_path).replace('.csv', '')
                accuracies = calculate_accuracies(dataset, predictors)
                print_accuracies(dataset_name, accuracies)
            except Exception as e:
                print(f"\n✗ Error processing {dataset_path}: {e}", file=sys.stderr)
    else:
        # Use default datasets
        datasets_to_process = [
            (args.ml_dataset, "ML App"),
            (args.io_dataset, "I/O Heavy App"),
            (args.general_dataset, "General App")
        ]
        
        success_count = 0
        for dataset_path, dataset_name in datasets_to_process:
            try:
                dataset = load_dataset_from_file(dataset_path)
                accuracies = calculate_accuracies(dataset, predictors)
                print_accuracies(dataset_name, accuracies)
                success_count += 1
            except FileNotFoundError:
                print(f"\n✗ Dataset not found: {dataset_path}", file=sys.stderr)
                print(f"  Run 'python3 datagen.py' to generate datasets first.", file=sys.stderr)
            except Exception as e:
                print(f"\n✗ Error processing {dataset_path}: {e}", file=sys.stderr)
        
        if success_count == 0:
            print("\n✗ No datasets could be processed.", file=sys.stderr)
            sys.exit(1)
        
        print(f"\n✓ Successfully processed {success_count} dataset(s)")


if __name__ == "__main__":
    main()
