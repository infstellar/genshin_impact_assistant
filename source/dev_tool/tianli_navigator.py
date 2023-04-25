from source.util import *
import source.astar as astar
import gimap
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from source.map.extractor.convert import MapConverter

import matplotlib.image as mpimg
class GenshinNavigationPoint():
    def __init__(self, id, position):
        self.id = id
        self.position = position
        self.links = []

class TianliNavigator(astar.AStar, MapConverter):
    NAVIGATION_POINTS = {}
    GIMAP_RAWIMG = cv2.imread(fr"F:/GIMAP.png")
    def __init__(self) -> None:
        super().__init__()
        ps = load_json("tianli_navigation_points_test.json", default_path=fr"{ASSETS_PATH}")
        self._build_navigation_points(ps)
        # self.GIMAP_IMG = cv2.cvtColor(self.GIMAP_RAWIMG, cv2.COLOR_BGRA2RGB)

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

    

class TianLiNavigatorDev(TianliNavigator):
    def __init__(self) -> None:
        super().__init__()

    def draw_navigation_in_gimap(self):
        fig, axe = plt.subplots(1, 1)
        plt.title("title")
        axe.invert_yaxis()
        plt.imshow(cv2.cvtColor(self.GIMAP_RAWIMG,cv2.COLOR_BGRA2RGB))
        xs = [self.convert_cvAutoTrack_to_GIMAP(p[1].position[0]) for p in self.NAVIGATION_POINTS.items()]
        ys = [self.convert_cvAutoTrack_to_GIMAP(p[1].position[1]) for p in self.NAVIGATION_POINTS.items()]
        print(xs,ys)
        plt.scatter(xs,ys)
        plt.show()

    def exec_command(self,x):
        """
        exec command when using
        """
        pass

    def analyze_path(self, filename):
        """
        add navigation positions by TeyvatMovePath
        """
        pass
    
    def del_point(self, x):
        """
        del point by id
        """
        pass

    def move_point(self,x,delta:list):
        """
        move point by id and list[x,y]
        """
        pass
    
    def speak(self):
        """
        高德地图持续为您导航
        """
        pass

if __name__ == '__main__':
    tn = TianLiNavigatorDev()
    tn.draw_navigation_in_gimap()
    # print([f"{i.id}" for i in tn.astar(tn.NAVIGATION_POINTS['1'], tn.NAVIGATION_POINTS['5'])])
    print()


