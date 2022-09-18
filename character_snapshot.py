from unit import *
from interaction_background import Interaction_BGD
import cv2
itt=Interaction_BGD()
ly=96
posi_charalist_q=[[339-ly,1591,339-ly+55,1591+55],[339,1591,339+55,1591+55],[339+ly,1591,339+ly+55,1591+55],[339+2*ly,1591,339+2*ly+55,1591+55]]
hp_charalist_posi=[[283,1698],[379,1698],[475,1698],[571,1698]]
posi_chara_list=[[218,1779,218+68,1779+61],[218+ly,1779,218+ly+68,1779+61],[218+2*ly,1779,218+2*ly+68,1779+61],[218+3*ly,1779,218+3*ly+68,1779+61]]
posi_chara_q=[915,1766,1015,1866]
posi_chara_e=[965,1666,1015,1716]

while(1):
    input("等待按键")
    cap=itt.capture()
    print('color: ')
    for i in range(4):
        cv2.imwrite('outputimgs/character_'+str(i)+'.png',cap[posi_chara_list[i][0]:posi_chara_list[i][2],posi_chara_list[i][1]:posi_chara_list[i][3]])
        cv2.imwrite('outputimgs/character_Q_'+str(i)+'.png',cap[posi_charalist_q[i][0]:posi_charalist_q[i][2],posi_charalist_q[i][1]:posi_charalist_q[i][3]])
        print(cap[hp_charalist_posi[i][0],hp_charalist_posi[i][1]],end='   ')
    
    cv2.imwrite('outputimgs/character_q.png', cap[posi_chara_q[0]:posi_chara_q[2],posi_chara_q[1]:posi_chara_q[3]])
    cv2.imwrite('outputimgs/character_e.png', cap[posi_chara_e[0]:posi_chara_e[2],posi_chara_e[1]:posi_chara_e[3]])
    