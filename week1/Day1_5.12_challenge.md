echo "# ROS2 환경 점검 ($(date +%F))"
echo "- ROS_DISTRO: ${ROS_DISTRO:-(미설정!)}"
echo "- ROS_DOMAIN_ID: ${ROS_DOMAIN_ID:-0(기본값)}"
echo "- ros2 명령: $(command -v ros2 || echo 없음)"
echo "- 설치 패키지 수: $(ros2 pkg list 2>/dev/null | wc -l)"
ros2 doctor --report 2>/dev/null | grep -A2 "NETWORK" | head -5


# ROS2 \ud658\uacbd \uc810\uac80 (2026-07-28) 
bash: !: event not found 
- ROS_DOMAIN_ID: 0(\uae30\ubcf8\uac12) 
- ros2 \uba85\ub839: /opt/ros/humble/bin/ros2 
- \uc124\uce58 \ud328\ud0a4\uc9c0 \uc218: 274    
NETWORK CONFIGURATION
inet         : 127.0.0.1
inet4        : ['127.0.0.1']
