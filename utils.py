
import cv2
import mediapipe as mp
import math
import numpy as np
from tkinter import *

class VideoROIExtractor:
    """Helper class for extracting and saving/showing ROI (Region Of Interest) from a video file."""

    def __init__(self, verbose=True, sFactor=0.4, zFactor=0.8 , outputSize=400 ,path='1.mp4'):
        """Creates a new VideoROIExtractor.

        Arguments:
            verbose     :   whether to print warnings and error messages
            sFactor     :   By adjusting this number, extracted roi videos can be
                            stabilized. If the roi (hands,feet) moves fast set this 
                            to a lower value close to 0. If the roi moves slow 
                            (i.e. stationary most of the time) set this to a higher value.
            zFactor     :   By adjusting this number, frame will be more zoomed in on
                            the roi. The lower the value, more zooming in. 0.8 is a 
                            preferable value
            OutputSize  :   The output size of the video
            Path        :   path to the video

        """
        self.verbose = verbose                          
        self.sFactor = sFactor
        self.zFactor = zFactor
        self.pose_estimator = mp.solutions.pose     #pose estimator
        self.hand_pose =  mp.solutions.holistic     #pose estimator for the hand
        self.drawer = mp.solutions.drawing_utils    #drawing class for the key points
        self.path = path                            #path of the video
        self.cap = cv2.VideoCapture(self.path)      #video capture
        self.image_width = int(self.cap.get(3))     #width of a frame
        self.image_hight = int(self.cap.get(4))     #height of a frame
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)   #frame rate of the video
        self.outputSize = outputSize                #output video dimension


    def HandExtractor(self, save=False , handSide='L' ,fillMiss=False,handVisual=False,P=0.1):
        """Reads frames and extract the hands.

        Arguments:
            save        : if True the extrcted roi videos will be saved.
            handSide    : which hand to track. Right or Left. Right ==> 'R' , Left ==> 'L'
            fillMiss    : if the keypoints are not detected in a frame previously detected
                          keypoits will be used.
            handVisual  : if true, hand landmarks and connection will be drawn on the frame

        """
        #############################################################
        print('width',self.image_width)
        print('height',self.image_hight)
        Pre_width=-1
        Pre_y=0
        Pre_x=0
        Pre_x_WRIST=-1
        # Pre_y_WRIST=-1
        # Pre_x_ELBOW=-1
        # Pre_y_ELBOW=-1
        if handVisual==True:
            pose = self.hand_pose.Holistic(upper_body_only=True,min_detection_confidence=0.5, min_tracking_confidence=0.5)
            self.pose_estimator=self.hand_pose
        else:
            pose = self.pose_estimator.Pose(upper_body_only=True,min_detection_confidence=0.5, min_tracking_confidence=0.5)
        ##############################################################
        if save:
            print('Saving Initialized.......')
            if handVisual:
                out = cv2.VideoWriter(self.path[:-4]+handSide+'Hand'+'Visual'+'.avi',
                                cv2.VideoWriter_fourcc('M','J','P','G'), self.fps, (self.outputSize,self.outputSize))
            else:
                out = cv2.VideoWriter(self.path[:-4]+handSide+'Hand'+'.avi',
                                cv2.VideoWriter_fourcc('M','J','P','G'), self.fps, (self.outputSize,self.outputSize))
        while self.cap.isOpened():
            skip=False
            success, image = self.cap.read()
            if not success and self.verbose:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                break
            ################the BGR image to RGB#####################
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            ################extracting the cordinates#################
            if results.pose_landmarks ==None:
                (x_WRIST,y_WRIST,x_ELBOW,y_ELBOW,x_INDEX,y_INDEX)=(None,None,None,None,None,None)
            else:
                if handSide=='L':
                    x_WRIST=int(results.pose_landmarks.landmark[self.pose_estimator.PoseLandmark.LEFT_WRIST].x * self.image_width)
                    y_WRIST=int(results.pose_landmarks.landmark[self.pose_estimator.PoseLandmark.LEFT_WRIST].y * self.image_hight)
                    x_ELBOW=int(results.pose_landmarks.landmark[self.pose_estimator.PoseLandmark.LEFT_ELBOW].x * self.image_width)
                    y_ELBOW=int(results.pose_landmarks.landmark[self.pose_estimator.PoseLandmark.LEFT_ELBOW].y * self.image_hight)
                    x_INDEX=int(results.pose_landmarks.landmark[self.pose_estimator.PoseLandmark.LEFT_INDEX].x * self.image_width)
                    y_INDEX=int(results.pose_landmarks.landmark[self.pose_estimator.PoseLandmark.LEFT_INDEX].y * self.image_hight)
                    if handVisual==True:
                        self.drawer.draw_landmarks(image, results.left_hand_landmarks, self.hand_pose.HAND_CONNECTIONS)
                    # image = cv2.circle(image, (x_INDEX,y_INDEX), radius=5, color=(0, 0, 255), thickness=2)
                else:
                    x_WRIST=int(results.pose_landmarks.landmark[self.pose_estimator.PoseLandmark.RIGHT_WRIST].x * self.image_width)
                    y_WRIST=int(results.pose_landmarks.landmark[self.pose_estimator.PoseLandmark.RIGHT_WRIST].y * self.image_hight)
                    x_ELBOW=int(results.pose_landmarks.landmark[self.pose_estimator.PoseLandmark.RIGHT_ELBOW].x * self.image_width)
                    y_ELBOW=int(results.pose_landmarks.landmark[self.pose_estimator.PoseLandmark.RIGHT_ELBOW].y * self.image_hight)
                    x_INDEX=int(results.pose_landmarks.landmark[self.pose_estimator.PoseLandmark.RIGHT_INDEX].x * self.image_width)
                    y_INDEX=int(results.pose_landmarks.landmark[self.pose_estimator.PoseLandmark.RIGHT_INDEX].y * self.image_hight)
                    if handVisual==True:
                        self.drawer.draw_landmarks(image, results.right_hand_landmarks, self.hand_pose.HAND_CONNECTIONS)
                                    
                ##########################################################
            #print(x_ELBOW,y_ELBOW,x_WRIST,y_WRIST,x_INDEX,y_INDEX)
           
            if ((x_WRIST==None) and (Pre_x_WRIST==-1)) :
                
                skip=True
                resized=np.zeros((self.outputSize,self.outputSize,3), dtype='uint8')
                cv2.putText(resized,'Selected body part cannot be detected.',(10,int(self.outputSize/2-20)),cv2.FONT_HERSHEY_COMPLEX,
                                            0.55,(0,0,255),1)
                cv2.putText(resized,'If you see this message continuously,',(10,int(self.outputSize/2)),cv2.FONT_HERSHEY_COMPLEX,
                                        0.55,(0,0,255),1)
                cv2.putText(resized,'play the original video.',(10,int(self.outputSize/2+20)),cv2.FONT_HERSHEY_COMPLEX,
                                        0.55,(0,0,255),1)                            
            elif (x_WRIST==None):
                if fillMiss:
                    (x_WRIST,y_WRIST,x_ELBOW,y_ELBOW,x_INDEX,y_INDEX) = (Pre_x_WRIST,Pre_y_WRIST,Pre_x_ELBOW,Pre_y_ELBOW, Pre_x_INDEX,Pre_y_INDEX)
                else:
                    skip=True
                    resized=np.zeros((self.outputSize,self.outputSize,3), dtype='uint8')
                    cv2.putText(resized,'Selected body part cannot be detected.',(10,int(self.outputSize/2-20)),cv2.FONT_HERSHEY_COMPLEX,
                                            0.55,(0,0,255),1)
                    cv2.putText(resized,'If you see this message continuously,',(10,int(self.outputSize/2)),cv2.FONT_HERSHEY_COMPLEX,
                                            0.55,(0,0,255),1)
                    cv2.putText(resized,'play the original video.',(10,int(self.outputSize/2+20)),cv2.FONT_HERSHEY_COMPLEX,
                                            0.55,(0,0,255),1)
            

            if not skip:
                (Pre_x_WRIST,Pre_y_WRIST,Pre_x_ELBOW,Pre_y_ELBOW,Pre_x_INDEX,Pre_y_INDEX) = (x_WRIST,y_WRIST,x_ELBOW,y_ELBOW,x_INDEX,y_INDEX)
                width = int(math.sqrt((x_WRIST-x_ELBOW)**2+(y_WRIST-y_ELBOW)**2))
                ##########################################################
                if width>=Pre_width:
                    Pre_width = width
                else:
                    width = Pre_width
                ##########################################################
                STATE01=((x_INDEX >= Pre_x-int(self.sFactor*width)) and (x_INDEX <= Pre_x+int(self.sFactor*width)))
                STATE02=((y_INDEX >= Pre_y-int(self.sFactor*width)) and (y_INDEX <= Pre_y+int(self.sFactor*width)))
                # STATE03=(x_WRIST<x_INDEX)
                # STATE04=(y_WRIST<y_INDEX)
                ##########################################################
                if  STATE01 and STATE02 :
                    y_INDEX = Pre_y
                    x_INDEX = Pre_x
                else:
                    Pre_y = y_INDEX
                    Pre_x = x_INDEX
                ##########################################################
                #Y1,Y2,X1,X2 = self._get_bbox_hand_(y_INDEX,x_INDEX,width,STATE03,STATE04,P)
                cropped=image[max(int(y_INDEX-width*self.zFactor),0):int(y_INDEX+width*self.zFactor),max(0,int(x_INDEX-width*self.zFactor)):int(x_INDEX+width*self.zFactor)]
                #print('cropped',int(y_WRIST-width*self.zFactor),int(y_WRIST+width*self.zFactor),int(x_WRIST-width*self.zFactor),int(x_WRIST+width*self.zFactor))
                #cropped=image[Y1:Y2,X1:X2]
                try:
                    resized = cv2.resize(cropped, (self.outputSize, self.outputSize))
                except:
                    resized=np.zeros((self.outputSize,self.outputSize,3), dtype='uint8')
                    cv2.putText(resized,'Selected body part cannot be detected.',(10,int(self.outputSize/2-20)),cv2.FONT_HERSHEY_COMPLEX,
                                            0.55,(0,0,255),1)
                    cv2.putText(resized,'If you see this message continuously,',(10,int(self.outputSize/2)),cv2.FONT_HERSHEY_COMPLEX,
                                            0.55,(0,0,255),1)
                    cv2.putText(resized,'play the original video.',(10,int(self.outputSize/2+20)),cv2.FONT_HERSHEY_COMPLEX,
                                            0.55,(0,0,255),1)
                #resized=cropped
            ##########################################################
            # if handVisual==True:
            #     hands = self.hand_pose.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
            #     resultshand = hands.process(resized)
            #     if resultshand.multi_hand_landmarks:
            #         for hand_landmarks in resultshand.multi_hand_landmarks:
            #             self.drawer.draw_landmarks(resized, hand_landmarks, self.hand_pose.HAND_CONNECTIONS)
            
            resized = cv2.cvtColor(resized, cv2.COLOR_RGB2BGR)
                
            if save:
                out.write(resized)
            else:
                cv2.imshow('MediaPipe Pose', resized)
                if cv2.waitKey(5) & 0xFF == 27: # press escape key to quit the video
                    break
                if cv2.getWindowProperty('MediaPipe Pose', 0) < 0:
                    break
        pose.close()
        if save:
            out.release()
            messagebox.showinfo(title="Message", message="SAVING COMPLETED!",icon='info')
        self.cap.release()
        cv2.destroyAllWindows()
        return None

    def _get_bbox_hand_(self,yw,xw,w,l1,l2,p):
        if (l1==True) and (l2==True):
            (y1,y2,x1,x2)=(max(0,int(yw-w*self.zFactor*(1-p))),min(self.image_hight,int(yw+w*self.zFactor*(1+p))),
                max(0,int(xw-w*self.zFactor*(1-p))),min(self.image_width,int(xw+w*self.zFactor*(1+p))))
        elif (l1==True) and (l2==False):
            (y1,y2,x1,x2)=(max(0,int(yw-w*self.zFactor*(1+p))),min(self.image_hight,int(yw+w*self.zFactor*(1-p))),
                max(0,int(xw-w*self.zFactor*(1-p))),min(self.image_width,int(xw+w*self.zFactor*(1+p))))
        elif (l1==False) and (l2==False):
            (y1,y2,x1,x2)=(max(0,int(yw-w*self.zFactor*(1+p))),min(self.image_hight,int(yw+w*self.zFactor*(1-p))),
                max(0,int(xw-w*self.zFactor*(1+p))),min(self.image_width,int(xw+w*self.zFactor*(1-p))))
        elif (l1==False) and (l2==True):
            (y1,y2,x1,x2)=(max(0,int(yw-w*self.zFactor*(1-p))),min(self.image_hight,int(yw+w*self.zFactor*(1+p))),
                max(0,int(xw-w*self.zFactor*(1+p))),min(self.image_width,int(xw+w*self.zFactor*(1-p))))
        return y1,y2,x1,x2


    def FootExtractor(self, save=False , footSide='L' ,fillMiss=False):
        """Reads frames and extracts the feet.

        Arguments:
            save        : if True the extrcted roi videos will be saved.
            footSide    : which foot to track. Right or Left. Right ==> 'R' , Left ==> 'L'
            fillMiss    : if the keypoints are not detected in a frame previously detected
                          keypoits will be used.

        """
        #############################################################
        Pre_width=-1
        Pre_y=0
        Pre_x=0
        Pre_x_HEEL=-1
        # Pre_y_WRIST=-1
        # Pre_x_ELBOW=-1
        # Pre_y_ELBOW=-1
        
        pose = self.pose_estimator.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        ##############################################################
        if save:
            out = cv2.VideoWriter(self.path[:-4]+footSide+'Foot'+'.avi',
                                cv2.VideoWriter_fourcc('M','J','P','G'), self.fps, (self.outputSize,self.outputSize))
        while self.cap.isOpened():
            skip=False
            success, image = self.cap.read()
            if not success and self.verbose:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                break
            ################the BGR image to RGB#####################
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            ################extracting the cordinates#################
            if results.pose_landmarks == None:
                (x_HEEL,y_HEEL,x_INDEX,y_INDEX)=(None,None,None,None)
            else:
                if footSide=='L':
                    x_HEEL=int(results.pose_landmarks.landmark[self.pose_estimator.PoseLandmark.LEFT_HEEL].x * self.image_width)
                    y_HEEL=int(results.pose_landmarks.landmark[self.pose_estimator.PoseLandmark.LEFT_HEEL].y * self.image_hight)
                    x_INDEX=int(results.pose_landmarks.landmark[self.pose_estimator.PoseLandmark.LEFT_FOOT_INDEX].x * self.image_width)
                    y_INDEX=int(results.pose_landmarks.landmark[self.pose_estimator.PoseLandmark.LEFT_FOOT_INDEX].y * self.image_hight)
                else:
                    x_HEEL=int(results.pose_landmarks.landmark[self.pose_estimator.PoseLandmark.RIGHT_HEEL].x * self.image_width)
                    y_HEEL=int(results.pose_landmarks.landmark[self.pose_estimator.PoseLandmark.RIGHT_HEEL].y * self.image_hight)
                    x_INDEX=int(results.pose_landmarks.landmark[self.pose_estimator.PoseLandmark.RIGHT_FOOT_INDEX].x * self.image_width)
                    y_INDEX=int(results.pose_landmarks.landmark[self.pose_estimator.PoseLandmark.RIGHT_FOOT_INDEX].y * self.image_hight)
                
                ##########################################################
            #print(x_HEEL,y_HEEL,x_INDEX,y_INDEX)
           
            if ((x_HEEL==None) and (Pre_x_HEEL==-1)) :
                
                skip=True
                resized=np.zeros((self.outputSize,self.outputSize,3), dtype='uint8')
                cv2.putText(resized,'Selected body part cannot be detected.',(10,int(self.outputSize/2-20)),cv2.FONT_HERSHEY_COMPLEX,
                                            0.55,(0,0,255),1)
                cv2.putText(resized,'If you see this message continuously,',(10,int(self.outputSize/2)),cv2.FONT_HERSHEY_COMPLEX,
                                        0.55,(0,0,255),1)
                cv2.putText(resized,'play the original video.',(10,int(self.outputSize/2+20)),cv2.FONT_HERSHEY_COMPLEX,
                                        0.55,(0,0,255),1)                            
            elif (x_HEEL==None):
                if fillMiss:
                    (x_HEEL,y_HEEL,x_INDEX,y_INDEX) = (Pre_x_HEEL,Pre_y_HEEL, Pre_x_INDEX,Pre_y_INDEX)
                else:
                    skip=True
                    resized=np.zeros((self.outputSize,self.outputSize,3), dtype='uint8')
                    cv2.putText(resized,'Selected body part cannot be detected.',(10,int(self.outputSize/2-20)),cv2.FONT_HERSHEY_COMPLEX,
                                            0.55,(0,0,255),1)
                    cv2.putText(resized,'If you see this message continuously,',(10,int(self.outputSize/2)),cv2.FONT_HERSHEY_COMPLEX,
                                            0.55,(0,0,255),1)
                    cv2.putText(resized,'play the original video.',(10,int(self.outputSize/2+20)),cv2.FONT_HERSHEY_COMPLEX,
                                            0.55,(0,0,255),1)
            

            if not skip:
                (Pre_x_HEEL,Pre_y_HEEL,Pre_x_INDEX,Pre_y_INDEX) = (x_HEEL,y_HEEL,x_INDEX,y_INDEX)
                width = int(math.sqrt((x_HEEL-x_INDEX)**2+(y_HEEL-y_INDEX)**2))*1
                x_CEN=int((x_HEEL+x_INDEX)/2)
                y_CEN=int((y_HEEL+y_INDEX)/2)
                ##########################################################
                if width>=Pre_width:
                    Pre_width = width
                else:
                    width = Pre_width
                ##########################################################
                STATE01=((x_CEN >= Pre_x-int(self.sFactor*width)) and (x_CEN<= Pre_x+int(self.sFactor*width)))
                STATE02=((y_CEN >= Pre_y-int(self.sFactor*width)) and (y_CEN <= Pre_y+int(self.sFactor*width)))
                # STATE03=(x_WRIST<x_INDEX)
                # STATE04=(y_WRIST<y_INDEX)
                ##########################################################
                if  STATE01 and STATE02 :
                    y_CEN = Pre_y
                    x_CEN = Pre_x
                else:
                    Pre_y = y_CEN
                    Pre_x = x_CEN
                ##########################################################
                #Y1,Y2,X1,X2 = self._get_bbox_hand_(y_INDEX,x_INDEX,width,STATE03,STATE04,P)
                cropped=image[max(int(y_CEN-width*self.zFactor),0):int(y_CEN+width*self.zFactor),max(0,int(x_CEN-width*self.zFactor)):int(x_CEN+width*self.zFactor)]
                #print('cropped',int(y_WRIST-width*self.zFactor),int(y_WRIST+width*self.zFactor),int(x_WRIST-width*self.zFactor),int(x_WRIST+width*self.zFactor))
                #cropped=image[Y1:Y2,X1:X2]
                try:
                    resized = cv2.resize(cropped, (self.outputSize, self.outputSize))
                except:
                    resized=np.zeros((self.outputSize,self.outputSize,3), dtype='uint8')
                    cv2.putText(resized,'Selected body part cannot be detected.',(10,int(self.outputSize/2-20)),cv2.FONT_HERSHEY_COMPLEX,
                                            0.55,(0,0,255),1)
                    cv2.putText(resized,'If you see this message continuously,',(10,int(self.outputSize/2)),cv2.FONT_HERSHEY_COMPLEX,
                                            0.55,(0,0,255),1)
                    cv2.putText(resized,'play the original video.',(10,int(self.outputSize/2+20)),cv2.FONT_HERSHEY_COMPLEX,
                                            0.55,(0,0,255),1)
            ##########################################################
            resized = cv2.cvtColor(resized, cv2.COLOR_RGB2BGR)
            if save:
                out.write(resized)
            else:
                cv2.imshow('MediaPipe Pose', resized)
                if cv2.waitKey(5) & 0xFF == 27: # press escape key to quit the video
                    break
                if cv2.getWindowProperty('MediaPipe Pose', 0) < 0:
                    break
        pose.close()
        cv2.destroyAllWindows()
        if save:
            out.release()
            messagebox.showinfo(title="Message", message="SAVING COMPLETED!",icon='info')
        self.cap.release()
        return None
    
    def HeadExtractor(self, save=False ,fillMiss=False):
        """Reads frames and extracts the head.

        Arguments:
            save        : if True the extrcted roi videos will be saved.
            fillMiss    : if the keypoints are not detected in a frame previously detected
                          keypoits will be used.

        """
        #############################################################
        Pre_width=-1
        Pre_y=0
        Pre_x=0
        Pre_x_NOSE=-1
        # Pre_y_WRIST=-1
        # Pre_x_ELBOW=-1
        # Pre_y_ELBOW=-1
        
        pose = self.pose_estimator.Pose(upper_body_only=True,min_detection_confidence=0.5, min_tracking_confidence=0.5)
        ##############################################################
        if save:
            out = cv2.VideoWriter(self.path[:-4]+'Head'+'.avi',
                                cv2.VideoWriter_fourcc('M','J','P','G'), self.fps, (self.outputSize,self.outputSize))
        while self.cap.isOpened():
            skip=False
            success, image = self.cap.read()
            if not success and self.verbose:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                break
            ################the BGR image to RGB#####################
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            ################extracting the cordinates#################
            if results.pose_landmarks ==None:
                (x_NOSE,y_NOSE,x_LS,y_LS,x_RS,y_RS)=(None,None,None,None,None,None)
            else:
                x_NOSE=int(results.pose_landmarks.landmark[self.pose_estimator.PoseLandmark.NOSE].x * self.image_width)
                y_NOSE=int(results.pose_landmarks.landmark[self.pose_estimator.PoseLandmark.NOSE].y * self.image_hight)
                x_LS=int(results.pose_landmarks.landmark[self.pose_estimator.PoseLandmark.LEFT_SHOULDER].x * self.image_width)
                y_LS=int(results.pose_landmarks.landmark[self.pose_estimator.PoseLandmark.LEFT_SHOULDER].y * self.image_hight)
                x_RS=int(results.pose_landmarks.landmark[self.pose_estimator.PoseLandmark.RIGHT_SHOULDER].x * self.image_width)
                y_RS=int(results.pose_landmarks.landmark[self.pose_estimator.PoseLandmark.RIGHT_SHOULDER].y * self.image_hight)
            ##########################################################
            #print(x_NOSE,y_NOSE,x_LS,y_LS,x_RS,y_RS)
           
            if ((x_NOSE==None) and (Pre_x_NOSE==-1)):
                
                skip=True
                resized=np.zeros((self.outputSize,self.outputSize,3), dtype='uint8')
                cv2.putText(resized,'Selected body part cannot be detected.',(10,int(self.outputSize/2-20)),cv2.FONT_HERSHEY_COMPLEX,
                                            0.55,(0,0,255),1)
                cv2.putText(resized,'If you see this message continuously,',(10,int(self.outputSize/2)),cv2.FONT_HERSHEY_COMPLEX,
                                        0.55,(0,0,255),1)
                cv2.putText(resized,'play the original video.',(10,int(self.outputSize/2+20)),cv2.FONT_HERSHEY_COMPLEX,
                                        0.55,(0,0,255),1)                            
            elif (x_NOSE==None):
                if fillMiss:
                    (x_NOSE,y_NOSE,x_LS,y_LS,x_RS,y_RS) = (Pre_x_NOSE,Pre_y_NOSE, Pre_x_LS,Pre_y_LS,Pre_x_RS,Pre_y_RS)
                else:
                    skip = True
                    resized=np.zeros((self.outputSize,self.outputSize,3), dtype='uint8')
                    cv2.putText(resized,'Selected body part cannot be detected.',(10,int(self.outputSize/2-20)),cv2.FONT_HERSHEY_COMPLEX,
                                            0.55,(0,0,255),1)
                    cv2.putText(resized,'If you see this message continuously,',(10,int(self.outputSize/2)),cv2.FONT_HERSHEY_COMPLEX,
                                            0.55,(0,0,255),1)
                    cv2.putText(resized,'play the original video.',(10,int(self.outputSize/2+20)),cv2.FONT_HERSHEY_COMPLEX,
                                            0.55,(0,0,255),1)
            

            if not skip:
                (Pre_x_NOSE,Pre_y_NOSE, Pre_x_LS,Pre_y_LS,Pre_x_RS,Pre_y_RS)=(x_NOSE,y_NOSE,x_LS,y_LS,x_RS,y_RS)
                width = int(math.sqrt((x_LS-x_RS)**2+(y_LS-y_RS)**2)/2)*1
                ##########################################################
                if width>=Pre_width:
                    Pre_width = width
                else:
                    width = Pre_width
                ##########################################################
                STATE01=((x_NOSE >= Pre_x-int(self.sFactor*width)) and (x_NOSE<= Pre_x+int(self.sFactor*width)))
                STATE02=((y_NOSE >= Pre_y-int(self.sFactor*width)) and (y_NOSE <= Pre_y+int(self.sFactor*width)))
                # STATE03=(x_WRIST<x_INDEX)
                # STATE04=(y_WRIST<y_INDEX)
                ##########################################################
                if  STATE01 and STATE02 :
                    y_NOSE = Pre_y
                    x_NOSE = Pre_x
                else:
                    Pre_y = y_NOSE
                    Pre_x = x_NOSE
                ##########################################################
                #Y1,Y2,X1,X2 = self._get_bbox_hand_(y_INDEX,x_INDEX,width,STATE03,STATE04,P)
                cropped=image[max(int(y_NOSE-width*self.zFactor*(0.8)),0):int(y_NOSE+width*self.zFactor*(1.2)),max(0,int(x_NOSE-width*self.zFactor)):int(x_NOSE+width*self.zFactor)]
                #print('cropped',int(y_WRIST-width*self.zFactor),int(y_WRIST+width*self.zFactor),int(x_WRIST-width*self.zFactor),int(x_WRIST+width*self.zFactor))
                #cropped=image[Y1:Y2,X1:X2]
                try:
                    resized = cv2.resize(cropped, (self.outputSize, self.outputSize))
                except:
                    resized=np.zeros((self.outputSize,self.outputSize,3), dtype='uint8')
                    cv2.putText(resized,'Selected body part cannot be detected.',(10,int(self.outputSize/2-20)),cv2.FONT_HERSHEY_COMPLEX,
                                            0.55,(0,0,255),1)
                    cv2.putText(resized,'If you see this message continuously,',(10,int(self.outputSize/2)),cv2.FONT_HERSHEY_COMPLEX,
                                            0.55,(0,0,255),1)
                    cv2.putText(resized,'play the original video.',(10,int(self.outputSize/2+20)),cv2.FONT_HERSHEY_COMPLEX,
                                            0.55,(0,0,255),1)
            ##########################################################
            resized = cv2.cvtColor(resized, cv2.COLOR_RGB2BGR)
            if save:
                out.write(resized)
            else:
                cv2.imshow('MediaPipe Pose', resized)
                if cv2.waitKey(5) & 0xFF == 27: # press escape key to quit the video
                    break
                if cv2.getWindowProperty('MediaPipe Pose', 0) < 0:
                    break
        pose.close()
        cv2.destroyAllWindows()
        if save:
            out.release()
            messagebox.showinfo(title="Message", message="SAVING COMPLETED!",icon='info')
        self.cap.release()
        return None
    def OriginalVideo(self):
        while self.cap.isOpened():
            success, image = self.cap.read()
            if not success and self.verbose:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                break
            cv2.imshow('MediaPipe Pose', image)
            cv2.waitKey(5)
            if cv2.waitKey(10) & 0xFF == 27: # press escape key to quit the video
                break
            if cv2.getWindowProperty('MediaPipe Pose', 0) < 0:
                    break
        self.cap.release()
        cv2.destroyAllWindows()
        return None

if __name__ == "__main__":
    vroiE = VideoROIExtractor(verbose=True, sFactor=0.5, zFactor=1.2, outputSize=400 ,path='Full_body.mp4')
    #vroiE.FootExtractor(footSide='R',save=False,fillMiss=False)
    vroiE.HandExtractor(handSide='R',save=True,fillMiss=False,handVisual=True,P=0.075)
    #vroiE.HeadExtractor(save=False,fillMiss=False)