
# Imports: -
import cv2               # For The LiveStream Detection
import os                # For Advanced Controls 
import mediapipe as mp   # Hand Detection Library
import ctypes
import time

clickflag=False
clicktime=  0
prev_time = 0
curr_time = 0

nirCmdPath="nircmd-x64"
os.chdir(nirCmdPath)

    #get screen dimensions
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
width = user32.GetSystemMetrics(0)
height = user32.GetSystemMetrics(1) 


# initialize hand tracking module
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

f1,f2,f3,f4,f5 = 0,0,0,0,0
mouseFlag=False
# initialize video capture from default camera

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# loop through frames from video capture
with mp_hands.Hands(max_num_hands = 1,min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, sFrame = cap.read()
        

        flipped = cv2.flip(sFrame,1)
        #frame = imutils.resize(flipped,width=width,height=height)
        
        if clickflag:
            curr_time = time.time()
            clicktime+=curr_time-prev_time
            prev_time = curr_time
            if clicktime>=2:
                clickflag=False
                clicktime=0



        # convert frame to RGB for hand tracking
        image = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # detect hands in the frame
        results = hands.process(image)

        # count the number of fingers raised
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                

                # draw hand landmarks on frame
                #mp_drawing.draw_landmarks(flipped, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # get landmarks for all finger tips
                fingertips = [hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP],
                            hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
                            hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP],
                            hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP],
                            hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]]
                
                
            
                fingerpips = [hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP],
                            hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP],
                            hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP],
                            hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP],
                            hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]]
                
                
                
                if (fingertips[0]).y < (fingerpips[0]).y:
                    f1=1
                else:
                    f1=0

                if (fingertips[1]).y<(fingerpips[1]).y:
                    f2=1
                else:
                    f2=0    

                if (fingertips[2]).y<(fingerpips[2]).y:
                    f3=1
                else:
                    f3=0     
                
                if (fingertips[3]).y<(fingerpips[3]).y:
                    f4=1
                else:
                    f4=0
            
                if (fingertips[4]).x < (fingerpips[4]).x:
                    f5=1
                else:
                    f5=0
                
                num_fingers_raised = f1+f2+f3+f4+f5

                if  f1 == 1 and f4==1 and f5==1 and f2==0 and f3==0:
                    mouseFlag=True
                elif f1 == 1 and  f4==1 and f5==0 and f2==0 and f3==0:
                    mouseFlag=False

                    
                    

                
                if not mouseFlag: 

                    if num_fingers_raised==1:
                        os.system('cmd /c nircmd.exe changesysvolume +900')
                        cv2.putText(flipped, "Raising Volume ", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                    elif num_fingers_raised==2:
                        os.system('cmd /c nircmd.exe changesysvolume -900')
                        cv2.putText(flipped, "Lowering Volume ", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                    elif num_fingers_raised==3:
                        os.system('cmd /c nircmd.exe changebrightness +1')
                        cv2.putText(flipped, "Raising Brightness ", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                    elif num_fingers_raised==4:
                        os.system('cmd /c nircmd.exe changebrightness -1')
                        cv2.putText(flipped, "Lowering Brightness ", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        

        
                else:  # virtual mouse code
                        cv2.putText(flipped,"Mouse is [ON]", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 80, 0), 2)
                        
                        f1_mcp=hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                        w=f1_mcp.x
                        h=f1_mcp.y
                        if w<0.5:
                            w=w-0.2*(0.5-w)/0.3
                        else:
                            w=w+0.2*(w-0.5)/0.3

                        if h<0.5:
                            h=h-0.2*(0.5-h)/0.3
                        else:
                            h=h+0.2*(h-0.5)/0.3

                        if w>1:
                            w=0.995
                        elif w<0:
                            w=0.001
                        if h>1:
                            h=0.98
                        elif h<0:
                            h=0 
                            

                        os.system(f'cmd /c nircmd.exe setcursor {w*width} {h*height}')

                        # Left Click
                        if f5==0 and f1==1 and f2==1 and f3==0 and f4==0 and not clickflag:
                            os.system('cmd /c nircmd.exe sendmouse left click')
                            cv2.putText(flipped, "Left Click ", (300, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                            clickflag=1
                            
                        # Right Click
                        if f5==1 and f1==1 and f2==0 and f3==0 and f4==0 and not clickflag:   
                            os.system('cmd /c nircmd.exe sendmouse right click')
                            cv2.putText(flipped, "Right Click ", (300, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                            clickflag=1

                        # Double Click
                        if f5==0 and f1==1 and f2==0 and f3==0 and f4==0 and not clickflag:
                            os.system('cmd /c nircmd.exe sendmouse left dblclick')
                            cv2.putText(flipped, "Double Click ", (300, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                            clickflag=1

                        # Scroll Down
                        if f5==0 and f1==1 and f2==1 and f3==1 and f4==0: 
                            os.system('cmd /c nircmd.exe sendmouse wheel -60')
                            cv2.putText(flipped, "Scroll Down ", (300, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

                        # Scroll Up
                        if f5==0 and f1==1 and f2==1 and f3==1 and f4==1: 
                            os.system('cmd /c nircmd.exe sendmouse wheel 60') 
                            cv2.putText(flipped, "Scroll up ", (300, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)


                        # Grap And Drop
                        if f5==0 and f1==0 and f2==0 and f3==0 and f4==0:
                            os.system('cmd /c nircmd.exe sendmouse left down')
                        else:
                            os.system('cmd /c nircmd.exe sendmouse left up')
                                

                            # our Refrence: -
                            #os.system('cmd /c nircmd.exe sendmouse [right | left | middle] [down | up | click | dblclick]')
                        

                cv2.putText(flipped, f"Fingers raised: {num_fingers_raised}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # display frame
        cv2.imshow('Hand tracking', flipped)

    # check for exit command
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break                       

# release video capture and close all windows
cap.release()
cv2.destroyAllWindows()