import time, struct
import board
import digitalio as dio
from busio import SPI
from adafruit_circuitpython_nrf24l01 import NRF24L01

pipes = (b'\x01\x02\x03\x04\x00', b'\x01\x02\x03\x04\x01')

cs = dio.DigitalInOut(board.D6)
ce = dio.DigitalInOut(board.D5) # TODO Remove this, tie low?

cs.direction = dio.Direction.OUTPUT
ce.direction = dio.Direction.OUTPUT

spi = SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
nrf = NRF24L01(spi, cs, ce, channel=0, payload_size=3)
