import datetime

from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse

from nickstagram.accounts.models import Profile

UserModel = get_user_model()


class CreateProfileViewTests(django_test.TestCase):
    VALID_USER_INFO = {
        'username': 'testuser',
        'password': '20042004Nk',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'Kiro',
        'last_name': 'Kirow',
        'username': 'testuser',
        'email': 'asdfads@abv.bg',
        'date_of_birth': datetime.date(day=2, year=2000, month=4)
    }

    @staticmethod
    def __create_user(**data):
        return UserModel.objects.create_user(**data)

    @staticmethod
    def __create_profile(**data):
        return Profile.objects.create(**data)

    def test_correct_template__expect_edit_profile_page_template(self):
        response = self.client.get(reverse('create profile page'))

        self.assertEqual('/account/profile/create/', response.wsgi_request.path)

    def test_redirecting_to_home_page_after_successful_creation(self):
        user = self.__create_user(**self.VALID_USER_INFO)
        self.client.login(**self.VALID_USER_INFO)

        response = self.client.post(reverse('create profile page'), data={
            **self.VALID_PROFILE_DATA
        })

        self.assertRedirects(response, '/')

    def test_creating_a_profile__expect_success(self):
        user = self.__create_user(**self.VALID_USER_INFO)
        self.client.login(**self.VALID_USER_INFO)

        self.client.post(reverse('create profile page'), data={
            **self.VALID_PROFILE_DATA
        })

        self.assertEqual('testuser', Profile.objects.get(username='testuser').username)
        