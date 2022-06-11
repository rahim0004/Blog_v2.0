from django.contrib import admin
from .models import Post,Contact,Comment
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','author','title']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id','name']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','author','text']