# Gazebo란 무엇인가

## 한 줄 정의
Gazebo는 **물리(중력·충돌·마찰)·센서·렌더링까지 갖춘 로봇 시뮬레이터**다.
turtlesim처럼 좌표만 그려주는 게 아니라, 로봇을 물리 법칙이 적용되는 3D
공간에 실제로 "떨어뜨려" 보고 그 반응을 관찰할 수 있다는 게 핵심 차이
([turtlesim_vs_go2_비교.md](turtlesim_vs_go2_비교.md) 참고).

## 구성 요소 (오늘 로그에서 직접 확인한 것)

Gazebo가 내부적으로 뭘 조합해서 돌아가는지, 오늘 실행 로그에 그대로 찍혀서
확인할 수 있었다:

| 역할 | 오늘 로그에서 본 것 |
|---|---|
| 물리 엔진 | `gz::physics::dartsim::Plugin` (DART 엔진을 플러그인으로 로드) |
| 렌더링 | `Ogre2RenderTarget` (OGRE2 그래픽 엔진) |
| 씬 표현 형식 | SDF(Simulation Description Format) 버전 1.11 |
| 서버/GUI 분리 | `gz sim server`(물리 계산) + `gz sim gui`(화면) 프로세스가 따로 뜸 |

즉 Gazebo는 "물리 엔진 + 렌더링 엔진 + 센서 모델"을 갈아 끼울 수 있게
플러그인 구조로 짜여 있고, 서버(물리 계산)와 GUI(화면 표시)가 별도 프로세스로
분리되어 있어서 `gui:=false`로 GUI만 끄고 헤드리스로 돌릴 수도 있다
(go2-edu README의 WSL2 저사양 대안이 이 구조 덕분에 가능한 것).

## Gazebo Classic vs 신버전 — 오늘 가장 헷갈렸던 부분

Gazebo라는 이름 아래 사실 **계보가 완전히 다른 두 세대**가 있다:

```
Gazebo Classic (1 ~ 11)          Ignition → Gazebo (신버전)
├─ 실행 파일: gazebo,             ├─ 실행 파일: gz sim
│  gzserver / gzclient            ├─ 세대명: Citadel → Fortress →
├─ ROS2 연동: gazebo_ros          │  Garden → Harmonic → Ionic ...
├─ 플러그인: libgazebo_ros_*.so   ├─ ROS2 연동: ros_gz(_bridge/_sim)
└─ (Gazebo11 이후 신규 개발 중단) └─ 플러그인: gz-sim-*-system
```

이 둘은 **명령어도, 플러그인 라이브러리 이름도, ROS 연동 패키지도 전부
다르다.** 오늘 `go2-edu`가 Classic 전용(`libgazebo_ros_planar_move.so` 등)으로
짜여 있는 걸 신버전(Harmonic, `gz sim`)에 그대로 실행하려다가 안 되는 걸
직접 겪으면서 이 차이를 몸으로 배움
([Go2_Gazebo_Harmonic_이식.md](Go2_Gazebo_Harmonic_이식.md) 참고).

## SDF — Gazebo가 세상을 표현하는 방식

- **World**: 하나의 시뮬레이션 공간 전체(바닥·조명·벽·로봇 여러 개 다 포함) —
  오늘 쓴 `mission.world`가 이것
- **Model**: world 안의 개체 하나(로봇 1대, 장애물 박스 1개 등), 안에 링크·조인트
- URDF(ROS 표준 로봷 기술 형식)는 SDF의 부분집합에 가까워서, `gz sdf -p`
  같은 도구로 URDF → SDF 변환이 가능함(오늘 실제로 해봄)

## ROS2와의 관계

Gazebo는 ROS2에 종속된 프로그램이 아니라 **원래 독립적인 시뮬레이터**다.
ROS2 쪽에서 Gazebo의 토픽/서비스를 ROS 토픽으로 이어주는 "다리" 역할을
하는 별도 패키지가 있어야 `/cmd_vel` 같은 ROS 토픽으로 시뮬레이터를
제어할 수 있다:

- Classic ↔ ROS2: `gazebo_ros` 패키지가 다리 역할
- 신버전 ↔ ROS2: `ros_gz_bridge` 패키지가 다리 역할

오늘 이 "다리" 패키지가 arm64 환경에서 apt로 설치가 안 되는 문제를 만났고,
그래서 다리 없이 **Gazebo 단독으로만** Go2 모델을 띄우는 우회 경로로 진행함
— 즉 지금 떠 있는 Go2는 Gazebo 물리 위에는 있지만 ROS2와는 아직 안 이어진
상태라는 걸 이 구조를 알고 나니 명확하게 이해됨.
