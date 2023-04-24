from source.util import *
import source.astar as astar
import gimap

class GenshinNavigationPoint():
    def __init__(self, id, position):
        self.id = id
        self.position = position
        self.links = []

class TianliNavigator(astar.AStar):
    NAVIGATION_POINTS = {}
    def __init__(self) -> None:
        super().__init__()
        ps = load_json("tianli_navigation_points_test.json", default_path=fr"{ASSETS_PATH}")
        self._build_navigation_points(ps)

    def _build_navigation_points(self, ps:dict):
        for i in ps:
            inti = int(i)
            self.NAVIGATION_POINTS[i] = GenshinNavigationPoint(i, position=ps[i]['position'])
        for i in self.NAVIGATION_POINTS:
            for ii in ps[i]['links']:
                self.NAVIGATION_POINTS[i].links.append(self.NAVIGATION_POINTS[ii])
    
    def _distance(self, n1:GenshinNavigationPoint, n2:GenshinNavigationPoint):
        """computes the distance between two stations"""
        latA, longA = n1.position
        latB, longB = n2.position
        # convert degres to radians!!
        latA, latB, longA, longB = map(
            lambda d: d * math.pi / 180, (latA, latB, longA, longB))
        x = (longB - longA) * math.cos((latA + latB) / 2)
        y = latB - latA
        return math.hypot(x, y)
    
    def heuristic_cost_estimate(self, current, goal) -> float:
        """
        Computes the estimated (rough) distance between a node and the goal.
        The second parameter is always the goal.
        This method must be implemented in a subclass.
        """
        return self._distance(current, goal)

    def distance_between(self, n1:GenshinNavigationPoint, n2:GenshinNavigationPoint) -> float:
        """
        Gives the real distance between two adjacent nodes n1 and n2 (i.e n2
        belongs to the list of n1's neighbors).
        n2 is guaranteed to belong to the list returned by the call to neighbors(n1).
        This method must be implemented in a subclass.
        """
        return self._distance(n1, n2)

    def neighbors(self, node:GenshinNavigationPoint):
        """
        For a given node, returns (or yields) the list of its neighbors.
        This method must be implemented in a subclass.
        """
        return node.links
    
    def draw_navigation_in_gimap(self):
        pass

tn = TianliNavigator()
if __name__ == '__main__':
    print([f"{i.id}" for i in tn.astar(tn.NAVIGATION_POINTS['1'], tn.NAVIGATION_POINTS['5'])])
    print()


