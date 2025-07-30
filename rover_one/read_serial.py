import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1.0)
time.sleep(3)
ser.reset_input_buffer()
print("serial ok")

class ReadSerial(Node):
    def __init__(self):
        super().__init__("read_serial")

        self.get_logger().info("read_serial node started")

        self.print_serial()

    def print_serial(self):
        while True:
            ser_data = ser.readline()
            self.get_logger().info(ser_data)





        

        

# send command via serial usb

def main(args=None):
    rclpy.init(args=args)

    node = ReadSerial()
    rclpy.spin(node)

    ser.close()
    rclpy.shutdown()