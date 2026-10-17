"""BIT 2118 Task 14: Curve Fitting and Approximation.
Real-world case: model server response time vs concurrent user load."""
import numpy as np
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

print("=== TASK 14: Curve Fitting and Approximation ===")

users = np.array([50, 100, 150, 200, 250, 300, 350], dtype=float)
response_ms = np.array([82, 95, 115, 145, 185, 238, 305], dtype=float)

def model(x, a, b, c):
    return a * x**2 + b * x + c

parameters, covariance = curve_fit(model, users, response_ms)
a, b, c = parameters
predicted = model(users, a, b, c)
rmse = np.sqrt(np.mean((response_ms - predicted) ** 2))

print("[B] Inputs: 7 (load, response-time) measurements. Operation: least-squares fit of y = ax^2 + bx + c.")
print(f"[D] Fitted model: y = {a:.6f}x^2 + {b:.4f}x + {c:.2f}")
print(f"[D] RMSE: {rmse:.2f} ms (typical fitting error per measurement)")
print(f"[D] Predicted response at 400 users: {model(400, a, b, c):.2f} ms")
print("[D] Interpretation: delay grows quadratically with load; the model supports capacity planning.")

x_plot = np.linspace(users.min(), 400, 300)
plt.figure()
plt.scatter(users, response_ms, label="Measurements")
plt.plot(x_plot, model(x_plot, a, b, c), label="Fitted quadratic")
plt.xlabel("Concurrent users"); plt.ylabel("Response time (ms)")
plt.title("Server response-time curve fitting")
plt.legend(); plt.grid(True)
import os

output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs", "figs")
os.makedirs(output_dir, exist_ok=True)
plt.savefig(os.path.join(output_dir, "task_14_curve_fit.png"), dpi=110)
plt.close()
print("[D] Figure saved: figures/task_14_curve_fit.png (curve tracks the upward-bending measurements)")

# [C] Parameter change: compare with a linear model
p_lin = np.polyfit(users, response_ms, 1)
lin_pred = np.polyval(p_lin, users)
rmse_lin = np.sqrt(np.mean((response_ms - lin_pred) ** 2))
print(f"[C] Linear fit RMSE = {rmse_lin:.2f} ms vs quadratic RMSE = {rmse:.2f} ms "
      f"-> quadratic captures the upward bend far better")

# [E] Modified case: exponential growth of a bacterial culture
print("\n[E] Modified case: fit bacterial population growth N(t) = A * exp(B t)")
time_h = np.array([0, 1, 2, 3, 4, 5], dtype=float)
pop = np.array([100, 168, 285, 480, 810, 1370], dtype=float)
def exp_model(t, A, B):
    return A * np.exp(B * t)
(A_, B_), _ = curve_fit(exp_model, time_h, pop)
pred = exp_model(time_h, A_, B_)
rmse_e = np.sqrt(np.mean((pop - pred) ** 2))
print(f"    Fitted: N(t) = {A_:.1f} * exp({B_:.4f} t); RMSE = {rmse_e:.1f} cells")
print(f"    Growth rate B = {B_:.4f}/h (~doubling every {np.log(2)/B_:.2f} h); "
      f"prediction at t=7 h: {exp_model(7, A_, B_):.0f} cells")