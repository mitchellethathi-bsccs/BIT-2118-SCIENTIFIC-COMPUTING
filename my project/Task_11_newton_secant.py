# Task 11: Root Finding - Newton-Raphson and Secant Methods
# B) Find a project internal rate of return from NPV cash flows.
# C) Add a sixth-year inflow and compare the IRR.
# D) Compare Newton and secant roots and check NPV.
# E) Find a monthly loan interest rate with secant iteration.

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
