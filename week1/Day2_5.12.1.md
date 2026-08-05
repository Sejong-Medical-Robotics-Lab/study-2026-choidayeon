#Day2_5.12.1
```
$ROS_DOMAIN_ID=7 ros2 run demo_nodes_cpp talker
$ROS_DOMAIN_ID=8 ros2 run demo_nodes_py listener
$ROS_DOMAIN_ID=7 ros2 run demo_nodes_py listener

확인 포인트 : 같은 컴퓨터 안에서도 도메인이 다르면 서로 보이지 않음. 옆 사람과 도메인을 맞추면
노트북 두 대 사이에서도 통신이 됨
