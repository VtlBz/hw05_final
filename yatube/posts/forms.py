from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('text', 'group', 'image')

    def clean_text(self):
        text = self.cleaned_data['text']

        if len(text) < 2:
            raise forms.ValidationError(
                'Текст сообщения должен содержать больше одного символа'
            )

        return text


class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ('text',)

    def clean_text(self):
        text = self.cleaned_data['text']

        if len(text) < 2:
            raise forms.ValidationError(
                'Текст комментария должен содержать больше одного символа'
            )

        return text
