import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import StaticTransformBroadcaster
from scipy.spatial.transform import Rotation
import math


class StaticCamTfNode(Node):
    def __init__(self):
        super().__init__("static_cam_tf_node")
        self.static_broadcaster = StaticTransformBroadcaster(self)

        tf_msg = TransformStamped()
        tf_msg.header.stamp = self.get_clock().now().to_msg()
        tf_msg.header.frame_id = "base_link"
        tf_msg.child_frame_id = "camera_link"

        # 平移
        tf_msg.transform.translation.x = 0.5
        tf_msg.transform.translation.y = 0.3
        tf_msg.transform.translation.z = 0.6

        # RPY(roll, pitch, yaw) → 四元数，顺序xyz，单位弧度
        r = Rotation.from_euler("xyz", [math.pi, 0.0, 0.0])
        q = r.as_quat()  # 返回 [x,y,z,w]
        tf_msg.transform.rotation.x = q[0]
        tf_msg.transform.rotation.y = q[1]
        tf_msg.transform.rotation.z = q[2]
        tf_msg.transform.rotation.w = q[3]

        self.static_broadcaster.sendTransform(tf_msg)
        self.get_logger().info("静态TF发布成功：base_link -> camera_link")


def main(args=None):
    rclpy.init(args=args)
    node = StaticCamTfNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
