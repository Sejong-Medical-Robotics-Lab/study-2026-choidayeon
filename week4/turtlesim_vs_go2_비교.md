# turtlesim(Week1) vs Go2(Week4) 비교

Week1에서 처음 ROS2 통신 구조를 익힐 때 쓴 `turtlesim`과, Week4에서 Gazebo에
올린 `Go2`를 같은 축으로 비교해서 "장난감 시뮬레이터"와 "물리 기반 로봇
시뮬레이터"의 차이를 정리.

| 비교 축 | turtlesim | Go2 (Gazebo) |
|---|---|---|
| 차원 | 2D (평면 위 거북이) | 3D (중력·충돌이 있는 공간) |
| 물리 엔진 | 없음 — 좌표를 그대로 갱신 | 있음(Gazebo, dartsim) — 중력·충돌·관성 계산 |
| 제어 입력 | `/turtle1/cmd_vel` (`geometry_msgs/Twist`) | `/cmd_vel` (`geometry_msgs/Twist`) — 같은 메시지 타입, 다만 Go2는 기립 상태가 아니면 무시됨 |
| 자유도 | 사실상 2 DOF(평면 위치+heading) | 몸통 6 DOF + 다리 12 DOF(hip·thigh·calf × 4다리) |
| 센서 | 없음 | IMU(`imu` 링크), LiDAR(`lidar_link`) |
| 좌표계/TF | 없음(단일 pose 토픽만) | `odom → base → … → lidar_link` tf 트리 |
| 노드 구성 | `turtlesim_node` 1개 | Gazebo server/gui + `go2_sim` 관제 노드(`supervisor`) 등 다중 |
| 다중 개체 | 거북이 여러 마리 스폰 → 추적(pursuit) 실습 | 로봇 1대, 대신 다리 4개가 각자 목표 관절각을 따라감(trot 패턴) |
| 실행 확인 방법 | `ros2 topic echo`로 pose 값 확인 | `gz service`로 엔티티 pose 조회 + 스크린샷으로 렌더링 확인 |
| 배웠던 핵심 | ROS2 노드·토픽 발행/구독 감 잡기 | URDF→SDF 변환, 물리 시뮬레이터에 로봇을 "올린다"는 것의 실제 의미 |

## 한 줄 정리
turtlesim은 "토픽이 오가면 화면 좌표가 바뀐다"는 통신 구조를 보여주는
장난감이었다면, Go2는 그 위에 물리(중력·충돌)·형상(URDF/SDF)·다관절
제어까지 다 얹힌 것 — 같은 `Twist` 메시지를 보내도 turtlesim은 즉시
반영되지만 Go2는 "기립 상태인가", "물리적으로 가능한 움직임인가"까지
따져야 함
