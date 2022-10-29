# LIBRARY IMPORTS
from django.urls import path, include
from rest_framework import routers

# APP IMPORTS
from watchlist_app.api.views import (WatchListAV, WatchListDetailAV, StreamPlatformAV,
                                     StreamPlatformVS, StreamPlatformDetailAV, StreamPlatformNames,
                                     ReviewList, ReviewDetail, ReviewCreate)


router = routers.DefaultRouter()
router.register(r'stream', StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    path('watchlist/', WatchListAV.as_view(), name='watchlist'),
    path('watchlist/<int:pk>', WatchListDetailAV.as_view(), name='watchlist-detail'),
    
    path('', include(router.urls)),
    # path('streamplatform/', StreamPlatformAV.as_view(), name='streamplatform'),
    # path('streamplatform/<int:pk>', StreamPlatformDetailAV.as_view(), name='streamplatform-detail'),
    path('streamplatform/names', StreamPlatformNames.as_view(), name='streamplatform-urls'),
    
    path('watchlist/<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('watchlist/<int:pk>/review/', ReviewList.as_view(), name='review-list'),
    path('watchlist/review/<int:pk>', ReviewDetail.as_view(), name='review-detail')
]
