import csv
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

def save_dataset_to_file(dataset: List[Tuple[str, str]], filename: str) -> str:
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
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        
        with open(filename, 'w', newline='') as file:  # newline='' for csv module
            writer = csv.writer(file)
            writer.writerow(["address", "outcome"])
            writer.writerows(dataset)
            
        print(f"✓ Successfully saved {len(dataset)} samples to {filename}")
        return filename
    except IOError as e:
        print(f"✗ Error saving dataset to {filename}: {e}", file=sys.stderr)
        raise

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
