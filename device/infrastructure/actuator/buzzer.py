import time

from ...domain import Buzzer as DomainBuzzer, CarNavigationType
from ..lib.buzzer import Buzzer as LibBuzzer


class Buzzer(DomainBuzzer):

    def __init__(self) -> None:
        super().__init__()
        self.buzzer = LibBuzzer()

    def on_navigation_mode_transition(self, car_navigation_type: CarNavigationType) -> None:
        match car_navigation_type:
            case CarNavigationType.OBSTACLE_DETECTED:
                self.sound_warning()
            case CarNavigationType.EMERGENCY_STOP:
                self.sound_alarm()
            case _:
                self.silence()

    def turn_off(self) -> None:
        self.buzzer.close()

    def sound_warning(self) -> None:
        print("⚠️ Buzzer: Warning tone")
        self.buzzer.set_state(True)
        time.sleep(0.25)
        self.buzzer.set_state(False)
        time.sleep(0.25)

    def sound_alarm(self) -> None:
        print("🚨 Buzzer: ALARM!")
        for _ in range(3):
            self.buzzer.set_state(True)
            time.sleep(0.25)
            self.buzzer.set_state(False)
            time.sleep(0.25)

    def silence(self) -> None:
        print("🔇 Buzzer: Silent")
        self.buzzer.set_state(False)
        time.sleep(0.1)
