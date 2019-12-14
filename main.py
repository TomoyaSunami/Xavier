#!/user/bin/env python3

#import yolo
#import communication_control
import concurrent.futures
import subprocess

def yolo():
    cmd = "python3 yolo.py"
    subprocess.submit(cmd.split(" "))

def communication_control():
    cmd = "python3 communication_control.py"
    subprocess.submit(cmd.split(" "))

def main():
    executor = concurrent.futures.ProcessPoolExecutor(max_workers=2)
    executor.submit(yolo)
    executor.submit(communication_control)
    

if __name__=="__main__":
    main()
