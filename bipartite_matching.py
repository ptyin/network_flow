import numpy as np
import pulp


class Solver:
    def __init__(self, left=0, right=0, A=None):
        self.left = left
        self.right = right
        self.A = A
        self.X = []
        self.m = pulp.LpProblem(name="MIP_Model", sense=pulp.LpMaximize)

    def solve(self):

        self.X = []
        for i in range(self.left):
            self.X.append([])
            for j in range(self.right):
                self.X[i].append(pulp.LpVariable(cat=pulp.LpBinary, name="x" + str(i) + str(j)))

        for i in range(self.left):
            self.m += pulp.LpConstraint(sum([self.X[i][j] for j in range(self.right)]), sense=pulp.LpConstraintLE, rhs=1)

        for j in range(self.right):
            self.m += pulp.LpConstraint(sum([self.X[i][j] for i in range(self.left)]), sense=pulp.LpConstraintLE, rhs=1)

        for i in range(self.left):
            for j in range(self.right):
                self.m += pulp.LpConstraint(self.X[i][j], sense=pulp.LpConstraintLE, rhs=self.A[i, j])

        self.m.setObjective(sum([self.X[i][j] for i in range(self.left) for j in range(self.right)]))

        self.m.solve()

    def ans(self):
        return self.m.objective.value()


if __name__ == '__main__':
    left = int(input("Input the number of vertices in left set: "))
    right = int(input("Input the number of vertices in right set: "))

    A = np.zeros((left, right), dtype=int)
    while(True):
        try:
            i, j = input("Input one pair(press CTRL+D to stop): ").split(" ")
            A[int(i), int(j)] = 1
        except EOFError:
            break

    solver = Solver(left, right, A)
    solver.solve()

    for i in range(left):
        for j in range(right):
            print(solver.X[i][j].varValue, end=", ")
        print("\n")

    print('Max Matching: %g' % solver.ans())



