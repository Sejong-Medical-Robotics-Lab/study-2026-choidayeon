import rclpy
from rclpy.node import Node
import time
import sys

# (참고) 실제 교육용 패키지의 클라이언트 임포트 경로에 맞게 사용하세요.
# from g1edu.client import G1RobotClient 

class Mission3ControlNode(Node):
    def __init__(self):
        super().__init__('mission3_control_node')
        self.get_logger().info("미션 3 제어 노드가 시작되었습니다.")

    def run_mission(self):
        # ① 초기화 : 클라이언트 준비
        self.get_logger().info("[1/6] 초기화 : 클라이언트 준비 중...")
        # robot = G1RobotClient()
        time.sleep(1)

        try:
            # ② 상태 확인 : 현재 모드·에러 확인
            self.get_logger().info("[2/6] 상태 확인 : 현재 모드 및 에러 확인 중...")
            # mode = robot.GetMode()
            # error = robot.GetLastError()
            # self.get_logger().info(f"현재 모드: {mode}, 에러: {error}")

            # ③ Damp() : 알려진 안전 상태에서 출발
            self.get_logger().info("[3/6] Damp() : 안전 상태 진입...")
            # robot.Damp()
            time.sleep(1)

            # ④ 기립 전이 : 명령 → 전이 완료를 기다림
            self.get_logger().info("[4/6] 기립 전이 : StandUp 명령 및 대기...")
            # robot.StandUp()
            # 기립 완료될 때까지 대기 (상태 전이 관점)
            time.sleep(3.0) 
            self.get_logger().info(" -> 기립 완료 (balance_stand 진입)")

            # ⑤ 모션 실행 : 상체 모션 및 보행 시퀀스
            self.get_logger().info("[5/6] 모션 실행 : 목적 동작 수행 중...")
            # robot.PlayAction("wave")     # 오른팔 인사 등
            time.sleep(2.0)
            
            # ⑥ 정리 : StopMove/자세 복귀 → Damp
            self.get_logger().info("[6/6] 정리 : 자세 복귀 및 안전 종료 준비...")
            # robot.StopMove()
            time.sleep(1)
            
            # robot.Damp()
            self.get_logger().info("미션 3 시퀀스가 성공적으로 완료되었습니다.")

        except Exception as e:
            # ※ try/except : 어느 단계에서 실패해도 except에서 Damp로 수렴 (안전 장치)
            self.get_logger().error(f"오류 발생: {e}")
            self.get_logger().warn("긴급 비상 정지: 안전 확보를 위해 Damp() 상태로 전환합니다.")
            try:
                # robot.StopMove()
                # robot.Damp()
                pass
            except Exception as sub_e:
                self.get_logger().error(f"비상 정지 중 추가 에러: {sub_e}")

def main(args=None):
    rclpy.init(args=args)
    node = Mission3ControlNode()
    
    try:
        node.run_mission()
    except KeyboardInterrupt:
        node.get_logger().info("사용자에 의해 중단되었습니다 (Ctrl+C 감지).")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
