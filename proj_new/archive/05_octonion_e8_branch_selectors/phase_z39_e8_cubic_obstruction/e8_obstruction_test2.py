"""
Follow-up: the actual Yukawa object built from the E8 cubic invariant is
Y_ij(phi) = epsilon_ijk phi_k, i.e. the (27,3)x(27,3)x(27bar-or-27,3)
trilinear coupling contracted down to a generation-space matrix once one
of the three flavor triplets is identified as the flavon/Higgs direction
phi. Check: (a) is the resulting mass spectrum pattern fixed by the
algebra regardless of phi's direction (yes -- that's the "structure"
part your framing correctly credits E8 with), and (b) is phi's direction
itself selected by anything internal to the algebra, or is it exactly
the same free modulus Z15-Z18 already found and closed negative.
"""
import numpy as np, itertools

def epsilon(i, j, k):
    perm = (i, j, k)
    if len(set(perm)) < 3:
        return 0
    inversions = sum(1 for a in range(3) for b in range(a+1, 3) if perm[a] > perm[b])
    return 1 if inversions % 2 == 0 else -1

def yukawa_matrix(phi):
    Y = np.zeros((3, 3), dtype=complex)
    for i, j, k in itertools.product(range(3), repeat=3):
        Y[i, j] += epsilon(i, j, k) * phi[k]
    return Y

rng = np.random.default_rng(1)
print(f"{'direction (normalized)':50s}  eigenvalues")
for _ in range(5):
    phi = rng.normal(size=3) + 1j*rng.normal(size=3)
    phi = phi / np.linalg.norm(phi)
    Y = yukawa_matrix(phi)
    eigs = np.round(np.linalg.eigvals(Y), 6)
    eigs_sorted = sorted(eigs, key=lambda z: (abs(z), z.real))
    print(f"{np.round(phi,3)}  ->  {eigs_sorted}")

print("\nPattern check: is it ALWAYS (0, +i|phi|, -i|phi|) up to phase, for any direction?")
print("If yes: the algebra fixes the *texture* (one exact zero mode, two equal")
print("magnitude), matching what your project's framing credits E8 with.")
print("But the DIRECTION of phi in flavor space (i.e. which linear combination")
print("of generations is massless) is not determined by anything shown above --")
print("it is exactly the same free flavon-VEV modulus Z15-Z18 already closed.")
