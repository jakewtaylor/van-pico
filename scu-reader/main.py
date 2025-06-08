import time
from machine import Pin
from umodbus.serial import Serial
import struct

def extract_bits(data: int, start_bit: int, number_of_bits: int):
    mask = number_of_bits << start_bit
    result = data & mask
    shifted_result = result >> start_bit
    return shifted_result

def read_input_registers(starting_address: int, quantity: int) -> bytes:
    """
    Create Modbus Protocol Data Unit for reading input registers.

    :param      starting_address:  The starting address
    :type       starting_address:  int
    :param      quantity:          Quantity of coils
    :type       quantity:          int

    :returns:   Packed Modbus message
    :rtype:     bytes
    """
    if not (1 <= quantity <= 125):
        raise ValueError('Invalid number of input registers')

    print(f"Packing using >BHH:\nfunc - {0x04}\nstarting_address: {starting_address}\nquantity: {quantity}")
    return struct.pack('>BHH', 0x04, starting_address, quantity)

def to_short(byte_array: bytes, signed: bool = True):
    """
    Convert bytes to tuple of integer values

    :param      byte_array:  The byte array
    :type       byte_array:  bytes
    :param      signed:      Indicates if signed
    :type       signed:      bool

    :returns:   Integer representation
    :rtype:     bytes
    """
    response_quantity = int(len(byte_array) / 2)
    fmt = '>' + (('h' if signed else 'H') * response_quantity)

    return struct.unpack(fmt, byte_array)


class Scu():
    battery_voltage_control_register_names = [
        "over_voltage_disconnect_voltage",
        "charging_limit_voltage",
        "over_voltage_reconnect_voltage",
        "equalize_charging_voltage",
        "boost_charging_voltage",
        "float_charging_voltage",
        "boost_reconnect_charging_voltage",
        "low_voltage_reconnect_voltage",
        "under_voltage_recover_voltage",
        "under_voltage_warning_voltage",
        "low_voltage_disconnect_voltage",
        "discharging_limit_voltage"
    ]

    def __init__(self, uart_id: int, tx: Pin, rx: Pin, ctrl: int, slave_address: int, baud_rate = 115200) -> None:
        self.slave_address = slave_address
        self.host = Serial(
            baudrate = baud_rate,
            data_bits = 8,
            stop_bits = 1,
            parity = None,
            pins = (tx, rx),
            ctrl_pin = ctrl,
            uart_id = uart_id
        )
    
    def read_registers(self, address: int, signed: bool = False):
        print(f"uart any {self.host._uart.any()}")
        modbus_pdu = read_input_registers(address, 1)
        print(f"generated modbus pdu: {modbus_pdu}")

        modbus_adu = bytearray()
        modbus_adu.append(self.slave_address)
        modbus_adu.extend(modbus_pdu)
        modbus_adu.extend(self.host._calculate_crc16(modbus_adu))

        print(f"full modbus_adu: {modbus_adu}")

        response = self.host._send_receive(slave_addr=self.slave_address,
                                      modbus_pdu=modbus_pdu,
                                      count=True)

        register_value = to_short(byte_array=response, signed=signed)

        return register_value

        # return self.host.read_input_registers(
        #     slave_addr = self.slave_address,
        #     starting_addr = address,
        #     register_qty = 1,
        #     signed = signed
        # )

    def read_register(self, address: int, decimals: int = 0, signed: bool = False):
        value, = self.read_registers(address, signed)
        print("got value: " + str(value) + " and decimals is given as: " + str(decimals) + " but we're not using that yet")
        return value

    def read_long(self, address: int, decimals: int = 0, signed: bool = False):
        return self.read_register(address, decimals, signed)

    # def read_bit(self, address: int, decimals: int = 0):
    #     return self.host.read_discrete_inputs(
    #         slave_addr = SLAVE_ADDRESS,
    #         starting_addr = address,
    #         input_qty = decimals
    #     )

    def get_solar_voltage(self):
        """PV array input in volts"""
        return self.read_register(address = 0x3100, decimals = 2)

    def get_solar_current(self):
        """PV array input in amps"""
        return self.read_register(address = 0x3101, decimals = 2)

    def get_solar_power(self):
        """PV array input power in watts"""
        return self.read_long(address = 0x3102, decimals = 2) / 100

    def get_battery_voltage(self):
        """Battery voltage in volts"""
        return self.read_register(address = 0x331A, decimals = 2)
    
    def get_battery_current(self):
        """Battery current in amps"""
        return self.read_long(address = 0x331B, decimals = 2, signed=True) / 100

    # The docs for my controller in the PDF in this repo don't document anything at the 0x3106 address
    # def get_battery_power(self):
    #     """Battery power in watts"""
    #     return self.read_long(address = 0x3106, decimals = 4) / 100

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
