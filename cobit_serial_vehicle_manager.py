#-*- coding:utf-8 -*-
import serial 
from threading import Thread
from adafruit_servokit import ServoKit
from cobit_car_motor_l9110 import CobitCarMotorL9110

servo = ServoKit(channels=16)
servo_offset = 0

motor = CobitCarMotorL9110()

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
                            angle = self.get_angle()
                            if angle is not -1:
                                print(angle)
                                servo.servo[0].angle = angle + servo_offset

                            throttle = self.get_throttle()
                            if throttle is not -1:
                                print(throttle)
                                motor.motor_all_start(throttle)

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

    def get_angle(self):
        cmd = str(self.command)
        start = cmd.find('x')
        end = cmd.find('y')
        if start is not -1 and end is not -1:
            joy_num = int(cmd[start+1:end])
            angle = joy_num/10 + 40 
            return angle
        else:
            return -1

    def get_throttle(self):
        cmd = str(self.command)
        start = cmd.find('y')
        end = cmd.find('z')
        if start is not -1 and end is not -1:
            throttle_num = int(cmd[start+1:end])
            throttle = throttle_num/10
            return throttle
        else:
            return -1

    def finish(self):
        servo.servo[0].angle = 90+servo_offset
        motor.motor_all_start(0)


        

if __name__ =='__main__':
    vehicle = SerialVehicleManager("/dev/ttyUSB0")
    vehicle.open_port()
    vehicle.update()
