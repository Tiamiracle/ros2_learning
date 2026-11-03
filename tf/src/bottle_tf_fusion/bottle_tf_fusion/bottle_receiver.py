import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
from scipy.spatial.transform import Rotation
import math


class DynamicBottleTfNode(Node):
    def __init__(self):
        super().__init__("dynamic_bottle_tf_node")
        # 动态TF广播器
        self.dynamic_broadcaster = TransformBroadcaster(self)

        # 定时器：10Hz，每0.1s发一次动态TF
        self.timer_period = 0.1
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

        # 用来模拟瓶子随时间运动
        self.t = 0.0
        self.get_logger().info("动态TF节点启动，发布 base_link -> bottle_link")

    def timer_callback(self):
        tf_msg = TransformStamped()
        tf_msg.header.stamp = self.get_clock().now().to_msg()
        tf_msg.header.frame_id = "base_link"  # 父坐标系
        tf_msg.child_frame_id = "bottle_link"  # 子坐标系（瓶子）

        # 模拟瓶子沿着X轴来回移动
        x = 0.3 + 0.2 * math.sin(self.t)
        y = 0.2
        z = 0.4
        tf_msg.transform.translation.x = x
        tf_msg.transform.translation.y = y
        tf_msg.transform.translation.z = z

        # 模拟瓶子绕Z轴慢慢旋转（yaw变化）
        yaw = self.t
        r = Rotation.from_euler("xyz", [0, 0, yaw])
        q = r.as_quat()
        tf_msg.transform.rotation.x = q[0]
        tf_msg.transform.rotation.y = q[1]
        tf_msg.transform.rotation.z = q[2]
        tf_msg.transform.rotation.w = q[3]

        # 发布动态TF
        self.dynamic_broadcaster.sendTransform(tf_msg)
        self.t += self.timer_period

        self.get_logger().info(f"bottle x={x:.2f}, yaw={yaw:.2f}")


def main(args=None):
    rclpy.init(args=args)
    node = DynamicBottleTfNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
