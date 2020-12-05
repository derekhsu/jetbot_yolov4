# Project

## Prepare image

### Method 1

Download the latest image from the link below according to your type of Jetson Nano and burn it into a SD card. 

https://jetbot.org/master/software_setup/sd_card.html

Install dependencies

```
sudo apt install libffi-dev
sudo pip3 install ipywidgets
sudo pip3 install traitlets
cd ~/jetbot
sudo python3 setup.py install
```

You need install Pytorch in order to run jetbot module, the instrution can be refer to https://forums.developer.nvidia.com/t/pytorch-for-jetson-version-1-7-0-now-available/72048.

Download Pytorch whl file according to your jetpack version. The script listed below installs for JetPack version 4.4.1

```
wget https://nvidia.box.com/shared/static/9eptse6jyly1ggt9axbja2yrmj6pbarc.whl -O torch-1.7.0-cp36-cp36m-linux_aarch64.whl
sudo apt-get install python3-pip libopenblas-base libopenmpi-dev 
pip3 install Cython
pip3 install numpy torch-1.7.0-cp36-cp36m-linux_aarch64.whl
```

Install libcanberra-gtk-module
```
sudo apt install libcanberra-gtk-module libcanberra-gtk3-module
```

### Method 2

## Model Training

## Car Deploying

This section introduces how to prepare the environment in your jetbot.


Install gdown for downloading TensorRT model from the google drive

```
sudo pip3 install gdown
```

Clone the project of tensorrt_demos to your home directory, and then setup environment by following its instruction.

```
git clone https://github.com/jkjung-avt/tensorrt_demos.git
```

Download model and config from the google drive (For CUDA 10.0)
```
cd ~/tensorrt_demos/yolo
gdown 'https://drive.google.com/uc?id=1nuVzboVN6sJLrQengTObuCrTUPzVMRtU'
gdown 'https://drive.google.com/uc?id=1LfTOhGf3C3cVMrLwG1MrXrdTnrH3sZMb'
```

Download model and config from the google drive (For CUDA 10.2)

```
cd ~/tensorrt_demos/yolo
gdown 'https://drive.google.com/uc?id=1Xl5ZJ3RNb2H-D3wx4ZyXnlbFYFXaJ2Aw'
gdown 'https://drive.google.com/uc?id=1LfTOhGf3C3cVMrLwG1MrXrdTnrH3sZMb'
```

Copy 'main.py' in this project to ~/tensorrt_demos

```
cp main.py ~/tensorrt_demos
```

Finally, you can run main.py now.

```
cd ~/tensorrt_demos
python3 main.py
```
