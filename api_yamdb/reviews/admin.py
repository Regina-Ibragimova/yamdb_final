from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_date',)
    list_editable = ('author',)
    search_fields = ('title', 'author', 'pub_date')
    list_filter = ('pub_date', 'author')
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'year')
    search_fields = ('name', 'year', 'genre', 'category')
    list_filter = ('name', 'year', 'genre', 'category')
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'author', 'pub_date',)
    list_editable = ('author',)
    search_fields = ('review', 'author', 'pub_date',)
    list_filter = ('pub_date', 'author')
    empty_value_display = '-пусто-'


admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Comment, CommentAdmin)
