from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post


class LatestPostFeed(Feed):
    title = 'WScrew - последние новости'
    link = '/feeds/'
    description = 'Последние новости WScrew'

    def items(self):
        return Post.custom.order_by('-update')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.get_absolute_url()
