import rclpy
import time
import math
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult


# --- 占位函数：语音播报 ---
def play_voice(text):
    # 仿真环境常用 espeak，如果没有安装请 sudo apt install espeak
    print(f"🔊 语音播报: {text}")
    # import os
    # os.system(f'espeak -v zh "{text}" &')


# --- 占位函数：拍照 ---
def take_photo(point_name):
    print(f"📸 拍照: 正在保存 {point_name} 的图像...")
    # 这里之后接入你的 cv_bridge 和 cv2.imwrite 逻辑


# --- 辅助函数：快速生成 PoseStamped 目标点 ---
def create_pose(navigator, x, y, yaw):
    pose = PoseStamped()
    pose.header.frame_id = "map"
    pose.header.stamp = navigator.get_clock().now().to_msg()
    pose.pose.position.x = float(x)
    pose.pose.position.y = float(y)
    pose.pose.position.z = 0.0
    pose.pose.orientation.z = math.sin(yaw / 2.0)
    pose.pose.orientation.w = math.cos(yaw / 2.0)
    return pose


# --- 核心巡逻逻辑（你之前写的那个） ---
def run_patrol_task(navigator, patrol_points, home_pose):
    while rclpy.ok():
        navigator.get_logger().info("🚀 开始新一轮巡逻任务！")

        # 1. 遍历每个巡逻点
        for i, target_pose in enumerate(patrol_points):
            point_name = f"巡逻点{i+1}"

            play_voice(f"准备前往{point_name}")
            navigator.get_logger().info(f"正在前往 {point_name}...")

            # 发送目标并等待完成
            navigator.goToPose(target_pose)
            while not navigator.isTaskComplete():
                # 在等待时可以加上 sleep，防止 CPU 占用过高
                time.sleep(0.1)

            result = navigator.getResult()
            if result == TaskResult.SUCCEEDED:
                navigator.get_logger().info(f"✅ 已到达 {point_name}")
                play_voice(f"已到达{point_name}")
                take_photo(point_name)
            else:
                navigator.get_logger().warn(f"❌ 前往 {point_name} 失败，跳过该点")

        # 2. 所有点巡逻完毕，返回初始位置
        navigator.get_logger().info("🏁 所有巡逻点已完成，准备返回初始位置...")
        play_voice("巡逻完毕，准备返回待命区")

        navigator.goToPose(home_pose)
        while not navigator.isTaskComplete():
            time.sleep(0.1)

        navigator.get_logger().info("🏠 已返回初始位置。")

        # 3. 休息（演示用 10 秒，真实业务用 300 秒）
        navigator.get_logger().info("💤 休眠 10 秒，等待下一次巡逻...")
        time.sleep(10)


# --- 主函数：入口 ---
def main(args=None):
    rclpy.init(args=args)

    # 初始化导航器
    navigator = BasicNavigator()

    # 等待 Nav2 激活（重要！否则发指令无效）
    navigator.get_logger().info("⏳ 等待 Nav2 系统激活...")
    navigator.waitUntilNav2Active()

    # 定义初始位置 (假设是 0,0,0)
    home_pose = create_pose(navigator, 0.0, 0.0, 0.0)

    # 设置初始位置
    navigator.setInitialPose(home_pose)

    # 定义巡逻点（请根据你的地图坐标修改这些值）
    patrol_points = [
        create_pose(navigator, 1.0, 1.0, 0.0),  # 巡逻点 A
        create_pose(navigator, 2.0, -1.0, 1.57),  # 巡逻点 B (朝向左侧)
        create_pose(navigator, -1.0, 0.0, 3.14),  # 巡逻点 C (朝向后方)
    ]

    try:
        # 启动巡逻大循环
        run_patrol_task(navigator, patrol_points, home_pose)
    except KeyboardInterrupt:
        navigator.get_logger().info("🛑 收到中断信号，取消当前任务。")
        navigator.cancelTask()

    navigator.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
