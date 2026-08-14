import math

import numpy as np

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from geometry_msgs.msg import Twist
from sensor_msgs.msg import PointCloud2


class StudentLidarStop(Node):

    def __init__(self):

        # ROS2 노드 이름 설정
        super().__init__('student_lidar_stop')


        # ==================================================
        # /cmd_vel Publisher
        # ==================================================
        #
        # 장애물 판단 결과에 따라
        # 전진 또는 정지 속도 명령을 발행한다.
        #
        self.publisher_ = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )


        # ==================================================
        # Hesai LiDAR Subscriber
        # ==================================================
        #
        # /lidar_points의 PointCloud2 데이터를 구독한다.
        #
        # 새로운 데이터가 들어오면
        # lidar_callback() 함수가 실행된다.
        #
        self.subscription = self.create_subscription(
            PointCloud2,
            '/lidar_points',
            self.lidar_callback,
            qos_profile_sensor_data
        )


        # ==================================================
        # 장애물 판단 상태
        # ==================================================

        # False
        # → 주행 가능

        # True
        # → 장애물이 가까워 정지
        self.stopped = False


        # 장애물이 이 거리보다 가까우면 정지
        self.stop_distance = 0.6

        # 장애물이 이 거리보다 멀어져야 다시 출발
        self.restart_distance = 0.8


        # 가장 최근에 측정한 최소 거리
        self.min_distance = None


        # ==================================================
        # 속도 명령 Timer
        # ==================================================
        #
        # 0.1초마다 publish_cmd()를 실행한다.
        #
        # 즉 약 10 Hz로 /cmd_vel을 계속 발행한다.
        #
        self.cmd_timer = self.create_timer(
            0.1,
            self.publish_cmd
        )


        self.get_logger().info(
            'Student LiDAR stop node started'
        )


    # ======================================================
    # LiDAR 데이터 처리
    # ======================================================

    def lidar_callback(self, msg):

        # --------------------------------------------------
        # Hesai PointCloud2 데이터 구조
        # --------------------------------------------------
        #
        # PointCloud2의 data는 바이너리 형태이므로
        # 각 값의 위치와 자료형을 정의한다.
        #
        point_dtype = np.dtype({

            'names': [
                'x',
                'y',
                'z',
                'intensity',
                'ring',
                'timestamp'
            ],

            'formats': [
                '<f4',
                '<f4',
                '<f4',
                '<f4',
                '<u2',
                '<f8'
            ],

            'offsets': [
                0,
                4,
                8,
                12,
                16,
                18
            ],

            'itemsize': msg.point_step
        })


        # --------------------------------------------------
        # PointCloud2 byte 데이터 → NumPy 배열
        # --------------------------------------------------

        points = np.frombuffer(
            msg.data,
            dtype=point_dtype,
            count=msg.width * msg.height
        )


        # PointCloud가 비어 있다면 처리하지 않는다.
        if points.size == 0:
            return


        # 각 점의 x, y, z 좌표 가져오기
        x = points['x']
        y = points['y']
        z = points['z']


        # ==================================================
        # Go2 전방 영역(ROI) 선택
        # ==================================================
        #
        # 모든 LiDAR 점을 사용하는 것이 아니라
        # Go2가 앞으로 이동할 때 충돌할 가능성이 있는
        # 전방 영역의 점만 선택한다.
        #
        mask = (
            np.isfinite(x) &
            np.isfinite(y) &
            np.isfinite(z) &

            # 로봇 바로 주변의 점 제외
            (x > 0.2) &

            # 전방 최대 3 m까지 검사
            (x < 3.0) &

            # 좌우 약 ±0.4 m
            (np.abs(y) < 0.4) &

            # 지나치게 높거나 낮은 점 제외
            (z > -0.5) &
            (z < 0.5)
        )


        # ==================================================
        # 전방 영역에 유효한 점이 없는 경우
        # ==================================================

        if not np.any(mask):

            # 현재 검출된 최소 거리 없음
            self.min_distance = None


            # 이전에 장애물 때문에 정지 중이었다면
            # 장애물이 사라진 것으로 보고 다시 주행 가능 상태
            if self.stopped:

                self.stopped = False

                self.get_logger().info(
                    'GO resumed | no obstacle'
                )

            return


        # ==================================================
        # 전방 영역의 점만 추출
        # ==================================================

        front_x = x[mask]
        front_y = y[mask]


        # ==================================================
        # 각 점까지의 평면 거리 계산
        #
        # distance² = x² + y²
        # ==================================================

        distance_sq = (
            front_x * front_x
            + front_y * front_y
        )


        # 가장 가까운 점의 index
        min_index = np.argmin(
            distance_sq
        )


        # 실제 최소 거리 계산
        self.min_distance = math.sqrt(
            float(
                distance_sq[min_index]
            )
        )


        # ==================================================
        # 장애물 판단 — 히스테리시스
        # ==================================================

        # --------------------------------------------------
        # 주행 중이며 장애물이 0.6 m보다 가까우면 정지
        # --------------------------------------------------

        if (
            not self.stopped
            and self.min_distance < self.stop_distance
        ):

            self.stopped = True

            self.get_logger().info(
                f'STOP triggered | '
                f'{self.min_distance:.2f} m'
            )


        # --------------------------------------------------
        # 정지 중이며 장애물이 0.8 m보다 멀어지면 재출발
        # --------------------------------------------------

        elif (
            self.stopped
            and self.min_distance > self.restart_distance
        ):

            self.stopped = False

            self.get_logger().info(
                f'GO resumed | '
                f'{self.min_distance:.2f} m'
            )


    # ======================================================
    # 속도 명령 발행
    # ======================================================

    def publish_cmd(self):

        # Twist 메시지 생성
        cmd = Twist()


        # 장애물이 가까우면 정지
        if self.stopped:

            cmd.linear.x = 0.0


        # 장애물이 없으면 전진
        else:

            # 전진 속도 0.2 m/s
            cmd.linear.x = 0.2


        # 좌우 이동 없음
        cmd.linear.y = 0.0

        # 회전 없음
        cmd.angular.z = 0.0


        # /cmd_vel 발행
        self.publisher_.publish(cmd)


    # ======================================================
    # 프로그램 종료 시 사용할 정지 함수
    # ======================================================

    def publish_stop(self):

        stop = Twist()

        stop.linear.x = 0.0
        stop.linear.y = 0.0
        stop.angular.z = 0.0

        self.publisher_.publish(stop)


# ==========================================================
# 프로그램 시작점
# ==========================================================

def main(args=None):

    # ROS2 초기화
    rclpy.init(args=args)


    # LiDAR Stop 노드 생성
    node = StudentLidarStop()


    try:

        # Subscriber callback과
        # Timer callback을 계속 처리
        rclpy.spin(node)


    except KeyboardInterrupt:

        pass


    finally:

        # 종료 전에 반드시 정지 명령 전송
        node.publish_stop()


        # 노드 제거
        node.destroy_node()


        # ROS2 종료
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
