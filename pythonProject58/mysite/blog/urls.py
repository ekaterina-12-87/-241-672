from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
 # представления поста
 path('', views.home_view, name='home_view'),
 path('room/<int:room_id>/', views.room_detail, name='room_detail'),
 path('hotel/<int:hotel_id>/', views.hotel_detail, name='hotel_detail')
]