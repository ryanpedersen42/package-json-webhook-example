import json

def convert_package_json(package_json_path):
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

    converted_data = data.copy()
    converted_data['dependencies'] = converted_dependencies

    return converted_data

def save_package_json(package_json_path, converted_data):
    with open(package_json_path, 'w') as file:
        json.dump(converted_data, file, indent=2)

# Example usage
package_json_path = 'package.json'
package_json_new_path = 'package-new.json'
converted_data = convert_package_json(package_json_path)
save_package_json(package_json_new_path, converted_data)