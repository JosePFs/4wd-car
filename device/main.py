import logging

from infrastructure import build_application

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.info("Demo started")

    app = build_application()

    try:
        app.run()

        app.obstacles_detector_toggle_on_off()
        app.obstacles_detector_detect()
        app.obstacles_detector_toggle_on_off()
        app.car_move_forward()
        app.car_turn_right()
        app.car_stop()
        app.car_toggle_on_off()

    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        logger.info("Demo ended")