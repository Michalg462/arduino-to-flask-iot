from threading import Lock
import threading

from serial import Serial
from serial.tools import list_ports
import time

# this class holds the information that were collected from arduino
class DataStorage:

    def __init__(self):
        self.lock = Lock()
        self.data = {
            "temperature" : None,
            "humidity" : None
        }

    # allows for update of data inside the object
    def update(self, **kwargs):
        with self.lock:
            self.data.update(kwargs)

    # returns the object data as a dictionary
    def get(self):
        with self.lock:
            return dict(self.data)

# creating a shared instance of the class
data_store = DataStorage()

# This function is used to auto-detect connected arduino boards
def detect_arduino():

    # gets the list of available ports, throws runtime error if none found
    try:
        ports = list_ports.comports()
    except Exception as e:
        raise RuntimeError(f"No arduino port found: {e}")

    # for every available port load it's data and compare it with given keywords
    for port in ports:
        desc = (port.description or "").lower()
        hwid = (port.hwid or "").lower()

        search_phrase = [
            "arduino",
            "ch340",
            "wchusb",
            "cdc",
            "usb serial",
            "mega",
            "uno",
            "nano"
        ]

        # if the port data matches key word, return it as a connection port
        for phrase in search_phrase:
            if (phrase in desc) or (phrase in hwid):
                return port

    # If no matching port has beed found, throw runtime error
    raise RuntimeError("No arduino port found")



# this function will be used by a separate thread to read data from the arduino
def read_parameters():

    # definition of a communication port with arduino
    port = detect_arduino()
    ser = Serial(port.device, 9600, timeout=1)

    while(True):
        command = 'GET\n'
        ser.write(command.encode())
        response =ser.readline().decode('utf-8', errors='ignore').strip()
        if response:
            readings = response.split(';')
            data_store.update(temperature=readings[0], humidity=readings[1])
        time.sleep(5)

# function that sets up the thread reading data from arduino
def start_comm_thread():
    if getattr(start_comm_thread, "started", False):
        return
    start_comm_thread.started = True
    t = threading.Thread(target=read_parameters, daemon=True)
    t.start()