import uuid

from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.decorators.cache import cache_page

from posts.models import Post
from users.forms import SignInForm, SignUpForm, ChangePasswordForm, UploadFileForm, FileUploadForm
from users.models import PasswordToken

from users.service import register_user, authorization_user, get_user_by_id, get_subscribed_status, get_follows_posts, \
    annotate_follows_posts_count, follow_user, unfollow_user, check_insta_link, handle_uploaded_file
from users.decorators import not_authorized
from users.service import change_password

User = get_user_model()


@cache_page(15)
def main_view(request):
    # time.sleep(5)
    # posts = Post.objects.all().order_by('date_of_creation')
    # if request.user.is_authenticated:
    #     annotate_follows_posts_count(request.user)
    #     posts = get_follows_posts(request.user).order_by('-date_of_creation')
    return render(request, 'users/main_page.html', {
        # 'posts': posts,
    })


@not_authorized
def sign_up_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data['password1']
            check_password = form.cleaned_data['password2']

            if password == check_password:
                register_user(form)
                return redirect('signIn')

    return render(request, 'users/sign_up.html')


class SignIn(View):
    template_name = 'users/sign_in.html'
    form = SignInForm

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = self.form(request.POST)

        if form.is_valid():
            authorization_user(request, form)
            return redirect('main')

        form.add_error('email', 'Неправильный логин или пароль')

        return render(request, self.template_name, {
            'form': form,
        })


@login_required
def logout_view(request):
    logout(request)
    return redirect('main')


class Profile(View):
    template_name = 'users/profile.html'

    def get(self, request, pk):
        profile_user = annotate_follows_posts_count(get_user_by_id(pk))
        posts = Post.objects.filter(owner=profile_user)
        subscribed = get_subscribed_status(profile_user, request.user)
        return render(request, self.template_name, {
            'subscribed': subscribed,
            'profile_user': profile_user,
            'posts': posts,
        })


class Follow(View):

    def get(self, request, pk):
        follow_user(request.user, pk)
        return redirect('profile', pk)

    def post(self, request, pk):
        unfollow_user(request.user, pk)
        return redirect('profile', pk)


def user_not_found_404(request, exception):
    print('sdfsdfsdfs')
    return render(request, 'users/404.html', status=404)


def instagram_view(request, link):
    if check_insta_link(link):
        return redirect(f'https://www.instagram.com/{link}')
    return redirect('main')


class ProfileSettingsView(View):
    template_name = 'users/profile_settings_page.html'
    form = ChangePasswordForm

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = self.form(request.POST)

        if form.is_valid():
            password = form.cleaned_data['password1']
            if password == form.cleaned_data['password2']:
                token = uuid.uuid1()
                absolute_uri = request.build_absolute_uri(reverse('password_token', args=(token,)))
                request.user.set_password(password)
                change_password(
                    token,
                    request.user,
                    absolute_uri,
                    request.user.password,
                )
                return redirect('main')
        return redirect('profile_settings')


class ChangePasswordView(View):
    template_name = 'users/password_token_page.html'

    def get(self, request, token):
        password_token = PasswordToken.objects.filter(token=token).first()
        token_status = False
        if password_token is not None and password_token.validity_status:
            password = password_token.hash_password
            password_token.validity_status = False
            password_token.save()
            request.user.password = password
            request.user.save()
            token_status = True
        return render(request, self.template_name, {
            'token': token,
            'token_status': token_status,
        })


@login_required
def upload_file(request):

    if request.method == 'POST':
        print('вьюха')
        form = FileUploadForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('files_upload_success')
    else:
        form = UploadFileForm()
    return render(request, 'users/file_upload_page.html', {
        'form': form
    })


def files_upload_success(request):
    return render(request, 'users/files_upload_success.html')