from django.contrib.syndication.feeds import Feed
from aggregator.models import FeedItem

class CommunityAggregatorFeed(Feed):
    title = "The News21 Community"
    link = "http://www.news21.com/community/"
    description = "Aggregated feeds from the News21 community."

    def items(self):
        return FeedItem.objects.all()[:10]
