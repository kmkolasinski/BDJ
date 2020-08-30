from datetime import datetime

from django import template
from django.template.loader import render_to_string

from bdj.models import FoodPlace


register = template.Library()


@register.simple_tag
def render_food_place(food_place: FoodPlace):
    context = {
        "name": food_place.name,
        "fb_info_page_url": food_place.fb_info_page_url,
        "fb_page_id": food_place.fb_page_id,
        "posts": [
            {
                "time": datetime.now(),
                "post_url": None,
                "text": "Loading ... ",
            }
        ],
        "load_posts_with_ajax": True,
        "food_place_id": food_place.id,
        "image": food_place.image.url
    }
    return render_to_string("bdj/fb/fb_card.html", context=context)
