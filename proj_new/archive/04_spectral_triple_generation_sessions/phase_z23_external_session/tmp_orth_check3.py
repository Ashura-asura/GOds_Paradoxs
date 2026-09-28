import numpy as np

C = np.array([
[2,0,-1,0,0,0,0,0],
[0,2,0,-1,0,0,0,0],
[-1,0,2,-1,0,0,0,0],
[0,-1,-1,2,-1,0,0,0],
[0,0,0,-1,2,-1,0,0],
[0,0,0,0,-1,2,-1,0],
[0,0,0,0,0,-1,2,-1],
[0,0,0,0,0,0,-1,2]], dtype=float)

def ip(x, y):
    return x @ C @ y

e6 = np.array([
[0,0,0,0,0,1,0,0],
[0,0,0,0,0,0,0,1],
[-1,-1,-1,-2,-1,-1,0,0],
[1,1,2,2,2,1,0,0],
[1,1,1,2,1,1,1,0],
[-1,0,-1,0,0,0,0,0]], dtype=float)

a2 = np.array([
[0,-1,0,0,0,0,0,0],
[0,0,-1,-1,0,0,0,0]], dtype=float)

print("A2 x E6 inner products (must be 0):")
for i in range(2):
    for j in range(6):
        print(f"  a2[{i}] . e6[{j}] = {ip(a2[i], e6[j]):.4f}")

print("\nE6 Cartan matrix (must be E6 up to permutation):")
Ce6 = np.array([[ip(e6[i], e6[j]) for j in range(6)] for i in range(6)])
print(np.rint(Ce6).astype(int))
print("\nA2 Cartan:")
print(np.rint(np.array([[ip(a2[i], a2[j]) for j in range(2)] for i in range(2)])).astype(int))
