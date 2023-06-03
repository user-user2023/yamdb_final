from api.permissions import (IsAdminOrModeratirOrAuthor, IsAdminOrReadOnly,
                             IsAdminOrSuperuser)
from api.serializers import (AuthorSerializer, CategorySerializer,
                             CommentSerializer, GenreSerializer,
                             GetTitleSerializer, ReviewSerializer,
                             SignUpSerializer, TitleSerializer,
                             TokenSerializer, UserSerializer)
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title
from users.models import User


class UserSignUpViewSet(viewsets.ModelViewSet):
    """ViewClass for user registration."""

    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        user, created = User.objects.get_or_create(
            username=username,
            email=email,
        )
        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        user.save()
        send_mail(
            subject='Код подтверждения',
            message=f'{username}, код подтверждения: {confirmation_code}',
            from_email='confirmation_code@example.com',
            recipient_list=[email],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenViewSet(viewsets.ModelViewSet):
    """ViewClass for receiving a JWT token by the user."""

    queryset = User.objects.all()
    serializer_class = TokenSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)
        refresh = RefreshToken.for_user(user)
        return Response(
            {'access': str(refresh.access_token)},
            status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ModelViewSet):
    """ViewClass for User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrSuperuser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        permission_classes=[IsAuthenticated],
        methods=['get', 'patch']
    )
    def me(self, request):
        if request.method == 'GET':
            user = get_object_or_404(User, id=request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        if request.method == 'PATCH':
            user = get_object_or_404(User, id=request.user.id)
            if request.user.is_admin:
                serializer = UserSerializer(
                    user, data=request.data, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
            serializer = AuthorSerializer(
                user, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class ReviewViewSet(viewsets.ModelViewSet):
    """Viewset for Review model."""

    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsAdminOrModeratirOrAuthor,
    )

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def get_serializer_context(self):
        return {
            'title_id': self.kwargs['title_id'],
            'request': self.request
        }


class CommentViewSet(viewsets.ModelViewSet):
    """Viewset for Comment model."""

    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsAdminOrModeratirOrAuthor,
    )

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class TitleViewSet(viewsets.ModelViewSet):
    """ViewClass for Title."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("name", "year")

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return GetTitleSerializer
        return TitleSerializer

    def get_queryset(self):
        self.serializer_class = GetTitleSerializer
        queryset = Title.objects.order_by("id").annotate(
            rating=Avg("reviews__score")
        )
        category = self.request.query_params.get('category')
        genre = self.request.query_params.get('genre')
        for key, value in self.request.query_params.items():
            if key == "category":
                queryset = queryset.filter(category__slug=category)
            elif key == "genre":
                queryset = queryset.filter(genre__slug=genre)
        return queryset


class CreateDestroyListViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """A viewset that provides `create()`,`destroy()`, `list()` actions."""
    pass


class CategoryViewSet(CreateDestroyListViewSet):
    """ViewClass for Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateDestroyListViewSet):
    """ViewClass for Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
