import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    # 1. 获取官方 nav2_bringup 的 share 目录
    nav2_bringup_dir = get_package_share_directory("nav2_bringup")

    # 2. 指定你刚才保存的地图 yaml 文件路径
    map_yaml_file = "/home/user/myRos2_learning/fangzhen/room/room.yaml"

    # 3. 指定你自己的 Nav2 参数配置文件绝对路径
    nav2_params_file = "/home/user/myRos2_learning/fangzhen/src/robot_description/config/nav2_params.yaml"

    # 4. 包含官方的 bringup_launch.py（负责启动算法核心，关掉它自带的 RViz）
    nav2_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_dir, "launch", "bringup_launch.py")
        ),
        launch_arguments={
            "use_sim_time": "True",
            "use_rviz": "False",  # 👈 这里改成 False，防止它崩了连累 RViz
            "map": map_yaml_file,
            "params_file": nav2_params_file,
            "slam": "False",
            "autostart": "True",
            "remappings": "[('/cmd_vel', '/diff_drive_controller/cmd_vel_unstamped')]",
        }.items(),
    )

    # 5. 👇 【核心新增】单独引入官方 Nav2 的 RViz 启动文件
    nav2_rviz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_dir, "launch", "rviz_launch.py")
        ),
        launch_arguments={
            "use_sim_time": "True",
        }.items(),
    )

    return LaunchDescription([nav2_bringup, nav2_rviz])
