# LIBRARY IMPORTS
from django.urls import path, include
from rest_framework import routers

# APP IMPORTS
# from watchlist_app.api.views import (WatchListAV, WatchListDetailAV, StreamPlatformAV,
#                                      StreamPlatformMVS, StreamPlatformDetailAV, StreamPlatformNames,
#                                      ReviewList, ReviewDetail, ReviewCreate)


router = routers.DefaultRouter()
router.register(r'streamplatform', StreamPlatformMVS, basename='streamplatform')

urlpatterns = [
    path('', include(router.urls)),
    
    path('watchlist/', WatchListAV.as_view(), name='watchlist'),
    path('watchlist/<int:pk>', WatchListDetailAV.as_view(), name='watchlist-detail'),
    
    path('watchlist/<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('watchlist/<int:pk>/review/', ReviewList.as_view(), name='review-list'),
    path('watchlist/review/<int:pk>', ReviewDetail.as_view(), name='review-detail')
    
    # path('streamplatform/', StreamPlatformAV.as_view(), name='streamplatform'),
    # path('streamplatform/<int:pk>', StreamPlatformDetailAV.as_view(), name='streamplatform-detail'),
    # path('streamplatform/names', StreamPlatformNames.as_view(), name='streamplatform-urls'),

]
