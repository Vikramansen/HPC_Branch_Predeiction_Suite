#!/usr/bin/env python3
"""
HPC Branch Prediction Suite - Main Driver
This is the main entry point for the branch prediction analysis suite.
"""

import sys
import argparse
import os


def check_datasets_exist():
    """Check if required dataset files exist"""
    datasets = [
        'ml_app_branch_dataset.csv',
        'io_app_branch_dataset.csv',
        'general_app_branch_dataset.csv'
    ]
    
    missing = [d for d in datasets if not os.path.exists(d)]
    return len(missing) == 0, missing


def generate_datasets():
    """Generate datasets using datagen.py"""
    print("Generating branch prediction datasets...")
    print("-" * 60)
    
    try:
        import datagen
        print("\nDatasets generated successfully!")
        print("Files created:")
        print("  - ml_app_branch_dataset.csv")
        print("  - io_app_branch_dataset.csv")
        print("  - general_app_branch_dataset.csv")
        return True
    except Exception as e:
        print(f"Error generating datasets: {e}")
        return False


def run_comparison():
    """Run the branch predictor comparison"""
    print("\nRunning branch predictor comparison...")
    print("=" * 60)
    
    try:
        import compare
        compare.main()
        return True
    except Exception as e:
        print(f"Error running comparison: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_legacy_prediction():
    """Run the legacy prediction.py script for compatibility"""
    print("\nRunning legacy prediction script...")
    print("-" * 60)
    
    try:
        import prediction
        return True
    except Exception as e:
        print(f"Error running prediction: {e}")
        return False


def print_welcome():
    """Print welcome message"""
    print("\n" + "=" * 80)
    print(" " * 15 + "HPC BRANCH PREDICTION ANALYSIS SUITE")
    print(" " * 20 + "High-Performance Computing Project")
    print("=" * 80)
    print("\nThis suite implements various branch prediction algorithms including:")
    print("  • Static Predictors: Always Taken, Never Taken")
    print("  • Dynamic Predictors: Bimodal, GShare, Perceptron")
    print("  • Advanced Predictors: TAGE (Tagged Geometric History Length)")
    print("\nBased on research in domain-specific branch prediction optimization")
    print("=" * 80 + "\n")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='HPC Branch Prediction Analysis Suite',
        epilog='For more information, see README.md'
    )
    
    parser.add_argument(
        '--generate',
        action='store_true',
        help='Generate branch prediction datasets'
    )
    
    parser.add_argument(
        '--compare',
        action='store_true',
        help='Run predictor comparison (requires datasets)'
    )
    
    parser.add_argument(
        '--legacy',
        action='store_true',
        help='Run legacy prediction.py script'
    )
    
    parser.add_argument(
        '--full',
        action='store_true',
        help='Run full pipeline: generate datasets and compare predictors'
    )
    
    args = parser.parse_args()
    
    # If no arguments, run full pipeline
    if not (args.generate or args.compare or args.legacy or args.full):
        args.full = True
    
    print_welcome()
    
    success = True
    
    # Generate datasets if requested
    if args.generate or args.full:
        if not generate_datasets():
            success = False
            print("\nDataset generation failed!")
            sys.exit(1)
        print()
    
    # Run comparison if requested
    if args.compare or args.full:
        # Check if datasets exist
        datasets_exist, missing = check_datasets_exist()
        
        if not datasets_exist:
            print("Error: Required datasets not found!")
            print("Missing files:")
            for f in missing:
                print(f"  - {f}")
            print("\nPlease run with --generate first to create datasets.")
            sys.exit(1)
        
        if not run_comparison():
            success = False
            print("\nComparison failed!")
            sys.exit(1)
    
    # Run legacy script if requested
    if args.legacy:
        if not run_legacy_prediction():
            success = False
            print("\nLegacy prediction failed!")
            sys.exit(1)
    
    if success:
        print("\n" + "=" * 80)
        print("Analysis Complete!")
        print("=" * 80 + "\n")
        return 0
    else:
        return 1


if __name__ == '__main__':
    sys.exit(main())
