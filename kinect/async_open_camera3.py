#!/usr/bin/env python
import freenect
import cv2
from . import frame_convert2
from multiprocessing import Process
import sys
sys.path.append("..")
import recognizer
import pyttsx3
#import frame_convert2
import time

class camera:
    def __init__(self, flags):
        self.flags = flags
        self.to_scan = 0
        self.face_thread = None
        self.recognizer = recognizer.Recognizer()
        time.sleep(10)
       
    def display_camera_fourth(self, dev, data, timestamp):
        if self.to_scan == 120:
            print('flags:' + str(self.flags))
            if(len(self.flags) > 0):
                print(self.flags[3].get())
            if self.flags[1] != False:
                rgb = data[:, :, ::-1]
                self.add_new_user(rgb, self.recognizer)
                #add thread deletion here
            else:
                if self.face_thread != None and self.face_thread.is_alive():
                    self.face_thread.terminate()
                rgb = data[:, :, ::-1]
                self.face_thread = Process(target = self.face_detect, args=(rgb, self.recognizer))
                self.face_thread.start()
        if self.flags[2] == True:
            cv2.imshow('RGB', frame_convert2.video_cv(data))
        cv2.waitKey(1)
        self.to_scan += 1

    def face_detect(self, image, recognizer):
        results = recognizer.recognize(image)
        print('face detected:' + str(results))
        if results and 'obama' in results:
            print('obama detected')
            #add obama sound

    def add_new_user(self, image, recognizer):
        if recognizer.detect_and_add(self.flags[1], image) == True:
            self.flags[1] = False
            self.flags[0] = True


    def body(self, *args):
        if self.flags[0]:
            cv2.destroyWindow('RGB')
            self.flags = False
            raise freenect.Kill

    def open_camera(self):
        cv2.startWindowThread()
        cv2.namedWindow('RGB')
        cv2.moveWindow('RGB', 30, 30)
        cv2.startWindowThread()
        cv2.waitKey(1)
        print('starting freenect')
        freenect.runloop(video = self.display_camera_fourth, body = self.body)


def cv2_test():
    vid = cv2.VideoCapture(0)
    frame = vid.read()
    frame = frame[:, :, ::-1]
    cv2.imshow('frame', frame)

def main():
    print('----camera 3 main----')

if __name__ == '__main__':
    main()
