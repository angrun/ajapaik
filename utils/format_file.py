import json

SOURCE_FILE = "../source_file.json"
value_descriptions = {"0": "not applicable", "1": "natural", "-1": "staged"}


def read_tags():
    tags_data = {}
d
    f = open(SOURCE_FILE)
    data = json.load(f)
    for element in data["CatTag"]:
        fields_data = data["CatTag"][element]["fields"]
        tags_data[element] = {"active": fields_data["active"], "level": fields_data["level"],
                              "name": fields_data["name"]}
    return tags_data


def read_file():
    tags = read_tags()

    f = open(SOURCE_FILE)
    data = json.load(f)
    result_dict = {}

    for element in data['CatPhoto']:
        pic_id = element
        inner_data = data['CatPhoto'][element]
        fields_data = data['CatPhoto'][element]['fields']
        result_dict[pic_id] = {"id": pic_id, "description": fields_data["slug"], "url": inner_data["description_url"],
                               "tagging": []}

    for element in data["CatTagPhoto"]:
        fields_data = data["CatTagPhoto"][element]['fields']
        tag = str(fields_data['tag'])
        tag_active = tags[tag]["active"]
        tag_level = tags[tag]["level"]
        tag_name = tags[tag]["name"]
        value = fields_data['value']
        album = fields_data['album']
        pic_id = str(fields_data['photo'])
        result_dict[pic_id]["album"] = album
        result_dict[pic_id]["tagging"].append(
            {"tag": tag, "tag_active": tag_active, "tag_level": tag_level, "tag_name": tag_name, "value": value,
             "value_name": value_descriptions[str(value)]})

    for k, v in result_dict.items():
        tags = v["tagging"]
        tags.sort(key=lambda x: (int(x["tag"]), x["value"], x["tag_level"]))
        result_dict[k]["tagging"] = tags

    return result_dict


def write_result_into_file(data):
    with open('formatted_data.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    data = read_file()
    write_result_into_file(data)
