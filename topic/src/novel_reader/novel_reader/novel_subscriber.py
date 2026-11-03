import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import threading
from queue import Queue
import espeakng


class NovelSubNode(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        # 创建队列
        self.novels_queue_ = Queue()
        # 订阅话题（截图话题名叫 novel，你可以改成 /novel_text）
        self.novel_subscriber_ = self.create_subscription(
            String, "novel_text", self.novel_callback, 10
        )
        # 创建并启动语音后台线程
        self.speech_thread_ = threading.Thread(target=self.speake_thread)
        self.speech_thread_.start()

    def novel_callback(self, msg):
        # ROS回调：收到消息丢进队列
        self.novels_queue_.put(msg.data)

    def speake_thread(self):
        # 在线程内部实例化espeakng，线程安全
        speaker = espeakng.Speaker()
        speaker.voice = "zh"
        # 可选设置语速 speaker.speed = 180

        while rclpy.ok():  # ROS节点存活就循环
            if self.novels_queue_.qsize() > 0:  # 判断队列有数据
                text = self.novels_queue_.get()
                self.get_logger().info(f"朗读: {text}")
                speaker.say(text)  # 发起朗读
                speaker.wait()  # 阻塞，等待读完


def main(args=None):
    rclpy.init(args=args)
    node = NovelSubNode("novel_sub_node")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
