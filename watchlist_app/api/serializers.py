# LIBRARY IMPORTS
from rest_framework import serializers

# APP IMPORTS
from watchlist_app.models import WatchList, StreamPlatform, Review



# REVIEWS
class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Review
        exclude = ['watchlist']


# WATCHLISTS
class WatchListSerializer(serializers.HyperlinkedModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = WatchList
        fields = "__all__"


# STREAM PLATFORMS
class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)
    
    class Meta:
        model = StreamPlatform
        fields = "__all__"
