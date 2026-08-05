#Day1_4.7.5
```
$git switch -c exp-a && sed -i 's/0.8/0.5/' params.yaml
$git add . && git commit -m "fix: slow down for safety"
$git switch main && sed -i 's/0.8/1.0/' params.yaml
$git add . && git commit -m "feat: max speed test"
$git merge exp-a
$nano params.yaml
$git add . && git commit -m "fix: resolve speed conflict at 0.5"

확인 포인트 : 실제 충돌이 나면 오늘의 순서(파일 열기 → 정리 → add → commit)를 그대로 반복

