import dearpygui.dearpygui as dpg
from health_detector import HealthDetector
from serial_connector import SerialConnector

# Create an instance of SerialConnector
serial_connector = SerialConnector(None, 115200)
serial_connected = serial_connector.connect()

# Create an instance of HealthDetector, passing in the SerialConnector instance (to write when health changes)
health_detector = HealthDetector(serial_connector)

class GUI:
    def __init__(self):
        self.serial_connected = serial_connected
        
        dpg.create_context()

        with dpg.window(tag="Health Detector") as window:
            with dpg.group(horizontal=True):
                dpg.add_text("Status:")
                dpg.add_text("Connected", tag="connect_status")
            dpg.add_button(label="Retry", tag="retry_button", show=False, callback=self.retry_callback)
            with dpg.group(horizontal=True):
                dpg.add_text("Health:", tag="health_text", show=False)
                dpg.add_text("0", tag="health_label", show=False)
            if self.serial_connected:
                dpg.set_value("connect_status", value="Connected")
                dpg.configure_item("health_text", show=True)
                dpg.configure_item("health_label", show=True)

            else:
                dpg.configure_item("retry_button", show=True, label="Retry")
                dpg.set_value("connect_status", value="Not connected. Please plug in the board.")

        dpg.create_viewport(title='Health Detector', width=400, height=200, resizable=False, max_height=200, max_width=400)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("Health Detector", True)

        while dpg.is_dearpygui_running():
            health_detector.detect_health()
            self.update_gui()
            dpg.render_dearpygui_frame()

        serial_connector.disconnect()
        dpg.destroy_context()

    def update_gui(self):
        dpg.set_value("health_label", health_detector.current_health)

    def retry_callback(self):
        if not self.serial_connected:
            self.serial_connected = serial_connector.connect()
        if self.serial_connected:
            dpg.set_value("connect_status", value="Connected")
            dpg.configure_item("retry_button", show=False)
            dpg.configure_item("health_text", show=True)
            dpg.configure_item("health_label", show=True)
        else:
            dpg.configure_item("retry_button", show=True, label="Retry (Failed)")
