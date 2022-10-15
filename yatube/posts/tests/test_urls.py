# posts/tests/test_urls.py

from http import HTTPStatus

from django.core.cache import cache
from django.test import Client, TestCase
from posts.models import Group, Post, User


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user_not_author = User.objects.create_user(username='not_author')
        cls.user_author = User.objects.create_user(username='post_author')

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-group-slug',
            description='Тестовое описание группы',
        )

        cls.post = Post.objects.create(
            text='Тестовый текст записи содержащий более 30 символов',
            author=cls.user_author,
            group=cls.group,
        )

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        cache.clear()

    # Проверяем общедоступные страницы
    def test_for_guest_url_exists_at_desired_location(self):
        """Страницы, не требующие авторизации, доступны любому пользователю."""
        urls = {
            '/': HTTPStatus.OK,
            f'/group/{self.group.slug}/': HTTPStatus.OK,
            f'/profile/{self.user_not_author.username}/': HTTPStatus.OK,
            f'/posts/{self.post.pk}/': HTTPStatus.OK,
            # Проверяем несуществующую страницу
            '/unexisting_page/': HTTPStatus.NOT_FOUND
        }
        for url, expected_status in urls.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(
                    response.status_code, expected_status,
                    f'Страница {url} возвращает не верный статус ответа')

    # Проверяем доступность страниц для авторизованного пользователя
    def test_for_authorized_url_exists_at_desired_location(self):
        """Страницы доступные авторизованному пользователю."""
        self.client.force_login(self.user_not_author)
        urls = {
            '/follow/': HTTPStatus.OK,
            '/create/': HTTPStatus.OK,
        }
        for url, expected_status in urls.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(
                    response.status_code, expected_status,
                    f'Страница {url} возвращает не верный статус ответа')

    # Проверяем доступность страниц для автора поста
    def test_for_author_url_exists_at_desired_location(self):
        """Страница 'posts/<post_id>/edit/' доступна только автору поста."""
        url = f'/posts/{self.post.pk}/edit/'
        self.client.force_login(self.user_author)

        response = self.client.get(url)
        self.assertEqual(
            response.status_code, HTTPStatus.OK,
            f'Страница {url} возвращает не верный статус ответа'
            'для автора поста')

        self.client.force_login(self.user_not_author)
        expexted_url = f'/posts/{self.post.pk}/'
        for method in (self.client.get, self.client.post):
            with self.subTest(method=method):
                response = method(url, follow=True)
                self.assertRedirects(
                    response, expexted_url, msg_prefix=f'{url}')

    # Проверяем редиректы для неавторизованного пользователя
    def test_url_redirect_anonymous_on_login(self):
        """Страницы требующие авторизации перенаправят анонимного пользователя
        на страницу логина."""
        urls = (
            '/posts/create/',
            f'/posts/{self.post.pk}/edit/',
            f'/posts/{self.post.pk}/comment/',
            '/follow/',
            f'/profile/{self.user_not_author.username}/follow/',
            f'/profile/{self.user_not_author.username}/unfollow/',
        )
        login_page = '/auth/login/'

        for url in urls:
            for method in (self.client.get, self.client.post):
                with self.subTest(url=url):
                    expexted_url = f'{login_page}?next={url}'
                    response = method(url, follow=True)
                    self.assertRedirects(
                        response, expexted_url,
                        msg_prefix=f'{url} with method {method.__name__}'
                    )

    # Проверка вызываемых шаблонов для каждого адреса
    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        addresses = {
            '/': 'posts/index.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.user_not_author.username}/': 'posts/profile.html',
            '/posts/create/': 'posts/create_post.html',
            f'/posts/{self.post.pk}/': 'posts/post_detail.html',
            f'/posts/{self.post.pk}/edit/': 'posts/create_post.html',
            '/follow/': 'posts/follow.html',
        }
        self.client.force_login(self.user_author)
        for url, template in addresses.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertTemplateUsed(response, template)
