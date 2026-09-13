import numpy as np

def vogel_approximation(cost, supply, demand):
    cost = np.array(cost, dtype=float)
    supply = supply.copy()
    demand = demand.copy()

    m, n = cost.shape
    allocation = np.zeros((m, n))
    active_rows = [True] * m
    active_cols = [True] * n

    while any(active_rows) and any(active_cols):
        row_penalty = []
        for i in range(m):
            if not active_rows[i]:
                row_penalty.append(-1)
                continue
            vals = [cost[i, j] for j in range(n) if active_cols[j]]
            vals.sort()
            row_penalty.append(vals[0] if len(vals) == 1
                               else vals[1] - vals[0])

        col_penalty = []
        for j in range(n):
            if not active_cols[j]:
                col_penalty.append(-1)
                continue
            vals = [cost[i, j] for i in range(m) if active_rows[i]]
            vals.sort()
            col_penalty.append(vals[0] if len(vals) == 1
                               else vals[1] - vals[0])

        if max(row_penalty) >= max(col_penalty):
            i = int(np.argmax(row_penalty))
            j = min((j for j in range(n) if active_cols[j]),
                    key=lambda j: cost[i, j])
        else:
            j = int(np.argmax(col_penalty))
            i = min((i for i in range(m) if active_rows[i]),
                    key=lambda i: cost[i, j])

        quantity = min(supply[i], demand[j])
        allocation[i, j] = quantity
        supply[i] -= quantity
        demand[j] -= quantity

        if supply[i] == 0:
            active_rows[i] = False
        if demand[j] == 0:
            active_cols[j] = False

    return allocation


cost = np.array([
    [16, 16, 29, 24],
    [25, 28, 19,  2],
    [ 1, 25, 13, 11]
], dtype=float)

supply = [18, 25, 12]
demand = [17, 12, 12, 14]

allocation = vogel_approximation(cost, supply, demand)
total_cost = np.sum(cost * allocation)

print("VAM Initial Basic Feasible Solution")
print(allocation.astype(int))
print("\nTotal transportation cost =", int(total_cost))
