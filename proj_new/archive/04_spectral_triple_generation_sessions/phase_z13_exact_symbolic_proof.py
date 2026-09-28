"""
Phase Z13 (this session) -- Z11's second flagged next step: every
result from Z8 through Z12 was computed numerically (floating point
SVD / eigh on a Gram matrix, with a 1e-6 tolerance for "zero"). That's
legitimate evidence, but it is not a closed-form proof, and the
project's own next-step notes said so explicitly. This phase redoes
the core single-channel computation with EXACT symbolic arithmetic
(sympy, rational + sqrt(3) radicals, zero floating-point tolerance
anywhere) to remove any residual doubt that "2 real parameters,
texture c*I_3" is a numerical-precision artifact.

## Key simplification (justified, not assumed)

The order-one condition factors as (internal Y_H) (x) (generation-space
expression) -- this is what made the Z9 argument ("Y_H is a nonzero
spectator, only its symmetry type matters") work in the first place.
That means the *internal* dimension of Y_H (16 in the physical model)
should not affect which su(3)_F representations of Y_gen survive --
only Y_H's symmetry type (Hermitian, real-symmetric here) and
nonzero-ness should matter. This phase tests that claim head-on by
replacing the physical 16-dim Y_H with the smallest possible
nontrivial stand-in (a 1x1 real scalar, Y_H = [1]) and checking
whether the exact symbolic kernel comes out identical (dimension 2,
texture c*I_3) to what Z9/Z10/Z11 found numerically with the real
16-dim gamma-matrix-derived Y_H. If it does, that's independent
confirmation that the internal-dimension-independence claim is
correct, not just plausible, AND it makes the problem small enough
(6x6 instead of 96x96) for exact symbolic computation across the full
8x8 su(3)_F generator algebra to be tractable.
"""
import sympy as sp
from sympy import I, sqrt, Rational, Matrix, symbols, conjugate, simplify, zeros, eye


def build_su3f_generators_exact():
    """Exact Gell-Mann matrices / 2, same convention as
    support/z2_hilbert_space.py's build_su3f_generators, but with
    sympy exact entries (Rational, sqrt(3)) instead of floats."""
    GM = [
        Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]]),
        Matrix([[0, -I, 0], [I, 0, 0], [0, 0, 0]]),
        Matrix([[1, 0, 0], [0, -1, 0], [0, 0, 0]]),
        Matrix([[0, 0, 1], [0, 0, 0], [1, 0, 0]]),
        Matrix([[0, 0, -I], [0, 0, 0], [I, 0, 0]]),
        Matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0]]),
        Matrix([[0, 0, 0], [0, 0, -I], [0, I, 0]]),
        (1 / sqrt(3)) * Matrix([[1, 0, 0], [0, 1, 0], [0, 0, -2]]),
    ]
    return [g / 2 for g in GM]


def embed_doubled_exact(Y):
    n = Y.shape[0]
    top = Y.row_join(zeros(n, n)) if False else None
    Z = zeros(n, n)
    return Matrix.vstack(
        Matrix.hstack(Z, Y),
        Matrix.hstack(Y.H, Z),
    )


def conj_matrix(M):
    return M.applyfunc(conjugate)


def run(Y_H=None, label='M10'):
    # --- generic 1-dim stand-in for the internal Y_H (spectator factor) ---
    if Y_H is None:
        Y_H = Matrix([[1]])  # real, symmetric, Hermitian, nonzero -- that's all that's used
    n_int_doubled = 2  # doubled internal dim = 2 * 1

    print()
    print('=' * 70)
    print(f'{label} channel: exact symbolic check, Y_gen symmetric complex, Y_H = {Y_H.tolist()}')
    print('=' * 70)

    su3f = build_su3f_generators_exact()

    # generic symmetric complex Y_gen: 6 complex = 12 real free symbols
    names_re = symbols('r11 r22 r33 r12 r13 r23', real=True)
    names_im = symbols('i11 i22 i33 i12 i13 i23', real=True)
    r11, r22, r33, r12, r13, r23 = names_re
    i11, i22, i33, i12, i13, i23 = names_im
    unknowns = list(names_re) + list(names_im)

    def cplx(rr, ii):
        return rr + I * ii

    Y_gen = Matrix([
        [cplx(r11, i11), cplx(r12, i12), cplx(r13, i13)],
        [cplx(r12, i12), cplx(r22, i22), cplx(r23, i23)],
        [cplx(r13, i13), cplx(r23, i23), cplx(r33, i33)],
    ])

    Y_full = sp.Matrix(sp.kronecker_product(Y_H, Y_gen))     # 3x3 (since Y_H is 1x1)
    D_F = embed_doubled_exact(Y_full)                        # 6x6

    I2 = eye(n_int_doubled)
    P_swap = Matrix([[0, 1], [1, 0]])  # swap the two 1-dim internal copies

    print('Building exact symbolic order-one condition over all 8x8=64 su(3)_F pairs...')
    print('(6x6 matrices, exact rational/sqrt(3) arithmetic -- no floats, no tolerance)')

    equations = []
    for a in range(8):
        T_a = su3f[a]
        a_HF = sp.Matrix(sp.kronecker_product(I2, T_a))
        inner = D_F * a_HF - a_HF * D_F
        for b in range(8):
            T_b = su3f[b]
            beta_prime = P_swap * conj_matrix(I2) * P_swap.inv()
            Jb_HF = sp.Matrix(sp.kronecker_product(beta_prime, conj_matrix(T_b)))
            L = inner * Jb_HF - Jb_HF * inner   # 6x6, exact, linear in the 12 unknowns
            for r in range(6):
                for c in range(6):
                    entry = sp.expand(L[r, c])
                    if entry != 0:
                        equations.append(sp.re(entry))
                        equations.append(sp.im(entry))
        print(f'  a={a} done ({(a + 1) * 8}/64 pairs)')

    print('Solving exact homogeneous linear system in 12 real unknowns...')
    eqs = [sp.expand(e) for e in equations if sp.expand(e) != 0]
    # Build the coefficient matrix exactly and take its exact nullspace.
    A = sp.Matrix([[sp.diff(eq, u) for u in unknowns] for eq in eqs])
    A = sp.simplify(A)
    rank = A.rank()
    nullspace = A.nullspace()
    print(f'Coefficient matrix: {A.shape[0]} equations x {A.shape[1]} unknowns')
    print(f'Exact rank: {rank}  ->  exact surviving real dimension: {12 - rank}')
    print(f'Number of independent null vectors found: {len(nullspace)}')
    for idx, nv in enumerate(nullspace):
        nv = sp.simplify(nv)
        print(f'--- exact null vector {idx} ---')
        vals = dict(zip(unknowns, nv))
        Re = Matrix([[vals[r11], vals[r12], vals[r13]],
                     [vals[r12], vals[r22], vals[r23]],
                     [vals[r13], vals[r23], vals[r33]]])
        Im = Matrix([[vals[i11], vals[i12], vals[i13]],
                     [vals[i12], vals[i22], vals[i23]],
                     [vals[i13], vals[i23], vals[i33]]])
        print('Re(Y_gen) =')
        sp.pprint(Re)
        print('Im(Y_gen) =')
        sp.pprint(Im)

    return rank, nullspace, unknowns


def run_antisymmetric():
    """Same exact-symbolic method, M120 channel: Y_H real antisymmetric
    (smallest nonzero stand-in is 2x2), Y_gen antisymmetric complex
    (3 complex = 6 real unknowns)."""
    Y_H = Matrix([[0, 1], [-1, 0]])  # smallest nonzero real antisymmetric stand-in
    n_int = 2
    n_int_doubled = 2 * n_int

    su3f = build_su3f_generators_exact()

    names_re = symbols('r12 r13 r23', real=True)
    names_im = symbols('i12 i13 i23', real=True)
    r12, r13, r23 = names_re
    i12, i13, i23 = names_im
    unknowns = list(names_re) + list(names_im)

    def cplx(rr, ii):
        return rr + I * ii

    z = sp.Integer(0)
    Y_gen = Matrix([
        [z, cplx(r12, i12), cplx(r13, i13)],
        [-cplx(r12, i12), z, cplx(r23, i23)],
        [-cplx(r13, i13), -cplx(r23, i23), z],
    ])

    Y_full = sp.Matrix(sp.kronecker_product(Y_H, Y_gen))     # 6x6
    D_F = embed_doubled_exact(Y_full)                        # 12x12

    I2 = eye(n_int_doubled)
    P_swap = Matrix.vstack(
        Matrix.hstack(zeros(n_int, n_int), eye(n_int)),
        Matrix.hstack(eye(n_int), zeros(n_int, n_int)),
    )

    print()
    print('=' * 70)
    print('M120 channel: exact symbolic check, Y_gen antisymmetric')
    print('=' * 70)

    equations = []
    for a in range(8):
        T_a = su3f[a]
        a_HF = sp.Matrix(sp.kronecker_product(I2, T_a))
        inner = D_F * a_HF - a_HF * D_F
        for b in range(8):
            T_b = su3f[b]
            beta_prime = P_swap * conj_matrix(I2) * P_swap.inv()
            Jb_HF = sp.Matrix(sp.kronecker_product(beta_prime, conj_matrix(T_b)))
            L = inner * Jb_HF - Jb_HF * inner
            for r in range(L.shape[0]):
                for c in range(L.shape[1]):
                    entry = sp.expand(L[r, c])
                    if entry != 0:
                        equations.append(sp.re(entry))
                        equations.append(sp.im(entry))
        print(f'  a={a} done ({(a + 1) * 8}/64 pairs)')

    eqs = [sp.expand(e) for e in equations if sp.expand(e) != 0]
    A = sp.Matrix([[sp.diff(eq, u) for u in unknowns] for eq in eqs])
    A = sp.simplify(A)
    rank = A.rank()
    nullspace = A.nullspace()
    print(f'Coefficient matrix: {A.shape[0]} equations x {A.shape[1]} unknowns')
    print(f'Exact rank: {rank}  ->  exact surviving real dimension: {6 - rank}')
    print(f'Number of independent null vectors found: {len(nullspace)} (expect 0)')
    return rank, nullspace


if __name__ == '__main__':
    run(Matrix([[1]]), label='M10')
    run(Matrix([[1 + I]]), label='M126')
    run_antisymmetric()
