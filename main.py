import mido
import serial
import time

import serial.tools.list_ports


def stream(inport):
    print("Reading MIDI messages. Press Ctrl+C to stop.")
    current_notes = set()
    pitch_bend = 0
    for msg in inport:
        if msg.type == "clock":
            continue
        elif msg.type == "note_on":
            if msg.velocity > 0:
                current_notes.add(msg.note)
                send_notes(current_notes)
            elif msg.note in current_notes:
                current_notes.remove(msg.note)
        elif msg.type == "pitchwheel":
            pitch_bend = msg.pitch
        if len(current_notes) != 0:
            print(current_notes, "pitch: ", pitch_bend)


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


ports = mido.get_input_names()
print("All available MIDI ports:")
for port in ports:
    print(port)

yamaha_port = next((port for port in ports if "YAMAHA" in port), None)
if yamaha_port is None:
    print("Yamaha piano not found.")
else:
    print(f"Yamaha piano found: {yamaha_port}")

    with mido.open_input(yamaha_port) as inport:
        stream(inport)
