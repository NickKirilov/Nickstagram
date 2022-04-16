import datetime

from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse

from nickstagram.accounts.models import Profile
from nickstagram.comments.models import Comments
from nickstagram.posts.models import Post
from nickstagram.web.models import Likes

UserModel = get_user_model()


class ProfileDetailsViewTests(django_test.TestCase):
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

    def test_redirecting_to_create_profile_page_if_no_profile_but_authenticated_user(self):
        user = self.__create_user(**self.VALID_USER_INFO)
        self.client.login(**self.VALID_USER_INFO)

        response = self.client.get(reverse('home page'))

        self.assertRedirects(response, '/account/profile/create/')

    def test_showing_all_posts_which_are_public_or_are_owned_by_the_user_or_someone_of_his_friends(self):
        user = self.__create_user(**self.VALID_USER_INFO)
        profile = self.__create_profile(**self.VALID_PROFILE_DATA, user=user)
        self.client.login(**self.VALID_USER_INFO)

        post = Post.objects.create(
            title='Test',
            description='Testing...',
            image='tests/test.png',
            profile=user
        )

        Comments.objects.create(
            text='Testing...',
            creator=profile,
            post=post
        )

        Likes.objects.create(
            like=True,
            creator=profile,
            post=post
        )

        response = self.client.get(reverse('home page'))

        self.assertEqual(1, len(response.context['posts'][post]['comments']))
        self.assertEqual(1, response.context['posts'][post]['likes'])

    def test_liking_a_post_and_redirecting_to_post_view__expect_success(self):
        user = self.__create_user(**self.VALID_USER_INFO)
        profile = self.__create_profile(**self.VALID_PROFILE_DATA, user=user)
        self.client.login(**self.VALID_USER_INFO)

        poster = Post.objects.create(
            title='Test',
            description='Testing...',
            image='tests/test.png',
            profile=user
        )

        response = self.client.post(reverse('home page'), data={
            'like': 'Testing...',
            'post-pk': poster.pk,
        })

        self.assertEqual(1, len(Likes.objects.filter(post=poster.pk)))
        self.assertRedirects(response, f'/posts/details/{poster.pk}/')

    def test_disliking_a_post__expect_success(self):
        user = self.__create_user(**self.VALID_USER_INFO)
        profile = self.__create_profile(**self.VALID_PROFILE_DATA, user=user)
        self.client.login(**self.VALID_USER_INFO)

        poster = Post.objects.create(
            title='Test',
            description='Testing...',
            image='tests/test.png',
            profile=user
        )

        like = Likes.objects.create(
            like=True,
            creator=profile,
            post=poster
        )

        response = self.client.post(reverse('home page'), data={
            'unlike': 'Testing...',
            'post-pk': poster.pk,
        })

        self.assertEqual(0, len(Likes.objects.filter(post=poster.pk)))
        self.assertRedirects(response, f'/posts/details/{poster.pk}/')

    def test_redirecting_to_home_page_if_nothing_had_posted(self):
        user = self.__create_user(**self.VALID_USER_INFO)
        profile = self.__create_profile(**self.VALID_PROFILE_DATA, user=user)
        self.client.login(**self.VALID_USER_INFO)

        poster = Post.objects.create(
            title='Test',
            description='Testing...',
            image='tests/test.png',
            profile=user
        )

        response = self.client.post(reverse('home page'), data={
            'post-pk': poster.pk,
        })

        self.assertRedirects(response, '/')