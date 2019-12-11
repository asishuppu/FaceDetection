import cv2
from flask import Flask, render_template, Response,request
from camera import VideoCamera
import time
import datetime
import os
import shutil
import os
import face_recognition
app = Flask(__name__, static_url_path = "/images/", static_folder = "images")
@app.route('/')
def index():
    return render_template('index.html')
def capture():
    return render_template('capture.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
def recognizeface(imgname):
    
  images = os.listdir('SavedImages')
  image_to_be_matched = face_recognition.load_image_file("images/"+imgname)


  image_to_be_matched_encoded = face_recognition.face_encodings(
      image_to_be_matched)[0]

  recresult="Not Detected"
  for image in images:

      current_image = face_recognition.load_image_file("SavedImages/" + image)

      current_image_encoded = face_recognition.face_encodings(current_image)[0]

      result = face_recognition.compare_faces(
          [image_to_be_matched_encoded], current_image_encoded)
      if result[0] == True:
        recresult="Matched with " + image 
  return recresult
def vcapture(camera,imgname):
    frame = camera.get_image()
    if os.path.exists("images"):
        shutil.rmtree("images")
    os.mkdir("images")
    file = "images/"+imgname
    cv2.imwrite(file, frame)
    camera.delete()
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture',methods=['GET', 'POST'])
def capture():
    t=time.localtime()
    d= datetime.date.today()
    ctime=time.strftime("%H_%M_%S",t)
    iname=str(d)+"-"+str(ctime)+".jpg"
    vcapture(VideoCamera(),iname)
    return render_template('capture.html',imgname=iname)
@app.route('/recognize/<imgname>',methods=['GET', 'POST'])
def recognize(imgname):
    recognized ="No face found"
    try:
        recognized=recognizeface(imgname)
        if recognized != "Not Detected":
            return render_template('recognize.html',recresult=recognized)  
            
        else:
            return render_template('saveimage.html',imgn=imgname)      
    except:
        recognized ="Image source has no face" 
        return render_template('recognize.html',recresult=recognized)

    return render_template('saveimage.html',imgn=imgname)
@app.route('/saveimage/<imgname>',methods=['GET', 'POST'])
def saveimage(imgname):
    srcfile="images\\"+imgname
    ename = request.form['ename']
    enamefull = ename.upper()
    destfile="images\\"+enamefull+".jpg"
    os.rename(srcfile,destfile) 
    shutil.move(destfile, "SavedImages\\")   
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
