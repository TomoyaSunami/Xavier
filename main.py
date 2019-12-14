#!/user/bin/env python3

import yolo
import communication_control
import concurrent.futures

def main():
    executor = concurrent.futures.ProcessPoolExecutor(max_workers=2)
    executor.submit(yolo.execute_cmdline)
    executor.submit(communication_control.main)
    

if __name__=="__main__":
    main()
