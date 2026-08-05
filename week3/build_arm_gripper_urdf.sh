set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RM75_EDU_DIR="${SCRIPT_DIR}/rm75-edu"
GRIPPER_DIR="${RM75_EDU_DIR}/gripper_description"
OUT_FILE="${GRIPPER_DIR}/urdf/arm_gripper.urdf.xacro"

if [ ! -d "${GRIPPER_DIR}" ]; then
  echo "[준비] gripper_description 이 없어 먼저 fetch_gripper_model.sh 를 실행합니다..."
  bash "${SCRIPT_DIR}/fetch_gripper_model.sh"
fi

echo "[생성] ${OUT_FILE} 작성 중..."
cat > "${OUT_FILE}" <<'XACRO'
<?xml version="1.0"?>
<!--
  RM75 팔 + EG2-4C2 그리퍼 결합 URDF/Xacro
  - rm_description/urdf/rm_75.urdf.xacro : 팔(Link1~Link7)
  - gripper_description/urdf/jaw.urdf.xacro : EG2-4C2 그리퍼(4C2_baselink 등)
  - arm_jaw_joint : 둘을 잇는 고정 조인트 (RealManRobot 공식 오프셋 사용)
-->
<robot name="rm75_eg2_4c2" xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- 팔: 마지막 링크 이름은 Link7 (link7_type 기본값) -->
  <xacro:include filename="$(find rm_description)/urdf/rm_75.urdf.xacro" />

  <!-- 그리퍼: EG2-4C2 (baselink: 4C2_baselink) -->
  <xacro:include filename="$(find rm_Lifting_robot_75B_jaw_description)/urdf/jaw.urdf.xacro" />

  <!-- 팔 끝(Link7) - 그리퍼 베이스(4C2_baselink) 결합 -->
  <joint name="arm_jaw_joint" type="fixed">
    <origin xyz="0 0 -0.009" rpy="0 0 -1.57" />
    <parent link="Link7" />
    <child link="4C2_baselink" />
  </joint>

  <!-- 파지 기준점 -->
  <link name="grasp_tcp"/>
  <joint name="grasp_tcp_joint" type="fixed">
    <origin xyz="0 0 0.12" rpy="0 0 0"/>
    <parent link="Link7"/>
    <child link="grasp_tcp"/>
  </joint>

</robot>
XACRO

echo "[완료] ${OUT_FILE}"
echo ""
echo "확인(문법 검사)은 아래 명령으로 가능합니다 (colcon 워크스페이스에서 두 패키지를 빌드/source 한 뒤):"
echo "  xacro ${OUT_FILE} > /tmp/rm75_eg2_4c2.urdf"
echo "  check_urdf /tmp/rm75_eg2_4c2.urdf"
