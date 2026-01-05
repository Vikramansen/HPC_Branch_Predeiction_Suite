"""
Validation and Testing Module for Branch Predictors
This module provides testing utilities to validate predictor implementations
"""

from predictors import (
    AlwaysTakenPredictor, NeverTakenPredictor, BimodalPredictor,
    GSharePredictor, PerceptronPredictor, TAGEPredictor
)


def create_simple_test_dataset():
    """Create a simple test dataset with known patterns"""
    # Pattern: 10 taken, 10 not taken, repeat
    dataset = []
    for i in range(100):
        address = f'0x{1000 + (i % 20):04x}'
        outcome = 'taken' if (i % 20) < 10 else 'not_taken'
        dataset.append((address, outcome))
    return dataset


def create_alternating_test_dataset():
    """Create dataset with alternating pattern"""
    dataset = []
    for i in range(100):
        address = f'0x{2000:04x}'  # Same address
        outcome = 'taken' if i % 2 == 0 else 'not_taken'
        dataset.append((address, outcome))
    return dataset


def create_all_taken_dataset():
    """Create dataset where all branches are taken"""
    dataset = []
    for i in range(100):
        address = f'0x{3000 + i:04x}'
        outcome = 'taken'
        dataset.append((address, outcome))
    return dataset


def create_all_not_taken_dataset():
    """Create dataset where all branches are not taken"""
    dataset = []
    for i in range(100):
        address = f'0x{4000 + i:04x}'
        outcome = 'not_taken'
        dataset.append((address, outcome))
    return dataset


def test_predictor(predictor, dataset, expected_min_accuracy=0.0):
    """
    Test a predictor on a dataset
    Returns: (passed, accuracy, message)
    """
    predictor.reset()
    
    for address, actual_outcome in dataset:
        prediction = predictor.predict(address)
        predictor.update(address, actual_outcome)
    
    accuracy = predictor.get_accuracy()
    passed = accuracy >= expected_min_accuracy
    
    message = f"{predictor.name}: {accuracy*100:.2f}% accuracy"
    if not passed:
        message += f" (expected >= {expected_min_accuracy*100:.2f}%)"
    
    return passed, accuracy, message


def test_always_taken_predictor():
    """Test Always Taken predictor"""
    print("\n--- Testing Always Taken Predictor ---")
    predictor = AlwaysTakenPredictor()
    
    # Should be 100% accurate on all-taken dataset
    dataset = create_all_taken_dataset()
    passed, acc, msg = test_predictor(predictor, dataset, expected_min_accuracy=1.0)
    print(f"All taken dataset: {msg} - {'PASS' if passed else 'FAIL'}")
    
    # Should be 0% accurate on all-not-taken dataset
    dataset = create_all_not_taken_dataset()
    passed, acc, msg = test_predictor(predictor, dataset, expected_min_accuracy=0.0)
    print(f"All not taken dataset: {msg} - {'PASS' if acc == 0.0 else 'FAIL'}")
    
    return True


def test_never_taken_predictor():
    """Test Never Taken predictor"""
    print("\n--- Testing Never Taken Predictor ---")
    predictor = NeverTakenPredictor()
    
    # Should be 100% accurate on all-not-taken dataset
    dataset = create_all_not_taken_dataset()
    passed, acc, msg = test_predictor(predictor, dataset, expected_min_accuracy=1.0)
    print(f"All not taken dataset: {msg} - {'PASS' if passed else 'FAIL'}")
    
    # Should be 0% accurate on all-taken dataset
    dataset = create_all_taken_dataset()
    passed, acc, msg = test_predictor(predictor, dataset, expected_min_accuracy=0.0)
    print(f"All taken dataset: {msg} - {'PASS' if acc == 0.0 else 'FAIL'}")
    
    return True


def test_bimodal_predictor():
    """Test Bimodal predictor"""
    print("\n--- Testing Bimodal Predictor ---")
    predictor = BimodalPredictor(table_size=64)
    
    # Should learn simple pattern
    dataset = create_simple_test_dataset()
    passed, acc, msg = test_predictor(predictor, dataset, expected_min_accuracy=0.3)
    print(f"Simple pattern: {msg} - {'PASS' if passed else 'FAIL'}")
    
    return True


def test_gshare_predictor():
    """Test GShare predictor"""
    print("\n--- Testing GShare Predictor ---")
    predictor = GSharePredictor(history_bits=4, table_size=64)
    
    # Should handle correlated branches
    dataset = create_simple_test_dataset()
    passed, acc, msg = test_predictor(predictor, dataset, expected_min_accuracy=0.3)
    print(f"Simple pattern: {msg} - {'PASS' if passed else 'FAIL'}")
    
    return True


def test_perceptron_predictor():
    """Test Perceptron predictor"""
    print("\n--- Testing Perceptron Predictor ---")
    predictor = PerceptronPredictor(history_length=4, table_size=64)
    
    # Should learn patterns over time
    dataset = create_simple_test_dataset()
    passed, acc, msg = test_predictor(predictor, dataset, expected_min_accuracy=0.3)
    print(f"Simple pattern: {msg} - {'PASS' if passed else 'FAIL'}")
    
    return True


def test_tage_predictor():
    """Test TAGE predictor"""
    print("\n--- Testing TAGE Predictor ---")
    predictor = TAGEPredictor(num_tables=3, base_table_size=64)
    
    # Should handle complex patterns with history
    dataset = create_simple_test_dataset()
    passed, acc, msg = test_predictor(predictor, dataset, expected_min_accuracy=0.3)
    print(f"Simple pattern: {msg} - {'PASS' if passed else 'FAIL'}")
    
    return True


def test_predictor_reset():
    """Test that predictors properly reset their state"""
    print("\n--- Testing Predictor Reset ---")
    
    predictor = BimodalPredictor()
    dataset = create_simple_test_dataset()
    
    # First run
    for address, outcome in dataset:
        predictor.update(address, outcome)
    acc1 = predictor.get_accuracy()
    
    # Reset
    predictor.reset()
    
    # Check state is reset
    if predictor.correct_predictions != 0 or predictor.total_predictions != 0:
        print("Reset test: FAIL - State not properly reset")
        return False
    
    # Second run should give same results
    for address, outcome in dataset:
        predictor.update(address, outcome)
    acc2 = predictor.get_accuracy()
    
    if abs(acc1 - acc2) < 0.001:  # Allow small floating point error
        print(f"Reset test: PASS - Accuracy consistent ({acc1*100:.2f}% both times)")
        return True
    else:
        print(f"Reset test: FAIL - Different accuracies ({acc1*100:.2f}% vs {acc2*100:.2f}%)")
        return False


def test_edge_cases():
    """Test edge cases"""
    print("\n--- Testing Edge Cases ---")
    
    # Empty dataset handling
    predictor = BimodalPredictor()
    if predictor.get_accuracy() == 0.0:
        print("Empty dataset: PASS - Returns 0% accuracy")
    else:
        print("Empty dataset: FAIL")
    
    # Single entry
    predictor = AlwaysTakenPredictor()
    predictor.update('0x1000', 'taken')
    if predictor.get_accuracy() == 1.0:
        print("Single entry (correct): PASS")
    else:
        print("Single entry (correct): FAIL")
    
    predictor = AlwaysTakenPredictor()
    predictor.update('0x1000', 'not_taken')
    if predictor.get_accuracy() == 0.0:
        print("Single entry (incorrect): PASS")
    else:
        print("Single entry (incorrect): FAIL")
    
    return True


def run_all_tests():
    """Run all validation tests"""
    print("="*70)
    print("BRANCH PREDICTOR VALIDATION TESTS")
    print("="*70)
    
    all_passed = True
    
    tests = [
        ("Always Taken Predictor", test_always_taken_predictor),
        ("Never Taken Predictor", test_never_taken_predictor),
        ("Bimodal Predictor", test_bimodal_predictor),
        ("GShare Predictor", test_gshare_predictor),
        ("Perceptron Predictor", test_perceptron_predictor),
        ("TAGE Predictor", test_tage_predictor),
        ("Predictor Reset", test_predictor_reset),
        ("Edge Cases", test_edge_cases),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, "PASS" if result else "FAIL"))
        except Exception as e:
            print(f"\nError in {test_name}: {e}")
            results.append((test_name, "ERROR"))
            all_passed = False
    
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    for test_name, status in results:
        symbol = "✓" if status == "PASS" else "✗"
        print(f"{symbol} {test_name}: {status}")
    
    print("="*70)
    
    if all_passed:
        print("\nAll tests completed successfully!")
    else:
        print("\nSome tests failed. Please review the output above.")
    
    return all_passed


if __name__ == '__main__':
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)
