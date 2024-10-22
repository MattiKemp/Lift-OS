#!/usr/bin/env python
#clean this up
import freenect
import cv2
from . import frame_convert2
from multiprocessing import Process
import sys
sys.path.append("..")
import recognizer
import pyttsx3
import time
import database
#import frame_convert2
import threading

class camera:
    def __init__(self, flags):
        # flags[0] = quit
        # flags[1] = add user
        # flags[2] = camera on or off
        self.flags = flags
        self.to_scan = 0
        self.db_update = 0
        self.face_thread = None
        self.db_thread = None
        self.db = database.Database('python', 'Hinoob22')
        self.recognizer = recognizer.Recognizer()
        self.faces = set()
        self.faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    
    #used for testing
    def display_camera_full(self,dev,data,timestamp):
        data = cv2.resize(data, (1900, 1050))
        cv2.imshow('RGB', frame_convert2.video_cv(data))
        if cv2.waitKey(1) == 27:
            self.flags[0] = False
    
    #used for testing
    def display_camera_half(self,dev,data,timestamp):
        data = cv2.resize(data, (1280,720))
        cv2.imshow('RGB', frame_convert2.video_cv(data))
        if cv2.waitKey(1) == 27:
            self.flags[0] = False
    
    #used for testing
    def display_camera_fourth(self,dev,data,timestamp):
        if self.to_scan == 120:
            print('flags[1]:' + str(self.flags[1]))
            if self.flags[1] != False:
                print('adding new user')
                rgb = data[:, :, ::-1]
                self.add_new_user(rgb, self.recognizer)
            else:
                if self.face_thread != None and self.face_thread.is_alive():
                    self.face_thread.terminate()
                rgb = data[:, :, ::-1]
                self.face_thread = Process(target = self.face_detect, args = (rgb, self.recognizer))
                self.face_thread.start()
            self.to_scan = 0
        cv2.imshow('RGB', frame_convert2.video_cv(data))
        if cv2.waitKey(1) == 27:
            self.flags[0] = False
        self.to_scan += 1
   
    #main function
    def display_camera_test(self, dev, data, timestamp):
        if self.to_scan==60:
            print('flags' + str(self.flags))
            if self.flags[1] != False:
                rgb = data[:, :, ::-1]
                self.add_new_user(data, rgb, self.recognizer)
            else: 
                if self.face_thread != None and self.face_thread.is_alive():
                    while True:
                        if not self.face_thread.is_alive():
                            break
                rgb = data[:, :, ::-1]
                self.face_thread = threading.Thread(target = self.face_detect, args = (data, rgb, self.recognizer, self.faces))
                self.face_thread.start()
            self.to_scan = 0
        if self.db_update == 480:
            print(self.faces)
            if self.db_thread != None and self.db_thread.is_alive():
                self.db_thread.terminate()
            if self.face_thread != None and self.face_thread.is_alive():
                while True:
                    if not self.face_thread.is_alive():
                        break
            self.db_thread = Process(target = self.update_db, args = (self.faces,))
            self.db_thread.start()
            self.db_update = 0
            self.faces = set()
        if self.flags[2] == True:
            data = cv2.flip(data, 1)
            data = cv2.resize(data, (1900, 1050))
            cv2.imshow('RGB', frame_convert2.video_cv(data))
        else:
            data = cv2.resize(data, (1,1))
            cv2.imshow('RGB', frame_convert2.video_cv(data))
        if cv2.waitKey(10) == 27:
            self.flags[0] = False
        self.to_scan += 1
        self.db_update += 1

    # freenect body
    def body(self,*args):
        if self.flags[0]:
            cv2.destroyWindow('RGB')
            self.flags = False
            raise freenect.Kill

    # properly initializes cv2 and runs freenect
    def open_camera(self):
        cv2.startWindowThread()
        cv2.namedWindow('RGB')
        cv2.moveWindow('RGB', 0, 0)
        cv2.startWindowThread()
        print('starting freenect')
        freenect.runloop(video=self.display_camera_test,body=self.body)

    # takes a bgr image from the kinect and uses the recognizer to detect and recognize faces. 
    def face_detect(self, bgr, image, recognizer, faces):
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        face_locs = self.faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30,30)
        )
        locations = [[y, x+w, y+h, x] for (x,y,w,h) in face_locs]
        results = None
        if len(locations) > 0:
            try:
                results = recognizer.recognize_face_loc(image, locations)
            except:
                print('exception occured in face_detect for camera')
        print(results)
        if results and 'obama' in results:
            print('obama detected')
            #playsound('./obama.mp3')
            #self.engine.say('A P T obama obama obama obama obama obama obama')
            #self.engine.runAndWait()
        if results:
            for k in results:
                faces.add(k)

   # detects and adds a new user face encoding to our dataset of faces 
    def add_new_user(self, bgr, image, recognizer):
        
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        face_locs = self.faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30,30)
        )
        locations = [[y, x+w, y+h, x] for (x,y,w,h) in face_locs]
        if len(locations) > 0:
            if(recognizer.detect_and_add(self.flags[1], image, locations)==True):
                print('user found changing add user flag to false')
                print('user: ' + str(self.flags[1]))
                self.flags[1] = False
                #self.flags[0] = True

    # updates the user workout data db 
    def update_db(self, names):
        print('updating db')
        if len(names) > 0:
            db = database.Database('python', 'Hinoob22')
            for k in names:
                print('adding: ' + k)
                db.add_time_now(k)
            db.close()

def main():
    #open_camera()
    print('wwwwwhhhhyhhyyyy')

#if __name__ == '__main__':
    #main()
