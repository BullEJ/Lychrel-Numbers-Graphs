from networkx import DiGraph, is_isomorphic
from utilities import antecesores, falta_completar
class Rama(DiGraph):
    def __init__(self, l1: tuple):
        super().__init__()
        self.fri : tuple[int] = l1
        
        filter_seeds = falta_completar((l1, ))
        while filter_seeds:
            for nodo in filter_seeds:
                self.add_edges_from(map(
                    lambda ant: (ant, nodo), # (antecesor, sucesor)
                    antecesores(nodo)))

            filter_seeds = falta_completar(map(
                            lambda nodo: self.predecessors(nodo),
                            filter_seeds))

    def __eq__(self, other):
        return is_isomorphic(self, other)

    def __hash__(self):
     	return hash(self.number_of_edges())