import logging

from config_common import Command, Env
from udp_server import UDPServer, UDPPort
from device import build_application

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    try:
        env = Env().load()
        udp_server = UDPServer(UDPPort(env.udp_port))
        udp_server.start()
        app = build_application()
        while True:
            command = udp_server.receive()
            match command:
                case Command.FORWARD:
                    logger.info("Forward")
                    app.car_move_forward()
                case Command.BACKWARD:
                    logger.info("Backward")
                    app.car_move_backward()
                case Command.LEFT:
                    logger.info("Left")
                    app.car_turn_left()
                case Command.RIGHT:
                    logger.info("Right")
                    app.car_turn_right()
                case Command.STOP:
                    logger.info("Stop")
                    app.car_stop()
                case Command.TOGGLE_CAR_ON_OFF:
                    logger.info("Toggle car on off")
                    app.car_toggle_on_off()
                case Command.TOGGLE_OBSTACLE_DETECTION_ON_OFF:
                    logger.info("Toggle obstacle detection on off")
                    app.obstacles_detector_toggle_on_off()
                case _:
                    continue
    except KeyboardInterrupt:
        logger.info("Closing...")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        logger.info("Exiting...")
