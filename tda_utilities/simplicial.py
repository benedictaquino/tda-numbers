"""Topological Feature Selection Functions"""
from __future__ import annotations
from itertools import combinations, product

NONE_ERROR_MESSAGES = (
    "unsupported operand type(s) for -: 'NoneType' and 'set'",
    "unsupported operand type(s) for |=: 'set' and 'NoneType'"
)


class Simplex:
    """Defines a k-simplex object"""
    def __init__(self, *points):
        """Simplex takes arguments as points that can make up a k-simplex"""
        self.points = frozenset(points)
        self.k = len(self.points) - 1  # k-simplex
        if self.k < 0:
            raise ValueError('Simplex requires at least one point')

    def __len__(self) -> int:
        return self.k

    def __contains__(self, other) -> object:
        return other in self.points

    def __repr__(self):
        return f'{self.k}-simplex: '\
            + ' '.join(str(point) for point in self.points)

    def __lt__(self, other) -> bool:
        return len(self) < len(other)

    def __eq__(self, other) -> bool:
        if type(other) == self.__class__:
            return self.points == other.points
        return False

    def __hash__(self) -> int:
        return hash(self.points)

    def faces(self) -> tuple:
        if not self:
            return None
        return set([Simplex(*combo)
                    for combo in combinations(self.points, self.k)])

    def orient(self, sigma: int):
        """assigns an orientation to the simplex"""
        self.orientation = sigma


class SimplicialComplex:
    """Defines a simplicial complex"""
    def __init__(self, *simplices):
        self.simplices = set(simplices)
        self._build_complex()
        self.k = len(max(self.simplices))  # largest dimension simplex

    def _build_complex(self):
        """add all faces of each simplex"""
        simplex_list = list(self.simplices)
        for simplex in simplex_list:
            try:
                simplex_list += list(simplex.faces() - self.simplices)
                self.simplices |= simplex.faces()
            except TypeError as error_message:
                if str(error_message) in NONE_ERROR_MESSAGES:
                    pass
                else:
                    raise TypeError(error_message)

    def __len__(self) -> int:
        return self.k

    def __lt__(self, other):
        return len(self) < len(other)

    def __repr__(self):
        return f'simplicial {self.k}-complex'

    def __iter__(self):
        return self.simplices.__iter__()

    def __getitem__(self, i: int) -> Simplex:
        return list(self.simplices)[i]

    def closure(self, *simplices) -> SimplicialComplex:
        """return the closure of the subset of simplices in a k-complex"""
        subset = set(simplices)

        for simplex in simplices:
            if simplex not in self:
                raise ValueError('not a subset of the complex')
            try:
                subset |= simplex.faces()
            except TypeError as error_message:
                if str(error_message) in NONE_ERROR_MESSAGES:
                    pass
                else:
                    raise TypeError(error_message)

        return SimplicialComplex(*subset)

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
    """Filtration object
    """
    # TODO: All of this I guess
    def __init__(self):
        raise NotImplementedError

    def create_filtration(self):
        raise NotImplementedError