import json
from json.decoder import JSONDecodeError


def get_json_with_values(values_file_name, structure_file_name):
    with open(values_file_name) as file:
        values = json.load(file)

    dict_values = {}

    for item in values["values"]:
        dict_values[item["id"]] = item["value"]

    with open(structure_file_name, 'r') as file:
        try:
            test_case = json.load(file)

            def go_through_dict(obj):
                for k, v in obj.items():
                    if isinstance(v, dict):
                        if v["id"] in list(dict_values.keys()):
                            v["value"] = dict_values[v["id"]]
                        go_through_dict(v)
                    elif isinstance(v, list):
                        for val in v:
                            if val["id"] in dict_values.keys():
                                val["value"] = dict_values[val["id"]]
                            go_through_dict(val)

            go_through_dict(test_case)

            with open('Result.json', 'w') as f:
                json.dump(test_case, f,
                          indent=4,
                          ensure_ascii=False,
                          separators=(',', ': '))
        except JSONDecodeError:
            data = {"error":
                        {"message": "Входные файлы некорректны"}
                    }
            with open('error.json', 'w') as f:
                json.dump(data, f,
                          indent=4,
                          ensure_ascii=False,
                          separators=(',', ': '))


get_json_with_values('Values.json', 'TestcaseStructure.json')
get_json_with_values('Values.json', 'TestcaseStructureWithError.json')
