# LIBRARY IMPORTS
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets

# APP IMPORTS
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer



# STREAM PLATFORM VIEWS
class StreamPlatform(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    
    @action(url_path='names', detail=False)
    def stream_platform_names(self, request):
        names = StreamPlatform.objects.all().values_list('name', flat=True)
        return Response(names)


# WATCH LIST VIEWS
class WatchList(viewsets.ModelViewSet):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    
    def get_serializer_class(self):
        if self.action == "watchlist_reviews" or self.action == "create_review":
            return ReviewSerializer
        else:
            return self.serializer_class
        
    
    @action(url_path='reviews', detail=True)
    def watchlist_reviews(self, request, pk=None):
        watchlist = self.get_object()
        serializer = self.get_serializer(watchlist.reviews, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(url_path='create-review', methods=["POST"], detail=True)
    def create_review(self, request, pk=None):
        watchlist = self.get_object()
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(watchlist=watchlist)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    
# REVIEW VIEWS
class Review(viewsets.ReadOnlyModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    