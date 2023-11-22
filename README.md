# Welcome!
This is a template repository that hosts a basic computer vision model, discoverable on [xeon](https://xeon.fun). It comes with a basic python package that you can use to manage your model as well as its dataset. We have created a simple guide on how to create and publish your own models with this template below.

Before you start, make sure you have Python installed. You can install Python for your system [here](https://www.python.org/downloads/). Also, you need to install this project's dependencies. You can do this by running the following command in the root directory of this project:
```
pip install -r requirements.txt
```

## Initializing a Project
To get started, you need to initialize a new project with the `init` command. You will be prompted to answer a few questions regarding your project:
```console
> python cli.py init
Project name: Counter Blox
Project description: A yolov8 object detection model trained to identify character models in Roblox's popular Counter Blox game.
Author: xeon
---
Pretrained model [yolov8n]:
Path to dataset [dataset/]: https://universe.roboflow.com/xeon/counter-blox-640x640/dataset/8

Installing dataset...
loading Roboflow workspace...
loading Roboflow project...
Dependency ultralytics==8.0.134 is required but found version=8.0.203, to fix: `pip install ultralytics==8.0.134`
Downloading Dataset Version Zip in ./dataset/ to yolov8:: 100%|███████████████████████| 77922/77922 [00:03<00:00, 21433.96it/s]

Extracting Dataset Version Zip to ./dataset/ in yolov8:: 100%|█████████████████████| 3332/3332 [00:01<00:00, 2152.23it/s]
```
In this case we are using a public dataset hosted on Roboflow. It is highly recommended that you use a Roboflow dataset as this installation guide is designed around it. There are also tons of perks when it comes to using Roboflow datasets in your pojects. You can learn more about Roboflow on their [website](https://roboflow.com).
> **Note**: If a manifest.json file already exists, you can use the ``--force`` option to overwrite it. It will delete the file and prompt you just like displayed above. If you do not use the ``--force`` option, the project will install the dataset and other dependencies.

## Training 
Now that we have our data installed and our project initialized, we can begin traning the model. This can be done using the `train` command:
```console
> python cli.py train
``` 

You can use the ``--epochs`` and ``--batch-size`` arguments to manipulate the size and duration of the training sessions. The default values are 10 and 8 respectively, and these (for most cases) are the optimal values for YOLO object recognition. If you are interested in getting more consistent results, you can train your model on a larger epoch value (e.g. 50 or 100).

Training on your CPU can be quite slow so we recommend you train on your GPU. To do that, you must install CUDA and cuDNN. A good tutorial on how to set up such an environment can be found [here](https://medium.com/analytics-vidhya/installing-cuda-and-cudnn-on-windows-d44b8e9876b5). Once you're in a CUDA environment, use the `--device` argument to specify the devices you would like to use.

## Publishing
After a successful training run, you should see a new directory pop up called `runs/`. This directory will contain all of your training, validation, or test runs and their outputs. To publish a run, use the following command:
```console
> python cli.py publish
No run specified. Using the most recent run.
What version of the model is this? [0.0.1]: 
Model published successfully.
```
To avoid getting prompted for the version, you can pass the name of the version you want to publish with the ``--version`` argument. To specifically specify the run to publish you can pass the name of the run with ``--run``. If no run is specified, the latest one will be used.
