import time
from machine import Pin
from modules.SCU import Scu

controller = Scu(ctrl= 3, uart_id=0, tx=Pin(0), rx = Pin(1), slave_address=1)

# Continuous reading loop
while True:
    try:
        print("Real Time Data")
        print(f"Solar voltage: {controller.get_solar_voltage()}V")
        print(f"Solar current: {controller.get_solar_current()}A")
        print(f"Solar power: {controller.get_solar_power()}W")
        print(f"Battery voltage: {controller.get_battery_voltage()}V")
        print(f"Battery current: {controller.get_battery_current()}A")
        # print(f"Battery power: {controller.get_battery_power()}W")

    except Exception as e:
        print('An error occurred:', e)

    # Wait for 5 seconds before the next reading
    time.sleep(5)
