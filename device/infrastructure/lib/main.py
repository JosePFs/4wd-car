import time

from servo import Servo
from ultrasonic import Ultrasonic
from motor import Ordinary_Car
from buzzer import Buzzer
from spi_ledpixel import Freenove_SPI_LedPixel


def test_Led():
    try:
        print("Led test starting ...")
        strip = Freenove_SPI_LedPixel(count=4)
        strip.set_all_led_color_data(0, 0, 0)
        strip.show(2)
        time.sleep(1)
        strip.set_led_color(0, 255, 0, 0)
        time.sleep(1)
        strip.set_led_color(0, 0, 255, 0)
        time.sleep(1)
        strip.set_led_color(0, 0, 0, 255)
        time.sleep(1)
        strip.set_led_color(0, 255, 255, 255)
        time.sleep(1)
        print("Led test finished")
    except KeyboardInterrupt:
        print("Led test interrupted by user")
    except Exception as e:
        print(f"Led test error: {e}")
    finally:
        strip.led_close()
        print("Led test stopped")


def test_Motor():
    try:
        print("Motor test starting ...")
        motors = Ordinary_Car()
        motors.set_motor_model(750, 750, 750, 750)
        time.sleep(1)
        motors.set_motor_model(-750, -750, -750, -750)
        time.sleep(1)
        motors.set_motor_model(-750, -750, 1500, 1500)
        time.sleep(1)
        motors.set_motor_model(1500, 1500, -750, -750)
        time.sleep(1)
        motors.set_motor_model(0, 0, 0, 0)
        print("Motor test finished")
    except KeyboardInterrupt:
        print("Motor test interrupted by user")
    except Exception as e:
        print(f"Motor test error: {e}")
    finally:
        motors.close()
        print("Motor test stopped")


def test_Ultrasonic():
    try:
        print("Ultrasonic test starting ...")
        ultrasonic = Ultrasonic()
        while True:
            distance = ultrasonic.get_distance()
            if distance is not None:
                print(f"Ultrasonic distance: {distance}cm")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Ultrasonic test interrupted by user")
    except Exception as e:
        print(f"Ultrasonic test error: {e}")
    finally:
        ultrasonic.close()
        print("Ultrasonic test stopped")


def test_Servo():
    try:
        print("Servo test starting ...")
        servo = Servo()
        while True:
            for i in range(50, 110, 1):
                servo.set_servo_pwm('0', i)
                time.sleep(0.01)
            for i in range(110, 50, -1):
                servo.set_servo_pwm('0', i)
                time.sleep(0.01)
            for i in range(80, 150, 1):
                servo.set_servo_pwm('1', i)
                time.sleep(0.01)
            for i in range(150, 80, -1):
                servo.set_servo_pwm('1', i)
                time.sleep(0.01)
    except KeyboardInterrupt:
        print("Servo test interrupted by user")
    except Exception as e:
        print(f"Servo test error: {e}")
    finally:
        servo.set_servo_pwm('0', 90)
        servo.set_servo_pwm('1', 90)
        print("Servo test stopped")


def test_Buzzer():
    try:
        print("Buzzer test starting ...")
        buzzer = Buzzer()
        buzzer.set_state(True)
        time.sleep(1)
        print("1 second passed")
        time.sleep(1)
        print("2 seconds passed")
        time.sleep(1)
        print("3 seconds passed")
        buzzer.set_state(False)
        print("Buzzer test finished")
    except KeyboardInterrupt:
        buzzer.set_state(False)
    except Exception as e:
        print(f"Buzzer test error: {e}")
    finally:
        buzzer.close()
        print("Buzzer test stopped")


if __name__ == '__main__':
    import sys

    print('Program is starting ... ')

    if len(sys.argv) < 2:
        print("Parameter error: Please assign the device")
        exit()

    match sys.argv[1]:
        case 'Led':
            test_Led()
            exit()
        case 'Motor':
            test_Motor()
            exit()
        case 'Ultrasonic':
            test_Ultrasonic()
            exit()
        case 'Servo':
            test_Servo()
            exit()
        case 'Buzzer':
            test_Buzzer()
            exit()
        case _:
            print("Parameter error: Please assign the device")
            exit()
