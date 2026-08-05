# 2026 하계 로봇 플랫폼 교육 학습 기록

세종대학교 Medical Robotics Lab 하계 로봇 플랫폼 교육 과정에서의 학습 기록 저장소입니다.
ROS2 기초부터 Unitree G1 휴머노이드 제어까지의 실습 내용과 학습일지를 주차별로 정리합니다.

## 폴더 구조

```
.
├── env_report.md      # 개발 환경 리포트 (OS, 커널, Python 버전 등)
├── week1/              # Week 1 — ROS2 공통교육
│   ├── 학습일지/        # 일자별 학습일지 (Linux/Git, ROS2 구조, rviz2 등)
│   ├── logs/            # 실습 로그
│   ├── data/, backup/   # 실습용 데이터 및 백업
│   ├── 3.7도전미션/      # 도전 미션 산출물 (data/logs/results)
│   ├── demo.launch.py   # turtlesim talker/listener 예제 launch 파일
│   ├── my_first_bag/    # 첫 rosbag 기록
│   └── Day1_*.md        # 일차별 실습 정리
├── week2/               # Week 2 — Unitree G1 휴머노이드 실습
│   ├── 학습일지/          # 일자별 학습일지 (균형 제어, 안전 수칙 등)
│   ├── g1-edu/            # G1 교육용 시뮬레이션(MuJoCo) 및 제어 코드 (하위 저장소)
│   ├── g1-real/           # G1 실기체 제어/모니터링 스크립트 (하위 저장소)
│   ├── 5page_mission3.py, 5page_mission4.py
│   └── 상체시퀀스 설계     # 상체 동작 시퀀스 설계 메모
└── week3/               # Week 3 — RM75 로봇팔 + 그리퍼 실습
    ├── 학습일지/                       # 일자별 학습일지
    ├── rm75-edu/                       # RM75 교육용 ROS2 패키지 (하위 저장소)
    ├── fetch_gripper_model.sh          # EG2-4C2 그리퍼 모델 파일 가져오기
    ├── build_arm_gripper_urdf.sh       # 팔+그리퍼 결합 URDF/Xacro 생성
    ├── display_rm75_jaw.sh             # RViz 표시용 launch 파일 생성/실행
    └── display_rm75_jaw_checklist.md   # RViz 표시 후 확인 포인트
```

## Week 1 — ROS2 공통교육

- Linux 터미널, Git/GitHub 기본 사용법 학습
- ROS2 노드/토픽 구조 이해, talker-listener 통신 실습
- turtlesim을 활용한 다중 노드 제어(추적 로봇) 실습
- rviz2를 통한 3D 공간 데이터 시각화
- Go2 / G1 / FR3 플랫폼 시연회 관람 및 관찰 기록

## Week 2 — G1 휴머노이드 실습

- G1 안전 수칙: 행어 미거치 단독 기립 금지, 2인 이상 작업(비상정지 전담자 포함), 보행 시 반경 2m 확보
- 관절 구성(하체/허리/팔) 및 균형 제어 원리(support polygon, 자세 보상 vs 스텝) 학습
- 거치 → 준비 → 기립 → 보행 순서와 `Damp()`를 기준점으로 한 안전 절차 이해
- MuJoCo 기반 시뮬레이션(`g1-edu`)에서 파라미터 조정을 통한 보행 균형 실험
- 상체 동작 시퀀스 설계 및 실기체(`g1-real`) 제어 스크립트 작성

## Week 3 — RM75 로봇팔 + 그리퍼 실습

- RM75 로봇팔에 EG2-4C2 그리퍼 모델을 결합, Gazebo 시뮬레이션 환경에서 구동 확인
- MoveIt 워크플로우(목표 지정 → Plan → Execute) 실습: RViz 인터랙티브 마커로 목표 pose 지정 후 계획·실행
- RealManRobot 공식 저장소에서 EG2-4C2 그리퍼 모델(mesh/urdf)을 가져와 팔과 결합한 Xacro 생성
  - `arm_jaw_joint`로 팔 끝(`Link7`)과 그리퍼 베이스(`4C2_baselink`) 연결, 실측 보정값(z=-0.009, rpy z=-1.57) 적용
  - 손끝 기준점 `grasp_tcp`(Link7 기준 z+0.12) 추가
- RViz 표시용 launch 파일 작성 및 관절 슬라이더(joint1~7 + jaw_Joint1)로 그리퍼 개폐 확인

## 개발 환경

- OS: Ubuntu 22.04.5 LTS (커널 5.15.0-186-generic)
- Python 3.10.12
- ROS2, MuJoCo 기반 시뮬레이션 환경

자세한 환경 정보는 [env_report.md](env_report.md) 참고.
