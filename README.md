# Piano LED
## Installation
We run the python file on a Raspberry Pi that is hooked up to an Arduino.

### Arduino
- for LED strip, install Arduino library `<Adafruit_NeoPixel.h>`
- for cloud, `<IRremote.h>`

### Pi
```
pip install pyserial mido python-rtmidi
```

Then run

```
python main.py
```

### LXM Deployment

Dm Anna/Aayush/Raffi for the ssh password.
```
ssh lxm@192.168.4.224
nohup python main.py &
```