from unit import *
from interaction_background import Interaction_BGD
import small_map, movement, cv2, time, threading, pdocr_api, text_manager as textM, posi_manager as PosiM, timer_module, img_manager
# sys.path.append("..")

import source.yolox_api
class Get_Reward(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.itt = Interaction_BGD()
        self.lockOnFlag=0
        self.pause_thread_flag=False
        self.working_flag=False
        self.stopFlag=False
        self.movenum=2.5
        reflash_config()
        
        self.isLiYue=configjson["isLiYueDomain"]
        self.resin_mode=configjson["resin"]
        self.move_timer=timer_module.Timer()
        self.ahead_timer=timer_module.Timer()
        
    def get_tree_posi(self):
        cap = self.itt.capture(shape='xy')
        cap = self.itt.png2jpg(cap)
        # cv2.imshow('123',cap)
        # cv2.waitKey(0)
        addition_info,ret2 = source.yolox_api.yolo_tree.predicte(cap)
        logger.debug(addition_info)
        if addition_info!=None:
            if addition_info[0][1][0]>=0.5:
                treex, treey=source.yolox_api.yolo_tree.get_center(addition_info)
                return (treex,treey)
        return False
    
    def get_tree_size(self):
        cap = self.itt.capture(shape='xy')
        cap = self.itt.png2jpg(cap)
        addition_info,ret2 = source.yolox_api.yolo_tree.predicte(cap)
        if addition_info!=None:
            if addition_info[0][1][0]>=0.5:
                posi=source.yolox_api.yolo_tree.get_maxap_pic_bbox(addition_info)
                return posi[2]-posi[0]
        return -1
            
    def align_to_tree(self):
        movement.view_to_angle(-90)
        tposi=self.get_tree_posi()
        if tposi != False:
            tx, ty=self.itt.get_mouse_point()
            dx=int(tposi[0]-tx)
            # movenum=2.5
            logger.debug(dx)
            
            if dx>=0:
                movement.move(movement.RIGHT,self.movenum)
                # self.itt.keyPress('w')
            else:
                movement.move(movement.LEFT,self.movenum)
                # self.itt.keyPress('w')
            if abs(dx)<=20:
                self.lockOnFlag+=1
                self.movenum=1
            return True
        else:
            self.movenum=4
            return False                
    
    def find_tree(self):
        movement.view_to_angle(90)
        tposi=self.get_tree_posi()
        if tposi != False:
            tx, ty=self.itt.get_mouse_point()
            dx=int(tposi[0]-tx)
            
            if dx>=0:
                movement.move(movement.RIGHT,4)
                #self.itt.keyPress('w')
            else:
                movement.move(movement.LEFT,4)
                # self.itt.keyPress('w')
            if dx<=8:
                logger.debug(dx)
                return 0
            else:
                return 1
        else:
            movement.cview(-30)
            
    def close_to_tree(self):
        while(1):
            a = self.find_tree()
            if a==0:
                self.itt.keyDown('w')
                if self.get_tree_size()>=320:
                    self.itt.keyUp('w')
                    return 0
            time.sleep(0.2)
    
    def approve_tree(self):
        for i in range(40):
            self.itt.keyDown('w')
            tposi=self.get_tree_posi()
            if tposi != False:
                tx, ty=self.itt.get_mouse_point()
                dx=int((tposi[0]-tx)/2)
                movement.cview(dx)
            self.itt.keyDown('w')
            time.sleep(0.2)
        self.itt.keyUp('w')
            
    def do_loop(self):
        self.close_to_tree()
        self.approve_tree()
    
    def continue_thread(self):
        self.pause_thread_flag=False
        self.lockOnFlag=0
        movement.reset_view()
        time.sleep(1)
    
    def pause_thread(self):
        self.pause_thread_flag=True
        
    def reset_flag(self):
        self.working_flag=True
    
    def get_statement(self):
        return self.working_flag
    
    def stop_thread(self):
        self.stopFlag=True
    
    def run(self):
        direc=True
        while(1):
            if self.stopFlag:
                break
            if self.pause_thread_flag:
                self.working_flag=False
                time.sleep(1)
                continue
            if self.lockOnFlag<=5:
                is_tree=self.align_to_tree()
                self.ahead_timer.reset()
                if is_tree==False:
                    movement.view_to_angle(-90)
                    
                    if self.isLiYue: # barrier treatment
                        if self.move_timer.getDiffTime()>=20:
                            direc=not direc
                            self.move_timer.reset()    
                        if direc:
                            movement.move(movement.LEFT,distance=4)
                        else:
                            movement.move(movement.RIGHT,distance=4)
                    
                    else: # maybe can't look at tree
                        logger.debug('can not find tree. moving back.')
                        movement.move(movement.BACK,distance=2)
            else:
                # do jump every five seconds
                if self.ahead_timer.getDiffTime()>=5:
                    self.itt.keyPress('spacebar')
                    self.ahead_timer.reset()
                
                movement.view_to_angle(-90)
                self.itt.keyDown('w')
                time.sleep(0.2)
                
                cap=self.itt.capture(posi=PosiM.posi_domain["ClaimRewards"]) # posi=PosiM.posi_domain["ClaimRewards"]
                cap=self.itt.png2jpg(cap,channel='ui')
                if pdocr_api.ocr.getTextPosition(cap, textM.text(textM.claim_rewards)) != -1:
                    self.itt.keyUp('w')
                    
                    self.itt.keyPress('f')
                    time.sleep(2)
                    
                    while(1):
                        if self.resin_mode=='40':
                            self.itt.appear_then_click(imgname=img_manager.USE_20X2RESIN_DOBLE_CHOICES)
                        elif self.resin_mode=='20':
                            self.itt.appear_then_click(imgname=img_manager.USE_20RESIN_DOBLE_CHOICES)
                        
                        if pdocr_api.ocr.getTextPosition(self.itt.capture(jpgmode=3), textM.text(textM.domain_obtain)) != -1:
                            break
                        time.sleep(2)
                        
                    self.working_flag=False
                    self.pause_thread()
                    time.sleep(2)
                    
                
                
        
if __name__=='__main__':
    gr=Get_Reward()
    gr.start()
    while(1):
        time.sleep(1)
                