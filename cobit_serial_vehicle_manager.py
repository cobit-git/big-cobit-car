#-*- coding:utf-8 -*-
import serial 
from threading import Thread

class SerialVehicleManager(Thread):

    def __init__(self, serial_port):

        Thread.__init__(self)
        self.seq = serial.Serial(
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        self.seq.port = serial_port
        self.is_serial_running = False
        self.daemon = True
        self.command = None

    def read_cmd(self):
        return self.command

    def run(self):
        while True: 
            if self.seq.isOpen() == True:  
                try:
                    if self.seq.inWaiting():
                        try:
                            self.command = self.seq.readline()
                            print(self.command)
                        except AttributeError:
                            print("attr error")
                except IOError:
                    print("IO error")

    def open_port(self):
        if self.seq.isOpen() == False:
            self.seq.open()

    def close_port(self):
        if self.seq.isOpen() == True:
            self.seq.close()

    def is_seq_open(self):
        if self.seq.isOpen() == True:
            return True
        else:
            return False

    #def set_serial_port(self, port_name):
    #    self.seq.port = port_name

    def get_serial_port(self):
        return self.seq.port

if __name__ =='__main__':
    vehicle = SerialVehicleManager("/dev/ttyUSB0")
    vehicle.open_port()
    vehicle.update()
