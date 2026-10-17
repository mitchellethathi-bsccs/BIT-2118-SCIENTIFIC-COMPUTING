"""BIT 2118 Task 18: Numerical Solution of ODEs Using SciPy.
Real-world case: voltage across a charging capacitor in an RC circuit."""
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

print("=== TASK 18: Numerical Solution of ODEs Using SciPy ===")

Vs = 5.0      # supply voltage (V)
R = 1000.0    # ohms
C = 0.001     # farads
V0 = 0.0      # initial capacitor voltage

def rc_circuit(t, V):
    return [(Vs - V[0]) / (R * C)]

t_eval = np.linspace(0, 5, 200)
solution = solve_ivp(rc_circuit, (0, 5), [V0], t_eval=t_eval, rtol=1e-9, atol=1e-11)
exact = Vs * (1 - np.exp(-solution.t / (R * C)))

print("[B] Inputs: ODE dV/dt = (Vs - V)/RC, V(0)=0, interval [0,5] s. Operation: adaptive Runge-Kutta (solve_ivp, RK45).")
print(f"[D] Solver success: {solution.success}")
print(f"[D] Capacitor voltage at 5 s: {solution.y[0, -1]:.4f} V (exact: {exact[-1]:.4f} V)")
print(f"[D] Maximum error against exact solution: {np.max(np.abs(solution.y[0] - exact)):.3e} V")
print(f"[D] Time constant tau = RC = {R*C:.0f} s; after 5 s (~5 tau) the capacitor is ~99% charged.")
print("[D] Interpretation: the solver tracks the analytical RC charging curve to machine precision.")

plt.figure()
plt.plot(solution.t, solution.y[0], label="solve_ivp")
plt.plot(solution.t, exact, linestyle="--", label="Exact")
plt.xlabel("Time (s)"); plt.ylabel("Capacitor voltage (V)")
plt.title("RC circuit charging")
plt.legend(); plt.grid(True)
import os

output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs", "figs")
os.makedirs(output_dir, exist_ok=True)

plt.savefig(os.path.join(output_dir, "task_18_rc_circuit.png"), dpi=110)
plt.close()
print("[D] Figure saved: figures/task_18_rc_circuit.png (numerical and exact curves are indistinguishable)")

# [C] Parameter change: double the capacitance (C = 0.002 F)
def rc2(t, V):
    return [(Vs - V[0]) / (R * 0.002)]
sol2 = solve_ivp(rc2, (0, 5), [V0], t_eval=t_eval, rtol=1e-9, atol=1e-11)
print(f"[C] With C=0.002 F (tau doubles to {R*0.002:.0f} s): V(5) = {sol2.y[0, -1]:.4f} V "
      f"(was {solution.y[0, -1]:.4f} V - slower charging, as expected)")

# [E] Modified case: caffeine decay in the bloodstream dC/dt = -k C
print("\n[E] Modified case: caffeine concentration C(0)=160 mg, k=0.14 /h, over 12 h")
k = 0.14
def caffeine(t, C_):
    return [-k * C_[0]]
sol3 = solve_ivp(caffeine, (0, 12), [160.0], t_eval=np.linspace(0, 12, 200), rtol=1e-9, atol=1e-11)
exact3 = 160 * np.exp(-k * sol3.t)
print(f"    C(12 h) = {sol3.y[0, -1]:.2f} mg (exact {exact3[-1]:.2f} mg); "
      f"max error = {np.max(np.abs(sol3.y[0] - exact3)):.2e}")
print(f"    Half-life ~ {np.log(2)/k:.2f} h: after 12 h about {160*np.exp(-k*12):.0f} mg remain "
      f"({np.exp(-k*12):.1%} of the initial dose).")