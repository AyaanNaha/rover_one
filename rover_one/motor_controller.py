import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import serial
import time

ser0 = serial.Serial('/dev/ttyUSB0', 9600, timeout=1.0)
time.sleep(3)
ser0.reset_input_buffer()
print("serial0 ok")

ser1 = serial.Serial('/dev/ttyUSB1', 9600, timeout=1.0)
time.sleep(3)
ser1.reset_input_buffer()
print("serial1 ok")

class MotorController(Node):
    def __init__(self):
        super().__init__("motor_controller")

        self.get_logger().info("motor_controller node started")

        self.cmd_vel_sub_ = self.create_subscription(Twist, "/cmd_vel", self.twist_callback, 10)

    def twist_callback(self, twist: Twist): # read cmd_vel
        x = twist.linear.x
        z = twist.angular.z

        self.get_logger().info(f"\ncmd_vel.linear.x: ${twist.linear.x}\ncmd_vel.angular.z: ${twist.angular.z}")
        
        ## convert cmd_vel into direction and rpm

        msg = ""
        dir = ""
        rpm = ""
        if(abs(z) > 0):
            if (z < 0):
                dir = "d"
            else:
                dir = "a"
            
            rpm = abs(z)*10
        elif(abs(x) > 0):
            if(x > 0):
                dir = "w"
            else:
                dir = "s"

            rpm = abs(x)*10
        else:
            dir = "q"
            rpm = 0

        msg = dir + " " + str(int(rpm))
        encoded_msg = bytes(msg, 'utf-8')

        self.get_logger().info(msg)

        try:
            self.get_logger().info("sending: " + msg)
            ser0.write(encoded_msg) 
            self.get_logger().info("msg sent to serial0")
            ser1.write(encoded_msg) 
            self.get_logger().info("msg sent to serial1")                
        except KeyboardInterrupt:
            self.get_logger().info("Closed Serial Comms")
            ser0.close()
            ser1.close()




        

        

# send command via serial usb

def main(args=None):
    rclpy.init(args=args)

    node = MotorController()
    rclpy.spin(node)

    ser0.close()
    ser1.close()

    rclpy.shutdown()