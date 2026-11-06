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

    # 👇 3. 【核心新增】指定你自己的 Nav2 参数配置文件绝对路径
    nav2_params_file = "/home/user/myRos2_learning/fangzhen/src/robot_description/config/nav2_params.yaml"

    # 4. 包含官方的 bringup_launch.py 并传入参数
    nav2_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_dir, "launch", "bringup_launch.py")
        ),
        launch_arguments={
            "use_sim_time": "True",  # 必须使用仿真时间
            # "use_rviz": "True",  # 自动拉起 RViz
            "map": map_yaml_file,  # 加载你建好的地图
            "params_file": nav2_params_file,  # 👈 【新增】读取你的自定义配置
            "slam": "False",  # 导航阶段不需要 SLAM
            "autostart": "True",  # 自动启动所有生命周期节点
        }.items(),
    )

    return LaunchDescription([nav2_bringup])
