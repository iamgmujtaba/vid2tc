from moviepy.editor import VideoFileClip
from PIL import Image
from click import progressbar
import glob
import os
import random
import shutil
import tempfile
import cv2

TMP_FRAMES_PATH = tempfile.mkdtemp()
numb_tc = 0

def generate_video_thumbnails(input_video, interval, size, columns, output_path):
    main_out_dir = os.path.dirname(output_path)

    videoFileClip = VideoFileClip(input_video)
    outputPrefix = get_output_prefix()
    
    generate_frames(videoFileClip, interval, outputPrefix, size)
    generate_sprite_from_frames(outputPrefix, columns, size, output_path)

    showVideoInfo(input_video, main_out_dir)

def generate_frames(video_file_clip, interval, output_prefix, size):
    duration = video_file_clip.duration
    frame_count = 0
    total_frames = int(duration / interval)
    
    global numb_tc
    numb_tc = total_frames

    print("Extracting {} Thumbnails".format(total_frames))

    with progressbar(range(0, int(duration), interval)) as items:
        for i in items:
            frame_count += 1       
            extract_frame(video_file_clip, i, output_prefix, size, frame_count)

def extract_frame(video_file_clip, moment, output_prefix, size, frame_count):
    output = output_prefix + ("%05d.jpg" % frame_count)
    video_file_clip.save_frame(output, t=int(moment))
    resize_frame(output, size)

def resize_frame(filename, size):
    image = Image.open(filename)
    image = image.resize(size, Image.ANTIALIAS)
    image.save(filename)

def get_output_prefix():
    if not os.path.exists(TMP_FRAMES_PATH):
        os.makedirs(TMP_FRAMES_PATH)
    return TMP_FRAMES_PATH + os.sep + ("%032x_" % random.getrandbits(128))

def generate_sprite_from_frames(frames_path, columns, size, output_path):
    frames_map = sorted(glob.glob(frames_path + "*.jpg"))

    master_width = size[0] * columns
    master_height = size[1] * columns

    line, column, mode = 0, 0, 'RGBA'
    tc_counter = 0

    try:
        final_image = Image.new(mode=mode,size=(master_width, master_height),color=(0, 0, 0, 0) )
        final_image.save(os.path.join(output_path, "M_%01d.jpg" % tc_counter))
    except IOError:
        mode = 'RGB'
        final_image = Image.new(mode=mode, size=(master_width, master_height))

    for filename in frames_map:
        with Image.open(filename) as image:

            location_x = size[0] * column
            location_y = size[1] * line

            final_image.paste(image, (location_x, location_y))

            column += 1

            if column == columns:
                line += 1
                column = 0
            
            if line == columns:
                final_image.save(os.path.join(output_path, "M_%01d.jpg" % tc_counter))
                
                tc_counter +=1
                line = 0

    final_image.save(os.path.join(output_path, "M_%01d.jpg" % tc_counter))

    shutil.rmtree(TMP_FRAMES_PATH, ignore_errors=True)

#Show video information
def showVideoInfo(video_path, output_path):
    info_file = open(os.path.join(output_path, "video_info.txt"), "w") 
    try:
        vhandle = cv2.VideoCapture(video_path)
        fps = vhandle.get(cv2.CAP_PROP_FPS)
        count = vhandle.get(cv2.CAP_PROP_FRAME_COUNT)
        size = (int(vhandle.get(cv2.CAP_PROP_FRAME_WIDTH)), int(vhandle.get(cv2.CAP_PROP_FRAME_HEIGHT)))      
        ret, firstframe = vhandle.read()

        if ret:
            print("FPS: %.2f" % fps)
            print("COUNT: %.2f" % count)
            print("WIDTH: %d" % size[0])
            print("HEIGHT: %d" % size[1])
           
            info_file.write("FPS: %.2f" % fps +' \n')
            info_file.write("Frames: %.2f" % count + '\n')
            info_file.write("WIDTH: %d" % size[0] + '\n')
            info_file.write("HEIGHT: %d" % size[1] + '\n')
            info_file.write("Thumbnail Containers: " + str(int(numb_tc/25)+1) + '\n')
            info_file.write("Thumbnails: " + str(numb_tc) )
            info_file.close()
            return vhandle, fps, size, firstframe
        else:
            print("Video can not read!")
    except:
        "Error in showVideoInfo"   
