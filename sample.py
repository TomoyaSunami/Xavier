import allocate_bandwidth_with_yolo as alb
import subprocess
def allocate():
    cmd = "python3 allocate_bandwidth_with_yolo.py"
    subprocess.call(cmd.split())

def main():
    allocate()


if __name__=="__main__":
    main()
