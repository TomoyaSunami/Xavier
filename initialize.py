import subprocess

def main():
    cmd = "rm output/*"
    print(cmd)
    subprocess.call(cmd.split(" "))

    cmd = ": > test_detected_series.txt"
    print(cmd)
    subprocess.call(cmd.split(" "))


    cmd = ": > test_prediction_series.txt"
    print(cmd)
    subprocess.call(cmd.split(" "))

if __name__=="__main__":
    main()
