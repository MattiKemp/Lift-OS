import voice_recog as voice
import text_processing as processing
import speech_synth as talk
import threading
import kinect
import time

def main():
    print('----Starting----')
    #print('listening')
    #print(voice.get_audio_reg())
    #print('listening ambient')
    #print(voice.get_audio_amb())
    
    #speech = voice.get_audio_reg()
    #print(speech)
    #print(processing.assistant_processing(speech))
    flags = [False, False, False]
    tp = processing.TextProcessor(flags)
    
    def Speech(textprocessor):
        time.sleep(20)
        while(1):
            print('listening')
            speech = voice.get_audio_reg()
            print(speech)
            response = textprocessor.assistant_processing(speech)
            print(response)
            #talk.say(speech)
    
    text_thread = threading.Thread(target = Speech, args = (tp,))
    text_thread.start()
    time.sleep(10)
    #open camera
    camera = kinect.async_open_camera2.camera(flags)
    camera.open_camera()

if __name__ == '__main__':
    main()

