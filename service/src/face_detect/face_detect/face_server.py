import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

# ✅ 重点导入路径：接口包名.srv.消息名
from face_srv.srv import FaceDetect
import cv2
from cv_bridge import CvBridge


class FaceDetectServer(Node):
    def __init__(self):
        super().__init__("face_detect_server")
        self.srv = self.create_service(FaceDetect, "face_detect", self.detect_callback)
        self.bridge = CvBridge()
        # 加载haar人脸检测器
        self.face_cascade = cv2.CascadeClassifier(
            "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"
        )
        self.get_logger().info("✅人脸检测服务已启动，等待图片请求")

    def detect_callback(self, request, response):
        # ROS图像转opencv
        cv_img = self.bridge.imgmsg_to_cv2(request.input_img, desired_encoding="bgr8")
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=4
        )
        face_num = len(faces)
        bbox_flat = []
        for x, y, w, h in faces:
            cv2.rectangle(cv_img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(
                cv_img,
                "face",
                (x, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                1,
            )
            bbox_flat.extend([x, y, x + w, y + h])

        response.result_img = self.bridge.cv2_to_imgmsg(cv_img, encoding="bgr8")
        response.face_num = face_num
        response.bboxes = [int(val) for val in bbox_flat]
        self.get_logger().info(f"检测到人脸数量：{face_num}, 坐标列表：{bbox_flat}")
        return response


def main():
    rclpy.init()
    node = FaceDetectServer()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
