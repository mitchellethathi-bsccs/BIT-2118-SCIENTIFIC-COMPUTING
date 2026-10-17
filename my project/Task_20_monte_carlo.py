"""BIT 2118 Task 20: Random Numbers and Monte Carlo Methods.
Real-world case: probability that a server becomes overloaded under random demand."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

print("=== TASK 20: Random Numbers and Monte Carlo Methods ===")

rng = np.random.default_rng(42)
capacity = 1000.0
mean_demand = 850.0
std_demand = 120.0
N = 100_000

demand = rng.normal(mean_demand, std_demand, N)
overloaded = demand > capacity
overload_probability = overloaded.mean()

print("[B] Inputs: demand ~ Normal(850, 120), capacity 1000, N=100,000 random scenarios. Operation: sample, evaluate indicator, average.")
print(f"[D] Estimated overload probability: {overload_probability:.4%}")
print(f"[D] Number of overload cases: {overloaded.sum()} out of {N}")
exact_prob = 1 - 0.5 * (1 + __import__("math").erf((capacity - mean_demand) / (std_demand * np.sqrt(2))))
print(f"[D] Exact (analytical) probability : {exact_prob:.4%}  -> Monte Carlo agrees within ~{abs(overload_probability - exact_prob):.4%}")

indices = np.logspace(1, np.log10(N), 200).astype(int) - 1
running = np.cumsum(overloaded) / np.arange(1, N + 1)
plt.figure()
plt.semilogx(indices + 1, running[indices])
plt.axhline(exact_prob, color="r", linestyle="--", label="Exact")
plt.xlabel("Number of simulations"); plt.ylabel("Estimated overload probability")
plt.title("Monte Carlo estimate of server-overload risk")
plt.legend(); plt.grid(True)
import os

output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs", "figs")
os.makedirs(output_dir, exist_ok=True)

plt.savefig(os.path.join(output_dir, "task_20_monte_carlo.png"), dpi=110)
plt.close()
print("[D] Figure saved: figures/task_20_monte_carlo.png (estimate stabilizes near the exact value as N grows: law of large numbers)")

# [C] Parameter change: lower demand variability
std2 = 80.0
demand2 = rng.normal(mean_demand, std2, N)
p2 = (demand2 > capacity).mean()
print(f"[C] With std reduced 120 -> 80: overload probability falls to {p2:.4%} "
	f"(more predictable demand -> less risk)")

# [E] Modified case: estimating pi with a quarter-circle dartboard
print("\n[E] Modified case: Monte Carlo estimate of pi")
n = 200_000
pts = rng.uniform(0, 1, (n, 2))
inside = (pts[:, 0]**2 + pts[:, 1]**2) <= 1.0
pi_est = 4 * inside.mean()
print(f"    {inside.sum()} of {n} points inside quarter circle -> pi ~ {pi_est:.6f} (true pi = {np.pi:.6f})")
plt.figure()
plt.scatter(pts[::200, 0], pts[::200, 1], s=1, alpha=0.3)
t = np.linspace(0, np.pi / 2, 100)
plt.plot(np.cos(t), np.sin(t), "r")
plt.title("Monte Carlo estimation of pi (sample of points shown)")
plt.axis("equal")
plt.savefig(os.path.join(output_dir, "task_20e_pi.png"), dpi=110)
plt.close()
print("[D] Figure saved: figures/task_20e_pi.png")
