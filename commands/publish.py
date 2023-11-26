import json
import os
import roboflow
import shutil

from dotenv import load_dotenv
from .utils import get_input, get_input_boolean

# Load environment variables from .env file
load_dotenv() 

def get_run(name):
    """
    Gets the run with the specified name.
    """
    if name is None:
        print("No run specified. Using the most recent run.")
        # Get the most recent run
        runs = os.listdir('./runs/detect/')
        runs.sort()

        runs = [x for x in runs if x.startswith('train')]
        
        return runs[-1]
    
    return name

def publish(args):
    """
    Pubishes a model from a successful training run.
    """
    # Load the manifest file
    with open('manifest.json', 'r') as file:
        manifest = json.load(file)

    if not os.path.exists('publish'):
        os.mkdir('publish')

    run = get_run(args.run)
    version = args.version if args.version else get_input('What version of the model is this?', "0.0.1")

    manifest['version'] = dict()
    manifest['version']['name'] = version
    manifest['version']['run'] = run

    # Check if a model with the same version already exists
    if not (f"{version}.onnx" in os.listdir('./publish/') and not get_input_boolean('A model with the same version already exists. Do you want to overwrite it?')):
        # Move the ONNX model to the publish directory
        shutil.copyfile(f'./runs/detect/{run}/weights/best.onnx', f'./publish/{version}.onnx')

    if manifest['dataset'].get('workspace') is not None:
        # We know that this is a Roboflow dataset, so create a Roboflow client
        client = roboflow.Roboflow(api_key=os.environ['ROBOFLOW_API_KEY'])

        workspace = client.workspace(manifest['dataset']['workspace'])
        project = workspace.project(manifest['dataset']['project'])
        version = project.version(int(manifest['dataset']['version']))

        version.deploy(manifest['model']['baseModel'][:-1], f"./runs/detect/{run}")

    print('Model published successfully.')

    # Save the manifest file
    with open('manifest.json', 'w') as file:
        json.dump(manifest, file, indent=4)
