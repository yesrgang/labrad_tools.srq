import json

old_filename = 'parameters/.values/20181030.json'
new_filename = 'parameters/.values/current.json'

if __name__ == '__main__':
    with open(old_filename, 'r') as infile:
        old_data = json.load(infile)
    
    with open(new_filename, 'r') as infile:
        new_data = json.load(infile)

    new_data.update(old_data)

    with open(new_filename, 'w') as outfile:
        json.dump(new_data, outfile)
