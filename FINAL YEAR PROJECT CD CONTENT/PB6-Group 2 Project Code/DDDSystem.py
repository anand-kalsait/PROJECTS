from sre_constants import SUCCESS
import cv2
import numpy as np
import dlib
from imutils import face_utils
import time
import alert
import multiprocessing
from pygame import mixer
import pyfirmata
import keyboard
from pyfirmata import Arduino
import pymsgbox
import RTSP

#board = Arduino('com7')
print('Arduino Connected Successfully!!')

        
rtsp_url = RTSP.x
cap = cv2.VideoCapture(0)
                                                                                                                            
'''if (rtsp_url == 0):
        cap = cv2.VideoCapture(0)
else:
        cap = cv2.VideoCapture(rtsp_url)
        #cap = cv2.VideoCapture("rtsp://192.168.137.69:8554/mjpeg/1")
        #cap = cv2.VideoCapture("rtsp://192.168.1.1/live/ch00_0")
'''

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

#variable for buzzer
buzzer = 12
pushbutton = 10
on = 1
off = 0


#variable for opencv
sleep = 0
drowsy = 0
active = 0
status0="SLEEPING !!!"
status=""
color=(0,0,0)


##def buzz():
##        kk=0
##        board = Arduino('com7')
##        print('Connected Successfully!!')
##        while True:
##                board.digital[buzzer].write(on)
####                kk = cv2.waitKey(1)
####                if (kk==32):
####                       board.digital[buzzer].write(off)
####                        break                
##                if (board.digital[pushbutton].read() == on):
##                        board.digital[buzzer].write(off)
##                        break
##        
##        status1="SLEEPING !!!"
##        return status1
##                
                


def timer1():
        start_time = time.time()
        seconds = 1
        sec=seconds
        
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            sec=sec-1

            if elapsed_time > seconds:
                    print('The device has recognized that the person is sleeping \n')
                    #board.digital[buzzer].write(on)
                    alert.emailalert()
                    pymsgbox.alert('The Notification Email with location has been Sent.\nPress OK to stop the Buzzer!!','Buzzer Alert')
                    #board.digital[buzzer].write(off)
                    
##                    status1 = buzz()
                    
                    
                                                
##                    mixer.init()
##                    mixer.music.load('alarm.mp3')
##                    mixer.music.play()
##                    time.sleep(5)
##                    mixer.music.stop()
                    break
        status1="SLEEPING !!!"
        return status1

def timer2():
        start_time = time.time()
        seconds = 1
        sec=seconds

        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            sec=sec-1

            if elapsed_time > seconds:
                    judgement()
                    break
        status1="Active !!!"
        return status1

def judgement1():
        sleep = 0
        active = 0
        con=0
        status0=7
        status=""
        status1=""
        color=(0,0,0)
        while True:
            success, frame = cap.read()
            #imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = detector(gray)
            
            for face in faces:
                x1 = face.left()
                y1 = face.top()
                x2 = face.right()
                y2 = face.bottom()

                face_frame = gray
                cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.imshow("Frame", frame)
                cv2.imshow("Result of detector", face_frame)
                landmarks = predictor(gray, face)
                landmarks = face_utils.shape_to_np(landmarks)

                left_blink = blinked(landmarks[36],landmarks[37], 
                        landmarks[38], landmarks[41], landmarks[40], landmarks[39])
                right_blink = blinked(landmarks[42],landmarks[43], 
                        landmarks[44], landmarks[47], landmarks[46], landmarks[45])
                
                if(left_blink==0 or right_blink==0):
                        sleep+=1
                        x="SLEEPING !!!"
                        
                        if(sleep>6):
                                        status1="SLEEPING !!!"
                                        color = (0,255,0)
                       
                        if status0==sleep:
                                kk=0
                                file = 'D:\Project final\Pictures'+str(kk)+'.jpg'
                                cv2.imwrite(file, frame)
                                status=timer1()
                                continue
                else:
                        active+=1
                        if(active>6):
                                        status="Active :)"
                                        color = (0,255,0)
                        if(status0==active):
                                status=timer2()
                                break
                cv2.putText(frame, status, (100,100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color,3)

                for n in range(0, 68):
                        (x,y) = landmarks[n]
                        cv2.circle(face_frame, (x, y), 1, (255, 255, 255), -1)
        
            key = cv2.waitKey(1)
            if key == 27:
                        break
        return status1

        




def countdown(t, l_b, r_b):
        status1=""
        status0="SLEEPING !!!"
        statu=""
        
        while t:
                mins, secs = divmod(t, 60)
                timer = '{:02d}:{:02d}'.format(mins, secs)
                print(timer, end="\r",)
                print("\n")
                time.sleep(1)
                t -= 1
                if(t==0):
                        statu=judgement1()
                        
        return statu                      
        

def compute(ptA,ptB):
                dist = np.linalg.norm(ptA - ptB)
                return dist

def blinked(a,b,c,d,e,f):
                up = compute(b,d) + compute(c,e)
                down = compute(a,f)
                ratio = up/(2.0*down)

                if(ratio>0.25):
                                return 2
                elif(ratio>0.21 and ratio<=0.25):
                                return 1
                else:
                                return 0

def judgement():
        sleep = 0
        drowsy = 0
        active = 0
        status=""
        status1=""
        statu=""
        lol = "Press & hold Esc key to exit"
        color1 = (255,255,255)
        color=(0,0,0)
        while True:
            SUCCESS, frame = cap.read()
            #imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = detector(gray)

            for face in faces:
                x1 = face.left()
                y1 = face.top()
                x2 = face.right()
                y2 = face.bottom()

                face_frame = gray
                cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                landmarks = predictor(gray, face)
                landmarks = face_utils.shape_to_np(landmarks)

                left_blink = blinked(landmarks[36],landmarks[37], 
                        landmarks[38], landmarks[41], landmarks[40], landmarks[39])
                right_blink = blinked(landmarks[42],landmarks[43], 
                        landmarks[44], landmarks[47], landmarks[46], landmarks[45])
                
                if(left_blink==0 or right_blink==0):
                        sleep+=1
                        drowsy=0
                        active=0
                        x="SLEEPING !!!"
                        if(sleep>3):
                                        status="SLEEPING !!!"
                                        color = (255,0,0)
                        if(x==status):
                                count1=countdown(1, left_blink,right_blink)
                                continue
                       
                
                elif(left_blink==1 or right_blink==1):
                        sleep=0
                        active=0
                        drowsy+=1
                        x="Drowsy !"
                        if(drowsy>6):
                                        status="Drowsy !"
                                        color = (0,0,255)

                else:
                        drowsy=0
                        sleep=0
                        active+=1
                        if(active>6):
                                        status="Active :)"
                                        color = (0,255,0)
                
                cv2.putText(frame, status, (100,100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color,3)
                cv2.putText(face_frame, lol, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, color1,2)

                for n in range(0, 68):
                        (x,y) = landmarks[n]
                        cv2.circle(face_frame, (x, y), 1, (255, 255, 255), -1)

            cv2.imshow("Frame", frame)
            cv2.imshow("Result of detector", face_frame)
            key= cv2.waitKey(1)
            if key == 27:
                break



judgement()



#---------------------------------------------------------------------------------------------------------------------------------------------------------------------#
