import pyttsx3


def say(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 200)
    engine.say(text)
    engine.runAndWait()



def test():
    engine = pyttsx3.init()
    engine.say("The bridges burst and twist around")
    engine.runAndWait()

def main():
    print('----speech synth main----')
    test()


if __name__ == '__main__':
    main()

