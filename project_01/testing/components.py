import time
import board
import busio
import adafruit_ssd1306
import Adafruit_BBIO.PWM as PWM
from PIL import Image, ImageDraw, ImageFont

i2c = busio.I2C(board.SCL_2, board.SDA_2)
print(board.SCL_2, board.SDA_2)
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
print(disp)

disp.fill(0)
disp.show()

width = disp.width
height = disp.height
image = Image.new("1", (width, height))

draw = ImageDraw.Draw(image)

padding = -2
top = padding
bottom = height - padding

x = 0

font = ImageFont.truetype('Oswald-Regular.ttf', 30)

draw.text((0, top), 'X+Y=Z', font=font, fill = 255)
disp.image(image)
disp.show()

PWM.start("P2_1", 75, 2000)
PWM.set_frequency("P2_1", 10)
time.sleep(0.4)
PWM.stop("P2_1")

#disp.fill(0)
disp.show()