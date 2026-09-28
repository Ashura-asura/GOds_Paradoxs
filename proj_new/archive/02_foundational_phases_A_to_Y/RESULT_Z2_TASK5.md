# RESULT_Z2_TASK5.md — applying the spectral-triple constraints:
the generation-block factorization theorem

Response to Task 5 of `PRIORITY_2_EXPLICIT_J_GAMMA_DIRAC_MODULI_PROMPT`.
New tests: `tests/test_order_one_condition.py` (3/3 pass, machine-precision
residuals, spot-checked and exhaustive-in-form — see derivation below).

## The result, stated first

**Theorem (checked directly on H_F, not merely argued):** for any
generation-trivial gauge-algebra element `a = alpha (x) I_3` (alpha an
arbitrary operator on the 32-dim Cl(10) factor — this includes every SM
generator Phase A1 has, and by the same argument extends to the full
so(10) Lie algebra, since the proof never uses any special property of
alpha beyond generation-triviality) and the corresponding `J b J^-1 =
beta' (x) I_3` (beta' = C_F . beta* . C_F^-1, from the J_F built in Task
3 — checked for BOTH surviving KO-dimension candidates, eps=+1 and
eps=-1), the order-one condition on a single generation-pair block
`D_F = M_kl (x) E_kl` reduces EXACTLY to

    [[D_F, a], JbJ^-1]  =  [[M_kl, alpha], beta']  (x)  E_kl

with **zero cross-block leakage**: turning on two blocks M_kl (x) E_kl and
M_k'l' (x) E_k'l' simultaneously produces an order-one-condition output
that is exactly the sum of the two single-block outputs, with no
interference term. Verified to machine precision (residuals ~ 1e-15,
i.e. floating-point zero) on the full 96x96 operators, not assumed from
the tensor-product algebra alone.

## Why this happens (the derivation, which the numerical check confirms
rather than merely illustrates)

For operators of the Kronecker form X (x) Y and A (x) I_3:

    (X (x) Y)(A (x) I_3) = (XA) (x) Y      and      (A (x) I_3)(X (x) Y) = (AX) (x) Y

so `[X (x) Y, A (x) I_3] = [X,A] (x) Y` — the generation factor Y is
completely inert. Chaining two such commutators (as the order-one
condition requires) never introduces any operator that acts nontrivially
on the generation index, because both a and JbJ^-1 are generation-trivial
by construction (a is generation-trivial because SU(3)_f is not part of
the gauge algebra A being gauged; JbJ^-1 is generation-trivial because
J_F's unitary part, C_F (x) I_3, is generation-trivial, per Task 3's own
construction). This is exact tensor algebra, not an approximation — the
numerical check exists to catch any bug in the code's bookkeeping of
that algebra, and finds none.

**The identical argument applies to the reality condition `J D_F = eps
D_F J` and the chirality condition `{Gamma_F (x) I_3, D_F} = 0`**, since
both Gamma_F (x) I_3 and J's unitary part are generation-trivial for
exactly the same reason. This was not separately re-coded as new tests
here (it is the same tensor-algebra fact, already exercised structurally
by `test_gamma_operator.py` / `test_reality_operator.py` on the Cl(10)
factor alone), but is stated explicitly so it is not silently assumed.

## What this does and does not prove

**Does prove:** the order-one/reality/chirality/gauge-covariance
conditions, applied to this H_F and this J/Gamma, cannot impose ANY
relation between different generation-pair coefficients M_kl. Whatever
freedom exists within a single block (Phase X's Hom_G computation, which
found dimension exactly 1 per eligible H per generation pair) survives
completely independently across all 9 blocks. There is no mechanism here
that could ever produce a texture zero, a fixed ratio, or any other
cross-generation relation — Outcome A (dim(M_D) < 6 or < 3) is now
excluded for this reason, not merely because no one has found it yet.

**Does not prove:** what the single-block dimension actually is —
that number (1, per eligible H) is imported from Phase X's own weight-
table computation, not independently re-derived here (Phase X's own
count is already correctly labeled: L1 for the 120 channel, L2 for the
10-vs-126 split). This phase's contribution is showing that whatever that
number is, it survives unchanged and un-related across generation
indices — i.e. that the *shape* of the freedom (block-diagonal,
generation-blind) is forced, even though the *value* of the per-block
count is not re-derived here.
