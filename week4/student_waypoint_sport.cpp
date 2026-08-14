#include <chrono>
#include <iostream>
#include <memory>
#include <thread>

#include <rclcpp/rclcpp.hpp>
#include "common/ros2_sport_client.h"


class StudentWaypointSport : public rclcpp::Node
{
public:

  StudentWaypointSport()
  : Node("student_waypoint_sport"),
    sport_client_(this)
  {
    RCLCPP_INFO(
      this->get_logger(),
      "Sport API Waypoint node started"
    );
  }


  // ========================================================
  // 일정 시간 동안 Go2를 이동시키는 함수
  // ========================================================
  //
  // vx       : 전후 이동 속도
  // vy       : 좌우 이동 속도
  // vyaw     : 회전 각속도
  // duration : 명령을 유지할 시간
  //
  void move_for(
    float vx,
    float vy,
    float vyaw,
    double duration_sec)
  {
    RCLCPP_INFO(
      this->get_logger(),
      "Move: vx=%.2f, vy=%.2f, vyaw=%.2f, time=%.1f",
      vx,
      vy,
      vyaw,
      duration_sec
    );

    // 이동 시작 시간 저장
    auto start =
      std::chrono::steady_clock::now();


    // 지정된 시간이 끝날 때까지 반복
    while (rclcpp::ok())
    {
      auto now =
        std::chrono::steady_clock::now();

      double elapsed =
        std::chrono::duration<double>(
          now - start
        ).count();


      // 목표 시간이 지나면 반복 종료
      if (elapsed >= duration_sec)
      {
        break;
      }


      // Go2 Sport API Move 명령 직접 호출
      sport_client_.Move(
        req_,
        vx,
        vy,
        vyaw
      );


      // ROS2 callback 처리
      rclcpp::spin_some(
        shared_from_this()
      );


      // 0.1초 대기
      // 약 10 Hz로 Move 명령 반복 전송
      std::this_thread::sleep_for(
        std::chrono::milliseconds(100)
      );
    }


    // 하나의 이동 구간이 끝나면 명시적으로 정지
    sport_client_.StopMove(req_);


    // 다음 동작 전에 잠시 대기
    std::this_thread::sleep_for(
      std::chrono::seconds(1)
    );
  }


  // ========================================================
  // 전체 Waypoint 주행
  // ========================================================

  void run_waypoint()
  {
    RCLCPP_INFO(
      this->get_logger(),
      "Waypoint sequence start"
    );


    // ------------------------------------------------------
    // 1. 기립
    // ------------------------------------------------------

    RCLCPP_INFO(
      this->get_logger(),
      "Stand Up"
    );

    sport_client_.StandUp(req_);


    // 실제 기립 동작이 완료될 시간을 확보
    std::this_thread::sleep_for(
      std::chrono::seconds(3)
    );


    // ------------------------------------------------------
    // 2. WP1까지 전진
    // ------------------------------------------------------

    RCLCPP_INFO(
      this->get_logger(),
      "WP1 : Forward"
    );

    move_for(
      0.2f,
      0.0f,
      0.0f,
      1.0
    );


    // ------------------------------------------------------
    // 3. 왼쪽 회전
    // ------------------------------------------------------

    RCLCPP_INFO(
      this->get_logger(),
      "Turn Left"
    );

    move_for(
      0.0f,
      0.0f,
      0.5f,
      1.5
    );


    // ------------------------------------------------------
    // 4. WP2까지 전진
    // ------------------------------------------------------

    RCLCPP_INFO(
      this->get_logger(),
      "WP2 : Forward"
    );

    move_for(
      0.2f,
      0.0f,
      0.0f,
      1.0
    );


    // ------------------------------------------------------
    // 5. 오른쪽 회전
    // ------------------------------------------------------

    RCLCPP_INFO(
      this->get_logger(),
      "Turn Right"
    );

    move_for(
      0.0f,
      0.0f,
      -0.5f,
      1.5
    );


    // ------------------------------------------------------
    // 6. WP3까지 전진
    // ------------------------------------------------------

    RCLCPP_INFO(
      this->get_logger(),
      "WP3 : Forward"
    );

    move_for(
      0.2f,
      0.0f,
      0.0f,
      1.0
    );


    // ------------------------------------------------------
    // 7. 최종 정지
    // ------------------------------------------------------

    sport_client_.StopMove(req_);

    RCLCPP_INFO(
      this->get_logger(),
      "Waypoint finished"
    );
  }


  // 프로그램 종료 전 사용할 정지 함수
  void stop()
  {
    sport_client_.StopMove(req_);
  }


private:

  // Go2 Sport API 명령을 사용하기 위한 Client
  SportClient sport_client_;

  // Unitree API Request 메시지
  unitree_api::msg::Request req_;
};


int main(int argc, char **argv)
{
  // ROS2 초기화
  rclcpp::init(argc, argv);


  // ROS2 노드 생성
  auto node =
    std::make_shared<StudentWaypointSport>();


  // DDS discovery를 위한 대기 시간
  std::this_thread::sleep_for(
    std::chrono::seconds(1)
  );


  // 사용자가 확인하기 전에는 로봇을 움직이지 않음
  std::cout << "\n";
  std::cout << "================================\n";
  std::cout << " Sport API Waypoint Test\n";
  std::cout << "================================\n";
  std::cout
    << "주변 공간과 비상정지 리모컨을 확인하세요.\n";
  std::cout
    << "Enter를 누르면 시작합니다.\n";


  std::cin.get();


  // Waypoint 주행 시작
  node->run_waypoint();


  // 프로그램 종료 전 다시 한 번 정지
  node->stop();


  rclcpp::shutdown();

  return 0;
}
