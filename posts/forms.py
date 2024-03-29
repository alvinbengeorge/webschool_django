from django import forms
from .models import Post

class PostForm(forms.ModelForm):

    template_name = 'posts/forms/post_create_form_snippet.html'
    class Meta:
        model = Post
        exclude = ('created_by',)

    def save(self, user, commit=True):
        post = super(PostForm, self).save(commit=False)
        post.created_by = user
        print("groups:",self.cleaned_data['groups'])
        if commit:
            post.save()
        return post