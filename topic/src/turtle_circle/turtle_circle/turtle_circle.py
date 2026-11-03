import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class TurtleCirclePub(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        # 创建发布器，话题 /turtle1/cmd_vel，消息Twist，队列10
        self.cmd_pub_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        # 定时器：每0.1s发一次速度指令
        self.timer_period = 0.1
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

    def timer_callback(self):
        msg = Twist()
        # 线速度向前
        msg.linear.x = 0.5
        # 旋转角速度
        msg.angular.z = 0.4
        self.cmd_pub_.publish(msg)
        self.get_logger().info("正在画圆...")


def main(args=None):
    rclpy.init(args=args)
    node = TurtleCirclePub("turtle_circle_pub")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
