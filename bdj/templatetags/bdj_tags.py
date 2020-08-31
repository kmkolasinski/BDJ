from datetime import datetime

from django import template
from django.core.handlers.wsgi import WSGIRequest
from django.template import RequestContext
from django.template.loader import render_to_string

from bdj.models import FoodPlace


register = template.Library()


@register.simple_tag(takes_context=True)
def render_food_place(context: RequestContext, food_place: FoodPlace):
    request: WSGIRequest = context.request

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
        "image": food_place.image_url,
        "query": request.GET
    }
    return render_to_string("bdj/fb/fb_card.html", context=context)
