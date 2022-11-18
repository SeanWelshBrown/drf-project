# LIBRARY IMPORTS
from django.urls import path, include
from rest_framework import routers

# APP IMPORTS
from watchlist_app.api.views import (
        StreamPlatformVS, 
        WatchListVS, 
        ReviewVS, 
        UserVS
        )


router = routers.DefaultRouter()
router.register(r'streamplatform', StreamPlatformVS, basename='streamplatform')
router.register(r'watchlist', WatchListVS, basename='watchlist')
router.register(r'review', ReviewVS, basename='review')
router.register(r'user', UserVS, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
