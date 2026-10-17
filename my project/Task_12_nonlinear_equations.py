# Task 12: Polynomial and Nonlinear Equation Solving
# B) Solve for circle-parabola intersections using scipy.optimize.root.
# C) Change the circle radius and search from multiple starting guesses.
# D) Print intersection points and residuals.
# E) Solve a chemical-equilibrium composition equation.

import numpy as np
from scipy.optimize import root

def equations(z):
	x, y = z
	return [x*x + y*y - 4, y - (x*x - 1)]
for guess in ([1., 1.], [-1., 1.]):
	result = root(equations, guess)
	print("Guess:", guess, "intersection:", result.x, "residual:", equations(result.x), "success:", result.success)
def equations_r3(z):
	x, y = z
	return [x*x + y*y - 9, y - (x*x - 1)]
found = set()
for guess in ([2., 2.], [-2., 2.], [0., 3.], [0., -3.]):
	result = root(equations_r3, guess)
	if result.success:
		point = tuple(np.round(result.x, 6))
		if point not in found:
			found.add(point); print("Radius 3:", point)
eq = root(lambda x: 4*x**2 + x - 1, [.3]).x[0]
print("Equilibrium extent:", eq, "mol A2:", 1-eq, "mol A:", 2*eq)
print("Equilibrium constant check:", 4*eq**2/(1-eq))
