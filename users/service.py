from datetime import datetime

from django.contrib.auth import get_user_model, authenticate, login
from django.db.models import Subquery, Q
from django.http import Http404
from django.shortcuts import get_object_or_404

from posts.models import Post
from users.models import Follows, PasswordToken
from users.tasks import change_password_task

User = get_user_model()


def register_user(form):
    email = form.cleaned_data['email']
    password = form.cleaned_data['password1']
    first_name = form.cleaned_data['first_name']
    last_name = form.cleaned_data['last_name']
    patronymic = form.cleaned_data['patronymic']

    user = User()
    user.email = email
    user.set_password(password)
    user.first_name = first_name
    user.last_name = last_name
    user.patronymic = patronymic

    user.save()


def authorization_user(request, form):
    email = form.cleaned_data['email']
    password = form.cleaned_data['password']

    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)


def get_user_by_id(pk):
    try:
        user = get_object_or_404(User, id=pk)
    except User.DoesNotExist:
        raise Http404
    return user


def get_subscribed_status(profile_user: User, user: User) -> bool:
    return Follows.objects.filter(
        user_subscribed=profile_user,
        user_signer=user
    ).exists()


def get_follows_posts(user: User):
    follows = Follows.objects.filter(user_signer_id=user.id)
    posts = Post.objects.filter(
        id__in=Subquery(follows.values('user_subscribed__posts'))
    )
    return posts


def annotate_follows_posts_count(user: User):
    return User.objects.annotate_follows_followers_count().get(id=user.id)


def follow_user(user_signer: User, pk):
    user_subscribed = get_user_by_id(pk)
    Follows.objects.create(user_subscribed=user_subscribed, user_signer=user_signer)


def unfollow_user(user_signer: User, pk):
    user_subscribed = get_user_by_id(pk)
    follow = Follows.objects.filter(user_subscribed=user_subscribed, user_signer=user_signer)
    follow.delete()


def check_insta_link(link):
    date_of_creation_limit = datetime.date(2005, 1, 1)
    result = User.objects.filter(
        Q(birthday__lte=date_of_creation_limit) | Q(phone_number__startswith='79')
    ).filter(
        instagram=link
    ).exists()
    return result


def change_password(token, user, token_url, hash_password):
    password_token = PasswordToken.objects.filter(user=user).first()
    if password_token is not None:
        password_token.token = token
        password_token.hash_password = hash_password
        password_token.date_of_updating = datetime.now()
        password_token.validity_status = True
        password_token.save()
    else:
        PasswordToken.objects.create(
            token=token,
            user=user,
            hash_password=hash_password,
        )
    change_password_task(user.email, token_url)


def handle_uploaded_file(file, file_name):
    print('Сервис')
    with open(f'../twitter/static/images/{file_name}.png', 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
