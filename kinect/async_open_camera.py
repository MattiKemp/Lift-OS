#!/usr/bin/env python
import freenect
import cv2
from . import frame_convert2
#import frame_convert2

#cv2.namedWindow('RGB')
keep_running = [False]

def display_camera(dev,data,timestamp):
    global keep_running
    cv2.imshow('RGB', frame_convert2.video_cv(data))
    if cv2.waitKey(10) == 27:
        keep_running = [False]

def body(*args):
    global keep_running
    if keep_running[0]:
        cv2.destroyWindow('RGB')
        keep_running = [False]
        raise freenect.Kill


def open_camera(keep_run): 
    cv2.namedWindow('RGB')
    global keep_running
    keep_running = keep_run
    print('starting freenect')
    freenect.runloop(video=display_camera,body=body)

def main():
    #open_camera()
    print('wwwwwhhhhyhhyyyy')

#if __name__ == '__main__':
    #main()
