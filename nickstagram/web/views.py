from django.contrib.auth import mixins as auth_mixins
from django.shortcuts import render, redirect
from django.db.models import Q
from django.views import generic as views
from nickstagram.accounts.models import Profile
from nickstagram.web.forms import CommentPostForm
from nickstagram.web.models import Post, Comments, Likes


class IndexView(views.TemplateView, auth_mixins.LoginRequiredMixin):
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

    @staticmethod
    def post(request, *args, **kwargs):
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


class SearchView(auth_mixins.LoginRequiredMixin, views.ListView):
    model = Profile
    template_name = 'search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            post_result = Profile.objects.filter(
                Q(first_name__contains=query) | Q(last_name__contains=query) | Q(username__contains=query)
            )
            result = post_result
        else:
            result = None

        return result

    def post(self, *args, **kwargs):
        profile = Profile.objects.get(pk=self.request.user.pk)
        person_to_follow = self.request.POST.get('person-to-follow')

        if person_to_follow not in profile.friends.split(' '):
            profile.friends += person_to_follow + ' '
            profile.save()

        return redirect('search page')
