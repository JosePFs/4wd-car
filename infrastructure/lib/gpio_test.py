import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(10, GPIO.OUT)
GPIO.output(10, GPIO.HIGH)

input("Mide GPIO 10 (pin 19) a GND, presiona Enter cuando termines...")
GPIO.cleanup()
