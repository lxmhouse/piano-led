# works on linux

import subprocess
import serial
import time
import re

import serial.tools.list_ports


def stream():
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
    print("Sending")
    note = ",".join(str(n) for n in notes) + "\n"
    note_bytes = str(note).encode("utf-8")
    arduino_serial.write(note_bytes)


def get_arduino_serial():
    ports = serial.tools.list_ports.comports()

    # pick the port where port[2]!='n/a'
    arduino_port = next((port for port in ports if port[2] != "n/a"), None)
    if arduino_port is None:
        print("Arduino not found.")
        return None
    else:
        print(f"Arduino found: {arduino_port}")
        return serial.Serial(arduino_port[0], 9600)


arduino_serial = get_arduino_serial()
if arduino_serial is None:
    exit()

stream()
