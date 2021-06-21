from tkinter import *
from gui import *
import bluetooth
from influxdb import InfluxDBClient
import json
import datetime

print("Searching for devices...")

# SCAN BLUETOOTH DEVICES

print("")
nearby_devices = bluetooth.discover_devices()
num = 0
print("Select your device by entering it's corresponding number...")

########### RECEIVING DATA #########################

sensor_address = '07:12:05:15:60:07'
socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
socket.connect((sensor_address, 1))

influx = InfluxDBClient('localhost', 8086, 'root', 'root', 'example')
influx.create_database('datas')

def log_stats(client, sensor_address, stats):
    json_body = [
        {
            "measurement": "sensor_data",
            "tags": {
                "client": sensor_address,
            },
            "time": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "fields": {
                "temperature": stats['temperature'],
                "humidity": stats['humidity'],
            }
        }
    ]

    client.write_points(json_body)

buffer = ""

while True:
    data = socket.recv(1024)
    buffer += str(data, encoding='ascii')
    try:
        data = json.loads(buffer)
        print("Received chunk", data)
        log_stats(influx, sensor_address, data)
        buffer = ""
    except json.JSONDecodeError as e:
        continue

socket.close()

#############################################################3

for i in nearby_devices:
    num += 1
    print(num, ": ", bluetooth.lookup_name(i))

# CHOOSE NUMBER
selection = int(input("> ")) - 1

# CONNECT BLUETOOTH
print("You have selected", bluetooth.lookup_name(nearby_devices[selection]))
bd_addr = nearby_devices[selection]

port = 1


class App(Frame):
    # protocol for bluetooth
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    def disconnect(self):
        # Close socket connection to device
        self.sock.close()

    def move(self):
        # sends to txt to arduino
        with open('codesender.txt', 'r+') as f:
            data = f.readlines()
            self.sock.send(data)
            f.close()
        del data[0]

    def createWidgets(self):

        # define buttons for arduino applier
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"] = "yellow"
        self.QUIT["command"] = self.quit

        self.QUIT.pack({"side": "left"})

        self.disconnectFrom = Button(self)
        self.disconnectFrom["text"] = "Disconnect"
        self.disconnectFrom["fg"] = "darkgrey"
        self.disconnectFrom["command"] = self.disconnect

        self.disconnectFrom.pack({"side": "left"})

        self.startFrom = Button(self)
        self.startFrom["text"] = "StartCode"
        self.startFrom["fg"] = "green"
        self.startFrom["command"] = self.move

        self.startFrom.pack({"side": "left"})

    def __init__(self, master=None):
        self.sock.connect((bd_addr, port))
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


root = Tk()
app = App(master=root)
app.mainloop()
root.destroy()
