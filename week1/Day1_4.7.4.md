#Day1_4.7.4
```
$git switch -c exp-tuning
$echo "speed: 0.8" > params.yaml
$git add . && git commit -m "feat: try faster walking params"
$git switch main 
$ls 
$git merge exp-tuning
$ls
$git branch -d exp-tuning 

확인 포인트 : 브랜치를 오갈 때 폴더의 파일이 나타났다 사라지는 것을 직접 목격하는 것

