import datetime

from django.core.exceptions import ValidationError

from nickstagram.accounts.models import Profile, NickstagramUser
from django import test


class ProfileTest(test.TestCase):
    def test_profile_create__when_first_name_contains_only_letters__expect_success(self):
        user = NickstagramUser.objects.create(username='habibi')
        profile = Profile.objects.create(first_name='Kiro',
                                         last_name='Kirow',
                                         user=user,
                                         username='habibi',
                                         email='asdfads@abv.bg',
                                         date_of_birth=datetime.date(day=2, year=2000, month=4))
        profile.full_clean()

        self.assertEqual('Kiro', profile.first_name)

    def test_profile_create__when_first_name_contains_a_digit__expect_to_fail(self):
        user = NickstagramUser.objects.create(username='habibi')
        person = Profile.objects.create(first_name='Kir0',
                                        last_name='Kirow',
                                        user=user,
                                        username='habibi',
                                        email='asdfads@abv.bg',
                                        date_of_birth=datetime.date(day=2, year=2000, month=4))

        with self.assertRaises(ValidationError) as ex:
            person.full_clean()

        self.assertEqual('The first name must contains only letters.', str(ex.exception.messages[0]))

    def test_profile_create__when_first_name_contains_a_sign__expect_to_fail(self):
        user = NickstagramUser.objects.create(username='habibi')
        person = Profile.objects.create(first_name='Kir%',
                                        last_name='Kirow',
                                        user=user,
                                        username='habibi',
                                        email='asdfads@abv.bg',
                                        date_of_birth=datetime.date(day=2, year=2000, month=4))

        with self.assertRaises(ValidationError) as ex:
            person.full_clean()

        self.assertEqual('The first name must contains only letters.', str(ex.exception.messages[0]))

    def test_profile_create__when_first_name_contains_a_space__expect_to_fail(self):
        user = NickstagramUser.objects.create(username='habibi')
        person = Profile.objects.create(first_name='Ki r%',
                                        last_name='Kirow',
                                        user=user,
                                        username='habibi',
                                        email='asdfads@abv.bg',
                                        date_of_birth=datetime.date(day=2, year=2000, month=4))

        with self.assertRaises(ValidationError) as ex:
            person.full_clean()

        self.assertEqual('The first name must contains only letters.', str(ex.exception.messages[0]))
