cmake_minimum_required(VERSION 3.8)
project(sys_monitor)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# 1.依赖包
find_package(ament_cmake REQUIRED)
#ros
find_package(rclcpp REQUIRED)
find_package(rosidl_default_generators REQUIRED)
#qt
find_package(Qt5 COMPONENTS Widgets REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)
# 2.生成自定义消息
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/SystemInfo.msg"
)
# 3.编译发布者
add_executable(sys_info_pub src/sys_info_pub.cpp)
ament_target_dependencies(sys_info_pub rclcpp)
rosidl_target_interfaces(sys_info_pub ${PROJECT_NAME} "rosidl_typesupport_cpp")
# 4.编译 Qt 订阅者
set(CMAKE_AUTOMOC ON)
add_executable(sys_info_sub_qt src/sys_info_sub_qt.cpp)
target_link_libraries(sys_info_sub_qt Qt5::Widgets)
ament_target_dependencies(sys_info_sub_qt rclcpp)
rosidl_target_interfaces(sys_info_sub_qt ${PROJECT_NAME} "rosidl_typesupport_cpp")
# 4. 安装可执行文件
install(TARGETS
  sys_info_pub
  sys_info_sub_qt
  DESTINATION lib/${PROJECT_NAME}
)
# 5. 测试与收尾
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  find_package(rosidl_default_generators REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()
ament_package()
