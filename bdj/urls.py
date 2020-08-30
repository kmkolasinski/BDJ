from django.urls import path

from bdj.parsers.fb.views import test_fb_post_parser_view, update_fb_post_parser_view
from bdj.views import *

urlpatterns = [
  path("groups/", FoodPlaceGroupListView.as_view(), name="food-place-group-list"),
  path("groups/<int:group_id>/", food_place_group_dashboard_view, name="food-place-group-dashboard"),
  path('', FoodPlaceListView.as_view(), name='food-place-list'),
  # Food Place
  path('create/', FoodPlaceCreateView.as_view(), name='food-place-create'),
  path('create-group/', FoodPlaceGroupCreateView.as_view(), name='food-place-group-create'),
  path('update-group/<int:pk>/', FoodPlaceGroupUpdateView.as_view(), name='food-place-group-update'),
  path("fb/test-parser/", test_fb_post_parser_view, name="fb-test-parser"),
  path("fb/update-parser/<int:food_place_id>/", update_fb_post_parser_view, name="fb-update-parser"),
  # AJAX or API
  path("api/load-food-place/", ajax_load_food_place, name="load-food-place"),
  path("api/search-food-place/", FoodPlaceAutocompleteView.as_view(), name="search-food-place"),
]
