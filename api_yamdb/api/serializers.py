from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    username = serializers.RegexField(
        max_length=150,
        regex=r'^[\w.@+-]',
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def validate_email(self, value):
        """Email field char length validator."""
        if len(value) > 254:
            raise serializers.ValidationError(
                'Email length longer then 254 chars'
            )
        return value

    class Meta:
        model = User
        fields = (
            'username', 'email', 'role', 'bio', 'first_name', 'last_name'
        )


class SignUpSerializer(serializers.ModelSerializer):
    """Serializer for User model. For registration."""

    class Meta:
        model = User
        fields = ('username', 'email')

    username = serializers.RegexField(
        required=True,
        max_length=150,
        regex=r'^[\w.@+-]',
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
    )

    def validate_username(self, username):
        """Username field validator."""
        if username == 'me':
            raise serializers.ValidationError(
                'Запрещено использовать имя "me".'
            )
        return username

    def validate(self, data):
        user = User.objects.filter(email=data["email"])
        if user:
            if user[0].username != data["username"]:
                raise serializers.ValidationError(
                    'User with this email has allready exists'
                )
        user = User.objects.filter(username=data["username"])
        if user:
            if user[0].email != data["email"]:
                raise serializers.ValidationError(
                    'User has allready exists with another email'
                )
        return data


class TokenSerializer(serializers.ModelSerializer):
    """Serializer for User model. When receiving a JWT token."""
    username = serializers.RegexField(
        required=True,
        max_length=150,
        regex=r'^[\w.@+-]',
    )

    def validate(self, data):
        user = get_object_or_404(User, username=data["username"])
        if data["confirmation_code"] != user.confirmation_code:
            raise serializers.ValidationError(
                'Bad confirmation code'
            )
        return data

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for authenticated user."""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model."""

    author = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)

    def create(self, validated_data):
        if not Review.objects.filter(
            author=self.context['request'].user,
            title=self.context['title_id']
        ).exists():
            return Review.objects.create(**validated_data)
        raise serializers.ValidationError(
            'На одно произведение можно оставить только один отзыв'
        )


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model."""

    author = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for Genre model."""

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleSerializer(serializers.ModelSerializer):
    """Serializer for Title model with method POST."""

    category = SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(),
        many=True
    )

    def validate_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                'Год создания произведения еще не наступил'
            )
        return value

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'category', 'genre')
        model = Title


class GetTitleSerializer(serializers.ModelSerializer):
    """Serializer for Title model with method GET."""

    rating = serializers.IntegerField(read_only=True)
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'category', 'genre',
                  'rating')
        model = Title
