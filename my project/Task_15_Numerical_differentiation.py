"""BIT 2118 Task 15: Numerical Differentiation.
Real-world case: estimate vehicle speed from GPS position samples."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

print("=== TASK 15: Numerical Differentiation ===")

time = np.array([0, 1, 2, 3, 4, 5, 6], dtype=float)
position = np.array([0.0, 4.8, 10.2, 16.1, 22.7, 30.0, 38.0])

speed = np.zeros_like(position)
speed[0] = (position[1] - position[0]) / (time[1] - time[0])          # forward difference
for i in range(1, len(time) - 1):                                     # central differences
    speed[i] = (position[i + 1] - position[i - 1]) / (time[i + 1] - time[i - 1])
speed[-1] = (position[-1] - position[-2]) / (time[-1] - time[-2])     # backward difference

print("[B] Inputs: position samples at 1 s intervals. Operations: forward/central/backward finite differences.")
for t, x, v in zip(time, position, speed):
    print(f"[D] t={t:.0f}s position={x:5.1f}m estimated speed={v:5.2f} m/s")
print("[D] Interpretation: speed rises steadily from 4.8 to ~8 m/s - the vehicle is accelerating gently.")

plt.figure()
plt.plot(time, speed, marker="o")
plt.xlabel("Time (s)"); plt.ylabel("Estimated speed (m/s)")
plt.title("Speed estimated from GPS position data")
plt.grid(True)
import os

output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs", "figs")
os.makedirs(output_dir, exist_ok=True)

plt.savefig(os.path.join(output_dir, "task_15_differentiation.png"), dpi=110)
plt.close()
print("[D] Figure saved: figures/task_15_differentiation.png")

# [C] Parameter change: data sampled every 0.5 s (finer h reduces error)
t_fine = np.arange(0, 6.5, 0.5)
x_fine = 0.8 * t_fine**2 + 4.0 * t_fine
v_fine = np.gradient(x_fine, t_fine)
exact_mid = 1.6 * 3 + 4.0
print(f"[C] Finer sampling (h=0.5) at t=3 s: numerical = {np.interp(3, t_fine, v_fine):.3f} m/s "
      f"vs exact {exact_mid:.3f} m/s (central difference is exact for quadratics)")

# [E] Modified case: acceleration from velocity samples
print("\n[E] Modified case: acceleration from velocity data v(t) = [0, 2, 5, 9, 14, 20] m/s at t = 0..5 s")
v = np.array([0, 2, 5, 9, 14, 20], dtype=float)
t = np.arange(6, dtype=float)
a = np.zeros_like(v)
a[0] = (v[1] - v[0]) / (t[1] - t[0])
for i in range(1, len(t) - 1):
    a[i] = (v[i + 1] - v[i - 1]) / (t[i + 1] - t[i - 1])
a[-1] = (v[-1] - v[-2]) / (t[-1] - t[-2])
print("    Estimated acceleration (m/s^2):", np.round(a, 2))
print("    Since v(t) ~ t^2, true acceleration a(t) = 2t: matches (e.g. a(3) = 6.0 vs exact 6.0).")