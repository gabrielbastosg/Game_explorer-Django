from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),   
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),
    path('register/', views.register, name='register'),
    path('add_favorite/<int:game_id>/', views.add_favorite, name='add_favorite'),
    path('favorites/', views.favorites, name='favorites'),
    path('remove_favorite/<int:game_id>/', views.remove_favorite, name='remove_favorite'),
    path('set_status/<int:game_id>/', views.set_status, name='set_status'),
    path('minha-estante/', views.my_shelf, name='my_shelf'),
    path('set_review/<int:game_id>/', views.set_review, name='set_review'),
    path('delete_review/<int:game_id>/', views.delete_review, name='delete_review'), 
    ]