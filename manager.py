import sys
import trace
import webbrowser
import kinect
import process_manager2
import time
from multiprocessing import Process
from multiprocessing import Queue
import process_manager
import threading


chrome_path = '/usr/bin/chromium-browser'

# manages the currently running processes.
# a lot of work needs to be done in here.
class Manager:
    def __init__(self):
        self.p_manager = process_manager2.PManager()
        self.p2_manager = process_manager.PManager()
        #self.start_recog([False, False, True])

    def getPManager(self):
        return self.p_manager

    def add( self, name, process, flags):
        self.p_manager.add(name, process, flags)
    
    def add2(self, name, process, flags):
        self.p2_manager.add(name, process, flags)

    def remove(self, name):
        self.p_manager.remove(name)

    def remove2(self, name):
        self.p2_manager.remove(name)

    def add_user(self, name):
        if self.p_manager.getProcess('camera') != None:
            self.remove('camera')
        time.sleep(10)
        print('user flag being changed')
        def helper(name):
            camera = kinect.async_open_camera2.camera([False, name])
            camera.open_camera()

        add_user_thread = Process(target = helper, args = (name,))
        add_user_thread.start()
        while True:
            if not add_user_thread.is_alive():
                break
        add_user_thread.terminate()
        add_user_thread.join()
    
    def start_recog(self, flags):
        def helper(flags):
            camera = kinect.async_open_camera3.camera(flags)
            camera.open_camera()
            while(True):
                time.sleep(1)
        self.add('camera', helper, flags)

    #def get_process(self, name):
        #return self.p_manager.get(name)

    def get_process2(self, name):
        return self.p2_manager.getProcess(name)

def open_chrome(manager, url):
    webbrowser.get(chrome_path).open(url)

def google_search(manager, text):
    query = 'https://www.google.com/search?q='
    for k in text:
        query += k + "+"
    open_chrome(query)

def youtube_search_first(manager, text):
    query = 'https://www.youtube.com/results?search_query='
    for k in text:
        query += k + "+"
    open_chrome(query)

def open_camera_reg(manager):
    def run_camera(flags):
        camera = kinect.async_open_camera2.camera(flags)
        camera.open_camera()
        while(True):
            print(flags[0])
            time.sleep(1)
            if flags[0] == True:
                break
        del camera
        #raise SystemExit()  
    manager.add2('camera', run_camera, [False, False, False])
    #run_camera([False, False, False])

def close_camera_reg(manager):
    #manager.remove2('camera')
    camera = manager.get_process2('camera')
    camera.flags[2] = False

def add_user(manager, name):
    camera = manager.get_process2('camera')
    camera.flags[1] = name

def start_recog(manager):
    #manager.start_recog([False, False, False, Queue()])
    open_camera_reg(manager)

def test_queue(manager):
    camera = manager.get_process2('camera')
    print(camera.flags)
    camera.flags[2] = True


def main():
    print('----manager main----')
    #google_search(['how','much','is','bitcoin'])
    #youtube_search_first(['under','your','spell'])

if __name__ == '__main__':
    main()

