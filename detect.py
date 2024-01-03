import mediapipe as mp 
import cv2 as cv
import autopy
import numpy as np


class Virtual_Pointer:
    def __init__(self):
        self.mp_drawing=mp.solutions.drawing_utils
        self.mp_drawing_styles=mp.solutions.drawing_styles
        self.mp_hands=mp.solutions.hands
        self.hands=self.mp_hands.Hands()
        self.cap=cv.VideoCapture(0)
        self.plocX=0
        self.plocY=0
        self.clocX=0
        self.clocY=0    
        self.wscr,self.hscr=autopy.screen.size()
        self.wCam,self.hCam=640,480
        self.smoothing=5



    def run(self):

        
        while True:
            ret,frame=self.cap.read()
            if not ret:
                break

            frame=cv.flip(frame,1)
            results=self.hands.process(frame)
            if results.multi_hand_landmarks:
                count={'1':0,'2':0}
                for landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(frame,landmarks,self.mp_hands.HAND_CONNECTIONS)

                index_x,index_y=landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].x*frame.shape[1],landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y*frame.shape[0]

                middle_x,middle_y=y=landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x*frame.shape[1],landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y*frame.shape[0]

                if index_y<landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP].y*frame.shape[0]:
                    count['1']=1
                   

                if  middle_y<landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y*frame.shape[0]:
                    count['2']=1
                    

                
                if count['1']==1 and count['2']==0:
                    cv.circle(frame,(int(index_x),int(index_y)),12,(0,255,0),-1)
                    x=np.interp(index_x,(100,self.wCam-100),(0,self.wscr))
                    y=np.interp(index_y,(100,self.hCam-100),(0,self.hscr))
                    self.clocX=self.plocX+(x-self.plocX)/self.smoothing
                    self.clocY=self.plocY+(y-self.plocY)/self.smoothing
                    try:
                        autopy.mouse.move(self.clocX, self.clocY)
                        self.plocX, self.plocY = self.clocX, self.clocY
                    except ValueError:
                        self.plocX, self.plocY = self.clocX, self.clocY
                        continue  
                    autopy.mouse.move(self.clocX,self.clocY)


                else:
                    p1=np.array((index_x,index_y))
                    p2=np.array((middle_x,middle_y))
                    dist=np.linalg.norm(p1-p2)
                    if int(dist)<50:

                        cv.line(frame,(int(index_x),int(index_y)),(int(middle_x),int(middle_y)),(255,255,255),2,cv.LINE_AA)
                        mid_x=int(index_x+middle_x)//2
                        mid_y=int(index_y+middle_y)//2
                        cv.circle(frame,(mid_x,mid_y),12,(0,255,0),-1)
                        autopy.mouse.click()

            cv.imshow('frame',frame)
            if cv.waitKey(1)==ord('q'):
                cv.destroyAllWindows()
                self.cap.release()
                break


if __name__=='__main__':
    obj=Virtual_Pointer()
    obj.run()


