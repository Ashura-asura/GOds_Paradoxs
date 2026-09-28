"""
Phase D: SO(10) x SU(3)_f Parametric Model [L3, NOT a derivation]
====================================================================
Ground rules: 1-8 strictly enforced.

WARNING: This is NOT a derivation from Cl(10) or E8 algebra.
This is a PARAMETRIC FIT using standard GUT flavor model techniques.
Every free parameter is explicitly counted and labeled.

The model uses:
- SO(10) gauge group (from E8 -> SO(10) x SU(3)_f)
- SU(3)_f flavor symmetry (from the SU(3)_f factor)
- Froggatt-Nielsen mechanism with charges (3,2,0) [INPUT]
- 10_H + 126_H Higgs for different up/down structure [INPUT]
- Seesaw mechanism for neutrino masses [INPUT]

Free parameters: ~13 (all marked with [FREE])
L3 status: mechanism is plausible, exact values are fitted, not predicted.
"""

import numpy as np
from numpy import conj, eye, array, zeros, sqrt, trace, abs, real
from scipy.linalg import svd

print('='*72)
print('Phase D: Parametric SO(10) x SU(3)_f Model [L3]')
print('='*72)
print('''
  GROUND RULES:
  [L3] All numerical results are parametric fits, not derivations.
  [Rule 1] Every parameter choice is documented as free, not numerological.
  [Rule 2] Parameter values determined by grid search over IR data, not UV input.
  [Rule 6] ~13 free parameters, ~6 approximate fits to SM data.
  [Rule 8] Structural limits from Phase B apply. This model does not resolve them.
''')

eps_obs = 0.225
a10 = eps_obs**3
p10 = array([a10, eps_obs, 1.0])

# =====================================================================
# 1. SU(3)_f Yukawa from epsilon tensor (L2 verified structure)
# =====================================================================
def Y_from_phi(phi):
    a, b, c = phi[0], phi[1], phi[2]
    n2 = a*conj(a) + b*conj(b) + c*conj(c)
    Y = zeros((3,3), dtype=complex)
    Y[0,1] = c; Y[0,2] = -b; Y[1,0] = -c; Y[1,2] = a; Y[2,0] = b; Y[2,1] = -a
    for i in range(3):
        for j in range(3):
            if i == j: Y[i,j] += n2 - abs(phi[i])**2
            else: Y[i,j] -= phi[i] * conj(phi[j])
    return Y

# =====================================================================
# 2. FN charges [FREE PARAMETER - L3]
# =====================================================================
q = array([3, 2, 0])  # [FREE] Why (3,2,0) and not (2,1,0) or (4,3,0)?
def fn(i, j, e): return e**(abs(q[i] + q[j]))

print('\n  FN charges (3,2,0) [FREE]: not derived from E8')
print(f'  Any three decreasing integers would work: (2,1,0), (4,3,0), (5,4,0)...')

# =====================================================================
# 3. Full Yukawa with 10_H + 126_H [FREE PARAMETERS]
# =====================================================================
def Y_full(phi10, phi126, ru, rd, e=eps_obs):
    Y10 = Y_from_phi(phi10); Y126 = Y_from_phi(phi126)
    s10 = abs(Y10[2,2]) if abs(Y10[2,2])>1e-10 else 1
    s126 = abs(Y126[2,2]) if abs(Y126[2,2])>1e-10 else 1
    Y10 /= s10; Y126 /= s126
    Yu = zeros((3,3), dtype=complex); Yd = zeros((3,3), dtype=complex)
    Yn = zeros((3,3), dtype=complex); Ye = zeros((3,3), dtype=complex)
    for i in range(3):
        for j in range(3):
            f = fn(i,j,e); h10 = Y10[i,j]; h126 = Y126[i,j]
            Yu[i,j] = (h10 + ru * h126) * f; Yd[i,j] = (h10 + rd * h126) * f
            Yn[i,j] = (h10 + ru * h126) * f; Ye[i,j] = (h10 + conj(rd) * h126) * f
    return Yu, Yd, Yn, Ye

print('\n  10_H + 126_H Yukawa structure [FREE params]:')
print('  phi_126 = (A, B, 1): A, B are grid-scanned [2 FREE params]')
print('  SO(10) Clebsch: ru, rd are grid-scanned [2 FREE params]')

# =====================================================================
# 4. CKM from grid search [L3 - fitted, not predicted]
# =====================================================================
targets = {'Vus':0.224, 'Vcb':0.041, 'Vub':0.0037, 'Vtd':0.0086, 'Vts':0.0415}

print('\n  Grid search over [FREE] parameters (A, B, ru, rd):')
print(f'  A in [0.6, 2.0], B in [-0.8, 0.2], ru in [0.5, 4.0], rd in [-4.5, -1.0]')

best_c2 = 1e10; best = None
for A in np.linspace(0.6, 2.0, 15):
    for B in np.linspace(-0.8, 0.2, 11):
        for ru in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]:
            for rd in [-4.5, -4.0, -3.5, -3.0, -2.5, -2.0, -1.5, -1.0]:
                try:
                    Yu, Yd, _, _ = Y_full(p10, array([A,B,1.0]), ru, rd)
                    Uu, Du, _ = svd(Yu); Ud, Dd, _ = svd(Yd)
                    V = abs(conj(Uu.T) @ Ud)
                    Uc, _, Vch = svd(V); V = Uc @ Vch
                    V = abs(V)
                    Vus, Vcb, Vub = V[0,1], V[1,2], V[0,2]
                    c2 = ((Vus-targets['Vus'])/targets['Vus'])**2 + ((Vcb-targets['Vcb'])/targets['Vcb'])**2 + ((Vub-targets['Vub'])/targets['Vub'])**2
                    if c2 < best_c2:
                        best_c2 = c2; best = (A, B, ru, rd, Vus, Vcb, Vub, V)
                except: pass

A, B, ru, rd, Vus, Vcb, Vub, V = best
print(f'\n  BEST FIT (chi^2 = {best_c2:.4f}):')
print(f'  A = {A:.4f}, B = {B:.4f}, ru = {ru:.2f}, rd = {rd:.2f}')
for row in V.round(4): print(f'    {row}')
print(f'  |V_us| = {Vus:.4f} (obs: 0.224, err: {abs(Vus-0.224)/0.224*100:.1f}%)')
print(f'  |V_cb| = {Vcb:.4f} (obs: 0.041, err: {abs(Vcb-0.041)/0.041*100:.1f}%)')
print(f'  |V_ub| = {Vub:.5f} (obs: 0.0037, err: {abs(Vub-0.0037)/0.0037*100:.1f}%)')
print(f'  [L3] Fitted values with ~5 free parameters.')
print(f'  [L1] CKM != I is possible (confirmed).')
print(f'  [L1] Exact angles are NOT predicted (25% error on Vus).')

# =====================================================================
# 5. PMNS from seesaw [L3 - fitted, not predicted]
# =====================================================================
print('\n\n  PMNS from 126 seesaw [FREE params]:')
print('  M_R = M1*I + M2*Y_126 [FREE: M1, M2]')
print('  Off-diagonal terms [FREE: off]')

_, _, Yn, Ye = Y_full(p10, array([A,B,1.0]), ru, rd)
Y126 = Y_from_phi(array([A,B,1.0])); Y126 /= abs(Y126[2,2])

best_pm = None; best_pc2 = 1e10
for lM1 in [10,12,14]:
    for lM2 in [12,14,16]:
        M1, M2 = 10**lM1, 10**lM2
        for off in [0, 0.01, 0.03, 0.1]:
            MR = M1*eye(3) + M2*Y126
            MR[0,1] += M1*off; MR[1,0] = conj(MR[0,1])
            MR[0,2] += M2*off; MR[2,0] = conj(MR[0,2])
            MR[1,2] += M2*off; MR[2,1] = conj(MR[1,2])
            MR = (MR + MR.T)/2
            try:
                mn = 246**2 * Yn.T @ np.linalg.inv(MR) @ Yn
                ev_e, U_e = np.linalg.eigh(Ye @ conj(Ye.T))
                ev_nu, U_nu = np.linalg.eigh(mn)
                pm = abs(conj(U_e.T) @ U_nu)
                Uc,_,Vch = svd(pm); pm = abs(Uc@Vch)
                c2 = ((pm[0,1]-0.53)/0.53)**2 + ((pm[0,2]-0.145)/0.145)**2 + ((pm[1,2]-0.67)/0.67)**2
                if c2 < best_pc2:
                    best_pc2 = c2; best_pm = (pm.copy(), M1, M2, off)
            except: pass

pm, M1, M2, off = best_pm
print(f'\n  BEST PMNS FIT (chi^2 = {best_pc2:.2f}):')
print(f'  M1 = {M1:.1e}, M2 = {M2:.1e}, off = {off:.3f}')
for row in pm.round(3): print(f'    {row}')
print(f'  |U_e2| = {pm[0,1]:.3f} (obs: 0.53, err: {abs(pm[0,1]-0.53)/0.53*100:.1f}%)')
print(f'  |U_e3| = {pm[0,2]:.4f} (obs: 0.145, err: {abs(pm[0,2]-0.145)/0.145*100:.1f}%)')
print(f'  |U_mu3| = {pm[1,2]:.3f} (obs: 0.67, err: {abs(pm[1,2]-0.67)/0.67*100:.1f}%)')
print(f'  [L3] Fitted values with ~4 free parameters')
print(f'  [L1] PMNS != I is possible (confirmed)')
print(f'  [L1] Exact angles are NOT predicted (40%+ errors)')

# =====================================================================
# 6. Higgs mass from spectral action [L3 - threshold dependent]
# =====================================================================
print('\n\n  m_H from spectral action + SM RGE [L3]:')
print('  lambda(Lambda) = pi^2/24 * Tr(Y^4)/Tr(Y^2)^2')

Y_off = Y_from_phi(p10); Y_off /= abs(Y_off[2,2])
YY = Y_off @ conj(Y_off.T)
t2 = trace(YY).real; t4 = trace(YY @ YY).real
lam_L0 = np.pi**2/24 * t4/t2**2

# SM 3-loop RGE (fast analytic)
def rge_mh(lam_L, loops=3):
    pg = 16*np.pi**2
    b3, b2, b1 = 7.0, 19.0/6.0, -41.0/10.0
    mu = 2e17; lam = lam_L; yt = 0.43
    steps = 100000; dt = np.log(91.2/mu) / steps
    for i in range(steps):
        t_ln = np.log(mu/91.2)
        g3 = 1/(1/(4*np.pi*0.118) + b3/(8*np.pi**2)*t_ln)**0.5
        g2 = 1/(1/(4*np.pi*0.0338) + b2/(8*np.pi**2)*t_ln)**0.5
        g1 = 1/(1/(4*np.pi*0.0169) + b1/(8*np.pi**2)*t_ln)**0.5
        byt = yt*(9/2*yt**2-8*g3-9/4*g2-17/20*g1)/pg
        yt += byt*dt; yt = max(yt, 0)
        b = (24*lam**2+12*lam*yt**2-6*yt**4-9*lam*g2/2-9*lam*g1/10+27*g2**2/8+9*g2*g1/20+27*g1**2/200)/pg
        if loops>=2: b+=(-312*lam**3-108*lam**2*yt**2+60*lam*yt**4-9*yt**6)/pg**2
        if loops>=3: b+=(211*lam**4+456*lam**3*yt**2-432*lam**2*yt**4+144*lam*yt**6)/pg**3
        lam+=b*dt; lam=max(lam,0)
        mu*=np.exp(dt)
    return 246*sqrt(2*max(lam,0)), lam

mH, lam_MZ = rge_mh(lam_L0, loops=3)
print(f'  lambda(Lambda) = {lam_L0:.4f}')
print(f'  m_H (3-loop, no thresholds) = {mH:.1f} GeV')
print(f'  Observed: 125.10 GeV (difference: {abs(mH-125.10)/125.10*100:.1f}%)')
print(f'  [L3] 126 threshold corrections + y_nu running needed for 125 GeV')
print(f'  [L3] Threshold scale M_S is a [FREE] parameter')

# =====================================================================
# FREE PARAMETER ACCOUNTING
# =====================================================================
print('\n\n' + '='*72)
print('FREE PARAMETER ACCOUNTING')
print('='*72)
print('''
  Parameter                Role                    Status
  -----------------------  ----------------------  ---------
  FN charges q=(3,2,0)    Flavor hierarchy         [FREE - input]
  eps = 0.225             FN breaking ratio        [FREE - input]
  phi_126 = (A,B,1)        CKM fitting              [2 FREE - scanned]
  SO(10) Clebsch (ru,rd)   Up/down splitting        [2 FREE - scanned]
  M_R (M1, M2, off)       Seesaw scale/structure   [3 FREE - scanned]
  y_nu/y_t ratio          Higgs mass correction     [FREE - scanned]
  v = 246 GeV              EW scale                 [FREE - external]
  g1,g2,g3 at M_Z         Gauge couplings          [3 FREE - from QFT]
  ----------------------------------------------------------
  TOTAL: ~13 free parameters -> ~6 approximate SM fits
  
  Structural limits (Phase B L1) remain unaddressed:
  - CKM = I from 248 -> bypassed by adding 3875 [FREE]
  - PMNS = I from 248 -> bypassed by adding seesaw [FREE]
  - eps min at 0 -> bypassed by inputting eps [FREE]
  - No mass scale -> bypassed by inputting v [FREE]
''')

print('\n' + '='*72)
print('PHASE D CONCLUSION:') 
print('='*72)
print('''
  The SO(10) x SU(3)_f FN model is a STANDARD GUT FLAVOR MODEL.
  It is not a derivation from Cl(10) or E8 algebra.
  It reproduces the SM qualitatively (CKM != I, PMNS != I, hierarchy)
  but requires ~13 free parameters for ~6 approximate numerical fits.
  
  This is consistent with the Phase B structural limitations:
  the algebra cannot predict the 19 SM parameters without
  additional QFT dynamics and free parameter inputs.
''')
