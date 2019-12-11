
import os
import face_recognition


def recognizeface():
    
  images = os.listdir('SavedImages')
  source = os.listdir('images')
  for image in source:
      image_to_be_matched = face_recognition.load_image_file("images/"+image)


  image_to_be_matched_encoded = face_recognition.face_encodings(
      image_to_be_matched)[0]


  for image in images:

      current_image = face_recognition.load_image_file("SavedImages/" + image)

      current_image_encoded = face_recognition.face_encodings(current_image)[0]

      result = face_recognition.compare_faces(
          [image_to_be_matched_encoded], current_image_encoded)

      return result[0]
