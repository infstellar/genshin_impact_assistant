import datetime

import pytz
from source.util import *
from source.map.extractor.convert import MapConverter

def is_real_index(i):
            # if i==0:return True
            # if i==1:return False
            # if i==2:return True
            # if i==3:return False
            # if i==4:return False
            # if i==5:return False
            # if i==6:return True
            # if i==7:return False
            # if i==8:return False
            # if i==9:return False
            # if i==10:return True
            # if i==11:return False
            
            
            
            return (i==0 or (i-2)%4==0)

def convert_tavern_curve_to_cvat(curve_poi:t.List[list]):
    tianli_posi_list = []
    for i in range(len(curve_poi)):
        if is_real_index(i):
            ky_posi = curve_poi[i]['x'], curve_poi[i]['y']
            tianli_posi_list.append(list(MapConverter.convert_kongying_curve_to_cvAutoTrack(ky_posi, decimal=2)))
    return tianli_posi_list


def convert_cvat_to_tavern_curve(tianli_posi_list:t.List[t.List]):
    curve_pos = []
    # 3 -> 8; 4 -> 12; 2 -> 4
    tl_pos = [tianli_posi_list[0][0], tianli_posi_list[0][1]]
    for i in range((len(tianli_posi_list) - 1)*4):
        if i != 0:
            ii = int((i-2)/4)+1
        else:
            ii = i
        if is_real_index(i):
            tl_pos = [tianli_posi_list[ii][0], tianli_posi_list[ii][1]]
        else:
            if ii >= len(tianli_posi_list) -1:
                # last point
                tl_pos = [(tianli_posi_list[ii-1][0]+tl_pos[0])/2, (tianli_posi_list[ii-1][1]+tl_pos[1])/2]
            else:
                tl_pos = [(tianli_posi_list[ii+1][0]+tl_pos[0])/2, (tianli_posi_list[ii+1][1]+tl_pos[1])/2]
        ky_pos = list(MapConverter.convert_cvAutoTrack_to_kongying_curve(tl_pos, decimal=2))
        curve_pos.append({
            'x': ky_pos[0],
            'y': ky_pos[1]
        })
    tz = pytz.timezone('Etc/GMT-8')
    t = datetime.datetime.now(tz)
    date = t.strftime("%Y%m%d%H%M%S")
    curve_dict = {
    "curveName": f"GIA-Generate-{date}",
    "curve_list": [
        {
            "lineName": "GIA-Generate",
            "curve_poi": curve_pos
        }
    ]
}
    return curve_dict

if __name__ == '__main__':
    S = [[-1004.39, -2406.393], [-1002.3100000000001, -2406.122], [-983.422, -2468.528], [-980.354, -2473.13], [-918.219, -2512.508], [-912.338, -2513.787], [-907.479, -2510.207], [-901.087, -2508.673], [-895.206, -2506.627], [-890.347, -2503.047], [-872.448, -2480.546], [-862.732, -2477.989], [-845.6, -2478.5], [-803.921, -2489.24], [-796.506, -2493.075], [-788.834, -2497.422], [-766.077, -2498.445], [-709.056, -2518.389], [-701.385, -2521.713], [-681.696, -2532.197], [-674.025, -2551.119], [-668.656, -2556.744], [-662.774, -2557.0], [-654.848, -2557.767], [-613.936, -2565.182], [-606.265, -2567.739], [-599.872, -2569.529], [-592.201, -2568.762], [-577.115, -2554.443], [-571.745, -2554.699], [-565.097, -2558.278], [-553.335, -2566.461], [-550.011, -2571.319], [-539.016, -2576.178], [-530.578, -2576.945], [-524.696, -2576.178], [-506.286, -2572.086]]
    saas = convert_cvat_to_tavern_curve(S)
    print(saas)
    save_json(x=saas, all_path=r"M:\ProgramData\GIA\genshin_impact_assistant\dev_assets\tlpp\导出的画布.json")
    print()