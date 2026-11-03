import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtle_patrol_srv.srv import PatrolTarget
import math
import threading
from rclpy.callback_groups import ReentrantCallbackGroup


class PatrolServer(Node):
    def __init__(self):
        super().__init__("patrol_server")
        self.cb_group = ReentrantCallbackGroup()
        self.srv = self.create_service(
            PatrolTarget,
            "patrol_service",
            self.patrol_callback,
            callback_group=self.cb_group,
        )
        self.cmd_pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.pose_sub = self.create_subscription(
            Pose, "/turtle1/pose", self.pose_cb, 10
        )

        self.curr_pose = Pose()
        self.arrive_flag = False
        self.flag_lock = threading.Lock()
        self.target_x = 0.0
        self.target_y = 0.0
        self.target_theta = 0.0
        self.arrive_event = threading.Event()
        self.timer = self.create_timer(
            0.01, self.control_loop, callback_group=self.cb_group
        )

    def pose_cb(self, msg: Pose):
        self.curr_pose = msg

    def patrol_callback(self, req, resp):
        self.get_logger().info(
            f"收到目标：x={req.target_x:.2f}, y={req.target_y:.2f}, theta={req.target_theta:.2f}"
        )
        # 1. 先更新目标，重置到达标志
        self.target_x = req.target_x
        self.target_y = req.target_y
        self.target_theta = req.target_theta
        with self.flag_lock:
            self.arrive_flag = False
            self.arrive_event.clear()

        # 2. 阻塞等待，直到到达
        self.arrive_event.wait()

        # 3. 到达之后，填充响应，再return发包
        resp.success = True
        resp.curr_x = self.curr_pose.x
        resp.curr_y = self.curr_pose.y
        resp.curr_theta = self.curr_pose.theta
        self.get_logger().info("到达目标，返回响应")
        return resp

    # 替换你的control_loop
    def control_loop(self):
        with self.flag_lock:
            if self.arrive_flag:
                self.cmd_pub.publish(Twist())
                return

        dx = self.target_x - self.curr_pose.x
        dy = self.target_y - self.curr_pose.y
        dist = math.hypot(dx, dy)
        target_yaw = math.atan2(dy, dx)
        yaw_err = target_yaw - self.curr_pose.theta
        yaw_err = math.atan2(math.sin(yaw_err), math.cos(yaw_err))

        vel = Twist()
        kp_ang = 2.0
        kp_lin = 0.8
        # 距离很远的时候，不管角度，边转边前进
        if dist < 0.15:
            # 位置到了，原地修正姿态
            angle_err = self.target_theta - self.curr_pose.theta
            angle_err = math.atan2(math.sin(angle_err), math.cos(angle_err))
            if abs(angle_err) < 0.08:
                with self.flag_lock:
                    self.arrive_flag = True
                    self.arrive_event.set()
                return
            vel.angular.z = kp_ang * angle_err
        else:
            # 重点改动：角度不对，依然给前进速度！不再砍掉linear.x
            vel.angular.z = kp_ang * yaw_err
            vel.linear.x = kp_lin * dist

        # 限速，防止飞出去
        vel.linear.x = min(vel.linear.x, 1.5)
        vel.angular.z = max(min(vel.angular.z, 2.0), -2.0)
        self.cmd_pub.publish(vel)


def main():
    rclpy.init()
    node = PatrolServer()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    rclpy.shutdown()
