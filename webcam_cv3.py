import cv2
import sys
from time import sleep
import boto3
import util

rekog = boto3.client('rekognition')
s3 = boto3.client('s3')

curr_frame = 0
frame_skip = 10

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    # Capture frame-by-frame
    ret, frame = video_capture.read()
    curr_frame += 1

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:

        roi = gray[y:y+h, x:x+w]
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)    
        
        if curr_frame % frame_skip == 0:
            bin_img = util.convertCvFrame2Bytes(gray)

            rfaces = rekog.detect_faces(Image={'Bytes': bin_img})
            for fd in rfaces['FaceDetails']:
                for lm in fd['Landmarks']:
                    y = int(frame.shape[0] * lm['Y'])
                    x = int(frame.shape[1] * lm['X'])
                    cv2.circle(frame, (x, y), 1, (0, 255, 0))
                    
            stream_img_roi = util.convertCvFrame2Stream(roi)
            s3.upload_fileobj(stream_img_roi,"prueba-face-rekog", str(curr_frame) + ".jpg")        

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
