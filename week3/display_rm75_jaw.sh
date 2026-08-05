#!/usr/bin/env bash
set -euo pipefail

cat > ~/ros2_ws/src/ros2_rm_robot/rm_description/launch/rm_75_jaw_display.launch.py << 'PYEOF'
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command, FindExecutable
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    share = get_package_share_directory('rm_description')
    xacro_file = os.path.join(share, 'urdf', 'rm_75_with_jaw.urdf.xacro')

    robot_description = ParameterValue(
        Command([FindExecutable(name='xacro'), ' ', xacro_file]),
        value_type=str,
    )

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{'robot_description': robot_description}],
            output='screen',
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', os.path.join(share, 'rviz', 'rm_75.rviz')],
        ),
    ])
PYEOF

python3 -m py_compile ~/ros2_ws/src/ros2_rm_robot/rm_description/launch/rm_75_jaw_display.launch.py && echo "문법 OK"

cd ~/ros2_ws
colcon build --packages-select rm_description
source install/setup.bash
ros2 launch rm_description rm_75_jaw_display.launch.py
