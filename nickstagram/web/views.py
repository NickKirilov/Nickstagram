from django.contrib.auth import get_user
from django.contrib.auth import mixins as auth_mixins
from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.views import generic as views

from nickstagram.accounts.models import Profile
from nickstagram.web.forms import CreatePostForm, EditPostForm, DeletePostForm, CommentPostForm
from nickstagram.web.models import Post, Comments, Likes


class IndexView(views.TemplateView, auth_mixins.LoginRequiredMixin):
    login_url = '/account/login/'

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
                likes = Likes.objects.filter(post_id=post.pk)
                posts[post] = {'comments': Comments.objects.filter(post_id=post.pk)[::-1],
                               'likes': len(Likes.objects.filter(post_id=post.pk)),
                               'user_likes': False}

                for like in likes:
                    if like.creator.pk == profile[0].pk:
                        posts[post]['user_likes'] = True

            profile = profile[0]

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
        likes = Likes.objects.filter(post_id=post.pk)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.creator = profile
            comment.post = post
            comment.save()

        if request.POST.get('like'):
            for like in likes:
                if like.creator.pk == profile.pk:
                    return redirect('home page')

            new_like = Likes()
            new_like.post = post
            new_like.creator = profile
            new_like.like = True

            new_like.save()
            return redirect('post details page', post.pk)

        if request.POST.get('unlike'):
            for like in likes:
                if like.creator.pk == profile.pk:
                    like.delete()
            return redirect('post details page', post.pk)

        return redirect('home page')


class CreatePostView(auth_mixins.LoginRequiredMixin, views.CreateView):
    model = Post

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


class PostDetailsView(auth_mixins.LoginRequiredMixin, views.View):
    def get(self, request,  pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        comment_form = CommentPostForm()
        comments = Comments.objects.filter(post_id=post.pk)
        likes = Likes.objects.filter(post_id=post.pk)
        user_liked = False

        for like in likes:
            if like.creator.pk == request.user.pk:
                user_liked = True

        context = {
            'post': post,
            'user': request.user,
            'comment_form': comment_form,
            'comments': comments,
            'likes': len(likes),
            'user_liked': user_liked,
        }

        return render(request, 'post_templates/post_details.html', context)

    def post(self, request, *args, **kwargs):
        comment_form = CommentPostForm(request.POST)
        post = Post.objects.get(pk=self.kwargs['pk'])
        profile = Profile.objects.get(pk=request.user.pk)
        likes = Likes.objects.filter(post_id=post.pk)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.creator = profile
            comment.post = post

            comment.save()

        if request.POST.get('like'):
            for like in likes:
                if like.creator.pk == profile.pk:
                    return redirect('post details page', post.pk)
            new_like = Likes()
            new_like.post = post
            new_like.creator = profile
            new_like.like = True

            new_like.save()
            return redirect('post details page', post.pk)

        if request.POST.get('unlike'):
            for like in likes:
                if like.creator.pk == profile.pk:
                    like.delete()
            return redirect('post details page', post.pk)

        return redirect('post details page', post.pk)


class EditPostView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    template_name = 'post_templates/edit_post.html'
    form_class = EditPostForm
    model = Post

    def get_success_url(self):
        success_url = reverse('post details page', kwargs=self.kwargs)
        return success_url


class DeletePostView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    form_class = DeletePostForm
    model = Post
    success_url = reverse_lazy('home page')
    template_name = 'post_templates/delete_post.html'
