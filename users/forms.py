from django import forms

from users.models import CustomUser


class SignInForm(forms.Form):
    email = forms.EmailField(label='Почта', required=True)
    password = forms.CharField(label='Пароль', required=True)


class SignUpForm(forms.Form):
    email = forms.EmailField(label='Почта', required=True)
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    patronymic = forms.CharField(label='Отчество')
    password1 = forms.CharField(label='Пароль', required=True)
    password2 = forms.CharField(label='Пароль', required=True)


class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(label='Пароль', required=True)
    password2 = forms.CharField(label='Пароль', required=True)


class UploadFileForm(forms.Form):
    file = forms.FileField()


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['file']
