#Source for test code: https://realpython.com/python-speech-recognition/#installing-speechrecognition
import speech_recognition as sr
r = sr.Recognizer()
mic = sr.Microphone()

def get_audio_reg():
    with mic as source:
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except:
        return 'error&!'

def get_audio_amb():
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except:
        return 'error&!'


