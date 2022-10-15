# posts/tests/test_models.py

from django.contrib.auth import get_user_model
from django.test import TestCase
from posts.models import POST_REPR_MAX_CHARS, Comment, Follow, Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Auth User')
        cls.author = User.objects.create_user(username='Author')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тест' * 10,
            group=cls.group
        )
        cls.comment = Comment.objects.create(
            author=cls.user,
            text='Коммент' * 10,
            post=cls.post
        )
        cls.follow = Follow.objects.create(
            author=cls.author,
            user=cls.user,
        )

    def test_model_group_have_correct_object_names(self):
        """Проверяем, что у модели Group корректно работает __str__."""
        group = PostModelTest.group
        expected_data = group.title
        self.assertEqual(
            str(group),
            expected_data,
            'Метод __str__ модели Group работает не верно'
        )

    def test_model_post_have_correct_object_names(self):
        """Проверяем, что у модели Post корректно работает __str__."""
        post = PostModelTest.post
        expected_data = f'{post.text[:POST_REPR_MAX_CHARS]}.....'
        self.assertEqual(
            str(post),
            expected_data,
            'Метод __str__ модели Post работает не верно'
        )

    def test_model_comment_have_correct_object_names(self):
        """Проверяем, что у модели Comment корректно работает __str__."""
        comment = PostModelTest.comment
        expected_data = f'{comment.text[:POST_REPR_MAX_CHARS]}.....'
        self.assertEqual(
            str(comment),
            expected_data,
            'Метод __str__ модели Comment работает не верно'
        )

    def test_model_follow_have_correct_object_names(self):
        """Проверяем, что у модели Follow корректно работает __str__."""
        follow = PostModelTest.follow
        expected_data = (f'{PostModelTest.user.username} >>> '
                         f'{PostModelTest.author.username}')
        self.assertEqual(
            str(follow),
            expected_data,
            'Метод __str__ модели Follow работает не верно'
        )

    def test_group_verbose_name(self):
        """verbose_name в полях модели Group совпадает с ожидаемым."""
        group = PostModelTest.group
        field_verboses = {
            'title': 'Название группы',
            'slug': 'Slug группы',
            'description': 'Описание группы',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).verbose_name,
                    expected_value
                )

    def test_group_help_text(self):
        """help_text в полях модели Group совпадает с ожидаемым."""
        group = PostModelTest.group
        field_help_texts = {
            'title': 'Введите название группы',
            'slug': ('Укажите адрес для страницы группы. Используйте только '
                     'латиницу, цифры, дефисы и знаки подчёркивания'),
            'description': 'Введите описание группы',
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).help_text,
                    expected_value
                )

    def test_post_verbose_name(self):
        """verbose_name в полях модели Post совпадает с ожидаемым."""
        post = PostModelTest.post
        field_verboses = {
            'text': 'Текст поста',
            'author': 'Автор поста',
            'group': 'Группа',
            'image': 'Изображение',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value)

    def test_post_help_text(self):
        """help_text в полях модели Post совпадает с ожидаемым."""
        post = PostModelTest.post
        field_help_texts = {
            'text': 'Введите текст записи',
            'author': 'Автор поста',
            'group': 'Выберите группу (не обязательно)',
            'image': 'Загрузите изображение (не обязательно)',
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value)

    def test_comment_verbose_name(self):
        """verbose_name в полях модели Comment совпадает с ожидаемым."""
        comment = PostModelTest.comment
        field_verboses = {
            'text': 'Текст комментария',
            'author': 'Автор комментария',
            'post': 'Комментируемый пост',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    comment._meta.get_field(field).verbose_name,
                    expected_value)

    def test_comment_help_text(self):
        """help_text в полях модели Comment совпадает с ожидаемым."""
        comment = PostModelTest.comment
        field_help_texts = {
            'text': 'Введите текст комментария',
            'author': 'Автор комментария',
            'post': 'Пост, к которому оставлен комментарий',
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    comment._meta.get_field(field).help_text,
                    expected_value)

    def test_follow_verbose_name(self):
        """verbose_name в полях модели Follow совпадает с ожидаемым."""
        follow = PostModelTest.follow
        field_verboses = {
            'user': 'Подписчик',
            'author': 'Автор',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    follow._meta.get_field(field).verbose_name,
                    expected_value)

    def test_follow_help_text(self):
        """help_text в полях модели Follow совпадает с ожидаемым."""
        follow = PostModelTest.follow
        field_help_texts = {
            'user': 'Подписчик',
            'author': 'Автор',
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    follow._meta.get_field(field).help_text,
                    expected_value)
