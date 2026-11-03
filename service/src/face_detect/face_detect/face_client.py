import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from face_srv.srv import FaceDetect
from cv_bridge import CvBridge
import cv2


class FaceDetectClient(Node):
    def __init__(self):
        super().__init__("face_detect_client")
        self.cli = self.create_client(FaceDetect, "face_detect")
        self.bridge = CvBridge()
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("⏳等待face_detect服务上线...")
        self.req = FaceDetect.Request()

    def send_img_request(self, cv_img):
        img_msg = self.bridge.cv2_to_imgmsg(cv_img, encoding="bgr8")
        self.req.input_img = img_msg
        future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, future)
        return future.result()


def main():
    rclpy.init()
    client = FaceDetectClient()
    # 修改这里为你本地图片路径
    img_path = "/home/user/myRos2_learning/service/src/face_detect/resource/face.jpg"
    cv_img = cv2.imread(img_path)
    if cv_img is None:
        print("图片读取失败，请检查路径！")
        return
    res = client.send_img_request(cv_img)
    print(f"===== 检测结果 =====")
    print(f"人脸总数：{res.face_num}")
    print(f"top数组：{res.top}")
    print(f"left数组：{res.left}")
    print(f"right数组：{res.right}")
    print(f"bottom数组：{res.bottom}")

    res_cv = client.bridge.imgmsg_to_cv2(res.result_img, "bgr8")
    cv2.imshow("face_result", res_cv)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    client.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
