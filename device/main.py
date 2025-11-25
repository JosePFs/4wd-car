import logging

from infrastructure import build_application
from application import CarMoveForwardCommand, CarTurnRightCommand, CarStopCommand, CarTurnOffCommand, ObstaclesDetectorDetectCommand, ObstaclesDetectorTurnOnCommand, ObstaclesDetectorTurnOffCommand

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    app = build_application()

    try:
        app.run()

        app.queue_obstacles_detector_command(ObstaclesDetectorTurnOnCommand())
        app.queue_obstacles_detector_command(ObstaclesDetectorDetectCommand())
        app.queue_obstacles_detector_command(ObstaclesDetectorTurnOffCommand())
        app.queue_car_command(CarMoveForwardCommand())
        app.queue_car_command(CarTurnRightCommand())
        app.queue_car_command(CarStopCommand())
        app.queue_car_command(CarTurnOffCommand())

    except Exception as e:
        logging.error(f"Error: {e}")
