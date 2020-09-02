import string
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from functools import cached_property
from typing import List, Set, Dict, Any, Optional
from dacite import from_dict
from facebook_scraper import get_posts
import unidecode
import re
import dataclasses as dc


@dataclass(frozen=True)
class FacebookPost:
    post_id: str
    time: datetime
    text: str
    post_text: str
    post_url: Optional[str] = None
    image: Optional[str] = None
    score: Optional[int] = None

    @classmethod
    def image_url(cls, url: str) -> str:
        return f" <span class='zoom zoomable-image'> <img src='{url}' style='width:100%' alt='' /> </span> "

    @cached_property
    def dtime(self) -> timedelta:
        return datetime.now() - self.time


@dataclass(frozen=True)
class KeywordsFilter:
    keywords: List[str] = field(default_factory=list)
    max_posts: int = 1
    sort_by_score: bool = False

    @property
    def clean_keywords(self) -> Set[str]:
        return {unidecode.unidecode(w).lower() for w in self.keywords}

    def match_score(self, text: str) -> int:
        text = unidecode.unidecode(text).lower()
        text = text.translate(string.punctuation).replace(":", " ").replace("!", " ")
        text = re.sub(r"\W+", " ", text)
        words = [w.strip() for w in text.split(" ")]
        return len(set(words) & self.clean_keywords)

    def filter_posts(self, posts: List[FacebookPost]) -> List[FacebookPost]:

        posts_with_scores = []
        for p in posts:
            p = dc.replace(p, score=self.match_score(p.text))
            posts_with_scores.append(p)

        best_posts = list(
            sorted(posts_with_scores, key=lambda p: p.score, reverse=True)
        )
        best_posts = best_posts[: self.max_posts]
        if self.sort_by_score:
            best_posts = sorted(best_posts, key=lambda p: p.score, reverse=True)
        else:
            best_posts = sorted(best_posts, key=lambda p: p.dtime.total_seconds())

        for p in best_posts:
            print(p.score, p.dtime, p.text[:10])

        return best_posts


@dataclass(frozen=True)
class FacebookPostParser:
    num_pages: int = 1
    menu_as_image: bool = False
    image_at_top: bool = True
    max_days_ago: int = -1

    def get_content(self, fb_page_id: str) -> List[FacebookPost]:
        posts = list(get_posts(fb_page_id, pages=self.num_pages))
        if self.menu_as_image:
            for p in posts:
                image_url = FacebookPost.image_url(p["image"])
                if self.image_at_top:
                    p["text"] = image_url + p["text"]
                else:
                    p["text"] = p["text"] + image_url

        posts = [from_dict(FacebookPost, p) for p in posts]
        if self.max_days_ago >= 0:
            posts = [p for p in posts if p.dtime.days <= self.max_days_ago]

        return posts


def parse_posts(
    fb_page_id: str, parser_config: Dict[str, Any], filter_config: Dict[str, Any]
) -> List[FacebookPost]:

    parsing_method = from_dict(FacebookPostParser, parser_config)
    filter_method = from_dict(KeywordsFilter, filter_config)

    posts = parsing_method.get_content(fb_page_id)
    posts = filter_method.filter_posts(posts)
    return posts
