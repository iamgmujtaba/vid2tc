import argparse

def parse_opts():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--inp_path', type=str, default='./input/', help='Input videos path')
    parser.add_argument('-o','--out_path', type=str, default='./output/', help='Output videos path')

    parser.add_argument('-s','--seg_len', type=int, default=10.0, help='Segments length (seconds)')
    parser.add_argument('-a','--audio', type=bool, default=False, help='Extract audio (True/False)')
    parser.add_argument('-f','--frames', type=bool, default=False, help='Extract video frames (True/False)')

    #Thumbnails Configurations
    # 160x90 is the default thumbnail size in the YouTube web player
    parser.add_argument('--thumb_width', type=str, default=160, help='Width of the each thumbnail')
    parser.add_argument('--thumb_height', type=str, default=90, help='Height of the each thumbnail')
    parser.add_argument('--thumb_interval', type=str, default=1, help='Extract first frame as thumbnails in every second')
    parser.add_argument('--thumb_container', type=str, default=5, help='5x5 (row,cloumn) is default Thumbnail Containers')

    return parser.parse_args()
