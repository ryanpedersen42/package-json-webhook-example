## Import the needed libraries
import requests
from decouple import config
import json

# Get environment variables using the config object or os.environ["KEY"]
# These are the credentials passed by the variables of your pipeline to your tasks and in to your env
WEBHOOK_URL = config("WEBHOOK_URL")
SERVICE_ID = config("SERVICE_ID")
PATH_TO_PACKAGE_JSON_FILE = config("PATH_TO_PACKAGE_JSON_FILE")


def add_entity_to_port(entity_object):
    """A function to create the passed entity in Port using the webhook URL

    Params
    --------------
    entity_object: dict
        The entity to add in your Port catalog
    
    Returns
    --------------
    response: dict
        The response object after calling the webhook
    """
    headers = {"Accept": "application/json"}
    response = requests.post(WEBHOOK_URL, json=entity_object, headers=headers)
    return response.json()


def convert_package_json(package_json_path):
    """This function takes a package.json file path, converts the "dependencies" property into a 
    JSON array using three keys (name, version, and id). It then sends this data to Port

    Params
    --------------
    package_json_path: str
        The path to the package.json file relative to the project's root folder
    
    Returns
    --------------
    response: dict
        The response object after calling the webhook
    """
    with open(package_json_path) as file:
        data = json.load(file)

    dependencies = data.get('dependencies', {})

    converted_dependencies = []
    for index, (name, version) in enumerate(dependencies.items(), start=1):
        pkg_id = f"pkg-{index}"
        converted_dependencies.append({
            'name': name,
            'version': version,
            'id': pkg_id
        })

    entity_object = {
        "service": SERVICE_ID,
        "dependencies": converted_dependencies
    }
    webhook_response = add_entity_to_port(entity_object)
    return webhook_response

converted_data = convert_package_json(PATH_TO_PACKAGE_JSON_FILE)
print(converted_data)