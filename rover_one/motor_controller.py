import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class MotorController(Node):
    def __init__(self):
        super().__init__("motor_controller")

        self.get_logger().info("motor_controller node started")

        self.cmd_vel_sub_ = self.create_subscription(Twist, "/cmd_vel", self.twist_callback, 10)

    def twist_callback(self, twist: Twist): # read cmd_vel
        x = twist.linear.x
        z = twist.angular.z

        self.get_logger().info(f"\ncmd_vel.linear.x: ${twist.linear.x}\ncmd_vel.angular.z: ${twist.angular.z}\n")
        
        ## convert cmd_vel into direction and rpm

        msg = ""
        dir = ""
        rpm = ""
        if(abs(z) > 0):
            if (z > 0):
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


        self.get_logger().info(msg)





        

        

# send command via serial usb

def main(args=None):
    rclpy.init(args=args)

    node = MotorController()
    rclpy.spin(node)

    rclpy.shutdown()