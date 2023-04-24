# -*- coding: utf-8 -*-

"""

Copyright (c) 2012-2021, Julien Rialland
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the {organization} nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

""" generic A-Star path searching algorithm """

import logging
from abc import ABC, abstractmethod
from heapq import heapify, heappush, heappop
from typing import Type, Callable, Dict, Iterable, Union, TypeVar, Generic
from math import inf as infinity

# introduce generic type
T = TypeVar("T")


################################################################################
class SearchNode(Generic[T]):
    """Representation of a search node"""

    __slots__ = ("data", "gscore", "fscore", "closed", "came_from", "in_openset")

    def __init__(
        self, data: T, gscore: float = infinity, fscore: float = infinity
    ) -> None:
        self.data = data
        self.gscore = gscore
        self.fscore = fscore
        self.closed = False
        self.in_openset = False
        self.came_from: Union[None, SearchNode[T]] = None

    def __lt__(self, b: "SearchNode[T]") -> bool:
        """Natural order is based on the fscore value & is used by heapq operations"""
        return self.fscore < b.fscore


################################################################################
class SearchNodeDict(Dict[T, SearchNode[T]]):
    """A dict that returns a new SearchNode when a key is missing"""

    def __missing__(self, k) -> SearchNode[T]:
        v = SearchNode(k)
        self.__setitem__(k, v)
        return v


################################################################################
SNType = TypeVar("SNType", bound=SearchNode)


class OpenSet(ABC, Generic[SNType]):
    """As we may have performance issues with the heapq module when an item is
    re-inserted, we may use other implementations for this feature.

     - By default the HeapQOpenSet class just relies on the heapq module, it does not need any external dependency.

     - The SortedContainersOpenSet class uses the sortedcointainers module. As
       this module is optional, it will be used only if your own project
       depends on it.

    """

    @abstractmethod
    def push(self, item: SNType) -> None:
        """Add an item to the queue"""
        raise NotImplementedError

    @abstractmethod
    def pop(self) -> SNType:
        """Remove and return the smallest item from the queue"""
        raise NotImplementedError

    @abstractmethod
    def remove(self, item: SNType) -> None:
        """remove an item from the queue, ensuring that the queue is still valid afterwards"""
        raise NotImplementedError


################################################################################
class HeapQOpenSet(OpenSet[SNType], Generic[SNType]):
    """just a wrapper around heapq operations"""

    def __init__(self):
        self.heap = []
        heapify(self.heap)

    def push(self, item: SNType) -> None:
        """Add an item to the queue"""
        item.in_openset = True
        heappush(self.heap, item)

    def pop(self) -> SNType:
        """Remove and return the smallest item from the queue"""
        item = heappop(self.heap)
        item.in_openset = False
        return item

    def remove(self, item: SNType):
        self.heap.remove(item)
        heapify(
            self.heap
        )  # costly operation but necessary as remove operation destroy the structure of the heap
        item.in_openset = False


################################################################################
OpenSetImpl: Type[OpenSet] = HeapQOpenSet

try:
    import sortedcontainers

    class SortedContainersOpenSet(OpenSet[SNType], Generic[SNType]):
        def __init__(self):
            self.sortedlist = sortedcontainers.SortedList(key=lambda x: x.fscore)

        def push(self, item: SNType) -> None:
            item.in_openset = True
            self.sortedlist.add(item)

        def pop(self) -> SNType:
            item = self.sortedlist.pop(0)
            item.in_openset = False
            return item

        def remove(self, item: SNType):
            self.sortedlist.remove(item)
            item.in_openset = False

    OpenSetImpl = SortedContainersOpenSet
    logging.info("using sortedcontainers for heap operations")

except Exception as e:
    logging.info("sortedcontainers module not loaded, using the default heapq module")


################################################################################*


class AStar(ABC, Generic[T]):
    __slots__ = ()

    @abstractmethod
    def heuristic_cost_estimate(self, current: T, goal: T) -> float:
        """
        Computes the estimated (rough) distance between a node and the goal.
        The second parameter is always the goal.
        This method must be implemented in a subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def distance_between(self, n1: T, n2: T) -> float:
        """
        Gives the real distance between two adjacent nodes n1 and n2 (i.e n2
        belongs to the list of n1's neighbors).
        n2 is guaranteed to belong to the list returned by the call to neighbors(n1).
        This method must be implemented in a subclass.
        """

    @abstractmethod
    def neighbors(self, node: T) -> Iterable[T]:
        """
        For a given node, returns (or yields) the list of its neighbors.
        This method must be implemented in a subclass.
        """
        raise NotImplementedError

    def is_goal_reached(self, current: T, goal: T) -> bool:
        """
        Returns true when we can consider that 'current' is the goal.
        The default implementation simply compares `current == goal`, but this
        method can be overwritten in a subclass to provide more refined checks.
        """
        return current == goal

    def reconstruct_path(self, last: SearchNode, reversePath=False) -> Iterable[T]:
        def _gen():
            current = last
            while current:
                yield current.data
                current = current.came_from

        if reversePath:
            return _gen()
        else:
            return reversed(list(_gen()))

    def astar(
        self, start: T, goal: T, reversePath: bool = False
    ) -> Union[Iterable[T], None]:
        if self.is_goal_reached(start, goal):
            return [start]

        openSet: OpenSet[SearchNode[T]] = OpenSetImpl()
        searchNodes: SearchNodeDict[T] = SearchNodeDict()
        startNode = searchNodes[start] = SearchNode(
            start, gscore=0.0, fscore=self.heuristic_cost_estimate(start, goal)
        )
        openSet.push(startNode)

        while openSet:
            current = openSet.pop()

            if self.is_goal_reached(current.data, goal):
                return self.reconstruct_path(current, reversePath)

            current.closed = True

            for neighbor in map(lambda n: searchNodes[n], self.neighbors(current.data)):
                if neighbor.closed:
                    continue

                tentative_gscore = current.gscore + self.distance_between(
                    current.data, neighbor.data
                )

                if tentative_gscore >= neighbor.gscore:
                    continue

                neighbor_from_openset = neighbor.in_openset

                if neighbor_from_openset:
                    # we have to remove the item from the heap, as its score has changed
                    openSet.remove(neighbor)

                # update the node
                neighbor.came_from = current
                neighbor.gscore = tentative_gscore
                neighbor.fscore = tentative_gscore + self.heuristic_cost_estimate(
                    neighbor.data, goal
                )

                openSet.push(neighbor)

        return None


################################################################################
U = TypeVar("U")


def find_path(
    start: U,
    goal: U,
    neighbors_fnct: Callable[[U], Iterable[U]],
    reversePath=False,
    heuristic_cost_estimate_fnct: Callable[[U, U], float] = lambda a, b: infinity,
    distance_between_fnct: Callable[[U, U], float] = lambda a, b: 1.0,
    is_goal_reached_fnct: Callable[[U, U], bool] = lambda a, b: a == b,
) -> Union[Iterable[U], None]:
    """A non-class version of the path finding algorithm"""

    class FindPath(AStar):
        def heuristic_cost_estimate(self, current: U, goal: U) -> float:
            return heuristic_cost_estimate_fnct(current, goal)  # type: ignore

        def distance_between(self, n1: U, n2: U) -> float:
            return distance_between_fnct(n1, n2)

        def neighbors(self, node) -> Iterable[U]:
            return neighbors_fnct(node)  # type: ignore

        def is_goal_reached(self, current: U, goal: U) -> bool:
            return is_goal_reached_fnct(current, goal)

    return FindPath().astar(start, goal, reversePath)


__all__ = ["AStar", "find_path"]
