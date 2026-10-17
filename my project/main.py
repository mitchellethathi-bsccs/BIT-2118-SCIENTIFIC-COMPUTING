import os

base = "/mnt/agents/output/bit2118_project"
code_dir = os.path.join(base, "code")
figs_dir = os.path.join(base, "outputs", "figs")
os.makedirs(code_dir, exist_ok=True)
os.makedirs(figs_dir, exist_ok=True)

def w(name, content):
	with open(os.path.join(code_dir, name), "w", encoding="utf-8") as f:
		f.write(content)
	print("wrote", name)

HEADER = '''"""BIT 2118 Scientific Computing - {title}
{B}
{C}
{D}
{E}
"""
'''

w("Task_02_numpy_arrays.py", HEADER.format(
	title="Task 02: NumPy Arrays and Numerical Computation",
	B="B) Inputs: 24 hourly temperature readings. Operations: mean, min, max, vectorized Fahrenheit conversion.",
	C="C) Parameter change: add 4 C to the readings and convert Celsius to Kelvin.",
	D="D) Output: daily statistics and element-wise converted readings.",
	E="E) Modified case: IoT soil-moisture sensor array.") + '''
import numpy as np

temperatures_c = np.array([18.5,18.0,17.8,17.5,17.9,19.0,21.5,23.8,25.6,27.1,28.3,29.0,29.4,29.1,28.5,27.6,26.2,24.8,23.4,22.1,21.0,20.2,19.6,19.0])
mean_temp = np.mean(temperatures_c)
print("ORIGINAL CASE: Weather-station temperatures")
print(f"Daily mean: {mean_temp:.2f} C; min: {temperatures_c.min():.2f} C; max: {temperatures_c.max():.2f} C")
print("First six Fahrenheit readings:", (1.8 * temperatures_c + 32)[:6])

hot_day = temperatures_c + 4.0
print("\\nC) PARAMETER CHANGE: heat-wave day (+4 C)")
print(f"New mean: {hot_day.mean():.2f} C (shift +{hot_day.mean()-mean_temp:.2f})")
print(f"New min/max: {hot_day.min():.2f} / {hot_day.max():.2f} C")
print("First six Kelvin readings:", (temperatures_c + 273.15)[:6])

moisture = np.array([31.2,30.8,30.1,29.4,28.9,28.0,27.2,26.5,25.8,25.1,24.6,24.0])
below = moisture < 25.0
print("\\nE) MODIFIED CASE: IoT soil moisture")
print(f"Mean: {moisture.mean():.2f}%; min/max: {moisture.min():.2f}% / {moisture.max():.2f}%")
print("Readings below 25%:", int(below.sum()), "at indices", np.where(below)[0].tolist())
''')

w("Task_03_vectorization.py", HEADER.format(
	title="Task 03: Mathematical Functions and Vectorization",
	B="B) Inputs: simulated network latencies. Compare division and squaring in a Python loop and vectorized NumPy.",
	C="C) Parameter change: vary array size to compare performance.",
	D="D) Output: squared latency values and timing comparison.",
	E="E) Modified case: vectorized image-pixel normalization.") + '''
import numpy as np
import timeit

rng = np.random.default_rng(42)
latency_ms = rng.uniform(5, 250, 1_000_000)
def loop_version():
	return [(value / 1000.0) ** 2 for value in latency_ms]
def vectorized_version():
	return (latency_ms / 1000.0) ** 2

loop_time = timeit.timeit(loop_version, number=1)
vector_time = timeit.timeit(vectorized_version, number=3) / 3
print("ORIGINAL CASE: Network latency")
print("First five squared values:", vectorized_version()[:5])
print(f"Loop: {loop_time:.4f}s; vectorized: {vector_time:.4f}s; speed-up: {loop_time/vector_time:.1f}x")

print("\\nC) PARAMETER CHANGE: array sizes")
for n in [10_000, 100_000, 1_000_000]:
	data = rng.uniform(5, 250, n)
	t_loop = timeit.timeit(lambda: [(v/1000.0)**2 for v in data], number=1)
	t_vec = timeit.timeit(lambda: (data/1000.0)**2, number=3) / 3
	print(f"n={n:,}: loop {t_loop:.4f}s; vectorized {t_vec:.6f}s; speed-up {t_loop/t_vec:.0f}x")

pixels = rng.integers(0, 256, size=(512, 512)).astype(float)
normalized = pixels / 255.0
print("\\nE) MODIFIED CASE: image-pixel normalization")
print(f"Image shape: {pixels.shape}; raw range {pixels.min():.0f}-{pixels.max():.0f}; normalized range {normalized.min():.3f}-{normalized.max():.3f}")
''')

w("Task_04_floating_point.py", HEADER.format(
	title="Task 04: Floating-Point Arithmetic and Numerical Errors",
	B="B) Inputs: decimal constants and sqrt(2); compare values and quantify error.",
	C="C) Parameter change: progressively shrink x to demonstrate cancellation.",
	D="D) Output: exact/tolerance comparisons and stable/unstable formula results.",
	E="E) Modified case: accumulated account deposits.") + '''
import numpy as np

calculated, expected = 0.1 + 0.2, 0.3
print("ORIGINAL CASE: Floating-point comparison")
print("0.1 + 0.2 =", calculated, "exact ==", calculated == expected, "np.isclose:", np.isclose(calculated, expected))
true_value, approx_value = np.sqrt(2), 1.414
error = abs(true_value - approx_value)
print(f"Absolute error: {error:.8f}; relative error: {error/abs(true_value):.8f}")

print("\\nC) PARAMETER CHANGE: shrinking x")
for x in [1e-4, 1e-8, 1e-12]:
	direct = (np.sqrt(1+x)-1)/x
	stable = 1/(np.sqrt(1+x)+1)
	print(f"x={x:.0e}: unstable={direct:.16f}; stable={stable:.16f}")

balance = 0.0
for _ in range(3):
	balance += 0.1
print("\\nE) MODIFIED CASE: accumulated account deposits")
print("Balance:", repr(balance), "exact == 0.3:", balance == 0.3, "np.isclose:", np.isclose(balance, 0.3))
print(f"Accumulated absolute error: {abs(balance-0.3):.2e}")
print("For money, use integer minor units or Decimal rather than binary floats.")
''')

w("Task_05_matrix_algebra.py", HEADER.format(
	title="Task 05: Matrix Algebra and Matrix Operations",
	B="B) Inputs: square corner points, rotation and scaling matrices; use matrix multiplication and determinant.",
	C="C) Parameter change: modify rotation angle and scale factors.",
	D="D) Output: transformed coordinates and area scale factor.",
	E="E) Modified case: robot-arm joint rotation.") + '''
import numpy as np

points = np.array([[0.,0.],[1.,0.],[1.,1.],[0.,1.]])
angle = np.deg2rad(45)
rotation = np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
scale = np.diag([2.0,1.5])
transform = rotation @ scale
print("ORIGINAL CASE: Graphics rotation and scaling")
print("Original points:\\n", points)
print("Transformation:\\n", transform)
print("Transformed points:\\n", points @ transform.T)
print("Determinant:", np.linalg.det(transform))

angle = np.deg2rad(90)
rotation = np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
transform = rotation @ np.diag([3.0,1.0])
print("\\nC) PARAMETER CHANGE: 90 degrees, scale (3, 1)")
print("Transformed points:\\n", points @ transform.T, "\\nDeterminant:", np.linalg.det(transform))

arm = np.array([[0.,0.],[2.,0.],[3.5,0.]])
theta = np.deg2rad(30)
R = np.array([[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]])
new_arm = arm @ R.T
print("\\nE) MODIFIED CASE: Robot-arm joint rotation")
print("Arm after 30-degree rotation:\\n", new_arm)
print(f"Tool-tip reach: {np.linalg.norm(new_arm[-1]):.4f} m (unchanged)")
''')

w("Task_06_linear_systems.py", HEADER.format(
	title="Task 06: Solution of Systems of Linear Equations",
	B="B) Inputs: server resource coefficient matrix A and usage vector b; solve Ax=b and verify residual.",
	C="C) Parameter change: increase total memory.",
	D="D) Output: server mix and residual norm.",
	E="E) Modified case: electrical-circuit analysis using Kirchhoff's laws.") + '''
import numpy as np

A = np.array([[4.,2.],[8.,12.]])
b = np.array([20.,72.])
solution = np.linalg.solve(A,b)
print("ORIGINAL CASE: Server resource allocation")
print(f"Type A: {solution[0]:.0f}; Type B: {solution[1]:.0f}")
print("Verification:", A @ solution, "residual:", b-A@solution, "norm:", np.linalg.norm(b-A@solution))

b2 = np.array([20.,96.])
s2 = np.linalg.solve(A,b2)
print("\\nC) PARAMETER CHANGE: total memory 72 -> 96 GB")
print(f"New solution: A={s2[0]:.2f}, B={s2[1]:.2f}")

A_c = np.array([[6.,-2.],[-2.,8.]])
b_c = np.array([10.,6.])
currents = np.linalg.solve(A_c,b_c)
print("\\nE) MODIFIED CASE: Electrical-circuit analysis")
print(f"Loop currents: I1={currents[0]:.3f} A, I2={currents[1]:.3f} A")
print("Verification:", A_c @ currents, "residual norm:", np.linalg.norm(b_c-A_c@currents))
print(f"Shared-branch current: {currents[0]-currents[1]:.3f} A")
''')

print("Batch 1 done")
