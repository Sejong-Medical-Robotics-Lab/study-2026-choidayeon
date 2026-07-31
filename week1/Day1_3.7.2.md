cd ~/robot_study/week1
mkdir data backup
touch data/exp_01.csv data/exp_02.csv data/exp_03.csv data/memo.txt
ls data
cp data/exp_*.csv backup/ 
mv data/memo.txt data/note.txt
rm backup/exp_03.csv
ls -al data backup
