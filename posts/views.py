from django.shortcuts import render, redirect
from django.views import View

from posts.forms import PostRefactorForm
from posts.service import get_post_with_owner, update_post_data


class PostPage(View):
    template_name = 'posts/post.html'
    form = PostRefactorForm

    def get(self, request, pk):
        post = get_post_with_owner(pk)
        return render(request, self.template_name, {
            "post": post,
        })

    def post(self, request, pk):
        form = PostRefactorForm(request.POST)

        if form.is_valid():
            update_post_data(form, pk)

        return redirect('post_page', pk)
