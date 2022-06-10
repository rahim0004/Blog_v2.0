from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('add/post/', views.add_post, name='add_post'),
    path('post-detail/<int:pk>/', views.post_detail, name='detail'),
    path('post-edit/<int:pk>/', views.post_edit, name='update'),
    path('post-delete/<int:pk>/', views.post_delete, name='delete'),
    path('search', views.search, name='search'),
]
