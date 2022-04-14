from django import forms

from nickstagram.web.models import Comments


class CommentPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for value, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control '})
            field.widget.attrs['placeholder'] = 'Comment...'

    class Meta:
        model = Comments
        fields = ('text',)
