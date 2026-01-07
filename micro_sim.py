#!/usr/bin/env python3
"""
HPC Branch Prediction Suite - Main CLI
"""

import argparse
import sys
import os
from src.predictors import (
    always_taken_predictor,
    never_taken_predictor,
    bimodal_predictor,
    gshare_predictor,
    perceptron_predictor
)
from src.datagen import (
    generate_ml_app_dataset,
    generate_io_app_dataset,
    generate_general_app_dataset
)
from src.utils import (
    load_dataset_from_file,
    save_dataset_to_file,
    calculate_accuracies,
    print_accuracies
)

def run_compare(args):
    """Run predictor comparison."""
    # Predictor configuration
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

    # Determine datasets
    datasets_to_process = []
    
    if args.datasets:
        for path in args.datasets:
            name = os.path.basename(path).replace('.csv', '')
            datasets_to_process.append((path, name))
    else:
        # Defaults
        datasets_to_process = [
            (args.ml_dataset, "ML App"),
            (args.io_dataset, "I/O Heavy App"),
            (args.general_dataset, "General App")
        ]

    success_count = 0
    for path, name in datasets_to_process:
        try:
            dataset = load_dataset_from_file(path)
            accuracies = calculate_accuracies(dataset, predictors)
            print_accuracies(name, accuracies)
            success_count += 1
        except FileNotFoundError:
            print(f"\n✗ Dataset not found: {path}", file=sys.stderr)
            print("  Tip: Run 'python main.py generate' first.", file=sys.stderr)
        except Exception as e:
            print(f"\n✗ Error processing {path}: {e}", file=sys.stderr)

    if success_count == 0:
        print("\n✗ No datasets could be processed.", file=sys.stderr)
        sys.exit(1)
    
    print(f"\n✓ Successfully processed {success_count} dataset(s)")

def run_generate(args):
    """Run data generation."""
    print(f"Generating branch prediction datasets with {args.size} samples each...")
    print(f"Output directory: {args.output_dir}\n")

    try:
        os.makedirs(args.output_dir, exist_ok=True)
        
        datasets = [
            (generate_ml_app_dataset(args.size), "ml_app_branch_dataset.csv"),
            (generate_io_app_dataset(args.size), "io_app_branch_dataset.csv"),
            (generate_general_app_dataset(args.size), "general_app_branch_dataset.csv")
        ]

        for data, filename in datasets:
            path = os.path.join(args.output_dir, filename)
            save_dataset_to_file(data, path)

        print("\n✓ All datasets generated successfully!")
    
    except Exception as e:
        print(f"✗ Error generating datasets: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="HPC Branch Prediction Analysis Suite")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # 'compare' command
    compare_parser = subparsers.add_parser("compare", help="Compare predictors on datasets")
    compare_parser.add_argument("--datasets", nargs="+", help="Paths to custom CSV datasets")
    compare_parser.add_argument("--ml-dataset", default="data/ml_app_branch_dataset.csv", help="Path to ML dataset")
    compare_parser.add_argument("--io-dataset", default="data/io_app_branch_dataset.csv", help="Path to I/O dataset")
    compare_parser.add_argument("--general-dataset", default="data/general_app_branch_dataset.csv", help="Path to General dataset")
    compare_parser.add_argument("--history-bits", type=int, default=8, help="History bits (default: 8)")

    # 'generate' command
    gen_parser = subparsers.add_parser("generate", help="Generate synthetic datasets")
    gen_parser.add_argument("--size", type=int, default=2000, help="Samples per dataset")
    gen_parser.add_argument("--output-dir", default="data", help="Output directory")

    args = parser.parse_args()

    if args.command == "compare":
        run_compare(args)
    elif args.command == "generate":
        run_generate(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
