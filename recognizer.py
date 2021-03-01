import face_recognition
import pickle
import numpy as np

import sys,os
sys.path.append(os.path.realpath('./'))
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '~/Projects/Lift-OS/')

# used for recognizing, encoding, and saving faces
# there is a minor bug in here (you should fix it next time you work on this lol).
class Recognizer:
    # loads the saved face encodings
    def __init__(self):
        with open('dataset_faces.dat', 'rb') as f:
            self.all_face_encodings = pickle.load(f)
        self.face_encodings = np.array(list(self.all_face_encodings.values()))
        self.face_names = list(self.all_face_encodings.keys())
        print('loaded:' + str(len(self.face_names)) + 'user faces:')
        for k in self.face_names:
            print(str(k))
    
    # detects a face in an image, encodes the face, and adds it to the saved dataset of faces. (deprecated)
    def detect_and_add(self, name, image):
        face_location = face_recognition.face_locations(image)
        if(len(face_location) > 0):
            print('face detected and being added')
            self.all_face_encodings[name] = face_recognition.face_encodings(image, face_location)[0]
            self.update()
            return True
        return False
    
    # takes a location of a face in an image, encodes the face, and saves it to the dataset of faces.
    def detect_and_add(self, name, image, location):
        print('face detected and being added')
        print(location)
        unknown_face_encoding = face_recognition.face_encodings(image, location)
        if(len(unknown_face_encoding) > 0):
            self.all_face_encodings[name] = unknown_face_encoding[0]
            self.update()
            return True
        return False

    # updates the face encoding dataset file.
    def update(self):
        with open('~/Projects/Lift-OS/dataset_faces.dat', 'wb') as f:
            pickle.dump(self.all_face_encodings, f)
        self.face_encodings = np.array(list(self.all_face_encodings.values()))

    # general function to detect and recognize faces in an image. (deprecated)
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
    
    # takes an image and the location of the faces in the image and compares them to the saved face encodings.
    def recognize_face_loc(self, image, locations):
        unknown_face_encodings = face_recognition.face_encodings(image, locations)
        result = face_recognition.compare_faces(self.face_encodings, unknown_face_encodings)
        names_with_result = list(zip(self.face_names, result))
        faces = [ k[0] for k in names_with_result if k[1] == True]
        if len(faces) > 0:
            return faces
        return False
    
# tool to delete a face from the saved face encodings.
def delete_face(name): 
    faces = None
    with open('~/Projects/Lift-OS/dataset_faces.dat', 'rb') as f:
        faces = pickle.load(f)
    faceIndex = -1
    for k in faces.keys():
        if k == name:
            break
        faceIndex += 1
    if faceIndex != len(faces.keys())-2: 
        print('deleting face')
        faces = np.delete(faces, faceIndex)
        with open('~/Projects/Lift-OS/dataset_faces.dat', 'wb') as f:
            pickle.dump(faces, f)

# tool to list all the names associated with each of the saved face encodings
def list_faces(): 
    faces = None
    with open('~/Projects/Lift-OS/dataset_faces.dat', 'rb') as f:
        faces = pickle.load(f)
    face_names = list(faces.keys())
    print('loaded:' + str(len(face_names)) + 'user faces:')
    for k in face_names:
        print(str(k))

def main():
    print('---face recognizer main---')
    print('---initializing obama---')
    #recognizer = Recognizer()
    #obama = face_recognition.load_image_file("./test/obama.jpeg")
    #obama_location = face_recognition.face_locations(obama)
    #obama_encoding = face_recognition.face_encodings(obama, obama_location)
    #recognizer.detect_and_add('obama', obama)
    #recognizer.update()
    #list_faces()

if __name__ == '__main__':
    main()
