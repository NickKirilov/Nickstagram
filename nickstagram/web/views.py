from django.contrib.auth import mixins as auth_mixins
from django.shortcuts import render, redirect
from django.db.models import Q
from django.views import generic as views
from nickstagram.accounts.models import Profile, NickstagramUser
from nickstagram.comments.models import Comments
from nickstagram.web.models import Post, Likes


class IndexView(views.TemplateView, auth_mixins.LoginRequiredMixin):
    def get(self, *args, **kwargs):
        profile = Profile.objects.filter(username=self.request.user)

        if not profile and self.request.user.is_authenticated:
            return redirect('create profile page')

        elif profile and self.request.user.is_authenticated:
            posts = {}
            profile = profile[0]
            got_posts = Post.objects.filter(Q(profile=self.request.user) | Q(public=True))

            if profile.friends:
                for friend in profile.friends.split(' '):
                    if friend.strip() != '':
                        creator = NickstagramUser.objects.filter(pk=int(friend))
                    else:
                        continue

                    if creator:
                        creator = creator[0]
                    else:
                        continue

                    got_posts = got_posts | Post.objects.filter(profile=creator)

            for post in got_posts:
                likes = Likes.objects.filter(post_id=post.pk)
                posts[post] = {'comments': Comments.objects.filter(post_id=post.pk)[::-1],
                               'likes': len(Likes.objects.filter(post_id=post.pk)),
                               'user_likes': False}

                for like in likes:
                    if like.creator.pk == profile.pk:
                        posts[post]['user_likes'] = True

        else:
            posts = {}

        context = {
            'profile': profile,
            'posts': posts,
        }
        return render(self.request, 'index.html', context)

    @staticmethod
    def post(request, *args, **kwargs):
        post_pk = request.POST.get('post-pk')
        post = Post.objects.get(pk=post_pk)
        profile = Profile.objects.get(pk=request.user.pk)
        likes = Likes.objects.filter(post_id=post.pk)

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
                Q(first_name__contains=query) | Q(last_name__contains=query) | Q(username__contains=query) &
                ~Q(pk=self.request.user.pk)
            )

            result = post_result
        else:
            result = None

        return result

    def post(self, *args, **kwargs):
        profile = Profile.objects.get(pk=self.request.user.pk)
        person_to_follow = self.request.POST.get('person-to-follow')

        if profile.friends:
            if person_to_follow not in profile.friends.split(' '):
                profile.friends += person_to_follow + ' '
                profile.save()
        else:
            profile.friends = person_to_follow + ' '
            profile.save()

        return redirect('search page')
