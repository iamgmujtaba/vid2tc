import os
import glob
import subprocess
import argparse

from utils.thumbnails_generator import generate_video_thumbnails
from utils.prepare_tc_csv import create_tc_csv

def generate_segments(input_video, dest_dir, seg_len):
    cmd = [
        'ffmpeg',
        '-i', input_video,
        '-force_key_frames', 'expr:gte(t,n_forced*10)',
        '-strict', '-2',
        '-c:a', 'aac',
        '-c:v', 'libx264',
        '-f', 'segment',
        '-segment_list_type', 'm3u8',
        '-segment_list_size', '0',
        '-segment_time', str(seg_len),
        '-segment_time_delta', '0.1',
        '-segment_list', os.path.join(dest_dir, 'out.m3u8'),
        os.path.join(dest_dir, 'out%02d.ts')
    ]
    print(' '.join(cmd))
    subprocess.run(cmd)

def vid2wav(input_video, dest_dir):
    output_wav = os.path.join(dest_dir, 'input.wav')
    cmd = [
        'ffmpeg',
        '-i', input_video,
        '-ac', '2',
        '-f', 'wav',
        output_wav
    ]
    print(' '.join(cmd))
    subprocess.run(cmd)

def wav2mp3(input_dir, dest_dir):
    input_wav = os.path.join(input_dir, 'input.wav')
    output_mp3 = os.path.join(dest_dir, 'input.mp3')
    cmd = [
        'ffmpeg',
        '-i', input_wav,
        '-vn',
        '-ar', '44100',
        '-ac', '2',
        '-b:a', '192k',
        output_mp3
    ]
    print(' '.join(cmd))
    subprocess.run(cmd)

def vid2frames(input_video, dest_dir):
    output_pattern = os.path.join(dest_dir, '02%d.jpg')
    cmd = [
        'ffmpeg',
        '-i', input_video,
        '-qscale:v', '2',
        '-vf', 'fps=1',
        output_pattern
    ]
    print(' '.join(cmd))
    subprocess.run(cmd)

def start_process(input_path, output_path, args):
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
                os.makedirs(thumbnail_path, exist_ok=True)
                thumbnail_size = (args.thumb_width, args.thumb_height)

                generate_video_thumbnails(
                    video, 
                    args.thumb_interval, 
                    thumbnail_size, 
                    args.thumb_container, 
                    thumbnail_path
                )
                create_tc_csv(thumbnail_path, main_video_path)
            
            # Split the video into HLS segments
            if not os.path.exists(seg_path):
                print(seg_path)
                os.makedirs(seg_path)
                generate_segments(video, seg_path + '/', args.seg_len)
            
            # Extract audio
            if args.audio:
                if not os.path.exists(audio_path):
                    print(audio_path)
                    os.makedirs(audio_path)    
                    vid2wav(video, audio_path)
                    #comment if you don't want to convert to mp3
                    wav2mp3(audio_path, audio_path)

            # Extract frames
            if args.frames:
                if not os.path.exists(frames_path):
                    print(frames_path)
                    os.makedirs(frames_path)
                    vid2frames(video, frames_path)


def parse_opts():
    parser = argparse.ArgumentParser()
    # Basic arguments
    parser.add_argument('-i', '--inp_path', type=str, default='./input/', help='Input videos path')
    parser.add_argument('-o', '--out_path', type=str, default='./output/', help='Output videos path')
    
    parser.add_argument('-s', '--seg_len', type=int, default=10, help='Segments length (seconds)')
    parser.add_argument('-a','--audio', type=bool, default=False, help='Extract audio (True/False)')
    parser.add_argument('-f','--frames', type=bool, default=False, help='Extract video frames (True/False)')
    
    # Thumbnail arguments
    parser.add_argument('--thumb_width', type=int, default=160, help='Thumbnail width')
    parser.add_argument('--thumb_height', type=int, default=90, help='Thumbnail height')
    parser.add_argument('--thumb_interval', type=int, default=1, help='Thumbnail extraction interval in seconds')
    parser.add_argument('--thumb_container', type=int, default=5, help='Thumbnail container size (e.g. 5 means 5x5 grid)')
    
    return parser.parse_args()
def main():
    args = parse_opts()
    start_process(args.inp_path, args.out_path, args)

if __name__ == "__main__":
    main()
