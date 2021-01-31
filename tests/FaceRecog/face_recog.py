import face_recognition

pic_of_me = face_recognition.load_image_file("./Me/Matt.png")
my_face_encoding = face_recognition.face_encodings(pic_of_me)[0]

unknown_pic = face_recognition.load_image_file("./Unknown/unknown.png")
unknown_face_encoding = face_recognition.face_encodings(unknown_pic)[0]

print('encodings completed')

results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)


if results[0] == True:
    print("It's a picture of me!")

else:
    print("It's not a picture of me!")


