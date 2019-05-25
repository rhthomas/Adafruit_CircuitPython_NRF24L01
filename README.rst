Adafruit_CircuitPython_NRF24L01
===============================

.. image:: https://travis-ci.org/rhthomas/Adafruit_CircuitPython_NRF24L01.svg?branch=master
    :target: https://travis-ci.org/rhthomas/Adafruit_CircuitPython_NRF24L01
    :alt: Build Status

.. image:: https://readthedocs.org/projects/circuitpython-nrf24l01/badge/?version=latest
    :target: https://circuitpython-nrf24l01.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Dependencies
============

This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Usage Example
=============

See `examples/` for an example of how to use the library.

Firstly import the necessary packages for your application.

.. code-block:: python

    import time
    import struct # transmitted packet must be a byte array
    import board
    import digitalio as dio
    from busio import SPI
    from adafruit_circuitpython_nrf24l01 import NRF24L01 # this library

Define the communication pipes (effectively device addresses/IDs) and the SPI connections to the radio.

.. code-block:: python

    pipes = (b'\x01\x02\x03\x04\x00', b'\x01\x02\x03\x04\x01') # tx, rx node ID's

    ce = dio.DigitalInOut(board.D5)
    ce.direction = dio.Direction.OUTPUT
    cs = dio.DigitalInOut(board.D6)
    cs.direction = dio.Direction.OUTPUT

    spi = SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO) # create instance of spi port
    nrf = NRF24L01(spi, cs, ce, channel=0, payload_size=1) # create instance of the radio

To transmit firstly open the TX and RX pipes, stop listening (puts radio in transmit mode) and send your packet (`buf`).

.. code-block:: python

    def radio_tx():
        nrf.open_tx_pipe(pipes[0])
        nrf.open_rx_pipe(1, pipes[1])
        nrf.stop_listening()

        i = 0

        while True:
            try:
                print("Sending: ", i)
                nrf.send(struct.pack('i', i)) # be sure to pack data in byte array
            except OSError:
                pass
            time.sleep(1) # send every 1s

To receive this data, again open the TX and RX pipes and start listening for data. The `nerf.any()` method returns true when there is data ready to be received.

.. code-block:: python

    def radio_rx():
        nrf.open_tx_pipe(pipes[1])
        nrf.open_rx_pipe(1, pipes[0])
        nrf.start_listening()

        while True:
            if nrf.any():
                while nrf.any():
                    buf = nrf.recv()
                    i = sutrct.unpack('i', buf) # byte array formats (`i`) must match
                    print("Received: ", i)
                    time.sleep(0.5) # poll every 0.5s for new data

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
