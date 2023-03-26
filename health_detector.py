import numpy
import pytesseract
from mss import mss
import cv2


class HealthDetector:
    def __init__(self, serial_connector):
        self.overwatch_health_area = {'top': 885, 'left': 145, 'width': 85, 'height': 48}
        self.last_health = 0
        self.serial_connector = serial_connector
        self.current_health = 0
        self.locate_tesseract()

    def locate_tesseract(self):
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    def detect_health(self):
        sct = mss()
        img = numpy.asarray(sct.grab(self.overwatch_health_area))
        __, screen = cv2.threshold(img, 230, 255, cv2.THRESH_TOZERO)
        text = pytesseract.image_to_string(screen, config='--psm 6')
        words = text.split()
        if words and words[0].isdigit():
            self.current_health = int(words[0])

        if self.current_health == 0 and self.last_health != 0:
            self.serial_connector.write(b'death\n\r')
        elif self.current_health < self.last_health and self.last_health != 0:
            self.serial_connector.write(b'loss\n\r')
        self.last_health = self.current_health
