# Go2 → Gazebo Harmonic 이식 기록 (2026-08-12)

`go2-edu`(Gazebo Classic 전용) 저장소의 Go2 로봇을, ROS 브릿지 없이 신버전
Gazebo(Harmonic, snap)에 직접 올리기 위해 진행한 변환 작업 기록. 산출물은
`~/go2_harmonic_sim/`에 있음(이 저장소 밖, 스크래치 작업 폴더).

## 왜 이렇게 했나

- `go2-edu`는 Gazebo Classic(`gazebo_ros`) 전용으로 짜여 있는데, 실습 환경(Ubuntu
  22.04 **arm64**)엔 Classic Gazebo 바이너리 자체가 없음(Ubuntu 공식/OSRF 공식
  저장소 둘 다)
- 대체재인 Ignition Fortress도 ROS 2 arm64 저장소 자체의 의존성 결함으로 설치 불가
  (`libignition-gazebo6`가 요구하는 `libignition-sensors6 >= 6.8.1`이 arm64엔
  6.8.0까지만 존재 — 빌드팜 쪽 문제, 로컬에서 손쓸 수 없음)
- 그래서 ROS 연동은 잠시 포기하고, **URDF를 SDF로 직접 변환해서 신버전 Gazebo에
  물리 시뮬레이션 위 로봇만이라도 올리는** 우회 경로를 택함

## 1단계 — URDF 정리 (`go2_clean.urdf`)

원본(`go2-edu/go2_gazebo/urdf/go2_sim.urdf`)에서 두 가지를 고침:

1. mesh 경로: `package://go2_description/dae/...` → 절대경로
   (ROS 워크스페이스가 빌드/source 안 된 상태라 `package://`가 해석 안 됨)
2. Gazebo **Classic 전용** ROS 플러그인 블록 제거: `libgazebo_ros_planar_move`,
   `libgazebo_ros_joint_state_publisher`, `libgazebo_ros_joint_pose_trajectory`,
   imu/lidar용 `libgazebo_ros_imu_sensor`·`libgazebo_ros_ray_sensor` — 전부
   Harmonic(`gz sim`)에는 없는 라이브러리라 로드 자체가 안 됨

```python
import re

mesh_dir = "/home/choidayeon/robot_ws/src/go2-edu/go2_description/dae"
text = text.replace("package://go2_description/dae/", mesh_dir + "/")

# libgazebo_ros_*.so 를 쓰는 <plugin> 블록 통째로 제거
text = re.sub(
    r'\s*<plugin name="[^"]*" filename="libgazebo_ros_[^"]*">.*?</plugin>',
    '', text, flags=re.DOTALL,
)
```

## 2단계 — URDF → SDF 변환

Harmonic에 번들된 변환 도구를 그대로 사용:

```bash
gazebo.gz sdf -p go2_clean.urdf > go2_model.sdf
```

- `<mesh>` 태그의 절대경로, 링크별 관성(inertia)·충돌·시각 형상이 모두 SDF
  형식으로 정확히 변환됨 (`<model name='go2_description'>` 루트)
- ⚠ snap으로 설치된 Gazebo는 confinement 때문에 `$HOME` 하위 파일만 읽을 수
  있어서, `/tmp` 스크래치 경로가 아니라 `~/go2_harmonic_sim/` 안에서 변환·실행
  해야 했음

## 3단계 — 월드에 이식 (`go2_mission.world`)

`go2-edu`의 `mission.world`(벽 4개·장애물 3개·waypoint 3개, 순수 SDF라 그대로
호환)를 베이스로, 두 가지만 바꿈:

- `<include><uri>model://sun</uri></include>` /
  `<include><uri>model://ground_plane</uri></include>` — 신버전 Gazebo가
  Classic 모델 데이터베이스 URI를 못 찾아서(`Unable to find uri`), 실제
  `<light>`/`<model name="ground_plane">` 내용을 직접 박아넣는 방식으로 교체
- 변환된 go2 모델을 `<model name='go2'>`로 이름 바꿔서 삽입, 스폰 높이
  `<pose>0 0 0.45 0 0 0</pose>` 지정(원래 launch 파일의 `-z 0.45`와 동일)

```python
model_block = model_block.replace(
    "<model name='go2_description'>",
    "<model name='go2'>\n    <pose>0 0 0.45 0 0 0</pose>",
    1,
)
world = world.replace("</world>", "\n" + model_block + "\n  </world>")
```

## 실행

```bash
~/go2_harmonic_sim/run_go2.sh
# 또는
gazebo.gz sim -r ~/go2_harmonic_sim/go2_mission.world
```

실행 후 확인한 것:
- `gz service -s /world/mission/scene/info ...` 로 `go2` 엔티티(id 45)가 실제
  월드에 존재하는 것 확인
- `gz service -s /gui/move_to` + `/gui/screenshot` 으로 로봇이 물리 시뮬레이션
  위에서 실제 렌더링되는 것 스크린샷으로 확인 (walls·장애물·waypoint 마커까지 정상)

## 지금 상태의 한계

- **다리를 잡아주는 컨트롤러가 없음** → 스폰 후 중력으로 그냥 주저앉은 자세로
  안착함 (`go2_sim`의 sport mode 관제 노드와 완전히 끊긴, "모델만 있는" 상태)
- `go2_sim`이 원래 쓰던 ROS 토픽(`/cmd_vel`, SportClient API, `/go2/lowstate`
  등)은 하나도 안 나옴 — ROS 브릿지(`ros-humble-ros-gz-bridge`)가 풀려야 이어서
  연결 가능

## 다음에 이어서 할 것 — 기립 자세

기존 `go2_sim/go2_sim/kinematics.py`의 `stand_pose()`를 그대로 돌려서 목표
관절각을 계산해둠(높이 0.30m 기준, 12축 모두 다리별로 동일):

```
hip_joint   = 0.0
thigh_joint = 0.7895
calf_joint  = -1.5789
```

ROS 없이 gz-sim 자체 시스템 플러그인(`JointPositionController`)으로 각 관절을
이 각도에 고정시키는 작업을 시작했으나 **오늘은 여기서 중단**. 이어서 할 때는
`<model name='go2'>` 안에 다음과 같은 블록을 12개(다리 4 × 관절 3) 넣으면 됨
(예시, hip 관절 기준 — thigh/calf는 목표값·effort 한계만 바꿔서 반복):

```xml
<plugin filename="gz-sim-joint-position-controller-system"
        name="gz::sim::systems::JointPositionController">
  <joint_name>FR_hip_joint</joint_name>
  <initial_position>0.0</initial_position>
  <p_gain>60</p_gain>
  <i_gain>0.5</i_gain>
  <d_gain>2</d_gain>
  <i_max>5</i_max>
  <i_min>-5</i_min>
  <cmd_max>23.7</cmd_max>
  <cmd_min>-23.7</cmd_min>
</plugin>
```

(effort 한계는 URDF `<limit effort="...">` 값 그대로: hip/thigh 23.7 N·m,
calf 45.43 N·m. p/i/d 게인은 감으로 넣은 값이라 실제로 세워지는지, 진동은
없는지 검증 필요.)
