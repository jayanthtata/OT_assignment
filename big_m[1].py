import numpy as np

def big_m_simplex(A, b, c, senses, M=1000000, max_iter=20):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    c = np.array(c, dtype=float)
    senses = senses.copy()

    m, n = A.shape
    names = [f"x{i+1}" for i in range(n)]
    tableau = A.copy()
    cj = list(c)
    basis = []

    for i, sense in enumerate(senses):
        if sense == "<=":
            col = np.zeros(m); col[i] = 1
            tableau = np.column_stack((tableau, col))
            names.append(f"s{i+1}"); cj.append(0)
            basis.append(len(cj) - 1)

        elif sense == ">=":
            col = np.zeros(m); col[i] = -1
            tableau = np.column_stack((tableau, col))
            names.append(f"s{i+1}"); cj.append(0)

            col = np.zeros(m); col[i] = 1
            tableau = np.column_stack((tableau, col))
            names.append(f"a{i+1}"); cj.append(-M)
            basis.append(len(cj) - 1)

        else:  # equality
            col = np.zeros(m); col[i] = 1
            tableau = np.column_stack((tableau, col))
            names.append(f"a{i+1}"); cj.append(-M)
            basis.append(len(cj) - 1)

    tableau = np.column_stack((tableau, b))
    cj = np.array(cj, dtype=float)

    for iteration in range(max_iter):
        cb = np.array([cj[j] for j in basis])
        zj = cb @ tableau[:, :-1]
        z = cb @ tableau[:, -1]
        reduced = cj - zj

        print(f"\nIteration {iteration}")
        print("Basis:", [names[j] for j in basis])
        print("Z =", round(z, 4))
        print("Cj-Zj:", np.round(reduced, 4))

        entering = int(np.argmax(reduced))
        if reduced[entering] <= 1e-9:
            break

        ratios = []
        for i in range(m):
            if tableau[i, entering] > 1e-9:
                ratios.append(tableau[i, -1] / tableau[i, entering])
            else:
                ratios.append(np.inf)

        leaving = int(np.argmin(ratios))
        if ratios[leaving] == np.inf:
            raise ValueError("The problem is unbounded.")

        pivot = tableau[leaving, entering]
        tableau[leaving] /= pivot

        for i in range(m):
            if i != leaving:
                tableau[i] -= tableau[i, entering] * tableau[leaving]

        basis[leaving] = entering

    values = np.zeros(len(cj))
    for i, j in enumerate(basis):
        values[j] = tableau[i, -1]

    artificial_values = [
        values[i] for i, name in enumerate(names) if name.startswith("a")
    ]
    if any(abs(v) > 1e-7 for v in artificial_values):
        raise ValueError("No feasible solution exists.")

    return values, cj @ values, names


# Case study:
# Maximize Z = 3x1 + 5x2
# x1 + 2x2 <= 8
# 3x1 + 2x2 >= 12
# x1, x2 >= 0

A = [[1, 2],
     [3, 2]]
b = [8, 12]
c = [3, 5]
senses = ["<=", ">="]

values, optimum, names = big_m_simplex(A, b, c, senses)

print("\n--- FINAL RESULT ---")
for name, value in zip(names, values):
    print(f"{name} = {value:.2f}")
print(f"Optimal objective value Z = {optimum:.2f}")
