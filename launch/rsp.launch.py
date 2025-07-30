from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command


def generate_launch_description():
    robot_state_pub_ = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[{
            "robot_description": Command(["xacro /home/dev/dev_ws/src/rover_one/description/rover.urdf.xacro"])
        }]
    )

    launch_description = LaunchDescription([robot_state_pub_])

    return launch_description