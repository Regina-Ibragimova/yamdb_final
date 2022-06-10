from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import (Category, Comment, Genre, Review,  # isort:skip
                            Title)
from users.models import User  # isort:skip


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def update(self, user, validated_data):
        if not (user.is_admin or user.is_superuser):
            validated_data.pop('role', {})
        super().update(user, validated_data)
        return user


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'score', 'pub_date')

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        user = self.context['request'].user
        title_id = self.context['view'].kwargs['title_id']
        if Review.objects.filter(author=user, title__id=title_id).exists():
            raise serializers.ValidationError(
                'Возможен только 1 отзыв'
            )
        return data


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id', )
        lookup_field = 'slug'
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id', )
        lookup_field = 'slug'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True,)
    rating = serializers.FloatField()

    class Meta:
        fields = ('id',
                  'name',
                  'year',
                  'rating',
                  'description',
                  'genre',
                  'category')
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
        fields = ('id',
                  'name',
                  'year',
                  'description',
                  'genre',
                  'category')
        model = Title

    def validate_year(self, value):
        if value > timezone.now().year:
            raise ValidationError(
                '%(value)s is not a correcrt year!',
                params={'value': value},)
        return value
