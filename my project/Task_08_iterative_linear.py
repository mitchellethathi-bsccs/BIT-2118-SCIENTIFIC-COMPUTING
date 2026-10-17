# Task 08: Iterative Methods for Linear Systems
# B) Solve a diagonally dominant temperature system with Jacobi and Gauss-Seidel.
# C) Compare tolerances and a larger grid.
# D) Print iteration counts and save a semilog convergence plot.
# E) Apply Jacobi to a 20-point heat-transfer grid.

import os
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def jacobi(A, b, tol=1e-8, max_iter=500):
	D = np.diag(A)
	R = A - np.diagflat(D)
	x = np.zeros_like(b)
	errors = []
	for _ in range(max_iter):
		xn = (b - R @ x) / D
		errors.append(np.linalg.norm(xn - x, np.inf))
		if errors[-1] < tol:
			return xn, errors
		x = xn
	return x, errors

def gauss_seidel(A, b, tol=1e-8, max_iter=500):
	x = np.zeros_like(b)
	errors = []
	for _ in range(max_iter):
		old = x.copy()
		for i in range(len(b)):
			x[i] = (b[i] - A[i, :i] @ x[:i] - A[i, i+1:] @ old[i+1:]) / A[i, i]
		errors.append(np.linalg.norm(x - old, np.inf))
		if errors[-1] < tol:
			return x, errors
	return x, errors

A = 2*np.eye(5) - np.diag(np.ones(4), 1) - np.diag(np.ones(4), -1)
b = np.array([100., 0., 0., 0., 20.])
xj, ej = jacobi(A, b)
xg, eg = gauss_seidel(A, b)
print("Jacobi:", np.round(xj, 4), "iterations:", len(ej))
print("Gauss-Seidel:", np.round(xg, 4), "iterations:", len(eg))
print("Direct:", np.linalg.solve(A, b))
for tol in (1e-4, 1e-8, 1e-12):
	print("Tolerance", tol, "iterations:", len(jacobi(A, b, tol)[1]), len(gauss_seidel(A, b, tol)[1]))
plt.figure()
plt.semilogy(ej, label="Jacobi")
plt.semilogy(eg, label="Gauss-Seidel")
plt.xlabel("Iteration"); plt.ylabel("Maximum change")
plt.title("Task 08 convergence"); plt.legend(); plt.grid(True)
figs = Path(__file__).resolve().parent / "outputs" / "figs"
figs.mkdir(parents=True, exist_ok=True)
plt.savefig(figs / "Task_08_convergence.png", dpi=120, bbox_inches="tight")
plt.show()
n = 20
A20 = 2*np.eye(n) - np.diag(np.ones(n-1), 1) - np.diag(np.ones(n-1), -1)
b20 = np.zeros(n); b20[0] = 100.; b20[-1] = 20.
x20, e20 = jacobi(A20, b20)
print("20-point iterations:", len(e20), "max direct error:", np.max(np.abs(x20 - np.linalg.solve(A20, b20))))
