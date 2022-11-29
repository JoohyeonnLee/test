import cv2
import argparse
from pathlib import Path
from glob import glob
import shutil
import os
from threading import Thread

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # file
main_data_path = ROOT.__str__()
save_path = ROOT
ENCODE_METHOD = 'utf-8'


def Write_error_to_txt(message, path="\\error_file\\error"):
    #오류메세지를 기록해두는 함수
    global current_time
    global error_txt_name
    global error_queue

    error_queue.insert(0, error_txt_name + ': Error: ' + message + '\n')

    if error_queue.__len__()==0:
        return
    try:
        with open(main_data_path + path + error_txt_name + ".txt",
                  'a', encoding=ENCODE_METHOD) as f:
            while error_queue.__len__() > 0:
                txt = error_queue.pop()
                f.write(txt)
    except OSError:
        pass
    except IndexError:
        pass


def Check_directory(dir_list):
    #해당 디렉토리가 존재하면 참을 반환하고, 없으면 만들고 거짓을 반환한다.
    # dir 존재확인
    try:
        if dir_list is list:
            for dir_name in dir_list:
                if not os.path.exists(dir_name):
                    print("Create File : " + dir_name)
                    os.makedirs(dir_name)
        else  :
            dir_name = dir_list
            if not os.path.exists(dir_name):
                    print("Create File : " + dir_name)
                    os.makedirs(dir_name)
    except OSError:
        Write_error_to_txt('Check_directory Error: Creating directory. ' + dir_list)
        print('Check_directory Error: Creating directory. ' + dir_list)

# mp4파일을 받으면 해당 파일 옆에 폴더안에 이미지를 만들어줌
def video2frame(invideofilename, save_path=None):
    save_path = save_path
    if save_path == None:
        #해당 파일의 부모 디렉토리 절대경로 
        save_path = Path(os.path.abspath(invideofilename)).parent
        #print("parrent directory : ", save_path)
        #basename = os.path.basename(save_path)
        #print("basename : ", basename)
        #해당 파일명 (확장자 빼고)
        stem_name = Path(invideofilename).stem
        #print("stem : ", stem_name)
        save_path = save_path.__str__() +"\\"+ stem_name
        #print("save directory : ", save_path)
    #print("save path : ", save_path)
    Check_directory(save_path)
    vidcap= cv2.VideoCapture(invideofilename)
    count = 0
    frame = "first"
    try:
        while True:
            success,image = vidcap.read()
            if not success:
                break
            #print ('Read a new frame: ', success)
            fname = "{}.jpg".format("{0:05d}".format(count))
            #print(save_path+"\\"+ fname)
            cv2.imwrite(save_path+"\\"+ fname, image) # save frame as JPEG file
            count += 1
            #print("{} images are extracted in {}.".format(count,save_path))
    except Exception as ex : 
        Write_error_to_txt(ex.__str__, + "video2frame", save_path+"\\"+ fname)
    print("end video2frame")


def delete_picked_string_in_string(input_str, str_start="C", str_end="x"):
    start_idx = max(input_str.find(str_start),0)
    end_idx = input_str.find(str_end, start_idx) + str_end.__len__()
    #print("input : ",input_str)
    #print("result : ", input_str[start_idx:end_idx])
    if( start_idx > end_idx):
        start_idx=0
        end_idx=0
    return start_idx, end_idx


def delete_picked_string_in_file(file_name, str_start='C', str_end="x"):
    with open(file_name, 'r') as fr:
        with open(file_name+"_result.txt", 'w') as fw:
            line = "start"
            while line != "":
                try:
                    #get line
                    line = fr.readline()
                    start, end = delete_picked_string_in_string(line, str_start, str_end)
                    
                    fw.write(line[0:start-1] + " ")
                    fw.write(line[end+1 : -1] + "\n")
                except:
                    print("error : next line")
                    

def read_all_file(path):
    output = os.listdir(path)
    file_list = []

    for i in output:
        if os.path.isdir(path+"/"+i): 
            file_list.extend(read_all_file(path+"/"+i)) 
        elif os.path.isfile(path+"/"+i):
            file_list.append(path+"/"+i)

    return file_list


def move_all_file(file_list, new_path):
    print("start move_all_file")
    
    #move all file
    print("move file")
    try:
        for src_path in file_list:
            if os.path.isdir(src_path) == True:
                continue
            file = src_path.split("/")[-1]
            #print("src_path, new_path :",src_path, new_path+"\\"+file)
            shutil.move(src_path, new_path+"\\"+file)
            #os.remove(src_path)
    except Exception as ex:
        print(ex.__str__(), "move_all_file")


#타겟폴더 내부에 있는 파일들을 타겟폴더로 모아준다.
def union_file(target_dir):
    # 타겟 폴더에 포함된 파일과 디렉토리를 받는다.
    print("target dir :", target_dir)
    
    file_list = read_all_file(target_dir)
    #print("file list\n", file_list)
    move_all_file(file_list, target_dir)


def runner(args):
    #union_file(args.src)
    video2frame(args.src)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', default="input_video.mp4") #input dir
    args = parser.parse_args()
    runner(args) 


#delete_picked_string_in_file("C:\\Users\\vbmrk\\PycharmProjects\\Yolov5_StrongSORT_OSNet\\runs\\track\\result.txt", "C", "640")
#video2frame("C:\\Users\\vbmrk\\Documents\\GitHub\\carom\\data\\videos\\lpba_8r.mp4")