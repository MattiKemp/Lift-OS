#!/usr/bin/env python
import freenect
import cv2
#from . import frame_convert2
import frame_convert2
#import frame_convert2
import recognizer
#cv2.namedWindow('RGB')
#keep_running = [False]

class Camera:
    def __init__(self, keep_run = [False]):
        self.keep_running = keep_run
        self.faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.recognizer = recognizer.Recognizer()
    
    def display_camera_full(self,dev,data,timestamp):
        data = cv2.resize(data, (1900, 1050))
        
        faces = self.facial_recog(data)
        for (x, y, w, h) in faces:
            cv2.rectangle(data, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        rgb = data[:, :, ::-1]
        self.recognizer.recognize(rgb)

        cv2.imshow('RGB', frame_convert2.video_cv(data))
        if cv2.waitKey(1) == 27:
            self.keep_running = [False]

    def display_camera_half(self,dev,data,timestamp):

        faces = self.facial_recog(data)
        for (x, y, w, h) in faces:
            cv2.rectangle(data, (x, y), (x+w, y+h), (0, 255, 0), 2)

        data = cv2.resize(data, (1280,720))
        cv2.imshow('RGB', frame_convert2.video_cv(data))
        if cv2.waitKey(1) == 27:
            self.keep_running = [False]

    def display_camera_fourth(self,dev,data,timestamp):
        faces = self.facial_recog(data)
        for (x, y, w, h) in faces:
            cv2.rectangle(data, (x, y), (x+w, y+h), (0, 255, 0), 2)
        print('faces')
        #print(faces)
        rgb = data[:, :, ::-1]
        locations = [[y,x+w,y+h,x] for (x,y,w,h) in faces]
        print(locations)
        if len(locations) > 0:
            print(self.recognizer.recognize_face_loc(rgb,locations))
        
        cv2.imshow('RGB', frame_convert2.video_cv(data))
        if cv2.waitKey(1) == 27:
            self.keep_running = [False]

    def display_camera_reg(self,dev,data,timestamp):
        cv2.imshow('RGB', frame_convert2.video_cv(data))
        if cv2.waitKey(1) == 27:
            self.keep_running = [False]

    def body(self,*args):
        if self.keep_running[0]:
            cv2.destroyWindow('RGB')
            self.keep_running = [False]
            raise freenect.Kill

    def facial_recog(self, data):    
        gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30,30)
        )
        print("Found {0} faces!".format(len(faces)))
        return faces

    def open_camera(self):
        cv2.startWindowThread()
        cv2.namedWindow('RGB')
        cv2.moveWindow('RGB', 20, 20)
        cv2.startWindowThread()
        print('starting freenect')
        freenect.runloop(video=self.display_camera_fourth,body=self.body)

def main():
    #open_camera()
    print('----facial recog kinect test main----')
    camera = Camera()
    camera.open_camera()

if __name__ == '__main__':
    main()
