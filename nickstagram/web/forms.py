from django import forms
from django.urls import reverse

from nickstagram.web.models import Post, Comments


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
        fields = ('title', 'description', 'image', 'public')


class EditPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for value, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control '})
            field.widget.attrs['placeholder'] = field.label
            if value == 'public':
                field.widget.attrs.update({'class': 'form-check-input'})

    class Meta:
        model = Post
        fields = ('title', 'description', 'image', 'public')


class DeletePostForm(forms.ModelForm):

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = Post
        fields = ()


class CommentPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for value, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control '})
            field.widget.attrs['placeholder'] = 'Comment...'

    class Meta:
        model = Comments
        fields = ('text',)
