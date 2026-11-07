from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, Command
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    pkg_dir = get_package_share_directory("robot_description")
    xacro_file = os.path.join(pkg_dir, "urdf", "first_robot.urdf.xacro")
    world_file = os.path.join(pkg_dir, "world", "model.sdf")
    rviz_config_file = "/home/user/myRos2_learning/fangzhen/rvizconfig/rviz.rviz"
    model_arg = DeclareLaunchArgument("robot_description", default_value=xacro_file)

    # gazebo 先启动，优先把 /clock 发出来
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
                ),
                "use_sim_time": True,  # 补上！！
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
            "0.0",
            "-y",
            "2.0",
            "-z",
            "0.01",  # 改成贴地，不要半空下落
            "-Y",
            "0.0",
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
        parameters=[{"use_sim_time": True}],
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
        parameters=[{"use_sim_time": True}],
        output="screen",
    )

    # rviz_node = Node(
    #     package="rviz2",
    #     executable="rviz2",
    #     arguments=["-d", rviz_config_file],
    #     name="rviz2",
    #     parameters=[{"use_sim_time": True}],  # 补上
    #     output="screen",
    # )

    return LaunchDescription(
        [
            model_arg,
            gazebo,  # 第一个启动 Gazebo，先出 /clock
            robot_state_publisher,
            spawn_entity,
            joint_state_broadcaster_spawner,
            diff_drive_controller_spawner,
            # rviz_node,
        ]
    )
