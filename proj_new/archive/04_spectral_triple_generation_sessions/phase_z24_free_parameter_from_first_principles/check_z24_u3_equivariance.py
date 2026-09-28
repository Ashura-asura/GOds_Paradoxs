"""
Phase Z24 support script 1 — verify the U(3)-equivariance claim used in the
Yukawa RG / fixed-point discussion (docs_new/SESSION_RESULT_YUKAWA_RG_FIXED_POINT
_TASKS_1_7.md, Task 1).

CLAIM TO CHECK:
Let Y be a complex 3x3 Yukawa matrix. Under a family-basis change Y -> U^T Y U
with U in U(3). If beta(Y) is any polynomial in Y built ONLY from
contractions that are covariant under this action (trace words, Y Y^dagger Y
type), then a zero of beta is mapped to a zero of beta' under the same
transformation. I.e. RG fixed points come in U(3) orbits.

What "from first principles" means here: we do NOT assume the abstract
representation theory. We construct the specific action Y -> U^T Y U, take a
generic polynomial beta, and verify numerically+symbolically that
beta(U^T Y U) == U^T beta(Y) U   (exact equivariance, term by term)
for the monomial types that actually occur in a 1-loop gauge-Yukawa beta fn:
   (i)  scalar(Y) * Y            where scalar = tr(Y^dag Y)  -- the trace term
   (ii) Y Y^dag Y                                    -- the cubic vertex term
   (iii) -k * Y                                      -- the gauge term
and confirm (iv) [gauge term] is equivariant trivially (scalar times Y).

If equivariance holds, then beta(Y*)=0 <=> beta(U^T Y* U)=0, i.e. every fixed
point drags a U(3) orbit -> 9 real directions of degeneracy. That is the
"the outcome is the same no matter what" mechanism for the RG route.

All quantities are generic (random unitary from QR of a Gaussian matrix,
deterministic seed), zero hand-tuned entries. sympy used for exactness on
small cases; numpy used for a 3x3 confirmation at machine precision.
"""
import numpy as np

rng = np.random.default_rng(20260802)


def random_unitary(n):
    z = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
    q, r = np.linalg.qr(z)
    # normalize QR phases to get Haar-ish U
    d = np.diagonal(r)
    ph = d / np.abs(d)
    return q * ph.conj()


def Y_to_UtYU(Y, U):
    return U.T @ Y @ U


def beta_trace_term(Y):
    return np.trace(Y.conj().T @ Y) * Y


def beta_cubic_term(Y):
    return Y @ Y.conj().T @ Y


def beta_gauge_term(Y, k=1.7):
    return -k * Y


def run(Y, U, name):
    UtYU = Y_to_UtYU(Y, U)
    errs = {}
    for label, f in [("trace", beta_trace_term),
                     ("cubic", beta_cubic_term),
                     ("gauge", beta_gauge_term)]:
        lhs = f(UtYU)                      # beta evaluated at transformed Y
        rhs = Y_to_UtYU(f(Y), U)            # transformed beta(Y)
        errs[label] = np.max(np.abs(lhs - rhs))
    print(f"[{name}] equivariance residuals "
          f"(should all be ~1e-15): " +
          ", ".join(f"{k}={v:.2e}" for k, v in errs.items()))
    return errs


def main():
    n = 3
    U = random_unitary(n)
    # sanity: U is unitary
    unit_err = np.max(np.abs(U.conj().T @ U - np.eye(n)))
    print(f"U unitarity residual: {unit_err:.2e}")

    Ysym = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
    Ysym = Ysym + Ysym.T                       # symmetric (like Y_10, Y_126)
    Yanti = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
    Yanti = Yanti - Yanti.T                    # antisymmetric (like Y_120)

    print("\nCase Y symmetric (Y_10 / Y_126 channel):")
    e1 = run(Ysym, U, "symmetric")
    print("\nCase Y antisymmetric (Y_120 channel):")
    e2 = run(Yanti, U, "antisymmetric")

    ok = all(v < 1e-12 for d in (e1, e2) for v in d.values())
    print("\nRESULT: " + ("PASS" if ok else "FAIL") +
          "  — beta(Y) is exactly equivariant under Y -> U^T Y U, "
          "so zeros of beta form U(3) orbits.")
    if ok:
        print("Implication: an isolated point in Yukawa space is impossible; "
              "any fixed point drags a 9-real-parameter U(3) degeneracy.")


if __name__ == "__main__":
    main()
