import nltk
import manager
import kinect

import speech_synth as talk
#import manager
# link to tutorial and examples used
# link: https://www.nltk.org/


# processes user speech that has been converted to text for voice commands. 
# A lot of work needs to be done in here.
class TextProcessor:
    def __init__(self, flags):
        self.mainManager = manager.Manager()
        self.flags = flags
 
    def assistant_processing(self,text):
        tokened = tokenize(text)
        lower_case(tokened)
        print(tokened)
        if tokened[0] != 'please':
            return -1
        
        else:
            if tokened[1] == 'google':
                manager.google_search(self.mainManager,tokened[2:])

            elif tokened[1] == 'youtube':
                manager.youtube_search_first(self.mainManager,tokened[2:])
            
            elif tokened[1] == 'open':
                if tokened[2] == 'camera':
                    print('camera open')
                    #manager.open_camera_reg(self.mainManager)
                    self.flags[2] = True
            
            elif tokened[1] == 'close':
                if tokened[2] == 'camera':
                    print('camera close')
                    #manager.close_camera_reg(self.mainManager)
                    self.flags[2] = False
            
            elif tokened[1] == 'add':
                if tokened[2] == 'user':
                    print('new user being added')
                    if(len(tokened) == 4):
                        #manager.add_user(self.mainManager, tokened[3])
                        self.flags[1] = tokened[3]
                    else:
                        print("what is the new users name? say: 'please add user NAME'")
            elif tokened[1] == 'start':
                manager.start_recog(self.mainManager)

            elif tokened[1] == 'test':
                manager.test_queue(self.mainManager)


def tokenize(text):
    return nltk.word_tokenize(text)

def lower_case(text):
    for i in range(len(text)):
        text[i] = text[i].lower()


def main():
    print('----text processing main----')
    sentence = """this is a test of text tokenizing"""
    tokens = nltk.word_tokenize(sentence)
    print(tokens)

if __name__ == '__main__':
    main()
