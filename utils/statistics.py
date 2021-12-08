from utils.format_file import read_file


def perform_statistics(data):
    tags = {}
    tag_value = {}
    for el in data:
        tagging = data[el]["tagging"]
        for tag in tagging:
            if tag["tag_name"] in tags:
                tags[tag["tag_name"]] += 1
            else:
                tags[tag["tag_name"]] = 1

            if tag["value_name"] != "not applicable":
                if tag["value_name"] in tag_value:
                    tag_value[tag["value_name"]] += 1
                else:
                    tag_value[tag["value_name"]] = 1

    print("STATISTICS")
    print("==========")
    print()
    analyse_tags(tags)
    print()
    analyse_tag_value(tag_value)


def analyse_tags(tags):
    total_tags_count = sum(list(tags.values()))
    result = {}
    for el in tags.keys():
        result[el] = round((tags[el] / total_tags_count) * 100, 2)
    print("TAGS TOTAL COUNT")
    print(tags)
    print()
    print("TAGS IN %")
    print(result)


def analyse_tag_value(tag_value):
    total_tags_count = sum(list(tag_value.values()))
    result = {}
    for el in tag_value.keys():
        result[el] = round((tag_value[el] / total_tags_count) * 100, 2)
    print("TAGS VALUE TOTAL COUNT")
    print(tag_value)
    print()
    print("TAGS VALUE IN %")
    print(result)


if __name__ == '__main__':
    result = read_file()
    perform_statistics(result)
