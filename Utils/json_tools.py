import json


def dump_to_json(data, filepath):
    # Serializing json
    json_object = json.dumps(data, indent=4)

    # Writing to sample.json
    with open(filepath, "w") as outfile:
        outfile.write(json_object)


def read_from_json(filepath):
    with open(filepath, "r") as openfile:
        # Reading from json file
        json_object = json.load(openfile)
    return json_object


def get_field(json, key, filterBy=""):
    values = []

    # entry: {name: string, id: number}
    for entry in json:
        if len(filterBy) > 1: 
            if(entry["name"] == filterBy):
                return entry["id"]
        else:
            values.append(entry[str(key)])
    return values

