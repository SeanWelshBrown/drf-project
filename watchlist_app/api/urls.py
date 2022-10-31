# LIBRARY IMPORTS
from django.urls import path, include
from rest_framework import routers

# APP IMPORTS
from watchlist_app.api.views import StreamPlatform, WatchList, Review


router = routers.DefaultRouter()
router.register(r'streamplatform', StreamPlatform, basename='streamplatform')
router.register(r'watchlist', WatchList, basename='watchlist')
router.register(r'review', Review, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]
