"""
Visualization and Reporting Module
Generates visual representations of predictor performance
Note: This module provides text-based visualizations that work without external dependencies
"""

import sys
from predictors import get_all_predictors
from config import load_dataset_from_file


def create_bar_chart(data, max_width=50):
    """
    Create a text-based bar chart
    data: dict of {label: value} where value is between 0 and 1
    """
    if not data:
        return []
    
    lines = []
    max_label_len = max(len(label) for label in data.keys())
    
    for label, value in data.items():
        bar_len = int(value * max_width)
        bar = '█' * bar_len
        percentage = f"{value * 100:>6.2f}%"
        lines.append(f"{label:<{max_label_len}} {percentage} {bar}")
    
    return lines


def evaluate_predictor(predictor, dataset):
    """Evaluate a predictor on a dataset"""
    predictor.reset()
    
    for address, actual_outcome in dataset:
        prediction = predictor.predict(address)
        predictor.update(address, actual_outcome)
    
    return predictor.get_accuracy()


def generate_comparison_chart(dataset_name, dataset_file):
    """Generate comparison chart for a single dataset"""
    print(f"\n{'='*80}")
    print(f"PREDICTOR COMPARISON - {dataset_name.upper()}")
    print(f"{'='*80}\n")
    
    # Load dataset
    dataset = load_dataset_from_file(dataset_file)
    if dataset is None:
        return False
    
    print(f"Dataset: {dataset_file}")
    print(f"Traces: {len(dataset)} branch instructions\n")
    
    # Evaluate all predictors
    predictors = get_all_predictors()
    results = {}
    
    for name, predictor in predictors.items():
        accuracy = evaluate_predictor(predictor, dataset)
        results[name] = accuracy
    
    # Sort by accuracy
    sorted_results = dict(sorted(results.items(), key=lambda x: x[1], reverse=True))
    
    # Display bar chart
    print("Prediction Accuracy:")
    print("-" * 80)
    
    for line in create_bar_chart(sorted_results, max_width=40):
        print(line)
    
    print("\n" + "="*80)
    
    return True


def generate_comparative_report():
    """Generate comprehensive comparative report"""
    datasets = {
        'ML App': 'ml_app_branch_dataset.csv',
        'I/O Heavy App': 'io_app_branch_dataset.csv',
        'General App': 'general_app_branch_dataset.csv'
    }
    
    print("\n" + "="*80)
    print("COMPREHENSIVE BRANCH PREDICTOR ANALYSIS")
    print("="*80)
    
    all_results = {}
    
    for dataset_name, dataset_file in datasets.items():
        dataset = load_dataset_from_file(dataset_file)
        if dataset is None:
            continue
        
        predictors = get_all_predictors()
        dataset_results = {}
        
        for name, predictor in predictors.items():
            accuracy = evaluate_predictor(predictor, dataset)
            dataset_results[name] = accuracy
        
        all_results[dataset_name] = dataset_results
    
    # Print comparison table
    print("\nPrediction Accuracy Comparison Table")
    print("="*80)
    
    # Header
    predictor_names = list(next(iter(all_results.values())).keys())
    header = f"{'Dataset':<20}"
    for pred in predictor_names:
        header += f"{pred:<15}"
    print(header)
    print("-" * 80)
    
    # Rows
    for dataset_name, results in all_results.items():
        row = f"{dataset_name:<20}"
        for pred in predictor_names:
            accuracy = results[pred]
            row += f"{accuracy*100:>6.2f}%      "
        print(row)
    
    print("\n" + "="*80)
    
    # Best predictor for each dataset
    print("\nBest Predictor by Dataset:")
    print("-" * 80)
    
    for dataset_name, results in all_results.items():
        best_pred = max(results.items(), key=lambda x: x[1])
        print(f"{dataset_name:<20} → {best_pred[0]:<15} ({best_pred[1]*100:.2f}%)")
    
    print("\n" + "="*80)
    
    # Average performance across all datasets
    print("\nAverage Performance Across All Datasets:")
    print("-" * 80)
    
    avg_performance = {}
    for pred in predictor_names:
        total = sum(results[pred] for results in all_results.values())
        avg = total / len(all_results)
        avg_performance[pred] = avg
    
    sorted_avg = dict(sorted(avg_performance.items(), key=lambda x: x[1], reverse=True))
    
    for line in create_bar_chart(sorted_avg, max_width=40):
        print(line)
    
    print("\n" + "="*80)
    
    return True


def generate_dataset_comparison_chart():
    """Generate chart comparing dataset characteristics"""
    datasets = {
        'ML App': 'ml_app_branch_dataset.csv',
        'I/O Heavy App': 'io_app_branch_dataset.csv',
        'General App': 'general_app_branch_dataset.csv'
    }
    
    print("\n" + "="*80)
    print("DATASET CHARACTERISTICS")
    print("="*80 + "\n")
    
    for dataset_name, dataset_file in datasets.items():
        dataset = load_dataset_from_file(dataset_file)
        if dataset is None:
            continue
        
        taken_count = sum(1 for _, outcome in dataset if outcome == 'taken')
        not_taken_count = len(dataset) - taken_count
        
        taken_pct = taken_count / len(dataset) if len(dataset) > 0 else 0
        not_taken_pct = not_taken_count / len(dataset) if len(dataset) > 0 else 0
        
        print(f"{dataset_name}:")
        print(f"  Total branches: {len(dataset)}")
        print(f"  Taken:          {taken_count:>5} ({taken_pct*100:>6.2f}%)")
        print(f"  Not Taken:      {not_taken_count:>5} ({not_taken_pct*100:>6.2f}%)")
        print(f"  Bias:           {'Taken' if taken_pct > 0.5 else 'Not Taken'}")
        
        # Show distribution bar
        bar_taken = int(taken_pct * 50)
        bar_not_taken = 50 - bar_taken
        print(f"  Distribution:   [{'█' * bar_taken}{'░' * bar_not_taken}]")
        print()
    
    print("="*80 + "\n")


def main():
    """Main visualization function"""
    print("\n" + "="*80)
    print("HPC BRANCH PREDICTOR VISUALIZATION")
    print("="*80)
    
    # Dataset characteristics
    generate_dataset_comparison_chart()
    
    # Individual dataset comparisons
    datasets = {
        'ML App': 'ml_app_branch_dataset.csv',
        'I/O Heavy App': 'io_app_branch_dataset.csv',
        'General App': 'general_app_branch_dataset.csv'
    }
    
    for dataset_name, dataset_file in datasets.items():
        generate_comparison_chart(dataset_name, dataset_file)
    
    # Comprehensive comparison
    generate_comparative_report()
    
    print("\nVisualization complete!")
    print("For publication-quality graphics, export results to CSV and use matplotlib/gnuplot")
    print()


if __name__ == '__main__':
    main()
