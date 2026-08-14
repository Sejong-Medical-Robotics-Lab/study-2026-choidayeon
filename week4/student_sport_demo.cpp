#include <chrono>
#include <iostream>
#include <memory>
#include <string>
#include <thread>

#include <rclcpp/rclcpp.hpp>
#include "common/ros2_sport_client.h"

class StudentSportDemo : public rclcpp::Node
{
public:
  StudentSportDemo()
  : Node("student_sport_demo"),
    sport_client_(this)
  {
    RCLCPP_INFO(
      this->get_logger(),
      "Student Sport API node started"
    );
  }

  void stand_up()
  {
    sport_client_.StandUp(req_);
    RCLCPP_INFO(
      this->get_logger(),
      "StandUp command sent"
    );
  }

  void stand_down()
  {
    sport_client_.StandDown(req_);
    RCLCPP_INFO(
      this->get_logger(),
      "StandDown command sent"
    );
  }

  void stop()
  {
    sport_client_.StopMove(req_);
    RCLCPP_INFO(
      this->get_logger(),
      "StopMove command sent"
    );
  }

private:
  SportClient sport_client_;
  unitree_api::msg::Request req_;
};

int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);

  auto node = std::make_shared<StudentSportDemo>();

  // ROS2 노드와 통신 환경이 준비될 시간을 잠시 기다림
  std::this_thread::sleep_for(
    std::chrono::seconds(1)
  );

  std::string input;

  while (rclcpp::ok())
  {
    std::cout << "\n";
    std::cout << "========================\n";
    std::cout << " Student Sport API Demo\n";
    std::cout << "========================\n";
    std::cout << "1 : Stand Up\n";
    std::cout << "2 : Stand Down\n";
    std::cout << "q : Stop and Quit\n";
    std::cout << "Select: ";

    std::getline(std::cin, input);

    if (input == "1")
    {
      node->stand_up();
    }
    else if (input == "2")
    {
      node->stand_down();
    }
    else if (input == "q" || input == "Q")
    {
      node->stop();
      break;
    }
    else
    {
      std::cout << "잘못된 입력입니다.\n";
    }

    // 현재 노드에 들어온 ROS2 작업을 처리
    rclcpp::spin_some(node);
  }

  rclcpp::shutdown();
  return 0;
}
