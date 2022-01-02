import json

from utils.util import write_result_into_file

# Current logic transforms formatted_data.json to format where each picture has just one
# category left (the one which is most popular)

SOURCE_FILE = "../files/formatted_data.json"
MOST_POPULAR_CATEGORY = "interior_or_exterior"


def transform_formatted_data_to_one_hot_encoding():
    result = {}
    f = open(SOURCE_FILE)
    data = json.load(f)
    for element in data:
        data[element].pop("tagging", None)

    result["data"] = data
    write_result_into_file(result, "../files/one_hot_encoding_data.json")
    return result


def transform_data_leave_only_data_of_one_most_popular_category():
    result = {}
    f = open(SOURCE_FILE)
    data = json.load(f)
    element_to_delete = []
    for element in data:
        most_popular_category = data[element]["most_popular_tag"]
        if most_popular_category != MOST_POPULAR_CATEGORY:
            element_to_delete.append(element)
            # data.pop(element, None)
        else:
            most_popular_tag = calculate_most_popular_tag(data[element]["tagging"])
            data[element]["most_popular_tag_value"] = most_popular_tag
            data[element].pop("tagging", None)

    while element_to_delete:
        element = element_to_delete.pop()
        data.pop(element, None)

    result["data"] = data
    write_result_into_file(result, "../files/interior_or_exterior_data.json")
    return result


def calculate_most_popular_tag(tagging):
    # Does not consider if tags are equal (50/50)
    result = {}
    for tag in tagging:
        if tag["tag_name"] == MOST_POPULAR_CATEGORY:
            value_name = tag["value_name"]
            if value_name in result.keys():
                result[value_name] += 1
            else:
                result[value_name] = 1
    return max(result, key=result.get)

if __name__ == '__main__':
    # print(transform_formatted_data_to_one_hot_encoding())
    print(transform_data_leave_only_data_of_one_most_popular_category())
