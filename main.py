#!/user/bin/env python3

import controll_iperf as coni
import concurrent.futures
import subprocess

def allocate():
    cmd = "python3 yolo_hmm.py"
    subprocess.call(cmd.split(" "))


def main():
    print("main")
    executor = concurrent.futures.ProcessPoolExecutor(max_workers=2)
    executor.submit(allocate)
    
    executor.submit(coni.main)
    


if __name__=="__main__":
    main()
