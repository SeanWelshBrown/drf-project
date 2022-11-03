# LIBRARY IMPORTS
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User

# APP IMPORTS
from watchlist_app.api.permissions import AdminOrReadOnly, ReviewUserOrReadOnly
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer, UserSerializer


# STREAM PLATFORM VIEWS
class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    
    @action(url_path='names', detail=False)
    def stream_platform_names(self, request):
        names = StreamPlatform.objects.all().values_list('name', flat=True)
        return Response(names)


# WATCHLIST VIEWS
class WatchListVS(viewsets.ModelViewSet):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    

    @action(url_path='reviews', 
            detail=True,)
    def watchlist_reviews(self, request, pk=None):
        watchlist = self.get_object()
        serializer = ReviewSerializer(watchlist.reviews, many=True, context={'request': request})
        return Response(serializer.data)

    @action(url_path='create-review', 
            detail=True, 
            methods=['post'], 
            serializer_class=ReviewSerializer,
            permission_classes=[IsAuthenticated])
    def create_review(self, request, pk=None):
        watchlist = self.get_object()
        user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=user)
        
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this item!")
        
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(watchlist=watchlist, review_user=user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


# REVIEW VIEWS
class ReviewVS(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'put', 'patch', 'delete', 'options', 'head']
      
    def get_permissions(self):
        if self.action == 'retrieve':
            self.permission_classes = [ReviewUserOrReadOnly | AdminOrReadOnly]
        return [permission() for permission in self.permission_classes]


# USER VIEWS
class UserVS(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer