import dearpygui.dearpygui as dpg
from health_detector import HealthDetector
from serial_connector import SerialConnector

# Create an instance of SerialConnector
serial_connector = SerialConnector(None, 115200) # Set the serial port to None, and the baud rate to 115200
serial_connected = serial_connector.connect() # Connect to the serial port

# Create an instance of HealthDetector, passing in the SerialConnector instance (to write when health changes)
health_detector = HealthDetector(serial_connector)

class GUI:
    def __init__(self):
        self.serial_connected = serial_connected # Set the serial_connected variable to the serial_connected variable from the serial_connector.py file

        dpg.create_context()

        with dpg.window(tag="Health Haptics") as window:
            with dpg.group(horizontal=True):
                dpg.add_text("Status:") # The status label
                dpg.add_text("Connected", tag="connect_status") # The status text
            dpg.add_button(label="Retry", tag="retry_button", show=False, callback=self.retry_callback)
            with dpg.group(horizontal=True):
                dpg.add_text("Health:", tag="health_text", show=False) # The health text
                dpg.add_text("0", tag="health_label", show=False) # The health label
            dpg.add_checkbox(label="Haptics Enabled?", tag="haptics_checkbox", default_value=True, callback=self.haptics_callback, show=self.serial_connected)
            dpg.set_item_pos("haptics_checkbox", [10, 180]) # Set the position of the haptics checkbox

            dpg.add_combo(label="", tag="game_selector", show=self.serial_connected, items=["Please Select a Game", "Overwatch", "Rust", "Fortnite", "Counter Strike: GO"], default_value="Please Select a Game", callback=self.game_selected)
            dpg.set_item_pos("game_selector", [200, 10]) # Set the position of the game selector

            if self.serial_connected:
                dpg.set_value("connect_status", value="Connected") # Set the status to connected
                dpg.configure_item("health_text", show=True) # Show the health text when connected
                dpg.configure_item("health_label", show=True) # Show the health label when connected

            else:
                dpg.configure_item("retry_button", show=True, label="Retry") # Show the retry button when not connected
                dpg.set_value("connect_status", value="Not connected. Please plug in the board.") # Set the status to connected

        dpg.create_viewport(title='Health Haptics', width=400, height=200, resizable=False, max_height=200, max_width=400)
        dpg.setup_dearpygui()  
        dpg.show_viewport() 
        dpg.set_primary_window("Health Haptics", True)

        while dpg.is_dearpygui_running():
            health_detector.detect_health()
            self.update_gui()
            dpg.render_dearpygui_frame()

        serial_connector.disconnect() 
        dpg.destroy_context()
        
    def game_selected(self):
        selected_game = dpg.get_value("game_selector")
        if selected_game == "Please Select a Game":
            return
        else:
            dpg.set_item_user_data("game_selector", ["Overwatch", "Rust", "Fortnite", "Counter Strike: GO"])
            health_detector.set_game(selected_game)  # Pass the selected game to HealthDetector

    def update_gui(self):
        dpg.set_value("health_label", health_detector.current_health) # Update the health label

    def retry_callback(self):
        if not self.serial_connected:
            self.serial_connected = serial_connector.connect() # Try to connect to the serial port
        if self.serial_connected:
            dpg.set_value("connect_status", value="Connected") # Set the status to connected
            dpg.configure_item("retry_button", show=False) # Hide the retry button when connected
            dpg.configure_item("health_text", show=True) # Show the health text when connected
            dpg.configure_item("health_label", show=True) # Show the health label when connected
            dpg.configure_item("haptics_checkbox", show=True)  # Show the checkbox when connected
            dpg.configure_item("game_selector", show=True)  # Show the game selector when connected
        else:
            dpg.configure_item("retry_button", show=True, label="Retry (Failed)") # Show the retry button when not connected

    def haptics_callback(self):
        health_detector.haptics_enabled = dpg.get_value("haptics_checkbox") 

