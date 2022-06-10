from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import Post
from .forms import UserForm,ContactForm,AdminProfileForm,UserProfileForm,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required 
# Create your views here.
def home(request):
    post = Post.objects.all()
    return render(request,'blog/home.html',{'posts':post,'home':'active bb','hsr':'Recent Posts'})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST or None)
        if form.is_valid():
            form.save()
            form = ContactForm()
    else:
        form = ContactForm()
    return render(request,'blog/contact.html',{'form':form,'contact':'active bb'})

def about(request):
    return render(request,'blog/about.html',{'about':'active bb'})

def user_signup(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = UserForm(request.POST or None)
            if form.is_valid():
                user = form.save()
                group = Group.objects.get(name='Member')
                user.groups.add(group)
                messages.success(request,'Accont Created Successfully. log in with username and password')
        else:
            form = UserForm()
        return render(request,'blog/signup.html',{'form':form,'signup':'active bb'})
    else:
        return HttpResponseRedirect('/dashboard/')

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request,user)
                    return render(request,'blog/dashboard.html',{'dashboard':'active bb'})
        else:
            form = AuthenticationForm()
        return render(request,'blog/login.html',{'form':form,'login':'active bb'})
    else:
        return HttpResponseRedirect('/dashboard/')

@login_required
def user_dashboard(request):
    if request.user.is_authenticated:
        if request.user.has_perm('blog.add_post'):
            posts = Post.objects.all()
            if request.method == 'POST':
                if request.user.is_superuser:
                    form = AdminProfileForm(request.POST, instance=request.user)
                    users = User.objects.all()
                else:
                    users = None
                    form = UserProfileForm(request.POST, instance=request.user)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('/dashboard/')
            else:
                if request.user.is_superuser:
                    form = AdminProfileForm(instance=request.user)
                    users = User.objects.all()
                else:
                    users = None
                    form = UserProfileForm(instance=request.user)
            return render(request,'blog/dashboard.html',{'form':form,'users':users,'dashboard':'active bb','post':posts})
        else:
            return render(request,'blog/dashboard.html') 
    else:
        return HttpResponseRedirect('/login/')

@login_required
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')

@login_required
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST or None)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/')
        else:
            form = PostForm()
        return render(request,'blog/add_post.html',{'form':form,'heading':'New Post','bn':'Post','ttl':'Add'})


def post_detail(request, pk):
    posts = Post.objects.get(id=pk)
    return render(request,'blog/detail.html',{'posts':posts})

@login_required
def post_edit(request,pk):
    post = Post.objects.get(id=pk)
    form = PostForm(request.POST or None, instance=post)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        return render(request,'blog/add_post.html',{'form':form,'heading':'Edit Post','bn':'Save','ttl':'Edit'})

@login_required
def post_delete(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:
        post = Post.objects.get(id=pk)
        post.delete()
        return HttpResponseRedirect('/')


def search(request):
    if request.method == 'GET':
        data = request.GET.get('name')
        posts = Post.objects.filter(desc__contains=data).all()
        count = posts.count()
        return render(request,'blog/home.html',{'posts':posts,'home':'active bb','hsr':'Searched Results','count':count})