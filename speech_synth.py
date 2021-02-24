import pyttsx3



def say(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 200)
    engine.say(text)
    engine.runAndWait()



def test():
    engine = pyttsx3.init()
    engine.say("Fuck my tight assssss daddy")
    engine.runAndWait()

def main():
    print('----speech synth main----')
    test()


if __name__ == '__main__':
    main()

