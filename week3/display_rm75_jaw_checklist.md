# display_rm75_jaw.sh 실행 후 확인 포인트

- [ ] RViz에 팔 + 그리퍼가 붙어서 보인다 (떠 있거나 파묻혀 있으면 arm_jaw_joint의 origin z 조정)
- [ ] 슬라이더 창에 관절 8개: joint1~joint7 + jaw_Joint1
- [ ] jaw_Joint1 슬라이더로 그리퍼가 열리고 닫힌다
- [ ] RViz의 Displays → TF를 켜면 grasp_tcp 프레임이 손가락 사이에 보인다

**로봇이 안 보이면**: Fixed Frame이 `base_link`인지, RobotModel 디스플레이가 켜져 있는지 확인
