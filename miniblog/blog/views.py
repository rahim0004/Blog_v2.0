from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from .models import Post,Comment
from .forms import UserForm,ContactForm,AdminProfileForm,UserProfileForm,PostForm,CommentForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required 

# Create your views here.
def home(request):
    post = Post.objects.all()
    comment = Comment.objects.all()
    return render(request,'blog/home.html',{'posts':post,'home':'active bb','hsr':'Recent Posts','comments':comment})

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
            posts = Post.objects.filter(author=request.user)
            gps = request.user.groups.all()
            if request.method == 'POST':
                if request.user.is_superuser:
                    form = AdminProfileForm(request.POST, instance=request.user)
                else:
                    
                    form = UserProfileForm(request.POST, instance=request.user)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('/dashboard/')
            else:
                if request.user.is_superuser:
                    form = AdminProfileForm(instance=request.user)
                else:
                    form = UserProfileForm(instance=request.user)
            return render(request,'blog/dashboard.html',{'form':form,'dashboard':'active bb','post':posts,'gps':gps})
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
        if request.user.has_perm('blog.add_post'):
            if request.method == 'POST':
                form = PostForm(request.POST or None)
                if form.is_valid():
                    form.instance.author = request.user
                    form.save()
                    return HttpResponseRedirect('/dashboard/')
            else:
                form = PostForm()
            return render(request,'blog/add_post.html',{'form':form,'heading':'New Post','bn':'Post','ttl':'Add'})


def post_detail(request, pk):
    # cmt = Comment.objects.filter(post=pk)
    posts = Post.objects.get(id=pk)
    cmt = posts.comments.all()
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentForm(request.POST or None)
            if form.is_valid():
                comment= form.save(commit=False)
                comment.post = posts
                comment.author = request.user
                comment.save() 
                return redirect(to='blog:detail', pk=pk)
        else:
            form = CommentForm()
    else:
        form = {}
    return render(request,'blog/detail.html',{'posts':posts,'form':form,'cmt':cmt})

@login_required
def post_edit(request,pk):
    post = Post.objects.get(id=pk)
    form = PostForm(request.POST or None, instance=post)
    if request.user == post.author:
        if request.method == 'POST':
                form.save()
                return HttpResponseRedirect('/')
        else:
            return render(request,'blog/add_post.html',{'forms':form,'heading':'Edit Post','bn':'Save','ttl':'Edit','post':post})
    else:
        return HttpResponseRedirect('/')

# @login_required
# def post_edit(request,pk):
#     if request.user == post.author:
#         if request.method == 'POST':
#             post = get_object_or_404(Post, id=pk)
#             form = PostForm(request.POST or None, instance=post)
#             form.save()
#             return HttpResponseRedirect('/')
#         else:
#             return render(request,'blog/add_post.html',{'form':form,'heading':'Edit Post','bn':'Save','ttl':'Edit'})
#     else:
#         return HttpResponseRedirect('/')





@login_required
def post_delete(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:
        post = Post.objects.get(id=pk)
        post.delete()
        return HttpResponseRedirect('/')


def search(request):
    if request.method == 'GET':
        data = request.GET.get('name')
        if len(data) != 0:
            posts = Post.objects.filter(desc__contains=data).all()
            count = posts.count()
            return render(request,'blog/home.html',{'posts':posts,'home':'active bb','hsr':'Searched Results','count':count})
        else:
            return HttpResponseRedirect('/')