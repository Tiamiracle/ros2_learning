from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
import os
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg_path = get_package_share_directory("robot_description")
    urdf_path = os.path.join(pkg_path, "urdf", "base_imu.urdf")

    # 加载urdf参数
    urdf_arg = DeclareLaunchArgument("robot_description", default_value=urdf_path)

    # 机器人状态发布节点
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[
            {
                # 关键！Command cat 读取文件内容
                "robot_description": Command(
                    ["cat ", LaunchConfiguration("robot_description")]
                )
            }
        ],
    )

    # rviz2节点
    rviz_node = Node(package="rviz2", executable="rviz2", name="rviz2", output="screen")

    return LaunchDescription([urdf_arg, robot_state_publisher_node, rviz_node])
