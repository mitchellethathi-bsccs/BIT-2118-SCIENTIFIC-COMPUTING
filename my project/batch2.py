"""Generate the Batch 2 numerical-method task scripts (Tasks 07–12)."""

from pathlib import Path


HEADER = """# {title}
# {B}
# {C}
# {D}
# {E}
"""


def w(filename, content):
	Path(filename).write_text(content, encoding="utf-8")


# ---------------- Task 07 ----------------
w("Task_07_gaussian_lu.py", HEADER.format(
	title="Task 07: Gaussian Elimination and LU Decomposition",
	B="B) Factor a fixed 3x3 coefficient matrix once and solve three measurement vectors.",
	C="C) Compare LU reuse and repeated direct solves for 50 right-hand sides.",
	D="D) Report solutions, residuals, and timings.",
	E="E) Apply LU reuse to quarterly Leontief input-output demand.") + '''
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
''')

# ---------------- Task 08 ----------------
w("Task_08_iterative_linear.py", HEADER.format(
	title="Task 08: Iterative Methods for Linear Systems",
	B="B) Solve a diagonally dominant temperature system with Jacobi and Gauss-Seidel.",
	C="C) Compare tolerances and a larger grid.",
	D="D) Print iteration counts and save a semilog convergence plot.",
	E="E) Apply Jacobi to a 20-point heat-transfer grid.") + '''
import os
import numpy as np
import matplotlib.pyplot as plt

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
figs = Path(__file__).resolve().parent.parent / "outputs" / "figs"
figs.mkdir(parents=True, exist_ok=True)
plt.savefig(figs / "task08_convergence.png", dpi=120, bbox_inches="tight")
n = 20
A20 = 2*np.eye(n) - np.diag(np.ones(n-1), 1) - np.diag(np.ones(n-1), -1)
b20 = np.zeros(n); b20[0] = 100.; b20[-1] = 20.
x20, e20 = jacobi(A20, b20)
print("20-point iterations:", len(e20), "max direct error:", np.max(np.abs(x20 - np.linalg.solve(A20, b20))))
'''.replace("import matplotlib.pyplot as plt", "import matplotlib.pyplot as plt\nfrom pathlib import Path"))

# ---------------- Task 09 ----------------
w("Task_09_eigenvalues.py", HEADER.format(
	title="Task 09: Eigenvalues and Eigenvectors",
	B="B) Find the dominant eigenpair and centrality scores of a four-node network.",
	C="C) Remove an edge and compare node scores.",
	D="D) Verify the eigenpair residual.",
	E="E) Compute PageRank-style scores for a directed graph.") + '''
import numpy as np

A = np.array([[0,1,1,0], [1,0,1,1], [1,1,0,1], [0,1,1,0]], dtype=float)
nodes = ["A", "B", "C", "D"]
def scores(matrix):
	vals, vecs = np.linalg.eig(matrix)
	i = np.argmax(vals.real)
	v = vecs[:, i].real
	return vals[i].real, np.abs(v) / np.abs(v).sum(), v
value, centrality, v = scores(A)
print("Dominant eigenvalue:", value)
for node, score in zip(nodes, centrality): print(node, round(score, 4))
print("Residual:", np.linalg.norm(A @ v - value * v))
A[2, 3] = A[3, 2] = 0
value2, centrality2, _ = scores(A)
print("After removing C-D:", list(zip(nodes, np.round(centrality2, 4))))

M = np.array([[0,1,1,0,0], [1,0,0,1,0], [1,0,0,1,1],
			  [0,1,1,0,1], [0,0,1,1,0]], dtype=float)
n = len(M); damping = .85
P = damping * M / M.sum(axis=0) + (1 - damping) / n
vals, vecs = np.linalg.eig(P)
i = np.argmax(vals.real)
pagerank = np.abs(vecs[:, i].real); pagerank /= pagerank.sum()
print("PageRank:", np.round(pagerank, 4), "eigenvalue:", vals[i].real)
''')

# ---------------- Task 10 ----------------
w("Task_10_root_finding.py", HEADER.format(
	title="Task 10: Root Finding - Bisection and Fixed-Point Methods",
	B="B) Find the heat-balance equilibrium by bisection and fixed-point iteration.",
	C="C) Vary brackets and starting guesses.",
	D="D) Compare roots and plot the function.",
	E="E) Find a bakery break-even volume.") + '''
import os
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.optimize import root_scalar

def heat_balance(T): return T - 25 - 10*np.exp(-T/20)
def g(T): return 25 + 10*np.exp(-T/20)
solution = root_scalar(heat_balance, bracket=[20, 40], method="bisect", xtol=1e-10)
T = 30.; history = [T]
for _ in range(100):
	Tn = g(T); history.append(Tn)
	if abs(Tn - T) < 1e-10: break
	T = Tn
print("Bisection:", solution.root, "fixed point:", history[-1], "iterations:", len(history)-1)
for bracket in ([20, 40], [25, 35], [26, 30]):
	print("Bracket", bracket, "root", root_scalar(heat_balance, bracket=bracket, method="bisect").root)
for start in (20., 30., 38.):
	T = start
	for _ in range(200):
		Tn = g(T)
		if abs(Tn-T) < 1e-10: break
		T = Tn
	print("Start", start, "fixed point", T)
temps = np.linspace(20, 40, 300)
plt.figure(); plt.plot(temps, heat_balance(temps)); plt.axhline(0); plt.axvline(solution.root, ls="--")
plt.grid(True); plt.title("Task 10 equilibrium"); plt.xlabel("Temperature (C)")
figs = Path(__file__).resolve().parent.parent / "outputs" / "figs"
figs.mkdir(parents=True, exist_ok=True)
plt.savefig(figs / "task10_equilibrium.png", dpi=120, bbox_inches="tight")
break_even = root_scalar(lambda x: 8*x - 5000, bracket=[0, 2000], method="bisect").root
print("Bakery break-even cakes:", break_even)
''')

# ---------------- Task 11 ----------------
w("Task_11_newton_secant.py", HEADER.format(
	title="Task 11: Root Finding - Newton-Raphson and Secant Methods",
	B="B) Find a project internal rate of return from NPV cash flows.",
	C="C) Add a sixth-year inflow and compare the IRR.",
	D="D) Compare Newton and secant roots and check NPV.",
	E="E) Find a monthly loan interest rate with secant iteration.") + '''
from scipy.optimize import root_scalar

cash_flows = [-10000, 3000, 3500, 4000, 2500]
def npv(rate, flows=cash_flows):
	return sum(cf / (1 + rate)**t for t, cf in enumerate(flows))
def d_npv(rate, flows=cash_flows):
	return sum(-t*cf / (1 + rate)**(t+1) for t, cf in enumerate(flows) if t)
newton = root_scalar(npv, fprime=d_npv, x0=.1, method="newton", xtol=1e-12)
secant = root_scalar(npv, x0=.05, x1=.2, method="secant", xtol=1e-12)
print("Newton IRR:", newton.root, "iterations:", newton.iterations)
print("Secant IRR:", secant.root, "iterations:", secant.iterations, "NPV:", npv(newton.root))
flows2 = cash_flows + [2000]
new_irr = root_scalar(lambda r: npv(r, flows2), fprime=lambda r: d_npv(r, flows2), x0=.1, method="newton")
print("IRR with additional inflow:", new_irr.root)
def loan_balance(r):
	if abs(r) < 1e-12: return 12000 - 1100*12
	return 12000 - 1100*(1 - (1+r)**-12)/r
loan = root_scalar(loan_balance, x0=.005, x1=.02, method="secant", xtol=1e-14)
print("Monthly loan rate:", loan.root, "annual effective:", (1+loan.root)**12-1)
''')

# ---------------- Task 12 ----------------
w("Task_12_nonlinear_equations.py", HEADER.format(
	title="Task 12: Polynomial and Nonlinear Equation Solving",
	B="B) Solve for circle-parabola intersections using scipy.optimize.root.",
	C="C) Change the circle radius and search from multiple starting guesses.",
	D="D) Print intersection points and residuals.",
	E="E) Solve a chemical-equilibrium composition equation.") + '''
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
''')

print("Batch 2 done")
