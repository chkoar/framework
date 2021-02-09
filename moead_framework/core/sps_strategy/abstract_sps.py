from abc import ABC, abstractmethod


class SpsStrategy(ABC):

    def __init__(self, algorithm_instance):
        """
        :param algorithm_instance: {:class:`~moead_framework.algorithm.abstract_moead.py.AbstractMoead`} instance of the algorithm
        """
        self.algorithm = algorithm_instance

    @abstractmethod
    def get_sub_problems(self):
        """
        get all sub-problems visited in the next generation

        :return: {list<integer>} indexes of sub-problems
        """
