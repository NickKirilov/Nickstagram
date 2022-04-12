import datetime

from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse

from nickstagram.accounts.models import Profile

UserModel = get_user_model()


class EditProfileViewTests(django_test.TestCase):
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
        response = self.client.get(reverse('edit profile page'))

        self.assertTemplateUsed("account_templates/edit_profile.html")

    def test_redirecting_to_create_profile_if_no_profile(self):
        user = self.__create_user(**self.VALID_USER_INFO)
        self.client.login(**self.VALID_USER_INFO)

        response = self.client.get(reverse('edit profile page'))

        self.assertEqual('/', response.url)

    def test_redirecting_to_profile_page_after_success(self):
        user = self.__create_user(**self.VALID_USER_INFO)
        profile = self.__create_profile(**self.VALID_PROFILE_DATA, user=user)
        self.client.login(**self.VALID_USER_INFO)

        self.client.get(reverse('edit profile page'))
        response = self.client.post(reverse('edit profile page'), data={
            **self.VALID_PROFILE_DATA,
            'image': 'image/test.png',
        })

        profile.refresh_from_db()

        self.assertRedirects(response, '/account/profile/')
