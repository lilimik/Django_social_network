from django.contrib.auth import get_user_model

from posts.models import Post

User = get_user_model()


def get_post_with_owner(pk):
    return Post.objects.annotate_likes_comments().get(id=pk)


def update_post_data(form, pk):
    post = Post.objects.get(id=pk)
    text = form.cleaned_data['text']

    post.text = text
    post.save()
