from django.urls import path

from hatch_blog_posts import views

urlpatterns = [
    path('ping/', views.get_ping, name='get_ping'),
    path('posts/', views.get_posts, name='get_posts'),
    # path('ping/', views.ping, name='ping'),
]

