# test_math_operations.py

from nlp_module.utils.math_operations import add_numbers

def test_add_numbers():
    assert add_numbers(1, 2) == 3
    assert add_numbers(-1, 1) == 0
    assert add_numbers(0, 0) == 0
    assert add_numbers(2, 3) == 5
