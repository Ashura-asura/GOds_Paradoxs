import numpy as np
from numpy import kron, eye, zeros
from itertools import product, combinations

I2 = eye(2, dtype=complex)
I16 = eye(16, dtype=complex)
def K(*mats):
    out = mats[0]
    for m in mats[1:]:
        out = kron(out, m)
    return out

s1 = np.array([[0,1],[1,0]], dtype=complex)
s2 = np.array([[0,-1j],[1j,0]], dtype=complex)
s3 = np.array([[1,0],[0,-1]], dtype=complex)

e = {}
e[1] = 1j * K(s1, s1, s1, s1)
e[2] = 1j * K(s1, s1, s3, I2)
e[3] = -1j * K(s1, s1, s1, s3)
e[4] = -1j * K(s1, s3, I2, I2)
e[5] = -1j * K(s1, s1, s1, s2)
e[6] = -1j * K(s1, s2, I2, I2)
e[7] = 1j * K(s1, s1, s2, I2)
e[8] = 1j * K(s2, I2, I2, I2)
eg = [e[i+1] for i in range(8)]

def eprod_eg(*indices):
    out = I16
    for i in indices:
        out = out @ eg[i]
    return out

B_g = {
    0: -eprod_eg(1, 2, 3, 4) + eprod_eg(1, 2, 5, 6) + eprod_eg(3, 4, 5, 6),
    1:  eprod_eg(0, 2, 3, 5) + eprod_eg(0, 2, 4, 6) + eprod_eg(3, 4, 5, 6),
    2:  eprod_eg(0, 1, 4, 5) - eprod_eg(0, 1, 3, 6) + eprod_eg(3, 4, 5, 6),
    3:  eprod_eg(0, 1, 4, 5) + eprod_eg(0, 2, 4, 6) + eprod_eg(1, 2, 5, 6),
    4: -eprod_eg(0, 1, 3, 6) + eprod_eg(0, 2, 3, 5) + eprod_eg(1, 2, 5, 6),
    5: -eprod_eg(0, 1, 3, 6) + eprod_eg(0, 2, 4, 6) - eprod_eg(1, 2, 3, 4),
    6:  eprod_eg(0, 1, 4, 5) + eprod_eg(0, 2, 3, 5) - eprod_eg(1, 2, 3, 4),
}

g_g = {}
for i in range(7):
    g_g[i] = 0.5 * eg[i] @ eg[7] @ (B_g[i] - I16)

print('g_i property check (anticomm i=j, comm i!=j):')
fail_any = False
for i in range(7):
    for j in range(7):
        if i == j:
            val = g_g[i] @ eg[j] + eg[j] @ g_g[i]
        else:
            val = g_g[i] @ eg[j] - eg[j] @ g_g[i]
        err = np.max(np.abs(val))
        if err > 1e-10:
            fail_any = True
            print(f'  g_{i} vs e_{j}: err={err:.2e} ({"anticomm" if i == j else "comm"})')

if not fail_any:
    print('  All OK')
else:
    print('  Some FAIL')

# Check g_i anticommutation with e_8 (eg[7])
print('\ng_i anticommutation with e_8:')
for i in range(7):
    val = g_g[i] @ eg[7] + eg[7] @ g_g[i]
    err = np.max(np.abs(val))
    status = 'OK' if err < 1e-10 else 'FAIL'
    print(f'  g_{i}: err={err:.2e} {status}')

# Check specific example: g_0 @ e_1 - e_1 @ g_0
print('\nDetailed check g_0 vs e_1:')
g0_e1 = g_g[0] @ eg[1]
e1_g0 = eg[1] @ g_g[0]
diff = g0_e1 - e1_g0
print(f'  max diff: {np.max(np.abs(diff)):.2e}')
print(f'  g0_e1 norm: {np.linalg.norm(g0_e1):.4f}')
print(f'  e1_g0 norm: {np.linalg.norm(e1_g0):.4f}')

# Check B_0 commutation with e_1
print('\nB_0 commutation with e_1:')
b0_e1 = B_g[0] @ eg[1]
e1_b0 = eg[1] @ B_g[0]
diff = b0_e1 - e1_b0
print(f'  max diff: {np.max(np.abs(diff)):.2e}')
sum_ = b0_e1 + e1_b0
print(f'  max sum: {np.max(np.abs(sum_)):.2e} ($\\uparrow$ anticomm if large)')
