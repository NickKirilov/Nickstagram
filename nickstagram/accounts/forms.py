from django import forms
from django.contrib.auth import forms as auth_forms

from nickstagram.accounts.models import Profile, NickstagramUser
from nickstagram.accounts.validators import validate_date_of_birth


class RegistrationForm(auth_forms.UserCreationForm):
    date_of_birth = forms.DateField(
        validators=(
            validate_date_of_birth,
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for value, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs['placeholder'] = field.label
            if value == 'date_of_birth':
                field.widget.input_type = 'date'

    class Meta:
        model = NickstagramUser
        fields = ('username', 'password1', 'password2', 'date_of_birth',)


class CreateProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for value, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control '})
            field.widget.attrs['placeholder'] = field.label
            if value == 'date_of_birth':
                field.widget.input_type = 'date'

    class Meta:
        model = Profile
        fields = ('date_of_birth', 'gender', 'image', 'email', 'first_name', 'last_name')


class EditProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for value, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control '})
            field.widget.attrs['placeholder'] = field.label

    class Meta:
        model = Profile
        fields = ('gender', 'image', 'email', 'first_name', 'last_name')


class DeleteProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('gender', 'image', 'email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = NickstagramUser.objects.get(username=self.instance.username)
        self.instance.delete()
        user.delete()
        return self.instance


class LoginForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for value, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs['placeholder'] = field.label
