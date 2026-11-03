import rclpy
from rclpy.node import Node
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from geometry_msgs.msg import TransformStamped


class TfListenerNode(Node):
    def __init__(self):
        super().__init__("tf_listener_node")
        # 1. 创建TF缓存，用来存放所有收到的静态+动态TF
        self.tf_buffer = Buffer()
        # 2. TF监听器，自动订阅 /tf 和 /tf_static，往buffer里填数据
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # 定时器：0.1s查一次（10Hz，和动态tf发布频率匹配）
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.get_logger().info("TF监听器启动，准备查询 base_link ← bottle_link")

    def timer_callback(self):
        try:
            # 查询：source_frame 在 target_frame 下的变换
            transform: TransformStamped = self.tf_buffer.lookup_transform(
                target_frame="base_link",
                source_frame="bottle_link",
                time=rclpy.time.Time(),  # Time() = 取最新可用的一条
            )

            # 拿到平移
            x = transform.transform.translation.x
            y = transform.transform.translation.y
            z = transform.transform.translation.z
            # 拿到四元数旋转
            qx = transform.transform.rotation.x
            qy = transform.transform.rotation.y
            qz = transform.transform.rotation.z
            qw = transform.transform.rotation.w

            self.get_logger().info(
                f"\n==== base_link -> bottle_link ====\n"
                f"位置: x={x:.2f}, y={y:.2f}, z={z:.2f}\n"
                f"四元数: x={qx:.2f}, y={qy:.2f}, z={qz:.2f}, w={qw:.2f}"
            )

        except TransformException as ex:
            # 查不到的时候会进这里（还没收到tf、frame名字写错、TF断了）
            self.get_logger().warn(f"查询失败：{ex}")


def main(args=None):
    rclpy.init(args=args)
    node = TfListenerNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
