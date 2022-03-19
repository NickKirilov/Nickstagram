from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from nickstagram.web.models import Post
from nickstagram.accounts.validators import validate_date_of_birth


class CreatePostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for value, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control '})
            field.widget.attrs['placeholder'] = field.label
            if value == 'public':
                field.widget.attrs.update({'class': 'form-check-input'})

    class Meta:
        model = Post
        fields = ('description', 'image', 'public')
