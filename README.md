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
│   ├── *.md               # 미션별 실습 정리 (지지영역, 상태전이, 상태전이판졀, 실패경로추적, 파라미터, 모니터링콜규약)
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
- Git 브랜치·병합·충돌 해결 실습(`Day1_4.7.2~5`): `git switch -c`로 실험 브랜치 생성 → 파라미터 값 변경·커밋 → `merge` 시 충돌 발생·수동 해결까지 직접 재현
- ROS2 네트워크 격리 실습(`Day2_5.12.1~3`): `ROS_DOMAIN_ID`를 다르게 주면 같은 컴퓨터 안에서도 talker/listener가 서로 안 보이는 것을 확인하고, 도메인을 맞춰 통신 복구 + `turtle_teleop_key`로 키 입력이 토픽으로 발행되는 것 확인

## Week 2 — G1 휴머노이드 실습

- G1 안전 수칙: 행어 미거치 단독 기립 금지, 2인 이상 작업(비상정지 전담자 포함), 보행 시 반경 2m 확보
- 관절 구성(하체/허리/팔) 및 균형 제어 원리(support polygon, 자세 보상 vs 스텝) 학습
- 지지 영역 체감 실험(`지지영역.md`): 두 발 벌리기/한 발로 서기/상체 앞으로 기울이기를 직접 해보며 지지 영역(두 발 사이 면적)-무게중심-자세 보상-스텝 전환의 관계를 몸으로 확인
- 거치 → 준비 → 기립 → 보행 순서와 `Damp()`를 기준점으로 한 안전 절차 이해
- 상태 전이(상태 기계) 미션(`상태전이.md`, `상태전이판졀.md`): `Damp → 준비/기립 → 균형 → 상체 모션 → 복귀` 흐름을 뜯어보고, 전이 사이 대기(sleep)가 필요한 이유·상황별 안전한/안전하지 않은 전이 여부 판별 연습
- 실패 경로 추적(`실패경로추적.md`): 기립 전이 실패·모션 중 Ctrl+C·통신 끊김 시나리오별로 로봇이 남는 상태와 예외 처리(Damp 복귀) 필요성 분석
- 모니터링 콜 규약(`모니터링콜규약.md`) 숙지: "상태 정상"/"토크 이상 — ○○ 관절"/"기울기 증가 중"/"모니터링 끊김" 등 상황별 콜을 반사적으로 나오도록 정리
- MuJoCo 기반 시뮬레이션(`g1-edu`)에서 파라미터 조정을 통한 보행 균형 실험
  - `파라미터.md`: 보행 속도/보폭/걸음 주기/발 높이 등 파라미터 후보와 추정 의미를 코드 확인 전 먼저 정리
  - `파라미터_관찰표_g1.md`: vx/step_period/step_height/com_shift 등을 한 번에 하나씩 바꿔가며 완주·낙상 경계 관찰(교재 4.3~4.4), 몸통을 밀어 외란(방향별 회복/낙상)을 관찰하는 실험 병행
- 상체 동작 시퀀스 설계 및 실기체(`g1-real`) 제어 스크립트 작성

## Week 3 — RM75 로봇팔 + 그리퍼 실습

- RM75 로봇팔에 EG2-4C2 그리퍼 모델을 결합, Gazebo 시뮬레이션 환경에서 구동 확인
- MoveIt 워크플로우(목표 지정 → Plan → Execute) 실습: RViz 인터랙티브 마커로 목표 pose 지정 후 계획·실행
- 팔+그리퍼 URDF/Xacro 결합을 스크립트 3단계로 직접 재현
  1. `fetch_gripper_model.sh` — RealManRobot 공식 저장소(`URDF-to-XACRO`)에서 EG2-4C2 그리퍼 모델(mesh/urdf)을 가져옴
  2. `build_arm_gripper_urdf.sh` — 팔(`rm_75.urdf.xacro`)과 그리퍼(`jaw.urdf.xacro`)를 `arm_jaw_joint`(고정 조인트)로 결합한 `arm_gripper.urdf.xacro` 생성
     - `arm_jaw_joint`로 팔 끝(`Link7`)과 그리퍼 베이스(`4C2_baselink`) 연결, 실측 보정값(z=-0.009, rpy z=-1.57) 적용
     - 손끝 기준점 `grasp_tcp`(Link7 기준 z+0.12) 추가
  3. `display_rm75_jaw.sh` — robot_state_publisher + joint_state_publisher_gui + rviz2 launch 파일 생성/실행
- `display_rm75_jaw_checklist.md` 기준으로 RViz 결합 결과 검증: 팔+그리퍼 표시, 관절 8개(joint1~7 + jaw_Joint1) 확인, `jaw_Joint1` 슬라이더로 그리퍼 개폐, TF에서 `grasp_tcp` 프레임 위치 확인

## 개발 환경

- OS: Ubuntu 22.04.5 LTS (커널 5.15.0-186-generic)
- Python 3.10.12
- ROS2, MuJoCo 기반 시뮬레이션 환경

자세한 환경 정보는 [env_report.md](env_report.md) 참고.
