# Requirements Traceability Matrix (RTM)

## R1: Language Detection
- System must detect Python (.py) files
- System must detect C (.c) files

## R2: Complexity Analysis
- Python files must be analyzed using Radon
- C files must be analyzed using Lizard
- Cyclomatic complexity must not exceed 10

## R3: Test Generation
- System must generate test cases automatically
- Test cases must cover all branches
- Python tests must use pytest
- C tests must use GTest

## R4: Code Coverage
- Python coverage must use coverage.py
- C coverage must use gcov and lcov
- Minimum coverage must be 80%

## R5: Performance
- CPU utilization must be checked using RMA
- RMA threshold for 3 tasks is 77.98%
- Execution time must be under 1 second

## R6: PR Decision
- APPROVE if all checks pass
- REQUEST_CHANGES if any check fails
- Suggest fixes to developer

