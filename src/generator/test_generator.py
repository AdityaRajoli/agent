import os

def load_context(folder_path):
    context = ""
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as f:
                    context += f.read() + "\n"
    return context

def generate_tests(constraints, rtm_path, pcm_path):
    rtm_context = load_context(rtm_path)
    pcm_context = load_context(pcm_path)

    generated_test_files = []
    os.makedirs("tests", exist_ok=True)

    for filepath, details in constraints.items():
        lang = details.get('lang')

        if lang == "python":
            print(f"Generating pytest tests for {filepath}...")
            test_code = generate_python_tests(filepath, details)
            test_filename = f"tests/test_{os.path.basename(filepath)}"
            with open(test_filename, "w") as f:
                f.write(test_code)
            generated_test_files.append(test_filename)

        elif lang == "c":
            print(f"Generating GTest tests for {filepath}...")
            test_code = generate_c_tests(filepath, details)
            test_filename = f"tests/test_{os.path.basename(filepath).replace('.c', '.cpp')}"
            with open(test_filename, "w") as f:
                f.write(test_code)
            generated_test_files.append(test_filename)

    return generated_test_files

def generate_python_tests(filepath, details):
    funcs     = details.get('functions', [])
    func_name = funcs[0] if funcs else "find_max"
    module    = os.path.basename(filepath).replace('.py', '')

    return f"""import sys
import os
sys.path.insert(0, os.path.abspath('app'))
from {module} import {func_name}

def test_first_greatest():
    assert {func_name}(10, 5, 3) == 10

def test_second_greatest():
    assert {func_name}(3, 9, 1) == 9

def test_third_greatest():
    assert {func_name}(2, 4, 7) == 7

def test_all_equal():
    assert {func_name}(5, 5, 5) == 5

def test_negative_numbers():
    assert {func_name}(-1, -5, -10) == -1

def test_with_zero():
    assert {func_name}(0, 0, 1) == 1
"""

def generate_c_tests(filepath, details):
    return """#include <gtest/gtest.h>

extern "C" {
    int find_max(int a, int b, int c);
}

TEST(AutoTest, Case1) { EXPECT_EQ(find_max(10, 5, 3),  10); }
TEST(AutoTest, Case2) { EXPECT_EQ(find_max(3, 9, 1),    9); }
TEST(AutoTest, Case3) { EXPECT_EQ(find_max(2, 4, 7),    7); }
TEST(AutoTest, Case4) { EXPECT_EQ(find_max(5, 5, 5),    5); }
TEST(AutoTest, Case5) { EXPECT_EQ(find_max(-1, -5, -10),-1); }
TEST(AutoTest, Case6) { EXPECT_EQ(find_max(0, 0, 1),    1); }
"""
