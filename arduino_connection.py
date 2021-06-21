from tkinter import *
from gui import *
import bluetooth

print("Searching for devices...")

# SCAN BLUETOOTH DEVICES

print("")
nearby_devices = bluetooth.discover_devices()
num = 0
print("Select your device by entering it's corresponding number...")

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
