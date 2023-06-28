import mido
import serial
import time


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


arduino_serial = serial.Serial("/dev/cu.usbmodem14401", 9600)

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
