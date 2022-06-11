from django.contrib.auth.forms import UserCreationForm,UserChangeForm,UsernameField
from django.contrib.auth.models import User
from django import forms
from .models import Contact,Post,Comment


class UserForm(UserCreationForm):
    password2 = forms.CharField(label='Re-Enter Password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name','last_name','username']
        widgets = {
            'first_name':forms.TextInput(attrs={'required':True,'autofocus':True}),
            'last_name':forms.TextInput(attrs={'required':True,'autofocus':True}),
            # 'last_name':forms.CharField(required=True),
            # 'name':forms.CharField(required=True),
        }

class ContactForm(forms.ModelForm):
    desc = forms.CharField(min_length=5, max_length=100, label='Your Message', widget=forms.Textarea(attrs={'rows':"4",}))
    class Meta:
        model = Contact
        fields = '__all__'
        
class UserProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['first_name','last_name','username']
        labels = {'email':'Email'}


class AdminProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = '__all__'
        labels = {'email':'Email'}


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # exclude = ('author',)
        fields = ['title','desc']
        labels = {
            'desc':'Text',
        }

class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'cols':2,'rows':2}))
    class Meta:
        model = Comment
        fields = ['text']