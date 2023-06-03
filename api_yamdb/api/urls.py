from django.urls import include, path
from rest_framework import routers

from api.views import (
    CategoryViewSet, CommentViewSet, GenreViewSet,
    ReviewViewSet, TitleViewSet, TokenViewSet,
    UserSignUpViewSet, UserViewSet
)

router = routers.DefaultRouter()
router.register(r'titles', TitleViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'users', UserViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/auth/signup/', UserSignUpViewSet.as_view({'post': 'create'})),
    path('v1/auth/token/', TokenViewSet.as_view({'post': 'create'})),
    path('v1/', include(router.urls)),
]
