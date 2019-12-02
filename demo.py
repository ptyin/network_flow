from bipartite_matching import Solver
import numpy as np

left = 3
right = 3
A = np.array([[1, 0, 0], [1, 1, 1], [0, 1, 0]])

solver = Solver(left, right, A)
solver.solve()

for i in range(left):
    for j in range(right):
        print(solver.X[i][j].varValue, end=", ")
    print("\n")

print('Max Matching: %g' % solver.ans())