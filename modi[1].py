import numpy as np

def modi_method(cost, allocation):
    cost = np.array(cost, dtype=float)
    allocation = allocation.astype(float)
    m, n = cost.shape

    for iteration in range(10):
        basic = [(i, j) for i in range(m) for j in range(n)
                 if allocation[i, j] > 1e-9]

        # Find potentials u and v from u_i + v_j = c_ij
        u = [None] * m
        v = [None] * n
        u[0] = 0

        changed = True
        while changed:
            changed = False
            for i, j in basic:
                if u[i] is not None and v[j] is None:
                    v[j] = cost[i, j] - u[i]
                    changed = True
                elif v[j] is not None and u[i] is None:
                    u[i] = cost[i, j] - v[j]
                    changed = True

        # Calculate opportunity costs Δij = cij - ui - vj
        delta = np.full((m, n), np.nan)
        for i in range(m):
            for j in range(n):
                if (i, j) not in basic:
                    delta[i, j] = cost[i, j] - u[i] - v[j]

        print(f"\nMODI iteration {iteration}")
        print("u =", u)
        print("v =", v)
        print("Opportunity-cost matrix (Δ):")
        print(np.round(delta, 2))
        print("Cost =", int(np.sum(cost * allocation)))

        if np.nanmin(delta) >= 0:
            return allocation, np.sum(cost * allocation)

        # Entering cell = most negative opportunity cost
        entering = np.unravel_index(np.nanargmin(delta), delta.shape)

        # Find a closed alternating row/column loop.
        cells = set(basic + [entering])

        def find_cycle(path, row_move):
            i, j = path[-1]
            if row_move:
                candidates = [(i, jj) for jj in range(n)
                              if jj != j and (i, jj) in cells]
            else:
                candidates = [(ii, j) for ii in range(m)
                              if ii != i and (ii, j) in cells]

            for cell in candidates:
                if cell == entering and len(path) >= 4:
                    return path + [cell]
                if cell not in path:
                    result = find_cycle(path + [cell], not row_move)
                    if result:
                        return result
            return None

        cycle = find_cycle([entering], True)
        if cycle is None:
            cycle = find_cycle([entering], False)

        # +, -, +, - ... around the loop
        minus_cells = cycle[1:-1:2]
        theta = min(allocation[i, j] for i, j in minus_cells)

        for k, (i, j) in enumerate(cycle[:-1]):
            if k % 2 == 0:
                allocation[i, j] += theta
            else:
                allocation[i, j] -= theta

        allocation[np.abs(allocation) < 1e-9] = 0

    raise ValueError("MODI did not converge.")


cost = np.array([
    [16, 16, 29, 24],
    [25, 28, 19,  2],
    [ 1, 25, 13, 11]
], dtype=float)

# Initial BFS obtained separately using VAM:
allocation = np.array([
    [ 5, 12,  1,  0],
    [ 0,  0, 11, 14],
    [12,  0,  0,  0]
], dtype=float)

final_allocation, minimum_cost = modi_method(cost, allocation)

print("\n--- FINAL OPTIMAL PLAN ---")
print(final_allocation.astype(int))
print("Minimum transportation cost =", int(minimum_cost))
