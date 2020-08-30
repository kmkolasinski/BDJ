import operator
from functools import reduce
from typing import List

from dal import autocomplete
from django.db.models import Q
from django.forms import ModelMultipleChoiceField
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from bdj.models import FoodPlace, FoodPlaceGroup
from bdj.parsers.fb.parsers import parse_posts


class FoodPlaceAutocompleteView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        queryset = FoodPlace.objects.all()

        if self.q:
            words: List[str] = self.q.lower().split(" ")
            search_query = reduce(
                operator.and_, (Q(name__icontains=word) for word in words)
            )
            queryset = queryset.filter(search_query)
        return queryset


class FoodPlaceAutoCompleteField(ModelMultipleChoiceField):
    def __init__(
        self,
        placeholder: str = "Search ...",
        min_input_length: int = 1,
        required: bool = False,
    ):
        super().__init__(
            queryset=FoodPlace.objects.all(),
            widget=autocomplete.ModelSelect2Multiple(
                url="search-food-place",
                attrs={
                    "data-placeholder": placeholder,
                    "data-minimum-input-length": min_input_length,
                },
            ),
            required=required,
        )


class FoodPlaceListView(ListView):

    model = FoodPlace
    template_name = "bdj/food_place_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FoodPlaceCreateView(CreateView):
    model = FoodPlace
    template_name = "bdj/food_place_create.html"
    fields = "__all__"


class FoodPlaceGroupListView(ListView):

    model = FoodPlaceGroup
    template_name = "bdj/food_place_group_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FoodPlaceGroupCreateView(CreateView):
    model = FoodPlaceGroup
    template_name = "bdj/food_place_group_create.html"
    fields = "__all__"

    def get_form(self, form_class=None):
        form = super(FoodPlaceGroupCreateView, self).get_form(form_class)
        form.fields["food_places"] = FoodPlaceAutoCompleteField()
        return form


class FoodPlaceGroupUpdateView(UpdateView):
    model = FoodPlaceGroup
    template_name = "bdj/food_place_group_create.html"
    fields = "__all__"

    def get_form(self, form_class=None):
        form = super(FoodPlaceGroupUpdateView, self).get_form(form_class)
        form.fields["food_places"] = FoodPlaceAutoCompleteField()
        return form


def food_place_group_dashboard_view(request, group_id: int):
    group = FoodPlaceGroup.objects.get(pk=group_id)
    objects = group.food_places.all()
    return render(
        request,
        "bdj/food_place_group_dashboard.html",
        {"objects": objects, "group": group},
    )


def ajax_load_food_place(requests):

    data = requests.POST
    try:
        food_place_id = int(data["foodPlaceId"])
        food_place = FoodPlace.objects.get(pk=food_place_id)
        print(f"Getting post data for {food_place.name}")
        posts = parse_posts(food_place.fb_page_id, **food_place.config_json)
        html = render_to_string("bdj/fb/fb_posts.html", context={"posts": posts})
        data = {"html": html}
    except Exception as error:
        data = {"html": f"{error}"}

    return JsonResponse(data=data)
