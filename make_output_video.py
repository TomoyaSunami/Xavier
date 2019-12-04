"""
yoloの推定結果の連続画像から動画を作成する
"""

import sys
import os
import getopt
import numpy as np
import cv2
import datetime

def execute_cmdline(argv):

    fps = 10
    input_path = "detected_images"
    output_name = "video.mp4"

    help_str = 'make_output_video.py -f <fps> -i <input_path> -o <output_name>'
    try:
        opts, args = getopt.getopt(argv, 'f:i:o:', ['fps=', 'input=', 'output='])
    except getopt.GetoptError as err:
        print(str(err))
        print(help_str)
        sys.exit(1)
    for opt,arg in opts:
        if opt in ("-f", "--fps"):
            fps = float(arg)
        elif opt in ("-i", "--input"):
            input_path = arg
        elif opt in ("-o", "--output"):
            output_name = arg

    if not os.path.exists(input_path):
        print(input_path, 'does not exist')
        sys.exit(1)

    write_video(fps, input_path, output_name)

def load_images(images_folder_path):
    # 画像名から時刻を取り出す
    img_names = [f for f in os.listdir(images_folder_path) if not f.startswith(".")]
    img_times = [s.strip(".jpg").strip("'") for s in img_names]
    img_times = [float(s) for s in img_times]
    img_times.sort() # 昇順に並び替え
    return img_times

def write_video(fps, images_folder_path, video_name):

    img_times = load_images(images_folder_path)
    images_count = len(img_times) # 画像の数を取得   

    # 計測時間を取得
    time = float(img_times[-1]) - float(img_times[0])

    fps_avg = images_count / time

    # 動画作成に必要な画像の枚数を計算
    img_list_size = int(time * fps)
    
    
    #　画像のサイズを取得
    base_image = cv2.imread(os.path.join(images_folder_path, str(img_times[0])+".jpg"))
    h, w, c = base_image.shape

    # 動画作成用の画像を格納するリストを作成
    time_list = [img_times[0]+n/fps for n in range(img_list_size)]
    time_diff = [0] * len(time_list)

    os.makedirs("video", exist_ok=True) # 保存先のディレクトリを作成

    fourcc = cv2.VideoWriter_fourcc("m","p","4","v")
    video = cv2.VideoWriter(os.path.join("video",video_name), fourcc, fps, (w,h))

    for i in range(img_list_size):
        idx = np.abs(np.asarray(img_times) - time_list[i]).argmin() # リスト中で最も近い値を探索
        time_diff[i] = img_times[idx] - time_list[i]
        img = cv2.imread(os.path.join(images_folder_path, str(img_times[idx])+".jpg"))
        video.write(img)

    video.release()

    save_discription(fps,fps_avg, img_times, time_list, time_diff)


def save_discription(fps, fps_avg, img_times, time_list, time_diff):
    # 作成した動画の詳細情報をテキストファイルで保存

    path_w = "video/video_discriptin.txt"
    img_dt = [datetime.datetime.fromtimestamp(n) for n in img_times]
    dt_format = [str(dt.year)+"/"+str(dt.month)+"/"+str(dt.day)+" "+str(dt.hour)+":"+str(dt.minute)+":"+str(dt.second)+"."+str(dt.microsecond) for dt in img_dt]
    l = ["target_fps : " + str(fps),  "fps_avg : " + str(fps_avg), "count_images : " + str(len(time_list)), "image_times : ", str(dt_format), "image_unix_times : " , str(time_list), "time_difference : " , str(time_diff)]

    with open(path_w, mode='w') as f:
        f.write('\n'.join(l))


if __name__ == '__main__':
    execute_cmdline(sys.argv[1:])


"""
def write_video(fps, input_folder="output",video_name="video.mp4"):
    fourcc = cv2.VideoWriter_fourcc("m","p","4","v")
    video = cv2.VideoWriter(video_name, fourcc, fps, (1280,720))
    
    path = os.getcwd()  
    files = os.listdir(path+"/"+input_folder)  
    count = len(files)  
    for i in range(1, count):
        img = cv2.imread(input_folder+"/*image{0:03d.jpg".format(i))
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
"""
