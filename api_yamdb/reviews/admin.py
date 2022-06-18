from django.contrib import admin
from users.models import User

from .models import Category, Comment, Genre, Review, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'category',
        'description',
    )
    list_editable = ('category',)
    search_fields = (
        'name',
        'year',
    )
    list_filter = ('name',)
    empty_value_display = '>empty<'


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '>empty<'


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '>empty<'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'review',
        'text',
        'author',
        'pub_date',
    )
    search_fields = (
        'review',
        'author',
    )
    list_filter = ('pub_date',)
    empty_value_display = '>empty<'


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'author',
        'score',
        'pub_date',
    )
    list_editable = ('score',)
    search_fields = (
        'title',
        'author',
    )
    list_filter = ('pub_date',)
    empty_value_display = '>empty<'


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'role',
        'email',
        'date_joined',
    )
    list_editable = ('role',)
    search_fields = ('username',)
    list_filter = ('date_joined',)
    empty_value_display = '>empty<'


admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(User, UserAdmin)
