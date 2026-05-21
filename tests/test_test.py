import sys
import os
sys.path.insert(0, os.path.abspath('app'))
from test import find_max

def test_first_greatest():
    assert find_max(10, 5, 3) == 10

def test_second_greatest():
    assert find_max(3, 9, 1) == 9

def test_third_greatest():
    assert find_max(2, 4, 7) == 7

def test_all_equal():
    assert find_max(5, 5, 5) == 5

def test_negative_numbers():
    assert find_max(-1, -5, -10) == -1

def test_with_zero():
    assert find_max(0, 0, 1) == 1
