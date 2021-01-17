from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views import generic
from django.urls import reverse_lazy
from .models import Post

from django.contrib.auth import get_user_model
user = get_user_model()


class CreatePost(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ('title', 'message', 'picture', 'group')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class PostList(generic.ListView):
    model = Post


class PostDetail(generic.DetailView):
    model = Post

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))


class DeletePost(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy("index")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)


class UserPosts(generic.ListView):
    model = Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        try:
            self.post_user = user.objects.prefetch_related("posts").get(
                username__iexact=self.kwargs.get("username")
            )
        except user.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context





