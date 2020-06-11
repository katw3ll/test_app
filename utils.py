import cv2
import os
from datetime import datetime

class MotionWriter:

    def __init__(self, fourcc, fps, width, height):
        self.out = cv2.VideoWriter("./temp.mp4", fourcc, fps, (width, height))
        self.is_motion_detected = False
        self.timestamp = None
        self.start_timestamp = None 
        self.all_timestaps = [] 
          
    def start(self):
        self.start_timestamp = datetime.now()
    
    def get_new_timestamp(self):
        return datetime.now() - self.start_timestamp
        
    def get_timestamp(self):
        return self.timestamp
    
    def get_name_timestamp(self):
        delta_start = self.get_timestamp()
        delta_end = self.get_new_timestamp()
        print(delta_start, delta_end)
        self.all_timestaps.append(dict(start=delta_start.seconds, end=delta_end.seconds))
        return "{}_{}.mp4".format(delta_start.seconds, delta_end.seconds)

    def detected_motion(self, frame):
        if not self.is_motion_detected:
            self.is_motion_detected = True
            self.timestamp = self.get_new_timestamp()
        self.out.write(frame)
    
    def undetected_motion(self):
        if self.is_motion_detected:
            self.is_motion_detected = False
            self.out.release()
            old_file = os.path.join("./", "temp.mp4")
            new_file = os.path.join("./video/", self.get_name_timestamp())
            os.rename(old_file, new_file)

    def end(self):
        self.undetected_motion()

    def get_all_timestaps(self):
        return self.all_timestaps
            
