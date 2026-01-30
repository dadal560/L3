import numpy as np
import cv2
import math

roiPts = []
track_mode = False
termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
roiBox = None
kernel = np.ones((5, 5), np.uint8)
frame_width_in_px = 640
number_of_histogram_elements = 16


def selectROI(event, x, y, flags, param):
    """
    Selection de 4 points pour définir la région d'intérêt par 4 clicks souris
    """
    global track_mode, roiPts

    if (event == cv2.EVENT_LBUTTONDOWN) and (len(roiPts) == 4):
        roiPts = []
        track_mode = False
    if (event == cv2.EVENT_LBUTTONDOWN) and (len(roiPts) < 4):
        roiPts.append([x, y])

cam = 0  # capture from camera at location 0
cap = cv2.VideoCapture(cam)
cv2.namedWindow("frame")
cv2.setMouseCallback("frame", selectROI)

while True:
    ret, frame = cap.read()
    # un peu de lissage...
    frame = cv2.boxFilter(frame, 0, (5, 5), normalize=True)
    print(roiPts)
    # tracé éventuel des 4 points
    if len(roiPts) <= 4 and len(roiPts) > 0:
        for x, y in roiPts:
            cv2.circle(
                frame, (x, y), 4, (0, 255, 0), 1
            )  # tracé de cercles autour des clicks

    if len(roiPts) == 4 and track_mode == False:  # initialisation du meanshift|camshift
        # Calcul de la boite englobante
        roiBox = np.array(roiPts, dtype=np.int32)
        s = roiBox.sum(axis=1)
        tl = roiBox[np.argmin(s)]
        br = roiBox[np.argmax(s)]
        roi = frame[tl[1] : br[1], tl[0] : br[0]]

        # conversion en HSV
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        

        # calcul de l'histogramme et normalisation
        roiHist = cv2.calcHist([hsv_roi], [0], None, [16], [0, 180])
        cv2.normalize(roiHist, roiHist, 0, 255, cv2.NORM_MINMAX)
        

        roiBox = (tl[0], tl[1], br[0], br[1])
        track_mode = True # Fin de la phase d'initialisation : la prochaine acquisition utilisera le meanshift|camshift

    # Mode meanshift|camshift
    if track_mode == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        backProj = cv2.calcBackProject([hsv], [0], roiHist, [0, 180], 1)  
        disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        backProj = cv2.morphologyEx(backProj, cv2.MORPH_OPEN, disc)
        backProj = cv2.morphologyEx(backProj, cv2.MORPH_CLOSE, disc)
        
        # Afficher la rétroprojection
        cv2.imshow("BackProj", backProj)
        
        r, roiBox = cv2.CamShift(backProj, roiBox, termination)
        
        M = cv2.moments(backProj)
  

        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        a = M['mu20'] / M['m00'] 
        b = 2 * (M['mu11'] / M['m00']) 
        c = M['mu02'] / M['m00'] 
        d = b**2 + (a - c)**2

        l = math.sqrt(((a + c) + math.sqrt(d)) / 2)
        w = math.sqrt(((a + c) - math.sqrt(d)) / 2)

        #angle 
        if (a - c) == 0:
                theta = math.pi / 2
        else:
            theta = 0.5 * math.atan(b / (a - c))
        
        cos_val = math.cos(theta)
        s = math.sin(theta)
        cv2.line( frame, (int(cX - cos_val * w), int(cY - s * w)), (int(cX + cos_val * w), int(cY + s * w)), (255, 255, 0),2,)
        cv2.line( frame, (int(cX + s * l), int(cY - cos_val * l)), (int(cX - s * l), int(cY + cos_val * l)), (255, 255, 0), 2,)
        
        pts = np.intp(
            cv2.boxPoints(r)
        )  # r contient les coordonnées mises à jour de la ROI (fonction meanshift ou camshift)
        # tracés de la boite englobante
        cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
    
    cv2.imshow("frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
