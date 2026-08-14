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
├── week3/               # Week 3 — RM75 로봇팔 + 그리퍼 실습
│   ├── 학습일지/                       # 일자별 학습일지
│   ├── rm75-edu/                       # RM75 교육용 ROS2 패키지 (하위 저장소)
│   ├── fetch_gripper_model.sh          # EG2-4C2 그리퍼 모델 파일 가져오기
│   ├── build_arm_gripper_urdf.sh       # 팔+그리퍼 결합 URDF/Xacro 생성
│   ├── display_rm75_jaw.sh             # RViz 표시용 launch 파일 생성/실행
│   ├── display_rm75_jaw_checklist.md   # RViz 표시 후 확인 포인트
│   ├── 그리퍼명령.md                    # 그리퍼 위치/힘 제어 토픽 명령 정리
│   ├── pick_place.py                   # MoveIt 액션 직접 호출 픽앤플레이스(고정 좌표)
│   ├── grasp_test.py                   # CLI 파라미터 기반 픽앤플레이스 검증 하네스
│   ├── vision_to_base_test.py          # 비전(YOLO+깊이) → base_link 좌표 변환 검증
│   ├── vision_approach_test.py         # 비전 좌표로 물체 앞까지 접근(파지 제외)
│   ├── vision_grasp_test.py            # 비전 기반 파지 확장용(현재 approach와 동일)
│   └── frames_2026-08-05_13.32.54.pdf  # 당시 TF 트리 스냅샷
└── week4/               # Week 4 — Go2 사족보행 + Gazebo 실습
    ├── 학습일지/                       # 일자별 학습일지 (Gazebo Classic/신버전, arm64 패키지 이슈, URDF→SDF 변환 등)
    ├── go2-edu/                        # Go2 교육용 ROS2 패키지 (하위 저장소)
    ├── unitree_ros2/                   # Unitree 공식 ROS2 지원 패키지 (하위 저장소, cyclonedds_ws + example)
    ├── Gazebo_설명.md                  # Gazebo 개념 정리 (구성요소, Classic vs 신버전, SDF, ROS2 연동)
    ├── Go2_Gazebo_Harmonic_이식.md     # URDF 정리·SDF 변환·월드 이식 코드 및 기립 자세 계산 기록
    ├── 구성요소.md                     # Go2 구성 요소 지도 그리기 (다리·관절·센서·관제 노드)
    ├── turtlesim_vs_go2_비교.md        # Week1 turtlesim ↔ Go2 비교표
    ├── 공식사양조사.md                 # Unitree 공식 사양 조사 + URDF 수치 대조
    ├── 배터리확인경로.md               # 실기체/시뮬레이션 배터리 확인 경로 조사
    ├── go2_keyboard_teleop.py          # /cmd_vel 키보드 조종 스크립트
    ├── 키보드조작.md                   # 실기체 키보드 조작 아키텍처(teleop→/cmd_vel→go2_nav_bridge→Sport API)
    ├── 키보드조작실행.md               # 실기체 teleop_twist_keyboard 실행 절차 + 안전수칙
    ├── student_sport_demo.cpp          # Sport API 직접 호출 노드 (StandUp/StandDown/StopMove 메뉴)
    ├── 코드구조확인.md                 # student_sport_demo.cpp의 SportClient·명령 구조 정리
    ├── student_waypoint_sport.cpp      # Sport API Move()로 직접 구현한 Waypoint 순회(전진·좌회전·전진·우회전·전진)
    ├── student_lidar_stop.py           # /lidar_points 기반 장애물 감지 정지·재출발(히스테리시스) 노드
    └── 실행전확인.md                   # 실기체 실행 전 코드 이해도 자가 점검 체크리스트(LiDAR stop)
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

- RM75 구성 요소 지도 그리기(`구성요소.md`): 관절 7개(J1~J7) + 일체형 관절 모듈 + 내장 컨트롤러 + 그리퍼 + 비상정지 버튼 + 제어 소프트웨어를 어깨(J1~J3)-팔꿈치(J4)-손목(J5~J7) 대응으로 정리
- 여유자유도(7DOF) 체감 실험(`여자유도.md`): 손끝 위치·자세를 고정한 채 팔꿈치만 움직여보며 남는 자유도 확인, 팔을 뻗을수록 손목 회전 여유가 줄어드는 것을 직접 관찰
- RM75 로봇팔에 EG2-4C2 그리퍼 모델을 결합, Gazebo 시뮬레이션 환경에서 구동 확인
- MoveIt 워크플로우(목표 지정 → Plan → Execute) 실습: 목표 지정(Set Goal)·경로 계획(Plan)·실행(Execute)이 분리된 3단계이고, Plan 단계에서 충돌 검사·IK 계산이 먼저 끝나야 Execute가 가능하다는 것을 확인 — RViz 인터랙티브 마커로 목표 pose를 손으로 끌어 지정 → Plan으로 초록색 trajectory 확인(충돌 없이 도달 가능할 때까지 목표를 조금씩 조정) → Execute로 Gazebo 상 팔+그리퍼가 실제로 움직이는 것까지 확인
- 팔+그리퍼 URDF/Xacro 결합을 스크립트 3단계로 직접 재현
  1. `fetch_gripper_model.sh` — RealManRobot 공식 저장소(`URDF-to-XACRO`)에서 EG2-4C2 그리퍼 모델(mesh/urdf)을 가져옴
  2. `build_arm_gripper_urdf.sh` — 팔(`rm_75.urdf.xacro`)과 그리퍼(`jaw.urdf.xacro`)를 `arm_jaw_joint`(고정 조인트)로 결합한 `arm_gripper.urdf.xacro` 생성
     - `arm_jaw_joint`로 팔 끝(`Link7`)과 그리퍼 베이스(`4C2_baselink`) 연결, 실측 보정값(z=-0.009, rpy z=-1.57) 적용
     - 손끝 기준점 `grasp_tcp`(Link7 기준 z+0.12) 추가
  3. `display_rm75_jaw.sh` — robot_state_publisher + joint_state_publisher_gui + rviz2 launch 파일 생성/실행
- `display_rm75_jaw_checklist.md` 기준으로 RViz 결합 결과 검증: 팔+그리퍼 표시, 관절 8개(joint1~7 + jaw_Joint1) 확인, `jaw_Joint1` 슬라이더로 그리퍼 개폐, TF에서 `grasp_tcp` 프레임 위치 확인 (`frames_2026-08-05_13.32.54.pdf`로 당시 TF 트리 스냅샷 저장)
- MoveIt 마커·예제 코드 분석(`마커관찰.md`, `예제해부.md`): 인터랙티브 마커의 공(위치)/고리(자세) 차이, plan 성공 확인 없이 execute를 호출하면 안 되는 이유, 쿼터니언 기반 orientation 재사용 패턴 정리
- 나만의 파지 시퀀스 설계(`나만의시퀀스설계.md`): 홈 → P 위 접근 → P로 하강 → 복귀 4단계로 목표 지정 방법·성공 확인·실패 시 대응을 미리 설계
- effort 필드 관찰 도전 미션(`effort필드관찰.md`): demo 모드의 effort 값(0/미채움) 확인, 실기체에서는 관절 토크 추정치가 다르게 나타날 것이라는 예측 정리
- 그리퍼 단독 명령 정리(`그리퍼명령.md`): `set_gripper_position_cmd`(위치 제어, 0~1000)와 `set_gripper_pick_on_cmd`(힘 제어, speed/force 지정) 두 토픽의 차이를 정리 — 위치 제어로 닫으면 물체에 막혔을 때 과부하 보호로 힘을 안 놓아 이송 중 미끄러지므로, 실제 파지에는 지정한 힘을 계속 유지하는 `pick_on`을 써야 한다는 이유까지 확인. 그리퍼 개방도는 ROS 토픽으로는 못 읽고 웹 UI에서만 확인 가능하다는 제약도 기록
- 픽앤플레이스 시뮬레이션 스크립트 2종 작성(`pick_place.py`, `grasp_test.py`) — MoveIt의 `MoveGroup`/`ExecuteTrajectory` 액션과 `ApplyPlanningScene`/`GetCartesianPath` 서비스를 직접 호출하는 방식
  - `pick_place.py`: 박스 1개를 고정 좌표로 pick→place. **닫기 전에 attach, 열고 살짝 후퇴한 뒤에 detach**해야 한다는 순서 규칙을 코드에 못박음(반대로 하면 그리퍼 여닫기가 충돌 판정으로 실패)
  - `grasp_test.py`: CLI 인자(`--shape box/cylinder/sphere`, `--pos`, `--radius`/`--height`/`--size`, `--grasp-dir top/front` 등)로 임의 물체를 잡아보는 범용 검증 하네스로 확장 — 물체 폭에서 그리퍼 닫힘값을 역산하는 `closed_value_for_width()`, 위/측면 두 파지 방향(top=위에서 하강, front=측면 감싸쥐기) 지원
- RealSense + YOLO 비전 파이프라인 검증 스크립트 3종 (`vision_to_base_test.py`, `vision_approach_test.py`, `vision_grasp_test.py`) — "05 테스트" 시리즈로 카메라 좌표 → 로봇 제어까지 단계적으로 검증
  - `vision_to_base_test.py`(A단계, v3): YOLOv8로 물체(bottle) 검출 → bbox 중앙 ROI의 median 깊이로 카메라 좌표 계산 → `camera_color_optical_frame → base_link` TF로 변환. v1 대비 (1) TF를 별도 스레드에서 계속 spin해 200Hz 스트림 버퍼 밀림 방지 (2) TF 나이(`MAX_TF_AGE`) 검사로 오래된 변환 거부 (3) 팔이 완전히 멈춘 뒤에만 "READY"로 측정 확정 (4) 깊이 센서가 주는 표면점을 원통 반지름만큼 시선 방향으로 밀어 중심축으로 보정(`RADIUS_COMPENSATION`) 하는 네 가지를 개선 — 여러 자세에서 같은 물체를 반복 측정해 평균/산포/오차(mm 단위)까지 계산
  - `vision_approach_test.py`(B단계): A단계 좌표 파이프라인으로 물병 위치를 구하고, `MoveJ_P`로 물병 앞 `APPROACH_BACK`만큼 떨어진 지점까지 접근만 수행(파지는 안 함). `GRASP_OFFSET`(0.098m)은 드래그 티칭으로 직접 물병을 감싼 뒤 `tf2_echo`로 역산한 실측값. MoveIt을 거치지 않아 충돌 검사가 없으므로 X/Y/Z 허용 범위·최대 이동량(`MAX_STEP`)을 코드 안에서 직접 점검해 범위를 벗어나면 발행 자체를 거부하는 안전장치를 넣음
  - `vision_grasp_test.py`: B단계를 확장해 실제 파지까지 이어갈 목적으로 만든 파일이지만, 현재는 `vision_approach_test.py`와 내용이 동일함(diff 없음) — 다음 단계(그리퍼 닫기·들어올리기 추가)가 아직 반영 전인 진행 중 상태
- 실기체 체험 기록(`실습기록.md`): 위치 제어 상태에서 밀어보기(충돌 보호 작동 확인), 직접 교시(부드럽게 따라오고 손 놓으면 그 자리 유지), 교시 자세 재생까지 실물 로봇으로 체험

## Week 4 — Go2 사족보행 + Gazebo 실습

- Gazebo Classic(`gazebo`, `gzserver`/`gzclient`)과 신버전 Gazebo(Ignition → Fortress/Garden/Harmonic, `gz sim`) 두 계보가 명령어·플러그인 이름(`libgazebo_ros_*.so` vs `gz-sim-*-system`)·설정 방식에서 전혀 다르다는 것을 확인
- 현재 실습 환경(Ubuntu 22.04 **arm64**)에서 Gazebo Classic 바이너리 자체가 Ubuntu 공식 저장소·OSRF 공식 저장소 어디에도 없는 것을 `apt-cache policy`/`apt-cache madison`으로 진단
- 대체재인 Ignition Fortress도 ROS 2 arm64 저장소 자체의 의존성 결함(`libignition-gazebo6`가 요구하는 `libignition-sensors6 >= 6.8.1`이 arm64엔 6.8.0까지만 존재)으로 설치 불가 확인 — 로컬 설정이 아니라 저장소(빌드팜) 쪽 문제라는 것을 원인까지 추적
- snap으로 신버전 Gazebo(Harmonic, 8.9.0) 설치
- ROS 브릿지 없이 우회하는 경로로 Go2 로봇을 신버전 Gazebo에 직접 이식
  - `go2-edu`(Gazebo Classic 전용) 저장소의 URDF에서 Classic 전용 플러그인(`planar_move`, `joint_state_publisher`, `joint_pose_trajectory`, imu/lidar 퍼블리셔) 제거, mesh 경로(`package://` → 절대경로) 수정
  - `gz sdf -p`로 URDF → SDF 변환 후 기존 `mission.world`(벽 4개·장애물 3개·waypoint 3개)에 이식
  - `gz sim`으로 실행, `gz service`로 엔티티 pose 조회 + 스크린샷으로 물리 시뮬레이션 위 로봇 렌더링 확인
  - 기존 `kinematics.py`의 `stand_pose()`로 기립 자세 목표 관절각(hip=0, thigh=0.79, calf=-1.58) 계산, `JointPositionController` 시스템 플러그인(ROS 불필요)으로 기립 작업 진행 중
- 변환 스크립트·삽입 코드·기립 자세 관절각·다음 단계(`JointPositionController` 예시)까지 전 과정을 [`Go2_Gazebo_Harmonic_이식.md`](week4/Go2_Gazebo_Harmonic_이식.md)에 정리
- Gazebo 개념 정리(`Gazebo_설명.md`): 물리 엔진(dartsim)·렌더링(OGRE2)·SDF World/Model 구조·server-gui 프로세스 분리, Classic ↔ 신버전 계보 차이를 오늘 실행 로그 기준으로 정리
- Go2 구성 요소 지도(`구성요소.md`): 다리 4×관절 3(hip·thigh·calf, 12 DOF) + IMU + LiDAR + sport mode 관제 노드 + SportClient API 대응 정리
- turtlesim ↔ Go2 비교(`turtlesim_vs_go2_비교.md`): 차원·물리엔진·형상표현·제어입력·자유도·센서·TF·다중개체 등 축별 비교표
- Unitree 공식 사양 조사(`공식사양조사.md`): 공식 사이트 기준 모델별(AIR/PRO/X/EDU) 스펙 정리, 오늘 URDF에서 본 calf 관절 토크(45.43 N·m)가 공식 "최대 관절 토크 약 45 N·m"와 일치하는 것 대조 확인
- 배터리 확인 경로 조사(`배터리확인경로.md`): 실기체는 `LowState_.bms_state.soc`(DDS `rt/lowstate`)로 확인 가능하지만, 시뮬레이션(`go2_sim`)의 `LowState.msg`엔 배터리 필드 자체가 없어 시뮬 범위 밖이라는 것을 코드로 직접 확인
- 키보드 조종 스크립트(`go2_keyboard_teleop.py`): `go2_sim`이 구독하는 `/cmd_vel`에 Twist 발행, 0.5초 워치독(`core.py CMD_VEL_TIMEOUT`)에 맞춰 10Hz로 현재 속도 재발행하는 방식으로 직접 구현 (i/,/j/l 전후진·회전, J/L 게걸음, k 정지)
- 실기체 Go2 키보드 조작 실습(`키보드조작.md`, `키보드조작실행.md`): 시뮬(`planar_move` 플러그인 직접 구동)과 달리 실기체는 `teleop_twist_keyboard → /cmd_vel → go2_nav_bridge → Unitree Sport API(Move()) → Go2` 순으로 브리지 노드가 한 번 더 변환해 전달한다는 것을 확인
  - 터미널 1에서 `go2_nav_bridge`(Sport API 브리지) 실행 유지, 터미널 2에서 `teleop_twist_keyboard --ros-args -p speed:=0.5 -p turn:=1.0` 실행
  - 실제 Go2로 전진/후진/좌우 이동/회전/정지(`k`)까지 직접 조작해 확인, `go2_nav_bridge.cpp`에서 `/cmd_vel` 구독 → `Move()` 호출로 이어지는 코드 흐름 확인
  - 실기체는 Gazebo Reset World 같은 되돌리기가 없다는 점 때문에 `k`/리모컨 비상정지를 실행 전에 미리 확보해두는 안전 수칙 숙지
- Sport API 직접 호출 실습(`student_sport_demo.cpp`, `코드구조확인.md`): `/cmd_vel` 브리지 없이 `SportClient`로 `StandUp()`/`StandDown()`/`StopMove()`를 직접 호출하는 C++ 노드를 작성 — 메뉴(1/2/q) 입력에 따라 실제 Go2가 기립/자세 낮추기/정지하는 것까지 확인, `CMakeLists.txt`에 실행 파일 등록 후 `colcon build`로 빌드
- Sport API 기반 Waypoint 주행(`student_waypoint_sport.cpp`): `/cmd_vel` 없이 `sport_client_.Move(vx, vy, vyaw)`를 0.1초 간격으로 직접 재호출하는 `move_for()` 함수로 전진→좌회전→전진→우회전→전진 시퀀스 구현 — 시작 전 Enter 입력으로 대기하는 확인 절차, 각 구간 종료 시 `StopMove()` 명시 호출
- LiDAR 장애물 정지(`student_lidar_stop.py`, `실행전확인.md`): `/lidar_points`(PointCloud2)를 구독해 전방 영역(x: 0.2~3.0 m, |y|<0.4 m)의 점만 골라 최소 거리 계산 → 0.6 m 미만이면 정지, 0.8 m 초과면 재출발(히스테리시스)하도록 `/cmd_vel`을 통해 `go2_nav_bridge`로 전달 — 코드만 보고 구독 토픽·마스크 조건·정지/재출발 거리 차이 이유를 먼저 자가 점검한 뒤 실기체에 실행
- Unitree 공식 ROS2 지원 패키지(`unitree_ros2/`) 직접 클론·빌드: `unitreerobotics/unitree_ros2` 클론 후 `ros-humble-rmw-cyclonedds-cpp`·`ros-humble-rosidl-generator-dds-idl` 설치, `cyclonedds_ws`(unitree_api/go/hg 메시지) + `example`(go2_sport_client 등) 빌드까지 성공
  - 저장소 기본 `setup*.sh`가 ROS2 foxy·`$HOME/unitree_ros2` 경로를 하드코딩하고 있는 걸 확인하고, 이 환경(Humble + 저장소 내부 경로)에 맞게 세 스크립트를 직접 수정
  - 실제 로봇이 물리적으로 연결되어 있지 않아 `setup_local.sh`(루프백 `lo`)로 소싱·빌드까지만 확인, `/sportmodestate` 등 실데이터 수신은 미확인
  - 수업 때 쓴 `my_go2_nav`/`go2_practice`(브리지·waypoint·LiDAR stop 패키지)는 멘토가 이 공식 저장소 위에 별도로 얹은 패키지라 이번 클론엔 포함되지 않았다는 것도 확인

## 개발 환경

- OS: Ubuntu 22.04.5 LTS (커널 5.15.0-186-generic)
- Python 3.10.12
- ROS2, MuJoCo 기반 시뮬레이션 환경

자세한 환경 정보는 [env_report.md](env_report.md) 참고.
