#!/bin/bash
mkdir -p ~/robot_study/experiments/$1/{data,logs,results}
echo "#experiments note: $1 ($(data +%F))" > ~/robot_study/experiments/$1/README.md
echo "complete: $1"

