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

ce = dio.DigitalInOut(board.CE0)
# ce = dio.DigitalInOut(board.D8)
cs = dio.DigitalInOut(board.D5)

# spi = SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
spi = board.SPI()
nrf = NRF24L01(spi, cs, ce)

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
            print('send() failed')
        except KeyboardInterrupt: break
        time.sleep(TX_DELAY)
        i += 1

def slave():
    nrf.open_tx_pipe(pipes[1])
    nrf.open_rx_pipe(1, pipes[0])
    nrf.start_listening()

    while True:
        try:
            if nrf.any():
                buf = nrf.recv()
                i = struct.unpack('i', buf)
                print("Received: ", i)
            time.sleep(RX_POLL_DELAY)
        except KeyboardInterrupt: break

print(
    '''
    NRF24L01 test module.
    Pinout:
        CE on D8
        CS on D5
        SPI pins on SPI1

    Run slave() on receiver, and master() on transmitter.
    '''
)
