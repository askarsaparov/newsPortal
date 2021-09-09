from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from news.models import Comment, Category, News


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control',}),
        }

class AdminCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class AdminNewsUpdate(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'
