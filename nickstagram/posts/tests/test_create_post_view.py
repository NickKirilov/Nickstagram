import datetime
import io
from PIL import Image
from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse
from nickstagram.accounts.models import Profile
from nickstagram.web.models import Post

UserModel = get_user_model()


class CreatePostViewTests(django_test.TestCase):
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

    @staticmethod
    def __generate_photo_file():
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def test_creating_post_redirecting_to_the_details_of_the_post(self):
        user = self.__create_user(**self.VALID_USER_INFO)
        profile = self.__create_profile(**self.VALID_PROFILE_DATA, user=user)
        self.client.login(**self.VALID_USER_INFO)

        response = self.client.post(reverse('create post page'), data={
            'title': 'Test',
            'description': 'Testing...',
            'image': self.__generate_photo_file()
        })

        post = Post.objects.filter(profile=user)

        if post:
            post = post[0]
        else:
            raise Exception('Not post created')

        self.assertRedirects(response, f'/posts/details/{post.pk}/')