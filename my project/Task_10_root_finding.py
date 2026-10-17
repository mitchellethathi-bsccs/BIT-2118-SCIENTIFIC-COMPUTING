# Task 10: Root Finding - Bisection and Fixed-Point Methods
# B) Find the heat-balance equilibrium by bisection and fixed-point iteration.
# C) Vary brackets and starting guesses.
# D) Compare roots and plot the function.
# E) Find a bakery break-even volume.

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
