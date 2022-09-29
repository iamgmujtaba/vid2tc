import glob
import os
from subprocess import call

from utils.thumbnails_generator import generate_video_thumbnails
from utils.prepare_tc_csv import create_tc_csv
from config import parse_opts

config = parse_opts()

def generate_segments(input_video, dest_dir, seg_len):
    cmd = 'ffmpeg -i '+ input_video +' -force_key_frames "expr:gte(t,n_forced*10)" -strict -2 -c:a aac -c:v libx264 -f segment -segment_list_type m3u8 -segment_list_size 0 -segment_time '+str(seg_len)+' -segment_time_delta 0.1 -segment_list ' +dest_dir+'out.m3u8 ' +dest_dir+'out%02d.ts'
    print(cmd)
    call(cmd,shell=True)

def vid2wav(input_video, dest_dir):
    cmd = 'ffmpeg -i ' + input_video +' -ac 2 -f wav ' + dest_dir + '/input.wav'
    print(cmd)
    call(cmd,shell=True)

def wav2mp3(input_dir, dest_dir):
    cmd = 'ffmpeg -i '+input_dir+'/input.wav -vn -ar 44100 -ac 2 -b:a 192k '+ dest_dir+'/input.mp3'     
    print(cmd)
    call(cmd,shell=True)

def vid2frames(input_video, dest_dir):
    cmd = 'ffmpeg -i ' + input_video +' -qscale:v 2 -vf fps=1 ' + dest_dir + '/02%d.jpg'
    print(cmd)
    call(cmd,shell=True)

def start_process(input_path, output_path):
    for file_name in [input_path]:
        video_list = glob.glob(file_name + '*.mp4')
        for video in video_list:
            print('-'*60)
            print('File Name: ', video)

            video_file_name = video.split('/')[-1].split(".")[0]

            main_video_path = os.path.join(output_path, video_file_name)
            seg_path = os.path.join(main_video_path, 'segments')
            audio_path = os.path.join(main_video_path, 'audio')
            frames_path = os.path.join(main_video_path, 'frames')
            thumbnail_path = os.path.join(main_video_path, 'thumbnails')
            
            # Generate thumbnails from the video
            if not os.path.exists(thumbnail_path):
                print(thumbnail_path)
                os.makedirs(thumbnail_path)
                thumbnail_size = (config.thumb_width, config.thumb_height)

                generate_video_thumbnails(video, config.thumb_interval, thumbnail_size, config.thumb_container, thumbnail_path)
                create_tc_csv(thumbnail_path, main_video_path)

            # Split the video into HLS segments
            if not os.path.exists(seg_path):
                print(seg_path)
                os.makedirs(seg_path)
                generate_segments(video, seg_path + '/', config.seg_len)
            
            # Extract audio
            if config.audio:
                if not os.path.exists(audio_path):
                    print(audio_path)
                    os.makedirs(audio_path)    
                    vid2wav(video, audio_path)
                    #comment if you don't want to convert to mp3
                    wav2mp3(audio_path, audio_path)

            # Extract frames
            if config.frames:
                if not os.path.exists(frames_path):
                    print(frames_path)
                    os.makedirs(frames_path)
                    vid2frames(video, frames_path)

  
if __name__ == '__main__':
    start_process(config.inp_path, config.out_path)
    print('All process completed')
