from django.shortcuts import redirect
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins

from nickstagram.accounts.models import Profile
from nickstagram.comments.forms import CommentPostForm, EditCommentForm
from nickstagram.comments.models import Comments
from nickstagram.posts.models import Post
from nickstagram.web.models import Likes


class CreateCommentView(auth_mixins.LoginRequiredMixin, views.CreateView):
    model = Comments
    form_class = CommentPostForm
    template_name = 'comment_templates/comment.html'

    def get_context_data(self, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        likes = Likes.objects.filter(post=post)
        return super(CreateCommentView, self).get_context_data(**{'post': post, 'likes': len(likes)})

    def post(self, request, *args, **kwargs):
        form_data = CommentPostForm(request.POST)
        post_pk = int(request.POST.get('post-pk'))
        post = Post.objects.filter(pk=post_pk)

        if post:
            post = post[0]
        else:
            return redirect('home page')

        profile = Profile.objects.get(pk=request.user.pk)

        if form_data.is_valid():
            comment = form_data.save(commit=False)
            comment.creator = profile
            comment.post = post
            comment.save()

        return redirect('post details page', post.pk)


class EditCommentView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    model = Comments
    form_class = EditCommentForm
    template_name = 'comment_templates/edit_comment.html'

    def get_context_data(self, **kwargs):
        comment = Comments.objects.filter(pk=self.kwargs['pk'])
        if comment:
            comment = comment[0]
        else:
            redirect('home page')

        post = comment.post
        likes = Likes.objects.filter(post=post)
        return super(EditCommentView, self).get_context_data(**{'post': post, 'likes': len(likes)})

    def post(self, request, *args, **kwargs):
        post_pk = int(request.POST.get('post-pk'))
        post = Post.objects.filter(pk=post_pk)
        comment = Comments.objects.filter(pk=kwargs['pk'])
        if post:
            post = post[0]
        else:
            return redirect('home page')

        if comment:
            comment = comment[0]
        else:
            return redirect('post details page', post.pk)

        form_data = EditCommentForm(request.POST, instance=comment)
        profile = Profile.objects.get(pk=request.user.pk)

        if form_data.is_valid():
            comment = form_data.save(commit=False)
            comment.creator = profile
            comment.post = post
            comment.save()

        return redirect('post details page', post.pk)


def delete_comment(request, pk):
    comment = Comments.objects.get(pk=pk)
    comment.delete()
    return redirect('home page')
