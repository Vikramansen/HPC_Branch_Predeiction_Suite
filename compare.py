"""
Branch Predictor Comparison Script
Compares various branch predictors on different workload datasets
"""

import csv
import sys
import time
from predictors import get_all_predictors
from config import load_dataset_from_file


def evaluate_predictor(predictor, dataset, measure_time=True):
    """
    Evaluate a predictor on a dataset
    Returns: (accuracy, execution_time)
    """
    predictor.reset()
    
    start_time = time.time() if measure_time else 0
    
    for address, actual_outcome in dataset:
        prediction = predictor.predict(address)
        predictor.update(address, actual_outcome)
    
    end_time = time.time() if measure_time else 0
    execution_time = end_time - start_time if measure_time else 0
    
    accuracy = predictor.get_accuracy()
    return accuracy, execution_time


def print_separator(char='=', length=80):
    """Print a separator line"""
    print(char * length)


def print_results(dataset_name, results):
    """Print comparison results in a formatted table"""
    print_separator()
    print(f"BRANCH PREDICTOR COMPARISON - {dataset_name.upper()}")
    print_separator()
    print(f"{'Predictor':<20} {'Accuracy':<15} {'Time (ms)':<15} {'Mispredictions':<15}")
    print_separator('-')
    
    # Sort by accuracy (descending)
    sorted_results = sorted(results.items(), key=lambda x: x[1]['accuracy'], reverse=True)
    
    for predictor_name, data in sorted_results:
        accuracy = data['accuracy'] * 100
        exec_time = data['time'] * 1000  # Convert to milliseconds
        mispred_rate = (1 - data['accuracy']) * 100
        print(f"{predictor_name:<20} {accuracy:>6.2f}%        {exec_time:>6.2f} ms      {mispred_rate:>6.2f}%")
    
    print_separator()
    print()


def print_summary(all_results):
    """Print overall summary across all datasets"""
    print_separator('=')
    print("OVERALL SUMMARY")
    print_separator('=')
    
    # Determine best predictor for each dataset
    for dataset_name, results in all_results.items():
        best_predictor = max(results.items(), key=lambda x: x[1]['accuracy'])
        print(f"\nBest for {dataset_name}: {best_predictor[0]} ({best_predictor[1]['accuracy']*100:.2f}% accuracy)")
    
    # Calculate average accuracy across all datasets for each predictor
    print("\nAverage Accuracy Across All Datasets:")
    print_separator('-')
    
    predictor_names = list(next(iter(all_results.values())).keys())
    avg_accuracies = {}
    
    for predictor_name in predictor_names:
        total_accuracy = sum(results[predictor_name]['accuracy'] for results in all_results.values())
        avg_accuracy = total_accuracy / len(all_results)
        avg_accuracies[predictor_name] = avg_accuracy
    
    # Sort by average accuracy
    sorted_avg = sorted(avg_accuracies.items(), key=lambda x: x[1], reverse=True)
    
    for predictor_name, avg_acc in sorted_avg:
        print(f"{predictor_name:<20} {avg_acc*100:>6.2f}%")
    
    print_separator('=')
    print()


def print_domain_specific_recommendation(all_results):
    """
    Print domain-specific recommendations based on paper's findings
    """
    print_separator('=')
    print("DOMAIN-SPECIFIC RECOMMENDATIONS")
    print("(Based on research paper findings)")
    print_separator('=')
    
    recommendations = {
        'ML App': 'For ML applications with repetitive patterns, neural network-based\n'
                  '          predictors (Perceptron) or history-based predictors (TAGE, GShare)\n'
                  '          provide superior accuracy despite higher complexity.',
        
        'I/O Heavy App': 'For I/O-heavy applications with predictable wait patterns,\n'
                         '          advanced predictors (TAGE, GShare) can exploit regular I/O cycles\n'
                         '          to improve prediction accuracy.',
        
        'General App': 'For general applications with unpredictable behavior,\n'
                       '          simpler predictors may offer better latency-accuracy tradeoff.\n'
                       '          Consider TAGE for best accuracy or simpler predictors for low latency.'
    }
    
    for dataset_name, results in all_results.items():
        print(f"\n{dataset_name}:")
        best_predictor = max(results.items(), key=lambda x: x[1]['accuracy'])
        print(f"  Best Predictor: {best_predictor[0]} ({best_predictor[1]['accuracy']*100:.2f}% accuracy)")
        
        if dataset_name in recommendations:
            print(f"\n  Recommendation: {recommendations[dataset_name]}")
    
    print_separator('=')
    print()


def main():
    """Main comparison function"""
    print("\n" + "="*80)
    print("HPC BRANCH PREDICTOR ANALYSIS SUITE")
    print("Comprehensive Branch Predictor Comparison")
    print("="*80 + "\n")
    
    # Dataset files
    datasets = {
        'ML App': 'ml_app_branch_dataset.csv',
        'I/O Heavy App': 'io_app_branch_dataset.csv',
        'General App': 'general_app_branch_dataset.csv'
    }
    
    all_results = {}
    
    # Evaluate each dataset
    for dataset_name, dataset_file in datasets.items():
        print(f"Loading {dataset_name} dataset from {dataset_file}...")
        dataset = load_dataset_from_file(dataset_file)
        print(f"Loaded {len(dataset)} branch traces.\n")
        
        # Get all predictors
        predictors = get_all_predictors()
        
        results = {}
        print(f"Evaluating predictors on {dataset_name} dataset...")
        
        for predictor_name, predictor in predictors.items():
            print(f"  Testing {predictor_name}...", end='', flush=True)
            accuracy, exec_time = evaluate_predictor(predictor, dataset)
            results[predictor_name] = {
                'accuracy': accuracy,
                'time': exec_time
            }
            print(f" Done (Accuracy: {accuracy*100:.2f}%)")
        
        print()
        all_results[dataset_name] = results
        
        # Print results for this dataset
        print_results(dataset_name, results)
    
    # Print overall summary
    print_summary(all_results)
    
    # Print domain-specific recommendations
    print_domain_specific_recommendation(all_results)
    
    print("Analysis complete!")
    print("\nNote: This implementation demonstrates domain-specific branch prediction")
    print("as discussed in the research paper. Different predictors excel in different")
    print("application domains based on their branch behavior characteristics.")
    print()


if __name__ == '__main__':
    main()
