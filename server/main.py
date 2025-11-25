import logging

from config_common import Command, Env
from udp_server import UDPServer, UDPPort

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    try:
        env = Env().load()
        udp_server = UDPServer(UDPPort(env.udp_port))
        udp_server.start()
        while True:
            command = udp_server.receive()
            match command:
                case Command.FORWARD:
                    logger.info("Forward")
                case Command.BACKWARD:
                    logger.info("Backward")
                case Command.LEFT:
                    logger.info("Left")
                case Command.RIGHT:
                    logger.info("Right")
                case Command.STOP:
                    logger.info("Stop")
                case Command.TOGGLE_CAR_ON_OFF:
                    logger.info("Toggle car on off")
                case Command.TOGGLE_OBSTACLE_DETECTION_ON_OFF:
                    logger.info("Toggle obstacle detection on off")
                case _:
                    continue
    except KeyboardInterrupt:
        logger.info("Closing...")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        logger.info("Exiting...")
