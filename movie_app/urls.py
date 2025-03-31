from django.urls import path
from . import views

urlpatterns = [
    path('',views.base,name='base'),
    path('home',views.home,name='home'),
    path('user_register',views.user_register,name='user_register'),
    path('user_login',views.user_login,name='user_login'),
    path('user_logout',views.user_logout,name='user_logout'),
    path('profile',views.profile,name='profile'),
    
    path('base_movie_list',views.base_movie_list,name='base_movie_list'),
    path('movie_list',views.movie_list,name='movie_list'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('edit_movie/<int:movie_id>/', views.edit_movie, name='edit_movie'),
    path('delete_movie/<int:movie_id>/', views.delete_movie, name='delete_movie'),
    path('add_review/<int:movie_id>/', views.add_review, name='add_review'),
    path('search_movie', views.search_movie, name='search_movie'),
    path('favorite_list', views.favorite_list, name='favorite_list'),
    path('delete_fav_list/<int:movie_id>/', views.delete_fav_list, name='delete_fav_list'),
    path('toggle_favorite/<int:movie_id>/', views.toggle_favorite, name='toggle_favorite'),

]
