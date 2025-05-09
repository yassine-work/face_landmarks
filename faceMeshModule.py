import cv2
import mediapipe as mp
import time
from mediapipe.python.solutions.face_mesh_connections import FACEMESH_TESSELATION
from mediapipe.python.solutions.face_mesh_connections import FACEMESH_CONTOURS



class FaceMeshDetector():
    def __init__(self, staticMode=False, maxFaces=2, minDetectionCon=0.5, minTrackCon=0.5):
        self.staticMode = staticMode
        self.maxFaces = maxFaces
        self.minDetectionCon = minDetectionCon
        self.minTrackCon = minTrackCon
        self.mpDraw=mp.solutions.drawing_utils
        self.mpFaceMesh=mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(
            static_image_mode=self.staticMode, 
            max_num_faces=self.maxFaces, 
            min_detection_confidence=self.minDetectionCon, 
            min_tracking_confidence=self.minTrackCon
        )        
        self.drawSpec=self.mpDraw.DrawingSpec(thickness=1,circle_radius=2)


    def findFaceMesh(self,img,draw=True):  
        self.imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.faceMesh.process(self.imgRGB)
        faces=[]
        if self.results.multi_face_landmarks:
            for face_index,faceLms in enumerate(self.results.multi_face_landmarks):
                if draw:
                    self.mpDraw.draw_landmarks(img,faceLms,FACEMESH_CONTOURS,
                    self.drawSpec,self.drawSpec)
                face=[]
                for id,lm in enumerate(faceLms.landmark):
                    ih,iw,ic=img.shape
                    x,y=int(lm.x*iw),int(lm.y*ih)
                    print(id,x,y)
                    face.append([x,y])
                faces.append(face)

                #save the landmarks to a json file for each face
                face_data = {"face_index": face_index, "landmarks": face}

                

        return img,faces

    
    


import json




def main():
    cap=cv2.VideoCapture("videos/video2.mp4")
    pTime=0
    detector=FaceMeshDetector()
    image_counter = 0
    while True:
        success,img=cap.read()
        if not success:
            break
        img,faces=detector.findFaceMesh(img)
    


        
        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime
        cv2.putText(img,f'FPS:{int(fps)}',(20,78),cv2.FONT_HERSHEY_PLAIN,
        3,(0,255,0),3)
        cv2.imshow("Image",img)
        cv2.waitKey(1)
    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()
















