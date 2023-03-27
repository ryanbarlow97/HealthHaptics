import numpy
import pytesseract
from mss import mss
import cv2

class HealthDetector:
    def __init__(self, serial_connector):
        self.overwatch_health_area = {'top': 885, 'left': 145, 'width': 85, 'height': 48}
        self.rust_health_area = {'top': 100, 'left': 100, 'width': 100, 'height': 100}  # Example values
        self.fortnite_health_area = {'top': 200, 'left': 200, 'width': 200, 'height': 200}  # Example values
        self.csgo_health_area = {'top': 300, 'left': 300, 'width': 300, 'height': 300}  # Example values

        self.game_areas = {
            "Overwatch": self.overwatch_health_area,
            "Rust": self.rust_health_area,
            "Fortnite": self.fortnite_health_area,
            "Counter Strike: GO": self.csgo_health_area
        }
        
        self.selected_game_area= None
        self.last_health = 0
        self.serial_connector = serial_connector
        self.current_health = 0
        self.haptics_enabled = True
        self.locate_tesseract()
        
    def set_game(self, game_name):
        self.selected_game_area = self.game_areas.get(game_name, self.game_areas)

    def locate_tesseract(self):
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    def detect_health(self):
        if self.selected_game_area is None:
            return
        
        if self.haptics_enabled:
            sct = mss()
            img = numpy.asarray(sct.grab(self.selected_game_area))
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