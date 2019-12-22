import os
import shutil

def main():
    target_dir = "output"
    shutil.rmtree(target_dir)
    os.mkdir(target_dir)
    print("clean output directory")

    with open("is_there_person.txt", mode='w') as f:
        str_w = ""
        f.write(str_w)
    with open("output_sequence.txt", mode='w') as f:
        str_w = ""
        f.write(str_w)
    with open("observed_sequence.txt", mode='w') as f:
        str_w = ""
        f.write(str_w)
    with open("decoded_state_sequence.txt", mode='w') as f:
        str_w = ""
        f.write(str_w)
    with open("mode_observed_sequence.txt", mode='w') as f:
        str_w = ""
        f.write(str_w)
    print("clean is_there_person.txt, output_sequence.txt observed_sequence.txt, decoded_state_sequence.txt, mode_observed_sequence.txt")


if __name__=="__main__":
    main()
