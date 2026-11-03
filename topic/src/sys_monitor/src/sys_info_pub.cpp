#include <chrono>
#include <memory>
#include <string>
#include <fstream>
#include <sstream>
#include <sys/utsname.h>
#include "rclcpp/rclcpp.hpp"
#include "sys_monitor/msg/system_info.hpp" // 自动生成的 msg 头文件

using namespace std::chrono_literals;

// 辅助函数：读取 CPU 信息 (简易版)
float get_cpu_percent()
{
    static unsigned long prev_user = 0, prev_nice = 0, prev_system = 0, prev_idle = 0;
    std::ifstream file("/proc/stat");
    std::string cpu;
    unsigned long user, nice, system, idle;
    file >> cpu >> user >> nice >> system >> idle;
    file.close();

    unsigned long prev_total = prev_user + prev_nice + prev_system + prev_idle;
    unsigned long total = user + nice + system + idle;
    unsigned long delta_total = total - prev_total;
    unsigned long delta_idle = idle - prev_idle;

    prev_user = user;
    prev_nice = nice;
    prev_system = system;
    prev_idle = idle;

    if (delta_total == 0)
        return 0.0f;
    return (1.0f - (float)delta_idle / delta_total) * 100.0f;
}

// 辅助函数：读取内存信息
void get_mem_info(float &percent, float &used, float &total)
{
    std::ifstream meminfo("/proc/meminfo");
    std::string line;
    long total_mem = 0, free_mem = 0, buffers = 0, cached = 0;
    while (std::getline(meminfo, line))
    {
        if (line.find("MemTotal:") == 0)
            sscanf(line.c_str(), "MemTotal: %ld kB", &total_mem);
        else if (line.find("MemFree:") == 0)
            sscanf(line.c_str(), "MemFree: %ld kB", &free_mem);
        else if (line.find("Buffers:") == 0)
            sscanf(line.c_str(), "Buffers: %ld kB", &buffers);
        else if (line.find("Cached:") == 0)
            sscanf(line.c_str(), "Cached: %ld kB", &cached);
    }
    total = total_mem / (1024.0 * 1024.0); // GB
    float avail = (free_mem + buffers + cached) / (1024.0 * 1024.0);
    used = total - avail;
    percent = (used / total) * 100.0f;
}
void get_disk_info(float &percent, float &used, float &total)
{
    struct statvfs fs;
    statvfs("/", &fs);
    total = (float)(fs.f_blocks * fs.f_frsize) / (1024 * 1024 * 1024);
    float avail = (float)(fs.f_bavail * fs.f_frsize) / (1024 * 1024 * 1024);
    used = total - avail;
    percent = used / total * 100.0f;
}

class SysInfoPublisher : public rclcpp::Node
{
public:
    SysInfoPublisher() : Node("sys_info_publisher")
    {
        pub_ = this->create_publisher<sys_monitor::msg::SystemInfo>("/system_monitor", 10);
        timer_ = this->create_wall_timer(1000ms, std::bind(&SysInfoPublisher::timer_callback, this));
    }

private:
    void timer_callback()
    {
        auto msg = sys_monitor::msg::SystemInfo();

        // 填充数据
        msg.timestamp = this->now().seconds();
        msg.cpu_percent = get_cpu_percent();
        get_mem_info(msg.mem_percent, msg.mem_used, msg.mem_total);
        get_disk_info(msg.disk_percent, msg.disk_used, msg.disk_total);
        // 主机名
        struct utsname buffer;
        uname(&buffer);
        msg.hostname = buffer.nodename;

        pub_->publish(msg);
        RCLCPP_INFO(this->get_logger(), "发布系统信息: CPU %.1f%%, MEM %.1f%%", msg.cpu_percent, msg.mem_percent);
    }

    rclcpp::Publisher<sys_monitor::msg::SystemInfo>::SharedPtr pub_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<SysInfoPublisher>());
    rclcpp::shutdown();
    return 0;
}