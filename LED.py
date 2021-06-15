from neopixel import *
import time

LED_COUNT = 4
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0
LED_STRIP = ws.WS2812_STRIP
def LED():

    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

    strip.begin()

    red, green, blue = 200, 100, 150
    color = (red << 16) |(green << 8) | blue
    for x in range(4):
        strip.setPixelColor(x, color)

    strip.show()

    time.sleep(2)
    strip.setBrightness(128)
    strip.show()
