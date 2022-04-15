import random

from django.contrib.auth import login, get_user, get_user_model
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.contrib.auth.hashers import get_hasher, check_password, make_password
from django.core.mail import send_mail, send_mass_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import mixins as auth_mixins
from django.urls import reverse_lazy
from django.views import generic as views
from nickstagram.accounts.forms import RegistrationForm, LoginForm, EditProfileForm, CreateProfileForm, \
    DeleteProfileForm
from nickstagram.accounts.models import Profile
from nickstagram.comments.forms import CommentPostForm
from nickstagram.comments.models import Comments
from nickstagram.web.models import Post, Likes

UserModel = get_user_model()


class RegisterView(views.CreateView):
    template_name = "account_templates/register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy('home page')

    def form_valid(self, *args, **kwargs):
        result = super().form_valid(*args, **kwargs)
        login(self.request, self.object)
        return result


class ProfileMoreInfo(auth_mixins.LoginRequiredMixin, views.TemplateView):
    def get(self, request, *args, **kwargs):
        profile = Profile.objects.filter(username=request.user)

        if not profile:
            return redirect('create profile page')

        profile = profile[0]

        got_posts = Post.objects.filter(profile=request.user)
        got_posts = got_posts[::-1]

        posts = {}

        for post in got_posts:
            posts[post] = Comments.objects.filter(post_id=post.pk)
            posts[post] = {'comments': Comments.objects.filter(post_id=post.pk)[::-1],
                           'likes': len(Likes.objects.filter(post_id=post.pk))}

        if profile.friends:
            friends = len(profile.friends.split(' ')) - 1
        else:
            friends = 0

        context = {
            'profile': profile,
            'posts': posts,
            'friends': friends
        }
        return render(
            request,
            "account_templates/profile.html",
            context
        )

    @staticmethod
    def post(request, *args, **kwargs):
        comment_form = CommentPostForm(request.POST)
        post_pk = request.POST.get('post-pk')
        post = Post.objects.filter(pk=post_pk)
        profile = Profile.objects.get(pk=request.user.pk)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.creator = profile
            if post:
                comment.post = post[0]
            else:
                return redirect('profile page', kwargs['pk'])

            comment.save()

            return redirect('profile page', kwargs['pk'])
        return redirect('profile page', kwargs['pk'])


class UserLoginView(auth_views.LoginView):
    template_name = 'account_templates/login.html'
    form_class = LoginForm

    def get_success_url(self):
        return reverse_lazy('home page')


class EditProfileView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    def get(self, request, *args, **kwargs):
        profile = Profile.objects.filter(username=request.user)

        if profile:
            profile = profile[0]
        else:
            return redirect('home page')

        profile_form = EditProfileForm(instance=profile)

        context = {
            'profile_form': profile_form,
            'profile': profile,
        }
        return render(request, "account_templates/edit_profile.html", context)

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.filter(username=self.request.user)[0]
        profile_form = EditProfileForm(request.POST, request.FILES, instance=profile)

        if profile_form.is_valid():

            profile = profile_form.save(commit=False)
            img = 'image'
            if img in request.FILES:
                profile.image = request.FILES[img]

            profile.save()
            return redirect('profile page', kwargs['pk'])

        context = {
            'profile_form': profile_form,
        }
        return render(request, "account_templates/edit_profile.html", context)


class CreateProfileView(auth_mixins.LoginRequiredMixin, views.CreateView):
    def get(self, request, *args, **kwargs):
        profile_form = CreateProfileForm()

        context = {
            'profile_form': profile_form,
        }
        return render(request, "account_templates/create_profile.html", context)

    def post(self, request, *args, **kwargs):
        profile_form = CreateProfileForm(data=request.POST)
        user = get_user(request=request)

        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.username = user.username
            img = 'image'
            if img in request.FILES:
                profile.image = request.FILES[img]
            profile.save()

            return redirect('home page')

        context = {
            'profile_form': profile_form,
        }
        return render(request, "account_templates/create_profile.html", context)


class DeleteProfileView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    def get(self, request, *args, **kwargs):
        return render(request, 'account_templates/delete_profile.html')

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.filter(username=request.user)[0]
        profile_form = DeleteProfileForm(request.POST, request.FILES, instance=profile)
        profile_form.save()
        return redirect('home page')


class ChangePasswordView(views.UpdateView, auth_mixins.LoginRequiredMixin):
    model = UserModel
    template_name = 'account_templates/reset_password.html'
    fields = ('password',)

    def post(self, request, *args, **kwargs):
        old_password = request.POST.get('old-password')
        new_password = request.POST.get('new-password')
        user = self.request.user
        algorithm, salt, sha1_hash = user.password.split('$', 2)
        hasher = get_hasher(algorithm)

        if hasher.verify(old_password, user.password):
            try:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Successful change of password!')
                return redirect('profile page', user.pk)
            except:
                return HttpResponse('Invalid new password! It must contain at least 8 characters, includes numbers, '
                                    'upper and lower letters!')
        else:
            messages.warning(request, 'The provided old password is not the same!')
            return redirect('profile page', user.pk)


class ForgottenPasswordView(views.View):
    @staticmethod
    def get(request, *args, **kwargs):
        return render(request, 'account_templates/sending_email_for_new_password.html')

    @staticmethod
    def post(request, *args, **kwargs):
        try:
            username = request.POST.get('username')
            user = UserModel.objects.get(username=username)
            profile = Profile.objects.get(username=username)
        except:
            messages.warning(request, 'Username is not correct!')
            return redirect('home page')

        new_password = ''.join(str(random.randint(1, 1000)) for _ in range(8))
        new_password += username[0].upper() + username[1]

        user.set_password(new_password)
        user.save()

        message = (
            'Forgotten password',
            f'This is your password: {new_password} || after logining with it change it!',
            'garaj.garaj.garaj@gmail.com',
            [profile.email]
        )
        try:
            send_mass_mail((message, ), fail_silently=False)
        except:
            messages.warning(request, "Something gone wrong!")
            return redirect('login page')
        return redirect('login page')
