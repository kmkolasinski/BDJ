from django import forms

from bdj.models import FoodPlace


class FacebookPostForm(forms.Form):
    food_place_id = forms.IntegerField(
        label="Id of the model in table (don't change)",
        initial=0,
        required=False,
    )
    fb_page_id = forms.CharField(
        label="Facebook restaurant page ID", max_length=500, initial="zebraresto"
    )
    keywords = forms.CharField(
        label="Keywords, comma separated",
        max_length=1000,
        widget=forms.Textarea,
        initial=",",
    )
    max_posts = forms.IntegerField(
        label="Max num posts to display", max_value=10, initial=1, min_value=1
    )
    num_pages = forms.IntegerField(label="Num pages", max_value=5, initial=1)
    max_days_ago = forms.IntegerField(
        label="Max days in past (set -1 to disable)",
        min_value=-1,
        initial=-1,
        max_value=10,
    )
    menu_as_image = forms.BooleanField(
        label="Menu as Image", initial=False, required=False
    )
    sort_by_score = forms.BooleanField(
        label="Sort by score", initial=False, required=False
    )

    @classmethod
    def from_food_place(cls, food_place: FoodPlace) -> "FacebookPostForm":

        config = food_place.config_json
        if 'filter_config' in config:
            del config['filter_config']['type']
            config['filter_config']['keywords'] = ",".join(config['filter_config']['keywords'])
        else:
            config['filter_config'] = {}

        if 'parser_config' in config:
            del config['parser_config']['type']
        else:
            config['parser_config'] = {}

        initial = {
            "food_place_id": food_place.id,
            "fb_page_id": food_place.fb_page_id,
            **config['filter_config'], **config['parser_config']
        }

        return FacebookPostForm(initial=initial)

    def get_filter_config(self):
        words = self.cleaned_data["keywords"].lower().split(",")
        return {
            "type": "KeywordsFilter",
            "keywords": list([w.strip() for w in words]),
            "max_posts": self.cleaned_data["max_posts"],
            "sort_by_score": self.cleaned_data["sort_by_score"],
        }

    def get_parser_config(self):
        return {
            "type": "FacebookPostParser",
            "num_pages": self.cleaned_data["num_pages"],
            "max_days_ago": self.cleaned_data["max_days_ago"],
            "menu_as_image": self.cleaned_data["menu_as_image"],
        }
