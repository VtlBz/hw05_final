# about/tests.py

from http import HTTPStatus

from django.test import Client, TestCase


class AboutURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.addresses = {
            '/about/author/': 'about/about_author.html',
            '/about/tech/': 'about/about_tech.html',
        }

    def setUp(self):
        self.client = Client()

    def test_for_guest_url_exists_at_desired_location(self):
        """Страницы, не требующие авторизации, доступны любому пользователю."""
        for url in self.addresses.keys():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(
                    response.status_code, HTTPStatus.OK,
                    f'Страница {url} возвращает не верный статус ответа')

    # Проверка вызываемых шаблонов для каждого адреса
    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        for url, template in self.addresses.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertTemplateUsed(response, template)
