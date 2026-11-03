import rclpy
from rclpy.node import Node
from turtle_patrol_srv.srv import PatrolTarget
import time


class PatrolClient(Node):
    def __init__(self):
        super().__init__("patrol_client")
        self.cli = self.create_client(PatrolTarget, "patrol_service")
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("等待服务端上线...")
        self.waypoints = [
            [2.0, 2.0, 0.0],
            [9.0, 2.0, 1.57],
            [9.0, 9.0, 3.14],
            [2.0, 9.0, -1.57],
        ]
        self.index = 0

    def send_goal(self, x, y, th):
        req = PatrolTarget.Request()
        req.target_x = x
        req.target_y = y
        req.target_theta = th
        future = self.cli.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        return future.result()

    def run_patrol(self):
        while rclpy.ok():
            wp = self.waypoints[self.index]
            self.get_logger().info(f"下发航点：{wp}")
            res = self.send_goal(wp[0], wp[1], wp[2])
            if res.success:
                self.get_logger().info(f"到达 x:{res.curr_x:.2f} y:{res.curr_y:.2f}")
            time.sleep(2.0)
            self.index = (self.index + 1) % len(self.waypoints)


def main():
    rclpy.init()
    client = PatrolClient()
    client.run_patrol()
    rclpy.shutdown()
