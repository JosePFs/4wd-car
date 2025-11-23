from infrastructure.lib.led import Led as LibLed

from domain import Leds as DomainLeds, CarNavigationType


class Leds(DomainLeds):
    def __init__(self) -> None:
        super().__init__()
        self.leds = LibLed()

    def turn_off(self) -> None:
        self.leds.colorBlink(0)

    def on_navigation_mode_transition(self, car_navigation_type: CarNavigationType) -> None:
        match car_navigation_type:
            case CarNavigationType.NORMAL:
                self.set_green()
            case CarNavigationType.OBSTACLE_DETECTED:
                self.set_red()

    def set_green(self) -> None:
        self.leds.ledIndex(0, 0, 255, 0)

    def set_red(self) -> None:
        self.leds.ledIndex(0, 255, 0, 0)
