import random
from typing import List, Tuple

def generate_ml_app_dataset(size: int = 1000) -> List[Tuple[str, str]]:
    """
    Generate a dataset for ML-based applications.
    Simulates training/inference cycles with repetitive patterns.
    """
    dataset = []
    for i in range(size):
        branch_address = f'0x{2000 + i:04x}'
        
        if i % 20 < 15:
            outcome = 'taken'
        else:
            outcome = 'not_taken'
            
        if random.random() < 0.05:
            outcome = 'taken' if random.random() < 0.7 else 'not_taken'
            
        dataset.append((branch_address, outcome))
    return dataset

def generate_io_app_dataset(size: int = 1000) -> List[Tuple[str, str]]:
    """
    Generate a dataset for I/O-heavy applications.
    Simulates distinct phases (e.g. checking status vs processing).
    """
    dataset = []
    for i in range(size):
        branch_address = f'0x{3000 + i:04x}'
        
        if i % 25 < 5:
            outcome = 'not_taken'
        else:
            outcome = 'taken'
            
        if random.random() < 0.15:
            outcome = 'taken' if random.random() < 0.5 else 'not_taken'
            
        dataset.append((branch_address, outcome))
    return dataset

def generate_general_app_dataset(size: int = 1000) -> List[Tuple[str, str]]:
    """
    Generate a dataset for general applications.
    Mixed behavior.
    """
    dataset = []
    for i in range(size):
        branch_address = f'0x{4000 + i:04x}'
        outcome = 'taken' if random.random() < 0.6 else 'not_taken'
        dataset.append((branch_address, outcome))
    return dataset
