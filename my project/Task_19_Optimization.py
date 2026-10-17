"""BIT 2118 Task 19: Numerical Optimization.
Real-world case: minimize cloud-server operating cost subject to a capacity requirement."""
import numpy as np
from scipy.optimize import minimize

print("=== TASK 19: Numerical Optimization ===")

def cost(z):
	x, y = z
	return 12 * x + 18 * y

def capacity_constraint(z):
	x, y = z
	return 100 * x + 170 * y - 1000     # >= 0

constraints = {"type": "ineq", "fun": capacity_constraint}
bounds = [(0, None), (0, None)]
solution = minimize(cost, x0=[5, 3], method="SLSQP", bounds=bounds, constraints=constraints)
x, y = solution.x

print("[B] Inputs: linear cost 12x + 18y, capacity constraint 100x + 170y >= 1000, x,y >= 0. Operation: constrained minimization (SLSQP).")
print(f"[D] Optimization success: {solution.success}")
print(f"[D] Type A allocation: {x:.3f}")
print(f"[D] Type B allocation: {y:.3f}")
print(f"[D] Total capacity   : {100*x + 170*y:.2f}")
print(f"[D] Minimum planning cost: {solution.fun:.2f}")
print("[D] Interpretation: Type B wins entirely (5.882 units). Per unit of capacity, A costs 12/100 = 0.12")
print("    and B costs 18/170 = 0.106, so B is the cheaper way to buy capacity; the constraint is active (capacity = 1000 exactly).")

best_integer = None
for a in range(0, 20):
	for b in range(0, 20):
		cap = 100 * a + 170 * b
		if cap >= 1000:
			c = 12 * a + 18 * b
			if best_integer is None or c < best_integer[0]:
				best_integer = (c, a, b, cap)
print("Best nearby integer solution (cost, A, B, capacity):", best_integer)

# [C] Parameter change: capacity requirement raised to 1500
def cap1500(z):
	return 100 * z[0] + 170 * z[1] - 1500
sol2 = minimize(cost, x0=[5, 5], method="SLSQP", bounds=bounds,
				constraints={"type": "ineq", "fun": cap1500})
print(f"[C] If capacity must be >= 1500: A = {sol2.x[0]:.3f}, B = {sol2.x[1]:.3f}, "
	  f"cost = {sol2.fun:.2f} (cost grows linearly with demand)")

# [E] Modified case: least-cost animal-feed blend
print("\n[E] Modified case: minimize feed cost 3x + 4y (x = kg of feed A, y = kg of feed B)")
print("    subject to protein 2x + y >= 8 and fibre x + 2y >= 6, x,y >= 0")
def feed_cost(z):
	return 3 * z[0] + 4 * z[1]
cons = [{"type": "ineq", "fun": lambda z: 2*z[0] + z[1] - 8},
		{"type": "ineq", "fun": lambda z: z[0] + 2*z[1] - 6}]
sol3 = minimize(feed_cost, x0=[3, 3], method="SLSQP", bounds=bounds, constraints=cons)
print(f"    Optimal blend: {sol3.x[0]:.3f} kg A + {sol3.x[1]:.3f} kg B; minimum cost = {sol3.fun:.2f}")
print(f"    Check constraints: protein = {2*sol3.x[0] + sol3.x[1]:.3f} (>= 8), fibre = {sol3.x[0] + 2*sol3.x[1]:.3f} (>= 6)")
