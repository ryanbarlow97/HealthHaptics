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


# Health Detector Hardware

The hardware device is an essential part of the Health Detector system. It interacts with the GUI program to receive and process health status updates from the game, providing feedback to the user in the form of haptic effects.

# Hardware Components

QT Py ESP32-S2 WiFi Dev Board.

Adafruit DRV2605L Haptic Motor.

# Hardware Code

code.py is responsible for managing the hardware components:

Initializes the NeoPixel LED and configures it to show a green color when waiting for input.

Sets up the I2C bus and the DRV2605 Haptic Feedback Motor Driver.

Continuously listens for incoming serial messages and reacts to the health changes:

If the received message is "loss", the motor driver plays a haptic effect (effect 14) to indicate health loss.

If the received message is "death", the motor driver plays a different haptic effect (effect 76) to indicate player death.
