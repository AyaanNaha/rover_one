from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
from ament_index_python.packages import get_package_share_directory
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    pkg_name = "rover_one"

    rsp_path = os.path.join(
        FindPackageShare(pkg_name).find(pkg_name),
        'launch',
        'rsp.launch.py'
    )
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(rsp_path)
    )
    
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory("gazebo_ros"), "launch", "gazebo.launch.py"
        )])
    )

    spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        name="spawn_entity",
        output="screen",
        arguments=['-topic', 'robot_description', '-entity', 'rover_one']
    )

    launch_description = LaunchDescription([rsp, gazebo, spawn_entity])

    return launch_description