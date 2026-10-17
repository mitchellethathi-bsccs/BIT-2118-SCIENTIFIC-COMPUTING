"""BIT 2118 Task 13: Interpolation.

Real-world case: estimate temperature every 10 minutes from hourly sensor readings.
"""
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d, CubicSpline
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

print("=== TASK 13: Interpolation ===")

hours = np.array([8, 9, 10, 11, 12, 13, 14], dtype=float)
temperature = np.array([18, 19, 21, 24, 27, 29, 30], dtype=float)
linear = interp1d(hours, temperature, kind="linear")
cubic = CubicSpline(hours, temperature)

ten_minute_times = np.arange(8, 14 + 1 / 6, 1 / 6)
linear_estimates = linear(ten_minute_times)
cubic_estimates = cubic(ten_minute_times)
target_time = 10.5

print("[B] Inputs: 7 (hour, temperature) samples. Operations: piecewise-linear interpolation; cubic-spline interpolation.")
print(f"[D] Linear estimate at 10:30 : {float(linear(target_time)):.2f} C")
print(f"[D] Cubic  estimate at 10:30 : {float(cubic(target_time)):.2f} C")
print("[D] Interpretation: both methods fill in the 10-minute gaps; the spline follows the data's curvature")

plt.figure()
plt.scatter(hours, temperature, label="Hourly measurements", zorder=3)
plt.plot(ten_minute_times, linear_estimates, label="Linear")
plt.plot(ten_minute_times, cubic_estimates, label="Cubic spline")
plt.xlabel("Hour of day")
plt.ylabel("Temperature (C)")
plt.title("Temperature interpolation")
plt.legend()
plt.grid(True)
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs", "figs")
os.makedirs(output_dir, exist_ok=True)

plt.savefig(os.path.join(output_dir, "task_13_interpolation.png"), dpi=110)
print("[D] Figure saved: figures/task_13_interpolation.png (spline is smooth; linear has kinks at the samples)")

# [C] Parameter change: quadratic interpolation instead of cubic
quad = interp1d(hours, temperature, kind="quadratic")
print(
	f"[C] Quadratic interpolation at 10:30: {float(quad(target_time)):.2f} C "
	f"(between linear {float(linear(target_time)):.2f} and cubic {float(cubic(target_time)):.2f})"
)

# [E] Modified case: pressure-sensor calibration table
print("\n[E] Modified case: estimate pressure at 3.5 V from a calibration table")
voltage = np.array([0, 1, 2, 3, 4, 5], dtype=float)
pressure = np.array([0.0, 11.8, 24.6, 36.1, 49.5, 58.2])  # kPa
p_lin = interp1d(voltage, pressure, kind="linear")
p_cub = CubicSpline(voltage, pressure)
print(
	f"    At 3.5 V: linear -> {float(p_lin(3.5)):.2f} kPa, "
	f"cubic spline -> {float(p_cub(3.5)):.2f} kPa"
)
print("    The spline better follows the sensor's gentle nonlinearity between calibration points.")
