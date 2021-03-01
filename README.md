# Face Detection and Tracking

Phát hiện và theo dõi khuôn mặt thời gian thực, sử dụng MOSSE và OpenCV


## Installation

```bash
chmod +x install.sh

```
To run your script, enter:
```bash
./install.sh
```
Another option is as follows to execute shell script:
```bash
sh install.sh
```
OR
```bash
bash install.sh
```
### How to use Usage

```bash
python3 run.py --video_src 0 
```

* Trong đó: 0 video_src là nguồn đầu vào hình ảnh 

Để kiểm tra toàn bộ danh sách thiêt bị ngoại vi được conect 


```bash
v4l2-ctl --list-device
```

Kết quả:

Integrated Webcam: Integrated W (usb-0000:00:14.0-5):
	/dev/video0
	/dev/video1

## Contributing

## License
