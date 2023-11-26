import json
import os
import roboflow
import yaml
import shutil

from dotenv import load_dotenv
from urllib.request import urlretrieve
from .utils import get_input, get_input_boolean

# Load environment variables from .env file
load_dotenv() 

def update_dataset(dataset, base_model):
    """
    Updates a dataset using the manifest file.
    """
    # We know that this is a Roboflow dataset, so create a Roboflow client
    client = roboflow.Roboflow(api_key=os.environ['ROBOFLOW_API_KEY'])

    workspace = client.workspace(dataset['workspace'])
    project = workspace.project(dataset['project'])

    if os.path.isdir('dataset'):
        shutil.rmtree('dataset')

    os.mkdir('dataset')

    # Get the latest version of the dataset
    latest_version = int(project.versions()[0].id.split('/')[-1])
    current_version = int(dataset['version'])

    # Check if the dataset is up to date
    if current_version != latest_version and get_input_boolean('Dataset is out of date. Would you like to update it?'):
        version = project.version(latest_version)
    # If we don't want to update the dataset, use the current version
    else:
        version = project.version(current_version)

    # Download the dataset
    version.download(model_format=base_model[:-1], location='./dataset/')

    # Update the manifest file with the new dataset version
    with open('manifest.json', 'r') as file:
        manifest = json.load(file)

    manifest['dataset']['version'] = str(latest_version)

    # Write the manifest file
    with open('manifest.json', 'w') as file:
        json.dump(manifest, file, indent=4)

    # Update the data.yaml file with the new dataset path
    with open('./dataset/data.yaml', 'r') as file:
        data = yaml.safe_load(file)

        data['path'] = os.path.abspath('.')

    with open('./dataset/data.yaml', 'w') as file:
        yaml.dump(data, file)

def update(args):
    """
    Updates an existing project using the manifest file.
    """
    # Check if we have a manifest file
    if not os.path.exists('manifest.json'):
        print('No manifest file found. Use `xeon init` to create one.')
        return

    # Load the manifest file
    with open('manifest.json', 'r') as file:
        manifest = json.load(file)

    # Check if this project uses a Roboflow dataset
    if 'dataset' in manifest and 'workspace' in manifest['dataset']:
        update_dataset(manifest['dataset'], manifest['model']['baseModel'])