from interaction_background import InteractionBGD

itt = InteractionBGD()
from posi_manager import *

while 1:
    input("等待按键")
    cap = itt.capture()
    print('color: ')
    for i in range(4):
        cv2.imwrite('outputimgs/characterlist_' + str(i) + '.png',
                    cap[posi_chara_list[i][0]:posi_chara_list[i][2], posi_chara_list[i][1]:posi_chara_list[i][3]])
        cv2.imwrite('outputimgs/character_listq_' + str(i) + '.png',
                    cap[posi_charalist_q[i][0]:posi_charalist_q[i][2], posi_charalist_q[i][1]:posi_charalist_q[i][3]])
        print(cap[hp_charalist_posi[i][0], hp_charalist_posi[i][1]], end='   ')

    cv2.imwrite('outputimgs/character_q.png', cap[posi_chara_q[0]:posi_chara_q[2], posi_chara_q[1]:posi_chara_q[3]])
    cv2.imwrite('outputimgs/character_e.png', cap[posi_chara_e[0]:posi_chara_e[2], posi_chara_e[1]:posi_chara_e[3]])
