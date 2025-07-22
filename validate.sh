#!/usr/bin/bash -l

if [ "$#" -eq 1 ]; then
    if [ "$1" = "--auto" ]; then
        td=$(date +"%Y%m%d")
    else
        td="$1"
    fi
else
    read -p "Please input the check date, format = [YYYYMMDD]:" td
fi

python main.py --date $td --switch vp
exit_code=$?
if [ $exit_code -ne 0 ]; then
    exit 1
fi

python main.py --date $td --switch fund
exit_code=$?
if [ $exit_code -ne 0 ]; then
    exit 1
fi

python main.py --date $td --switch macro
exit_code=$?
if [ $exit_code -ne 0 ]; then
    exit 1
fi

echo "[INF] Data of $td passed all checks"
exit 0
