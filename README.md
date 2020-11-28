# Project

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
