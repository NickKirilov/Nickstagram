from django.contrib.auth import get_user, login
from django.contrib.auth.views import LoginView
from django.contrib.messages import views as msg_views
from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic as views

from nickstagram.accounts.models import Profile
from nickstagram.web.forms import CreatePostForm, EditPostForm, DeletePostForm
from nickstagram.web.models import Post


class IndexView(views.TemplateView):
    def get(self, *args, **kwargs):
        profile = Profile.objects.filter(username=self.request.user)

        if not profile and self.request.user.is_authenticated:
            return redirect('create profile page')

        elif profile and self.request.user.is_authenticated:
            posts = Post.objects\
                .filter(Q(profile=self.request.user) | Q(public=True))\
                .order_by('date_of_creation')

        else:
            posts = []

        context = {
            'profile': profile,
            'posts': posts,
        }
        return render(self.request, 'index.html', context)


class CreatePostView(views.View):
    def get(self, request, *args, **kwargs):
        post_form = CreatePostForm()
        context = {
            'post_form': post_form,
        }
        return render(request, 'post_templates/create_post.html', context)

    def post(self, request, *args, **kwargs):
        post_form = CreatePostForm(request.POST, request.FILES)
        user = get_user(request=request)

        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.profile = user
            img = 'image'
            if img in request.FILES:
                post.image = request.FILES[img]

            post.save()

            return redirect('home page')

        context = {
            'post_form': post_form,
        }
        return render(request, "account_templates/create_profile.html", context)


class PostDetailsView(views.View):
    def get(self, request,  pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        context = {
            'post': post,
            'user': request.user,
        }

        return render(request, 'post_templates/post_details.html', context)


class EditPostView(views.UpdateView):
    template_name = 'post_templates/edit_post.html'
    form_class = EditPostForm
    model = Post
    success_url = reverse_lazy('home page')


class DeletePostView(views.DeleteView):
    form_class = DeletePostForm
    model = Post
    success_url = reverse_lazy('home page')
    template_name = 'post_templates/delete_post.html'
