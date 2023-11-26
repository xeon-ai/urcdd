from ultralytics import YOLO

def predict(args):
    """Run an inference on an image"""
    model = YOLO(args.model)

    model.predict(args.image)

    print('Predictions saved to predictions/')