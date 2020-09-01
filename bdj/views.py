import operator
from functools import reduce
from typing import List

from dal import autocomplete
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
from django.forms import ModelMultipleChoiceField
from django.http import JsonResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.functional import SimpleLazyObject
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from bdj.models import FoodPlace, FoodPlaceGroup, BDJUser
from bdj.parsers.fb.parsers import parse_posts


class DefaultLoginRequiredMixin(LoginRequiredMixin):
    login_url = "/accounts/login/"
    redirect_field_name = "redirect_to"

    def get_user(self) -> BDJUser:
        return self.request.user


class IsAdminTestMixin(UserPassesTestMixin):
    def test_func(self):
        user: User = self.request.user
        return user.username == "admin"


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


class FoodPlaceListView(DefaultLoginRequiredMixin, IsAdminTestMixin, ListView):

    model = FoodPlace
    template_name = "bdj/food_place_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FoodPlaceCreateView(DefaultLoginRequiredMixin, IsAdminTestMixin, CreateView):

    model = FoodPlace
    template_name = "bdj/food_place_create.html"
    fields = "__all__"


class FoodPlaceGroupListView(DefaultLoginRequiredMixin, ListView):

    model = FoodPlaceGroup
    template_name = "bdj/food_place_group_list.html"

    def get_queryset(self):
        user = self.get_user()
        if user.is_superuser:
            objects = FoodPlaceGroup.objects.all()
        else:
            objects = FoodPlaceGroup.objects.filter(creator=user)

        return objects


class FoodPlaceGroupViewMixinDefault(DefaultLoginRequiredMixin):
    model = FoodPlaceGroup
    template_name = "bdj/food_place_group_create.html"
    fields = ("name", "food_places")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.creator = self.request.user
        obj.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super(FoodPlaceGroupViewMixinDefault, self).get_form(form_class)
        form.fields["food_places"] = FoodPlaceAutoCompleteField()
        return form


class FoodPlaceGroupCreateView(FoodPlaceGroupViewMixinDefault, CreateView):
    pass


class FoodPlaceGroupUpdateView(FoodPlaceGroupViewMixinDefault, UpdateView):
    pass


@login_required(login_url="/accounts/login/")
def food_place_group_dashboard_view(request: HttpRequest, group_id: int):

    if request.user.is_superuser:
        group = FoodPlaceGroup.objects.get(pk=group_id)
    else:
        group = get_object_or_404(FoodPlaceGroup, pk=group_id, creator=request.user)

    objects = group.food_places.all()
    return render(
        request,
        "bdj/food_place_group_dashboard.html",
        {"objects": objects, "group": group, "query": request.GET},
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
