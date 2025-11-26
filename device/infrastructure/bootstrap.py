import logging
from logging import Logger
from queue import Queue

from domain import Car, ObstaclesDetector
from application import Application
from infrastructure import Motors, Leds, Buzzer, Ultrasonic, Servo


def build_application() -> Application:
    motors = Motors()
    leds = Leds()
    buzzer = Buzzer()
    car = Car(motors, leds, buzzer)
    obstacles_detector = ObstaclesDetector(Ultrasonic(), Servo())
    return Application(car, obstacles_detector)
