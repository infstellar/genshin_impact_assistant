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
    
    def __str__(self):
        return f"GNP: {self.id}"

class TianliNavigator(astar.AStar, MapConverter):
    NAVIGATION_POINTS = {}
    def __init__(self) -> None:
        super().__init__()
        self.navigation_dict = load_json("tianli_navigation_points_test.json", default_path=fr"{ASSETS_PATH}")
        self._build_navigation_points()
        # self.GIMAP_IMG = cv2.cvtColor(self.GIMAP_RAWIMG, cv2.COLOR_BGRA2RGB)
        

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
    GIMAP_RAWIMG = cv2.imread(fr"F:/GIMAP.png")
    def __init__(self) -> None:
        super().__init__()
        plt.title("title")
        plt.ion()
        self.fig, self.axe = plt.subplots(1, 1)
        self.axe.invert_yaxis()
        self.history_dict = {}
        self.scatter_s = 50
        self.head_width = 4
        self.head_length = 6
        self.fig.canvas.mpl_connect('button_press_event', self._on_press)
        self.last_press_x = 0
        self.last_press_y = 0

    def _scatter(self, position, convert=False):
        if convert:
            position = self.convert_cvAutoTrack_to_GIMAP(position)
        plt.scatter(position[0],position[1],c='r',s=self.scatter_s)

    def _arrow(self, p_start, pend, convert=False):
        if convert:
            p_start = self.convert_cvAutoTrack_to_GIMAP(p_start)
            pend = self.convert_cvAutoTrack_to_GIMAP(pend)
        plt.arrow(p_start[0], p_start[1], pend[0]-p_start[0], pend[1]-p_start[1], width=0.3,head_width=self.head_width,head_length=self.head_length,fc='b')

    def _on_press(self, event):
        print("you pressed" ,event.button, event.xdata, event.ydata)
        self.last_press_x = event.xdata
        self.last_press_y = event.ydata
    
    def draw_navigation_in_gimap(self, refresh = True):
        # if refresh:
        #     self.fig.canvas.draw()
        if refresh:
            xlim, ylim = plt.xlim(), plt.ylim()
            plt.clf()
        logger.debug(f"reshow GIMAP")
        plt.imshow(cv2.cvtColor(self.GIMAP_RAWIMG,cv2.COLOR_BGRA2RGB))
        # print(xlim, ylim)
        logger.debug(f"drawing points and links")
        for k in self.NAVIGATION_POINTS.items():
            self._scatter(k[1].position, convert=True)
            for link_node in k[1].links:
                # link_node = self.NAVIGATION_POINTS[link]
                self._arrow(k[1].position, link_node.position, convert=True)
            plt.annotate(str(k[0]), xy=tuple(self.convert_cvAutoTrack_to_GIMAP(k[1].position)))
            # print(k[1].position, link_node.position)
        logger.debug('drawing')
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        logger.debug(f"refreshing")
        if refresh:
            print(xlim, ylim)
            plt.xlim(xlim)
            plt.ylim(ylim)

    def _get_latest_id(self)->str:
        return str(max([int(i[0]) for i in self.navigation_dict.items()])+1)
    
    def exec_command(self,x:str):
        """
        exec command when using
        """
        redraw = True
        for command in x.split(';'):
            cmd = command.split(' ')
            if cmd[0]=='undo': # save as files in the future, python like memory address too much...
                self.navigation_dict = self.history_dict.copy()
                logger.info('undo succ')
            else:
                self.history_dict = self.navigation_dict.copy()
            if cmd[0]=='del':
                if '~' in cmd[1]:
                    start = int(cmd[1].split('~')[0])
                    end = int(cmd[1].split('~')[1])
                    for i in range(start, end):
                        self.del_point(str(i))
                else:
                    self.del_point(cmd[1])
            elif cmd[0]=='link':
                logger.info(f"link {cmd[1]} -> {cmd[2]}")
                self.link_points(cmd[1], cmd[2])
            elif cmd[0]=='add':
                kid = self._get_latest_id()
                upper_link = ''
                full_link = ''
                for c in cmd:
                    if '=' in c:
                        if 'l' == c.split('=')[0]:
                            upper_link = c.split('=')[1]
                        elif 'fl' == c.split('=')[0]:
                            full_link = c.split('=')[1]
                            if full_link == '' or full_link == " ":
                                full_link = str(int(kid)-1)
                        elif 'redraw' == c.split('=')[0]:
                            redraw = bool(int(c.split('=')[1]))
                            logger.info(f"redraw: {redraw}")
                posi = cmd[1]
                if posi in ['a', 'auto', '.']:
                    posi = f"{self.last_press_x},{self.last_press_y}"
                logger.info(f"posi {posi} kid {kid} upper_link {upper_link} full_link {full_link}")
                self.add_point(list(map(float, posi.split(','))), kid, upper_link=upper_link, full_link=full_link)
            elif cmd[0]=='move': # move `x`,`y`
                self.move_point(cmd[1], list(map(float, cmd[2].split(','))))
            elif cmd[0]=='save': # save
                self.save()
                redraw = False
                logger.info('saved')
            elif cmd[0]=='size': # size `x`,`y`,`z`
                self.scatter_s, self.head_width, self.head_length = list(map(int,cmd[1].split(',')))
            elif cmd[0]=='import': # import `tmf path id`
                self.analyze_path(cmd[1])
            elif cmd[0]=='flink': # flink `a` `b`
                logger.info(f"link {cmd[1]} <-> {cmd[2]}")
                self.link_points(cmd[1], cmd[2])
                self.link_points(cmd[2], cmd[1])
            elif cmd[0]=='relink': # relink `a`~`b`
                # 删除a,b间所有id相邻的点，仅保留a,b并将a,b重新全连接。
                logger.info(f"relink {cmd[1]}")
                start = int(cmd[1].split('~')[0])
                end = int(cmd[1].split('~')[1])
                for i in range(start+1, end):
                    self.del_point(str(i))
                self.link_points(str(start), str(end))
                self.link_points(str(end), str(start))
                
        if redraw:
            self._build_navigation_points()
            self.draw_navigation_in_gimap()

    def get_path_file(self, path_file_name:str):
        return load_json(path_file_name+".json","assets\\TeyvatMovePath")
    
    def analyze_path(self, filename):
        """
        add navigation positions by TeyvatMovePath
        """
        path_json = self.get_path_file(filename)
        upper_link = None
        for i in path_json["break_position"]:
            posi = self.convert_cvAutoTrack_to_GIMAP(i)
            curr_id = self._get_latest_id()
            if upper_link != None:
                full_link = upper_link
            else:
                full_link = ''
            logger.info(f"add: {posi} {curr_id} {full_link}")
            self.add_point(list(posi), curr_id, upper_link='', full_link=full_link)
            upper_link = curr_id
            
    
    def del_point(self, x):
        """
        del point by id
        """

        for i in self.navigation_dict.items():
            if x in i[1]['links']:
                logger.info(f"del {i[0]} {i[1]['links']}.pop{i[1]['links'].index(x)}")
                i[1]['links'].pop(i[1]['links'].index(x))

        # for i in self.navigation_dict.items():
        #     if x in [i.id for i in i[1].links]:
        #         i[1].links.pop(i[1].links.index(self.NAVIGATION_POINTS[x]))
        logger.info(f"pop {x}")
        self.navigation_dict.pop(x)
        # self.NAVIGATION_POINTS.pop(x)

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
            try:
                self.exec_command(input("command:"))
            except Exception as e:
                logger.exception(e)

if __name__ == '__main__':
    tlnd = TianLiNavigatorDev()
    # print(list(tlnd.astar(tlnd.NAVIGATION_POINTS['14'], tlnd.NAVIGATION_POINTS['16'])))
    tlnd.run()
    # print([f"{i.id}" for i in tn.astar(tn.NAVIGATION_POINTS['1'], tn.NAVIGATION_POINTS['5'])])
    print()


