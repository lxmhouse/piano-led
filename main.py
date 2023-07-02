import argparse
import subprocess
import serial
import re

import serial.tools.list_ports


def stream(device):
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
                    send_notes(current_notes, device)
            elif "Note off" in output:
                note = int(re.search(r"note (\d+)", output).group(1))
                if note in current_notes:
                    current_notes.remove(note)
            if len(current_notes) != 0:
                print(current_notes)


def send_notes(notes, device):
    """
    Send notes to Arduino via serial with throttling.
    """
    note = ",".join(str(n) for n in notes) + "\n"
    note_bytes = str(note).encode("utf-8")
    device.write(note_bytes)


def get_arduino_serial(device_id):
    if device_id == "cloud":
        arduino_port = "ttyACM0"
    else:
        arduino_port = "ttyAMA0"

    if arduino_port is None:
        print("Arduino not found.")
        return None
    else:
        print(f"Arduino found: {arduino_port}")
        return serial.Serial(arduino_port, 9600)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--device",
        type=str,
        default="led",
        help="The device to stream to (cloud or led)",
    )
    args = parser.parse_args()
    device = get_arduino_serial(args.device)
    if device is None:
        exit()
    stream(device)


if __name__ == "__main__":
    main()
