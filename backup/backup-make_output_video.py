import sys
import os
import cv2

def write_video(fps, input_folder="output",video_name="video.mp4"):
    fourcc = cv2.VideoWriter_fourcc("m","p","4","v")
    video = cv2.VideoWriter(video_name, fourcc, fps, (1280,720))
    
    path = os.getcwd()  
    files = os.listdir(path+"/"+input_folder)  
    count = len(files)  
    for i in range(1, count):
        img = cv2.imread(input_folder+"/*image{0:03d}.jpg".format(i))
        video.write(img)

    video.release()

if __name__ == '__main__':
    args = sys.argv
    if len(args)<2:
        print("No argument!")
        sys.exit()
    elif len(args)<3:
        write_video(float(args[1]))
    else:
        write_video(float(args[1]),args[2],args[3])

