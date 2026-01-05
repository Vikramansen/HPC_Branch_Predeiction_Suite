import csv

# Redefining the load_dataset_from_file function with csv module imported
def load_dataset_from_file(filename):
    dataset = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            address, outcome = row
            dataset.append((address, outcome))
    return dataset

# Redefining the predictor functions
# Always Taken Predictor
def always_taken_predictor(dataset):
    return sum(outcome == 'taken' for _, outcome in dataset) / len(dataset)

# Never Taken Predictor
def never_taken_predictor(dataset):
    return sum(outcome == 'not_taken' for _, outcome in dataset) / len(dataset)

# Bimodal Predictor
def bimodal_predictor(dataset, initial_prediction='taken'):
    prediction = initial_prediction
    correct_predictions = sum(prediction == outcome for _, outcome in dataset)
    return correct_predictions / len(dataset)

# Gshare Predictor
def gshare_predictor(dataset, history_bits=1):
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

# Perceptron Predictor
def perceptron_predictor(dataset, history_bits=8, threshold=1.5):
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

def calculate_accuracies(dataset):
    accuracies = {}
    for name, predictor in predictors.items():
        accuracies[name] = predictor(dataset)
    return accuracies


# Predictor functions dictionary
predictors = {
    "Always Taken": always_taken_predictor,
    "Never Taken": never_taken_predictor,
    "Bimodal": bimodal_predictor,
    "Gshare": gshare_predictor,
    "Perceptron": perceptron_predictor
}

# Load the datasets
ml_app_dataset = load_dataset_from_file('ml_app_branch_dataset.csv')
io_app_dataset = load_dataset_from_file('io_app_branch_dataset.csv')
general_app_dataset = load_dataset_from_file('general_app_branch_dataset.csv')

# Calculate accuracies
ml_app_accuracies = calculate_accuracies(ml_app_dataset)
io_app_accuracies = calculate_accuracies(io_app_dataset)
general_app_accuracies = calculate_accuracies(general_app_dataset)

def print_accuracies(dataset_name, accuracies):
    print(f"Accuracies for {dataset_name} Dataset:")
    for predictor_name, accuracy in accuracies.items():
        print(f"  - {predictor_name}: {accuracy * 100:.2f}%")
    print()

# Print the accuracies for each dataset
print_accuracies("ML App", ml_app_accuracies)
print_accuracies("I/O Heavy App", io_app_accuracies)
print_accuracies("General App", general_app_accuracies)
