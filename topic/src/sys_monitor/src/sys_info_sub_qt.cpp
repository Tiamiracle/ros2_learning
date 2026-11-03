#include <memory>
#include <QApplication>
#include <QWidget>
#include <QVBoxLayout>
#include <QLabel>
#include <QTimer>
#include "rclcpp/rclcpp.hpp"
#include "sys_monitor/msg/system_info.hpp"

// 自定义 Qt 窗口
class SystemMonitorWidget : public QWidget
{
    Q_OBJECT
public:
    SystemMonitorWidget(QWidget *parent = nullptr) : QWidget(parent)
    {
        QVBoxLayout *layout = new QVBoxLayout(this);

        label_cpu_ = new QLabel("CPU 使用率: 等待数据...", this);
        label_mem_ = new QLabel("内存使用率: 等待数据...", this);
        label_disk_ = new QLabel("磁盘使用率: 等待数据...", this);
        label_host_ = new QLabel("主机名: 等待数据...", this);

        QFont font = label_cpu_->font();
        font.setPointSize(16);
        label_cpu_->setFont(font);
        label_mem_->setFont(font);
        label_disk_->setFont(font);
        label_host_->setFont(font);

        layout->addWidget(label_cpu_);
        layout->addWidget(label_mem_);
        layout->addWidget(label_disk_);
        layout->addWidget(label_host_);
        setWindowTitle("ROS 2 系统监控");
        resize(400, 300);
    }

    void update_data(const sys_monitor::msg::SystemInfo::SharedPtr msg)
    {
        // 在 Qt 主线程中更新 UI
        label_cpu_->setText(QString("CPU 使用率: %1 %").arg(msg->cpu_percent, 0, 'f', 1));
        label_mem_->setText(QString("内存使用率: %1 % (%2/%3 GB)")
                                .arg(msg->mem_percent, 0, 'f', 1)
                                .arg(msg->mem_used, 0, 'f', 1)
                                .arg(msg->mem_total, 0, 'f', 1));
        label_disk_->setText(QString("磁盘使用率: %1 %").arg(msg->disk_percent, 0, 'f', 1));
        label_host_->setText(QString("主机名: %1").arg(QString::fromStdString(msg->hostname)));
    }

private:
    QLabel *label_cpu_;
    QLabel *label_mem_;
    QLabel *label_disk_;
    QLabel *label_host_;
};

// ROS 2 节点类
class SysInfoSubNode : public rclcpp::Node
{
public:
    SysInfoSubNode(SystemMonitorWidget *widget) : Node("sys_info_subscriber"), widget_(widget)
    {
        sub_ = this->create_subscription<sys_monitor::msg::SystemInfo>(
            "/system_monitor", 10,
            [this](const sys_monitor::msg::SystemInfo::SharedPtr msg)
            {
                this->widget_->update_data(msg); // 直接传给 Qt 窗口
            });
    }

private:
    std::shared_ptr<rclcpp::Subscription<sys_monitor::msg::SystemInfo>> sub_;
    SystemMonitorWidget *widget_;
};

int main(int argc, char **argv)
{
    // 1. 初始化 ROS 2
    rclcpp::init(argc, argv);

    // 2. 初始化 Qt
    QApplication app(argc, argv);

    // 3. 创建界面和节点
    SystemMonitorWidget widget;
    auto node = std::make_shared<SysInfoSubNode>(&widget);

    // 4. 使用 Qt 的定时器来触发 ROS 2 的 Spin，防止阻塞 UI
    QTimer ros_timer;
    QObject::connect(&ros_timer, &QTimer::timeout, [&node]()
                     { rclcpp::spin_some(node); });
    ros_timer.start(100); // 每 100ms 处理一次 ROS 回调

    widget.show();
    int ret = app.exec();

    rclcpp::shutdown();
    return ret;
}

// 【注意】包含 Q_OBJECT 宏，必须在文件末尾包含 moc 生成的文件
#include "sys_info_sub_qt.moc"