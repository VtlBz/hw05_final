from django.contrib import admin

from .models import Comment, Follow, Group, Post

DEFAULT_FOR_EMPTY: str = '-пусто-'


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'group',)
    list_editable = ('group',)
    search_fields = ('text', 'author',)
    list_filter = ('pub_date',)
    empty_value_display = DEFAULT_FOR_EMPTY


# Знаю, что в одном проекте - один стиль,
# но в этом учебном проекте решил оставить оба варианта на память.
# Прошу отнестись с пониманием и не обращать внимание)


@admin.register(Group)  # Первый вариант регистрации модели
class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'description',)
    search_fields = ('title', 'description', 'slug',)
    list_filter = ('title',)
    empty_value_display = DEFAULT_FOR_EMPTY


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'created', 'author', 'post',)
    search_fields = ('text', 'author', 'post',)
    list_filter = ('created',)
    empty_value_display = DEFAULT_FOR_EMPTY


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author',)
    search_fields = ('user', 'author',)
    list_filter = ('user', 'author',)
    empty_value_display = DEFAULT_FOR_EMPTY


admin.site.register(Post, PostAdmin)  # Второй вариант регистрации модели
