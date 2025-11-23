import logging

from infrastructure import build_application
from application import CarMoveForwardCommand, CarTurnRightCommand, CarStopCommand, CarTurnOffCommand

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    app = build_application()

    try:
        app.start()

        app.queue_car_command(CarMoveForwardCommand())
        app.queue_car_command(CarTurnRightCommand())
        app.queue_car_command(CarStopCommand())
        app.queue_car_command(CarTurnOffCommand())

        app.stop()
    except KeyboardInterrupt:
        logging.info("CTRL+C detected")
