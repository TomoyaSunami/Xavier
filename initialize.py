import subprocess

def main():
    cmd = "rm output/*"
    print(cmd)
    subprocess.call(cmd.split(" "))

    with open("observed_sequence.txt", mode='w') as f:
        str_w = ""
        f.write(str_w)
    with open("decoded_state_sequence.txt", mode='w') as f:
        str_w = ""
        f.write(str_w)
    with open("mode_observed_sequence.txt", mode='w') as f:
        str_w = ""
        f.write(str_w)
    print("clean observed_sequence.txt, decoded_state_sequence.txt, mode_observed_sequence.txt")

    cmd = "cp backup_iperf_flag.txt iperf_flag.txt"
    print(cmd)
    subprocess.call(cmd.split(" "))

if __name__=="__main__":
    main()
