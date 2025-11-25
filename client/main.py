import logging

from config_common import Command, Env
from udp_client import UDPClient, UDPTarget
from keyboard_controller import KeyboardController
from event_handler import EventHandler
from event import UpPressedEvent, DownPressedEvent, LeftPressedEvent, RightPressedEvent, SpacePressedEvent, ShiftPressedEvent, EscapePressedEvent

logging.basicConfig(level=logging.INFO)    

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.info("Starting...")

    env = Env().load()
    udp_client = UDPClient(UDPTarget(env.udp_host, env.udp_port))
    event_handler = EventHandler()
    event_handler.add_callback(UpPressedEvent, lambda event: udp_client.send(Command.FORWARD))
    event_handler.add_callback(DownPressedEvent, lambda event: udp_client.send(Command.BACKWARD))
    event_handler.add_callback(LeftPressedEvent, lambda event: udp_client.send(Command.LEFT))
    event_handler.add_callback(RightPressedEvent, lambda event: udp_client.send(Command.RIGHT))
    event_handler.add_callback(SpacePressedEvent, lambda event: udp_client.send(Command.TOGGLE_CAR_ON_OFF))
    event_handler.add_callback(ShiftPressedEvent, lambda event: udp_client.send(Command.TOGGLE_OBSTACLE_DETECTION_ON_OFF))
    event_handler.add_callback(EscapePressedEvent, lambda event: cleanup())
    keyboard_controller = KeyboardController(event_handler)
    
    def cleanup():
        keyboard_controller.stop()
        udp_client.close()

    try:
        keyboard_controller.run()
    except KeyboardInterrupt:
        logger.info("Closing...")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        logger.info("Exiting...")
