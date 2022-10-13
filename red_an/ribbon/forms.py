from django import forms
from django.forms import ModelForm
from .models import Section, SectionPost, Comment
from django.contrib import admin
from users.forms import CustomClearableFileInput


class SectionCreateForm(ModelForm):
    image = forms.ImageField(widget=CustomClearableFileInput, required=True)
    banner = forms.ImageField(widget=CustomClearableFileInput, required=False)

    class Meta:
        model = Section
        fields = '__all__'
        exclude = ['owner']
        widgets = {
            'banner_color': forms.TextInput(attrs={
                'type': 'color',
            })
        }

    def __init__(self, *args, **kwargs):
        super(SectionCreateForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'input',
            'placeholder': 'Section Name',
        })
        self.fields['short_description'].widget.attrs.update({
            'class': 'input',
            'placeholder': 'Short description of section',
        })
        self.fields['description'].widget.attrs.update({
            'class': 'input',
            'placeholder': 'Full description of section',
        })


class SectionCreateFormAdmin(admin.ModelAdmin):
    form = SectionCreateForm


class PostCreateForm(ModelForm):
    image = forms.ImageField(widget=CustomClearableFileInput, required=False)

    class Meta:
        model = SectionPost
        fields = '__all__'
        exclude = ['section_id', 'profile_id', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={
                'resize': 'vertical',
            })
        }

    def __init__(self, *args, **kwargs):
        super(PostCreateForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'input',
            'placeholder': 'Post title',
        })
        self.fields['content'].widget.attrs.update({
            'class': 'input',
            'placeholder': 'Post text content, up to 4000 symbols',
            'style': 'resize: vertical;',
        })


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 6,
            })
        }
        exclude = ['profile_id', 'section_post_id']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({
            'class': 'input',
            'placeholder': 'Comment text, up to 500 symbols',
            'style': 'resize: none;'
        })
        self.fields['text'].label = 'Add new comment'
