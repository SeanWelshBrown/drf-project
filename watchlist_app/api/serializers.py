# LIBRARY IMPORTS
from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.auth.models import User

# APP IMPORTS
from watchlist_app.api.models import (
        WatchList, 
        StreamPlatform, 
        Review
        )


#-- REVIEWS --#
class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        exclude = ['watchlist']


#-- WATCHLISTS --#
class WatchListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='watchlist-detail')
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = WatchList
        fields = "__all__"
    
    # Serialize the 'platform' field as a URL
    def to_representation(self, instance):
        watchlist = super().to_representation(instance)
        request = self.context.get('request')
        watchlist['platform'] = reverse('streamplatform-detail', args=[watchlist['platform']], request=request)
        return watchlist


# class CreateWatchListSerializer(serializers.ModelSerializer):
#     """
#     Create WatchList with StreamPlatform ID instead of Hyperlinked URL
#     """
#     class Meta:
#         model = WatchList
#         fields = "__all__"


#-- STREAM PLATFORMS --#
class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)
    
    class Meta:
        model = StreamPlatform
        fields = "__all__"


#-- USERS --#
class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = User
        exclude = ['password']