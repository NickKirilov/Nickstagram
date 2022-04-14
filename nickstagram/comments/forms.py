from django import forms
from nickstagram.comments.models import Comments


class CommentPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for value, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control '})
            field.widget.attrs['placeholder'] = 'Comment...'

    class Meta:
        model = Comments
        fields = ('text',)


class EditCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for value, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control '})
            field.widget.attrs['placeholder'] = 'Comment...'

    class Meta:
        model = Comments
        fields = ('text',)
