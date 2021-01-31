import face_recognition
import pickle
import numpy as np

class Recognizer:
    def __init__(self):
        with open('dataset_faces.dat', 'rb') as f:
            self.all_face_encodings = pickle.load(f)
        self.face_encodings = np.array(list(self.all_face_encodings.values()))
        self.face_names = list(self.all_face_encodings.keys())
        #print('temp')
        #self.all_face_encodings = {}
    
    def add(self, name, image, location):
        self.all_face_encodings[name] = face_recognition.face_encodings(image, location)[0]
        self.update()

    def update(self):
        with open('dataset_faces.dat', 'wb') as f:
            pickle.dump(self.all_face_encodings, f)
        self.face_encodings = np.array(list(self.all_face_encodings.values()))

    def recognize(self, image):
        unknown_face_locations = face_recognition.face_locations(image)
        if len(unknown_face_locations) > 0:
            print('found face')
            #unknown_face_locations = unknown_face_locations[0]
            unknown_face_encodings = face_recognition.face_encodings(image)
            print('face encodings generated')
            result = face_recognition.compare_faces(self.face_encodings, unknown_face_encodings)
            names_with_result = list(zip(self.face_names, result))
            faces = [ k[0] for k in names_with_result if k[1] == True]
            if len(faces) > 0:
                return faces
            return False 
        return None

def main():
    print('---face recognizer main---')
    print('---initializing obama---')
    recognizer = Recognizer()
    #obama = face_recognition.load_image_file("./test/obama.jpeg")
    #obama_location = face_recognition.face_locations(obama)
    #obama_encoding = face_recognition.face_encodings(obama, obama_location)
    #recognizer.add('obama', obama, obama_location)
    #recognizer.update()

if __name__ == '__main__':
    main()
