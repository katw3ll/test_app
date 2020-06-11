import numpy as np
import cv2
from deepgaze.motion_detection import DiffMotionDetector
from deepgaze.mask_analysis import BinaryMaskAnalyser
from utils import MotionWriter

class VideoAnalyser:
    def __init__(self, path):
        #Open the video file and loading the background image
        self.video_capture = cv2.VideoCapture(path)
        ret, background_img = self.video_capture.read()
       
        #Сreate an error if the video failed to load
        if not ret: Exception("No file")

        #Getting info about video: fps, width and height
        self.fps = self.video_capture.get(cv2.CAP_PROP_FPS)
        self.width = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Define the codec
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')    

        #Decalring the motion detector object and setting the background
        self.my_motion_detector = DiffMotionDetector()
        self.my_motion_detector.setBackground(background_img)

        #Declaring the binary mask analyser object
        self.my_mask_analyser = BinaryMaskAnalyser()

        #Declaring the controlled MotionWriter helper
        self.motion_writer = MotionWriter(self.fourcc, self.fps, self.width, self.height)
    
    def analyze(self):
        print("Analysing...")
        self.motion_writer.start()

        while(True):
        # Capture frame-by-frame
            ret, frame = self.video_capture.read()
            if not ret: break

            frame_mask = self.my_motion_detector.returnMask(frame, threshold=10)

            if(self.my_mask_analyser.returnNumberOfContours(frame_mask) > 0):
                self.my_mask_analyser.drawMaxAreaRectangle(frame, frame_mask)
                self.motion_writer.detected_motion(frame)       
            else:
                self.motion_writer.undetected_motion()    

        self.motion_writer.end()

    def get_all_timestaps(self):
        return self.motion_writer.get_all_timestaps()
