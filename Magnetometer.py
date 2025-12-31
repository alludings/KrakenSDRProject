import smbus2
import math
import time

MMC5603_ADDR = 0x30

class MMC5603:
    def __init__(self, bus=1):
        self.bus = smbus2.SMBus(bus)

        # Calibration values (example placeholders)
        self.x_offset = 0
        self.y_offset = 0
        self.x_scale = 1.0
        self.y_scale = 1.0

        self._init_sensor()

    def _init_sensor(self):
        # Continuous measurement mode
        self.bus.write_byte_data(MMC5603_ADDR, 0x1B, 0x01)

    def read_raw(self):
        data = self.bus.read_i2c_block_data(MMC5603_ADDR, 0x00, 6)
        x = (data[0] << 8) | data[1]
        y = (data[2] << 8) | data[3]
        z = (data[4] << 8) | data[5]
        return x, y, z

    def read_heading(self):
        x, y, _ = self.read_raw()

        # Apply calibration
        x = (x - self.x_offset) * self.x_scale
        y = (y - self.y_offset) * self.y_scale

        heading = math.degrees(math.atan2(y, x))
        if heading < 0:
            heading += 360

        return heading
