import django_filters
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import TitleFilter  # isort:skip
from api.permissions import (AdminOnly, AdminOrReadOnly,  # isort:skip
                             IsAuthorOrAdministratorOrReadOnly)
from api.serializers import (CategorySerializer,  # isort:skip
                             CommentSerializer, GenreSerializer,
                             ReviewSerializer, TitleCreateSerializer,
                             TitleSerializer, UserSerializer)
from reviews.models import (Category, Genre, Review, Title)  # isort:skip
from users.models import User  # isort:skip


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    lookup_value_regex = r'[\w.@+-]+'

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated],
            url_path='me')
    def own_user_account(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(request.user,
                                        data=request.data,
                                        partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrAdministratorOrReadOnly,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'),
                                   title__id=self.kwargs.get('title_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review,
                                   id=self.kwargs['review_id'],
                                   title=self.kwargs['title_id'],)
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrAdministratorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CreateDestroyListViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'slug'


class CategoryViewSet(CreateDestroyListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateDestroyListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('name')
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_class = TitleFilter
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleCreateSerializer
        return TitleSerializer
