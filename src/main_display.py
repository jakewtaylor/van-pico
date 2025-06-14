from pimoroni import Button
from pimoroni_bus import SPIBus
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_RGB565
from machine import Pin
# import time

from modules.display.ScreenController import ScreenController
from modules.can.MCP2515 import MCP2515
from modules.can.CANMessager import CANMessager

a_btn = Button(12)
b_btn = Button(13)

spibus = SPIBus(cs=17, dc=16, sck=18, mosi=19)

display = PicoGraphics(
    display=DISPLAY_PICO_DISPLAY_2,
    # maybe remove this (falling back to RGB332) if performance becomes an issue... but the colours are much nicer like this!
    pen_type=PEN_RGB565,
#    bus = spibus
)

screen_controller = ScreenController(a_btn, b_btn, display)

can = MCP2515(
   spi_id = 1,
   sck = Pin(10),
   mosi = Pin(11),
   miso = Pin(8),
   cs_pin_number = 9
)

builder = CANMessager()

print("init...")
can.Init()
id = 0x123 #max 7ff
readbuf = []
while True:
    screen_controller.tick()
    readbuf = can.Receive(id)

    if readbuf is not None:
        print("received: ", readbuf)
        print("received: ", builder.parse_can_message(readbuf))