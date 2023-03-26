import supervisor
import neopixel
import board
import adafruit_drv2605
import busio


pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
i2c = busio.I2C(board.SCL1, board.SDA1)

drv = adafruit_drv2605.DRV2605(i2c)

while True:
    
    if supervisor.runtime.serial_bytes_available:
        value = input().strip()
        if value == "loss":
            drv.sequence[0] = adafruit_drv2605.Effect(14)
            drv.play()     
        if value == "death":
            drv.sequence[0] = adafruit_drv2605.Effect(76) 
            drv.play()
            
    else:
        pixel.fill((0, 10 , 0)) #green when waiting      