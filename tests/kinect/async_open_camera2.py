#!/usr/bin/env python
import freenect
import cv2
#from . import frame_convert2
import frame_convert2

#cv2.namedWindow('RGB')
#keep_running = [False]

class camera:
    def __init__(self, keep_run = [False]):
        self.keep_running = keep_run
    
    
    def display_camera_full(self,dev,data,timestamp):
        data = cv2.resize(data, (1900, 1050))
        cv2.imshow('RGB', frame_convert2.video_cv(data))
        if cv2.waitKey(1) == 27:
            self.keep_running = [False]

    def display_camera_half(self,dev,data,timestamp):
        data = cv2.resize(data, (1280,720))
        cv2.imshow('RGB', frame_convert2.video_cv(data))
        if cv2.waitKey(1) == 27:
            self.keep_running = [False]

    def display_camera_fourth(self,dev,data,timestamp):
        cv2.imshow('RGB', frame_convert2.video_cv(data))
        if cv2.waitKey(1) == 27:
            self.keep_running = [False]
    
    def body(self,*args):
        if self.keep_running[0]:
            cv2.destroyWindow('RGB')
            self.keep_running = [False]
            raise freenect.Kill


    def open_camera(self):
        cv2.startWindowThread()
        cv2.namedWindow('RGB')
        cv2.moveWindow('RGB', 20, 20)
        cv2.startWindowThread()
        print('starting freenect')
        freenect.runloop(video=self.display_camera_full,body=self.body)

def main():
    open_camera()
    print('wwwwwhhhhyhhyyyy')

#if __name__ == '__main__':
    #main()
