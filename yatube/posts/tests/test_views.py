# posts/tests/test_views.py

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Comment, Follow, Group, Post

User = get_user_model()

POSTS_PER_PAGE = settings.POSTS_PER_PAGE


class PostsViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user_not_author = User.objects.create_user(username='not_author')
        cls.user_author = User.objects.create_user(username='post_author')

        cls.group_1 = Group.objects.create(
            title='Тестовая группа 1',
            slug='test-group-1-slug',
            description='Тестовое описание группы номер 1',
        )

        cls.group_2 = Group.objects.create(
            title='Тестовая группа 2',
            slug='test-group-2-slug',
            description='Тестовое описание группы номер 2',
        )

        cls.post = Post.objects.create(
            text='Тестовый текст записи содержащий более 30 символов',
            author=cls.user_author,
            group=cls.group_1,
        )

        cls.comment = Comment.objects.create(
            text='Тестовый текст записи содержащий более 30 символов',
            author=cls.user_author,
            post=cls.post,
        )

        Follow.objects.create(user=cls.user_not_author, author=cls.user_author)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user_author)

    def tearDown(self):
        cache.clear()

    # Проверяем используемые шаблоны
    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        addresses = {
            reverse('posts:main_page'): 'posts/index.html',
            reverse('posts:group_list',
                    kwargs={'slug': self.group_1.slug}):
                        'posts/group_list.html',
            reverse('posts:profile',
                    kwargs={'username': self.user_author.username}):
                        'posts/profile.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_detail',
                    kwargs={'post_id': self.post.pk}):
                        'posts/post_detail.html',
            reverse('posts:post_edit',
                    kwargs={'post_id': self.post.pk}):
                        'posts/create_post.html',
            reverse('posts:follow_index'): 'posts/follow.html',
        }
        for reverse_name, template in addresses.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_context_in_template_index(self):
        """Шаблон index сформирован с правильным контекстом."""
        url = reverse('posts:main_page')
        response = self.authorized_client.get(url)
        last_post = response.context['page_obj'][0]
        self.assertEqual(last_post, self.post)

    def test_context_in_template_group(self):
        """Шаблон group сформирован с правильным контекстом."""
        url = reverse('posts:group_list', kwargs={'slug': self.group_1.slug})
        response = self.authorized_client.get(url)
        test_group = response.context['group']
        test_post = response.context['page_obj'][0]
        self.assertEqual(test_group, self.group_1)
        self.assertEqual(test_post, self.post)

    def test_post_not_another_group(self):
        """Созданный пост не попал в группу, для которой не предназначен"""
        url = reverse('posts:group_list', kwargs={'slug': self.group_2.slug})
        response = self.authorized_client.get(url)
        self.assertEqual(len(response.context['page_obj']), 0)

    def test_context_in_template_post_detail(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        url = reverse('posts:post_detail', kwargs={'post_id': self.post.pk})
        response = self.authorized_client.get(url)
        test_post = response.context['post']
        last_comment = response.context['comments'][0]
        self.assertEqual(test_post, self.post)
        self.assertEqual(last_comment, self.comment)

    def test_context_in_template_profile(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:profile',
                    kwargs={'username': self.user_author.username}))
        test_user = response.context['user']
        test_post = response.context['page_obj'][0]
        self.assertEqual(test_user, self.user_author)
        self.assertEqual(test_post, self.post)

    def test_context_in_template_create_post(self):
        """Шаблон create_post сформирован с правильным контекстом
        при создании поста."""
        url = reverse('posts:post_create')
        response = self.authorized_client.get(url)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for field, expected in form_fields.items():
            with self.subTest(field=field):
                form_field = response.context.get('form').fields.get(field)
                self.assertIsInstance(form_field, expected)

    def test_context_in_template_create_post_is_edit(self):
        """Шаблон create_post сформирован с правильным контекстом
        при редактировании поста."""
        url = reverse('posts:post_edit', kwargs={'post_id': self.post.pk})
        response = self.authorized_client.get(url)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for field, expected in form_fields.items():
            with self.subTest(field=field):
                form_field = response.context.get('form').fields.get(field)
                self.assertIsInstance(form_field, expected)
        is_edit_context = response.context.get('is_edit')
        self.assertTrue(is_edit_context)
        self.assertIsInstance(is_edit_context, bool)

    def test_context_in_template_follow(self):
        """Шаблон follow сформирован с правильным контекстом."""
        self.authorized_client.logout()
        self.authorized_client.force_login(self.user_not_author)
        url = reverse('posts:follow_index')
        response = self.authorized_client.get(url)
        last_post = response.context['page_obj'][0]
        self.assertEqual(last_post, self.post)

    def test_index_cache(self):
        """Проверяем работу кэширования главной страницы"""
        url = reverse('posts:main_page')
        response = self.authorized_client.get(url)
        self.assertEqual(len(response.context['page_obj']), 1)
        post = Post.objects.get(id=self.post.pk)
        post.delete()
        response = self.authorized_client.get(url)
        # self.assertEqual(post, response.context['page_obj'][0])
        self. assertIn(post.text, response.content.decode())
        cache.clear()
        response = self.authorized_client.get(url)
        self.assertNotIn(post.text, response.content.decode())


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Test User')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.PAGE_TEST_OFFSET: int = int(POSTS_PER_PAGE / 2)
        _posts_range = POSTS_PER_PAGE + cls.PAGE_TEST_OFFSET
        for count in range(_posts_range):
            cls.post = Post.objects.create(
                text=f'Тестовый пост номер {count}',
                author=cls.user)

    def test_first_page_contains_expected_count_of_records(self):
        """Проверяем, что первая страница содержит POSTS_PER_PAGE постов"""
        response = self.authorized_client.get(reverse('posts:main_page'))
        self.assertEqual(
            len(response.context.get('page_obj').object_list),
            POSTS_PER_PAGE
        )

    def test_second_page_contains_second_page_with_records(self):
        """Проверяем, что существует вторая страница с остальными постами"""
        response = self.authorized_client.get(
            reverse('posts:main_page') + '?page=2'
        )
        self.assertEqual(
            len(response.context.get('page_obj').object_list),
            self.PAGE_TEST_OFFSET
        )
