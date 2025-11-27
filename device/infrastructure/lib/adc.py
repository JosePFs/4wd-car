try:
    import smbus  # Try system smbus first
except ImportError:
    import smbus2 as smbus  # Fallback to smbus2 if system smbus not available
import time  # Import the time module for sleep functionality
# Import the ParameterManager class from the parameter module
from parameter import ParameterManager


class ADC:
    def __init__(self):
        """Initialize the ADC class."""
        self.I2C_ADDRESS = 0x48                                               # Set the I2C address of the ADC
        # Set the command byte for ADS7830
        self.ADS7830_COMMAND = 0x84
        # Create an instance of ParameterManager
        self.parameter_manager = ParameterManager()
        # Get the PCB version
        self.pcb_version = self.parameter_manager.get_pcb_version()
        # Set the ADC voltage coefficient based on the PCB version
        self.adc_voltage_coefficient = 3.3 if self.pcb_version == 1 else 5.2
        # Initialize the I2C bus
        self.i2c_bus = smbus.SMBus(1)

    def _read_stable_byte(self) -> int:
        """Read a stable byte from the ADC."""
        while True:
            # Read the first byte from the ADC
            value1 = self.i2c_bus.read_byte(self.I2C_ADDRESS)
            # Read the second byte from the ADC
            value2 = self.i2c_bus.read_byte(self.I2C_ADDRESS)
            if value1 == value2:
                # Return the value if both reads are the same
                return value1

    def read_adc(self, channel: int) -> float:
        """Read the ADC value for the specified channel using ADS7830."""
        command_set = self.ADS7830_COMMAND | ((((channel << 2) | (
            channel >> 1)) & 0x07) << 4)  # Calculate the command set for the specified channel
        # Write the command set to the ADC
        self.i2c_bus.write_byte(self.I2C_ADDRESS, command_set)
        # Read a stable byte from the ADC
        value = self._read_stable_byte()
        # Convert the ADC value to voltage
        voltage = value / 255.0 * self.adc_voltage_coefficient
        # Return the voltage rounded to 2 decimal places
        return round(voltage, 2)

    def scan_i2c_bus(self) -> None:
        """Scan the I2C bus for connected devices."""
        print("Scanning I2C bus...")                                          # Print a message indicating the start of I2C bus scanning
        # Iterate over possible I2C addresses (0 to 127)
        for device in range(128):
            try:
                # Try to read data from the current device address
                self.i2c_bus.read_byte_data(device, 0)
                # Print the address of the found device
                print(f"Device found at address: 0x{device:02X}")
            except OSError:
                # Ignore any OSError exceptions
                pass

    def close_i2c(self) -> None:
        """Close the I2C bus."""
        self.i2c_bus.close()                                                  # Close the I2C bus


if __name__ == '__main__':
    # Print a message indicating the start of the program
    print('Program is starting ... ')
    # Create an instance of the ADC class
    adc = ADC()
    try:
        while True:
            # Read the left photoresistor value
            left_idr = adc.read_adc(0)
            # Read the right photoresistor value
            right_idr = adc.read_adc(1)
            # Calculate the power value based on the PCB version
            power = adc.read_adc(2) * (3 if adc.pcb_version == 1 else 2)
            # Print the values of left IDR, right IDR, and power
            print(
                f"Left IDR: {left_idr}V, Right IDR: {right_idr}V, Power: {power}V")
            # Wait for 1 second
            time.sleep(1)
    except KeyboardInterrupt:
        # Close the I2C bus when the program is interrupted
        adc.close_i2c()
