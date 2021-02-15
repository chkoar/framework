import numpy as np
from moead_framework.problem.problem import Problem
from moead_framework.solution.one_dimension_solution import OneDimensionSolution


class Mubqp(Problem):
    """
    Implementation of the Multiobjective Unconstrained Binary Quadratic Programming problem.
    The problem is compatible with files generated
    by the mocobench generator http://mocobench.sourceforge.net/index.php?n=Problem.MUBQP
    """
    def __init__(self, instance_file):
        """
        Constructor of the problem

        :param instance_file: {string} text file generated by the mubqp generator : http://mocobench.sourceforge.net/index.php?n=Problem.RMNK#Code
        """
        file = open(instance_file, 'r')
        file_content = list(map(str.strip, file.readlines()))
        file.close()

        file_content = file_content[6:]

        definition = file_content[0].split(" ")
        self.rho = float(definition[2])
        self.m = int(definition[3])
        self.n = int(definition[4])
        self.d = float(definition[5])
        file_content = file_content[2:]

        super().__init__(objective_number=self.m)

        self.qs = np.zeros((self.m, self.n, self.n))
        self.load_qs(file_content)

    def f(self, function_id, solution):
        fit = 0

        for i in range(self.n):
            if solution[i] == 1:
                for j in range(i+1):
                    if solution[j] == 1:
                        fit += self.qs[function_id][i][j]

        return - fit

    def generate_random_solution(self, evaluate=True):
        return self.generate_solution(array=np.random.randint(0, 2, self.n).tolist()[:], evaluate=evaluate)

    def generate_solution(self, array, evaluate=True):
        x = OneDimensionSolution(np.array(array, dtype=int))

        for j in range(self.number_of_objective):
            if evaluate:
                x.F.append(self.f(j, x.solution))
            else:
                x.F.append(None)

        return x

    def load_qs(self, file_content):
        """
        Load values of the instance file

        :param file_content: {list<float>} content of the instance file
        :return:
        """
        line = 0
        for i in range(self.n):
            for j in range(self.n):
                s = file_content[line].split("  ")
                line += 1
                for n in range(self.m):
                    self.qs[n][i][j] = int(s[n])
                pass

