import subprocess
import serial
import re

import serial.tools.list_ports


def stream(devices):
    print("Reading MIDI messages. Press Ctrl+C to stop.")
    current_notes = []
    pitch_bend = 0

    # Construct the aseqdump command
    device_id = "20:0"
    command = ["aseqdump", "-p", device_id]

    # Start the process
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        output = process.stdout.readline().decode("utf-8")
        if output:
            if "Note on" in output:
                velocity = int(re.search(r"velocity (\d+)", output).group(1))
                note = int(re.search(r"note (\d+)", output).group(1))
                if velocity > 0:
                    current_notes += [note]
                    send_notes(current_notes)
            elif "Note off" in output:
                note = int(re.search(r"note (\d+)", output).group(1))
                if note in current_notes:
                    current_notes.remove(note)
            if len(current_notes) != 0:
                print(current_notes)


def send_notes(notes):
    """
    Send notes to Arduino via serial with throttling.
    """
    note = ",".join(str(n) for n in notes) + "\n"
    note_bytes = str(note).encode("utf-8")
    cloud_device.write(note_bytes)
    led_device.write(note_bytes)


def get_arduino_serial(device_id):
    if device_id == "cloud":
        arduino_port = "/dev/ttyACM0"
    else:
        arduino_port = "/dev/ttyAMA0"

    if arduino_port is None:
        print("Arduino not found.")
        return None
    else:
        print(f"Arduino found: {arduino_port}")
        return serial.Serial(arduino_port, 9600)


cloud_device = get_arduino_serial("cloud")
led_device = get_arduino_serial("led")

if cloud_device is None and led_device is None:
    print("No devices found.")
    exit()
elif cloud_device is None:
    print("Only led device found.")
    stream([led_device])
elif led_device is None:
    print("Only cloud device found.")
    stream([cloud_device])
else:
    stream([cloud_device, led_device])
