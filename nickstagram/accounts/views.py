from django.contrib.auth import login, get_user
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from django.contrib.auth import mixins as auth_mixins


from django.urls import reverse_lazy
from django.views import generic as views

from nickstagram.accounts.forms import RegistrationForm, LoginForm, EditProfileForm, CreateProfileForm, \
    DeleteProfileForm
from nickstagram.accounts.models import Profile
from nickstagram.web.forms import CommentPostForm
from nickstagram.web.models import Post, Comments, Likes


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

        got_posts = Post.objects.filter(profile=request.user)
        got_posts = got_posts[::-1]

        posts = {}

        for post in got_posts:
            posts[post] = Comments.objects.filter(post_id=post.pk)
            posts[post] = {'comments': Comments.objects.filter(post_id=post.pk)[::-1],
                           'likes': len(Likes.objects.filter(post_id=post.pk))}
        if posts:
            comment_form = CommentPostForm()
        else:
            comment_form = None
        context = {
            'profile': profile[0],
            'posts': posts,
            'comment_form': comment_form
        }
        return render(
            request,
            "account_templates/profile.html",
            context
        )

    def post(self, request,  *args, **kwargs):
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
                return redirect('profile page')

            comment.save()

            return redirect('profile page')
        return redirect('profile page')


class UserLoginView(auth_views.LoginView):
    template_name = 'account_templates/login.html'
    form_class = LoginForm

    def get_success_url(self):
        return reverse_lazy('home page')


class EditProfileView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    def get(self, request, *args, **kwargs):
        profile = Profile.objects.filter(username=request.user)[0]
        profile_form = EditProfileForm(instance=profile)

        context = {
            'profile_form': profile_form,
            'profile': profile,
        }
        return render(request, "account_templates/edit_profile.html", context)

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.filter(username=request.user)[0]
        profile_form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if 'image' in request.FILES and profile.image != 'images/profile_imgs/default.png':
            profile.image.delete()

        if profile_form.is_valid():

            edited_profile = profile_form.save(commit=False)
            img = 'image'
            if img in request.FILES:
                edited_profile.image = request.FILES[img]

            edited_profile.save()
            return redirect('home page')

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
            else:
                profile.image = 'images/profile_imgs/default.png'
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

