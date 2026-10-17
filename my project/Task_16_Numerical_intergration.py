"""BIT 2118 Task 16: Numerical Integration.
Real-world case: total energy consumed from smart-meter power readings."""
import numpy as np
from scipy.integrate import simpson

trapezoid = getattr(np, "trapezoid", None) or np.trapz

print("=== TASK 16: Numerical Integration ===")

time_hours = np.array([0, 2, 4, 6, 8, 10, 12], dtype=float)
power_kw = np.array([0.8, 1.0, 1.4, 1.8, 1.6, 1.2, 0.9])

energy_trapezoid = trapezoid(power_kw, time_hours)
energy_simpson = simpson(power_kw, x=time_hours)

print("[B] Inputs: power samples every 2 h. Operations: trapezoidal rule; Simpson's rule (parabolic segments).")
print(f"[D] Energy using trapezoidal rule: {energy_trapezoid:.3f} kWh")
print(f"[D] Energy using Simpson's rule  : {energy_simpson:.3f} kWh")
print(f"[D] Difference between estimates : {abs(energy_simpson - energy_trapezoid):.3f} kWh (~1.2% - sampling is coarse)")
print("[D] Interpretation: roughly 15.8 kWh was consumed over the 12-hour window (energy = integral of power over time).")

# [C] Parameter change: hourly samples (finer grid shrinks the gap)
t2 = np.arange(0, 13, 1, dtype=float)
p2 = np.array([0.8, 0.9, 1.0, 1.2, 1.4, 1.6, 1.8, 1.7, 1.6, 1.4, 1.2, 1.0, 0.9])
e_trap2 = trapezoid(p2, t2); e_simp2 = simpson(p2, x=t2)
print(f"[C] With hourly samples: trapezoid {e_trap2:.3f} kWh vs Simpson {e_simp2:.3f} kWh "
	f"(difference now only {abs(e_simp2 - e_trap2):.3f} kWh)")

# [E] Modified case: distance travelled from velocity readings (km/h at 1-hour marks)
print("\n[E] Modified case: distance from velocity data")
t3 = np.arange(0, 7, dtype=float)
v3 = np.array([0, 30, 50, 60, 55, 40, 20], dtype=float)   # km/h
d_trap = trapezoid(v3, t3); d_simp = simpson(v3, x=t3)
print(f"    Distance (trapezoid): {d_trap:.2f} km; (Simpson): {d_simp:.2f} km over the 6-hour trip")
print(f"    Average speed: {d_trap/6:.1f} km/h")
