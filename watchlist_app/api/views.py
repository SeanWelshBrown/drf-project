# LIBRARY IMPORTS
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from django.contrib.auth.models import User

# APP IMPORTS
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import WatchListSerializer, CreateWatchListSerializer, StreamPlatformSerializer, ReviewSerializer, UserSerializer


# STREAM PLATFORM VIEWS
class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(url_path='names', detail=False)
    def stream_platform_names(self, request):
        """
        List all Streaming Platform names as an array of strings
        """
        names = StreamPlatform.objects.all().values_list('name', flat=True)
        return Response(names)


# WATCHLIST VIEWS
class WatchListVS(viewsets.ModelViewSet):
    queryset = WatchList.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateWatchListSerializer
        elif self.action in ['reviews', 'create_review']:
            return ReviewSerializer
        else:
            return WatchListSerializer

    def get_permissions(self):
        if self.action == 'create_review':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAdminOrReadOnly]
        return super().get_permissions()

    @action(url_path='reviews', detail=True)
    def watchlist_reviews(self, request, pk=None):
        """
        List all reviews for a watchlist item
        """
        watchlist = self.get_object()
        serializer = ReviewSerializer(watchlist.reviews, many=True, context={'request': request})
        return Response(serializer.data)

    @action(url_path='create-review', detail=True, methods=['post'])
    def create_review(self, request, pk=None):
        """
        Create a review for a watchlist item
        """
        watchlist = self.get_object()
        user = self.request.user

        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=user)
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this item!")
            
        serializer = ReviewSerializer(data=request.data, context={'request': request})    
        if serializer.is_valid():
            if watchlist.avg_rating == 0:
                watchlist.avg_rating = serializer.validated_data['rating']
            else:
                watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating']) / 2
            watchlist.num_ratings = watchlist.num_ratings + 1

            watchlist.save()
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
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsReviewUserOrReadOnly]
        return super().get_permissions()


# USER VIEWS
class UserVS(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
