from unit import *
import threading
import video_loop


class Pickup_Loop(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__()
        self.posi=[1,2,3,4]
        video_loop.video_cap.registered_events(self.trigger,'pickuploop')
        self.pick_flag=False
        
        
    # def trigger(self,cap):
    #     if video_loop.video_cap.itt.similar_img('pickup.jpg',cap[self.posi[0]:self.posi[2],self.posi[1]:self.posi[3]])>=0.8:
    #         return True
        
    def operate(self):
        self.pick_flag=True
        
    def stop(self):
        video_loop.video_cap.logout('pickuploop')
        
    def run(self):
        pass