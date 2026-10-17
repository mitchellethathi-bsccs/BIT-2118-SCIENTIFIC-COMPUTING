"""BIT 2118 Task 17: Ordinary Differential Equations - Euler Method.
Real-world case: Newton's law of cooling for a hot object.
"""
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


print("=== TASK 17: Ordinary Differential Equations - Euler Method ===")

T_AMBIENT = 25.0
T_INITIAL = 90.0
k = 0.12


def cooling_rate(temperature):
	"""Return dT/dt according to Newton's law of cooling."""
	return -k * (temperature - T_AMBIENT)


def euler(step_size, end_time):
	"""Approximate the cooling ODE using the explicit Euler method."""
	time = np.arange(0.0, end_time + step_size, step_size)
	temperature = np.zeros_like(time)
	temperature[0] = T_INITIAL

	for i in range(len(time) - 1):
		temperature[i + 1] = (
			temperature[i] + step_size * cooling_rate(temperature[i])
		)
	return time, temperature


time1, temp1 = euler(1.0, 30.0)
time2, temp2 = euler(0.5, 30.0)
exact = T_AMBIENT + (T_INITIAL - T_AMBIENT) * np.exp(-k * time1)

print(
	"[B] Inputs: ODE dT/dt = -k(T - 25), T(0)=90, step h. "
	"Operation: explicit Euler update y[n+1] = y[n] + h*f(y[n])."
)
print(f"[D] Euler temperature after 30 min (h=1.0): {temp1[-1]:.2f} C")
print(f"[D] Euler temperature after 30 min (h=0.5): {temp2[-1]:.2f} C")
print(f"[D] Exact temperature after 30 min        : {exact[-1]:.2f} C")
print(
	f"[D] Final absolute error (h=1.0): {abs(temp1[-1] - exact[-1]):.4f} C; "
	f"(h=0.5): {abs(temp2[-1] - exact[-1]):.4f} C"
)
print(
	"[D] Interpretation: the object cools toward 25 C; the smaller step "
	"produces a more accurate Euler approximation."
)

plt.figure()
plt.plot(time1, temp1, marker="o", label="Euler h=1.0")
plt.plot(time2, temp2, marker=".", label="Euler h=0.5")
plt.plot(time1, exact, label="Exact solution")
plt.xlabel("Time (minutes)")
plt.ylabel("Temperature (C)")
plt.title("Cooling of a hot object")
plt.legend()
plt.grid(True)
plt.tight_layout()
import os

output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs", "figs")
os.makedirs(output_dir, exist_ok=True)

plt.savefig(os.path.join(output_dir, "task_17_euler.png"), dpi=110)
print("[D] Figure saved: figures/task_17_euler.png")

# [C] Parameter change: weaker cooling constant k = 0.06.
k = 0.06
_, tempk = euler(1.0, 30.0)
exactk = T_AMBIENT + (T_INITIAL - T_AMBIENT) * np.exp(-0.06 * time1)
print(
	f"[C] With k=0.06 (slower cooling): T(30) = {tempk[-1]:.2f} C "
	f"vs exact {exactk[-1]:.2f} C (object stays hotter)."
)
k = 0.12  # Restore the original cooling constant.

# [E] Modified case: population growth dP/dt = rP.
print("\n[E] Modified case: exponential population growth dP/dt = 0.03 P, P(0) = 500")
r = 0.03
P0 = 500.0
step_size = 1.0
years = 20
t = np.arange(0.0, years + step_size, step_size)
population = np.zeros_like(t)
population[0] = P0
for i in range(len(t) - 1):
	population[i + 1] = population[i] + step_size * r * population[i]

population_exact = P0 * np.exp(r * t)
error = abs(population[-1] - population_exact[-1])
print(
	f"    Euler P(20) = {population[-1]:.2f}; exact = {population_exact[-1]:.2f}; "
	f"error = {error:.2f} ({100 * error / population_exact[-1]:.1f}%)"
)
print(
	"    The population roughly doubles in 20 years "
	"(rule of 72: 72/3 = 24 years)."
)
