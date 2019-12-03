#!/user/bin/env python3

import allocate_bandwidth_with_yolo as alb
import controll_iperf as coni
import concurrent.futures
import subprocess

def allocate():
    cmd = "python3 allocate_bandwidth_with_yolo.py"
    subprocess.call(cmd.split(" "))


def main():
    print("main")
    executor = concurrent.futures.ProcessPoolExecutor(max_workers=2)
    executor.submit(allocate)
    print("a")
    executor.submit(coni.main)
    print("b")


if __name__=="__main__":
    main()
