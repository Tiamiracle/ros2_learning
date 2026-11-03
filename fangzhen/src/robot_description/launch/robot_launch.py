from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, Command
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    pkg_dir = get_package_share_directory("robot_description")
    # 对应你路径 urdf/robot/first_robot.urdf.xacro
    xacro_file = os.path.join(pkg_dir, "urdf", "first_robot.urdf.xacro")
    world_file = os.path.join(pkg_dir, "world", "model.sdf")
    model_arg = DeclareLaunchArgument("robot_description", default_value=xacro_file)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    get_package_share_directory("gazebo_ros"),
                    "launch",
                    "gazebo.launch.py",
                )
            ]
        ),
        launch_arguments={"world": world_file}.items(),
    )
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[
            {
                "robot_description": Command(
                    ["xacro ", LaunchConfiguration("robot_description")]
                )
            }
        ],
        output="screen",
    )
    spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-topic",
            "robot_description",
            "-entity",
            "my_robot",
            "-x",
            "0.0",  # 移到 X=5 的位置
            "-y",
            "2.0",  # 移到 Y=5 的位置
            "-z",
            "0.5",  # 从半米高落下
        ],
        output="screen",
    )
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
        ],
        output="screen",
    )
    diff_drive_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "diff_drive_controller",
            "--controller-manager",
            "/controller_manager",
        ],
        output="screen",
    )

    rviz_node = Node(package="rviz2", executable="rviz2", name="rviz2", output="screen")

    return LaunchDescription(
        [
            model_arg,
            robot_state_publisher,
            gazebo,
            # rviz_node,
            spawn_entity,
            joint_state_broadcaster_spawner,  # 然后唤醒状态广播器
            diff_drive_controller_spawner,
        ]
    )
