from django.urls import path
from . import views
from .views import cipher_share

urlpatterns = [
    path('', views.home, name="home"),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('profile/followers/<int:pk>', views.followers, name='followers'),
    path('profile/follows/<int:pk>', views.follows, name='follows'),
    path('login/', views.login_user, name= 'login'),
    path('logout/', views.logout_user, name= 'logout'),
    path('register/', views.register_user, name= 'register'),
    path('update_user/', views.update_user, name='update_user'),
    path('cipher_like/<int:pk>', views.cipher_like, name = "cipher_like"),
    path('cipher_share/<int:pk>', views.cipher_share, name = "cipher_share"),
    path('unfollow/<int:pk>', views.unfollow, name = "unfollow"),
    path('follow/<int:pk>', views.follow, name = "follow"),
    path('delete_cipher/<int:pk>', views.delete_cipher, name = "delete_cipher"),
    path('edit_cipher/<int:pk>', views.edit_cipher, name = "edit_cipher"),
    path('search/', views.search, name= 'search'),
    path('search_user/', views.search_user, name= 'search_user'),
]
