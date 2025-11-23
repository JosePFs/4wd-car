import time
from spi_ledpixel import Freenove_SPI_LedPixel

print("Inicializando LEDs del kit Freenove...")

# Crear instancia: 8 LEDs, brillo 50, secuencia GRB, bus SPI 0
strip = Freenove_SPI_LedPixel(
    count=8, bright=50, sequence='GRB', bus=0, device=0)

if strip.check_spi_state() != 0:
    print("✅ SPI inicializado correctamente")
    strip.spi_gpio_info()

    print("\nTest de LEDs individuales:")

    # Apagar todos primero
    strip.set_all_led_color(0, 0, 0)
    time.sleep(0.5)

    # Test cada LED
    for i in range(8):
        print(f"LED {i}: Rojo")
        strip.set_led_color(i, 255, 0, 0)
        time.sleep(0.5)

        print(f"LED {i}: Verde")
        strip.set_led_color(i, 0, 255, 0)
        time.sleep(0.5)

        print(f"LED {i}: Azul")
        strip.set_led_color(i, 0, 0, 255)
        time.sleep(0.5)

        # Apagar
        strip.set_led_color(i, 0, 0, 0)

    print("\nTest completo - todos los LEDs en blanco")
    strip.set_all_led_color(255, 255, 255)
    time.sleep(2)

    # Apagar al final
    strip.set_all_led_color(0, 0, 0)
    strip.led_close()
    print("✅ Test completado")

else:
    print("❌ Error: SPI no inicializado")
    print("Verifica que SPI esté habilitado: sudo raspi-config")
