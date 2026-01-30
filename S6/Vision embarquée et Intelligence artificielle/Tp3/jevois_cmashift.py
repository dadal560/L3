import libjevois as jevois
import cv2
import numpy as np

class Camshit:
    def __init__(self):
        self.timer = jevois.Timer("processing timer", 100, jevois.LOG_INFO)
        
        # Param�tres de tracking
        self.track_mode = False
        self.termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
        
        # D�finition d'une ROI initiale (x, y, w, h) au centre de l'image 320x240
        self.roiBox = (130, 90, 60, 60) 
        self.roiHist = None

    

    def process(self, inframe, outframe):
        # Acquisition de l'image
        frame = inframe.getCvBGR()
        self.timer.start()
        
        # Lissage pour r�duire le bruit
        frame = cv2.GaussianBlur(frame, (5, 5), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Initialisation
        if not self.track_mode:
            
            x, y, w, h = self.roiBox
            roi = frame[y:y+h, x:x+w]
            hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            
            # Calcul de l'histogramme sur la teinte (H)
            self.roiHist = cv2.calcHist([hsv_roi], [0], None, [16], [0, 180])
            cv2.normalize(self.roiHist, self.roiHist, 0, 255, cv2.NORM_MINMAX)
            
            # Dessin de la zone de d�part
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            self.track_mode = True 

        #CamShift
        else:
            # Mode meanshift|camshift
            # retroprojection de l'histogramme sur l'image courante
            backProj = cv2.calcBackProject([hsv], [0], self.roiHist, [0, 180], 1)

            disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
            backProj = cv2.morphologyEx(backProj, cv2.MORPH_OPEN, disc )
            backProj = cv2.morphologyEx(backProj, cv2.MORPH_CLOSE, disc)

            # application du camshift 
            r, self.roiBox = cv2.CamShift(
                backProj, self.roiBox, self.termination
            ) 

    
            pts = np.intp(
                cv2.boxPoints(r)
            )  # r contient les coordonn�es mises � jour de la ROI (fonction meanshift ou camshift)
            # trac�s de la boite englobante
            cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
            
            
        # Envoi du r�sultat vers l'USB
        outframe.sendCv(frame)