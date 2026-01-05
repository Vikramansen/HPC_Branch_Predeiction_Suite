"""
Branch Predictor Implementations
This module contains various branch predictor algorithms including:
- Static predictors (Always Taken, Never Taken)
- Dynamic predictors (Bimodal, GShare, Perceptron, TAGE)
"""


class BranchPredictor:
    """Base class for branch predictors"""
    
    def __init__(self, name):
        self.name = name
        self.correct_predictions = 0
        self.total_predictions = 0
    
    def predict(self, address, history=None):
        """
        Make a prediction for a branch
        
        Args:
            address: Branch address (string or int)
            history: Optional global history (for predictors that use it)
            
        Returns:
            str: 'taken' or 'not_taken'
        """
        raise NotImplementedError
    
    def update(self, address, actual_outcome, history=None):
        """
        Update predictor state based on actual outcome
        
        Args:
            address: Branch address (string or int)
            actual_outcome: Actual branch outcome ('taken' or 'not_taken')
            history: Optional global history (for predictors that use it)
        """
        raise NotImplementedError
    
    def get_accuracy(self):
        """Calculate prediction accuracy"""
        if self.total_predictions == 0:
            return 0.0
        return self.correct_predictions / self.total_predictions
    
    def reset(self):
        """Reset predictor state"""
        self.correct_predictions = 0
        self.total_predictions = 0


class AlwaysTakenPredictor(BranchPredictor):
    """Always predicts branches as taken"""
    
    def __init__(self):
        super().__init__("Always Taken")
    
    def predict(self, address, history=None):
        return 'taken'
    
    def update(self, address, actual_outcome, history=None):
        self.total_predictions += 1
        if actual_outcome == 'taken':
            self.correct_predictions += 1


class NeverTakenPredictor(BranchPredictor):
    """Always predicts branches as not taken"""
    
    def __init__(self):
        super().__init__("Never Taken")
    
    def predict(self, address, history=None):
        return 'not_taken'
    
    def update(self, address, actual_outcome, history=None):
        self.total_predictions += 1
        if actual_outcome == 'not_taken':
            self.correct_predictions += 1


class BimodalPredictor(BranchPredictor):
    """
    Bimodal predictor using a table of 2-bit saturating counters
    Each branch address maps to a counter that predicts based on past behavior
    """
    
    def __init__(self, table_size=1024):
        super().__init__("Bimodal")
        self.table_size = table_size
        self.table = [1] * table_size  # Initialize to weakly taken (state 1)
    
    def _get_index(self, address):
        """Hash the address to table index"""
        if isinstance(address, str):
            address = int(address, 16) if address.startswith('0x') else int(address)
        return address % self.table_size
    
    def predict(self, address, history=None):
        index = self._get_index(address)
        # 2-bit counter: 0,1 = not taken, 2,3 = taken
        return 'taken' if self.table[index] >= 2 else 'not_taken'
    
    def update(self, address, actual_outcome, history=None):
        index = self._get_index(address)
        
        # Make prediction before update
        prediction = 'taken' if self.table[index] >= 2 else 'not_taken'
        
        self.total_predictions += 1
        if prediction == actual_outcome:
            self.correct_predictions += 1
        
        # Update counter
        if actual_outcome == 'taken':
            self.table[index] = min(3, self.table[index] + 1)
        else:
            self.table[index] = max(0, self.table[index] - 1)
    
    def reset(self):
        super().reset()
        self.table = [1] * self.table_size


class GSharePredictor(BranchPredictor):
    """
    GShare predictor combines branch address with global history
    Uses XOR of address and history to index into pattern table
    """
    
    def __init__(self, history_bits=10, table_size=1024):
        super().__init__("GShare")
        self.history_bits = history_bits
        self.table_size = table_size
        self.history = 0
        self.table = [1] * table_size  # 2-bit saturating counters
    
    def _get_index(self, address):
        """XOR address with history to get table index"""
        if isinstance(address, str):
            address = int(address, 16) if address.startswith('0x') else int(address)
        return (address ^ self.history) % self.table_size
    
    def predict(self, address, history=None):
        index = self._get_index(address)
        return 'taken' if self.table[index] >= 2 else 'not_taken'
    
    def update(self, address, actual_outcome, history=None):
        index = self._get_index(address)
        
        # Make prediction before update
        prediction = 'taken' if self.table[index] >= 2 else 'not_taken'
        
        self.total_predictions += 1
        if prediction == actual_outcome:
            self.correct_predictions += 1
        
        # Update counter
        if actual_outcome == 'taken':
            self.table[index] = min(3, self.table[index] + 1)
        else:
            self.table[index] = max(0, self.table[index] - 1)
        
        # Update global history
        self.history = ((self.history << 1) | (1 if actual_outcome == 'taken' else 0)) & ((1 << self.history_bits) - 1)
    
    def reset(self):
        super().reset()
        self.history = 0
        self.table = [1] * self.table_size


class PerceptronPredictor(BranchPredictor):
    """
    Perceptron-based branch predictor
    Uses neural network concept with weights for history bits
    """
    
    def __init__(self, history_length=8, table_size=256, threshold=1.5):
        super().__init__("Perceptron")
        self.history_length = history_length
        self.table_size = table_size
        self.threshold = threshold
        self.history = 0
        # Initialize weights table: each entry has (history_length + 1) weights
        self.weights = [[0] * (history_length + 1) for _ in range(table_size)]
    
    def _get_index(self, address):
        """Hash address to get perceptron index"""
        if isinstance(address, str):
            address = int(address, 16) if address.startswith('0x') else int(address)
        return address % self.table_size
    
    def _compute_output(self, index):
        """Compute perceptron output"""
        # Bias weight
        output = self.weights[index][0]
        
        # Add weighted sum of history bits
        for i in range(self.history_length):
            bit = (self.history >> i) & 1
            weight = self.weights[index][i + 1]
            output += weight * (1 if bit else -1)
        
        return output
    
    def predict(self, address, history=None):
        index = self._get_index(address)
        output = self._compute_output(index)
        return 'taken' if output >= 0 else 'not_taken'
    
    def update(self, address, actual_outcome, history=None):
        index = self._get_index(address)
        output = self._compute_output(index)
        
        # Make prediction before update
        prediction = 'taken' if output >= 0 else 'not_taken'
        
        self.total_predictions += 1
        if prediction == actual_outcome:
            self.correct_predictions += 1
        
        # Update weights if prediction was wrong or output magnitude is below threshold
        actual = 1 if actual_outcome == 'taken' else -1
        if (actual * output <= self.threshold):
            # Update bias
            self.weights[index][0] += actual
            
            # Update history weights
            for i in range(self.history_length):
                bit = (self.history >> i) & 1
                self.weights[index][i + 1] += actual * (1 if bit else -1)
        
        # Update history
        self.history = ((self.history << 1) | (1 if actual_outcome == 'taken' else 0)) & ((1 << self.history_length) - 1)
    
    def reset(self):
        super().reset()
        self.history = 0
        self.weights = [[0] * (self.history_length + 1) for _ in range(self.table_size)]


class TAGEPredictor(BranchPredictor):
    """
    TAGE (TAgged GEometric history length) predictor
    Uses multiple tables with different history lengths
    Implements a simplified version of the TAGE algorithm
    """
    
    def __init__(self, num_tables=4, base_table_size=1024):
        super().__init__("TAGE")
        self.num_tables = num_tables
        self.base_table_size = base_table_size
        
        # Base predictor (bimodal)
        self.base_table = [1] * base_table_size
        
        # Tagged tables with geometric history lengths
        self.tagged_tables = []
        self.history_lengths = []
        
        for i in range(num_tables):
            # Geometric history length: 2, 4, 8, 16, etc.
            history_len = 2 ** (i + 1)
            self.history_lengths.append(history_len)
            
            # Each entry: [counter, tag, useful]
            table = [[1, 0, 0] for _ in range(base_table_size)]
            self.tagged_tables.append(table)
        
        self.global_history = 0
        self.max_history = self.history_lengths[-1] if self.history_lengths else 0
    
    def _get_base_index(self, address):
        """Get index for base predictor"""
        if isinstance(address, str):
            address = int(address, 16) if address.startswith('0x') else int(address)
        return address % self.base_table_size
    
    def _get_tag(self, address, history_len):
        """Compute tag for tagged table"""
        if isinstance(address, str):
            address = int(address, 16) if address.startswith('0x') else int(address)
        # Simple tag computation
        history_mask = (1 << history_len) - 1
        hist = self.global_history & history_mask
        return (address ^ hist) % 256
    
    def _get_index(self, address, table_id):
        """Get index for tagged table"""
        if isinstance(address, str):
            address = int(address, 16) if address.startswith('0x') else int(address)
        history_len = self.history_lengths[table_id]
        history_mask = (1 << history_len) - 1
        hist = self.global_history & history_mask
        return (address ^ hist) % self.base_table_size
    
    def predict(self, address, history=None):
        # Check tagged tables from longest to shortest history
        for i in range(self.num_tables - 1, -1, -1):
            index = self._get_index(address, i)
            tag = self._get_tag(address, self.history_lengths[i])
            
            entry = self.tagged_tables[i][index]
            if entry[1] == tag:  # Tag match
                return 'taken' if entry[0] >= 2 else 'not_taken'
        
        # No match in tagged tables, use base predictor
        base_index = self._get_base_index(address)
        return 'taken' if self.base_table[base_index] >= 2 else 'not_taken'
    
    def update(self, address, actual_outcome, history=None):
        # Find the matching table (provider) and make prediction
        provider_table = -1
        provider_index = -1
        prediction = None
        
        for i in range(self.num_tables - 1, -1, -1):
            index = self._get_index(address, i)
            tag = self._get_tag(address, self.history_lengths[i])
            
            if self.tagged_tables[i][index][1] == tag:
                provider_table = i
                provider_index = index
                prediction = 'taken' if self.tagged_tables[i][index][0] >= 2 else 'not_taken'
                break
        
        # If no match, use base predictor
        if prediction is None:
            base_index = self._get_base_index(address)
            prediction = 'taken' if self.base_table[base_index] >= 2 else 'not_taken'
        
        self.total_predictions += 1
        if prediction == actual_outcome:
            self.correct_predictions += 1
        
        # Update the provider
        if provider_table >= 0:
            # Update counter
            entry = self.tagged_tables[provider_table][provider_index]
            if actual_outcome == 'taken':
                entry[0] = min(3, entry[0] + 1)
            else:
                entry[0] = max(0, entry[0] - 1)
        else:
            # Update base predictor
            base_index = self._get_base_index(address)
            if actual_outcome == 'taken':
                self.base_table[base_index] = min(3, self.base_table[base_index] + 1)
            else:
                self.base_table[base_index] = max(0, self.base_table[base_index] - 1)
        
        # Allocate new entry if prediction was wrong
        if prediction != actual_outcome:
            # Try to allocate in a table with longer history than provider
            for i in range(self.num_tables - 1, provider_table, -1):
                index = self._get_index(address, i)
                tag = self._get_tag(address, self.history_lengths[i])
                
                # Simple allocation: replace if useful bit is 0
                if self.tagged_tables[i][index][2] == 0:
                    self.tagged_tables[i][index] = [2 if actual_outcome == 'taken' else 1, tag, 0]
                    break
        
        # Update global history
        if self.max_history > 0:
            self.global_history = ((self.global_history << 1) | (1 if actual_outcome == 'taken' else 0)) & ((1 << self.max_history) - 1)
    
    def reset(self):
        super().reset()
        self.base_table = [1] * self.base_table_size
        for i in range(self.num_tables):
            self.tagged_tables[i] = [[1, 0, 0] for _ in range(self.base_table_size)]
        self.global_history = 0


def get_all_predictors():
    """Returns a dictionary of all available predictors"""
    return {
        'Always Taken': AlwaysTakenPredictor(),
        'Never Taken': NeverTakenPredictor(),
        'Bimodal': BimodalPredictor(),
        'GShare': GSharePredictor(),
        'Perceptron': PerceptronPredictor(),
        'TAGE': TAGEPredictor()
    }
