from django.core.context_processors import request
import queries
import random
import memcache
import json


def get_randomized_tags():
    mc = memcache.Client(['127.0.0.1:8079'], debug=0)
    data = mc.get("tags")

    if data:
        return json.loads(data)
    else:
        popular_tags = queries.get_popular_tags()[0:25]

        if popular_tags.count() == 0:
            return []

        max_count = popular_tags[0].quest_count
        min_count = popular_tags[len(popular_tags)-1].quest_count
        count_dif = max_count - min_count

        #prevent division by zero
        if count_dif == 0:
            count_dif = 1

        weight_count = 5

        #popular_tags_list = list(popular_tags)
        #random.shuffle(popular_tags_list)

        tags_dict = {}
        for tag in popular_tags:
            weight = tag.quest_count % count_dif * weight_count / count_dif + 1
            tags_dict[tag.name] = weight

        data = json.dumps(tags_dict)
        mc.set("tags", data, 60*5)

        return tags_dict


def tags(request):
    popular_tags_list = get_randomized_tags()

    return {
        'popular_tags': popular_tags_list,
    }

def last_registered(request):
    mc = memcache.Client(['127.0.0.1:8079'], debug=0)
    data = mc.get("last_registered_users")

    if data:
        last_registered_list = json.loads(data)
    else:
        users = queries.get_last_registered_users()
        last_registered_list = [obj.username for obj in users]

        data = json.dumps(last_registered_list)
        mc.set("last_registered_users", data, 60*5)

    return {
            'last_registered_left': last_registered_list[0:len(last_registered_list)/2],
            'last_registered_right': last_registered_list[len(last_registered_list)/2: len(last_registered_list)],
    }
