import json

old_filename = 'parameters/.values/old_parameter_values.json'
new_filename = 'parameters/.values/new_parameter_values.json'

if __name__ == '__main__':
    with open(old_filename, 'r') as infile:
        old_data = json.load(infile)
    
    new_data = {}
    for device_name, device_parameters in old_data.items():
        for parameter_name, parameter_value in device_parameters.items():
            new_data_key = '{}.{}'.format(device_name, parameter_name.replace('*', ''))
            new_data[new_data_key] = parameter_value
    
    with open(new_filename, 'w') as outfile:
        json.dump(new_data, outfile)
