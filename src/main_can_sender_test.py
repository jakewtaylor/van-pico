from machine import Pin
import time

from modules.can.MCP2515 import MCP2515
from modules.can.CANMessager import CANMessager

can = MCP2515(
    spi_id = 1,
    sck = Pin(10),
    mosi = Pin(11),
    miso = Pin(12),
    cs_pin_number = 13
)

builder = CANMessager()

print("init...")
can.Init()

id = 0x123 #max 7ff

battery_voltage_id = 0x331A
battery_current_id = 0x331B
solar_voltage_id = 0x3100
solar_current_id = 0x3101
solar_power_id = 0x3102

print("Pre loop")

while True:
    voltage_msg = builder.build_can_message(battery_voltage_id, 1378)
    print("sending data", voltage_msg)
    can.Send(id, voltage_msg, 8)

    time.sleep(0.1)

    solar_voltage_msg = builder.build_can_message(solar_voltage_id, 1468)
    print("sending data", solar_voltage_msg)
    can.Send(id, solar_voltage_msg, 8)

    print("waiting...")
    time.sleep(5)