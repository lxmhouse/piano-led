import subprocess
import serial
import re
import time

import serial.tools.list_ports
from serial.serialutil import SerialException

def get_device_id():
    command = ["amidi", "-l"]
    try:
        output = subprocess.check_output(command).decode("utf-8")
        lines = output.split("\n")
        for line in lines:
            if "Roland Digital Piano MIDI 1" in line:
                parts = line.split()
                return parts[1]  # Return the device ID
    except subprocess.CalledProcessError:
        print("Failed to get MIDI device ID.")
    return None

def stream(devices):
    print("Reading MIDI messages. Press Ctrl+C to stop.")
    current_notes = []
    pitch_bend = 0

    # Get the device ID
    device_id = get_device_id()
    if device_id is None:
        print("Failed to get MIDI device ID, using default 'hw:1,0,0'.")
        device_id = "hw:1,0,0"
    command = ["aseqdump", "-p", device_id]

    # Start the process
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        print("Could not start process:", e)
        return

    while True:
        # while process.poll() is not None:
        #     print("Piano is off...attempting to reconnect, poll is ", process.poll())
        #     process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #     time.sleep(1)

        try:
            output = process.stdout.readline().decode("utf-8")
            if output:
                if "Note on" in output:
                    velocity = int(re.search(r"velocity (\d+)", output).group(1))
                    note = int(re.search(r"note (\d+)", output).group(1))
                    if velocity > 0:
                        current_notes += [note]
                        for device in devices:
                            send_notes(current_notes, device)
                elif "Note off" in output:
                    note = int(re.search(r"note (\d+)", output).group(1))
                    if note in current_notes:
                        current_notes.remove(note)
                if len(current_notes) != 0:
                    print(current_notes)       
        except Exception as e:
            print(e)
            print("Connection to Cloud/LED lost...attempting to reconnect")
            # process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            cloud_device = get_arduino_serial("cloud")
            led_device = get_arduino_serial("led")
            if cloud_device is None:
                print("Cloud off. Waiting.")
            if led_device is None:
                print("LED off. Waiting.")
            while cloud_device is None and led_device is None:
                cloud_device = get_arduino_serial("cloud")
                led_device = get_arduino_serial("led")
                time.sleep(1)

def send_notes(notes, device):
    """
    Send notes to Arduino via serial with throttling.
    """
    try:
        note = ",".join(str(n) for n in notes) + "\n"
        note_bytes = str(note).encode("utf-8")
        device.write(note_bytes)
        print('Sent note bytes to arduino!')
    except Exception as e:
        print("Could not send notes to device", e)


def get_arduino_serial(device_id):
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(f"Device: {port.device}, Description: {port.description}")

    if device_id == "cloud":
        arduino_port = "/dev/ttyACM0"
    else:  # led
        arduino_port = "/dev/ttyUSB0"
        
    try:
        print("Connecting to Arduino at port", arduino_port)
        ser = serial.Serial(arduino_port, 9600)
        print(f"Arduino found: {arduino_port}")
        return ser
    except SerialException:
        print(f"Arduino not found at port {arduino_port}.")
        return None
    except Exception as e:
        print(f"Arduino not found at port {arduino_port}, Exception occurred: {e}")
        return None


def main():
    cloud_device = get_arduino_serial("cloud")
    led_device = get_arduino_serial("led")

    if cloud_device is None and led_device is None:
        print("No devices found.")
        return
    elif cloud_device is None:
        print("Only led device found.")
        stream([led_device])
    elif led_device is None:
        print("Only cloud device found.")
        stream([cloud_device])
    else:
        print("Both cloud and led devices found.")
        stream([cloud_device, led_device])


if __name__ == "__main__":
    main()
