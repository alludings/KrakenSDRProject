import smbus2
import math

LSM6DSOX_ADDR = 0x6A  # default I2C address

class LSM6DSOX:
    def __init__(self, bus=1):
        self.bus = smbus2.SMBus(bus)
        self._init_sensor()

    def _init_sensor(self):
        # Enable accelerometer (example)
        self.bus.write_byte_data(LSM6DSOX_ADDR, 0x10, 0x80)
        # Enable gyro (example)
        self.bus.write_byte_data(LSM6DSOX_ADDR, 0x11, 0x80)

    def read_accel(self):
        # Read 6 bytes of accelerometer data
        data = self.bus.read_i2c_block_data(LSM6DSOX_ADDR, 0x28, 6)
        x = self._twos_complement((data[1]<<8) | data[0], 16)
        y = self._twos_complement((data[3]<<8) | data[2], 16)
        z = self._twos_complement((data[5]<<8) | data[4], 16)
        return x, y, z

    def read_gyro(self):
        data = self.bus.read_i2c_block_data(LSM6DSOX_ADDR, 0x22, 6)
        x = self._twos_complement((data[1]<<8) | data[0], 16)
        y = self._twos_complement((data[3]<<8) | data[2], 16)
        z = self._twos_complement((data[5]<<8) | data[4], 16)
        return x, y, z

    def _twos_complement(self, val, bits):
        if val & (1 << (bits - 1)):
            val -= 1 << bits
        return val
