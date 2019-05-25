'''
    Simple example of library usage.

    Master transmits an incrementing integer every second. Receiver polls the
    radio every 0.5s and prints the received value.

    This is a simple test to get communications up and running. For additional
    features such as ACK and timeouts, please refer to the original micropython
    driver test:

    https://github.com/micropython/micropython/blob/master/drivers/nrf24l01/nrf24l01test.py
'''

import time, struct
import board
import digitalio as dio
from busio import SPI
from adafruit_circuitpython_nrf24l01 import NRF24L01

pipes = (b'\x01\x02\x03\x04\x00', b'\x01\x02\x03\x04\x01')

ce = dio.DigitalInOut(board.D5)
cs = dio.DigitalInOut(board.D6)

cs.direction = dio.Direction.OUTPUT
ce.direction = dio.Direction.OUTPUT

spi = SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
nrf = NRF24L01(spi, cs, ce, channel=0, payload_size=1)

TX_DELAY      = 1
RX_POLL_DELAY = 0.5

def master():
    nrf.open_tx_pipe(pipes[0])
    nrf.open_rx_pipe(1, pipes[1])
    nrf.stop_listening()

    i = 0

    while True:
        try:
            print("Sending: ", i)
            nrf.send(struct.pack('i', i))
        except OSError:
            pass
        time.sleep(TX_DELAY)

def slave():
    nrf.open_tx_pipe(pipes[1])
    nrf.open_rx_pipe(1, pipes[0])
    nrf.start_listening()

    while True:
        if nrf.any():
            while nrf.any():
                buf = nrf.recv()
                i = sutrct.unpack('i', buf)
                print("Received: ", i)
                time.sleep(RX_POLL_DELAY)

print(
    '''
    NRF24L01 test module.
    Pinout:
        CE on D5
        CS on D6
        SPI pins on SPI1

    Run nrf24l01_simpletest.slave() on receiver, and nrf24l01_simpletest.master() on transmitter.
    '''
)
