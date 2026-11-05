from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    pkg = get_package_share_directory("robot_description")
    slam_yaml = os.path.join(pkg, "config", "slam.yaml")

    slam_node = Node(
        package="slam_toolbox",
        executable="async_slam_toolbox_node",
        name="async_slam_toolbox_node",
        parameters=[
            slam_yaml,
            {"use_sim_time": True},
            # 【加上下面这行，强制指定 QoS 兼容 Gazebo】
            {"qos_overrides./scan.subscription.reliability": "best_effort"},
        ],
        remappings=[("/odom", "/diff_drive_controller/odom")],
        output="screen",
    )
    return LaunchDescription([slam_node])
