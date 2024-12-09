import cv2
import tempfile
from pathlib import Path
from tqdm import tqdm
from PIL import Image
import shutil

TMP_FRAMES_PATH = tempfile.mkdtemp()
numb_tc = 0

def generate_video_thumbnails(input_video, interval, size, columns, output_path):
    """Generate video thumbnails with progress tracking"""
    video_capture = cv2.VideoCapture(input_video)
    if not video_capture.isOpened():
        raise ValueError("Could not open video file")

    fps = video_capture.get(cv2.CAP_PROP_FPS)
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = int(total_frames / fps)
    
    output_prefix = get_output_prefix()
    generate_frames(video_capture, interval, fps, output_prefix, size, duration)
    generate_sprite_from_frames(output_prefix, columns, size, output_path)
    show_video_info(input_video, Path(output_path).parent)
    clean_temp_files()
    video_capture.release()

def generate_frames(video_capture, interval, fps, output_prefix, size, duration):
    """Extract frames chronologically with progress tracking"""
    total_frames = duration // interval
    global numb_tc
    numb_tc = total_frames

    for frame_count, t in enumerate(tqdm(range(0, duration, interval), 
                                       desc="Extracting frames", 
                                       total=total_frames), 1):
        frame_pos = int(t * fps)
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
        success, frame = video_capture.read()
        
        if success:
            output = f"{output_prefix}{frame_count:05d}.jpg"
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)
            image.thumbnail(size, Image.LANCZOS)
            image.save(output)

def get_output_prefix():
    """Create temporary directory for frames"""
    Path(TMP_FRAMES_PATH).mkdir(parents=True, exist_ok=True)
    return str(Path(TMP_FRAMES_PATH) / "frame_")

def generate_sprite_from_frames(frames_path, columns, size, output_path):
    """Generate sprite sheets from frames"""
    frames_map = sorted(list(Path(TMP_FRAMES_PATH).glob("*.jpg")))
    master_width = size[0] * columns
    master_height = size[1] * columns
    
    tc_counter = 0
    line = column = 0
    
    # Always create RGB image for JPEG compatibility
    final_image = Image.new(mode='RGB', size=(master_width, master_height), color=(255, 255, 255))

    try:
        for frame_path in frames_map:
            with Image.open(frame_path) as image:
                # Convert to RGB if needed
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                location_x = size[0] * column
                location_y = size[1] * line
                final_image.paste(image, (location_x, location_y))
                
                column += 1
                if column == columns:
                    line += 1
                    column = 0
                
                if line == columns:
                    sprite_path = Path(output_path) / f"M_{tc_counter:02d}.jpg"
                    final_image.save(sprite_path, format='JPEG', quality=95)
                    tc_counter += 1
                    line = 0
                    final_image = Image.new(mode='RGB', size=(master_width, master_height), color=(255, 255, 255))

        # Save any remaining images
        if line > 0 or column > 0:
            sprite_path = Path(output_path) / f"M_{tc_counter:02d}.jpg"
            final_image.save(sprite_path, format='JPEG', quality=95)
    except Exception as e:
        print(f"Error generating sprite sheet: {e}")
        raise

def show_video_info(video_path, output_path):
    """Save video information to file"""
    video = cv2.VideoCapture(video_path)
    info = {
        'duration': video.get(cv2.CAP_PROP_FRAME_COUNT) / video.get(cv2.CAP_PROP_FPS),
        'fps': video.get(cv2.CAP_PROP_FPS),
        'width': int(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    }
    video.release()
    
    info_path = Path(output_path) / "video_info.txt"
    with open(info_path, 'w') as f:
        for key, value in info.items():
            f.write(f"{key}: {value}\n")

def clean_temp_files():
    """Clean up temporary files"""
    try:
        shutil.rmtree(TMP_FRAMES_PATH, ignore_errors=True)
    except Exception as e:
        print(f"Warning: Could not clean temporary files: {e}")