#!/usr/bin/env python3
"""Go2 키보드 조종 — /cmd_vel(Twist) 발행.

go2_sim/supervisor.py 가 구독하는 그 /cmd_vel 그대로 씀(README §5 참고).
그쪽 워치독이 0.5초형(core.py CMD_VEL_TIMEOUT=0.5)이라 — 키를 누른 순간만
한 번 쏘는 게 아니라, 현재 속도 값을 10Hz 타이머로 계속 재발행하다가
'k' 또는 종료 시 0으로 만들어서 보낸다. (README 체크포인트 ② "키를 떼면?"
의 답이 바로 이 워치독 — 여기선 k를 눌러야 정지, 실기체/원본 teleop_twist_keyboard
는 그냥 키를 놓으면 재발행이 끊겨서 0.5초 뒤 자동 정지)

키맵 (교재 5.1 확인 양식과 동일):
  i : 전진(+vx)      , : 후진(-vx)
  j : 좌회전(+wz)     l : 우회전(-wz)
  J : 좌측 게걸음(+vy) L : 우측 게걸음(-vy)
  k : 즉시 정지
  Ctrl+C : 종료(정지 명령 보내고 빠짐)

실행 전: 시뮬레이터(sim.launch.py) + go2_supervisor 가 떠 있고, 로봇이
기립 상태여야 함(엎드린 상태면 관제 노드가 속도 명령을 무시하고 경고 — README §5).
"""
import sys
import termios
import tty

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node

STEP_V = 0.3   # m/s, i/, 한 번에 늘어나는 양
STEP_W = 0.5   # rad/s, j/l 한 번에 늘어나는 양
MAX_V = 1.0    # go2_supervisor 기본 max_v 와 동일(README §5.1)
MAX_W = 1.5
PUBLISH_HZ = 10.0  # 0.5초 워치독보다 훨씬 빠르게 재발행

KEY_HELP = """\
Go2 키보드 조종 (Ctrl+C 로 종료)
---------------------------
   i        : 전진
   ,        : 후진
 j     l    : 좌/우 회전
 J     L    : 좌/우 게걸음(strafe)
   k        : 정지
---------------------------
"""


def read_key(settings) -> str:
    tty.setraw(sys.stdin.fileno())
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


class Go2Teleop(Node):
    def __init__(self):
        super().__init__("go2_keyboard_teleop")
        self.pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.vx = self.vy = self.wz = 0.0
        self.create_timer(1.0 / PUBLISH_HZ, self._publish)

    def _publish(self):
        tw = Twist()
        tw.linear.x, tw.linear.y, tw.angular.z = self.vx, self.vy, self.wz
        self.pub.publish(tw)

    def apply(self, key: str) -> bool:
        """True 를 리턴하면 종료."""
        if key == "i":
            self.vx = clamp(self.vx + STEP_V, -MAX_V, MAX_V)
        elif key == ",":
            self.vx = clamp(self.vx - STEP_V, -MAX_V, MAX_V)
        elif key == "j":
            self.wz = clamp(self.wz + STEP_W, -MAX_W, MAX_W)
        elif key == "l":
            self.wz = clamp(self.wz - STEP_W, -MAX_W, MAX_W)
        elif key == "J":
            self.vy = clamp(self.vy + STEP_V, -MAX_V, MAX_V)
        elif key == "L":
            self.vy = clamp(self.vy - STEP_V, -MAX_V, MAX_V)
        elif key == "k":
            self.vx = self.vy = self.wz = 0.0
        elif key == "\x03":  # Ctrl+C
            return True
        self.get_logger().info(
            f"vx={self.vx:+.2f} vy={self.vy:+.2f} wz={self.wz:+.2f}",
            throttle_duration_sec=0.0,
        )
        return False


def main():
    settings = termios.tcgetattr(sys.stdin)
    rclpy.init()
    node = Go2Teleop()
    print(KEY_HELP)
    try:
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0.0)
            key = read_key(settings)
            if node.apply(key):
                break
    except KeyboardInterrupt:
        pass
    finally:
        # 정지 명령을 마지막으로 한 번 더 보내고 종료(안전)
        node.vx = node.vy = node.wz = 0.0
        node._publish()
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
