### Typings

Run this command to install the pimoroni pico stubs into the typings folder for autocompletion

```
pip3 install pimoroni-pico-stubs --target ./typings --no-user
```

and another one for the umodbus typings:

```
pip3 install git+https://github.com/brainelectronics/micropython-modbus --target ./typings --no-user
```

### Install `umodbus` on a connected board

1. Find the address it's mounted at on your machine (right now mine is `/dev/cu.usbmodem42123101`)
1. Install `mpremote` (I used `brew install pipx && pipx install mpremote`)
1. Run this command to install umodbus on the board:
   ```
   mpremote connect /dev/cu.usbmodem42123101 mip install github:brainelectronics/micropython-modbus
   ```
