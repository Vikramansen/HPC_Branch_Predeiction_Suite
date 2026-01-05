"""
Results Export Module
Exports predictor comparison results to CSV format for external analysis
"""

import csv
import os
from datetime import datetime
from predictors import get_all_predictors
from config import load_dataset_from_file


def evaluate_predictor(predictor, dataset):
    """Evaluate a predictor on a dataset"""
    predictor.reset()
    
    for address, actual_outcome in dataset:
        prediction = predictor.predict(address)
        predictor.update(address, actual_outcome)
    
    accuracy = predictor.get_accuracy()
    correct = predictor.correct_predictions
    total = predictor.total_predictions
    
    return {
        'accuracy': accuracy,
        'correct': correct,
        'total': total,
        'mispredictions': total - correct,
        'misprediction_rate': 1 - accuracy if total > 0 else 0
    }


def export_detailed_results(output_dir='results'):
    """Export detailed results to CSV files"""
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    datasets = {
        'ml_app': 'ml_app_branch_dataset.csv',
        'io_app': 'io_app_branch_dataset.csv',
        'general_app': 'general_app_branch_dataset.csv'
    }
    
    all_results = {}
    
    # Evaluate all predictors on all datasets
    print("\nEvaluating predictors...")
    for dataset_key, dataset_file in datasets.items():
        print(f"  Processing {dataset_key}...")
        dataset = load_dataset_from_file(dataset_file)
        if dataset is None:
            print(f"    Warning: Could not load {dataset_file}")
            continue
        
        predictors = get_all_predictors()
        dataset_results = {}
        
        for pred_name, predictor in predictors.items():
            results = evaluate_predictor(predictor, dataset)
            dataset_results[pred_name] = results
        
        all_results[dataset_key] = dataset_results
    
    # Export summary table
    summary_file = os.path.join(output_dir, f'summary_{timestamp}.csv')
    print(f"\nExporting summary to {summary_file}...")
    
    with open(summary_file, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Header
        predictor_names = list(next(iter(all_results.values())).keys())
        header = ['Dataset'] + predictor_names
        writer.writerow(header)
        
        # Data rows
        for dataset_key, results in all_results.items():
            row = [dataset_key]
            for pred_name in predictor_names:
                accuracy = results[pred_name]['accuracy']
                row.append(f"{accuracy:.6f}")
            writer.writerow(row)
    
    # Export detailed results for each dataset
    for dataset_key, results in all_results.items():
        detail_file = os.path.join(output_dir, f'{dataset_key}_detailed_{timestamp}.csv')
        print(f"Exporting {dataset_key} details to {detail_file}...")
        
        with open(detail_file, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'Predictor', 'Accuracy', 'Correct', 'Total', 
                'Mispredictions', 'Misprediction_Rate'
            ])
            
            # Data rows
            for pred_name, metrics in results.items():
                writer.writerow([
                    pred_name,
                    f"{metrics['accuracy']:.6f}",
                    metrics['correct'],
                    metrics['total'],
                    metrics['mispredictions'],
                    f"{metrics['misprediction_rate']:.6f}"
                ])
    
    # Export comparative analysis
    comp_file = os.path.join(output_dir, f'comparative_analysis_{timestamp}.csv')
    print(f"Exporting comparative analysis to {comp_file}...")
    
    with open(comp_file, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Calculate statistics
        writer.writerow(['Predictor', 'Avg_Accuracy', 'Min_Accuracy', 'Max_Accuracy', 'Std_Dev'])
        
        predictor_names = list(next(iter(all_results.values())).keys())
        for pred_name in predictor_names:
            accuracies = [results[pred_name]['accuracy'] for results in all_results.values()]
            
            avg = sum(accuracies) / len(accuracies)
            min_acc = min(accuracies)
            max_acc = max(accuracies)
            
            # Calculate standard deviation
            variance = sum((x - avg) ** 2 for x in accuracies) / len(accuracies)
            std_dev = variance ** 0.5
            
            writer.writerow([
                pred_name,
                f"{avg:.6f}",
                f"{min_acc:.6f}",
                f"{max_acc:.6f}",
                f"{std_dev:.6f}"
            ])
    
    print(f"\nExport complete! Files saved in '{output_dir}/' directory")
    print("\nGenerated files:")
    print(f"  - {os.path.basename(summary_file)}")
    for dataset_key in all_results.keys():
        print(f"  - {dataset_key}_detailed_{timestamp}.csv")
    print(f"  - {os.path.basename(comp_file)}")
    
    return True


def export_for_plotting(output_dir='results'):
    """Export data in format suitable for plotting tools"""
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plot_file = os.path.join(output_dir, f'plot_data_{timestamp}.csv')
    
    datasets = {
        'ML App': 'ml_app_branch_dataset.csv',
        'I/O Heavy App': 'io_app_branch_dataset.csv',
        'General App': 'general_app_branch_dataset.csv'
    }
    
    print(f"\nExporting plot data to {plot_file}...")
    
    with open(plot_file, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Header
        writer.writerow(['Dataset', 'Predictor', 'Accuracy', 'Misprediction_Rate'])
        
        # Data
        for dataset_name, dataset_file in datasets.items():
            dataset = load_dataset_from_file(dataset_file)
            if dataset is None:
                continue
            
            predictors = get_all_predictors()
            for pred_name, predictor in predictors.items():
                results = evaluate_predictor(predictor, dataset)
                writer.writerow([
                    dataset_name,
                    pred_name,
                    f"{results['accuracy']:.6f}",
                    f"{results['misprediction_rate']:.6f}"
                ])
    
    print(f"Plot data exported to {plot_file}")
    print("\nThis file can be used with plotting tools like:")
    print("  - gnuplot")
    print("  - matplotlib (Python)")
    print("  - ggplot2 (R)")
    print("  - Excel/LibreOffice Calc")
    
    return True


def main():
    """Main export function"""
    print("="*70)
    print("BRANCH PREDICTOR RESULTS EXPORT")
    print("="*70)
    
    # Export detailed results
    export_detailed_results()
    
    # Export for plotting
    export_for_plotting()
    
    print("\n" + "="*70)
    print("Export complete!")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()
