from api.validator import validate
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Наименование категории'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='slug_Категория'
    )

    class Meta:
        verbose_name = 'Категория',
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Наименование жанра'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='slug_Жанр'
    )

    class Meta:
        verbose_name = 'Жанр',
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField('Название произведения',
                            max_length=150, db_index=True, blank=False)
    year = models.IntegerField(
        'Год произведения',
        blank=True,
        validators=[validate]
    )
    description = models.CharField(
        'Описание',
        blank=True,
        max_length=250,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория',
        blank=True
    )

    class Meta:
        verbose_name = 'Произведение',
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return f'{self.name} {self.year}'


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['genre', 'title'],
                name='unique title-genre couple'),
        ]

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews',
                              verbose_name='Произведение'
                              )
    text = models.TextField("Текст отзыва")
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='reviews',
                               verbose_name='Автор отзыва'
                               )
    score = models.IntegerField(
        validators=[
            MinValueValidator(
                1,
                message='Оценка не может быть ниже 1'
            ),
            MaxValueValidator(
                10,
                message='Оценка не может быть выше 10'
            )
        ],
        verbose_name='Оценка произведения'
    )
    pub_date = models.DateTimeField("Дата публикации отзыва",
                                    auto_now_add=True,
                                    db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review')
        ]
        ordering = ['pub_date']

    def __str__(self):
        return f'{self.title} оценка {self.score}'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField("Текст комментария")
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Автор комментария'
                               )
    pub_date = models.DateTimeField("Дата публикации комментария",
                                    auto_now_add=True,
                                    db_index=True)

    class Meta:
        verbose_name = 'Комментарий',
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date']

    def __str__(self):
        return self.text[:15]
