set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${SCRIPT_DIR}/rm75-edu/gripper_description"
TMP_DIR="$(mktemp -d)"
REPO_URL="https://github.com/RealManRobot/URDF-to-XACRO.git"
ZIP_NAME="rm_Lifting_robot_75B_jaw_description.zip"

cleanup() { rm -rf "${TMP_DIR}"; }
trap cleanup EXIT

echo "[1/4] URDF-to-XACRO 저장소를 임시 폴더에 클론합니다..."
git clone --depth 1 "${REPO_URL}" "${TMP_DIR}/URDF-to-XACRO"

ZIP_PATH="${TMP_DIR}/URDF-to-XACRO/${ZIP_NAME}"
if [ ! -f "${ZIP_PATH}" ]; then
  echo "오류: ${ZIP_NAME} 파일을 저장소에서 찾지 못했습니다." >&2
  exit 1
fi

echo "[2/4] ${ZIP_NAME} 압축을 해제합니다..."
mkdir -p "${TMP_DIR}/extracted"
unzip -q "${ZIP_PATH}" -d "${TMP_DIR}/extracted"

echo "[3/4] ${TARGET_DIR} 로 그리퍼 모델(urdf/xacro/mesh)을 복사합니다..."
mkdir -p "${TARGET_DIR}"
# zip 안에 최상위 폴더가 하나 더 있는 경우와 없는 경우를 모두 처리
if [ "$(find "${TMP_DIR}/extracted" -mindepth 1 -maxdepth 1 -type d | wc -l)" -eq 1 ] \
   && [ "$(find "${TMP_DIR}/extracted" -mindepth 1 -maxdepth 1 -type f | wc -l)" -eq 0 ]; then
  cp -r "${TMP_DIR}"/extracted/*/. "${TARGET_DIR}/"
else
  cp -r "${TMP_DIR}"/extracted/. "${TARGET_DIR}/"
fi

echo "[4/4] 완료. 그리퍼 모델 파일 위치: ${TARGET_DIR}"
find "${TARGET_DIR}" -maxdepth 2 -print
