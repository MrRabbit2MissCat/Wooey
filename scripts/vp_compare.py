# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Author:       yunhgu
# Date:         2024-07-02 14:39:49
# @Copyright:  www.shujiajia.com  Inc. All rights reserved.
# Description: 注意：本内容仅限于数据堂公司内部传阅，禁止外泄以及用于其他的商业目的
# -------------------------------------------------------------------------------
import argparse
import base64
import json
import os
import re
import subprocess


def create_base64_str(name, top, wav_length):
    # 模拟平台，WORKINFO由平台设置
    data = {
        "set": {
            "mode": "",
            "execParameter": {
                "name": name,
                "top": top,
                "wav_length": wav_length,
            },
            "stage": name,
            "jobName": name,
            "ioMap": [],
        },
    }
    s = json.dumps(data)
    code = (base64.b64encode(s.encode("utf-8"))).decode("utf-8")
    return code


docker_id = "harbor-internal.datatang.com/rd-tools/vp_com:datatang_v1.0.6"


def get_gpu_free():
    try:
        cmd = "/usr/bin/nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits"
        num = float(os.popen(cmd).readlines()[0].strip())
        return int(num / 1024)
    except Exception as e:
        print(e)
        return 0


def main():
    free_num = get_gpu_free()
    if free_num < 6:
        print(f"显存不足:{free_num}G")
        return
    code = create_base64_str(inargs.name, inargs.top, inargs.wav_length)
    input_path = re.sub(r"\\\\\d+\.\d+\.\d+\.\d+\\", r"/mnt/", inargs.path).replace("\\", "/")
    save_path = re.sub(r"\\\\\d+.\d+.\d+.\d+\\", r"/mnt/", inargs.save).replace("\\", "/")
    print(f"input:{input_path}\noutput:{save_path}")
    cmd_line = f"""/usr/bin/docker run -it -e WORKINFO={code} --rm --gpus "device=0" -v "{input_path}":/input -v "{save_path}":/output {docker_id} /bin/bash"""
    print(cmd_line)
    import pdb
    pdb.set_trace()
    result = subprocess.Popen(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while result.poll() is None:
        line = result.stdout.readline().decode()
        if line:
            print(line.strip())
    if result.returncode == 0:
        print("Subprogram success")
        return True
    else:
        print("Subprogram failed")
        return False


def is_within_range(min_value, max_value):
    def check_type(value):
        ivalue = int(value)
        if min_value <= ivalue <= max_value:
            return ivalue
        raise argparse.ArgumentTypeError(f"Value {value} is out of range [{min_value}, {max_value}]")

    return check_type


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="音频声纹对比检测工具")
    parser.add_argument("--path", help="音频路径", required=True, type=str)
    parser.add_argument("--name", help="项目编号", required=True, type=str)
    parser.add_argument("--top", default=3, type=int, required=True, help="检测结果输出个数")
    parser.add_argument("--wav_length", default=30, type=int, required=True, help="音频检测长度")
    parser.add_argument("--save", help="结果保存路径", required=True, type=str)
    inargs = parser.parse_args()
    print(inargs)
    main()
