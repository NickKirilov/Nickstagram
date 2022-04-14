from django.shortcuts import render, redirect
from django.contrib.auth import get_user
from django.contrib.auth import mixins as auth_mixins
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from nickstagram.accounts.models import Profile
from nickstagram.posts.forms import CreatePostForm, EditPostForm, DeletePostForm
from nickstagram.posts.models import Post
from nickstagram.web.forms import CommentPostForm
from nickstagram.web.models import Comments, Likes


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
    @staticmethod
    def get(request, pk, *args, **kwargs):
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
