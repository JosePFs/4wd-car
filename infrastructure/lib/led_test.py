import time
from rpi_ws281x import PixelStrip, Color

LED_COUNT = 1  # Solo primer LED
LED_PIN = 10
LED_BRIGHTNESS = 30  # Bajo
LED_CURRENT = 0
LED_INTERVAL = 3

strip = PixelStrip(LED_COUNT, LED_PIN, 800000, 10, False, LED_BRIGHTNESS, 0)
strip.begin()

print(f"Test LED {LED_CURRENT} - {LED_INTERVAL} seconds each color")

print(f"Red solid")
strip.setPixelColor(LED_CURRENT, Color(255, 0, 0))
strip.show()
time.sleep(LED_INTERVAL)

print(f"Green solid")
strip.setPixelColor(LED_CURRENT, Color(0, 255, 0))
strip.show()
time.sleep(LED_INTERVAL)

print(f"Blue solid")
strip.setPixelColor(LED_CURRENT, Color(0, 0, 255))
strip.show()
time.sleep(LED_INTERVAL)

# Off
print(f"Off")
strip.setPixelColor(LED_CURRENT, Color(0, 0, 0))
strip.show()
