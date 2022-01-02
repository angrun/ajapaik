import json
from utils.util import write_result_into_file

SOURCE_FILE = "../files/formatted_data.json"
NOT_APPLICABLE = "not applicable"


def read_tags():
    tags_data = {}

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
        fields_data = data["CatTagPhoto"][element]["fields"]
        tag = str(fields_data["tag"])
        tag_active = tags[tag]["active"]
        tag_level = tags[tag]["level"]
        tag_name = tags[tag]["name"]
        value = fields_data["value"]
        album = fields_data["album"]
        pic_id = str(fields_data["photo"])
        result_dict[pic_id]["album"] = album
        result_dict[pic_id]["tagging"].append(
            {"tag": tag, "tag_active": tag_active, "tag_level": tag_level, "tag_name": tag_name, "value": value,
             "value_name": get_tag_name(tags, tag, value)})

    for element in result_dict:
        result_dict[element]["most_popular_tag"] = get_most_popular_tag_per_picture(result_dict[element]["tagging"])
        result_dict[element]["most_popular_tag_value"] = get_most_popular_tag_value_per_picture(
            result_dict[element]["tagging"])

    for k, v in result_dict.items():
        tags = v["tagging"]
        tags.sort(key=lambda x: (int(x["tag"]), x["value"], x["tag_level"]))
        result_dict[k]["tagging"] = tags

    return result_dict


def get_tag_name(tags, tag, value):
    names = tags[tag]["name"].split("_")
    if value == 1:
        return names[0]
    if value == -1:
        return names[2]
    return NOT_APPLICABLE


def get_most_popular_tag_per_picture(tagging):
    result = {}
    for tag in tagging:
        if tag["value_name"] != NOT_APPLICABLE:
            if tag["tag_name"] in result:
                result[tag["tag_name"]] += 1
            else:
                result[tag["tag_name"]] = 1
    if result == {}:
        return "None"
    return max(result, key=result.get)


def get_most_popular_tag_value_per_picture(tagging):
    result = {}
    for tag in tagging:
        if tag["value_name"] != NOT_APPLICABLE:
            if tag["value_name"] in result:
                result[tag["value_name"]] += 1
            else:
                result[tag["value_name"]] = 1
    if result == {}:
        return "None"
    return max(result, key=result.get)


if __name__ == '__main__':
    data = read_file()
    write_result_into_file(data, "../files/formatted_data.json")
