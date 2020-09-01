import json
from typing import Any, Dict

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

from BDJ import settings


class BDJUser(AbstractUser):
    pass


class FoodPlace(models.Model):

    created_at = models.DateField(auto_created=True, auto_now=True)
    name = models.CharField(max_length=512)
    fb_page_id = models.CharField(max_length=512, help_text="Facebook web page id")
    image = models.ImageField(upload_to="uploads/", null=True, blank=True)
    updated_at = models.DateField(auto_now_add=True)
    config = models.TextField(
        max_length=5000, help_text="String with JSON config of the parser", default="{}"
    )

    @property
    def config_json(self) -> Dict[str, Any]:
        return json.loads(self.config)

    def get_absolute_url(self):
        return reverse("fb-update-parser", kwargs={"food_place_id": self.id})

    @property
    def fb_info_page_url(self) -> str:
        return f"https://www.facebook.com/{self.fb_page_id}/about/?ref=page_internal"

    @property
    def image_url(self) -> str:
        if self.image.name != "":
            return self.image.url
        else:
            return "/static/bdj/favicon.png"

    def __str__(self):
        return f"({self.pk}) {self.name}"


class FoodPlaceGroup(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    name = models.CharField(max_length=512)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    food_places = models.ManyToManyField(FoodPlace)

    def __str__(self):
        return f"({self.pk}) {self.name}"

    def get_absolute_url(self):
        return reverse("food-place-group-dashboard", kwargs={"group_id": self.id})
