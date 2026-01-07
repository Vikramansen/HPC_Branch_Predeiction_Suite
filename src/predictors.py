from typing import List, Tuple

def always_taken_predictor(dataset: List[Tuple[str, str]]) -> float:
    """
    Always predicts 'taken' for every branch.
    """
    return sum(outcome == 'taken' for _, outcome in dataset) / len(dataset)

def never_taken_predictor(dataset: List[Tuple[str, str]]) -> float:
    """
    Always predicts 'not_taken' for every branch.
    """
    return sum(outcome == 'not_taken' for _, outcome in dataset) / len(dataset)

def bimodal_predictor(dataset: List[Tuple[str, str]], initial_prediction: str = 'taken') -> float:
    """
    Bimodal predictor that maintains a state machine per branch address.
    Uses a 2-bit saturating counter.
    """
    prediction_table = {}
    correct_predictions = 0
    
    for address, outcome in dataset:
        if address not in prediction_table:
            prediction_table[address] = 2 if initial_prediction == 'taken' else 1
        
        prediction = 'taken' if prediction_table[address] >= 2 else 'not_taken'
        correct_predictions += (prediction == outcome)
        
        if outcome == 'taken':
            prediction_table[address] = min(3, prediction_table[address] + 1)
        else:
            prediction_table[address] = max(0, prediction_table[address] - 1)
    
    return correct_predictions / len(dataset)

def gshare_predictor(dataset: List[Tuple[str, str]], history_bits: int = 1) -> float:
    """
    GShare predictor using global history register and pattern table.
    """
    history = 0
    pattern_table = [0] * (2 ** history_bits)
    correct_predictions = 0

    for address, outcome in dataset:
        addr_value = int(address, 16) if isinstance(address, str) and address.startswith('0x') else hash(address)
        index = (addr_value ^ history) & ((2 ** history_bits) - 1)
        
        prediction = 'taken' if pattern_table[index] > 0 else 'not_taken'
        correct_predictions += prediction == outcome
        
        history = ((history << 1) & (2 ** history_bits - 1)) | (1 if outcome == 'taken' else 0)
        pattern_table[index] += 1 if outcome == 'taken' else -1

    return correct_predictions / len(dataset)

def perceptron_predictor(dataset: List[Tuple[str, str]], history_bits: int = 8, threshold: float = 1.5) -> float:
    """
    Perceptron-based branch predictor using machine learning.
    """
    history = 0
    num_perceptrons = 2 ** history_bits
    weights = [[0] * (history_bits + 1) for _ in range(num_perceptrons)]
    correct_predictions = 0

    for address, outcome in dataset:
        addr_value = int(address, 16) if isinstance(address, str) and address.startswith('0x') else hash(address)
        index = addr_value & (num_perceptrons - 1)
        
        x = [1] + [1 if bit == '1' else -1 for bit in bin(history)[2:].zfill(history_bits)]
        y = 1 if outcome == 'taken' else -1
        dot_product = sum(w * x_i for w, x_i in zip(weights[index], x))
        prediction = 'taken' if dot_product > 0 else 'not_taken'
        correct_predictions += (prediction == outcome)
        
        if y * dot_product <= threshold:
            weights[index] = [w + y * x_i for w, x_i in zip(weights[index], x)]
        history = ((history << 1) & (num_perceptrons - 1)) | (1 if outcome == 'taken' else 0)

    return correct_predictions / len(dataset)
