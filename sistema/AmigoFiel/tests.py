from django.contrib.auth import SESSION_KEY, get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class WebLoginSecurityTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="adotante",
            password="SenhaForte123!",
        )

    def test_login_page_renders_with_csrf_cookie(self):
        client = Client(enforce_csrf_checks=True)

        response = client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("csrftoken", response.cookies)
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_login_post_requires_csrf_token(self):
        client = Client(enforce_csrf_checks=True)

        response = client.post(
            reverse("login"),
            {"username": "adotante", "password": "SenhaForte123!"},
        )

        self.assertEqual(response.status_code, 403)
        self.assertNotIn(SESSION_KEY, client.session)

    def test_login_with_valid_credentials_creates_session(self):
        response = self.client.post(
            reverse("login"),
            {"username": "adotante", "password": "SenhaForte123!"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/")
        self.assertEqual(int(self.client.session[SESSION_KEY]), self.user.pk)

    def test_login_with_invalid_credentials_does_not_create_session(self):
        response = self.client.post(
            reverse("login"),
            {"username": "adotante", "password": "senha-errada"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_logout_requires_post(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("logout"))

        self.assertEqual(response.status_code, 405)
        self.assertIn(SESSION_KEY, self.client.session)

    def test_logout_post_clears_session(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse("logout"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("login"))
        self.assertNotIn(SESSION_KEY, self.client.session)
