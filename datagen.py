import random

# Function to generate a dataset for an ML-based app
def generate_ml_app_dataset(size=1000):
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

# Function to generate a dataset for an I/O heavy app
def generate_io_app_dataset(size=1000):
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

# Function to generate a dataset for a general app
def generate_general_app_dataset(size=1000):
    dataset = []
    for i in range(size):
        branch_address = f'0x{4000 + i:04x}'

        # Random and less predictable
        outcome = 'taken' if random.random() < 0.6 else 'not_taken'

        dataset.append((branch_address, outcome))

    return dataset


def save_dataset_to_file(dataset, filename):
    with open(f'{filename}', 'w') as file:
        for address, outcome in dataset:
            file.write(f"{address},{outcome}\n")
    return filename


def main():
    """Main function to generate all datasets"""
    # Generate the datasets
    ml_app_dataset = generate_ml_app_dataset(size=2000)
    io_app_dataset = generate_io_app_dataset(size=2000)
    general_app_dataset = generate_general_app_dataset(size=2000)
    
    # Save the datasets to files
    ml_app_dataset_filename = save_dataset_to_file(ml_app_dataset, "ml_app_branch_dataset.csv")
    io_app_dataset_filename = save_dataset_to_file(io_app_dataset, "io_app_branch_dataset.csv")
    general_app_dataset_filename = save_dataset_to_file(general_app_dataset, "general_app_branch_dataset.csv")
    
    return (ml_app_dataset_filename, io_app_dataset_filename, general_app_dataset_filename)


if __name__ == '__main__':
    main()

