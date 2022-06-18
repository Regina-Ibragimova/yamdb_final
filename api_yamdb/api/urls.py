from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import SignUpUser, TokenRegistrate, UsersViewSet

router = DefaultRouter()
router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register('users', UsersViewSet, basename='users')

authpatterns = [
    path('signup/',
         SignUpUser.as_view(),
         name='get_registration_email'
         ),
    path('token/',
         TokenRegistrate.as_view(),
         name='get_token'
         )
]
urlpatterns = [
    path('v1/',
         include(router.urls),
         name='api_v1'
         ),
    path('v1/auth/',
         include(authpatterns),
         name='api_v1_auth'
         ),
]
