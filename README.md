# Generate Thumbnail Containers from Videos like YouTube

This repository explains the process of generating thumbnail containers from videos. In recent years, several methods have been designed to improve the demanding timeline manipulation for video browsing. One of the most popular methods for web-based video players is using lightweight thumbnail containers. Users can quickly skim through the video player and instantly preview a lengthy video by watching the thumbnail preview in the web player interface. As the thumbnails are easy to integrate and navigate in web-based video players, several famous video-on-demand (VoD) streaming platforms adopt these in their end-user video players [ref1](https://arxiv.org/abs/2201.09049).

<p align="center">
  <img src="https://github.com/iamgmujtaba/vid2tc/blob/master/figures/thumb_sample.png" width="550" height="300">
</p>
<p align="center">
  <em>Orientation of thumbnails on a single thumbnail container image (left), and the thumbnail usage for instant preview in the client web-based YouTube video player</em>
</p>

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)
- [References](#references)

## Overview
This project provides a framework to generate thumbnail containers from videos, similar to the functionality on platforms like YouTube. The generated thumbnails can provide instant previews in web-based video players, enhancing the user experience by allowing efficient video browsing.

## Installation
To install and set up the project, follow these steps:

- Clone the repository
```bash
git clone https://github.com/iamgmujtaba/vid2tc.git
```

- Navigate to the project directory

```bash
cd vid2tc
```

- Create an anaconda environment and install packages
```bash
conda create -n vid2tc python=3.10 -y
conda activate vid2tc
```

- To install dependencies using pip please type the command.
```bash
pip install -r requirements.txt
```
## Usage
To use the project, run the main script with the appropriate arguments. Below is an example command:


```bash
python .\main.py -h

`optional arguments:
  -h, --help            show this help message and exit
  -i INP_PATH, --inp_path INP_PATH   Input videos path
  -o OUT_PATH, --out_path OUT_PATH   Output videos path
  -s SEG_LEN,  --seg_len SEG_LEN     Segments length (seconds)
  -a AUDIO,    --audio AUDIO         Extract audio (True/False)
  -f FRAMES,   --frames FRAMES       Extract video frames (True/False)
  --thumb_width THUMB_WIDTH          Thumbnail width
  --thumb_height THUMB_HEIGHT        Thumbnail height
  --thumb_interval THUMB_INTERVAL    Thumbnail extraction interval in seconds
  --thumb_container THUMB_CONTAINER  Thumbnail container size (e.g. 5 means 5x5 grid)
```

## Example
To generate thumbnail containers and prepare video segments, run the following script.
```bash
python .\main.py -i .\input\ -o .\output\
```

## References
This code is referenced in the following papers. If you utilize this code for your research, please cite our work.
```bash
@article{mujtaba2023frc,
  title = {FRC-GIF: Frame Ranking-based Personalized Artistic Media Generation Method for Resource Constrained Devices},
  author = {Mujtaba, Ghulam and Ali Khowaja, Sunder and Aslam Jarwar, Muhammad and Choi, Jaehyuk and Ryu, Eun-Seok},
  journal = {IEEE Transactions on Big Data},
  volume = {},
  pages = {1-14},
  year = {2023},
  publisher = {IEEE},
  doi = {10.1109/TBDATA.2023.3338012},
}

@article{mujtaba2020client,
  title={Client-driven personalized trailer framework using thumbnail containers},
  author={Mujtaba, Ghulam and Ryu, Eun-Seok},
  journal={IEEE Access},
  volume={8},
  pages={60417--60427},
  year={2020},
  publisher={IEEE}
}

@article{mujtaba2022ltc,
  title={LTC-SUM: Lightweight Client-driven Personalized Video Summarization Framework Using 2D CNN},
  author={Mujtaba, Ghulam and Malik, Adeel and Ryu, Eun-Seok},
  journal={IEEE Access},
  year={2022}
}

@article{mujtaba2021,
  title={Client-driven animated GIF generation framework using an acoustic feature},
  author={Mujtaba, Ghulam and Lee, Sangsoon and Kim, Jaehyoun and Ryu, Eun-Seok},
  journal={Multimedia Tools and Applications},
  year={2021},
  publisher={Springer}}
```
