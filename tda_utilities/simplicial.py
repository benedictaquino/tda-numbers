"""Topological Feature Selection Functions"""
from __future__ import annotations
from itertools import combinations, product

NONETYPE_ERROR_MESSAGES = (
    "unsupported operand type(s) for -: 'NoneType' and 'set'",
    "unsupported operand type(s) for |=: 'set' and 'NoneType'",
    "unsupported operand type(s) for |: 'NoneType' and 'NoneType'"
)


class Simplex:
    """Defines a k-simplex object"""
    def __init__(self, *points):
        """Simplex takes arguments as points that can make up a k-simplex"""
        self.__points = frozenset(points)

    @property
    def points(self) -> frozenset:
        """points of the simplex"""
        return self.__points

    @property
    def k(self) -> int:
        """dimension of the simplex"""
        return len(self.points) - 1

    @property
    def boundary(self) -> set:
        """returns the union of faces of the simplex"""
        if not self:
            return None
        combos = combinations(self.points, self.k)
        return {Simplex(*combo) for combo in combos}

    @property
    def interior(self) -> set:
        """returns the complement of the boundary"""
        if not self:
            return None
        subset = set()
        for k in range(1, self.k):
            combos = combinations(self.points, k)
            subset |= {Simplex(*combo) for combo in combos}
        return subset

    def __len__(self) -> int:
        return self.k

    def __contains__(self, other) -> object:
        return other in self.points

    def __repr__(self):
        point_string = ' '.join(str(point) for point in self.points)
        return f'{self.k}-simplex: ' + point_string

    def __eq__(self, other) -> bool:
        if type(other) == self.__class__:
            return self.points == other.points
        return False

    def __lt__(self, other) -> bool:
        return len(self) < len(other)

    def __hash__(self) -> int:
        return hash(self.points)


class SimplicialComplex:
    """Defines a simplicial complex"""
    def __init__(self, *simplices):
        """adds all faces of simplices passed in to simplicial complex"""
        simplex_set = set(simplices)
        for simplex in simplices:
            try:
                simplex_set |= simplex.boundary | simplex.interior
            except TypeError as error_message:
                if str(error_message) in NONETYPE_ERROR_MESSAGES:
                    pass
                else:
                    raise TypeError(error_message)
        self.__simplices = simplex_set

    @property
    def simplices(self):
        return self.__simplices

    @property
    def k(self):
        return len(max(self.simplices))  # largest dimension simplex

    def __len__(self) -> int:
        return self.k

    def __repr__(self):
        return f'simplicial {self.k}-complex'

    def __iter__(self):
        return self.simplices.__iter__()

    def __contains__(self, other) -> bool:
        return other in self.simplices

    def __eq__(self, other) -> bool:
        return self.simplices == other.simplices

    def closure(self, *simplices) -> SimplicialComplex:
        """return the closure of the subset of simplices in a k-complex"""
        if not set(simplices).issubset(self.simplices):
            raise ValueError('not a subset of the complex')
        return SimplicialComplex(*simplices)

    def star(self, *simplices) -> SimplicialComplex:
        """return the star of the set of simplices"""
        simplices = set(simplices)
        star = set()
        for simplex_1, simplex_2 in product(simplices, self.simplices):
            if simplex_1 in self.closure(simplex_2):
                star.add(simplex_2)
        return star if star else None

    def link(self, *simplices) -> SimplicialComplex:
        """return the link of the set of simplices"""
        simplices = set(simplices)
        star = self.star(*simplices)
        closed_star = self.closure(*star).simplices
        return closed_star - star

    def chain(self, k):
        """returns the k-chain"""
        raise NotImplementedError


class SimplicialChain:
    """Defines a simplicial k-chain"""
    def __init__(self, complex: SimplicialComplex, orientation: int = 0):
        # TODO: ???
        raise NotImplementedError
        self.chain = None
        self.orientation = orientation

    def boundary(self):
        """returns a (k-1)-Chain"""
        raise NotImplementedError


class Filtration:
    """Filtration object"""
    # TODO: All of this I guess
    def __init__(self):
        raise NotImplementedError

    def create_filtration(self):
        raise NotImplementedError
