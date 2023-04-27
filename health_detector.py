import numpy as np
import pytesseract
from mss import mss
import cv2

class HealthDetector:
    def __init__(self, serial_connector):
        self.overwatch_health_area = {'top': 885, 'left': 150, 'width': 85, 'height': 48}
        self.rust_health_area = {'top': 970, 'left': 1705, 'width': 45, 'height': 18}
        self.fortnite_health_areahp = {'top': 940, 'left': 570, 'width': 60, 'height': 30}
        self.fortnite_health_areashield = {'top': 905, 'left': 570, 'width': 60, 'height': 30}
        self.csgo_health_area = {'top': 1030, 'left': 50, 'width': 70, 'height': 45}

        self.game_areas = {
            "Overwatch": self.overwatch_health_area,
            "Rust": self.rust_health_area,
            "Fortnite": self.fortnite_health_areahp,
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
            img = np.asarray(sct.grab(self.selected_game_area))
            if self.selected_game_area == self.rust_health_area:
                height, width = img.shape[:2]
                scale_factor = 5
                new_width = int(width * scale_factor)
                new_height = int(height * scale_factor)
                resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
                
                gray = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
                text = pytesseract.image_to_string(gray, config='--psm 6 -c tessedit_char_whitelist=0123456789')
                #cv2.imshow("debug", gray)
                
            elif self.selected_game_area == self.overwatch_health_area:
                
                lower_white = np.array([255, 255, 255])
                upper_white = np.array([255, 255, 255])
                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img_gray_expanded = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)

                screen = cv2.inRange(img_gray_expanded, lower_white, upper_white)
                text = pytesseract.image_to_string(screen, config='--psm 6 -c tessedit_char_whitelist=0123456789')
                #cv2.imshow("debug", screen)
                
            elif self.selected_game_area == self.csgo_health_area:
                
                lower_white = np.array([255, 255, 255])
                upper_white = np.array([255, 255, 255])
                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img_gray_expanded = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
                
                __, screen = cv2.threshold(img_gray_expanded, 200, 255, cv2.THRESH_BINARY)
                text = pytesseract.image_to_string(screen, config='--psm 6 -c tessedit_char_whitelist=0123456789')
                
                #print(text)
                cv2.imshow("debug", screen)              
                
            elif self.selected_game_area == self.fortnite_health_areahp:
                armorValue = np.asarray(sct.grab(self.fortnite_health_areashield))

                lower_white = np.array([255, 255, 255])
                upper_white = np.array([255, 255, 255])
                
                #FOR HP
                img_gray_HP = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img_gray_expanded_HP = cv2.cvtColor(img_gray_HP, cv2.COLOR_GRAY2BGR)
                __, screenHP = cv2.threshold(img_gray_expanded_HP, 240, 255, cv2.THRESH_BINARY)
                
                #FOR ARMOR:
                img_gray_armor = cv2.cvtColor(armorValue, cv2.COLOR_BGR2GRAY)
                img_gray_expanded_armor = cv2.cvtColor(img_gray_armor, cv2.COLOR_GRAY2BGR)
                __, screenArmor = cv2.threshold(img_gray_expanded_armor, 200, 255, cv2.THRESH_BINARY)
                
                #FOR TEXT VALUES
                textHP = pytesseract.image_to_string(screenHP, config='--psm 6 -c tessedit_char_whitelist=0123456789')
                textArmor = pytesseract.image_to_string(screenArmor, config='--psm 6 -c tessedit_char_whitelist=0123456789')
                hp=0
                armor=0
                
                if textHP:
                    hp = min(100, max(0, int(textHP)))
                    
                if textArmor:
                    armor = min(100, max(0, int(textArmor)))
                
                if hp + armor <= 200:
                    textInt = hp+ armor
                    text= str(textInt)
                
                #print(text)
                #cv2.imshow("debug", screenHP)              
                #cv2.imshow("debug", screenArmor)              
                
            words = text.split()
            if words and words[0].isdigit():
                self.current_health = int(words[0])

            if self.current_health == 0 and self.last_health != 0:
                self.serial_connector.write(b'death\n\r')
            elif self.current_health < self.last_health and self.last_health != 0:
                self.serial_connector.write(b'loss\n\r')
            self.last_health = self.current_health