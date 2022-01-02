import json

SOURCE_FILE = "../files/formatted_data.json"


def print_categories_rating():
    result = {}
    f = open(SOURCE_FILE)
    data = json.load(f)
    for element in data:
        most_popular_category = data[element]["most_popular_tag"]
        if most_popular_category in result:
            result[most_popular_category] += 1
        else:
            result[most_popular_category] = 1

    for key, value in result.items():
        print("{:30}{}".format(key, value))

if __name__ == '__main__':
    print_categories_rating()
