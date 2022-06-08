#community_page/forms.py

from django import forms
from .models import Post

class PostWriteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostWriteForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = '제목'
        self.fields['title'].widget.attrs.update({
            'placeholder': '제목을 입력해주세요.',
            'class': 'form-control',
            'autofocus': True,
        })

    class Meta:
        model = Post
        fields = ['title', 'content']