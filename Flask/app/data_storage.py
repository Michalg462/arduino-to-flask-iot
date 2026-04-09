from threading import Lock
import threading
import serial
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

# definition of a communication port with arduino
ser = serial.Serial('COM6', 9600, timeout=1)

# this function will be used by a separate thread to read data from the arduino
def read_parameters():
    while(True):
        command = 'GET\n'
        ser.write(command.encode())
        response =ser.readline().decode('utf-8', errors='ignore').strip()
        print(response)
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