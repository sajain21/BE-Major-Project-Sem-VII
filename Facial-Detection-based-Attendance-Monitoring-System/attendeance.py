# hog algorithm use kr rahe hai isme 
import cv2 
import numpy as np
import face_recognition
import os # images ko read krne k liye
from datetime import datetime # date and time ko mark krne k liye

path = "images"
images = []
personName = []
myList = os.listdir(path)
print(myList)

# Retrieve names from image list
for cu_img in myList:
    current_Img = cv2.imread(f"{path}/{cu_img}")
    images.append(current_Img)
    personName.append(os.path.splitext(cu_img)[0])
print(personName)

# Encode images
def faceEncoding(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def attendance(name):
    with open("Attendance.csv", "r+") as f:
        myDataList = f.readline()
        nameList = []
        for line in myDataList:
            entry = line.split(",")
            nameList.append(entry[0])
        
        if name not in nameList:
            time_now = datetime.now() # capture current time and date 
            tStr = time_now.strftime("%H:%M:%S")
            dStr = time_now.strftime("%D/%m/%Y")
            f.writelines(f'{name}, {tStr}, {dStr} \n')
            return 0



encodeListKnow = faceEncoding(images)
print("All encoding complete")


# To access the camera
cap = cv2.VideoCapture(0)
while True:
    ret, frame  = cap.read()
    faces = cv2.resize(frame, (0,0), None, 0.25, 0.25)
    faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)

    facesCurrentFrame = face_recognition.face_locations(faces)
    encodesCurrentFrame = face_recognition.face_encodings(faces, facesCurrentFrame)

    for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
        matches = face_recognition.compare_faces(encodeListKnow, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnow, encodeFace)
        # print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = personName[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            attendance(name)
            break


    cv2.imshow("camera", frame)
    if cv2.waitKey(1) == 13:
        break
cap.release()
cv2.destroyAllWindows()
