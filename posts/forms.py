from django import forms


class PostRefactorForm(forms.Form):
    text = forms.CharField(label='Текст', required=True)