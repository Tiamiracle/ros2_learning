import rclpy
from rclpy.node import Node
import cv2
import os
from face_srv.srv import FaceDetect
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from ament_index_python.packages import get_package_share_directory


class FaceServiceNode(Node):
    def __init__(self):
        super().__init__("face_servertest")
        self.service = self.create_service(
            FaceDetect, "face_detect", self.detectCallback
        )
        self.bridge = CvBridge()
        self.face_cascade = cv2.CascadeClassifier(
            "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"
        )
        self.default_image_path = os.path.join(
            get_package_share_directory("face_detect"), "resource/face.jpg"
        )

    def detectCallback(self, request, response):
        if request.input_img.data:
            # 如果请求里带了图像，把ROS Image消息转成OpenCV格式
            cv_image = self.bridge.imgmsg_to_cv2(request.input_img)
        else:
            # 客户端没传图像，加载默认图片
            cv_image = cv2.imread(self.default_image_path)
            self.get_logger().info("传入图像为空，使用默认图像!")
        # 核心：face_recognition 检测所有人脸框
        self.get_logger().info("start!!!")
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        face_locations = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        # 人脸总数
        response.face_num = len(face_locations)
        # 循环把每个人脸框坐标存入response的数组
        for x, y, w, h in face_locations:
            left = x
            top = y
            right = x + w
            bottom = y + h
            cv2.rectangle(cv_image, (left, top), (right, bottom), (0, 255, 0), 2)
            response.top.append(top)
            response.left.append(left)
            response.right.append(right)
            response.bottom.append(bottom)
        response.result_img = self.bridge.cv2_to_imgmsg(cv_image, encoding="bgr8")
        return response


def main():
    rclpy.init()
    node = FaceServiceNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
