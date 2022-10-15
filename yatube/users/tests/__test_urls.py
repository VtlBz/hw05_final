# users/tests/test_urls.py
"""Не проверять, это доролнительное задание не доделано"""

from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()


class UsersURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='NoName')

    def setUp(self):
        self.client = Client()

    # Проверяем общедоступные страницы
    def test_for_guest_url_exists_at_desired_location(self):
        """Страницы, не требующие авторизации, доступны любому пользователю."""
        urls = (
            '/auth/login/',
            '/auth/logout/',
            '/auth/signup/',
            '/auth/password_reset/complete/',
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(
                    response.status_code, HTTPStatus.OK,
                    f'Страница {url} возвращает не верный статус ответа')

    # # Проверяем доступность страниц для авторизованного пользователя
    # def test_for_authorized_url_exists_at_desired_location(self):
    #     """Страница '/create/' доступна авторизованному пользователю."""
    #     self.client.force_login(self.user_not_author)
    #     url = '/create/'
    #     response = self.client.get(url)
    #     self.assertEqual(
    #         response.status_code, HTTPStatus.OK,
    #         f'Страница {url} возвращает не верный статус ответа')

    # # Проверяем доступность страниц для автора поста
    # def test_for_author_url_exists_at_desired_location(self):
    #     """Страница 'posts/<post_id>/edit/' доступна автору поста."""
    #     self.client.force_login(self.user_author)
    #     url = f'/posts/{self.post.pk}/edit/'
    #     response = self.client.get(url)
    #     self.assertEqual(
    #         response.status_code, HTTPStatus.OK,
    #         f'Страница {url} возвращает не верный статус ответа')

    # Проверяем редиректы для неавторизованного пользователя
    def test_url_redirect_anonymous_on_login(self):
        """Страницы требующие авторизации перенаправят анонимного пользователя
        на страницу логина."""
        urls = (
            '/auth/password_change/',
            '/auth/password_change/done/',
            '/auth/password_reset/',
            '/auth/password_reset/done/',
            '/auth/password_reset/<uidb64>/<token>/',
        )
        for url in urls:
            with self.subTest(url=url):
                expexted_url = f'/auth/login/?next={url}'
                response = self.client.get(url, follow=True)
                self.assertRedirects(
                    response, expexted_url, msg_prefix=f'{url}')

    # Проверка вызываемых шаблонов для каждого адреса
    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        addresses = {
            '/auth/login/': 'users/login.html',
            '/auth/signup/': 'users/signup.html',
            '/auth/password_change/': 'users/password_change_form.html',
            '/auth/password_change/done/': 'users/password_change_done.html',
            '/auth/password_reset/': 'users/password_reset_form.html',
            '/auth/password_reset/done/': 'users/password_reset_done.html',
            '/auth/password_reset/<uidb64>/<token>/':
                'users/password_reset_confirm.html',
            '/auth/password_reset/complete/':
                'users/password_reset_complete.html',
            '/auth/logout/': 'users/logged_out.html',
        }
        self.client.force_login(self.user)
        for url, template in addresses.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertTemplateUsed(response, template)
