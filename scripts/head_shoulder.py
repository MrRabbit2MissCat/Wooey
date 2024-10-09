# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Author:       yunhgu
# Date:         2024-07-02 14:39:49
# @Copyright:  www.shujiajia.com  Inc. All rights reserved.
# Description: 注意：本内容仅限于数据堂公司内部传阅，禁止外泄以及用于其他的商业目的
# -------------------------------------------------------------------------------
import argparse
import os
import re
import subprocess


image = "harbor.datatang.com/gyh-tools/head_shoulders:1.3"


def main():
    print("start")
    path = re.sub(r"\\\\\d+\.\d+\.\d+\.\d+\\", r"/mnt/", inargs.path).replace("\\", "/")
    cmd = f"docker run --rm --gpus all -v {path}:/input {image}"
    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while result.poll() is None:
        line = result.stdout.readline().decode()
        if line:
            print(line.strip())
    if result.returncode == 0:
        print('Subprogram success')
        return True
    else:
        print('Subprogram failed')
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="头肩检测模型")
    parser.add_argument("--path", help="图片路径", required=True, type=str)
    inargs = parser.parse_args()
    main()
