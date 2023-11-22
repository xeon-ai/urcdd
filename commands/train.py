import json
import os

from ultralytics import YOLO

def train(args):
    """
    Trains a new model using the manifest file.
    """
    # Load the manifest file
    with open('manifest.json', 'r') as file:
        manifest = json.load(file)

    # Load the model
    model = YOLO(f"yolo/{manifest['model']['baseModel']}.pt")

    # Train the model
    results = model.train(
        data="./dataset/data.yaml",
        epochs=args.epochs,
        batch=args.batch_size,
        device=args.device,
    )

    # Save the model in onnx format to the models folder
    model.export(format='onnx')