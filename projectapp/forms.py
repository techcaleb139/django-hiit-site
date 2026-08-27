from django import forms
from projectapp.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        # fields = ["name", "body"]