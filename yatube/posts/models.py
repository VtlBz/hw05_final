from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

POST_REPR_MAX_CHARS: int = 30


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название группы',
        help_text='Введите название группы'
    )
    slug = models.SlugField(
        unique=True,
        max_length=200,
        verbose_name='Slug группы',
        help_text='Укажите адрес для страницы группы. Используйте только '
                  'латиницу, цифры, дефисы и знаки подчёркивания'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание группы',
        help_text='Введите описание группы'
    )

    class Meta:
        db_table = 'groups'
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст поста',
        help_text='Введите текст записи'
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор поста',
        help_text='Автор поста'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        verbose_name='Группа',
        help_text='Выберите группу (не обязательно)'
    )
    image = models.ImageField(
        verbose_name='Изображение',
        help_text='Загрузите изображение (не обязательно)',
        upload_to='posts/',
        blank=True
    )

    class Meta:
        db_table = 'posts'
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __repr__(self):
        return (
            f'Post id: {self.pk}, '
            f'Start text: {self.text[:POST_REPR_MAX_CHARS]}.....'
        )

    def __str__(self):
        return (
            f'{self.text[:POST_REPR_MAX_CHARS]}.....'
        )


class Comment(models.Model):
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Введите текст комментария'
    )
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
        help_text='Автор комментария'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментируемый пост',
        help_text='Пост, к которому оставлен комментарий'
    )

    class Meta:
        db_table = 'comments'
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __repr__(self):
        return (
            f'Comment id: {self.pk}, '
            f'Start text: {self.text[:POST_REPR_MAX_CHARS]}.....'
        )

    def __str__(self):
        return (
            f'{self.text[:POST_REPR_MAX_CHARS]}.....'
        )


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        help_text='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
        help_text='Автор',
    )

    class Meta:
        db_table = 'follows'
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
        constraints = [models.UniqueConstraint(
            fields=['user', 'author'],
            name='unique_follow')
        ]

    def __repr__(self):
        return (
            f'Follow id: {self.pk}, '
            f'{self.user.username} >>> {self.author.username}'
        )

    def __str__(self):
        return f'{self.user.username} >>> {self.author.username}'
