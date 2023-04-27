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
        self.navigation_dict = load_json("tianli_navigation_points_test.json", default_path=fr"{ASSETS_PATH}")
        self._build_navigation_points()
        # self.GIMAP_IMG = cv2.cvtColor(self.GIMAP_RAWIMG, cv2.COLOR_BGRA2RGB)
        plt.title("title")
        plt.ion()
        self.fig, self.axe = plt.subplots(1, 1)
        self.axe.invert_yaxis()
        self.history_dict = {}
        

    def _build_navigation_points(self):
        self.NAVIGATION_POINTS = {}
        for i in self.navigation_dict:
            self.NAVIGATION_POINTS[i] = GenshinNavigationPoint(i, position=self.navigation_dict[i]['position'])
        for i in self.NAVIGATION_POINTS:
            for ii in self.navigation_dict[i]['links']:
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

    def _scatter(self, position, convert=False):
        if convert:
            position = self.convert_cvAutoTrack_to_GIMAP(position)
        plt.scatter(position[0],position[1],c='r',s=50)

    def _arrow(self, p_start, pend, convert=False):
        if convert:
            p_start = self.convert_cvAutoTrack_to_GIMAP(p_start)
            pend = self.convert_cvAutoTrack_to_GIMAP(pend)
        plt.arrow(p_start[0], p_start[1], pend[0]-p_start[0], pend[1]-p_start[1], width=0.3,head_width=2,head_length=2,fc='b')

    def draw_navigation_in_gimap(self, refresh = True):
        # if refresh:
        #     self.fig.canvas.draw()
        if refresh:
            xlim, ylim = plt.xlim(), plt.ylim()
            plt.clf()
        plt.imshow(cv2.cvtColor(self.GIMAP_RAWIMG,cv2.COLOR_BGRA2RGB))
        # print(xlim, ylim)
        for k in self.NAVIGATION_POINTS.items():
            self._scatter(k[1].position, convert=True)
            for link_node in k[1].links:
                # link_node = self.NAVIGATION_POINTS[link]
                self._arrow(k[1].position, link_node.position, convert=True)
            plt.annotate(str(k[0]), xy=tuple(self.convert_cvAutoTrack_to_GIMAP(k[1].position)))
            # print(k[1].position, link_node.position)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        if refresh:
            print(xlim, ylim)
            plt.xlim(xlim)
            plt.ylim(ylim)

    def exec_command(self,x:str):
        """
        exec command when using
        """
        
        for command in x.split(';'):
            cmd = command.split(' ')
            if cmd[0]!='undo':
                self.history_dict = self.navigation_dict
            if cmd[0]=='del':
                self.del_point(cmd[1])
            elif cmd[0]=='link':
                self.link_points(cmd[1], cmd[2])
            elif cmd[0]=='add':
                kid = str(max([int(i[0]) for i in self.navigation_dict.items()])+1)
                upper_link = ''
                full_link = ''
                for c in cmd:
                    if '=' in c:
                        if 'l' == c.split('=')[0]:
                            upper_link = c.split('=')[1]
                        elif 'fl' == c.split('=')[0]:
                            full_link = c.split('=')[1]
                logger.info(f"posi {cmd[1]} kid {kid} upper_link {upper_link} full_link {full_link}")
                self.add_point(list(map(float, cmd[1].split(','))), kid, upper_link=upper_link, full_link=full_link)
            elif cmd[0]=='move':
                self.move_point(cmd[1], list(map(float, cmd[2].split(','))))
            elif cmd[0]=='save':
                self.save()
                logger.info('saved')
            elif cmd[0]=='undo':
                self.navigation_dict = self.history_dict
                logger.info('undo succ')
        self.draw_navigation_in_gimap()

    def analyze_path(self, filename):
        """
        add navigation positions by TeyvatMovePath
        """
        pass
    
    def del_point(self, x):
        """
        del point by id
        """

        for i in self.navigation_dict.items():
            if x in i[1]['links']:
                logger.trace(f"del {i[0]} {i[1]['links']}.pop{i[1]['links'].index(x)}")
                i[1]['links'].pop(i[1]['links'].index(x))

        # for i in self.navigation_dict.items():
        #     if x in [i.id for i in i[1].links]:
        #         i[1].links.pop(i[1].links.index(self.NAVIGATION_POINTS[x]))
        logger.trace(f"pop {x}")
        self.navigation_dict.pop(x)
        # self.NAVIGATION_POINTS.pop(x)
        self._build_navigation_points()

    def link_points(self, x, y):
        self.navigation_dict[x]['links'].append(y)
    
    def move_point(self,x,delta:list):
        """
        move point by id and list[x,y]
        """
        self.navigation_dict[x]['position']=list(np.array(self.navigation_dict[x]['position'])+np.array(delta))

    def add_point(self, posi:list, id:str, upper_link:str='', full_link:str=''):
        posi=list(self.convert_GIMAP_to_cvAutoTrack(posi))
        self.navigation_dict[id] = {
            "position":posi,
            "links":[]
        }
        if upper_link != '':
            for upper_id in upper_link.split(','):
                self.navigation_dict[upper_id]['links'].append(id)
        if full_link != '':
            for upper_id in full_link.split(','):
                self.navigation_dict[upper_id]['links'].append(id)
                self.navigation_dict[id]['links'].append(upper_id)
        self._build_navigation_points()
        # self.NAVIGATION_POINTS[id]=GenshinNavigationPoint(id=id, position=posi)

    def save(self):
        save_json(self.navigation_dict,"tianli_navigation_points_test.json", default_path=fr"{ASSETS_PATH}")

    def speak(self):
        """
        高德地图持续为您导航
        """
        pass
# add 4506,3016
    def run(self):
        self.draw_navigation_in_gimap(refresh=False)
        while 1:
            self.exec_command(input("command:"))

if __name__ == '__main__':
    tlnd = TianLiNavigatorDev()
    tlnd.run()
    # print([f"{i.id}" for i in tn.astar(tn.NAVIGATION_POINTS['1'], tn.NAVIGATION_POINTS['5'])])
    print()


