# Assignment 1 - Optimization Methods

**Student:** Srinath Kalvala  
**Roll No.:** 2501AI44

## Contents
- `big_m.py` - Big-M Simplex Method
- `vam.py` - Vogel's Approximation Method (VAM)
- `modi.py` - MODI transportation optimality method
- Output text files and screenshot-style code/output images
- `Assignment_1_Optimization.pdf` - submission-ready report

## Case studies

### Big-M
Maximize:
Z = 3x1 + 5x2

Subject to:
x1 + 2x2 <= 8
3x1 + 2x2 >= 12
x1, x2 >= 0

Result:
x1 = 8, x2 = 0, Z = 24

### Transportation
Cost matrix:
[[16, 16, 29, 24],
 [25, 28, 19,  2],
 [ 1, 25, 13, 11]]

Supply = [18, 25, 12]
Demand = [17, 12, 12, 14]

VAM initial cost = 550
MODI optimal cost = 549
Final allocation:
[[6, 12, 0, 0],
 [0, 0, 11, 14],
 [11, 0, 1, 0]]
