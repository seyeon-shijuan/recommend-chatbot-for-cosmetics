#!/bin/bash

readonly type=$1
if [ $type = "-d" ]; then
    echo "build whl"
    python3 setup.py sdist
elif [ $type = "-s" ]; then
    echo "build tar.gz"
    python3 setup.py bdist_wheel
else
    echo "-s 또는 -d 만 입력해주세요"
fi