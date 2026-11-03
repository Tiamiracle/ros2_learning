import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class NovelPublisher(Node):
    def __init__(self):
        super().__init__("novel_publisher")
        self.publisher_ = self.create_publisher(String, "/novel_text", 10)
        timer_period = 5.0
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.novel_lines = [
            "第一章 清晨的果园",
            "晨雾轻轻笼罩整片苹果园。",
            "露水挂在翠绿的叶子上，微微发亮。",
            "一台机械臂静静立在果树旁边。",
            "它的摄像头缓缓抬起，寻找成熟的苹果。",
            "红色的果子藏在枝叶之间。",
            "视觉算法识别目标，计算三维坐标。",
            "机械臂缓缓移动，准备采摘。",
            "故事到此结束。",
        ]
        self.index = 0

    def timer_callback(self):
        if self.index >= len(self.novel_lines):
            self.get_logger().info("✅小说全部发送完毕，停止发布")
            self.destroy_timer(self.timer)
            return
        msg = String()
        msg.data = self.novel_lines[self.index]
        self.publisher_.publish(msg)
        self.get_logger().info(f"📤发布第{self.index+1}行：{msg.data}")
        self.index += 1


def main(args=None):
    rclpy.init(args=args)
    node = NovelPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
