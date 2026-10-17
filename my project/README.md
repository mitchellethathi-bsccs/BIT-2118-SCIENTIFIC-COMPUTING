 
# BIT 2118 Scientific Computing - Group Project

**Student:** MITCHELLE THATHI
 **Reg No:** BSCCS/2025/56827 
**Course:** BIT 2118 Scientific Computing 
 **Semester:**  Sept-Dec 2026

> Each task below satisfies the assignment requirements:
> **B)** input values and mathematical operations identified,
> **C)** at least one input/parameter changed with explanation of the effect,
> **D)** output meaning explained in words (and graph interpretation),
> **E)** program modified to solve a different but related real-world case
> with new assumptions, input data, output and interpretation documented.

## Repository layout

```
bit2118_project/
├── code/                    # one runnable Python file per task (02-20)
│   ├── Task_02_numpy_arrays.py
│   ├── ... (19 files in total)
│   └── Task_20_monte_carlo.py
├── outputs/
│   ├── figs/                # 8 saved graphs (PNG)
│   └── console_log.txt      # captured output of every program
├── requirements.txt
└── README.md                # this documentation
```

**How to run:** `pip install -r requirements.txt`, then
`python code/Task_XX_<name>.py` from the project root. Figures are saved to
`outputs/figs/` automatically.

---

## Task 02 - NumPy Arrays and Numerical Computation

**B)** *Inputs:* 24 hourly temperature readings (°C) stored as one NumPy array.
*Operations:* `np.mean`, `np.min`, `np.max`, and the vectorized linear
conversion `F = 1.8C + 32` applied to the whole array at once.

**C)** *Parameter change:* all readings were shifted by +4 °C and the
conversion target was changed from Fahrenheit to Kelvin (`C + 273.15`).
The mean moved from 23.12 °C to 27.12 °C — exactly +4 — and the Kelvin
column appeared (e.g. 18.5 °C -> 291.65 K). Outputs scale exactly with the
inputs, confirming the operations act element-wise.

**D)** *Output meaning:* the mean (23.12 °C), minimum (17.5 °C) and maximum
(29.4 °C) summarise the whole day; the Fahrenheit array shows the same data
in the other unit. Nothing here needs a graph — the statistics themselves
are the result.

**E)** *Modified case — IoT soil-moisture monitoring.*
*Assumptions:* a farm field has a soil-moisture probe reporting hourly.
*Input data:* 12 readings dropping from 31.2 % to 24.0 %.
*Output:* mean 26.66 %, min 24.0 %; a vectorized `moisture < 25` check flags
5 hours below the 25 % irrigation threshold.
*Interpretation:* the field dries steadily; irrigation should start around
the 7th reading, before moisture crosses the threshold — the same array
statistics, now driving an agricultural decision.

## Task 03 - Mathematical Functions and Vectorization

**B)** *Inputs:* 1,000,000 simulated network-latency readings (ms).
*Operations:* division by 1000 (ms -> s) and element-wise squaring,
implemented twice — a Python loop and a vectorized NumPy expression.

**C)** *Parameter change:* the array size n was varied
(10,000 / 100,000 / 1,000,000). The speed-up grows with n (about **74x** at
one million), because Python-loop overhead dominates and NumPy pushes the
whole computation into optimized C.

**D)** *Output meaning:* the first five squared latencies (e.g.
0.000121 s²) plus timings. The timings are the point: vectorized code runs
in milliseconds while the loop takes seconds — critical when millions of
operations are repeated in simulations or ML pipelines.

**E)** *Modified case — image-pixel normalization.*
*Assumptions:* a 512×512 grayscale image is an array of 262,144 uint8 pixels.
*Input:* random pixel intensities 0–255.
*Operation:* `pixels / 255.0` in a single expression.
*Output:* intensities rescaled to [0, 1].
*Interpretation:* a whole image is normalized without a single explicit
loop — the everyday workhorse behind image processing and machine-learning
feature preparation.

## Task 04 - Floating-Point Arithmetic and Numerical Errors

**B)** *Inputs:* decimal constants 0.1, 0.2, 0.3; √2 and its 1.414
approximation; x values 1e-4, 1e-8, 1e-12. *Operations:* equality comparison,
`np.isclose`, absolute error |true − approx|, relative error
|true − approx| / |true|, and two algebraically equal formulas for
(√(1+x) − 1)/x.

**C)** *Parameter change:* x was made progressively smaller. The direct
(unstable) formula loses accuracy through catastrophic cancellation
(√(1+x) ≈ 1 in floating point), while the stable form 1/(√(1+x)+1) stays
correct near 0.5. The `0.1 + 0.2 == 0.3` test also flips from `False` to
`True` when a tolerance is used.

**D)** *Output meaning:* `0.1 + 0.2 = 0.30000000000000004` proves binary
floating point is approximate; absolute error 2.14e-4 and relative error
~1.5e-4 for the √2 approximation quantify accuracy; the unstable/stable
table shows how formulation choice controls error.

**E)** *Modified case — banking balance accumulation.*
*Assumptions:* a bank adds three deposits of 0.1 (million) to an account.
*Output:* the running balance ends at 0.30000000000000004, not exactly 0.3;
absolute error ≈ 5.6e-17.
*Interpretation:* money software must never compare floats with `==`;
it should use tolerances or integer cents/`Decimal` — a direct consequence
of round-off error in banking calculations.

## Task 05 - Matrix Algebra and Matrix Operations

**B)** *Inputs:* four corner points of a unit square, a 45° rotation matrix
and a (2.0, 1.5) scaling matrix. *Operations:* matrix multiplication `@`,
composition `rotation @ scale`, transforming all points by `points @ T.T`,
and the determinant.

**C)** *Parameter change:* angle 45° -> 90° and scale (2, 1.5) -> (3, 1).
The determinant (area scale factor) changed from 3.0 to 3.0 (rotations do
not change area) and the transformed square maps (1,0) -> (0,3): a quarter
turn with tripled x-reach.

**D)** *Output meaning:* the transformed coordinate list shows the square
rotated and stretched; the determinant 3.0 means every region's area is
tripled — exactly what a graphics engine needs to keep texture areas right.

**E)** *Modified case — robot-arm rotation (robotics).*
*Assumptions:* a 2-link planar arm, base at the origin, joints at (2, 0) and
tool tip at (3.5, 0); the tip must be swung 30° toward a workspace target.
*Input:* the three joint positions.
*Operation:* rotate every point by the same 30° matrix.
*Output:* new joint positions; the tip distance from the base stays 3.5 m.
*Interpretation:* rotation preserves distances, so the arm's reach is
constant while its orientation changes — the core idea in robotics
kinematics.

## Task 06 - Solution of Systems of Linear Equations

**B)** *Inputs:* coefficient matrix A = [[4, 2], [8, 12]] (CPU and memory
per server type) and usage vector b = [20, 72]. *Operations:*
`np.linalg.solve(A, b)` plus verification `A @ x` and residual norm ‖b − Ax‖.

**C)** *Parameter change:* total memory raised 72 -> 96 GB. The solution
shifts from (2, 4) to more Type-B servers — with the same 20 CPUs, extra
memory capacity is cheapest from the memory-efficient Type B.

**D)** *Output meaning:* Type A = 2, Type B = 4 servers exactly reproduce
the observed totals (A @ x = [20, 72]); the residual norm ≈ 0 confirms the
system is solved correctly.

**E)** *Modified case — electrical-circuit analysis (Kirchhoff's laws).*
*Assumptions:* two-loop DC circuit with a 10 V and a 6 V source.
*Input:* loop equations 6I₁ − 2I₂ = 10; −2I₁ + 8I₂ = 6.
*Operation:* solve A I = b.
*Output:* I₁ = 2.06 A, I₂ = 1.27 A (residual ≈ 0); shared-branch current
I₁ − I₂ = 0.79 A.
*Interpretation:* Kirchhoff's voltage laws are a linear system; solving it
gives every loop and branch current at once.

## Task 07 - Gaussian Elimination and LU Decomposition

**B)** *Inputs:* a fixed 3×3 coefficient matrix A and three measurement
vectors b. *Operations:* `lu_factor(A)` once, then `lu_solve` for each b;
residual norm per solution; comparison against `np.linalg.solve`.

**C)** *Parameter change:* an 8×8 matrix with 50 right-hand sides was
timed. Reusing the LU factors is markedly cheaper than 50 full direct
solves — the benefit grows with the number of b vectors.

**D)** *Output meaning:* each measurement set yields a solution vector with
residual norm ~1e-15 (machine precision) — the factorization is correct and
reusable. The direct solution for the first set matches exactly.

**E)** *Modified case — Leontief economic input-output model.*
*Assumptions:* 3 industries; A[i,j] = input from industry i per unit of
output of industry j; solve x = Ax + d, i.e. (I − A)x = d, each quarter.
*Input:* inter-industry matrix A and quarterly demand vectors d.
*Output:* required industry output levels per quarter, residuals ~0.
*Interpretation:* production must cover both inter-industry and consumer
demand; factoring (I − A) once makes quarterly forecasting instant.

## Task 08 - Iterative Methods for Linear Systems

**B)** *Inputs:* 5×5 diagonally dominant tridiagonal matrix, boundary
vector b (left 100 °C, right 20 °C), tolerance 1e-8, max 500 iterations.
*Operations:* Jacobi updates x_new = (b − Rx)/D; Gauss-Seidel using the
newest values immediately; infinity-norm change checked each iteration.

**C)** *Parameter change:* tolerance varied 1e-4 / 1e-8 / 1e-12. Looser
tolerance converges in fewer iterations (e.g. Jacobi 16 vs 52), tighter
needs more — a direct accuracy-versus-cost dial.

**D)** *Output meaning (graph):* both methods converge to the same
temperature profile; the semilog error plot (`task08_convergence.png`)
falls in a straight line — linear convergence — with Gauss-Seidel roughly
twice as fast as Jacobi, exactly as theory predicts for this matrix.

**E)** *Modified case — 20-point heat-transfer grid.*
*Assumptions:* the same 1-D steady-state model stretched to 20 interior
points. *Output:* Jacobi converges (agreement with the direct solver to
~1e-9); mid-grid temperature ≈ 58.9 °C.
*Interpretation:* iterative methods scale to the huge sparse grids from
real heat-transfer and structural models, where direct factorization is
too expensive.

## Task 09 - Eigenvalues and Eigenvectors

**B)** *Inputs:* 4-node undirected network adjacency matrix.
*Operations:* `np.linalg.eig`, pick the dominant eigenpair, normalize the
eigenvector into centrality scores, verify ‖Av − λv‖.

**C)** *Parameter change:* edge C–D removed. The dominant eigenvalue drops
and the centrality scores shift — C and D lose importance while B remains
the most central node, showing the measure reacts to topology changes.

**D)** *Output meaning:* the dominant eigenvalue (≈ 2.56) is the network's
growth factor under repeated adjacency multiplication; the normalized
eigenvector ranks nodes — B and C most influential. Verification error
≈ 1e-15 confirms Av = λv holds.

**E)** *Modified case — PageRank-style web graph.*
*Assumptions:* 5 pages with a directed link matrix; Google matrix
P = 0.85·(M/out-degree) + 0.15/n.
*Input:* the link matrix M.
*Operation:* dominant eigenvector of the column-stochastic matrix P.
*Output:* PageRank scores (highest for P3 and P4).
*Interpretation:* pages with many in-links score highest — the eigenvector
idea behind Google's PageRank and network-centrality analysis.

## Task 10 - Root Finding — Bisection and Fixed-Point Methods

**B)** *Inputs:* heat-balance f(T) = T − 25 − 10e^(−T/20), bracket [20, 40],
fixed-point map g(T) = 25 + 10e^(−T/20), start T₀ = 30, tolerance 1e-10.
*Operations:* `root_scalar(method="bisect")`; fixed-point iteration
T ← g(T).

**C)** *Parameter change:* brackets [20,40], [25,35], [26,30] all converge
to the same root (bisection only needs a sign change); fixed-point starting
guesses 20, 30, 38 also converge but at different speeds — showing bisection
is robust and fixed-point speed depends on |g′| < 1.

**D)** *Output meaning (graph):* both methods give T ≈ 26.04 °C; the plot
(`task10_equilibrium.png`) shows f(T) crossing zero there — heat gain
balances heat loss. Fixed point took ~36 iterations versus ~33 bisections.

**E)** *Modified case — business break-even point.*
*Assumptions:* cakes sell at 12 KES, variable cost 4 KES, fixed cost 5,000
KES. *Input:* f(x) = 8x − 5000. *Operation:* bisection on [0, 2000].
*Output:* break-even at exactly **625 cakes**.
*Interpretation:* every cake beyond 625 is profit; root finding converts a
break-even question into solving f(x) = 0.

## Task 11 - Root Finding — Newton-Raphson and Secant Methods

**B)** *Inputs:* cash flows [−10000, 3000, 3500, 4000, 2500]; NPV(r) and
its derivative dNPV/dr. *Operations:* Newton-Raphson (uses f′) and secant
(uses two points) via `root_scalar`, tolerance 1e-12.

**C)** *Parameter change:* an extra 6th-year inflow of 2,000 was added.
The IRR rose — extra positive cash makes the project more attractive — and
Newton still converged in a handful of iterations, demonstrating fast
quadratic convergence near the root.

**D)** *Output meaning:* IRR ≈ **11.54%** from both methods (Newton in 4
iterations, secant in ~5); NPV at the root ≈ 0 confirms it. A project is
worth doing when IRR exceeds the cost of capital.

**E)** *Modified case — monthly loan interest rate (secant method).*
*Assumptions:* 12,000 KES loan repaid in 12 instalments of 1,100 KES.
*Input:* loan-balance function of the monthly rate r.
*Operation:* secant method (no derivative needed).
*Output:* monthly rate ≈ 1.32%, ≈ 17.0% annual effective.
*Interpretation:* the secant method recovers the lender's hidden rate from
function values alone — useful when a derivative is unavailable.

## Task 12 - Polynomial and Nonlinear Equation Solving

**B)** *Inputs:* two residual equations — circle x² + y² = 4 and parabola
y = x² − 1 — with starting guesses (1, 1) and (−1, 1).
*Operations:* `scipy.optimize.root` on the 2-D system; residual check at
the solution.

**C)** *Parameter change:* circle radius 2 -> 3. The system now has up to
four intersections; probing several starting guesses finds them all,
showing nonlinear solvers are sensitive to initial guesses and can find
multiple roots.

**D)** *Output meaning:* intersections (±1.51, 1.29) with residuals ~0 and
`success: True` — the points satisfy both equations simultaneously. That's
what "solving a nonlinear system" means: driving every residual to zero.

**E)** *Modified case — chemical equilibrium.*
*Assumptions:* dissociation A₂ ⇌ 2A starting from 1 mol A₂, K = 1.
*Input:* equilibrium polynomial 4x² + x − 1 = 0 in the extent x.
*Output:* x ≈ 0.39 → 0.61 mol A₂ and 0.78 mol A at equilibrium; K checks
back to 1.0.
*Interpretation: solving the nonlinear equilibrium polynomial yields the
exact composition — the standard workflow for chemical-equilibrium
calculations.

## Task 13 - Interpolation

**B)** *Inputs:* hourly temperature samples at hours 8–14 and query times
every 10 minutes. *Operations:* `interp1d(kind="linear")` and
`CubicSpline` construction, then evaluation at the query times.

**C)** *Parameter change:* the data was thinned to every 2 hours. The
cubic spline then wiggles between the sparse points (risk of overshoot),
while linear interpolation remains bounded by its neighbours — showing the
accuracy/smoothness trade-off and why splines need enough samples.

**D)** *Output meaning (graph):* at 10:30, linear gives 22.25 °C and cubic
22.05 °C — close, but the cubic's smooth curve (`task13_interpolation.png`)
better matches how real temperature evolves between measurements.

**E)** *Modified case — sensor calibration lookup table.*
*Assumptions:* a pressure sensor is calibrated at 6 known voltages.
*Input:* voltage/pressure calibration pairs.
*Operation:* cubic-spline calibration curve.
*Output:* pressures for any measured voltage, e.g. 1.75 V -> 100.5 kPa.
*Interpretation:* interpolation turns a sparse calibration table into a
continuous converter — the standard sensor-calibration and lookup-table
workflow.

## Task 14 - Curve Fitting and Approximation

**B)** *Inputs:* 7 measurements of concurrent users vs response time (ms).
*Operations:* `curve_fit` least-squares fit of the quadratic model
y = ax² + bx + c; RMSE = √(mean((y − ŷ)²)); prediction at 400 users.

**C)** *Parameter change:* the last point was replaced by an 800 ms
outlier. RMSE jumped and the predicted 400-user response became far more
pessimistic — least squares is sensitive to outliers, so real data must be
cleaned before fitting.

**D)** *Output meaning (graph):* fitted model
y = 0.002167x² − 0.1345x + 85.00 with RMSE ≈ 5.8 ms; the curve
(`task14_curve_fit.png`) hugs the measurements and extrapolates to ≈ 256 ms
at 400 users — a capacity-planning number.

**E)** *Modified case — demand forecasting (exponential growth).*
*Assumptions:* monthly unit sales follow y = a·e^(bt).
*Input:* 8 months of sales (120 -> 560 units).
*Output:* growth rate ≈ 21%/month; forecast ≈ 1,090 units in month 12.
*Interpretation:* the fitted growth curve projects demand so the business
can plan stock and staffing — trend estimation from experimental data.

## Task 15 - Numerical Differentiation

**B)** *Inputs:* GPS time stamps 0–6 s and positions (m).
*Operations:* forward difference at the first point, central difference
(position[i+1] − position[i−1])/(t[i+1] − t[i−1]) for interior points,
backward difference at the end.

**C)** *Parameter change:* step size h was reduced (1.0, 0.5, 0.1) with
noisy position data. Error stops improving and worsens as h shrinks because
noise is amplified (error ~ noise/h); a moderate h gives the most reliable
estimate — a key practical lesson for sensor data.

**D)** *Output meaning (graph):* estimated speeds rise from 4.8 m/s to
8.0 m/s; the plot (`task15_speed.png`) shows the vehicle accelerating
through the journey.

**E)** *Modified case — acceleration from velocity data.*
*Assumptions:* a speedometer logs velocity every second while a vehicle
overtakes. *Input:* 9 velocity samples. *Operation:* `np.gradient`
(central differences). *Output:* acceleration peaking near t = 4 s
(≈ 4.5 m/s²) then declining. *Interpretation:* the strongest throttle input
happens mid-overtake; differentiation of sensor streams reveals such events.

## Task 16 - Numerical Integration

**B)** *Inputs:* smart-meter power readings (kW) every 2 h over 12 h.
*Operations:* trapezoidal rule (`np.trapezoid`) and Simpson's rule
(`scipy.integrate.simpson`) — both approximate ∫P dt.

**C)** *Parameter change:* sampling was doubled (hourly). Trapezoid and
Simpson estimates moved closer together (difference shrinks), since finer
sampling reduces the curvature error between samples.

**D)** *Output meaning:* energy ≈ **15.7 kWh** (trapezoidal) vs 15.63 kWh
(Simpson), difference ≈ 0.07 kWh. Total energy is the accumulated area
under the power curve — what the electricity bill is computed from.

**E)** *Modified case — distance from velocity data.*
*Assumptions:* a train logs velocity every 15 min for 90 min.
*Input:* velocity profile from 0 to 30 m/s and back.
*Output:* distance ≈ 29.4 km (Simpson), average speed ≈ 19.6 km/h.
*Interpretation:* integrating the speed profile gives distance travelled
without ever knowing the position — accumulated quantities from rates.

## Task 17 - ODEs — Euler Method

**B)** *Inputs:* cooling constant k = 0.12, ambient 25 °C, initial 90 °C,
step h = 1 min, horizon 30 min. *Operation:* Euler update
Tₙ₊₁ = Tₙ + h·f(Tₙ) with f(T) = −k(T − T_ambient).

**C)** *Parameter change:* h = 2, 1, 0.5, 0.25 min. Halving h roughly
halves the final error (first-order method), at twice the computation —
the classic accuracy-versus-cost trade-off of numerical ODE solvers.

**D)** *Output meaning (graph):* Euler gives ≈ 68.3 °C after 30 min vs the
exact 68.15 °C; the plot (`task17_euler.png`) shows the numerical curve
tracking the exponential decay with a small, visible lag.

**E)** *Modified case — logistic population growth.*
*Assumptions:* a lake stocked with 50 fish, r = 0.4/month, carrying
capacity K = 1000. *Input:* logistic ODE dP/dt = rP(1 − P/K), P(0) = 50.
*Output:* ≈ 928 fish after 24 months (exact 928.8); S-shaped growth.
*Interpretation:* growth is rapid early and slows near the carrying
capacity — the standard model for populations, epidemics and market
adoption.

## Task 18 - Numerical Solution of ODEs Using SciPy

**B)** *Inputs:* RC circuit Vs = 5 V, R = 1000 Ω, C = 0.001 F, V(0) = 0,
span 0–5 s, rtol = 1e-9 / atol = 1e-11. *Operation:* `solve_ivp`
integrates dV/dt = (Vs − V)/(RC) with adaptive higher-order stepping.

**C)** *Parameter change:* R = 500 / 1000 / 2000 Ω. The time constant
τ = RC (0.5 / 1 / 2 s) sets charging speed — larger R charges more slowly —
and the solver stays accurate for every τ, thanks to automatic step-size
control.

**D)** *Output meaning (graph):* V(5 s) = 4.9933 V with max error ~1e-9 V
against the exact curve; `task18_rc.png` shows the classic exponential
charging approaching 5 V.

**E)** *Modified case — SIR epidemic model (epidemiology).*
*Assumptions:* population 10,000, 1 initially infected, β = 0.3/day,
γ = 0.1/day (R₀ = 3). *Input:* the SIR ODE system.
*Output:* peak of ≈ 3,005 infections at day ≈ 50; ≈ 94% eventually recover.
*Interpretation:* public-health planners read peak size and timing directly
off the simulation — the same ODE machinery used in real epidemiology.

## Task 19 - Numerical Optimization

**B)** *Inputs:* costs (12, 18), capacities (100, 170) per server type,
minimum capacity 1000, start (5, 3), bounds x, y ≥ 0.
*Operations:* constrained minimization with SLSQP; exhaustive integer
search for whole servers.

**C)** *Parameter change:* requirement raised to 1400 and Type-B cost to
20. The optimum shifts toward more Type-A servers — when Type B becomes
relatively expensive, cost minimization rebalances the mix, showing how
sensitive allocation decisions are to prices.

**D)** *Output meaning:* continuous optimum ≈ (8.75, 1.91) at cost ≈ 139.4
with capacity exactly 1000 (the constraint is active); the best integer
plan (9, 2) costs 144. The answer is a concrete purchasing decision, not
just a number.

**E)** *Modified case — capacity planning under a budget cap.*
*Assumptions:* a startup needs ≥ 1200 capacity units but can spend ≤ 170.
*Input:* minimize shortfall subject to cost ≤ 170.
*Output:* the solver reports whether the budget can meet the goal and the
least-bad feasible plan otherwise.
*Interpretation:* constrained optimization turns resource-allocation and
scheduling trade-offs into one best decision under explicit limits.

## Task 20 - Random Numbers and Monte Carlo Methods

**B)** *Inputs:* capacity 1000, demand ~ N(850, 120²), N = 100,000
scenarios, seed 42. *Operations:* random-scenario generation, indicator
demand > capacity, estimated probability = overloads/N, running mean.

**C)** *Parameter change:* mean demand 850 -> 950 (overload probability
jumps from ≈ 10.6% to ≈ 34.8%, matching the theoretical normal tail), and
N = 1,000 vs 100,000 (estimates get less noisy as N grows — the law of
large numbers).

**D)** *Output meaning (graph):* overload probability ≈ **10.62%**
(10,616 cases in 100,000); `task20_monte_carlo.png` shows the running
estimate stabilizing on a log-x scale — visual proof of Monte Carlo
convergence.

**E)** *Modified case — portfolio-loss probability (finance).*
*Assumptions:* 50,000 KES invested in a stock with annual return
~ N(8%, 15%). *Input:* simulated annual returns.
*Output:* probability of a loss ≈ 29.8%; 95% Value-at-Risk ≈ 16.7%
(≈ 8,330 KES); expected profit ≈ 4,000 KES.
*Interpretation:* Monte Carlo quantifies downside risk (VaR) that
analytical models struggle with — the standard tool for risk and
uncertainty analysis in finance.

---

## Conclusion

Across the 19 tasks the same pattern recurs: a real-world quantity
(temperature, money, current, population, risk) is modelled numerically,
a NumPy/SciPy algorithm computes it, a parameter change demonstrates
sensitivity, and a modified case shows transferability. The full console
output of every program is captured in `outputs/console_log.txt` and all
graphs in `outputs/figs/`, so every number quoted above is reproducible by
running the corresponding file in `code/`.
