import json

from django.http import HttpResponse
from rest_framework.decorators import api_view

import requests

HATCHWAYS_IO_ASSESSMENT = "https://hatchways.io/api/assessment/blog/posts"
VALID_SORT_FIELDS = ['id', 'reads', 'likes', 'popularity']
VALID_DIRECTIONS = ['desc', 'asc']


@api_view(['GET'])
def get_ping(request):
    response_body = {"success": "true"}
    response = HttpResponse(json.dumps(response_body), content_type="application/json", status=200)
    return response


@api_view(['GET'])
def get_posts(request):
    tags = request.GET.get('tags')
    if not tags:
        return request_field_error({"error": "Tags parameter is required"})

    sort_by = request.GET.get('sortBy', 'id')
    if sort_by not in VALID_SORT_FIELDS:
        return request_field_error({"error": "sortBy parameter is invalid"})

    direction = request.GET.get('direction', 'asc')
    if direction not in VALID_DIRECTIONS:
        return request_field_error({"error": "direction parameter is invalid"})

    all_combined_posts = get_all_combined_posts(tags)

    sorted_combined_posts = sort_posts(all_combined_posts, sort_by, direction)

    response_body = {"posts": list(sorted_combined_posts.values())}
    response = HttpResponse(json.dumps(response_body),
                            content_type="application/json", status=200)
    return response


def sort_posts(all_combined_posts, sort_by, direction):
    reverse = False
    if direction == 'desc':
        reverse = True
    return {k: v for k, v in sorted(all_combined_posts.items(), key=lambda item: item[1][sort_by], reverse=reverse)}


def get_all_combined_posts(tags):
    tag_list = tags.split(',')
    all_combined_posts = {}
    for tag in tag_list:
        posts_list = call_hatchways_api(tag)
        for post in posts_list:
            all_combined_posts[post.get('id')] = post
    return all_combined_posts


def call_hatchways_api(tag):
    params = {'tag': tag}
    r = requests.get(url=HATCHWAYS_IO_ASSESSMENT, params=params)
    data = r.json()
    return data.get('posts', [])


# Invalid request responses
def request_field_error(message):
    response = HttpResponse(json.dumps(message), content_type="application/json", status=400)
    return response
