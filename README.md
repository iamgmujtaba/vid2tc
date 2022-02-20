# Generate thumbnai containers from videos like YouTube

This repository explains the process to generate thumbnail contaienrs from videos. In recent years, several methods have been designed to improve the demanding timeline manipulation for video browsing. One of the most popular methods for web-based video players is the use of lightweight thumbnail containers. Users can skim through the video player for efficiency and instantly preview a lengthy video, by watching the thumbnails preview in the web player interface. As the thumbnails are easy to integrate and navigate in web-based video players, several famous video-on-demand (VoD) streaming platforms adopt these in their end-user video players [ref1](https://arxiv.org/abs/2201.09049).


<p>
  <center>
<img src="https://github.com/iamgmujtaba/tc-generator/blob/master/figures/thumb_sample.png" width="550" height="300">
    </center>
<em>
  Orientation of thumbnails on a single thumbnail container image (left), and the thumbnail usage for instant preview in the client webbased YouTube video player (right) .
  </em>
</p>


## Getting Started
### Installation
- Clone the repo by using the following command.
```shell
git clone https://github.com/iamgmujtaba/vid2tc
cd vid2tc
```
- To install dependencies using pip please type the command.
```shell
pip install -r requirements.txt
```

### Usage

```shell
python .\main.py -h

`optional arguments:
  -h, --help            show this help message and exit
  -i INP_PATH, --inp_path INP_PATH   Input videos path
  -o OUT_PATH, --out_path OUT_PATH   Output videos path
  -s SEG_LEN,  --seg_len SEG_LEN     Segments length (seconds)
  -a AUDIO,    --audio AUDIO         Extract audio (True/False)
  -f FRAMES,   --frames FRAMES       Extract video frames (True/False)
  --thumb_width THUMB_WIDTH          Width of the each thumbnail
  --thumb_height THUMB_HEIGHT        Height of the each thumbnail
  --thumb_interval THUMB_INTERVAL    Extract first frame as thumbnails at every 1 second
  --thumb_container THUMB_CONTAINER  5x5 (row,cloumn) is default Thumbnail Containers
```
#### Example
To generate thumbnail containers and prepare video sgemgnets run the following script.
```shell
python .\main.py -i .\input\ -o .\output\
```

## Citation
This is code is used in the following papers. If you use this code for your research, please cite our paper.
```bash
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
  journal={arXiv preprint arXiv:2201.09049},
  year={2022}
}

@article{mujtaba2022ltc,
  title={LTC-GIF: Attracting More Clicks on Feature-length Sports Videos},
  author={Mujtaba, Ghulam and Choi, Jaehyuk and Ryu, Eun-Seok},
  journal={arXiv preprint arXiv:2201.09077},
  year={2022}
}

@article{mujtaba2021,
  title={Client-driven animated GIF generation framework using an acoustic feature},
  author={Mujtaba, Ghulam and Lee, Sangsoon and Kim, Jaehyoun and Ryu, Eun-Seok},
  journal={Multimedia Tools and Applications},
  year={2021},
  publisher={Springer}}
```


### Acknowledgement:
The base code for this repository is borrowed from [Video Thumbnail Generator](https://github.com/flavioribeiro/video-thumbnail-generator).
