import sys, os
import numpy as np
from numpy import kron
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'support'))
from cl10_gamma_J import build_cl10_gammas, build_gamma_F
from z2_hilbert_space import N_GEN, E_kl

sys.path.insert(0, os.path.dirname(__file__))
from phase_z4_physical_projection_test import build_M10

G = build_cl10_gammas()
Gamma_F = build_gamma_F(G)
Gamma_F_HF = kron(Gamma_F, np.eye(N_GEN, dtype=complex))

M10, V = build_M10()
T32 = V @ M10[0] @ V.conj().T
Y01, Y12 = 1.3 + 0.4j, -0.7 + 0.9j
D_F_phys = kron(Y01 * T32, E_kl(0, 1)) + kron(Y12 * T32, E_kl(1, 2))

anticomm = Gamma_F_HF @ D_F_phys + D_F_phys @ Gamma_F_HF
comm = Gamma_F_HF @ D_F_phys - D_F_phys @ Gamma_F_HF
print("||{Gamma_F, D_F_phys}|| (should be ~0 if D_F flips chirality):", np.linalg.norm(anticomm))
print("||[Gamma_F, D_F_phys]|| (should be ~0 if D_F preserves chirality):", np.linalg.norm(comm))
print("||D_F_phys|| for reference:", np.linalg.norm(D_F_phys))

print("\n--- same check on T32 alone (32x32) ---")
anticomm32 = Gamma_F @ T32 + T32 @ Gamma_F
comm32 = Gamma_F @ T32 - T32 @ Gamma_F
print("||{Gamma_F, T32}||:", np.linalg.norm(anticomm32), " ||[Gamma_F, T32]||:", np.linalg.norm(comm32), " ||T32||:", np.linalg.norm(T32))
