"""
Phase L: Does Cl(10) Actually Contain SU(2)_L x SU(2)_R? [L1, NEW]
======================================================================
Direct follow-up on Phase J's flagged open question, using the real
CCvS algebra now confirmed from the primary source (arXiv:1304.8050):
A = H_R (+) H_L (+) M4(C), where H_R and H_L are SEPARATE quaternion
algebras, each with unitary group SU(2) -- i.e. genuinely two
independent SU(2)'s, not one bigger group.

Standard fact being tested here (textbook Lie theory, so(4) = su(2)
(+) su(2) via self-dual/anti-self-dual decomposition of the 4d
rotation generators -- cited, not invented): SO(10) contains
SO(6)xSO(4) as a maximal subgroup, SO(6)~SU(4), and SO(4)~SU(2)xSU(2).
Phase A1 built SU(2)_L from Witt pair {3,4} (a 4-real-dimensional
Cl(4) subalgebra) using a SIMPLE embedding that only exposes ONE
SU(2). The question: does that SAME 4-dimensional subspace, viewed
through the SO(4)=SU(2)xSU(2) isomorphism instead, actually contain
BOTH SU(2)'s already -- making Cl(10) x E8 compatible with CCvS's
H_R (+) H_L after all, using no new assumptions beyond re-reading the
same algebra Phase A1 already built?
"""
import numpy as np
import sys
sys.path.insert(0, '.')
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'support'))
from qosc_division_connection import build_octonion_structure_constants

print('=' * 72)
print('Phase L: SO(4) = SU(2)_L x SU(2)_R inside Cl(10)s own Witt pair {3,4}?')
print('=' * 72)

# Rebuild the exact same 10 gamma matrices Phase A1 used
C, _, _, _ = build_octonion_structure_constants()
s1 = np.array([[0, 1], [1, 0]], dtype=complex)
s2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
s3 = np.array([[1, 0], [0, -1]], dtype=complex)
I8 = np.eye(8, dtype=complex)
I16 = np.eye(16, dtype=complex)
G8 = [np.kron(s1, C[i]) for i in range(1, 8)] + [1j * np.kron(s2, I8)]
gammas = [np.kron(G8[i], s3) for i in range(8)] + [
    np.kron(I16, 1j * np.array([[0, 1], [1, 0]], dtype=complex)),
    np.kron(I16, 1j * np.array([[0, -1j], [1j, 0]], dtype=complex)),
]

# Verify Clifford algebra: {gamma_i, gamma_j} = -2 delta_ij (or +2, check sign)
anticomm_check = np.allclose(
    gammas[0] @ gammas[1] + gammas[1] @ gammas[0], np.zeros((32, 32)), atol=1e-8)
print(f"Sanity check -- {{gamma_0,gamma_1}}=0 as required for Clifford algebra: "
      f"{anticomm_check}")

# Witt pair {3,4} in Phase A1's indexing corresponds to gamma indices 6,7,8,9
# (pair j uses gamma_{2j}, gamma_{2j+1}; j=3 -> 6,7; j=4 -> 8,9)
idx = [6, 7, 8, 9]
g = [gammas[i] for i in idx]

# Build the 6 antisymmetric SO(4) generators: M_munu = (i/4)[gamma_mu, gamma_nu]
def comm(A, B):
    return A @ B - B @ A

M = {}
for a in range(4):
    for b in range(a+1, 4):
        M[(a, b)] = (1j/4) * comm(g[a], g[b])

pairs = [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)]
print(f"\nBuilt 6 so(4) generators M_munu from Witt pair {{3,4}} (gamma indices 6-9).")

# Self-dual / anti-self-dual combinations (standard construction):
# T_i^(+) = 1/2 (M_0i + 1/2 eps_ijk M_jk),  T_i^(-) = 1/2 (M_0i - 1/2 eps_ijk M_jk)
eps = np.zeros((3,3,3))
eps[0,1,2]=eps[1,2,0]=eps[2,0,1]=1
eps[0,2,1]=eps[2,1,0]=eps[1,0,2]=-1

M0 = [M[(0,1)], M[(0,2)], M[(0,3)]]     # M_0i, i=1,2,3 (here indices 1,2,3 of the 4)
Mjk = [M[(1,2)], M[(1,3)], M[(2,3)]]    # M_23, M_13(sign), M_12 -- need care with eps contraction
# Build dual generators D_i = 1/2 eps_ijk M_jk explicitly for i=1(->jk=23),2(->jk=31),3(->jk=12)
D1 = M[(2,3)]
D2 = -M[(1,3)]
D3 = M[(1,2)]
D = [D1, D2, D3]

Tplus  = [0.5*(M0[i] + D[i]) for i in range(3)]
Tminus = [0.5*(M0[i] - D[i]) for i in range(3)]

def su2_check(T, name):
    ok_alg = True
    for (i,j,k) in [(0,1,2),(1,2,0),(2,0,1)]:
        lhs = comm(T[i], T[j])
        rhs = 1j*T[k]
        if not np.allclose(lhs, rhs, atol=1e-6):
            ok_alg = False
    print(f"  {name}: [T_i,T_j]=i*eps_ijk*T_k holds for all i,j,k: {ok_alg}")
    return ok_alg

print("\nChecking whether T^(+) and T^(-) EACH independently close as su(2):")
ok_plus = su2_check(Tplus, "T^(+) (candidate SU(2)_L)")
ok_minus = su2_check(Tminus, "T^(-) (candidate SU(2)_R)")

print("\nChecking whether T^(+) and T^(-) commute with EACH OTHER "
      "(required for a genuine SU(2)_L x SU(2)_R direct product, not one bigger group):")
cross_comm = [comm(Tplus[i], Tminus[j]) for i in range(3) for j in range(3)]
all_commute = all(np.allclose(c, np.zeros((32,32)), atol=1e-6) for c in cross_comm)
print(f"  [T^(+)_i, T^(-)_j] = 0 for all i,j: {all_commute}")

print('=' * 72)
print('RESULT')
print('=' * 72)
if ok_plus and ok_minus and all_commute:
    print("""
CONFIRMED: the SAME 4-real-dimensional Witt-pair subspace Phase A1
used to build a single SU(2)_L (via the simple U(1)xSU(2) embedding)
ALSO contains a genuinely independent second SU(2), via the standard
SO(4)=SU(2)xSU(2) self-dual/anti-self-dual decomposition -- with no
new assumptions, no new pairs, no algebra imported from outside
Cl(10). This is a real, positive, previously-untested structural
result: Cl(10)'s own algebra is compatible with CCvS's H_R (+) H_L
requirement (two independent SU(2)'s), resolving the specific open
question flagged in Phase J.

IMPORTANT SCOPE LIMIT, stated honestly: this shows the GROUP THEORY
is compatible -- it does NOT show that Phase A1's specific fermion-
charge assignment (which used the simple embedding, not this one)
automatically reproduces CCvS's exact (2,1,4)+(1,2,4) fermion
representation content under this NEW basis choice. That requires
re-deriving which of Cl(10)'s 16 states transform under T^(+) as a
doublet vs singlet, and matching them explicitly to CCvS's psi_aI
assignment -- real follow-up work, not yet done, and now precisely
scoped instead of vague.
""")
else:
    print("""
NOT confirmed as stated -- see which check failed above. This would
mean Cl(10)'s Witt-pair {3,4} does NOT cleanly reproduce the
SO(4)=SU(2)xSU(2) split via this construction, and R1's SU(2)_R
question remains open. Recorded honestly either way.
""")

print('=' * 72)
print('Phase L addendum: checking the OPPOSITE-sign convention for T^(-)')
print('=' * 72)
print("""
Standard fact (textbook, not new): self-dual and anti-self-dual parts
of so(4) generate su(2) algebras of OPPOSITE orientation --
[T+_i,T+_j]=+i eps_ijk T+_k but [T-_i,T-_j]=-i eps_ijk T-_k. The first
check above only tested the '+' sign convention against both; that
was the test's error, not the algebra's. Re-checking T^(-) against
its correct sign:
""")

def su2_check_signed(T, name, sign):
    ok_alg = True
    for (i,j,k) in [(0,1,2),(1,2,0),(2,0,1)]:
        lhs = comm(T[i], T[j])
        rhs = sign*1j*T[k]
        if not np.allclose(lhs, rhs, atol=1e-6):
            ok_alg = False
    print(f"  {name}: [T_i,T_j]={'+.' if sign>0 else '-'}i*eps_ijk*T_k holds: {ok_alg}")
    return ok_alg

ok_minus_v2 = su2_check_signed(Tminus, "T^(-) (candidate SU(2)_R, opposite-orientation su(2))", -1)

print('=' * 72)
print('CORRECTED RESULT')
print('=' * 72)
if ok_plus and ok_minus_v2 and all_commute:
    print("""
CONFIRMED (corrected): Cl(10)'s Witt-pair {3,4} subspace DOES contain
two independent, mutually commuting su(2) algebras -- T^(+) (standard
orientation) and T^(-) (opposite orientation, exactly as expected for
anti-self-dual generators). This is the real SO(4)=SU(2)xSU(2) split,
present in Cl(10)'s OWN algebra with no new assumptions, no algebra
imported from outside, using the same gamma matrices Phase A1 already
built. This resolves the specific open question from Phase J: Cl(10)
is group-theoretically compatible with CCvS's H_R (+) H_L requirement.

STILL OPEN, honestly: which of Cl(10)'s 16 fermion states are doublets
under T^(+) vs T^(-) has not been worked out, and Phase A1's original
charge assignment (built from the SIMPLE embedding, not this one) is
not automatically the same labeling as this SO(4) embedding -- the two
constructions coexist inside the same Cl(10) algebra but are DIFFERENT
choices of which generators to call "the" gauge group. Reconciling
them (showing the SM charges Phase A1 already derived come out the
same way under this new basis) is the concrete next step, not yet
done.
""")
else:
    print("Still not fully confirmed -- see flags above.")
