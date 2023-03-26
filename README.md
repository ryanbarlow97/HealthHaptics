# Health Detector
A simple and fancy GUI-based health detector program that interfaces with a hardware device to monitor a user's health in FPS games (with text health). The program detects the health status and sends the relevant information to the connected hardware device.

# Files Overview

gui.py - The main graphical user interface (GUI) file, responsible for creating and updating the GUI. It handles the integration with the health_detector and serial_connector modules.

health_detector.py - Contains the HealthDetector class, which is responsible for detecting the user's health in the game using image processing techniques and pytesseract OCR.

serial_connector.py - Contains the SerialConnector class, which handles the communication with the hardware device using serial communication.

# Usage

Ensure that the required dependencies are installed: dearpygui, numpy, pytesseract, mss, cv2, adafruit_board_toolkit, and serial.
Connect the hardware device to your computer.

Run gui.py to start the GUI, and the program will automatically detect and connect to the hardware device.

The GUI will display the current health status, and the hardware device will react to health changes as the user plays the game.

If the hardware device is not connected or recognized, click the "Retry" button to attempt reconnection.
