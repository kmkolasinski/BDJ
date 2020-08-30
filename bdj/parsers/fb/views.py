import json

from django.shortcuts import render, get_object_or_404

from bdj.models import FoodPlace
from bdj.parsers.fb.forms import FacebookPostForm
from bdj.parsers.fb.parsers import parse_posts


def test_fb_post_parser_view(request):
    posts = []
    fb_page_id = None
    image = None
    errors = None
    config = {}

    if request.method == "POST":
        form = FacebookPostForm(request.POST)
        if form.is_valid():
            fb_page_id = form.cleaned_data["fb_page_id"]
            config = {
                "parser": form.get_parser_config(),
                "filter": form.get_filter_config(),
            }
            try:
                posts = parse_posts(
                    fb_page_id, form.get_parser_config(), form.get_filter_config()
                )
                image = posts[0].image if len(posts) > 0 else None

            except Exception as error:
                posts = []
                errors = error

    else:
        form = FacebookPostForm()

    return render(
        request,
        "bdj/fb/test_parser.html",
        {
            "form": form,
            "posts": posts,
            "image": image,
            "config": config,
            "errors": errors,
            "fb_page_id": fb_page_id,
        },
    )


def update_fb_post_parser_view(request, food_place_id: int):

    food_place = get_object_or_404(FoodPlace, pk=food_place_id)

    if request.method == "POST":
        form = FacebookPostForm(request.POST)
        if form.is_valid():
            config = {
                "parser_config": form.get_parser_config(),
                "filter_config": form.get_filter_config(),
            }
            food_place.config = json.dumps(config)
            food_place.save()

    else:
        form = FacebookPostForm.from_food_place(food_place)

    image = food_place.image.url

    return render(
        request,
        "bdj/fb/test_parser.html",
        {
            "form": form,
            "posts": [],
            "image": image,
            "config": None,
            "errors": None,
            "fb_page_id": food_place.fb_page_id,
        },
    )