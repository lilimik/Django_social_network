"""twitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth.decorators import login_required
from django.urls import path, re_path

from users.decorators import not_authorized
from users.views import logout_view, sign_up_view, main_view, Profile, SignIn, Follow, user_not_found_404, \
    instagram_view, ProfileSettingsView, ChangePasswordView, upload_file, files_upload_success

urlpatterns = [
    path('', main_view, name='main'),
    path('signIn/', not_authorized(SignIn.as_view()), name='signIn'),
    path('logout/', logout_view, name='logout'),
    path('signUp/', sign_up_view, name='signUp'),
    path('users/<int:pk>', login_required(Profile.as_view()), name='profile'),
    path('follow/<int:pk>', login_required(Follow.as_view()), name='follow'),
    re_path(r'^instagram/(?P<link>.*)', instagram_view, name='instagram'),
    path('profile/', login_required(ProfileSettingsView.as_view()), name='profile_settings'),
    re_path('password/(?P<token>.*)/', login_required(ChangePasswordView.as_view()), name='password_token'),
    path('files_upload/', upload_file, name='file_upload'),
    path('files_upload_success', files_upload_success, name='files_upload_success'),
]

handler404 = user_not_found_404
