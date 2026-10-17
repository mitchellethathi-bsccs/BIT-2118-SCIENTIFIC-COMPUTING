# Task 07: Gaussian Elimination and LU Decomposition
# B) Factor a fixed 3x3 coefficient matrix once and solve three measurement vectors.
# C) Compare LU reuse and repeated direct solves for 50 right-hand sides.
# D) Report solutions, residuals, and timings.
# E) Apply LU reuse to quarterly Leontief input-output demand.

import timeit
import numpy as np
from scipy.linalg import lu_factor, lu_solve

A = np.array([[4., -1., 0.], [-1., 4., -1.], [0., -1., 3.]])
measurements = [np.array(v) for v in ([15., 10., 10.], [16., 11., 9.], [14., 12., 11.])]
lu, piv = lu_factor(A)
for i, b in enumerate(measurements, 1):
	x = lu_solve((lu, piv), b)
	print(f"Measurement {i}: x={x}, residual={np.linalg.norm(b - A @ x):.2e}")
print("Direct solution:", np.linalg.solve(A, measurements[0]))

rng = np.random.default_rng(0)
n = 8
A_big = rng.normal(size=(n, n)) + n * np.eye(n)
bs = [rng.normal(size=n) for _ in range(50)]
def lu_reuse():
	factors = lu_factor(A_big)
	return [lu_solve(factors, b) for b in bs]
def direct_each():
	return [np.linalg.solve(A_big, b) for b in bs]
print("LU reuse:", timeit.timeit(lu_reuse, number=100) / 100)
print("Direct solves:", timeit.timeit(direct_each, number=100) / 100)

A_io = np.array([[.2, .3, .1], [.1, .2, .3], [.2, .1, .2]])
M = np.eye(3) - A_io
factors = lu_factor(M)
quarters = {"Q1": [100., 60., 80.], "Q2": [120., 55., 90.], "Q3": [90., 70., 75.]}
for quarter, demand in quarters.items():
	d = np.array(demand)
	x = lu_solve(factors, d)
	print(f"{quarter}: output={np.round(x, 2)}, residual={np.linalg.norm(d - M @ x):.1e}")
