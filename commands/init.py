import json
import os

from urllib.parse import urlparse
from .update import update_dataset
from .utils import get_input, get_input_boolean

allowed_models = ["yolov8n", "yolov8s", "yolov8m", "yolov8l", "yolov8x"]

def get_manifest():
    """
    Builds a new manifest.json file with the provided user inputs.
    """
    data = dict()

    # Get basic information on the project
    data['name'] = get_input('Project name')
    data['description'] = get_input('Project description')
    data['author'] = get_input('Author')

    print('---')
    
    # Get specific information on the model associated with the project
    data['model'] = dict()
    data['model']['baseModel'] = get_input('Pretrained model', 'yolov8n')

    # Check if the model is valid
    if data['model']['baseModel'] not in allowed_models:
        print('Invalid model. Please choose one of the following:')
        print(allowed_models)
        return

    # Get information on the dataset associated with the project
    data['dataset'] = dict()
    data['dataset']['path'] = get_input('Path to dataset', 'dataset/')

    # Parse the dataset path as a URL
    url = urlparse(data['dataset']['path'])

    # Check if the dataset path exists
    if url.netloc == '' and not os.path.exists(data['dataset']['path']):
        print('Dataset path does not exist.')
        return
    
    # If the dataset path is a robloflow dataset URL, parse it
    if url.netloc in ['universe.roboflow.com', 'app.roboflow.com']:
        split = url.path.split('/')

        size = len(split)
        # Check if the dataset path is valid
        if size > 5 or size < 4:
            print('Invalid dataset URL. Make sure you copy it exactly as it appears in the Roboflow app.')
            return

        data['dataset']['workspace'] = split[1]
        data['dataset']['project'] = split[2]
        data['dataset']['version'] = int(split[3] if size == 4 else split[4])

        print("\nInstalling dataset...")
        update_dataset(data['dataset'], data['model']['baseModel'])


    return data

def init(args):
    """
    Initialize a new xeon project.
    """
    # Check if we already have a manifest file
    if os.path.exists('manifest.json') and not args.force:
        print('A manifest file already exists. Use --force to overwrite it.')

        # Load the manifest file
        with open('manifest.json', 'r') as file:
            manifest = json.load(file)
    else:
        # Get the manifest data
        manifest = get_manifest()

        # Write the manifest file
        with open('manifest.json', 'w') as f:
            json.dump(manifest, f, indent=4)
    