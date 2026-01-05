#!/usr/bin/env python3
"""
Branch Prediction Dataset Generator

This module generates synthetic branch prediction datasets for different
application types: ML-based, I/O-heavy, and general applications.
"""

import random
import argparse
import sys
import os


def generate_ml_app_dataset(size=1000):
    """
    Generate a dataset for ML-based applications.
    
    Args:
        size: Number of branch samples to generate
        
    Returns:
        List of tuples (branch_address, outcome)
    """
    dataset = []
    for i in range(size):
        branch_address = f'0x{2000 + i:04x}'
        
        # Repetitive pattern for training/inference cycles
        if i % 20 < 15:
            outcome = 'taken'
        else:
            outcome = 'not_taken'

        # Data-driven conditions
        if random.random() < 0.05:
            outcome = 'taken' if random.random() < 0.7 else 'not_taken'

        dataset.append((branch_address, outcome))

    return dataset


def generate_io_app_dataset(size=1000):
    """
    Generate a dataset for I/O-heavy applications.
    
    Args:
        size: Number of branch samples to generate
        
    Returns:
        List of tuples (branch_address, outcome)
    """
    dataset = []
    for i in range(size):
        branch_address = f'0x{3000 + i:04x}'

        # Checking for I/O errors or data availability
        if i % 25 < 5:
            outcome = 'not_taken'
        else:
            outcome = 'taken'

        # External resource states influencing branching
        if random.random() < 0.15:
            outcome = 'taken' if random.random() < 0.5 else 'not_taken'

        dataset.append((branch_address, outcome))

    return dataset


def generate_general_app_dataset(size=1000):
    """
    Generate a dataset for general applications.
    
    Args:
        size: Number of branch samples to generate
        
    Returns:
        List of tuples (branch_address, outcome)
    """
    dataset = []
    for i in range(size):
        branch_address = f'0x{4000 + i:04x}'

        # Random and less predictable
        outcome = 'taken' if random.random() < 0.6 else 'not_taken'

        dataset.append((branch_address, outcome))

    return dataset


def save_dataset_to_file(dataset, filename):
    """
    Save dataset to a CSV file.
    
    Args:
        dataset: List of tuples (branch_address, outcome)
        filename: Output filename
        
    Returns:
        filename if successful
        
    Raises:
        IOError: If file cannot be written
    """
    try:
        with open(filename, 'w') as file:
            file.write("address,outcome\n")  # Add header
            for address, outcome in dataset:
                file.write(f"{address},{outcome}\n")
        print(f"✓ Successfully saved {len(dataset)} samples to {filename}")
        return filename
    except IOError as e:
        print(f"✗ Error saving dataset to {filename}: {e}", file=sys.stderr)
        raise


def main():
    """Main function to generate and save datasets."""
    parser = argparse.ArgumentParser(
        description='Generate synthetic branch prediction datasets'
    )
    parser.add_argument(
        '--size',
        type=int,
        default=2000,
        help='Number of samples per dataset (default: 2000)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='.',
        help='Output directory for datasets (default: current directory)'
    )
    
    args = parser.parse_args()
    
    # Validate size
    if args.size <= 0:
        print("✗ Error: Size must be positive", file=sys.stderr)
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    if args.output_dir != '.':
        try:
            os.makedirs(args.output_dir, exist_ok=True)
        except OSError as e:
            print(f"✗ Error creating directory {args.output_dir}: {e}", file=sys.stderr)
            sys.exit(1)
    
    print(f"Generating branch prediction datasets with {args.size} samples each...")
    print()
    
    try:
        # Generate the datasets
        ml_app_dataset = generate_ml_app_dataset(size=args.size)
        io_app_dataset = generate_io_app_dataset(size=args.size)
        general_app_dataset = generate_general_app_dataset(size=args.size)
        
        # Save the datasets to files
        ml_filename = os.path.join(args.output_dir, "ml_app_branch_dataset.csv")
        io_filename = os.path.join(args.output_dir, "io_app_branch_dataset.csv")
        general_filename = os.path.join(args.output_dir, "general_app_branch_dataset.csv")
        
        save_dataset_to_file(ml_app_dataset, ml_filename)
        save_dataset_to_file(io_app_dataset, io_filename)
        save_dataset_to_file(general_app_dataset, general_filename)
        
        print()
        print("✓ All datasets generated successfully!")
        
    except Exception as e:
        print(f"✗ Error generating datasets: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
