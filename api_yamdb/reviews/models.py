from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.utils import current_year_validator  # isort:skip
from users.models import User  # isort:skip


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        blank=False,
        db_index=True,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        unique=True,
        blank=False,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        db_index=True,
        verbose_name='Название жанра')
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        db_index=True,
        verbose_name='Название произведения'
    )
    year = models.IntegerField(
        validators=[current_year_validator],
        verbose_name='Год создания'
    )
    description = models.TextField(verbose_name='Аннотация')
    genre = models.ManyToManyField(Genre, blank=False)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews')
    text = models.TextField(verbose_name='Отзыв')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор')
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True,
                                    verbose_name='Дата публикации')
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1, 'оценка по шкале от 1'),
                    MaxValueValidator(10, 'оценка по шкале до 10')],
        verbose_name='Оценка')

    class Meta:
        ordering = ('-pub_date', 'score')
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='unique review')
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments', verbose_name='Отзыв')
    text = models.TextField(verbose_name='Комментарий')
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True,
                                    verbose_name='Дата публикации')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
