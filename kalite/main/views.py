from django.http import HttpResponse, HttpResponseNotFound
from annoying.decorators import render_to
from kalite import settings
import json

slug_key = {
    "Topic": "id",
    "Video": "readable_id",
    "Exercise": "name",
}

title_key = {
    "Topic": "title",
    "Video": "title",
    "Exercise": "display_name",
}

def splat_handler(request, splat):
    slugs = filter(lambda x: x, splat.split("/"))
    current_node = settings.TOPICS
    seeking = "Topic"
    for slug in slugs:
        if slug == "v":
            seeking = "Video"
        elif slug == "e":
            seeking = "Exercise"
        else:
            children = [child for child in current_node['children'] if child['kind'] == seeking]
            if not children:
                return HttpResponseNotFound("No children of type '%s' found for node '%s'!" %
                    (seeking, current_node[title_key[current_node['kind']]]))
            match = None
            prev = None
            next = None
            for child in children:
                if match:
                    next = child
                    break
                if child[slug_key[seeking]] == slug:
                    match = child
                else:
                    prev = child
            if not match:
                return HttpResponseNotFound("Child with slug '%s' of type '%s' not found in node '%s'!" %
                    (slug, seeking, current_node[title_key[current_node['kind']]]))
            current_node = match
    if current_node["kind"] == "Topic":
        return topic_handler(request, current_node)
    if current_node["kind"] == "Video":
        return video_handler(request, video=current_node, prev=prev, next=next)
    if current_node["kind"] == "Exercise":
        return exercise_handler(request, current_node)
    return HttpResponseNotFound("No valid item found at this address!")

@render_to("topic.html")
def topic_handler(request, topic):
    videos = filter(lambda node: node["kind"] == "Video", topic["children"])
    exercises = filter(lambda node: node["kind"] == "Exercise" and node["live"], topic["children"])
    topics = filter(lambda node: node["kind"] == "Topic" and not node["hide"], topic["children"])
    context = {
        "topic": topic,
        "title": topic[title_key["Topic"]],
        "videos": videos,
        "exercises": exercises,
        "topics": topics,
    }
    return context
    
@render_to("video.html")
def video_handler(request, video, prev=None, next=None):
    context = {
        "video": video,
        "title": video[title_key["Video"]],
        "prev": prev,
        "next": next,
    }
    return context