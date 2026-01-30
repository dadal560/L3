import libjevois as jevois
import cv2 as cv
import numpy as np

## Dense Optical Flow Farneback en Niveaux de Gris
class FlowGray:
    def __init__(self):
        self.old_gray = None
        self.timer = jevois.Timer('FlowGray', 50, jevois.LOG_DEBUG)

    def process(self, inframe, outframe):
        frame_bgr = inframe.getCvBGR()
        frame_gray = cv.cvtColor(frame_bgr, cv.COLOR_BGR2GRAY)
        self.timer.start()
        
        if self.old_gray is None:
            self.old_gray = frame_gray.copy()
            outframe.sendCv(frame_bgr)
            return

        flow = cv.calcOpticalFlowFarneback(self.old_gray, frame_gray, None, 
                                          0.5, 3, 15, 3, 5, 1.2, 0)

        mag, _ = cv.cartToPolar(flow[..., 0], flow[..., 1])

        seuil = 0.75

        _,mag_binaire = cv.threshold(mag,seuil,255,cv.THRESH_BINARY)
        display_frame = (mag_binaire)

        self.old_gray = frame_gray.copy()

        fps = self.timer.stop()
        cv.putText(display_frame, fps, (3, 15), 
                   cv.FONT_HERSHEY_SIMPLEX, 0.4, 255, 1)

        outframe.sendCv(display_frame)