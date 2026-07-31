#3.7.3
cd ~/robot_study/week1
for i in $(seq 1 100); do echo "[INFO] step $i: joint state ok" >> robot.log; done
echo "[ERROR] step 41: motor 3 overheat" >> robot.log
echo "[WARN] step 77: battery low (18%)" >> robot.log
wc -1 robot.log
tail -n 5 robot.log
grep ERROR robot.log
grep -n "motor 3" robot.log

