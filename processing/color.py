import cv2
import numpy as np

class CarColorExtractor:
    def extract(self, frame, bbox):
        x1, y1, x2, y2 = map(int, bbox)
        w, h = x2-x1, y2-y1
        cx1, cy1 = x1 + int(w*0.25), y1 + int(h*0.25)
        cx2, cy2 = x1 + int(w*0.75), y1 + int(h*0.75)
        crop = frame[cy1:cy2, cx1:cx2]
        if crop.size == 0:
            return "unknown"

        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
        h_mean = np.mean(hsv[:,:,0])
        s_mean = np.mean(hsv[:,:,1])
        v_mean = np.mean(hsv[:,:,2])

        if v_mean > 200 and s_mean < 40:
            return "white"
        if v_mean < 70:
            return "black"

        if s_mean > 60:
            if h_mean < 10 or h_mean > 160:
                return "red"
            if 35 < h_mean < 85:
                return "green"
            if 90 < h_mean < 130:
                return "blue"

        return "white" if v_mean > 140 else "black"