import datetime

from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse

from nickstagram.accounts.models import Profile
from nickstagram.web.models import Post, Comments, Likes

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

    def test_correct_template__expect_profile_page_template(self):
        response = self.client.get(reverse('profile page'))

        self.assertTemplateUsed("account_templates/profile.html")

    def test_when_there_is_not_an_user__expect_redirect_to_login_page(self):
        response = self.client.get(reverse('profile page'))

        self.assertEqual('/account/login/?next=/account/profile/', response.url)

    def test_when_no_posts__should_not_have_any_posts(self):
        user = self.__create_user(**self.VALID_USER_INFO)
        profile = self.__create_profile(**self.VALID_PROFILE_DATA,
                                        user=user)

        self.client.login(**self.VALID_USER_INFO)
        response = self.client.get(reverse('profile page'))

        self.assertEqual({}, response.context['posts'])
        self.assertIsNone(response.context['comment_form'])

    def test_when_there_are_posts__should_have_posts_but_without_comments_and_likes(self):
        user = self.__create_user(**self.VALID_USER_INFO)
        profile = self.__create_profile(**self.VALID_PROFILE_DATA,
                                        user=user)

        self.client.login(**self.VALID_USER_INFO)
        post = Post.objects.create(
            title='Test',
            description='Testing...',
            image='images/default.png',
            profile=user
        )
        response = self.client.get(reverse('profile page'))

        self.assertEqual(1, len(response.context['posts']))

    def test_when_there_are_posts__should_have_posts_with_comments_but_without_likes(self):
        user = self.__create_user(**self.VALID_USER_INFO)
        profile = self.__create_profile(**self.VALID_PROFILE_DATA,
                                        user=user)

        self.client.login(**self.VALID_USER_INFO)
        post = Post.objects.create(
            title='Test',
            description='Testing...',
            image='images/default.png',
            profile=user
        )
        comment = Comments.objects.create(
            text='Testing...',
            creator=profile,
            post=post
        )
        response = self.client.get(reverse('profile page'))
        comments = response.context['posts'][post]['comments']
        self.assertEqual(1, len(comments))

    def test_when_there_are_posts__should_have_posts_with_comments_and_likes(self):
        user = self.__create_user(**self.VALID_USER_INFO)
        profile = self.__create_profile(**self.VALID_PROFILE_DATA,
                                        user=user)

        self.client.login(**self.VALID_USER_INFO)
        post = Post.objects.create(
            title='Test',
            description='Testing...',
            image='images/default.png',
            profile=user
        )
        comment = Comments.objects.create(
            text='Testing...',
            creator=profile,
            post=post
        )
        like = Likes.objects.create(like=True, creator=profile, post=post)
        response = self.client.get(reverse('profile page'))
        comments = response.context['posts'][post]['comments']
        likes = response.context['posts'][post]['likes']
        self.assertEqual(1, len(comments))
        self.assertEqual(1, likes)
        comment.delete()

    def test_when_no_profile__should_redirect_to_create_profile_page(self):
        user = self.__create_user(**self.VALID_USER_INFO)
        self.client.login(**self.VALID_USER_INFO)
        response = self.client.get(reverse('profile page'))

        self.assertEqual('/account/profile/create/', response.url)

    def test_commenting_the_correct_post(self):
        user = self.__create_user(**self.VALID_USER_INFO)
        profile = self.__create_profile(**self.VALID_PROFILE_DATA,
                                        user=user)

        self.client.login(**self.VALID_USER_INFO)
        Post.objects.create(
            title='Test',
            description='Testing...',
            image='images/default.png',
            profile=user
        )
        Post.objects.create(
            title='Test',
            description='Testing...',
            image='images/default.png',
            profile=user
        )

        response = self.client.post(reverse('profile page'), data={
            "text": ["testing"],
            "post-pk": 1
        })
        post_context = self.client.get(reverse('profile page')).context['posts']

        self.assertEqual("{<Post: Post object (2)>: {'comments': [], 'likes': 0}, <Post: Post object (1)>: {"
                         "'comments': [<Comments: Comments object (1)>], 'likes': 0}}",
                         str(post_context))

