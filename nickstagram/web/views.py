from django.contrib.auth import get_user, login
from django.contrib.auth.views import LoginView
from django.contrib.messages import views as msg_views
from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.views import generic as views

from nickstagram.accounts.models import Profile
from nickstagram.web.forms import CreatePostForm, EditPostForm, DeletePostForm, CommentPostForm
from nickstagram.web.models import Post, Comments


class IndexView(views.TemplateView):
    def get(self, *args, **kwargs):
        profile = Profile.objects.filter(username=self.request.user)

        if not profile and self.request.user.is_authenticated:
            return redirect('create profile page')

        elif profile and self.request.user.is_authenticated:
            posts = {}
            comment_form = CommentPostForm()
            got_posts = Post.objects \
                .order_by('date_of_creation')\
                .filter(Q(profile=self.request.user) | Q(public=True))
            got_posts = got_posts[::-1]
            for post in got_posts:
                posts[post] = Comments.objects.filter(post_id=post.pk)

        else:
            posts = {}
            comment_form = {}

        context = {
            'profile': profile,
            'posts': posts,
            'comment_form': comment_form,
        }
        return render(self.request, 'index.html', context)

    def post(self, request,  *args, **kwargs):
        comment_form = CommentPostForm(request.POST)
        post_pk = request.POST.get('post-pk')
        post = Post.objects.get(pk=post_pk)
        profile = Profile.objects.get(pk=request.user.pk)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.creator = profile
            comment.post = post

            comment.save()

            return redirect('home page')
        return redirect('home page')


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

            return redirect('post details page', post.pk)

        context = {
            'post_form': post_form,
        }
        return render(request, "account_templates/create_profile.html", context)


class PostDetailsView(views.View):
    def get(self, request,  pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        comment_form = CommentPostForm()
        comments = Comments.objects.filter(post_id=post.pk)

        context = {
            'post': post,
            'user': request.user,
            'comment_form': comment_form,
            'comments': comments,
        }

        return render(request, 'post_templates/post_details.html', context)

    def post(self, request, *args, **kwargs):
        comment_form = CommentPostForm(request.POST)
        post = Post.objects.get(pk=self.kwargs['pk'])
        profile = Profile.objects.get(pk=request.user.pk)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.creator = profile
            comment.post = post

            comment.save()

            return redirect('post details page', post.pk)
        return redirect('post details page', post.pk)


class EditPostView(views.UpdateView):
    template_name = 'post_templates/edit_post.html'
    form_class = EditPostForm
    model = Post

    def get_success_url(self):
        success_url = reverse('post details page', kwargs=self.kwargs)
        return success_url


class DeletePostView(views.DeleteView):
    form_class = DeletePostForm
    model = Post
    success_url = reverse_lazy('home page')
    template_name = 'post_templates/delete_post.html'
